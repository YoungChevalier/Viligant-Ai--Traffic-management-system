from fastapi import APIRouter, HTTPException
from app.api.schemas import PreprocessRequest
from app.services.preprocess_service import preprocess_frame

router = APIRouter()

@router.post("/frames/preprocess")
async def post_preprocess_frame(request: PreprocessRequest):
    """
    Accepts a frame preprocessing job (simulating a consumed queue event),
    and delegates quality checks, normalization, and enhancement to the 
    preprocessing service layer.
    """
    try:
        result = await preprocess_frame(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
