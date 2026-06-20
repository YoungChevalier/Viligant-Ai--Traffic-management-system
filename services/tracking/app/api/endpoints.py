from fastapi import APIRouter, HTTPException
from app.api.schemas import TrackingRequest
from app.services.tracking_service import track_frame

router = APIRouter()

@router.post("/frames/track")
async def post_track_frame(request: TrackingRequest):
    """
    Accepts a tracking job (simulating a consumed queue event),
    and delegates bounding box association, motion feature extraction,
    and downstream publishing to the tracking service layer.
    """
    try:
        result = await track_frame(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
