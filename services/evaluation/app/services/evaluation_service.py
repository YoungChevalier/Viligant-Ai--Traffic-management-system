"""
evaluation_service.py
Core orchestrator for running performance evaluations.

Loads ground truth, matches predictions, computes metrics across all
requested slices (overall, per-class, per-camera), and outputs the
EvaluationResult schema.
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional

from app.api.schemas import (
    EvaluationRequest,
    EvaluationResult,
    ViolationMetrics,
    EfficiencyMetrics,
)
from app.services.ground_truth import load_ground_truth, match_predictions_to_ground_truth
from app.services.metrics import (
    compute_confusion_matrix,
    compute_precision,
    compute_recall,
    compute_f1,
    compute_accuracy,
    compute_false_positive_rate,
    compute_false_negative_rate,
    compute_average_precision,
    compute_class_metrics,
)
from app.services.efficiency import compute_efficiency_metrics

import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


def _group_pairs_by_violation(
    pairs: List[tuple],
) -> Dict[str, List[tuple]]:
    """Groups prediction-GT pairs by the true violation type."""
    grouped = defaultdict(list)
    for pred, gt in pairs:
        # Use ground truth type as the definitive class bucket
        vtype = gt["violation_type"]
        grouped[vtype].append((pred, gt))
    return dict(grouped)


def _group_pairs_by_camera(
    pairs: List[tuple],
) -> Dict[str, List[tuple]]:
    """Groups prediction-GT pairs by camera ID."""
    grouped = defaultdict(list)
    for pred, gt in pairs:
        cam_id = gt.get("camera_id") or pred.get("camera_id") or "unknown"
        grouped[cam_id].append((pred, gt))
    return dict(grouped)


async def run_evaluation(request: EvaluationRequest) -> EvaluationResult:
    """
    Executes a full evaluation run.

    1. Load ground truth (from request or fallback to mocked dataset)
    2. Match predictions to ground truth
    3. Filter by requested violation_types or camera_ids
    4. Compute per-violation-type metrics
    5. Compute overall (system-wide) metrics
    6. Compute per-camera metrics
    7. Compute efficiency metrics
    8. Persist results (Mocked)
    """
    eval_id = request.evaluation_id or f"eval-{uuid.uuid4().hex[:8]}"
    logger.info("Starting evaluation run: %s on dataset %s", eval_id, request.dataset_name)

    # 1. Ground Truth
    ground_truths = [gt.model_dump() for gt in request.ground_truths]
    if not ground_truths:
        logger.info("No ground truth in request. Attempting to load from dataset %s", request.dataset_name)
        ground_truths = load_ground_truth(request.dataset_name) or []
    
    if not ground_truths:
        raise ValueError(f"No ground truth data available for dataset {request.dataset_name}")

    # 2. Match pairs
    predictions = [p.model_dump() for p in request.predictions]
    pairs = match_predictions_to_ground_truth(predictions, ground_truths)

    if not pairs:
        raise ValueError("No matching prediction-ground truth pairs found")

    # 3. Filter pairs based on request
    filtered_pairs = pairs
    if request.violation_types:
        filtered_pairs = [
            (p, gt) for p, gt in filtered_pairs
            if gt["violation_type"] in request.violation_types
        ]
    
    if request.camera_ids:
        filtered_pairs = [
            (p, gt) for p, gt in filtered_pairs
            if gt.get("camera_id") in request.camera_ids
        ]

    logger.info("Evaluating %d pairs after filtering", len(filtered_pairs))

    # 4. Per-violation metrics
    grouped_by_type = _group_pairs_by_violation(filtered_pairs)
    per_violation_results = []
    
    for vtype, class_pairs in grouped_by_type.items():
        metrics_dict = compute_class_metrics(class_pairs, vtype, request.confidence_threshold)
        per_violation_results.append(ViolationMetrics(**metrics_dict))

    # 5. Overall System Metrics
    overall_cm = compute_confusion_matrix(filtered_pairs, request.confidence_threshold)
    tp, fp, tn, fn = overall_cm["tp"], overall_cm["fp"], overall_cm["tn"], overall_cm["fn"]

    overall_accuracy = compute_accuracy(tp, fp, tn, fn)
    overall_precision = compute_precision(tp, fp)
    overall_recall = compute_recall(tp, fn)
    overall_f1 = compute_f1(overall_precision, overall_recall)
    
    fpr = compute_false_positive_rate(fp, tn)
    fnr = compute_false_negative_rate(fn, tp)

    # Overall mAP is mean of per-class APs
    class_aps = [r.average_precision for r in per_violation_results]
    mean_ap = sum(class_aps) / len(class_aps) if class_aps else 0.0

    # 6. Per-camera metrics (accuracy only for simplicity)
    grouped_by_camera = _group_pairs_by_camera(filtered_pairs)
    per_camera_acc = {}
    for cam_id, cam_pairs in grouped_by_camera.items():
        cam_cm = compute_confusion_matrix(cam_pairs, request.confidence_threshold)
        acc = compute_accuracy(cam_cm["tp"], cam_cm["fp"], cam_cm["tn"], cam_cm["fn"])
        per_camera_acc[cam_id] = acc

    # 7. Efficiency metrics
    eff_dict = compute_efficiency_metrics(
        predictions=predictions,
        throughput_images_per_sec=request.throughput_images_per_sec,
        cpu_usage_percent=request.cpu_usage_percent,
        memory_usage_mb=request.memory_usage_mb,
    )
    efficiency = EfficiencyMetrics(**eff_dict)

    # Build final result
    result = EvaluationResult(
        evaluation_id=eval_id,
        dataset_name=request.dataset_name,
        dataset_split=request.dataset_split,
        confidence_threshold=request.confidence_threshold,
        overall_accuracy=overall_accuracy,
        overall_precision=overall_precision,
        overall_recall=overall_recall,
        overall_f1_score=overall_f1,
        mean_average_precision=round(mean_ap, 4),
        false_positive_rate=fpr,
        false_negative_rate=fnr,
        total_samples=len(filtered_pairs),
        per_violation_metrics=per_violation_results,
        per_camera_accuracy=per_camera_acc,
        efficiency=efficiency,
        violation_types_evaluated=list(grouped_by_type.keys()),
    )

    # 8. Persist results (Mocked)
    logger.info("Saving evaluation results for %s (Mocked DB persist)", eval_id)
    # In production:
    # db = next(get_db())
    # db.add(EvaluationRecord(**result.dict()))
    # db.commit()

    return result
