from pydantic import BaseModel, Field
from datetime import datetime

class FrameIngestRequest(BaseModel):
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: datetime = Field(..., description="ISO-8601 timestamp of frame capture")
    image_payload: str = Field(..., description="Base64 encoded raw frame image")
