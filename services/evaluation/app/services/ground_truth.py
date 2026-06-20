"""
ground_truth.py
Ground-truth dataset loader and sample-matching utilities.

MOCKED: Provides sample ground-truth datasets for development.
In production, this would load from a labeled dataset store,
annotation database, or COCO-format JSON files.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ── Mocked Ground-Truth Datasets ───────────────────────────────────────────

_MOCK_DATASETS: Dict[str, List[Dict[str, Any]]] = {
    "helmet-val-v1": [
        {"sample_id": "img-001", "violation_type": "NO_HELMET", "true_label": 1, "camera_id": "cam-01"},
        {"sample_id": "img-002", "violation_type": "NO_HELMET", "true_label": 0, "camera_id": "cam-01"},
        {"sample_id": "img-003", "violation_type": "NO_HELMET", "true_label": 1, "camera_id": "cam-02"},
        {"sample_id": "img-004", "violation_type": "NO_HELMET", "true_label": 1, "camera_id": "cam-02"},
        {"sample_id": "img-005", "violation_type": "NO_HELMET", "true_label": 0, "camera_id": "cam-01"},
    ],
    "multi-violation-test-v1": [
        {"sample_id": "img-101", "violation_type": "NO_HELMET", "true_label": 1, "camera_id": "cam-01"},
        {"sample_id": "img-102", "violation_type": "NO_HELMET", "true_label": 0, "camera_id": "cam-01"},
        {"sample_id": "img-103", "violation_type": "RED_LIGHT", "true_label": 1, "camera_id": "cam-02"},
        {"sample_id": "img-104", "violation_type": "RED_LIGHT", "true_label": 0, "camera_id": "cam-02"},
        {"sample_id": "img-105", "violation_type": "WRONG_WAY", "true_label": 1, "camera_id": "cam-03"},
        {"sample_id": "img-106", "violation_type": "WRONG_WAY", "true_label": 0, "camera_id": "cam-03"},
        {"sample_id": "img-107", "violation_type": "ILLEGAL_PARKING", "true_label": 1, "camera_id": "cam-01"},
        {"sample_id": "img-108", "violation_type": "TRIPLE_RIDING", "true_label": 1, "camera_id": "cam-02"},
        {"sample_id": "img-109", "violation_type": "NO_SEATBELT", "true_label": 0, "camera_id": "cam-03"},
        {"sample_id": "img-110", "violation_type": "NO_SEATBELT", "true_label": 1, "camera_id": "cam-01"},
    ],
}


def load_ground_truth(dataset_name: str) -> Optional[List[Dict[str, Any]]]:
    """
    Loads a ground-truth dataset by name.

    MOCKED: Returns in-memory sample data. In production, this would:
      - Load from a COCO-format annotation JSON
      - Query a labeled dataset database
      - Read from a cloud storage annotation bucket

    Args:
        dataset_name: Name of the dataset to load.

    Returns:
        List of ground-truth entry dicts, or None if not found.
    """
    data = _MOCK_DATASETS.get(dataset_name)
    if data is None:
        logger.warning("Ground-truth dataset '%s' not found (Mocked)", dataset_name)
        return None

    logger.info(
        "Loaded ground-truth dataset '%s' with %d samples (Mocked)",
        dataset_name, len(data),
    )
    return data


def match_predictions_to_ground_truth(
    predictions: List[Dict[str, Any]],
    ground_truths: List[Dict[str, Any]],
) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """
    Matches prediction entries to ground-truth entries by sample_id.

    Only matched pairs are returned. Unmatched predictions and ground
    truths are logged as warnings.

    Args:
        predictions: List of prediction dicts with 'sample_id'.
        ground_truths: List of ground-truth dicts with 'sample_id'.

    Returns:
        List of (prediction, ground_truth) tuples.
    """
    gt_map = {gt["sample_id"]: gt for gt in ground_truths}
    matched = []
    unmatched_preds = []

    for pred in predictions:
        sid = pred["sample_id"]
        gt = gt_map.pop(sid, None)
        if gt is not None:
            matched.append((pred, gt))
        else:
            unmatched_preds.append(sid)

    if unmatched_preds:
        logger.warning(
            "%d predictions have no matching ground truth: %s",
            len(unmatched_preds), unmatched_preds[:5],
        )
    if gt_map:
        logger.warning(
            "%d ground truths have no matching prediction: %s",
            len(gt_map), list(gt_map.keys())[:5],
        )

    logger.info("Matched %d prediction–ground-truth pairs", len(matched))
    return matched
