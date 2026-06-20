"""
wrongside_rule.py
Orchestrator for wrong-side driving violation detection.

Follows the same pattern as intersection_rule.py:
  1. Accept tracked-object payload
  2. Filter to vehicle tracks (car, truck, bus, motorcycle, auto)
  3. Load camera lane config (mocked)
  4. Compute vehicle direction from trajectory
  5. Determine which lane the vehicle is in
  6. Compare vehicle direction against allowed lane direction
  7. Build violation candidates for wrong-side vehicles
  8. Persist candidates (mocked DB)
  9. Publish downstream event (mocked queue)
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from app.services.lane_config import get_lane_config, find_vehicle_lane
from app.services.direction import (
    compute_direction_vector,
    compute_average_direction,
    compute_heading_angle,
    is_wrong_direction,
    angle_between_vectors,
    compute_direction_confidence,
)
from app.services.wrongside_candidate import build_wrongside_candidate

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Vehicle class names that are relevant for wrong-side detection
VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle", "auto", "van", "tempo"}

# Minimum displacement (pixels) to consider a vehicle as moving
MIN_DISPLACEMENT = 5.0


def _extract_vehicle_tracks(tracked_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filters tracked objects to only include vehicles.
    Non-vehicle classes (person, bicycle, animal) are excluded.
    """
    vehicles = [
        t for t in tracked_objects
        if t.get("class_name", "").lower() in VEHICLE_CLASSES
    ]
    logger.info("Filtered %d vehicles from %d tracked objects", len(vehicles), len(tracked_objects))
    return vehicles


def _get_trajectory_points(track: Dict[str, Any]) -> List[Tuple[float, float]]:
    """
    Extracts positional trajectory from a tracked object.

    Supports two formats:
      1. TrackedObject with 'points' list (from common-schemas/tracking.py)
      2. TrackedObject with 'bbox_center' + 'motion_vector' (from rule-engine schemas)

    Returns a list of (x, y) tuples in chronological order.
    """
    # Format 1: points list (from tracking service output)
    points = track.get("points")
    if points and len(points) >= 2:
        return [(p.get("x", 0), p.get("y", 0)) for p in points]

    # Format 2: single bbox_center + motion_vector (infer previous position)
    center = track.get("bbox_center")
    motion = track.get("motion_vector")
    if center and motion:
        prev = (center[0] - motion[0], center[1] - motion[1])
        return [prev, tuple(center)]

    # Fallback: try to compute center from bbox
    bbox = track.get("bbox")
    if bbox and isinstance(bbox, dict):
        cx = (bbox.get("x1", 0) + bbox.get("x2", 0)) / 2
        cy = (bbox.get("y1", 0) + bbox.get("y2", 0)) / 2
        return [(cx, cy)]

    return []


def _get_displacement(trajectory: List[Tuple[float, float]]) -> float:
    """Compute total displacement from first to last point."""
    if len(trajectory) < 2:
        return 0.0
    dx = trajectory[-1][0] - trajectory[0][0]
    dy = trajectory[-1][1] - trajectory[0][1]
    return (dx * dx + dy * dy) ** 0.5


def _evaluate_vehicle(
    track: Dict[str, Any],
    lane_config: Dict[str, Any],
    frame_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Evaluates a single vehicle track for wrong-side driving.

    Steps:
      1. Extract trajectory and compute direction
      2. Find which lane the vehicle is in
      3. Get allowed direction for that lane (or default)
      4. Compare vehicle direction vs allowed direction
      5. Return a violation candidate if wrong-side detected

    Returns a violation candidate dict or None if no violation.
    """
    track_id = track.get("track_id", "unknown")
    trajectory = _get_trajectory_points(track)

    if len(trajectory) < 2:
        return None  # Need at least 2 points to compute direction

    # Skip stationary vehicles
    if _get_displacement(trajectory) < MIN_DISPLACEMENT:
        return None

    # 1. Compute vehicle direction
    vehicle_direction = compute_average_direction(trajectory)
    if vehicle_direction is None:
        return None

    vehicle_heading = compute_heading_angle(vehicle_direction)
    vehicle_position = trajectory[-1]  # current position

    # 2. Find which lane the vehicle is in
    lanes = lane_config.get("lanes", [])
    matched_lane = find_vehicle_lane(vehicle_position, lanes)

    # 3. Get allowed direction
    if matched_lane:
        allowed_direction = tuple(matched_lane["allowed_direction"])
        lane_id = matched_lane.get("lane_id")
        lane_desc = matched_lane.get("description")
    else:
        # Use camera default direction
        allowed_direction = tuple(lane_config.get("default_direction", (0.0, -1.0)))
        lane_id = None
        lane_desc = "No lane match — using camera default"

    # 4. Compare directions
    if not is_wrong_direction(vehicle_direction, allowed_direction):
        return None  # Vehicle is travelling in the correct direction

    angle_diff = angle_between_vectors(vehicle_direction, allowed_direction)
    confidence = compute_direction_confidence(vehicle_direction, allowed_direction)

    logger.info(
        "Wrong-side detected | track_id=%s | heading=%.1f° | allowed=%s | angle_diff=%.1f° | confidence=%.3f",
        track_id, vehicle_heading, allowed_direction, angle_diff, confidence,
    )

    # 5. Build violation candidate
    return build_wrongside_candidate(
        track_id=track_id,
        frame_id=frame_id,
        confidence=confidence,
        vehicle_direction=vehicle_direction,
        vehicle_heading_angle=vehicle_heading,
        allowed_direction=allowed_direction,
        direction_angle_diff=angle_diff,
        lane_id=lane_id,
        lane_description=lane_desc,
        vehicle_position=vehicle_position,
    )


async def run_wrongside_rule(request_data: Any) -> Dict[str, Any]:
    """
    Full wrong-side driving rule orchestrator:
      1. Extract vehicle tracks from tracked objects
      2. Load lane config for camera
      3. Evaluate each vehicle's direction against allowed lane direction
      4. Build violation candidates
      5. Persist violation candidates (Mocked DB)
      6. Publish downstream event (Mocked Queue)

    Args:
        request_data: WrongSideRuleRequest Pydantic model.

    Returns:
        Result dict with frame info, violation candidates, and queue status.
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp

    # Serialize Pydantic models to dicts for processing
    tracked_objects = [t.model_dump() for t in request_data.tracked_objects]

    # 1. Filter to vehicle tracks
    vehicle_tracks = _extract_vehicle_tracks(tracked_objects)

    if not vehicle_tracks:
        logger.info("Frame %s: No vehicle tracks found — skipping wrong-side rule", frame_id)
        return {
            "frame_id": frame_id,
            "rule": "WRONG_WAY",
            "vehicles_evaluated": 0,
            "violations": [],
            "queue_status": "none",
        }

    # 2. Load lane config
    lane_config = get_lane_config(camera_id)

    # 3 & 4. Evaluate each vehicle
    candidates: List[Dict[str, Any]] = []
    for track in vehicle_tracks:
        candidate = _evaluate_vehicle(track, lane_config, frame_id)
        if candidate:
            candidate["camera_id"] = camera_id
            candidate["timestamp"] = timestamp
            candidates.append(candidate)

    logger.info(
        "Frame %s: Evaluated %d vehicles, found %d wrong-side violations",
        frame_id, len(vehicle_tracks), len(candidates),
    )

    # 5. Persist Violation Candidates (MOCKED DB)
    # db = next(get_db())
    # # Save each candidate to the violation_candidates table
    # db.commit()
    logger.info("Saved %d wrong-side violation candidates to database (Mocked)", len(candidates))

    # 6. Publish to Downstream Queue (MOCKED)
    # In production, publish to the ANPR or incident-fusion queue if candidates exist.
    if candidates:
        downstream_job = {
            "frame_id": frame_id,
            "camera_id": camera_id,
            "timestamp": timestamp,
            "violations": candidates,
        }
        logger.info("Frame %s published to downstream fusion queue: %s", frame_id, downstream_job)
    else:
        logger.info("Frame %s has no wrong-side violations. Pipeline terminates here.", frame_id)

    return {
        "frame_id": frame_id,
        "rule": "WRONG_WAY",
        "vehicles_evaluated": len(vehicle_tracks),
        "violations": candidates,
        "queue_status": "published" if candidates else "none",
    }
