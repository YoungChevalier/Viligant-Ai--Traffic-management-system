"""
intersection_rule.py
Orchestrator for intersection violation detection (red-light + stop-line).

Follows the same pattern as helmet_rule.py:
  1. Accept tracked-object payload + signal state
  2. Filter to vehicle tracks (car, truck, bus, motorcycle, auto)
  3. Load camera zone config (mocked)
  4. Check each vehicle's trajectory against the stop-line
  5. Classify violations based on signal state
  6. Persist candidates (mocked DB)
  7. Publish downstream event (mocked queue)
"""

import logging
from typing import Any, Dict, List

from app.services.zone_config import get_zone_config
from app.services.geometry import has_crossed_line, compute_crossing_point
from app.services.intersection_candidate import build_intersection_candidate

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Vehicle class names that are relevant for intersection violations
VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle", "auto", "van", "tempo"}

# Confidence scoring constants
BASE_CONFIDENCE_RED_LIGHT = 0.92
BASE_CONFIDENCE_STOP_LINE = 0.78


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


def _get_trajectory_points(track: Dict[str, Any]) -> List[tuple]:
    """
    Extracts positional trajectory from a tracked object.

    Supports two formats:
      1. TrackedObject with 'points' list (from common-schemas/tracking.py)
      2. TrackedObject with 'bbox_center' (from rule-engine/api/schemas.py)

    Returns a list of (x, y) tuples in chronological order.
    """
    # Format 1: points list (from tracking service output)
    points = track.get("points")
    if points and len(points) >= 2:
        return [(p.get("x", 0), p.get("y", 0)) for p in points]

    # Format 2: single bbox_center (use with motion_vector to infer previous)
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
        # Without motion info, we can't determine crossing
        return [(cx, cy)]

    return []


def _evaluate_crossing(
    track: Dict[str, Any],
    stop_line: tuple,
    signal_state: str,
    frame_id: str,
) -> Dict[str, Any] | None:
    """
    Evaluates whether a single vehicle track crosses the stop-line,
    and classifies the violation based on signal state.

    Returns a violation candidate dict or None if no violation.
    """
    trajectory = _get_trajectory_points(track)
    if len(trajectory) < 2:
        return None  # Need at least 2 points to detect crossing

    line_start, line_end = stop_line
    track_id = track.get("track_id", "unknown")

    # Check each consecutive pair of points for crossing
    for i in range(len(trajectory) - 1):
        prev_pt = trajectory[i]
        curr_pt = trajectory[i + 1]

        if has_crossed_line(prev_pt, curr_pt, line_start, line_end):
            crossing = compute_crossing_point(prev_pt, curr_pt, line_start, line_end)

            # Classify based on signal state
            if signal_state == "RED":
                violation_type = "RED_LIGHT"
                confidence = BASE_CONFIDENCE_RED_LIGHT
            elif signal_state == "YELLOW":
                violation_type = "STOP_LINE"
                confidence = BASE_CONFIDENCE_STOP_LINE
            else:
                # GREEN — no violation
                return None

            logger.info(
                "Crossing detected | track_id=%s | signal=%s | type=%s | point=%s",
                track_id, signal_state, violation_type, crossing,
            )

            return build_intersection_candidate(
                track_id=track_id,
                frame_id=frame_id,
                violation_type=violation_type,
                confidence=confidence,
                crossing_point=crossing,
                prev_position=prev_pt,
                curr_position=curr_pt,
            )

    return None


async def run_intersection_rule(request_data: Any) -> Dict[str, Any]:
    """
    Full intersection rule orchestrator:
      1. Extract vehicle tracks from tracked objects
      2. Load zone config for camera
      3. Evaluate each vehicle for stop-line crossing
      4. Classify violations based on signal state
      5. Persist violation candidates (Mocked DB)
      6. Publish downstream event (Mocked Queue)

    Args:
        request_data: IntersectionRuleRequest Pydantic model.

    Returns:
        Result dict with frame info, violation candidates, and queue status.
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp
    signal_state = request_data.signal_state.upper()

    # Serialize Pydantic models to dicts for existing logic
    tracked_objects = [t.model_dump() for t in request_data.tracked_objects]

    # 1. Filter to vehicle tracks
    vehicle_tracks = _extract_vehicle_tracks(tracked_objects)

    if not vehicle_tracks:
        logger.info("Frame %s: No vehicle tracks found — skipping intersection rule", frame_id)
        return {
            "frame_id": frame_id,
            "rule": "INTERSECTION",
            "signal_state": signal_state,
            "vehicles_evaluated": 0,
            "violations": [],
            "queue_status": "none",
        }

    # 2. Load zone config
    zone_config = get_zone_config(camera_id)
    stop_line = zone_config["stop_line"]

    # 3 & 4. Evaluate each vehicle
    candidates: List[Dict[str, Any]] = []
    for track in vehicle_tracks:
        candidate = _evaluate_crossing(track, stop_line, signal_state, frame_id)
        if candidate:
            candidate["camera_id"] = camera_id
            candidate["timestamp"] = timestamp
            candidates.append(candidate)

    logger.info(
        "Frame %s: Evaluated %d vehicles, found %d intersection violations (signal=%s)",
        frame_id, len(vehicle_tracks), len(candidates), signal_state,
    )

    # 5. Persist Violation Candidates (MOCKED DB)
    # db = next(get_db())
    # # Save each candidate to the violation_candidates table
    # db.commit()
    logger.info("Saved %d intersection violation candidates to database (Mocked)", len(candidates))

    # 6. Publish to Downstream Queue (MOCKED)
    # In production, publish to the ANPR or incident-fusion queue if candidates exist.
    if candidates:
        downstream_job = {
            "frame_id": frame_id,
            "camera_id": camera_id,
            "timestamp": timestamp,
            "signal_state": signal_state,
            "violations": candidates,
        }
        logger.info("Frame %s published to downstream fusion queue: %s", frame_id, downstream_job)
    else:
        logger.info("Frame %s has no intersection violations. Pipeline terminates here.", frame_id)

    return {
        "frame_id": frame_id,
        "rule": "INTERSECTION",
        "signal_state": signal_state,
        "vehicles_evaluated": len(vehicle_tracks),
        "violations": candidates,
        "queue_status": "published" if candidates else "none",
    }
