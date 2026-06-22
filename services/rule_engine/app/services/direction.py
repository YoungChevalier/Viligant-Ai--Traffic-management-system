"""
direction.py
Vehicle direction computation and comparison utilities.

Computes the heading direction of a vehicle from its tracked trajectory,
and compares it against the allowed lane direction to determine if the
vehicle is driving on the wrong side.

Uses standard 2D vector math — no external dependencies.
"""

import math
from typing import Any, Dict, List, Optional, Tuple

Point = Tuple[float, float]

# ── Direction Computation ──────────────────────────────────────────────────


def compute_direction_vector(prev_point: Point, curr_point: Point) -> Point:
    """
    Computes a unit direction vector from prev_point to curr_point.

    Args:
        prev_point: Previous position (x, y).
        curr_point: Current position (x, y).

    Returns:
        (dx, dy) unit vector. Returns (0, 0) if points are coincident.
    """
    dx = curr_point[0] - prev_point[0]
    dy = curr_point[1] - prev_point[1]
    magnitude = math.sqrt(dx * dx + dy * dy)

    if magnitude < 1e-6:
        return (0.0, 0.0)

    return (dx / magnitude, dy / magnitude)


def compute_heading_angle(direction: Point) -> float:
    """
    Converts a direction vector to an angle in degrees [0, 360).
    0° = right (+x), 90° = down (+y), 180° = left, 270° = up.

    Args:
        direction: (dx, dy) unit direction vector.

    Returns:
        Heading angle in degrees.
    """
    angle = math.degrees(math.atan2(direction[1], direction[0]))
    if angle < 0:
        angle += 360.0
    return round(angle, 1)


def compute_average_direction(trajectory: List[Point]) -> Optional[Point]:
    """
    Computes the average direction vector from a sequence of trajectory points.
    Uses the overall displacement (first → last) for stability.

    Args:
        trajectory: List of (x, y) positions in chronological order.

    Returns:
        (dx, dy) unit direction vector, or None if trajectory is too short.
    """
    if len(trajectory) < 2:
        return None

    # Use overall displacement for stability (less noisy than per-frame)
    return compute_direction_vector(trajectory[0], trajectory[-1])


# ── Direction Comparison ───────────────────────────────────────────────────


def dot_product(a: Point, b: Point) -> float:
    """Dot product of two 2D vectors."""
    return a[0] * b[0] + a[1] * b[1]


def angle_between_vectors(a: Point, b: Point) -> float:
    """
    Computes the angle between two vectors in degrees [0, 180].

    Args:
        a, b: Unit direction vectors.

    Returns:
        Angle in degrees. 0 = same direction, 180 = opposite.
    """
    dot = dot_product(a, b)
    # Clamp to [-1, 1] to handle floating point precision
    dot = max(-1.0, min(1.0, dot))
    return round(math.degrees(math.acos(dot)), 1)


def is_wrong_direction(
    vehicle_direction: Point,
    allowed_direction: Point,
    threshold_degrees: float = 120.0,
) -> bool:
    """
    Determines if the vehicle direction conflicts with the allowed lane direction.

    A vehicle is driving on the wrong side if the angle between its
    direction and the allowed direction exceeds the threshold.

    Args:
        vehicle_direction: (dx, dy) unit vector of vehicle heading.
        allowed_direction: (dx, dy) unit vector of allowed lane direction.
        threshold_degrees: Minimum angle to classify as wrong-side (default: 120°).
                          120° is chosen to tolerate lane changes and curves
                          while catching clear opposing traffic.

    Returns:
        True if the vehicle is going the wrong way.
    """
    # Skip if vehicle is stationary (zero vector)
    if abs(vehicle_direction[0]) < 1e-6 and abs(vehicle_direction[1]) < 1e-6:
        return False

    angle = angle_between_vectors(vehicle_direction, allowed_direction)
    return angle >= threshold_degrees


def compute_direction_confidence(
    vehicle_direction: Point,
    allowed_direction: Point,
) -> float:
    """
    Computes a confidence score for the wrong-side violation.

    Higher confidence when the vehicle direction is more directly opposed
    to the allowed direction.

    Args:
        vehicle_direction: (dx, dy) unit vector of vehicle heading.
        allowed_direction: (dx, dy) unit vector of allowed lane direction.

    Returns:
        Confidence score [0.0, 1.0].
        - 1.0 = perfectly opposite (180°)
        - 0.5 = perpendicular (90°, borderline)
        - 0.0 = same direction (0°)
    """
    angle = angle_between_vectors(vehicle_direction, allowed_direction)
    # Map [0°, 180°] → [0.0, 1.0]
    raw_confidence = angle / 180.0
    return round(raw_confidence, 3)
