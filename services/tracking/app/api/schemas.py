from pydantic import BaseModel, Field
from typing import Dict, List, Any

class DetectionItem(BaseModel):
    class_name: str
    confidence: float
    bbox: Dict[str, float]

class TrackingRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    detections: List[DetectionItem] = Field(default_factory=list, description="List of detected objects in the frame")
    processed_storage_path: str = Field(None, description="URI where the preprocessed frame is stored")
