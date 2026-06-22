"""
lane_config.py
Camera-specific lane direction configuration provider.

MOCKED: Returns hardcoded allowed-direction vectors and lane boundaries
for known cameras. In production, this would load from a database or
configuration service.

Each lane config contains:
  - lanes: list of lane definitions, each with:
      - lane_id: unique lane identifier
      - allowed_direction: (dx, dy) unit vector of legal travel direction
      - boundaries: list of (x, y) points defining the lane polygon
      - description: human-readable lane description
  - default_direction: fallback allowed direction for the whole camera view
"""

import logging
import math
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

Point = Tuple[float, float]


# ── Mocked Lane Configurations ─────────────────────────────────────────────
# Coordinates are in pixel-space relative to the camera's frame resolution.

_LANE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "cam-northex-01": {
        "default_direction": (0.0, -1.0),  # northbound
        "lanes": [
            {
                "lane_id": "lane-1",
                "allowed_direction": (0.0, -1.0),
                "boundaries": [(100.0, 0.0), (300.0, 0.0), (300.0, 600.0), (100.0, 600.0)],
                "description": "Lane 1 — Northbound",
            },
            {
                "lane_id": "lane-2",
                "allowed_direction": (0.0, -1.0),
                "boundaries": [(300.0, 0.0), (500.0, 0.0), (500.0, 600.0), (300.0, 600.0)],
                "description": "Lane 2 — Northbound",
            },
            {
                "lane_id": "lane-3",
                "allowed_direction": (0.0, 1.0),  # southbound counter-flow lane
                "boundaries": [(500.0, 0.0), (700.0, 0.0), (700.0, 600.0), (500.0, 600.0)],
                "description": "Lane 3 — Southbound (opposite direction)",
            },
        ],
    },
    "cam-southex-02": {
        "default_direction": (0.0, 1.0),  # southbound
        "lanes": [
            {
                "lane_id": "lane-1",
                "allowed_direction": (0.0, 1.0),
                "boundaries": [(100.0, 0.0), (350.0, 0.0), (350.0, 600.0), (100.0, 600.0)],
                "description": "Lane 1 — Southbound",
            },
            {
                "lane_id": "lane-2",
                "allowed_direction": (0.0, 1.0),
                "boundaries": [(350.0, 0.0), (600.0, 0.0), (600.0, 600.0), (350.0, 600.0)],
                "description": "Lane 2 — Southbound",
            },
        ],
    },
    "cam-east-03": {
        "default_direction": (1.0, 0.0),  # eastbound
        "lanes": [
            {
                "lane_id": "lane-1",
                "allowed_direction": (1.0, 0.0),
                "boundaries": [(0.0, 100.0), (800.0, 100.0), (800.0, 300.0), (0.0, 300.0)],
                "description": "Lane 1 — Eastbound",
            },
            {
                "lane_id": "lane-2",
                "allowed_direction": (-1.0, 0.0),  # westbound counter-flow
                "boundaries": [(0.0, 300.0), (800.0, 300.0), (800.0, 500.0), (0.0, 500.0)],
                "description": "Lane 2 — Westbound (opposite direction)",
            },
        ],
    },
}

# Default config for unknown cameras
_DEFAULT_LANE_CONFIG: Dict[str, Any] = {
    "default_direction": (0.0, -1.0),
    "lanes": [
        {
            "lane_id": "lane-default",
            "allowed_direction": (0.0, -1.0),
            "boundaries": [(0.0, 0.0), (800.0, 0.0), (800.0, 600.0), (0.0, 600.0)],
            "description": "Default lane (fallback — entire frame)",
        },
    ],
}


def get_lane_config(camera_id: str) -> Dict[str, Any]:
    """
    Returns the lane direction configuration for a given camera.

    MOCKED: Looks up an in-memory dictionary. In production this would
    query a camera-config database or REST config service.

    Args:
        camera_id: Unique identifier of the traffic camera.

    Returns:
        A dict with keys: default_direction, lanes.
    """
    config = _LANE_CONFIGS.get(camera_id)

    if config is None:
        logger.warning(
            "No lane config found for camera_id=%s — using default config",
            camera_id,
        )
        config = _DEFAULT_LANE_CONFIG

    logger.info(
        "Loaded lane config for camera_id=%s | %d lanes defined",
        camera_id, len(config.get("lanes", [])),
    )
    return config


def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    """
    Ray-casting algorithm to test if a point is inside a polygon.
    Used to determine which lane a vehicle is in.
    """
    x, y = point
    n = len(polygon)
    inside = False

    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i

    return inside


def find_vehicle_lane(
    position: Point, lanes: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Determines which lane a vehicle is in based on its position.

    Args:
        position: (x, y) position of the vehicle.
        lanes: List of lane config dicts with 'boundaries' polygons.

    Returns:
        The matching lane config dict, or None if no lane matches.
    """
    for lane in lanes:
        boundaries = lane.get("boundaries", [])
        if boundaries and point_in_polygon(position, boundaries):
            return lane
    return None
