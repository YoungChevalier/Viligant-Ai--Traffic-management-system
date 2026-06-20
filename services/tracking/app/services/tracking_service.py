import logging
from typing import Dict, Any

from libs.vision_utils.image_io import load_image_from_path
from libs.common_utils.time_utils import utc_now
from app.services.tracker_loader import get_tracker_instance
from app.services.tracker_update import (
    update_tracker,
    convert_tracker_output_to_tracked_objects,
)
from app.services.motion_features import compute_motion_vector, compute_direction_angle

# MOCK: If DB or Redis is not ready, we mock the state persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Mocked in-memory dictionary to hold track history for motion feature calculation
# In production, use Redis to store the last known center coordinate per track_id.
_mock_track_history = {}

async def track_frame(request_data: Any) -> Dict[str, Any]:
    """
    Orchestrates the full tracking pipeline for a single frame:
      1. Load frame dimensions (for bbox clipping)
      2. Feed detections into the cached tracker instance
      3. Compute motion features based on previous state
      4. Persist updated track states (Mocked DB/Redis)
      5. Publish downstream event (Mocked Queue)
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp
    storage_path = request_data.processed_storage_path
    
    # We serialize the Pydantic models back to dicts for the generic tracker interface
    detections = [d.model_dump() for d in request_data.detections]

    # 1. Determine frame dimensions
    if storage_path:
        image = load_image_from_path(storage_path)
        frame_shape = (image.shape[0], image.shape[1])
    else:
        frame_shape = (1080, 1920)

    # 2. Update Tracker
    tracker = get_tracker_instance()
    raw_tracks = update_tracker(tracker, detections, frame_shape)
    tracked_objects = convert_tracker_output_to_tracked_objects(raw_tracks)

    # 3. Compute Motion Features
    enriched_tracks = []
    for obj in tracked_objects:
        track_id = obj["track_id"]
        center = obj["bbox_center"]
        
        last_center = _mock_track_history.get(track_id)
        if last_center:
            motion_vector = compute_motion_vector(last_center, center)
            direction_angle = compute_direction_angle(motion_vector)
            obj["motion_vector"] = motion_vector
            obj["direction_angle"] = direction_angle
        else:
            obj["motion_vector"] = (0.0, 0.0)
            obj["direction_angle"] = 0.0
            
        # Update history
        _mock_track_history[track_id] = center
        enriched_tracks.append(obj)

    logger.info(f"Frame {frame_id}: Associated {len(enriched_tracks)} active tracks")

    # 4. Persist Track States (MOCKED DB/REDIS)
    # db = next(get_db())
    # # Save each enriched_track to the tracks and track_history tables
    # db.commit()
    logger.info(f"Saved {len(enriched_tracks)} track records to state storage (Mocked)")

    # 5. Publish to Downstream Queue (MOCKED)
    # In production, publish to the `rules` queue for the rule engine.
    downstream_job = {
        "frame_id": frame_id,
        "camera_id": camera_id,
        "timestamp": timestamp,
        "processed_storage_path": storage_path,
        "tracked_objects": enriched_tracks
    }
    logger.info(f"Frame {frame_id} published to downstream rule-engine queue: {downstream_job}")

    return {
        "frame_id": frame_id,
        "tracked_count": len(enriched_tracks),
        "tracked_objects": enriched_tracks,
        "queue_status": "published"
    }
