from typing import Dict, Any

from libs.vision_utils.image_io import load_image_from_path, encode_image_to_jpg_bytes
from libs.common_utils.path_utils import build_evidence_object_key
from app.services.build_assets import (
    build_thumbnail,
    build_annotated_frame,
    build_evidence_manifest,
)


import logging
import uuid
from typing import Dict, Any
from pathlib import Path

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

async def generate_evidence(request_data: Any) -> Dict[str, Any]:
    """
    Full evidence generation & aggregation orchestrator:
      1. Bundle frame and violation data into a single case
      2. Load the source frame
      3. Build an annotated evidence frame and thumbnail
      4. Encode to JPEG and save (Mocked Storage)
      5. Persist the incident case (Mocked DB)
      6. Publish downstream review event (Mocked Queue)
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp
    storage_path = request_data.processed_storage_path
    
    # 1. Generate an incident case grouping these violations
    incident_id = f"inc-{uuid.uuid4().hex[:8]}"
    incident_data = {
        "incident_id": incident_id,
        "frame_id": frame_id,
        "camera_id": camera_id,
        "timestamp": timestamp,
        "violations": request_data.candidates_with_plates
    }

    # 2. Load the source frame
    image = load_image_from_path(storage_path)

    # 3. Build visual assets (delegates to drawing_utils & evidence_generator)
    annotated = build_annotated_frame(image, incident_data)
    thumbnail = build_thumbnail(annotated)

    # 4. Save Assets (MOCKED LOCAL STORAGE)
    # In production, this uploads to S3/GCS.
    annotated_key = build_evidence_object_key(incident_id, "annotated_frame")
    thumbnail_key = build_evidence_object_key(incident_id, "thumbnail")
    
    # Mocking storage write
    dest_path_annotated = Path("./object_storage") / annotated_key
    dest_path_thumbnail = Path("./object_storage") / thumbnail_key
    dest_path_annotated.parent.mkdir(parents=True, exist_ok=True)
    dest_path_annotated.write_bytes(encode_image_to_jpg_bytes(annotated))
    dest_path_thumbnail.write_bytes(encode_image_to_jpg_bytes(thumbnail, quality=80))

    logger.info(f"Incident {incident_id}: Saved evidence artifacts to object_storage (Mocked)")

    # 5. Persist Incident Case (MOCKED DB)
    manifest = build_evidence_manifest(incident_data, [
        {"asset_type": "annotated_frame", "storage_path": annotated_key},
        {"asset_type": "thumbnail", "storage_path": thumbnail_key},
    ])
    
    # db = next(get_db())
    # # Save the full incident and manifest to incidents table
    # db.commit()
    logger.info(f"Saved incident {incident_id} case record to database (Mocked)")

    # 6. Publish to Downstream Queue (MOCKED)
    # In production, publish to the `dashboard` or `review` queue.
    downstream_job = {
        "incident_id": incident_id,
        "status": "AWAITING_REVIEW",
        "manifest": manifest
    }
    logger.info(f"Incident {incident_id} published to downstream review queue: {downstream_job}")

    return {
        "incident_id": incident_id,
        "manifest": manifest,
        "queue_status": "published"
    }
