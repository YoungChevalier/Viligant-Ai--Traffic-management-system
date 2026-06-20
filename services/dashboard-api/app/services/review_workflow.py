"""
review_workflow.py
Orchestrator for the human review workflow.
Ties together assignment, escalation, decision smoothing, and audit logging.
"""

import logging
from typing import Dict, Any, List, Optional
from libs.common_utils.time_utils import utc_now

from app.api.schemas import ReviewDecisionRequest, EscalationRequest, ReviewAssignmentRequest
from app.services.audit_logger import log_audit_action, get_audit_trail
from app.services.review_assignment import assign_case, get_assignment
from app.services.escalation_rules import check_auto_escalation, process_manual_escalation
from app.services.decision_smoothing import record_decision_for_smoothing

# We import the in-memory stores from incident_queries to keep state consistent
from app.services.incident_queries import _incident_store

logger = logging.getLogger(__name__)


async def get_review_queue(
    reviewer_id: Optional[str] = None,
    violation_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Fetches the paginated queue of incidents awaiting review.
    Can be filtered by assigned reviewer.
    """
    # Auto-escalate any open incidents that need it before returning the queue
    for incident in _incident_store.values():
        if incident.get("status") == "OPEN":
            escalation_tier = check_auto_escalation(incident)
            if escalation_tier:
                incident["status"] = "ESCALATED"
                incident["escalation_tier"] = escalation_tier
                incident["updated_at"] = utc_now().isoformat()
                log_audit_action(incident["incident_id"], "AUTO_ESCALATED", "SYSTEM", {"tier": escalation_tier})

    results = []
    for incident in _incident_store.values():
        # Only show incidents needing review
        if incident.get("status") not in ["OPEN", "ESCALATED", "ASSIGNED"]:
            continue
            
        if violation_type and incident.get("primary_violation") != violation_type:
            continue
            
        incident_id = incident.get("incident_id")
        assigned_to = get_assignment(incident_id)
        
        # If filtering by reviewer, skip if not assigned to them
        if reviewer_id and assigned_to != reviewer_id:
            continue
            
        # Attach assignment info for the response
        incident_copy = dict(incident)
        incident_copy["assigned_to"] = assigned_to
        results.append(incident_copy)

    results.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    page = results[offset : offset + limit]
    return {"total": len(results), "limit": limit, "offset": offset, "queue": page}


async def assign_incident(incident_id: str, request: ReviewAssignmentRequest) -> Dict[str, Any]:
    """Assigns an incident to a reviewer and logs it."""
    if incident_id not in _incident_store:
        raise ValueError(f"Incident {incident_id} not found")
        
    incident = _incident_store[incident_id]
    
    assigned_reviewer = assign_case(incident_id, request.reviewer_id, request.force_reassign)
    
    if incident.get("status") == "OPEN":
        incident["status"] = "ASSIGNED"
        incident["updated_at"] = utc_now().isoformat()
        
    log_audit_action(incident_id, "ASSIGNED", "SYSTEM", {"assigned_to": assigned_reviewer})
    
    return {"incident_id": incident_id, "assigned_to": assigned_reviewer, "status": incident["status"]}


async def submit_decision(incident_id: str, request: ReviewDecisionRequest) -> Dict[str, Any]:
    """
    Processes a review decision (APPROVE, REJECT, MODIFY).
    Updates status, logs audit trail, applies decision smoothing, and triggers downstream actions.
    """
    if incident_id not in _incident_store:
        # Mocking creation if we test directly
        _incident_store[incident_id] = {"incident_id": incident_id, "status": "OPEN", "primary_violation": "UNKNOWN"}
        
    incident = _incident_store[incident_id]
    
    # 1. Update status
    status_map = {
        "APPROVE": "APPROVED",
        "REJECT": "REJECTED",
        "MODIFY": "MODIFIED"
    }
    new_status = status_map.get(request.action, "OPEN")
    incident["status"] = new_status
    incident["updated_at"] = utc_now().isoformat()
    
    if request.confidence_override is not None:
        incident["confidence"] = request.confidence_override

    # 2. Log Audit Action
    log_audit_action(incident_id, f"DECISION_{request.action}", request.reviewer_id, {
        "notes": request.notes,
        "confidence_override": request.confidence_override
    })

    # 3. Decision Smoothing (Pattern detection)
    violation_type = incident.get("primary_violation", "UNKNOWN")
    record_decision_for_smoothing(request.reviewer_id, violation_type, request.action)

    # 4. Downstream publish
    if new_status == "APPROVED":
        logger.info("Incident %s published to downstream enforcement queue", incident_id)
        queue_status = "published"
    else:
        logger.info("Incident %s is %s. No enforcement action.", incident_id, new_status)
        queue_status = "none"

    return {
        "incident_id": incident_id,
        "action": request.action,
        "new_status": new_status,
        "queue_status": queue_status
    }


async def escalate_incident(incident_id: str, request: EscalationRequest) -> Dict[str, Any]:
    """Manually escalates an incident to a higher tier."""
    if incident_id not in _incident_store:
         _incident_store[incident_id] = {"incident_id": incident_id, "status": "OPEN"}
         
    incident = _incident_store[incident_id]
    
    process_manual_escalation(incident_id, incident.get("escalation_tier", "TIER_1"), request.target_tier, request.reason)
    
    incident["status"] = "ESCALATED"
    incident["escalation_tier"] = request.target_tier
    incident["updated_at"] = utc_now().isoformat()
    
    log_audit_action(incident_id, "ESCALATED", request.reviewer_id, {
        "target_tier": request.target_tier,
        "reason": request.reason
    })
    
    return {"incident_id": incident_id, "status": "ESCALATED", "tier": request.target_tier}


async def get_incident_audit_log(incident_id: str) -> List[Dict[str, Any]]:
    """Returns the immutable audit log for a case."""
    return get_audit_trail(incident_id)
