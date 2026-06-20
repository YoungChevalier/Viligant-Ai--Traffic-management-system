from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.api.schemas import PipelineEvent, MonitoringSummaryResponse

router = APIRouter()

@router.post("/obs/ingest")
async def post_ingest_event(event: PipelineEvent):
    """
    Consumes a pipeline event (from any service) and records it for 
    audit tracing, metrics aggregation, and monitoring.
    """
    from app.services.obs_service import record_pipeline_event
    try:
        result = await record_pipeline_event(event)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obs/traces/{trace_id}")
async def get_pipeline_trace(trace_id: str):
    """Fetches the full execution history and audit log for a specific frame or incident ID."""
    from app.services.obs_service import fetch_trace_history
    result = await fetch_trace_history(trace_id)
    if not result:
        raise HTTPException(status_code=404, detail="Trace not found")
    return result

@router.get("/obs/summary", response_model=MonitoringSummaryResponse)
async def get_monitoring_summary():
    """Returns aggregated pipeline metrics, stage health summaries, and active alerts."""
    from app.services.obs_service import generate_monitoring_summary
    try:
        return await generate_monitoring_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
