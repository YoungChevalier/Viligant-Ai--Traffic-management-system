from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class RetrainingCandidate(BaseModel):
    trace_id: str = Field(..., description="ID of the incident or frame")
    service_name: str = Field(..., description="Service emitting the candidate (e.g., 'detection', 'helmet-rule')")
    reason: str = Field(..., description="Reason for intake (e.g., 'LOW_CONFIDENCE', 'HUMAN_DISAGREEMENT')")
    artifact_path: str = Field(..., description="Path to the original image crop or frame")
    ground_truth: Optional[str] = Field(None, description="Human-provided ground truth label if available")

class DatasetVersion(BaseModel):
    dataset_id: str
    task: str
    candidate_count: int
    created_at: str
    stratification: Optional[Dict[str, int]] = Field(None, description="Counts of items per category")

class ModelRegistration(BaseModel):
    model_name: str = Field(..., description="Name of the model (e.g., 'helmet-classifier')")
    version: str = Field(..., description="Version tag (e.g., 'v2.1.0')")
    task: str = Field(..., description="Task category (e.g., 'classification', 'detection')")
    dataset_id: str = Field(..., description="Dataset ID used for training")
    metrics: Dict[str, float] = Field(..., description="Training/Validation metrics (e.g., mAP, F1-score)")
    artifact_path: str = Field(..., description="Path to model weights (ONNX/PT)")

class ModelStatusUpdate(BaseModel):
    status: str = Field(..., description="Target status: 'STAGING', 'PRODUCTION', or 'ARCHIVED'")

class RetrainingJobRequest(BaseModel):
    task: str = Field(..., description="The task to retrain (e.g., 'helmet-rule', 'detection')")
    model_name: str = Field(..., description="Base model to fine-tune (e.g., 'helmet-classifier')")

class RetrainingJobResponse(BaseModel):
    job_id: str
    status: str
    dataset_id: str
    baseline_metrics: Optional[Dict[str, float]] = None
    new_metrics: Optional[Dict[str, float]] = None
    deployment_decision: Optional[str] = None
    new_version: Optional[str] = None
