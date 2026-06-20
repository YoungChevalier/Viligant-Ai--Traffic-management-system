import cv2
import numpy as np
from typing import List, Tuple


def order_quad_points(points: List[Tuple[float, float]]) -> np.ndarray:
    """
    Orders four corner points of a quadrilateral in a consistent order:
    [top-left, top-right, bottom-right, bottom-left].

    This is required for a correct perspective warp.

    Args:
        points: A list of 4 (x, y) tuples.

    Returns:
        A (4, 2) NumPy float32 array with ordered points.
    """
    pts = np.array(points, dtype=np.float32)

    # Sort by sum (x + y): smallest = top-left, largest = bottom-right
    s = pts.sum(axis=1)
    # Sort by diff (y - x): smallest = top-right, largest = bottom-left
    d = np.diff(pts, axis=1).flatten()

    ordered = np.zeros((4, 2), dtype=np.float32)
    ordered[0] = pts[np.argmin(s)]   # top-left
    ordered[1] = pts[np.argmin(d)]   # top-right
    ordered[2] = pts[np.argmax(s)]   # bottom-right
    ordered[3] = pts[np.argmax(d)]   # bottom-left

    return ordered


def warp_plate_perspective(
    image: np.ndarray,
    quad_points: List[Tuple[float, float]],
    output_width: int = 200,
    output_height: int = 60,
) -> np.ndarray:
    """
    Applies a perspective warp to extract a license plate from a skewed view
    into a flat, front-facing rectangle.

    Args:
        image: Source image (BGR).
        quad_points: Four corner points of the plate in the source image.
        output_width: Desired width of the output plate image.
        output_height: Desired height of the output plate image.

    Returns:
        A warped plate image of shape (output_height, output_width, 3).
    """
    src = order_quad_points(quad_points)

    dst = np.array([
        [0, 0],
        [output_width - 1, 0],
        [output_width - 1, output_height - 1],
        [0, output_height - 1],
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, matrix, (output_width, output_height))

    return warped
