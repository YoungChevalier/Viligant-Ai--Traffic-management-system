from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict
from datetime import datetime
import uuid

class QueueEnvelope(BaseModel):
    envelope_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the message envelope")
    topic: str = Field(..., description="The queue topic this message belongs to")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the envelope was created")
    payload: Dict[str, Any] = Field(..., description="The actual message data payload")
    version: str = Field("1.0", description="Version of the envelope schema")

def build_queue_envelope(payload: Dict[str, Any], topic: str) -> QueueEnvelope:
    """
    Builds a QueueEnvelope around the given payload for the specified topic.
    """
    return QueueEnvelope(payload=payload, topic=topic)

def validate_queue_envelope(data: Dict[str, Any]) -> QueueEnvelope:
    """
    Validates a raw dictionary and parses it into a QueueEnvelope.
    Raises ValidationError if the data is invalid.
    """
    return QueueEnvelope(**data)
