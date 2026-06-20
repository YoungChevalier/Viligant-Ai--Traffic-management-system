from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ReviewDecisionRequest(BaseModel):
    reviewer_id: str = Field(..., description="Unique ID of the human reviewer")
    action: str = Field(..., description="Action taken: APPROVE, REJECT, MODIFY")
    notes: Optional[str] = Field(None, description="Reason or context for the decision")
    confidence_override: Optional[float] = Field(None, description="Optional manually adjusted confidence")

class EscalationRequest(BaseModel):
    reviewer_id: str = Field(..., description="Unique ID of the human reviewer escalating")
    reason: str = Field(..., description="Reason for escalation (e.g., 'UNCLEAR_PLATE', 'EDGE_CASE')")
    target_tier: str = Field("TIER_2", description="Target escalation tier (e.g., TIER_2, ADMIN)")

class ReviewAssignmentRequest(BaseModel):
    reviewer_id: Optional[str] = Field(None, description="Specific reviewer ID to assign. If null, auto-assigns.")
    force_reassign: bool = Field(False, description="If true, bypasses existing assignment locks.")

class AuditLogEntry(BaseModel):
    incident_id: str = Field(..., description="ID of the incident")
    action_type: str = Field(..., description="E.g., VIEWED, ASSIGNED, DECISION_SUBMITTED, ESCALATED")
    reviewer_id: str = Field(..., description="Reviewer who performed the action")
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context (e.g., previous_status)")

class ReviewQueueFilter(BaseModel):
    violation_type: Optional[str] = None
    camera_id: Optional[str] = None
    min_confidence: Optional[float] = None
    max_confidence: Optional[float] = None
    assigned_to: Optional[str] = Field(None, description="Filter by assigned reviewer ID")
    limit: int = 50
    offset: int = 0
