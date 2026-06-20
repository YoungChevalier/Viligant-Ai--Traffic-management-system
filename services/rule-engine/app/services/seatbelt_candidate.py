"""
seatbelt_candidate.py
Builds violation candidate dicts for seatbelt violations.

Follows the same pattern as intersection_candidate.py and parking_candidate.py.
"""

from typing import Any, Dict, Optional, Tuple


def build_seatbelt_candidate(
    track_id: str,
    frame_id: str,
    confidence: float,
    label: str,
    cabin_region: Optional[Dict[str, float]] = None,
    seat_position: str = "driver",
    vehicle_bbox: Optional[Dict[str, float]] = None,
    plate_text: Optional[str] = None,
    plate_confidence: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Builds a clean seatbelt-violation-candidate dict ready for
    the incident fusion service.

    Args:
        track_id:         Unique tracking ID of the vehicle.
        frame_id:         Frame ID where the violation was detected.
        confidence:       Confidence score (0.0–1.0).
        label:            Classification label ('no_seatbelt').
        cabin_region:     Cabin crop bounding box used for classification.
        seat_position:    "driver" or "passenger".
        vehicle_bbox:     Original vehicle bounding box.
        plate_text:       Recognized license plate text (if available).
        plate_confidence: Plate recognition confidence (if available).

    Returns:
        A violation candidate dict.
    """
    candidate: Dict[str, Any] = {
        "violation_type": "NO_SEATBELT",
        "confidence": round(confidence, 3),
        "track_id": track_id,
        "frame_id": frame_id,
        "label": label,
        "cabin_metadata": {
            "seat_position": seat_position,
            "cabin_region": cabin_region,
            "vehicle_bbox": vehicle_bbox,
        },
    }

    if plate_text is not None:
        candidate["plate_text"] = plate_text
        candidate["plate_confidence"] = (
            round(plate_confidence, 3) if plate_confidence else None
        )

    return candidate
