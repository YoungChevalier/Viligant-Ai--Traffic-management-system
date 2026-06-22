from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class TrackedObject(BaseModel):
    track_id: str
    class_name: str
    confidence: float
    bbox: Dict[str, float]
    bbox_center: tuple[float, float]
    motion_vector: tuple[float, float]
    direction_angle: float

class HelmetRuleRequest(BaseModel):
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    processed_storage_path: str = Field(..., description="URI where the preprocessed frame is stored")
    tracked_objects: List[TrackedObject] = Field(default_factory=list, description="List of tracked objects")


class IntersectionRuleRequest(BaseModel):
    """
    Request schema for intersection violation evaluation (red-light + stop-line).
    The caller provides tracked objects and the current signal state.
    """
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    signal_state: str = Field(..., description="Traffic signal state: RED, YELLOW, or GREEN")
    tracked_objects: List[TrackedObject] = Field(default_factory=list, description="List of tracked objects with positional history")


class WrongSideRuleRequest(BaseModel):
    """
    Request schema for wrong-side driving violation evaluation.
    No signal state needed — direction comparison is signal-independent.
    """
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    tracked_objects: List[TrackedObject] = Field(default_factory=list, description="List of tracked objects with positional history")


class ParkingTrackedObject(BaseModel):
    """
    Extended tracked object with optional dwell-time state.
    dwell_time_seconds is provided by the tracking service or accumulated
    by the caller across frames.
    """
    track_id: str
    class_name: str
    confidence: float
    bbox: Dict[str, float]
    bbox_center: tuple[float, float]
    motion_vector: tuple[float, float]
    direction_angle: float
    dwell_time_seconds: Optional[float] = Field(None, description="Accumulated dwell time in seconds within a zone")
    first_seen_timestamp: Optional[str] = Field(None, description="ISO-8601 timestamp when the vehicle first entered the zone")


class ParkingRuleRequest(BaseModel):
    """
    Request schema for illegal parking violation evaluation.
    Carries tracked objects with optional dwell-time accumulation.
    """
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    tracked_objects: List[ParkingTrackedObject] = Field(default_factory=list, description="List of tracked objects with optional dwell-time state")


class SeatbeltRuleRequest(BaseModel):
    """
    Request schema for seatbelt violation evaluation.
    Requires the frame image path for cabin crop extraction, like the helmet rule.
    """
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    processed_storage_path: str = Field(..., description="URI where the preprocessed frame is stored")
    tracked_objects: List[TrackedObject] = Field(default_factory=list, description="List of tracked objects")


class TripleRidingRuleRequest(BaseModel):
    """
    Request schema for triple-riding violation evaluation.
    Needs person + motorcycle tracks in the same frame.
    """
    frame_id: str = Field(..., description="Unique identifier of the frame")
    camera_id: str = Field(..., description="Unique identifier for the camera")
    timestamp: str = Field(..., description="ISO-8601 timestamp of frame capture")
    tracked_objects: List[TrackedObject] = Field(default_factory=list, description="List of tracked objects (persons + motorcycles)")
