"""
parking_rule.py
Orchestrator for illegal parking violation detection.

Follows the same pattern as intersection_rule.py and wrongside_rule.py:
  1. Accept tracked-object payload
  2. Filter to vehicle tracks
  3. Load camera parking zone config (mocked)
  4. For each vehicle, check if it is inside a parking zone
  5. Compute dwell time and evaluate against zone thresholds
  6. Build violation candidates
  7. Persist candidates (mocked DB)
  8. Publish downstream event (mocked queue)
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from app.services.parking_zone_config import get_parking_zone_config, find_vehicle_zones
from app.services.dwell_time import (
    is_vehicle_stationary,
    compute_dwell_time,
    exceeds_dwell_threshold,
    compute_parking_confidence,
)
from app.services.parking_candidate import build_parking_candidate

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Vehicle class names relevant for parking violations
VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle", "auto", "van", "tempo"}


def _extract_vehicle_tracks(tracked_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filters tracked objects to only include vehicles.
    Pedestrians, bicycles, and animals are excluded.
    """
    vehicles = [
        t for t in tracked_objects
        if t.get("class_name", "").lower() in VEHICLE_CLASSES
    ]
    logger.info("Filtered %d vehicles from %d tracked objects", len(vehicles), len(tracked_objects))
    return vehicles


def _get_vehicle_position(track: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    """
    Extracts the vehicle's current position from the tracked object.

    Tries bbox_center first, then falls back to computing center from bbox.
    """
    center = track.get("bbox_center")
    if center:
        return tuple(center)

    bbox = track.get("bbox")
    if bbox and isinstance(bbox, dict):
        cx = (bbox.get("x1", 0) + bbox.get("x2", 0)) / 2
        cy = (bbox.get("y1", 0) + bbox.get("y2", 0)) / 2
        return (cx, cy)

    return None


def _evaluate_vehicle_parking(
    track: Dict[str, Any],
    zones: List[Dict[str, Any]],
    frame_id: str,
    current_timestamp: str,
) -> List[Dict[str, Any]]:
    """
    Evaluates a single vehicle track for illegal parking violations.

    A vehicle can violate multiple zones simultaneously (e.g., parked
    in an area that is both a no-parking zone and a fire-hydrant zone).

    Steps:
      1. Get vehicle position
      2. Find which parking zones the vehicle is inside
      3. Check if vehicle is stationary
      4. Compute dwell time
      5. Evaluate dwell against zone thresholds
      6. Build violation candidates for each violated zone

    Returns a list of violation candidate dicts (may be empty).
    """
    track_id = track.get("track_id", "unknown")
    position = _get_vehicle_position(track)

    if position is None:
        return []

    # Find all zones this vehicle is inside
    matched_zones = find_vehicle_zones(position, zones)
    if not matched_zones:
        return []

    # Check if vehicle is stationary
    motion = track.get("motion_vector", (0, 0))
    stationary = is_vehicle_stationary(tuple(motion))

    if not stationary:
        # Moving vehicles are not parking violations
        return []

    # Compute dwell time
    dwell_seconds = compute_dwell_time(track, current_timestamp)

    candidates = []
    for zone in matched_zones:
        zone_id = zone.get("zone_id", "unknown")
        zone_type = zone.get("zone_type", "NO_PARKING")
        max_dwell = zone.get("max_dwell_seconds", 0)
        zone_desc = zone.get("description")

        # Check threshold
        if not exceeds_dwell_threshold(dwell_seconds, max_dwell, zone_type):
            continue

        # Compute confidence
        confidence = compute_parking_confidence(
            dwell_seconds, max_dwell, zone_type, stationary
        )

        logger.info(
            "Illegal parking detected | track_id=%s | zone=%s (%s) | "
            "dwell=%.1fs | max=%.1fs | confidence=%.3f",
            track_id, zone_id, zone_type, dwell_seconds, max_dwell, confidence,
        )

        candidate = build_parking_candidate(
            track_id=track_id,
            frame_id=frame_id,
            confidence=confidence,
            dwell_time_seconds=dwell_seconds,
            zone_id=zone_id,
            zone_type=zone_type,
            zone_description=zone_desc,
            max_dwell_seconds=max_dwell,
            vehicle_position=position,
            entry_timestamp=track.get("first_seen_timestamp"),
            current_timestamp=current_timestamp,
        )
        candidates.append(candidate)

    return candidates


async def run_parking_rule(request_data: Any) -> Dict[str, Any]:
    """
    Full illegal parking rule orchestrator:
      1. Extract vehicle tracks from tracked objects
      2. Load parking zone config for camera
      3. Evaluate each vehicle for illegal parking
      4. Build violation candidates
      5. Persist violation candidates (Mocked DB)
      6. Publish downstream event (Mocked Queue)

    Args:
        request_data: ParkingRuleRequest Pydantic model.

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
        logger.info("Frame %s: No vehicle tracks found — skipping parking rule", frame_id)
        return {
            "frame_id": frame_id,
            "rule": "ILLEGAL_PARKING",
            "vehicles_evaluated": 0,
            "violations": [],
            "queue_status": "none",
        }

    # 2. Load parking zone config
    zone_config = get_parking_zone_config(camera_id)
    zones = zone_config.get("zones", [])

    if not zones:
        logger.info("Frame %s: No parking zones configured for camera %s", frame_id, camera_id)
        return {
            "frame_id": frame_id,
            "rule": "ILLEGAL_PARKING",
            "vehicles_evaluated": len(vehicle_tracks),
            "violations": [],
            "queue_status": "none",
        }

    # 3 & 4. Evaluate each vehicle
    candidates: List[Dict[str, Any]] = []
    for track in vehicle_tracks:
        vehicle_candidates = _evaluate_vehicle_parking(track, zones, frame_id, timestamp)
        for c in vehicle_candidates:
            c["camera_id"] = camera_id
            c["timestamp"] = timestamp
        candidates.extend(vehicle_candidates)

    logger.info(
        "Frame %s: Evaluated %d vehicles across %d zones, found %d parking violations",
        frame_id, len(vehicle_tracks), len(zones), len(candidates),
    )

    # 5. Persist Violation Candidates (MOCKED DB)
    # db = next(get_db())
    # # Save each candidate to the violation_candidates table
    # db.commit()
    logger.info("Saved %d parking violation candidates to database (Mocked)", len(candidates))

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
        logger.info("Frame %s has no parking violations. Pipeline terminates here.", frame_id)

    return {
        "frame_id": frame_id,
        "rule": "ILLEGAL_PARKING",
        "vehicles_evaluated": len(vehicle_tracks),
        "zones_checked": len(zones),
        "violations": candidates,
        "queue_status": "published" if candidates else "none",
    }
