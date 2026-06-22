from typing import Dict, Any, List
import numpy as np

from libs.vision_utils.image_io import load_image_from_path
from libs.vision_utils.crop_utils import crop_head_region_from_person_bbox
from app.services.helmet_model_loader import get_loaded_helmet_model
from app.services.helmet_inference import classify_helmet_crop, build_helmet_candidate
from app.services.rider_association import associate_riders_to_motorcycles


def extract_rider_crops(
    image: np.ndarray,
    rider_associations: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Crops the head region for each associated rider from the source image.

    Returns a list of dicts, each containing:
      - rider_track_id: str
      - motorcycle_track_id: str
      - head_crop: np.ndarray
    """
    crops = []

    for assoc in rider_associations:
        head_crop = crop_head_region_from_person_bbox(image, assoc["rider_bbox"])

        # Skip tiny or invalid crops
        if head_crop.size == 0 or head_crop.shape[0] < 10 or head_crop.shape[1] < 10:
            continue

        crops.append({
            "rider_track_id": assoc["rider_track_id"],
            "motorcycle_track_id": assoc["motorcycle_track_id"],
            "head_crop": head_crop,
        })

    return crops


def evaluate_helmet_candidates(
    image: np.ndarray,
    rider_associations: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Extracts head crops for all associated riders and classifies each
    for helmet presence. Returns violation candidates for riders
    classified as 'no_helmet'.
    """
    model = get_loaded_helmet_model()
    crops = extract_rider_crops(image, rider_associations)

    candidates = []
    for crop_info in crops:
        score = classify_helmet_crop(model, crop_info["head_crop"])

        if score["label"] == "no_helmet":
            candidate = build_helmet_candidate(
                track_id=crop_info["rider_track_id"],
                frame_id="",  # filled by the caller
                score=score,
            )
            candidate["motorcycle_track_id"] = crop_info["motorcycle_track_id"]
            candidates.append(candidate)

    return candidates


import logging

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

async def run_helmet_rule(request_data: Any) -> Dict[str, Any]:
    """
    Full helmet rule orchestrator:
      1. Load the frame image
      2. Separate person and motorcycle tracks
      3. Associate riders to motorcycles
      4. Evaluate helmet presence for each rider
      5. Persist violation candidates (Mocked DB)
      6. Publish downstream event (Mocked Queue)
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp
    storage_path = request_data.processed_storage_path
    
    # Serialize Pydantic models to dicts for existing logic
    tracked_objects = [t.model_dump() for t in request_data.tracked_objects]

    # 1. Load image
    image = load_image_from_path(storage_path)

    # 2. Filter tracks
    person_tracks = [t for t in tracked_objects if t["class_name"] == "person"]
    motorcycle_tracks = [t for t in tracked_objects if t["class_name"] == "motorcycle"]

    # 3. Associate & 4. Evaluate
    associations = associate_riders_to_motorcycles(person_tracks, motorcycle_tracks)
    candidates = evaluate_helmet_candidates(image, associations)

    for c in candidates:
        c["frame_id"] = frame_id
        c["camera_id"] = camera_id
        c["timestamp"] = timestamp

    logger.info(f"Frame {frame_id}: Associated {len(associations)} riders, found {len(candidates)} helmet violations")

    # 5. Persist Violation Candidates (MOCKED DB)
    # db = next(get_db())
    # # Save each candidate to the violation_candidates table
    # db.commit()
    logger.info(f"Saved {len(candidates)} violation candidates to database (Mocked)")

    # 6. Publish to Downstream Queue (MOCKED)
    # In production, publish to the `anpr` or `fusion` queue if candidates exist.
    if candidates:
        downstream_job = {
            "frame_id": frame_id,
            "camera_id": camera_id,
            "timestamp": timestamp,
            "violations": candidates
        }
        logger.info(f"Frame {frame_id} published to downstream fusion queue: {downstream_job}")
    else:
        logger.info(f"Frame {frame_id} has no violations. Pipeline terminates here.")

    return {
        "frame_id": frame_id,
        "rule": "NO_HELMET",
        "associations_found": len(associations),
        "violations": candidates,
        "queue_status": "published" if candidates else "none"
    }
