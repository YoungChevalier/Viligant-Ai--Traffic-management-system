"""
schemas.py
Pydantic request/response schemas for the evaluation service.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class PredictionEntry(BaseModel):
    """A single model prediction for one sample."""
    sample_id: str = Field(..., description="Unique identifier for the image/sample")
    violation_type: str = Field(..., description="Predicted violation type")
    predicted_label: int = Field(..., description="1 = violation detected, 0 = no violation")
    confidence: float = Field(0.0, description="Model confidence score (0.0–1.0)")
    camera_id: Optional[str] = Field(None, description="Camera ID for per-camera evaluation")
    inference_latency_ms: Optional[float] = Field(None, description="Inference time in milliseconds")


class GroundTruthEntry(BaseModel):
    """A single ground-truth label for one sample."""
    sample_id: str = Field(..., description="Unique identifier matching the prediction")
    violation_type: str = Field(..., description="Ground-truth violation type")
    true_label: int = Field(..., description="1 = violation present, 0 = no violation")
    camera_id: Optional[str] = Field(None, description="Camera ID for per-camera evaluation")


class EvaluationRequest(BaseModel):
    """
    Request schema for running evaluation.
    Carries predictions + ground truth for one evaluation run.
    """
    evaluation_id: Optional[str] = Field(None, description="Unique evaluation run ID (auto-generated if not provided)")
    dataset_name: str = Field("default", description="Name of the dataset being evaluated")
    dataset_split: str = Field("test", description="Dataset split: train, val, or test")
    violation_types: Optional[List[str]] = Field(
        None,
        description="Evaluate only these violation types. If None, evaluate all types found in data.",
    )
    camera_ids: Optional[List[str]] = Field(
        None,
        description="Evaluate only these cameras. If None, evaluate all cameras.",
    )
    confidence_threshold: float = Field(0.5, description="Confidence threshold for binary classification")
    predictions: List[PredictionEntry] = Field(..., description="List of model predictions")
    ground_truths: List[GroundTruthEntry] = Field(..., description="List of ground-truth labels")
    throughput_images_per_sec: Optional[float] = Field(None, description="Measured throughput (images/sec)")
    cpu_usage_percent: Optional[float] = Field(None, description="Average CPU usage during inference (%)")
    memory_usage_mb: Optional[float] = Field(None, description="Peak memory usage during inference (MB)")


class ViolationMetrics(BaseModel):
    """Metrics for a single violation type."""
    violation_type: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    average_precision: float = Field(0.0, description="Average Precision (AP) for this class")
    true_positives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    false_negatives: int = 0
    support: int = Field(0, description="Number of ground-truth positives")
    sample_count: int = Field(0, description="Total samples evaluated for this type")


class EfficiencyMetrics(BaseModel):
    """Computational efficiency metrics."""
    avg_latency_ms: float = Field(0.0, description="Average inference latency per image (ms)")
    p50_latency_ms: float = Field(0.0, description="50th percentile latency (ms)")
    p95_latency_ms: float = Field(0.0, description="95th percentile latency (ms)")
    p99_latency_ms: float = Field(0.0, description="99th percentile latency (ms)")
    max_latency_ms: float = Field(0.0, description="Maximum latency (ms)")
    throughput_images_per_sec: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    memory_usage_mb: Optional[float] = None


class EvaluationResult(BaseModel):
    """Complete evaluation result for one run."""
    evaluation_id: str
    dataset_name: str
    dataset_split: str
    confidence_threshold: float
    overall_accuracy: float
    overall_precision: float
    overall_recall: float
    overall_f1_score: float
    mean_average_precision: float = Field(0.0, description="mAP across all violation types")
    false_positive_rate: float = 0.0
    false_negative_rate: float = 0.0
    total_samples: int = 0
    per_violation_metrics: List[ViolationMetrics] = Field(default_factory=list)
    per_camera_accuracy: Dict[str, float] = Field(default_factory=dict)
    efficiency: EfficiencyMetrics = Field(default_factory=EfficiencyMetrics)
    violation_types_evaluated: List[str] = Field(default_factory=list)
