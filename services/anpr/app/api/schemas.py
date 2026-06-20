from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ViolationCandidate(BaseModel):
    violation_type: str
    confidence: float
    track_id: str
    motorcycle_track_id: Optional[str] = None
    vehicle_bbox: Optional[Dict[str, float]] = None  # Expected to be enriched by the rule engine or tracker state

class ANPRRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    processed_storage_path: str = Field(..., description="URI where the preprocessed frame is stored")
    violations: List[ViolationCandidate] = Field(default_factory=list, description="List of violation candidates needing plate reads")
