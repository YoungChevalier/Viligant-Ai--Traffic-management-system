"""
parking_zone_config.py
Camera-specific parking zone configuration provider.

MOCKED: Returns hardcoded no-parking zones and time-limited parking zones
for known cameras. In production, this would load from a database or
configuration service.

Each parking zone config contains:
  - zones: list of zone definitions, each with:
      - zone_id: unique zone identifier
      - zone_type: "NO_PARKING" or "TIME_LIMITED"
      - boundaries: list of (x, y) points defining the zone polygon
      - max_dwell_seconds: allowed parking duration (0 for NO_PARKING, N for TIME_LIMITED)
      - description: human-readable zone description
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

Point = Tuple[float, float]

# Zone types
ZONE_NO_PARKING = "NO_PARKING"
ZONE_TIME_LIMITED = "TIME_LIMITED"


# ── Mocked Parking Zone Configurations ─────────────────────────────────────

_PARKING_ZONE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "cam-northex-01": {
        "zones": [
            {
                "zone_id": "pz-north-01",
                "zone_type": ZONE_NO_PARKING,
                "boundaries": [(50.0, 400.0), (200.0, 400.0), (200.0, 550.0), (50.0, 550.0)],
                "max_dwell_seconds": 0,
                "description": "North Expressway — No-Parking Zone (bus lane)",
            },
            {
                "zone_id": "pz-north-02",
                "zone_type": ZONE_TIME_LIMITED,
                "boundaries": [(600.0, 400.0), (780.0, 400.0), (780.0, 580.0), (600.0, 580.0)],
                "max_dwell_seconds": 120,  # 2 minutes
                "description": "North Expressway — 2-min pickup/drop zone",
            },
        ],
    },
    "cam-southex-02": {
        "zones": [
            {
                "zone_id": "pz-south-01",
                "zone_type": ZONE_NO_PARKING,
                "boundaries": [(100.0, 350.0), (550.0, 350.0), (550.0, 500.0), (100.0, 500.0)],
                "max_dwell_seconds": 0,
                "description": "South Expressway — No-Parking Zone (intersection clearance)",
            },
        ],
    },
    "cam-east-03": {
        "zones": [
            {
                "zone_id": "pz-east-01",
                "zone_type": ZONE_TIME_LIMITED,
                "boundaries": [(50.0, 100.0), (250.0, 100.0), (250.0, 300.0), (50.0, 300.0)],
                "max_dwell_seconds": 300,  # 5 minutes
                "description": "East Ring Road — 5-min loading zone",
            },
            {
                "zone_id": "pz-east-02",
                "zone_type": ZONE_NO_PARKING,
                "boundaries": [(500.0, 350.0), (750.0, 350.0), (750.0, 500.0), (500.0, 500.0)],
                "max_dwell_seconds": 0,
                "description": "East Ring Road — No-Parking Zone (fire hydrant)",
            },
        ],
    },
}

# Default config for unknown cameras — single no-parking zone
_DEFAULT_PARKING_CONFIG: Dict[str, Any] = {
    "zones": [
        {
            "zone_id": "pz-default-01",
            "zone_type": ZONE_NO_PARKING,
            "boundaries": [(0.0, 400.0), (800.0, 400.0), (800.0, 600.0), (0.0, 600.0)],
            "max_dwell_seconds": 0,
            "description": "Default no-parking zone (fallback — bottom strip)",
        },
    ],
}


def get_parking_zone_config(camera_id: str) -> Dict[str, Any]:
    """
    Returns the parking zone configuration for a given camera.

    MOCKED: Looks up an in-memory dictionary. In production this would
    query a camera-config database or REST config service.

    Args:
        camera_id: Unique identifier of the traffic camera.

    Returns:
        A dict with key: zones (list of zone definitions).
    """
    config = _PARKING_ZONE_CONFIGS.get(camera_id)

    if config is None:
        logger.warning(
            "No parking zone config found for camera_id=%s — using default",
            camera_id,
        )
        config = _DEFAULT_PARKING_CONFIG

    logger.info(
        "Loaded parking zone config for camera_id=%s | %d zones defined",
        camera_id, len(config.get("zones", [])),
    )
    return config


def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    """
    Ray-casting algorithm to test if a point is inside a polygon.
    Used to determine whether a vehicle is within a parking zone.
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


def find_vehicle_zones(
    position: Point, zones: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Finds all parking zones a vehicle is currently inside.

    A vehicle can be in multiple overlapping zones (e.g., a no-parking zone
    that overlaps with a time-limited zone).

    Args:
        position: (x, y) position of the vehicle.
        zones: List of zone config dicts with 'boundaries' polygons.

    Returns:
        List of matching zone config dicts.
    """
    matches = []
    for zone in zones:
        boundaries = zone.get("boundaries", [])
        if boundaries and point_in_polygon(position, boundaries):
            matches.append(zone)
    return matches
