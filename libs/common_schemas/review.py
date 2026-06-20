from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .enums import IncidentStatus

class ReviewActionRequest(BaseModel):
    incident_id: str = Field(..., description="Unique identifier of the incident being reviewed")
    action: str = Field(..., description="Action taken by the reviewer (e.g., 'VERIFY', 'REJECT', 'DISMISS')")
    reviewer_id: str = Field(..., description="Unique identifier of the user performing the review")
    notes: Optional[str] = Field(None, description="Optional notes, comments, or reasons provided by the reviewer")

class ReviewActionResponse(BaseModel):
    incident_id: str = Field(..., description="Unique identifier of the incident")
    new_status: IncidentStatus = Field(..., description="The newly updated status of the incident after the review")
    updated_at: datetime = Field(..., description="Timestamp of when the review action was processed")
    action_recorded: bool = Field(True, description="Indicates whether the review action was successfully saved")
