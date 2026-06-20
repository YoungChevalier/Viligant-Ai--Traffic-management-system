from pydantic import BaseModel, Field
from typing import Dict

class DetectionRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    processed_storage_path: str = Field(..., description="URI where the preprocessed frame is stored")
    quality_metrics: Dict[str, float] = Field(default_factory=dict, description="Quality scores from preprocessing")
