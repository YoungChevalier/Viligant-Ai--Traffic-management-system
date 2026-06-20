"""
seatbelt_rule.py
Orchestrator for seatbelt violation detection.

Follows the helmet_rule.py pattern closely (both are image-based
classification rules):
  1. Accept tracked-object payload with frame image path
  2. Filter to car/vehicle tracks
  3. For each car, estimate the driver cabin region
  4. Crop the cabin region from the image
  5. Run seatbelt classification on the crop
  6. Build violation candidates for "no_seatbelt" predictions
  7. Persist candidates (mocked DB)
  8. Publish downstream event (mocked queue)
"""

import logging
from typing import Any, Dict, List

from app.services.cabin_region import estimate_cabin_region, crop_cabin_region
from app.services.seatbelt_inference import (
    get_loaded_seatbelt_model,
    classify_seatbelt_crop,
)
from app.services.seatbelt_candidate import build_seatbelt_candidate

# MOCK: Image loading
# In production: from libs.vision_utils.image_io import load_image_from_path
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Vehicle class names where seatbelt rules apply
# Motorcycles/autos are excluded (seatbelt is not applicable)
SEATBELT_VEHICLE_CLASSES = {"car", "truck", "van", "bus"}


def _extract_car_tracks(tracked_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filters tracked objects to only include cars and enclosed vehicles
    where seatbelt rules apply.
    """
    cars = [
        t for t in tracked_objects
        if t.get("class_name", "").lower() in SEATBELT_VEHICLE_CLASSES
    ]
    logger.info("Filtered %d seatbelt-applicable vehicles from %d tracked objects", len(cars), len(tracked_objects))
    return cars


def _load_frame_image(storage_path: str) -> Any:
    """
    Loads the preprocessed frame image from storage.

    MOCKED: Returns a placeholder. In production, this would call
    load_image_from_path() to get an np.ndarray.
    """
    # In production:
    # return load_image_from_path(storage_path)
    logger.info("Loading frame image from %s (Mocked)", storage_path)
    return {"_mock_image": True, "path": storage_path, "width": 1920, "height": 1080}


def _evaluate_car_seatbelt(
    track: Dict[str, Any],
    image: Any,
    model: Dict[str, Any],
    frame_id: str,
) -> Dict[str, Any] | None:
    """
    Evaluates a single car track for seatbelt violation.

    Steps:
      1. Estimate the driver cabin region from the car bbox
      2. Crop the cabin region from the image
      3. Classify seatbelt presence
      4. Build violation candidate if no seatbelt detected

    Returns a violation candidate dict or None if no violation.
    """
    track_id = track.get("track_id", "unknown")
    bbox = track.get("bbox", {})

    # 1. Estimate driver cabin region
    cabin_region = estimate_cabin_region(bbox, seat="driver")
    if cabin_region is None:
        logger.debug("Track %s: cabin region too small — skipping", track_id)
        return None

    # 2. Crop cabin region from image
    crop = crop_cabin_region(image, cabin_region)
    if crop is None:
        logger.debug("Track %s: cabin crop failed — skipping", track_id)
        return None

    # 3. Classify seatbelt
    result = classify_seatbelt_crop(model, crop)

    # 4. Check for violation
    if result["label"] != "no_seatbelt":
        return None  # Seatbelt is present — no violation

    logger.info(
        "Seatbelt violation detected | track_id=%s | label=%s | confidence=%.3f",
        track_id, result["label"], result["confidence"],
    )

    return build_seatbelt_candidate(
        track_id=track_id,
        frame_id=frame_id,
        confidence=result["confidence"],
        label=result["label"],
        cabin_region=cabin_region,
        seat_position="driver",
        vehicle_bbox=bbox,
    )


async def run_seatbelt_rule(request_data: Any) -> Dict[str, Any]:
    """
    Full seatbelt rule orchestrator:
      1. Load the frame image
      2. Filter to car/enclosed-vehicle tracks
      3. Load the seatbelt classification model
      4. Evaluate each car for seatbelt presence
      5. Persist violation candidates (Mocked DB)
      6. Publish downstream event (Mocked Queue)

    Args:
        request_data: SeatbeltRuleRequest Pydantic model.

    Returns:
        Result dict with frame info, violation candidates, and queue status.
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp
    storage_path = request_data.processed_storage_path

    # Serialize Pydantic models to dicts
    tracked_objects = [t.model_dump() for t in request_data.tracked_objects]

    # 1. Load image
    image = _load_frame_image(storage_path)

    # 2. Filter to seatbelt-applicable vehicles
    car_tracks = _extract_car_tracks(tracked_objects)

    if not car_tracks:
        logger.info("Frame %s: No seatbelt-applicable vehicles found — skipping", frame_id)
        return {
            "frame_id": frame_id,
            "rule": "NO_SEATBELT",
            "vehicles_evaluated": 0,
            "violations": [],
            "queue_status": "none",
        }

    # 3. Load model
    model = get_loaded_seatbelt_model()

    # 4. Evaluate each car
    candidates: List[Dict[str, Any]] = []
    for track in car_tracks:
        candidate = _evaluate_car_seatbelt(track, image, model, frame_id)
        if candidate:
            candidate["camera_id"] = camera_id
            candidate["timestamp"] = timestamp
            candidates.append(candidate)

    logger.info(
        "Frame %s: Evaluated %d vehicles, found %d seatbelt violations",
        frame_id, len(car_tracks), len(candidates),
    )

    # 5. Persist Violation Candidates (MOCKED DB)
    # db = next(get_db())
    # # Save each candidate to the violation_candidates table
    # db.commit()
    logger.info("Saved %d seatbelt violation candidates to database (Mocked)", len(candidates))

    # 6. Publish to Downstream Queue (MOCKED)
    if candidates:
        downstream_job = {
            "frame_id": frame_id,
            "camera_id": camera_id,
            "timestamp": timestamp,
            "violations": candidates,
        }
        logger.info("Frame %s published to downstream fusion queue: %s", frame_id, downstream_job)
    else:
        logger.info("Frame %s has no seatbelt violations. Pipeline terminates here.", frame_id)

    return {
        "frame_id": frame_id,
        "rule": "NO_SEATBELT",
        "vehicles_evaluated": len(car_tracks),
        "violations": candidates,
        "queue_status": "published" if candidates else "none",
    }
