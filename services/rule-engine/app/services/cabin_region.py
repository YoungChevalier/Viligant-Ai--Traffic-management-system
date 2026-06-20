"""
cabin_region.py
Driver/occupant cabin region estimation from vehicle bounding boxes.

MOCKED: Estimates the driver-side cabin region using geometric heuristics
applied to the vehicle's bounding box. In production, this would use a
trained occupant detection model or a more sophisticated windshield
localization approach.

The cabin region is the sub-area of the vehicle image where the driver
(front-left for left-hand-drive countries, front-right for right-hand-drive)
is expected to be visible through the windshield.
"""

import logging
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# Driving side configuration
# "LEFT" = driver on left side of vehicle (most countries)
# "RIGHT" = driver on right side (UK, India, Japan, etc.)
DRIVING_SIDE = "LEFT"

# Cabin region as fraction of vehicle bbox
# These ratios estimate the windshield / front-cabin area
CABIN_TOP_RATIO = 0.15      # cabin starts 15% from top of vehicle bbox
CABIN_BOTTOM_RATIO = 0.55   # cabin ends 55% from top
CABIN_DRIVER_LEFT_RATIO = 0.05   # driver side starts 5% from left edge
CABIN_DRIVER_RIGHT_RATIO = 0.50  # driver side ends at 50% (left half)
CABIN_PASSENGER_LEFT_RATIO = 0.50
CABIN_PASSENGER_RIGHT_RATIO = 0.95

# Minimum crop dimensions (pixels) for a viable classification
MIN_CROP_WIDTH = 20
MIN_CROP_HEIGHT = 20


def estimate_cabin_region(
    bbox: Dict[str, float],
    seat: str = "driver",
    driving_side: str = DRIVING_SIDE,
) -> Optional[Dict[str, float]]:
    """
    Estimates the cabin/occupant region within a vehicle bounding box.

    MOCKED: Uses fixed geometric ratios to derive the windshield area.
    In production, this would be replaced with a trained cabin-detection
    model or windshield segmentation.

    Args:
        bbox: Vehicle bounding box with keys x1, y1, x2, y2.
        seat: "driver" or "passenger".
        driving_side: "LEFT" or "RIGHT" (which side the driver sits on).

    Returns:
        A dict with x1, y1, x2, y2 for the cabin region, or None if
        the resulting crop would be too small.
    """
    x1 = bbox.get("x1", 0)
    y1 = bbox.get("y1", 0)
    x2 = bbox.get("x2", 0)
    y2 = bbox.get("y2", 0)

    width = x2 - x1
    height = y2 - y1

    if width < MIN_CROP_WIDTH or height < MIN_CROP_HEIGHT:
        return None

    # Vertical: cabin area (windshield region)
    cabin_y1 = y1 + height * CABIN_TOP_RATIO
    cabin_y2 = y1 + height * CABIN_BOTTOM_RATIO

    # Horizontal: depends on seat and driving side
    if seat == "driver":
        if driving_side == "LEFT":
            cabin_x1 = x1 + width * CABIN_DRIVER_LEFT_RATIO
            cabin_x2 = x1 + width * CABIN_DRIVER_RIGHT_RATIO
        else:
            cabin_x1 = x1 + width * CABIN_PASSENGER_LEFT_RATIO
            cabin_x2 = x1 + width * CABIN_PASSENGER_RIGHT_RATIO
    else:  # passenger
        if driving_side == "LEFT":
            cabin_x1 = x1 + width * CABIN_PASSENGER_LEFT_RATIO
            cabin_x2 = x1 + width * CABIN_PASSENGER_RIGHT_RATIO
        else:
            cabin_x1 = x1 + width * CABIN_DRIVER_LEFT_RATIO
            cabin_x2 = x1 + width * CABIN_DRIVER_RIGHT_RATIO

    # Validate minimum dimensions
    crop_w = cabin_x2 - cabin_x1
    crop_h = cabin_y2 - cabin_y1
    if crop_w < MIN_CROP_WIDTH or crop_h < MIN_CROP_HEIGHT:
        logger.debug(
            "Cabin region too small (%.0fx%.0f) — skipping",
            crop_w, crop_h,
        )
        return None

    region = {
        "x1": round(cabin_x1, 1),
        "y1": round(cabin_y1, 1),
        "x2": round(cabin_x2, 1),
        "y2": round(cabin_y2, 1),
    }

    logger.info(
        "Estimated %s cabin region: %s (from vehicle bbox %.0fx%.0f)",
        seat, region, width, height,
    )
    return region


def crop_cabin_region(
    image: Any,
    cabin_bbox: Dict[str, float],
) -> Optional[Any]:
    """
    Crops the cabin region from the source image.

    MOCKED: In production, this would use OpenCV/NumPy to extract the
    sub-image. Currently returns a placeholder dict representing the crop
    so downstream code can operate without real image dependencies.

    Args:
        image: Source image (np.ndarray in production, Any for mock).
        cabin_bbox: Cabin region bounding box.

    Returns:
        Cropped image region, or None if crop fails.
    """
    x1 = int(cabin_bbox["x1"])
    y1 = int(cabin_bbox["y1"])
    x2 = int(cabin_bbox["x2"])
    y2 = int(cabin_bbox["y2"])

    # MOCKED: Return a placeholder representing the crop metadata
    # In production: return image[y1:y2, x1:x2].copy()
    crop_placeholder = {
        "_mock": True,
        "region": cabin_bbox,
        "width": x2 - x1,
        "height": y2 - y1,
    }

    logger.info(
        "Cropped cabin region: %dx%d pixels (Mocked)",
        x2 - x1, y2 - y1,
    )
    return crop_placeholder
