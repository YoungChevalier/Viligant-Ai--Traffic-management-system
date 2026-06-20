"""
wrongside_candidate.py
Builds violation candidate dicts for wrong-side driving violations.

Follows the same pattern as intersection_candidate.py.
"""

from typing import Any, Dict, Optional, Tuple


def build_wrongside_candidate(
    track_id: str,
    frame_id: str,
    confidence: float,
    vehicle_direction: Tuple[float, float],
    vehicle_heading_angle: float,
    allowed_direction: Tuple[float, float],
    direction_angle_diff: float,
    lane_id: Optional[str] = None,
    lane_description: Optional[str] = None,
    vehicle_position: Optional[Tuple[float, float]] = None,
    plate_text: Optional[str] = None,
    plate_confidence: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Builds a clean wrong-side-violation-candidate dict ready for
    the incident fusion service.

    Args:
        track_id:              Unique tracking ID of the vehicle.
        frame_id:              Frame ID where the violation was detected.
        confidence:            Confidence score (0.0–1.0).
        vehicle_direction:     (dx, dy) computed vehicle heading vector.
        vehicle_heading_angle: Vehicle heading in degrees.
        allowed_direction:     (dx, dy) allowed lane direction vector.
        direction_angle_diff:  Angle between vehicle and allowed (degrees).
        lane_id:               ID of the lane the vehicle is in.
        lane_description:      Human-readable lane description.
        vehicle_position:      (x, y) vehicle position at detection time.
        plate_text:            Recognized license plate text (if available).
        plate_confidence:      Plate recognition confidence (if available).

    Returns:
        A violation candidate dict.
    """
    candidate: Dict[str, Any] = {
        "violation_type": "WRONG_WAY",
        "confidence": round(confidence, 3),
        "track_id": track_id,
        "frame_id": frame_id,
        "direction_metadata": {
            "vehicle_direction": vehicle_direction,
            "vehicle_heading_angle": vehicle_heading_angle,
            "allowed_direction": allowed_direction,
            "direction_angle_diff": direction_angle_diff,
            "lane_id": lane_id,
            "lane_description": lane_description,
            "vehicle_position": vehicle_position,
        },
    }

    if plate_text is not None:
        candidate["plate_text"] = plate_text
        candidate["plate_confidence"] = (
            round(plate_confidence, 3) if plate_confidence else None
        )

    return candidate
