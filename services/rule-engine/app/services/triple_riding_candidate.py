"""
triple_riding_candidate.py
Builds violation candidate dicts for triple-riding violations.

Follows the same pattern as other candidate builders.
"""

from typing import Any, Dict, List, Optional


def build_triple_riding_candidate(
    motorcycle_track_id: str,
    frame_id: str,
    confidence: float,
    rider_count: int,
    rider_track_ids: List[str],
    motorcycle_bbox: Optional[Dict[str, float]] = None,
    plate_text: Optional[str] = None,
    plate_confidence: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Builds a clean triple-riding-violation-candidate dict ready for
    the incident fusion service.

    Args:
        motorcycle_track_id: Tracking ID of the motorcycle.
        frame_id:            Frame ID where the violation was detected.
        confidence:          Confidence score (0.0–1.0).
        rider_count:         Number of riders detected on this motorcycle.
        rider_track_ids:     List of tracking IDs for each associated rider.
        motorcycle_bbox:     Motorcycle bounding box.
        plate_text:          Recognized license plate text (if available).
        plate_confidence:    Plate recognition confidence (if available).

    Returns:
        A violation candidate dict.
    """
    candidate: Dict[str, Any] = {
        "violation_type": "TRIPLE_RIDING",
        "confidence": round(confidence, 3),
        "track_id": motorcycle_track_id,
        "frame_id": frame_id,
        "rider_metadata": {
            "rider_count": rider_count,
            "rider_track_ids": rider_track_ids,
            "motorcycle_bbox": motorcycle_bbox,
        },
    }

    if plate_text is not None:
        candidate["plate_text"] = plate_text
        candidate["plate_confidence"] = (
            round(plate_confidence, 3) if plate_confidence else None
        )

    return candidate
