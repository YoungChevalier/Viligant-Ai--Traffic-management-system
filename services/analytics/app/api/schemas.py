from pydantic import BaseModel, Field
from typing import Optional, Dict

class ReviewedCaseEvent(BaseModel):
    incident_id: str = Field(..., description="The ID of the incident case")
    status: str = Field(..., description="The final review status (e.g., APPROVED, REJECTED)")
    reviewer_id: str = Field(..., description="The ID of the reviewer")
    primary_violation: str = Field(..., description="The type of violation")
    plate_text: Optional[str] = Field(None, description="The recognized license plate")
    camera_id: str = Field(..., description="The ID of the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of the incident")

class AnalyticsSummaryResponse(BaseModel):
    total_cases: int
    by_violation_type: Dict[str, int]
    by_status: Dict[str, int]
    top_cameras: Dict[str, int]
