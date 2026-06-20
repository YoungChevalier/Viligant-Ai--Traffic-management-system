from typing import Dict, Any

from libs.vision_utils.image_io import load_image_from_path
from libs.vision_utils.crop_utils import crop_bbox
from app.services.plate_model_loader import get_loaded_plate_detector
from app.services.plate_detection import detect_plate_bbox, select_best_plate_bbox
from app.services.ocr_adapter import run_paddle_ocr, extract_best_ocr_text
from app.services.plate_text import normalize_plate_text, validate_indian_plate_format


import logging

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

def process_single_vehicle(image, vehicle_bbox, track_id, frame_id) -> Dict[str, Any]:
    """Helper to process ANPR on a single vehicle crop."""
    if vehicle_bbox:
        vehicle_crop = crop_bbox(image, vehicle_bbox)
    else:
        vehicle_crop = image

    detector = get_loaded_plate_detector()
    candidates = detect_plate_bbox(detector, vehicle_crop)
    best_plate = select_best_plate_bbox(candidates)

    base_result = {
        "frame_id": frame_id,
        "track_id": track_id,
        "plate_detected": False,
        "plate_text": None,
        "confidence": 0.0,
        "format_valid": False,
    }

    if not best_plate:
        return base_result

    plate_crop = crop_bbox(vehicle_crop, best_plate["bbox"])
    raw_ocr = run_paddle_ocr(plate_crop)
    best_text = extract_best_ocr_text(raw_ocr)

    if not best_text:
        base_result.update({"plate_detected": True, "confidence": best_plate["confidence"]})
        return base_result

    normalized = normalize_plate_text(best_text["text"])
    is_valid = validate_indian_plate_format(normalized)

    base_result.update({
        "plate_detected": True,
        "plate_text": normalized,
        "raw_text": best_text["text"],
        "confidence": best_text["confidence"],
        "format_valid": is_valid,
    })
    return base_result

async def read_plate_batch(request_data: Any) -> Dict[str, Any]:
    """
    Full ANPR orchestrator for a batch of violation candidates:
      1. Load the frame image
      2. For each violation, crop the vehicle region
      3. Detect plate and run OCR
      4. Persist plate reads (Mocked DB)
      5. Publish downstream event (Mocked Queue)
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp
    storage_path = request_data.processed_storage_path
    
    image = load_image_from_path(storage_path)
    
    plate_results = []
    
    # Process each violation candidate
    for violation in request_data.violations:
        # Use motorcycle_track_id if available, otherwise fallback to track_id
        target_track_id = violation.motorcycle_track_id or violation.track_id
        
        # In a real event-driven architecture, the tracker state or rule engine 
        # would inject the vehicle_bbox here. If missing, we scan the whole frame.
        v_bbox = violation.vehicle_bbox if hasattr(violation, 'vehicle_bbox') else None
        
        result = process_single_vehicle(image, v_bbox, target_track_id, frame_id)
        
        # Attach the read back to the candidate
        plate_results.append({
            "violation": violation.model_dump(),
            "anpr": result
        })

    logger.info(f"Frame {frame_id}: Processed ANPR for {len(plate_results)} vehicles")

    # 4. Persist Plate Records (MOCKED DB)
    # db = next(get_db())
    # # Save each valid plate read to the plate_reads and plate_candidates tables
    # db.commit()
    logger.info(f"Saved {len(plate_results)} plate reads to database (Mocked)")

    # 5. Publish to Downstream Queue (MOCKED)
    # In production, publish to the `fusion` queue for the Incident Fusion service.
    downstream_job = {
        "frame_id": frame_id,
        "camera_id": camera_id,
        "timestamp": timestamp,
        "processed_storage_path": storage_path,
        "candidates_with_plates": plate_results
    }
    logger.info(f"Frame {frame_id} published to downstream incident-fusion queue: {downstream_job}")

    return {
        "frame_id": frame_id,
        "processed_count": len(plate_results),
        "results": plate_results,
        "queue_status": "published"
    }
