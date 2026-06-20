from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from app.api.schemas import (
    ReviewDecisionRequest,
    EscalationRequest,
    ReviewAssignmentRequest,
    AuditLogEntry,
    ReviewQueueFilter
)

router = APIRouter()

# --- Legacy Endpoints (Left intact for backward compatibility) ---

@router.get("/incidents")
async def get_incidents(
    status: Optional[str] = None,
    violation_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """Returns a paginated list of incidents, optionally filtered."""
    from app.services.incident_queries import list_incidents
    try:
        return await list_incidents(status, violation_type, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/incidents/{incident_id}")
async def get_incident_by_id(incident_id: str):
    """Returns full details for a single incident including evidence assets."""
    from app.services.incident_queries import load_incident_detail
    detail = await load_incident_detail(incident_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return detail

# --- New Human Review Workflow Endpoints ---

@router.get("/review/queue")
async def get_review_queue(
    reviewer_id: Optional[str] = None,
    violation_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Fetches the paginated queue of incidents awaiting review."""
    from app.services.review_workflow import get_review_queue as get_queue
    try:
        return await get_queue(reviewer_id, violation_type, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/review/{incident_id}/assign")
async def assign_incident_to_reviewer(incident_id: str, request: ReviewAssignmentRequest):
    """Assigns a review case to a specific reviewer or auto-assigns."""
    from app.services.review_workflow import assign_incident
    try:
        return await assign_incident(incident_id, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/review/{incident_id}/decision")
async def submit_review_decision(incident_id: str, request: ReviewDecisionRequest):
    """Submits a final decision (APPROVE/REJECT/MODIFY) for a review case."""
    from app.services.review_workflow import submit_decision
    try:
        return await submit_decision(incident_id, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/review/{incident_id}/escalate")
async def escalate_review_case(incident_id: str, request: EscalationRequest):
    """Escalates a review case to a higher tier."""
    from app.services.review_workflow import escalate_incident
    try:
        return await escalate_incident(incident_id, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/review/{incident_id}/audit-log")
async def get_case_audit_log(incident_id: str):
    """Fetches the immutable audit trail for a specific incident."""
    from app.services.review_workflow import get_incident_audit_log
    try:
        return await get_incident_audit_log(incident_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
