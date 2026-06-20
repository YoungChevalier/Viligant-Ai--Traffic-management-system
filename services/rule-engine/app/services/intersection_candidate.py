"""
intersection_candidate.py
Builds violation candidate dicts for intersection rule violations.

Follows the same pattern as helmet_inference.py::build_helmet_candidate.
"""

from typing import Any, Dict, List, Optional, Tuple


def build_intersection_candidate(
    track_id: str,
    frame_id: str,
    violation_type: str,
    confidence: float,
    crossing_point: Optional[Tuple[float, float]],
    prev_position: Optional[Tuple[float, float]],
    curr_position: Optional[Tuple[float, float]],
    plate_text: Optional[str] = None,
    plate_confidence: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Builds a clean intersection-violation-candidate dict ready for
    the incident fusion service.

    Args:
        track_id:        Unique tracking ID of the vehicle.
        frame_id:        Frame ID where the crossing was detected.
        violation_type:  "RED_LIGHT" or "STOP_LINE".
        confidence:      Confidence score (0.0–1.0).
        crossing_point:  (x, y) where the vehicle crossed the stop-line.
        prev_position:   Vehicle position in previous frame.
        curr_position:   Vehicle position in current frame.
        plate_text:      Recognized license plate text (if available).
        plate_confidence: Plate recognition confidence (if available).

    Returns:
        A violation candidate dict.
    """
    candidate: Dict[str, Any] = {
        "violation_type": violation_type,
        "confidence": round(confidence, 3),
        "track_id": track_id,
        "frame_id": frame_id,
        "geometry": {
            "crossing_point": crossing_point,
            "prev_position": prev_position,
            "curr_position": curr_position,
        },
    }

    if plate_text is not None:
        candidate["plate_text"] = plate_text
        candidate["plate_confidence"] = round(plate_confidence, 3) if plate_confidence else None

    return candidate
