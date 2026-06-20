from pydantic import BaseModel, Field
from typing import List, Optional

class PlateCandidate(BaseModel):
    plate_text: str = Field(..., description="The alphanumeric text read from the license plate")
    confidence: float = Field(..., description="Confidence score of the plate read (0.0 to 1.0)")
    region: Optional[str] = Field(None, description="Optional detected region/state/country of the plate")

class AnprRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the frame")
    track_id: Optional[str] = Field(None, description="Optional tracked object ID associated with the vehicle")
    storage_path: str = Field(..., description="Path or URI where the frame image is stored")

class AnprResponse(BaseModel):
    frame_id: str = Field(..., description="Unique identifier for the frame")
    track_id: Optional[str] = Field(None, description="Optional tracked object ID associated with the vehicle")
    candidates: List[PlateCandidate] = Field(default_factory=list, description="List of recognized plate candidates")
