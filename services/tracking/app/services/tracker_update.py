import logging
from typing import Any, Dict, List, Tuple
import numpy as np

from libs.vision_utils.bbox_utils import clip_bbox_to_image, compute_bbox_center
from libs.common_utils.id_utils import build_track_id

logger = logging.getLogger(__name__)


def convert_detections_to_tracker_input(
    detections: List[Dict[str, Any]],
) -> np.ndarray:
    """
    Converts structured detection items into the NumPy array format
    expected by SORT/ByteTrack trackers.

    Each row: [x1, y1, x2, y2, confidence]

    Returns an (N, 5) array. If no detections, returns an empty (0, 5) array.
    """
    if not detections:
        return np.empty((0, 5), dtype=np.float32)

    rows = []
    for det in detections:
        bbox = det["bbox"]
        rows.append([
            bbox["x1"], bbox["y1"],
            bbox["x2"], bbox["y2"],
            det["confidence"],
        ])

    return np.array(rows, dtype=np.float32)


def update_tracker(
    tracker: Any,
    detections: List[Dict[str, Any]],
    frame_shape: Tuple[int, int],
) -> List[Dict[str, Any]]:
    """
    Feeds detections into the tracker and returns updated track states.

    In production this would call tracker.update(det_array) on a
    SORT / DeepSORT / ByteTrack instance and return active tracks.
    Currently uses a stub matching strategy for development.

    Args:
        tracker: The tracker instance (from tracker_loader).
        detections: Structured detection items with bbox dicts.
        frame_shape: (height, width) of the current frame.

    Returns:
        A list of raw track dicts with track_id, bbox, class_name, and confidence.
    """
    det_array = convert_detections_to_tracker_input(detections)

    logger.info(
        "Updating tracker | detections=%d | frame_shape=%s",
        len(detections), frame_shape,
    )

    # TODO: Replace stub with actual tracker update
    # Example with SORT:
    #   tracked = tracker.update(det_array)
    #   return _parse_sort_output(tracked, detections)

    # Stub: assign a track ID to each detection
    active_tracks = tracker.get("active_tracks", {})
    next_id = tracker.get("next_track_id", 1)
    results = []

    for det in detections:
        bbox = clip_bbox_to_image(det["bbox"], frame_shape)
        center = compute_bbox_center(bbox)

        track_id = f"trk_{next_id:04d}"
        next_id += 1

        results.append({
            "track_id": track_id,
            "class_name": det["class_name"],
            "confidence": det["confidence"],
            "bbox": bbox,
            "center": {"x": center[0], "y": center[1]},
        })

    tracker["next_track_id"] = next_id

    logger.info("Tracker updated | active_tracks=%d", len(results))
    return results


def convert_tracker_output_to_tracked_objects(
    results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Converts raw tracker output into the standardised TrackedObject format
    expected downstream by the rule engine and incident fusion services.
    """
    tracked_objects = []

    for trk in results:
        tracked_objects.append({
            "track_id": trk["track_id"],
            "class_name": trk["class_name"],
            "confidence": trk["confidence"],
            "bbox": trk["bbox"],
            "center": trk["center"],
            "is_active": True,
        })

    return tracked_objects
