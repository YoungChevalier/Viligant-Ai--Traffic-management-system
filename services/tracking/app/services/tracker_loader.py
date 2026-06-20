import os
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Module-level singleton for the tracker instance
_tracker_instance: Optional[Any] = None

# Configurable tracker parameters via env vars
MAX_AGE = int(os.getenv("TRACKER_MAX_AGE", "30"))
MIN_HITS = int(os.getenv("TRACKER_MIN_HITS", "3"))
IOU_THRESHOLD = float(os.getenv("TRACKER_IOU_THRESHOLD", "0.3"))


def build_tracker() -> Dict[str, Any]:
    """
    Builds and returns a new tracker instance.

    In production this would instantiate a SORT / DeepSORT / ByteTrack tracker.
    Currently returns a stub tracker dict for development.
    """
    global _tracker_instance

    logger.info(
        "Building tracker | max_age=%d | min_hits=%d | iou_threshold=%.2f",
        MAX_AGE, MIN_HITS, IOU_THRESHOLD,
    )

    # TODO: Replace stub with actual tracker
    # Example with SORT:
    #   from sort import Sort
    #   tracker = Sort(max_age=MAX_AGE, min_hits=MIN_HITS, iou_threshold=IOU_THRESHOLD)
    _tracker_instance = {
        "type": "stub",
        "max_age": MAX_AGE,
        "min_hits": MIN_HITS,
        "iou_threshold": IOU_THRESHOLD,
        "active_tracks": {},
        "next_track_id": 1,
    }

    logger.info("Tracker built successfully (stub mode)")
    return _tracker_instance


def get_tracker_instance() -> Any:
    """
    Returns the cached tracker singleton.
    If no tracker has been built yet, creates one with default parameters.
    """
    global _tracker_instance

    if _tracker_instance is None:
        build_tracker()

    return _tracker_instance
