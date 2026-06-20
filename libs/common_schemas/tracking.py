from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TrackPoint(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of this point in the track")
    x: float = Field(..., description="X coordinate (e.g., center point or bounding box base)")
    y: float = Field(..., description="Y coordinate (e.g., center point or bounding box base)")
    speed: Optional[float] = Field(None, description="Estimated instantaneous speed at this point")

class TrackedObject(BaseModel):
    track_id: str = Field(..., description="Unique tracking identifier for the object")
    class_name: str = Field(..., description="Object classification (e.g., car, truck, person)")
    points: List[TrackPoint] = Field(default_factory=list, description="Chronological points forming the object's historical path")
    is_active: bool = Field(True, description="Whether the object is still actively being tracked")

class TrackingRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the current frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: datetime = Field(..., description="Timestamp of the frame")

class TrackingResponse(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the processed frame")
    tracked_objects: List[TrackedObject] = Field(default_factory=list, description="List of active tracked objects for the frame")
