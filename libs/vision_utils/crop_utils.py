from typing import Dict, Tuple
import numpy as np


def crop_bbox(image: np.ndarray, bbox: Dict[str, float]) -> np.ndarray:
    """
    Crops a region from the image defined by the bbox dict.
    Coordinates are clamped to image boundaries.

    Args:
        image: Source image (BGR or grayscale).
        bbox: Dict with keys x1, y1, x2, y2.

    Returns:
        Cropped image region as a NumPy array.
    """
    h, w = image.shape[:2]

    x1 = max(0, int(bbox["x1"]))
    y1 = max(0, int(bbox["y1"]))
    x2 = min(w, int(bbox["x2"]))
    y2 = min(h, int(bbox["y2"]))

    return image[y1:y2, x1:x2].copy()


def expand_bbox(
    bbox: Dict[str, float],
    image_shape: Tuple[int, int],
    margin_ratio: float = 0.1,
) -> Dict[str, float]:
    """
    Expands a bbox by a relative margin on all sides, clamped to image boundaries.

    Args:
        bbox: Dict with keys x1, y1, x2, y2.
        image_shape: (height, width) of the image.
        margin_ratio: Fraction of bbox size to add as margin (e.g., 0.1 = 10%).

    Returns:
        A new expanded bbox dict.
    """
    img_h, img_w = image_shape

    bw = bbox["x2"] - bbox["x1"]
    bh = bbox["y2"] - bbox["y1"]
    margin_x = bw * margin_ratio
    margin_y = bh * margin_ratio

    return {
        "x1": max(0.0, bbox["x1"] - margin_x),
        "y1": max(0.0, bbox["y1"] - margin_y),
        "x2": min(float(img_w), bbox["x2"] + margin_x),
        "y2": min(float(img_h), bbox["y2"] + margin_y),
    }


def crop_head_region_from_person_bbox(
    image: np.ndarray,
    person_bbox: Dict[str, float],
) -> np.ndarray:
    """
    Extracts the approximate head region from a person bounding box.
    Assumes the head occupies roughly the top 25% of the person bbox.

    Useful for helmet detection on motorcycle riders.

    Args:
        image: Source image (BGR).
        person_bbox: Dict with keys x1, y1, x2, y2.

    Returns:
        Cropped head region as a NumPy array.
    """
    person_height = person_bbox["y2"] - person_bbox["y1"]
    head_bbox = {
        "x1": person_bbox["x1"],
        "y1": person_bbox["y1"],
        "x2": person_bbox["x2"],
        "y2": person_bbox["y1"] + (person_height * 0.25),
    }

    return crop_bbox(image, head_bbox)
