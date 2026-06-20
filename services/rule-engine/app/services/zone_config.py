"""
zone_config.py
Camera-specific intersection zone configuration provider.

MOCKED: Returns hardcoded stop-line positions and lane direction vectors
for known cameras. In production, this would load from a database or
configuration service.

Each zone config contains:
  - stop_line: tuple of two (x, y) endpoints defining the stop-line segment
  - lane_direction: (dx, dy) unit vector pointing in the direction of legal travel
  - zone_polygon: optional list of (x, y) points defining the approach zone
  - description: human-readable description of the zone
"""

import logging
from typing import Any, Dict, Optional, Tuple, List

logger = logging.getLogger(__name__)

# Type aliases
Point = Tuple[float, float]
Line = Tuple[Point, Point]


# ── Mocked Zone Configurations ─────────────────────────────────────────────
# Coordinates are in pixel-space relative to the camera's frame resolution.
# stop_line: ((x1,y1), (x2,y2)) — the two endpoints of the painted stop line
# lane_direction: (dx, dy) — unit vector of legal travel direction (towards intersection)
# zone_polygon: list of (x,y) — optional approach zone bounding polygon

_ZONE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "cam-northex-01": {
        "stop_line": ((200.0, 400.0), (600.0, 400.0)),
        "lane_direction": (0.0, -1.0),  # vehicles travel upward (north)
        "zone_polygon": [(180.0, 350.0), (620.0, 350.0), (620.0, 500.0), (180.0, 500.0)],
        "description": "North Expressway — Intersection A, Lanes 1-3",
    },
    "cam-southex-02": {
        "stop_line": ((150.0, 450.0), (550.0, 450.0)),
        "lane_direction": (0.0, 1.0),  # vehicles travel downward (south)
        "zone_polygon": [(130.0, 400.0), (570.0, 400.0), (570.0, 550.0), (130.0, 550.0)],
        "description": "South Expressway — Intersection B, Lanes 1-2",
    },
    "cam-east-03": {
        "stop_line": ((400.0, 150.0), (400.0, 500.0)),
        "lane_direction": (-1.0, 0.0),  # vehicles travel leftward (east approach)
        "zone_polygon": [(350.0, 130.0), (500.0, 130.0), (500.0, 520.0), (350.0, 520.0)],
        "description": "East Ring Road — Intersection C, Lanes 1-2",
    },
}

# Default zone for unknown cameras (sensible fallback for development)
_DEFAULT_ZONE: Dict[str, Any] = {
    "stop_line": ((200.0, 400.0), (600.0, 400.0)),
    "lane_direction": (0.0, -1.0),
    "zone_polygon": [(180.0, 350.0), (620.0, 350.0), (620.0, 500.0), (180.0, 500.0)],
    "description": "Default intersection zone (fallback)",
}


def get_zone_config(camera_id: str) -> Dict[str, Any]:
    """
    Returns the intersection zone configuration for a given camera.

    MOCKED: Looks up an in-memory dictionary. In production this would
    query a camera-config database or REST config service.

    Args:
        camera_id: Unique identifier of the traffic camera.

    Returns:
        A dict with keys: stop_line, lane_direction, zone_polygon, description.
    """
    config = _ZONE_CONFIGS.get(camera_id)

    if config is None:
        logger.warning(
            "No zone config found for camera_id=%s — using default zone",
            camera_id,
        )
        config = _DEFAULT_ZONE.copy()
        config["camera_id"] = camera_id

    logger.info(
        "Loaded zone config for camera_id=%s | description=%s",
        camera_id, config.get("description"),
    )
    return config


def get_stop_line(camera_id: str) -> Line:
    """Convenience: returns just the stop-line segment for a camera."""
    config = get_zone_config(camera_id)
    return config["stop_line"]


def get_lane_direction(camera_id: str) -> Point:
    """Convenience: returns the lane direction vector for a camera."""
    config = get_zone_config(camera_id)
    return config["lane_direction"]
