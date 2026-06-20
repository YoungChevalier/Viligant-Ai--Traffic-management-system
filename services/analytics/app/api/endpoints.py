from fastapi import APIRouter, HTTPException
from typing import Optional
from app.api.schemas import ReviewedCaseEvent, AnalyticsSummaryResponse

router = APIRouter()

@router.post("/analytics/ingest")
async def post_ingest_event(event: ReviewedCaseEvent):
    """
    Consumes a reviewed-case event and projects it into the analytics read model.
    """
    from app.services.analytics_service import project_case_event
    try:
        result = await project_case_event(event)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/cases")
async def get_search_cases(
    plate: Optional[str] = None,
    violation_type: Optional[str] = None,
    status: Optional[str] = None,
    camera_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Searches and filters projected case records."""
    from app.services.analytics_service import search_cases
    try:
        return await search_cases(plate, violation_type, status, camera_id, start_date, end_date, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/cases/{case_id}")
async def get_case_by_id(case_id: str):
    """Fetches a single projected case record by ID."""
    from app.services.analytics_service import get_case
    result = await get_case(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Case not found")
    return result

@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary():
    """Returns aggregated counts and summaries of all projected cases."""
    from app.services.analytics_service import generate_summary
    try:
        return await generate_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
