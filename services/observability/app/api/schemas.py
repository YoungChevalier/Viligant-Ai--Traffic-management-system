from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class PipelineEvent(BaseModel):
    trace_id: str = Field(..., description="Unique ID for the frame/case lifecycle (e.g., frame_id or incident_id)")
    service_name: str = Field(..., description="Name of the service emitting the event (e.g., 'detection', 'anpr')")
    event_type: str = Field(..., description="Type of event (e.g., 'PROCESSING_STARTED', 'MODEL_INFERENCE', 'CASE_REVIEWED')")
    status: str = Field(..., description="Status of the operation (e.g., 'SUCCESS', 'FAILED')")
    latency_ms: Optional[int] = Field(None, description="Execution time in milliseconds")
    model_version: Optional[str] = Field(None, description="Version of the model used (if applicable)")
    confidence_score: Optional[float] = Field(None, description="Average or primary confidence score (if applicable)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional structured audit payload")
    timestamp: str = Field(..., description="ISO-8601 timestamp of the event")

class StageMetrics(BaseModel):
    total_events: int
    failure_rate: float
    avg_latency_ms: float
    low_confidence_count: int

class MonitoringSummaryResponse(BaseModel):
    system_health: str
    active_alerts: List[str]
    stage_metrics: Dict[str, StageMetrics]
