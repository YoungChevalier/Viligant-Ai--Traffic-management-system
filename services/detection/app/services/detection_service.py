import logging
from typing import Dict, Any

from libs.vision_utils.image_io import load_image_from_path
from app.services.model_loader import get_loaded_detection_model
from app.services.inference import run_detection_inference
from app.services.format_results import (
    extract_detection_items,
    filter_detection_items,
    build_detection_response,
)

# MOCK: If DB is not ready, we mock the DB dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

async def detect_frame(request_data: Any) -> Dict[str, Any]:
    """
    Orchestrates the full detection pipeline:
      1. Load the preprocessed image from storage
      2. Retrieve the cached detection model
      3. Run raw inference
      4. Extract and filter structured detection items
      5. Persist detection records (Mocked DB)
      6. Publish downstream event (Mocked Queue)
    """
    frame_id = request_data.frame_id
    storage_path = request_data.processed_storage_path

    # 1. Load the preprocessed image
    image = load_image_from_path(storage_path)

    # 2 & 3. Run Inference
    model = get_loaded_detection_model()
    raw_result = run_detection_inference(model, image)

    # 4. Extract and Filter Detections
    items = extract_detection_items(raw_result)
    filtered_items = filter_detection_items(items, min_confidence=0.5)
    
    # Format the local response
    response = build_detection_response(frame_id, filtered_items)
    
    logger.info(f"Frame {frame_id}: Detected {len(filtered_items)} objects above threshold")

    # 5. Persist Detection Records (MOCKED DB)
    # db = next(get_db())
    # # Save each item in filtered_items to the detections table
    # db.commit()
    logger.info(f"Saved {len(filtered_items)} detection records to database (Mocked)")

    # 6. Publish to Downstream Queue (MOCKED)
    # In production, publish to the `tracks` queue for the tracking service.
    downstream_job = {
        "frame_id": frame_id,
        "camera_id": request_data.camera_id,
        "timestamp": request_data.timestamp,
        "detections": filtered_items
    }
    logger.info(f"Frame {frame_id} published to downstream tracking queue: {downstream_job}")

    # Return full orchestration state
    return {
        "frame_id": frame_id,
        "num_detections": len(filtered_items),
        "detections": filtered_items,
        "queue_status": "published"
    }
