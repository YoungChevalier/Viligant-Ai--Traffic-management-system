from fastapi import APIRouter, HTTPException
from app.api.schemas import EvidenceRequest
from app.services.evidence_service import generate_evidence

router = APIRouter()

@router.post("/evidence/generate")
async def post_generate_evidence(request: EvidenceRequest):
    """
    Accepts an ANPR output batch (simulating a consumed queue event),
    aggregates it into an incident case, renders the evidence artifact,
    and publishes the final reviewable case.
    """
    try:
        result = await generate_evidence(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
