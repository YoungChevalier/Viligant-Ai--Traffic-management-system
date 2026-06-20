import logging
from datetime import datetime
from typing import Dict, Any

from libs.common_utils.id_utils import build_frame_id
from libs.common_utils.path_utils import build_raw_frame_object_key
from app.services.object_store import save_uploaded_frame
from app.services.queue_publisher import publish_raw_frame_job

# MOCK: If DB is not ready, we mock the DB dependency here.
# In production, import your SQLAlchemy Session and models.
# from services.persistence.app.db.session import get_db
# from services.persistence.app.models.frame_models import Frame

logger = logging.getLogger(__name__)

async def ingest_frame(camera_id: str, timestamp: datetime, image_bytes: bytes) -> Dict[str, Any]:
    """
    Orchestrates the full ingestion pipeline:
      1. Build a storage record (frame ID + object key)
      2. Save raw bytes to object storage (or local mock)
      3. Persist metadata to the database
      4. Publish job to downstream queue
    """
    # 1. Prepare Identifiers & Paths
    frame_id = build_frame_id()
    storage_path = build_raw_frame_object_key(camera_id=camera_id, captured_at=timestamp)

    # 2. Save Image Bytes
    # (Uses object_store.py which currently saves locally as a mock)
    stored_uri = save_uploaded_frame(file_bytes=image_bytes, object_key=storage_path)
    logger.info(f"Frame {frame_id} saved to {stored_uri}")

    # 3. Persist Database Record
    # MOCK: Replace this with actual SQLAlchemy insertion
    # db = next(get_db())
    # new_frame = Frame(frame_id=frame_id, camera_id=camera_id, timestamp=timestamp, storage_path=stored_uri)
    # db.add(new_frame); db.commit()
    logger.info(f"Frame metadata {frame_id} recorded in database (Mocked)")

    # 4. Publish to Queue
    # (Uses queue_publisher.py which currently logs the envelope as a mock)
    job_payload = {
        "frame_id": frame_id,
        "camera_id": camera_id,
        "timestamp": timestamp.isoformat(),
        "storage_path": stored_uri,
    }
    envelope = publish_raw_frame_job(payload=job_payload)
    logger.info(f"Frame {frame_id} published to downstream queue")

    return {
        "frame_id": frame_id,
        "storage_path": stored_uri,
        "queue_status": "published"
    }

async def fetch_camera_config(camera_id: str):
    """
    Stub for fetching configuration for a specific camera.
    """
    return {"camera_id": camera_id, "status": "active"}
