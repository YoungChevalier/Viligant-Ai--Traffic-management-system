from fastapi import APIRouter, HTTPException
from app.api.schemas import ANPRRequest
from app.services.anpr_service import read_plate_batch

router = APIRouter()

@router.post("/anpr/read")
async def post_read_plate(request: ANPRRequest):
    """
    Accepts a violation candidate job (simulating a consumed queue event),
    and delegates to the ANPR plate detection and OCR logic.
    """
    try:
        result = await read_plate_batch(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
