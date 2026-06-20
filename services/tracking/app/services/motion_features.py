import math
from typing import Tuple


def compute_motion_vector(
    previous_point: Tuple[float, float],
    current_point: Tuple[float, float],
) -> Tuple[float, float]:
    """
    Computes the motion vector (dx, dy) between two consecutive track points.

    Args:
        previous_point: (x, y) coordinates at the previous frame.
        current_point: (x, y) coordinates at the current frame.

    Returns:
        A tuple (dx, dy) representing the displacement.
    """
    dx = current_point[0] - previous_point[0]
    dy = current_point[1] - previous_point[1]

    return (dx, dy)


def compute_direction_angle(
    previous_point: Tuple[float, float],
    current_point: Tuple[float, float],
) -> float:
    """
    Computes the direction angle (in degrees) of motion between two
    consecutive track points.

    Uses atan2 so the angle covers the full 360° range:
      - 0°   = moving right
      - 90°  = moving down (image coordinates)
      - 180° = moving left
      - 270° = moving up

    Returns:
        Direction angle in degrees [0, 360).
    """
    dx = current_point[0] - previous_point[0]
    dy = current_point[1] - previous_point[1]

    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    # Normalize to [0, 360)
    if angle_deg < 0:
        angle_deg += 360.0

    return angle_deg
