"""
metrics.py
Core metric computation for classification evaluation.

All math is implemented from scratch — no sklearn dependency needed.
Supports per-class binary classification metrics and Average Precision.
"""

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


def compute_confusion_matrix(
    pairs: List[Tuple[Dict[str, Any], Dict[str, Any]]],
    confidence_threshold: float = 0.5,
) -> Dict[str, int]:
    """
    Computes confusion matrix counts from matched prediction–GT pairs.

    A prediction with confidence >= threshold and predicted_label == 1
    is treated as a positive prediction.

    Args:
        pairs: List of (prediction_dict, ground_truth_dict) tuples.
        confidence_threshold: Minimum confidence to accept a positive prediction.

    Returns:
        Dict with keys: tp, fp, tn, fn.
    """
    tp = fp = tn = fn = 0

    for pred, gt in pairs:
        true_label = gt.get("true_label", 0)
        pred_label = pred.get("predicted_label", 0)
        confidence = pred.get("confidence", 0.0)

        # Apply confidence threshold: if confidence < threshold, treat as negative
        effective_pred = 1 if (pred_label == 1 and confidence >= confidence_threshold) else 0

        if effective_pred == 1 and true_label == 1:
            tp += 1
        elif effective_pred == 1 and true_label == 0:
            fp += 1
        elif effective_pred == 0 and true_label == 0:
            tn += 1
        else:  # effective_pred == 0 and true_label == 1
            fn += 1

    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def compute_precision(tp: int, fp: int) -> float:
    """Precision = TP / (TP + FP). Returns 0.0 if denominator is 0."""
    denom = tp + fp
    return round(tp / denom, 4) if denom > 0 else 0.0


def compute_recall(tp: int, fn: int) -> float:
    """Recall = TP / (TP + FN). Returns 0.0 if denominator is 0."""
    denom = tp + fn
    return round(tp / denom, 4) if denom > 0 else 0.0


def compute_f1(precision: float, recall: float) -> float:
    """F1 = 2 * (precision * recall) / (precision + recall)."""
    denom = precision + recall
    return round(2 * precision * recall / denom, 4) if denom > 0 else 0.0


def compute_accuracy(tp: int, fp: int, tn: int, fn: int) -> float:
    """Accuracy = (TP + TN) / (TP + FP + TN + FN)."""
    total = tp + fp + tn + fn
    return round((tp + tn) / total, 4) if total > 0 else 0.0


def compute_false_positive_rate(fp: int, tn: int) -> float:
    """FPR = FP / (FP + TN)."""
    denom = fp + tn
    return round(fp / denom, 4) if denom > 0 else 0.0


def compute_false_negative_rate(fn: int, tp: int) -> float:
    """FNR = FN / (FN + TP)."""
    denom = fn + tp
    return round(fn / denom, 4) if denom > 0 else 0.0


def compute_average_precision(
    pairs: List[Tuple[Dict[str, Any], Dict[str, Any]]],
) -> float:
    """
    Computes Average Precision (AP) using the 11-point interpolation method.

    Sorts predictions by confidence (descending), then computes
    precision-recall at each threshold.

    Args:
        pairs: List of (prediction_dict, ground_truth_dict) tuples.

    Returns:
        AP score [0.0, 1.0].
    """
    if not pairs:
        return 0.0

    # Sort by confidence descending
    sorted_pairs = sorted(pairs, key=lambda p: p[0].get("confidence", 0.0), reverse=True)

    total_positives = sum(1 for _, gt in sorted_pairs if gt.get("true_label", 0) == 1)
    if total_positives == 0:
        return 0.0

    tp_cumulative = 0
    fp_cumulative = 0
    precisions = []
    recalls = []

    for pred, gt in sorted_pairs:
        true_label = gt.get("true_label", 0)
        if true_label == 1:
            tp_cumulative += 1
        else:
            fp_cumulative += 1

        prec = tp_cumulative / (tp_cumulative + fp_cumulative)
        rec = tp_cumulative / total_positives
        precisions.append(prec)
        recalls.append(rec)

    # 11-point interpolation
    ap = 0.0
    for t in [i / 10.0 for i in range(11)]:
        # Find max precision at recall >= t
        p_interp = 0.0
        for prec, rec in zip(precisions, recalls):
            if rec >= t:
                p_interp = max(p_interp, prec)
        ap += p_interp

    ap /= 11.0
    return round(ap, 4)


def compute_class_metrics(
    pairs: List[Tuple[Dict[str, Any], Dict[str, Any]]],
    violation_type: str,
    confidence_threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Computes all metrics for a single violation type.

    Args:
        pairs: Matched (prediction, ground_truth) pairs for this class.
        violation_type: Name of the violation class.
        confidence_threshold: Confidence threshold for classification.

    Returns:
        Dict with all metric values.
    """
    cm = compute_confusion_matrix(pairs, confidence_threshold)
    tp, fp, tn, fn = cm["tp"], cm["fp"], cm["tn"], cm["fn"]

    precision = compute_precision(tp, fp)
    recall = compute_recall(tp, fn)
    f1 = compute_f1(precision, recall)
    accuracy = compute_accuracy(tp, fp, tn, fn)
    ap = compute_average_precision(pairs)

    return {
        "violation_type": violation_type,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "average_precision": ap,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "support": tp + fn,  # number of actual positives
        "sample_count": tp + fp + tn + fn,
    }
