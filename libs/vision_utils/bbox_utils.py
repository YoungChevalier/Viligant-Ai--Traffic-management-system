from typing import Dict, Tuple


def xyxy_to_bbox_dict(x1: float, y1: float, x2: float, y2: float) -> Dict[str, float]:
    """
    Converts raw x1, y1, x2, y2 coordinates into a structured bbox dict.
    """
    return {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "width": x2 - x1,
        "height": y2 - y1,
    }


def clip_bbox_to_image(bbox: Dict[str, float], image_shape: Tuple[int, int]) -> Dict[str, float]:
    """
    Clips a bbox dict so it does not exceed image boundaries.

    Args:
        bbox: Dict with keys x1, y1, x2, y2.
        image_shape: (height, width) of the image.

    Returns:
        A new bbox dict with coordinates clamped to valid ranges.
    """
    img_h, img_w = image_shape

    x1 = max(0.0, min(bbox["x1"], float(img_w)))
    y1 = max(0.0, min(bbox["y1"], float(img_h)))
    x2 = max(0.0, min(bbox["x2"], float(img_w)))
    y2 = max(0.0, min(bbox["y2"], float(img_h)))

    return {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "width": x2 - x1,
        "height": y2 - y1,
    }


def compute_bbox_center(bbox: Dict[str, float]) -> Tuple[float, float]:
    """
    Computes the center point (cx, cy) of a bbox dict.

    Returns:
        A tuple (center_x, center_y).
    """
    cx = (bbox["x1"] + bbox["x2"]) / 2.0
    cy = (bbox["y1"] + bbox["y2"]) / 2.0

    return (cx, cy)
