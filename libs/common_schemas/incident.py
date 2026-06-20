from pydantic import BaseModel, Field
from typing import List, Optional
from .enums import ViolationType, IncidentStatus

class ViolationCandidate(BaseModel):
    violation_type: ViolationType = Field(..., description="Type of the detected violation")
    confidence: float = Field(..., description="Confidence score of the violation detection")
    track_id: str = Field(..., description="Track ID of the offending vehicle")
    frame_id: str = Field(..., description="Frame ID where the violation was first detected")

class IncidentScoreBreakdown(BaseModel):
    detection_score: float = Field(0.0, description="Score contributed by object detection")
    tracking_score: float = Field(0.0, description="Score contributed by tracking persistence")
    anpr_score: float = Field(0.0, description="Score contributed by ANPR confidence")
    rule_score: float = Field(0.0, description="Score contributed by rule engine conditions")

class IncidentFusionRequest(BaseModel):
    track_id: str = Field(..., description="Unique track ID for the suspected incident")
    candidates: List[ViolationCandidate] = Field(..., description="List of violation candidates from the rule engine")

class IncidentFusionResponse(BaseModel):
    incident_id: str = Field(..., description="Unique identifier for the generated incident")
    track_id: str = Field(..., description="Track ID of the offending vehicle")
    status: IncidentStatus = Field(default=IncidentStatus.OPEN, description="Current status of the incident")
    confidence_score: float = Field(..., description="Overall confidence score of the incident (0.0 to 1.0)")
    breakdown: IncidentScoreBreakdown = Field(..., description="Breakdown of how the overall score was calculated")
