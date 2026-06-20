"""
parking_candidate.py
Builds violation candidate dicts for illegal parking violations.

Follows the same pattern as intersection_candidate.py and wrongside_candidate.py.
"""

from typing import Any, Dict, Optional, Tuple


def build_parking_candidate(
    track_id: str,
    frame_id: str,
    confidence: float,
    dwell_time_seconds: float,
    zone_id: str,
    zone_type: str,
    zone_description: Optional[str] = None,
    max_dwell_seconds: float = 0,
    vehicle_position: Optional[Tuple[float, float]] = None,
    entry_timestamp: Optional[str] = None,
    current_timestamp: Optional[str] = None,
    plate_text: Optional[str] = None,
    plate_confidence: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Builds a clean illegal-parking-violation-candidate dict ready for
    the incident fusion service.

    Args:
        track_id:           Unique tracking ID of the vehicle.
        frame_id:           Frame ID where the violation was detected.
        confidence:         Confidence score (0.0–1.0).
        dwell_time_seconds: How long the vehicle has been in the zone.
        zone_id:            ID of the parking zone violated.
        zone_type:          "NO_PARKING" or "TIME_LIMITED".
        zone_description:   Human-readable zone description.
        max_dwell_seconds:  Allowed parking duration for the zone.
        vehicle_position:   (x, y) vehicle position at detection time.
        entry_timestamp:    When the vehicle first entered the zone.
        current_timestamp:  Current evaluation timestamp.
        plate_text:         Recognized license plate text (if available).
        plate_confidence:   Plate recognition confidence (if available).

    Returns:
        A violation candidate dict.
    """
    candidate: Dict[str, Any] = {
        "violation_type": "ILLEGAL_PARKING",
        "confidence": round(confidence, 3),
        "track_id": track_id,
        "frame_id": frame_id,
        "parking_metadata": {
            "dwell_time_seconds": round(dwell_time_seconds, 1),
            "zone_id": zone_id,
            "zone_type": zone_type,
            "zone_description": zone_description,
            "max_dwell_seconds": max_dwell_seconds,
            "vehicle_position": vehicle_position,
            "entry_timestamp": entry_timestamp,
            "current_timestamp": current_timestamp,
        },
    }

    if plate_text is not None:
        candidate["plate_text"] = plate_text
        candidate["plate_confidence"] = (
            round(plate_confidence, 3) if plate_confidence else None
        )

    return candidate
