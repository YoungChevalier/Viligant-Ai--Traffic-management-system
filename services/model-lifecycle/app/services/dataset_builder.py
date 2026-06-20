"""
dataset_builder.py
Creates structured, stratified datasets from raw retraining candidates.
"""

import uuid
import logging
from typing import List, Dict, Any
from libs.common_utils.time_utils import utc_now

logger = logging.getLogger(__name__)

def build_stratified_dataset(task: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compiles candidates into a simulated dataset object.
    Computes stratification metadata (e.g., how many False Positives vs False Negatives).
    """
    dataset_id = f"ds-{task}-{uuid.uuid4().hex[:6]}"
    
    # Stratification counting
    stratification = {
        "FALSE_POSITIVE": 0,
        "FALSE_NEGATIVE": 0,
        "LOW_CONFIDENCE": 0,
        "TOTAL": len(candidates)
    }
    
    for c in candidates:
        reason = c.get("reason", "UNKNOWN")
        if reason in stratification:
            stratification[reason] += 1
            
    dataset_record = {
        "dataset_id": dataset_id,
        "task": task,
        "candidate_count": len(candidates),
        "created_at": utc_now().isoformat(),
        "stratification": stratification,
        "status": "READY_FOR_TRAINING",
        # In production: "s3_uri": f"s3://datasets/{dataset_id}/annotations.json"
    }
    
    logger.info(f"Built stratified dataset {dataset_id} for {task}. Stratification: {stratification}")
    return dataset_record
