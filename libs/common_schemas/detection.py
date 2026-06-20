from pydantic import BaseModel, Field
from typing import List

class BBox(BaseModel):
    x1: float = Field(..., description="Top-left x coordinate")
    y1: float = Field(..., description="Top-left y coordinate")
    x2: float = Field(..., description="Bottom-right x coordinate")
    y2: float = Field(..., description="Bottom-right y coordinate")

class DetectionItem(BaseModel):
    class_name: str = Field(..., description="Detected object class name (e.g., car, person)")
    confidence: float = Field(..., description="Confidence score of the detection (0.0 to 1.0)")
    bbox: BBox = Field(..., description="Bounding box of the detected object")

class DetectionRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the frame")
    storage_path: str = Field(..., description="Path or URI where the frame image is stored")

class DetectionResponse(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the frame")
    detections: List[DetectionItem] = Field(default_factory=list, description="List of detected objects")
