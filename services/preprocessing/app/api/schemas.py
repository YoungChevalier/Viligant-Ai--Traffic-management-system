from pydantic import BaseModel, Field
from typing import Dict, Any, List

class PreprocessRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    storage_path: str = Field(..., description="URI or path where the raw frame is stored")

class PreprocessResponse(BaseModel):
    frame_id: str
    processed_storage_path: str
    metrics: Dict[str, float] = Field(..., description="Calculated quality scores (blur, brightness, noise, rain, shadow)")
    conditions_detected: List[str] = Field(..., description="Conditions flagged (e.g. LOW_LIGHT, RAIN)")
    plan_applied: List[str] = Field(..., description="Ordered list of enhancements applied")
    queue_status: str
