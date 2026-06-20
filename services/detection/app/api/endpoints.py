from fastapi import APIRouter, HTTPException
from app.api.schemas import DetectionRequest
from app.services.detection_service import detect_frame

router = APIRouter()

@router.post("/frames/detect")
async def post_detect_frame(request: DetectionRequest):
    """
    Accepts a detection job (simulating a consumed queue event),
    and delegates model loading, inference, and formatting to the 
    detection service layer.
    """
    try:
        result = await detect_frame(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
