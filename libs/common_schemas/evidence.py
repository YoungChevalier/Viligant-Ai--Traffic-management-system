from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EvidenceAssetRef(BaseModel):
    asset_id: str = Field(..., description="Unique identifier for the evidence asset (e.g., frame ID)")
    asset_type: str = Field(..., description="Type of the asset (e.g., full_frame, cropped_plate, video_clip)")
    storage_path: str = Field(..., description="Path or URI where the evidence asset is stored")

class EvidenceGenerateRequest(BaseModel):
    incident_id: str = Field(..., description="Unique identifier of the incident")
    track_id: str = Field(..., description="Track ID associated with the violation")
    violation_type: str = Field(..., description="Type of violation detected")
    assets: List[EvidenceAssetRef] = Field(default_factory=list, description="List of assets to include in the evidence package")
    timestamp: datetime = Field(..., description="Timestamp when the incident occurred")

class EvidenceGenerateResponse(BaseModel):
    evidence_package_id: str = Field(..., description="Unique identifier for the generated evidence package")
    incident_id: str = Field(..., description="Unique identifier of the incident")
    package_url: str = Field(..., description="URL or URI to access the generated evidence package (e.g., PDF report, ZIP file)")
    created_at: datetime = Field(..., description="Timestamp when the package was generated")
