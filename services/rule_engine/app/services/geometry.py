"""
geometry.py
Pure geometry helpers for stop-line crossing detection.

Uses cross-product-based line segment intersection to determine
whether a vehicle's movement trajectory crosses the stop-line
between consecutive frames.

No external dependencies — only standard library math.
"""

from typing import Tuple, Optional
import math

Point = Tuple[float, float]


def _cross(o: Point, a: Point, b: Point) -> float:
    """
    Returns the cross product of vectors OA and OB.
    Positive = counter-clockwise, Negative = clockwise, Zero = collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _on_segment(p: Point, q: Point, r: Point) -> bool:
    """
    Checks if point q lies on segment pr (assuming p, q, r are collinear).
    """
    return (
        min(p[0], r[0]) <= q[0] <= max(p[0], r[0])
        and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])
    )


def segments_intersect(
    p1: Point, p2: Point,
    p3: Point, p4: Point,
) -> bool:
    """
    Determines whether line segment p1→p2 intersects segment p3→p4.

    Uses the standard cross-product orientation test:
      - Compute orientations d1..d4
      - Segments intersect if orientations straddle (opposite signs)
      - Special-case: collinear overlap

    Args:
        p1, p2: Endpoints of the first segment (vehicle trajectory).
        p3, p4: Endpoints of the second segment (stop-line).

    Returns:
        True if the two segments intersect, False otherwise.
    """
    d1 = _cross(p3, p4, p1)
    d2 = _cross(p3, p4, p2)
    d3 = _cross(p1, p2, p3)
    d4 = _cross(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    # Collinear special cases
    if d1 == 0 and _on_segment(p3, p1, p4):
        return True
    if d2 == 0 and _on_segment(p3, p2, p4):
        return True
    if d3 == 0 and _on_segment(p1, p3, p2):
        return True
    if d4 == 0 and _on_segment(p1, p4, p2):
        return True

    return False


def has_crossed_line(
    prev_point: Point,
    curr_point: Point,
    line_start: Point,
    line_end: Point,
) -> bool:
    """
    Checks whether the movement from prev_point to curr_point crosses
    the stop-line defined by line_start → line_end.

    Args:
        prev_point: Vehicle position in the previous frame (x, y).
        curr_point: Vehicle position in the current frame (x, y).
        line_start: First endpoint of the stop-line.
        line_end:   Second endpoint of the stop-line.

    Returns:
        True if the vehicle trajectory crosses the stop-line.
    """
    return segments_intersect(prev_point, curr_point, line_start, line_end)


def compute_crossing_point(
    prev_point: Point,
    curr_point: Point,
    line_start: Point,
    line_end: Point,
) -> Optional[Point]:
    """
    Computes the exact intersection point of the vehicle trajectory
    with the stop-line. Returns None if the segments don't intersect.

    Uses parametric line intersection formula.
    """
    x1, y1 = prev_point
    x2, y2 = curr_point
    x3, y3 = line_start
    x4, y4 = line_end

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-10:
        return None  # parallel or coincident

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return (round(ix, 2), round(iy, 2))

    return None


def point_to_line_distance(
    point: Point,
    line_start: Point,
    line_end: Point,
) -> float:
    """
    Computes the perpendicular distance from a point to a line segment.
    Used for confidence scoring — closer crossings get higher confidence.

    Returns the minimum distance from the point to the line segment.
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end

    dx = x2 - x1
    dy = y2 - y1
    seg_len_sq = dx * dx + dy * dy

    if seg_len_sq < 1e-10:
        # Degenerate segment (single point)
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    # Project point onto the line, clamped to [0, 1]
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / seg_len_sq))

    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return math.sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)
