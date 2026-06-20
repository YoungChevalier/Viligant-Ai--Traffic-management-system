import logging
from typing import Any, Dict, List, Optional
import numpy as np

logger = logging.getLogger(__name__)


def detect_plate_bbox(model: Any, vehicle_crop: np.ndarray) -> List[Dict[str, Any]]:
    """
    Runs plate localisation inference on a vehicle crop image.

    In production this would feed the crop through a plate detection model
    and return candidate plate bounding boxes.
    Currently returns stub candidates for development.

    Args:
        model: The loaded plate detector model (from plate_model_loader).
        vehicle_crop: Cropped vehicle region as a NumPy array (BGR).

    Returns:
        A list of candidate dicts, each containing:
          - bbox: dict with x1, y1, x2, y2 (relative to the crop)
          - confidence: float (0.0 to 1.0)
    """
    logger.info(
        "Detecting plate bbox | crop_shape=%s | model_type=%s",
        vehicle_crop.shape, model.get("type", "unknown"),
    )

    # TODO: Replace stub with actual inference
    h, w = vehicle_crop.shape[:2]

    # Stub: assume plate is in the bottom-center of the vehicle crop
    candidates = [
        {
            "bbox": {
                "x1": w * 0.25,
                "y1": h * 0.65,
                "x2": w * 0.75,
                "y2": h * 0.90,
            },
            "confidence": 0.91,
        },
    ]

    logger.info("Plate detection complete | candidates=%d", len(candidates))
    return candidates


def select_best_plate_bbox(
    candidates: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Selects the highest-confidence plate candidate from a list.

    Returns the best candidate dict, or None if no candidates exist.
    """
    if not candidates:
        return None

    best = max(candidates, key=lambda c: c["confidence"])
    return best
