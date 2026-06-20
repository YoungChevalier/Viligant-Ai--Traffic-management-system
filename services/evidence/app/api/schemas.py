from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class EvidenceRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    processed_storage_path: str = Field(..., description="URI where the preprocessed frame is stored")
    candidates_with_plates: List[Dict[str, Any]] = Field(default_factory=list, description="List of matched violations and ANPR results")
