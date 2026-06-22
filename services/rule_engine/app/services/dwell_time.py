

"""
dwell_time.py
Dwell-time computation and threshold evaluation for parking violations.

Computes how long a vehicle has been stationary within a parking zone
and evaluates whether it exceeds the allowed duration.

In production, dwell time would be accumulated by the tracking service
across frames. For development, this module also provides a fallback
estimator based on motion vectors.
"""

import logging
import math
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# Minimum motion magnitude (pixels/frame) below which a vehicle is
# considered stationary. Accounts for tracker jitter.
STATIONARY_THRESHOLD = 3.0

# Minimum dwell time (seconds) before even considering a violation.
# Prevents false positives from momentary stops (e.g., traffic congestion).
MIN_VIOLATION_DWELL_SECONDS = 10.0


def is_vehicle_stationary(motion_vector: Tuple[float, float]) -> bool:
    """
    Determines if a vehicle is effectively stationary based on its
    motion vector magnitude.

    Args:
        motion_vector: (dx, dy) motion displacement between frames.

    Returns:
        True if the vehicle's motion is below the stationary threshold.
    """
    magnitude = math.sqrt(motion_vector[0] ** 2 + motion_vector[1] ** 2)
    return magnitude < STATIONARY_THRESHOLD


def compute_dwell_time(
    track: Dict[str, Any],
    current_timestamp: str,
) -> float:
    """
    Returns the dwell time for a tracked vehicle in seconds.

    Priority:
      1. Use explicit dwell_time_seconds from the tracking payload (if provided)
      2. Estimate from first_seen_timestamp and current timestamp
      3. Fallback: return 0 if no timing data is available

    Args:
        track: Tracked object dict (may contain dwell_time_seconds, first_seen_timestamp).
        current_timestamp: ISO-8601 timestamp of the current frame.

    Returns:
        Dwell time in seconds.
    """
    # Priority 1: explicit dwell time from tracking service
    explicit = track.get("dwell_time_seconds")
    if explicit is not None and explicit >= 0:
        return float(explicit)

    # Priority 2: compute from first_seen_timestamp
    first_seen = track.get("first_seen_timestamp")
    if first_seen and current_timestamp:
        try:
            from libs.common_utils.time_utils import parse_iso_datetime
            t_first = parse_iso_datetime(first_seen)
            t_now = parse_iso_datetime(current_timestamp)
            delta = (t_now - t_first).total_seconds()
            return max(0.0, delta)
        except Exception:
            pass

    # Priority 3: fallback
    return 0.0


def exceeds_dwell_threshold(
    dwell_seconds: float,
    max_dwell_seconds: float,
    zone_type: str,
) -> bool:
    """
    Checks whether a vehicle's dwell time violates the parking zone rules.

    Args:
        dwell_seconds:     How long the vehicle has been in the zone.
        max_dwell_seconds: Maximum allowed parking duration (0 = no parking at all).
        zone_type:         "NO_PARKING" or "TIME_LIMITED".

    Returns:
        True if the dwell time constitutes a violation.
    """
    if zone_type == "NO_PARKING":
        # Any stationary presence beyond the minimum threshold is a violation
        return dwell_seconds >= MIN_VIOLATION_DWELL_SECONDS

    if zone_type == "TIME_LIMITED":
        # Violation only if dwell exceeds the configured limit
        return dwell_seconds > max_dwell_seconds

    return False


def compute_parking_confidence(
    dwell_seconds: float,
    max_dwell_seconds: float,
    zone_type: str,
    is_stationary: bool,
) -> float:
    """
    Computes a confidence score for the parking violation.

    Factors:
      - NO_PARKING zones get higher base confidence
      - Longer dwell time → higher confidence
      - Stationary vehicle → confidence boost

    Returns:
        Confidence score [0.0, 1.0].
    """
    if zone_type == "NO_PARKING":
        # Base: 0.80, scales up with dwell time
        base = 0.80
        # Every 30s of dwell adds 0.04 confidence, capped at 0.98
        time_bonus = min(0.18, (dwell_seconds / 30.0) * 0.04)
    else:
        # TIME_LIMITED: base depends on how much they exceeded
        if max_dwell_seconds > 0:
            overshoot_ratio = dwell_seconds / max_dwell_seconds
            base = min(0.90, 0.50 + overshoot_ratio * 0.15)
        else:
            base = 0.70
        time_bonus = 0.0

    stationary_bonus = 0.05 if is_stationary else 0.0

    confidence = min(0.98, base + time_bonus + stationary_bonus)
    return round(confidence, 3)
