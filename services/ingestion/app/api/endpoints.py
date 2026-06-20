import base64
from fastapi import APIRouter, HTTPException
from app.api.schemas import FrameIngestRequest
from app.services.ingestion_service import ingest_frame, fetch_camera_config

router = APIRouter()

@router.post("/frames/ingest")
async def post_ingest_frame(request: FrameIngestRequest):
    """
    Accepts a raw camera frame payload, validates it, and delegates 
    storage and queue publishing to the ingestion service layer.
    """
    try:
        # Decode base64 payload to bytes at the boundary
        image_bytes = base64.b64decode(request.image_payload)
        
        # Pass to service layer
        result = await ingest_frame(
            camera_id=request.camera_id,
            timestamp=request.timestamp,
            image_bytes=image_bytes
        )
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/cameras/{camera_id}/config")
async def get_camera_config(camera_id: str):
    """
    Returns the current configuration for the specified camera.
    Delegates retrieval to the ingestion service layer.
    """
    config = await fetch_camera_config(camera_id)
    if config is None:
        raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found")
    return config
