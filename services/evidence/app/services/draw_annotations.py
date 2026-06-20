import cv2
import numpy as np
from typing import Dict, Any

# Color palette (BGR)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 200, 0)
COLOR_YELLOW = (0, 220, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_OVERLAY_BG = (40, 40, 40)


def draw_bbox(
    image: np.ndarray,
    bbox: Dict[str, float],
    label: str,
    color: tuple = COLOR_RED,
    thickness: int = 2,
) -> np.ndarray:
    """
    Draws a bounding box and label on the image.

    Args:
        image: Source image (BGR). Modified in place and returned.
        bbox: Dict with keys x1, y1, x2, y2.
        label: Text label to display above the bbox.
        color: BGR color tuple for the rectangle and text background.
        thickness: Line thickness for the rectangle.

    Returns:
        The annotated image.
    """
    x1 = int(bbox["x1"])
    y1 = int(bbox["y1"])
    x2 = int(bbox["x2"])
    y2 = int(bbox["y2"])

    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    # Label background
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    label_thickness = 1
    (tw, th), baseline = cv2.getTextSize(label, font, font_scale, label_thickness)

    label_y = max(y1 - 6, th + 6)
    cv2.rectangle(image, (x1, label_y - th - 6), (x1 + tw + 8, label_y + 2), color, -1)
    cv2.putText(image, label, (x1 + 4, label_y - 2), font, font_scale, COLOR_WHITE, label_thickness)

    return image


def draw_incident_header(
    image: np.ndarray,
    incident_summary: Dict[str, Any],
) -> np.ndarray:
    """
    Draws an incident summary header bar at the top of the image.

    Displays violation type, confidence score, and incident ID.

    Args:
        image: Source image (BGR). Modified in place and returned.
        incident_summary: Dict with keys 'incident_id', 'primary_violation', 'confidence_score'.

    Returns:
        The annotated image.
    """
    h, w = image.shape[:2]
    bar_height = 40

    # Semi-transparent header bar
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (w, bar_height), COLOR_OVERLAY_BG, -1)
    cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)

    font = cv2.FONT_HERSHEY_SIMPLEX
    violation = incident_summary.get("primary_violation", "UNKNOWN")
    score = incident_summary.get("confidence_score", 0.0)
    incident_id = incident_summary.get("incident_id", "")

    header_text = f"{violation} | Score: {score:.2f} | {incident_id}"
    cv2.putText(image, header_text, (10, 26), font, 0.55, COLOR_YELLOW, 1)

    return image


def draw_plate_text(
    image: np.ndarray,
    plate_text: str,
    position: tuple = None,
) -> np.ndarray:
    """
    Draws a plate text overlay at the bottom of the image.

    Args:
        image: Source image (BGR). Modified in place and returned.
        plate_text: The recognised plate string to display.
        position: Optional (x, y) for text placement. Defaults to bottom-left.

    Returns:
        The annotated image.
    """
    h, w = image.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2

    if position is None:
        position = (10, h - 15)

    label = f"PLATE: {plate_text}"
    (tw, th), baseline = cv2.getTextSize(label, font, font_scale, thickness)

    # Background rectangle
    bx, by = position
    cv2.rectangle(image, (bx - 4, by - th - 8), (bx + tw + 8, by + 6), COLOR_OVERLAY_BG, -1)
    cv2.putText(image, label, (bx, by), font, font_scale, COLOR_GREEN, thickness)

    return image
