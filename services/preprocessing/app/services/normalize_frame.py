import cv2
import numpy as np
from typing import Tuple


def resize_with_letterbox(image: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
    """
    Resizes the image to fit within the target size while preserving aspect ratio.
    Pads the remaining area with a neutral gray (114, 114, 114) to form a letterbox.

    This is the standard preprocessing step for YOLO-family detectors.

    Args:
        image: Input BGR image.
        target_size: (width, height) tuple for the output dimensions.

    Returns:
        Letterboxed image of exactly target_size dimensions.
    """
    target_w, target_h = target_size
    h, w = image.shape[:2]

    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Create canvas filled with neutral gray
    canvas = np.full((target_h, target_w, 3), 114, dtype=np.uint8)

    # Center the resized image on the canvas
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    canvas[offset_y:offset_y + new_h, offset_x:offset_x + new_w] = resized

    return canvas


def normalize_color_space(image: np.ndarray) -> np.ndarray:
    """
    Converts the image from BGR (OpenCV default) to RGB and normalizes
    pixel values to the 0.0–1.0 range as float32.

    This is the standard input format expected by most deep learning models.

    Returns:
        Float32 RGB image with values in [0.0, 1.0].
    """
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    normalized = rgb.astype(np.float32) / 255.0

    return normalized
