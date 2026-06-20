from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GPSPoint(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

class FrameIngestRequest(BaseModel):
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: datetime = Field(..., description="Timestamp of when the frame was captured")
    image_payload: str = Field(..., description="Base64 encoded image or URI to the image")
    location: Optional[GPSPoint] = Field(None, description="Optional GPS coordinates of the camera at capture time")

class FrameStoredResponse(BaseModel):
    frame_id: str = Field(..., description="Unique identifier generated for the stored frame")
    storage_path: str = Field(..., description="Path or URI where the frame is stored")
    timestamp: datetime = Field(..., description="Timestamp of the frame")

class FrameJobPayload(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: datetime = Field(..., description="Timestamp of the frame")
    storage_path: str = Field(..., description="Path or URI where the frame is stored")
