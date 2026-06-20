"""
evaluation_comparator.py
Evaluates newly trained models and compares them against the production baseline.
"""

import logging
import random
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

# MOCK: In production, this would call `services/evaluation/` to run a full benchmark.
def _mock_run_evaluation(model_name: str, task: str) -> Dict[str, float]:
    """Generates slightly randomized but generally high metrics for the new model."""
    if task == "classification":
        return {"f1": round(random.uniform(0.86, 0.95), 3), "precision": 0.90, "recall": 0.88}
    else:
        return {"map": round(random.uniform(0.76, 0.90), 3), "map_50": 0.92}

def _mock_get_baseline_metrics(task: str) -> Dict[str, float]:
    """Returns the metrics of the current model in PRODUCTION."""
    if task == "classification":
        return {"f1": 0.85, "precision": 0.84, "recall": 0.86}
    else:
        return {"map": 0.75, "map_50": 0.85}

def evaluate_and_compare(model_name: str, task: str) -> Tuple[Dict[str, float], Dict[str, float], bool]:
    """
    Runs evaluation on the new model, fetches baseline metrics, and decides if
    the new model is strictly better than the baseline.
    Returns: (baseline_metrics, new_metrics, is_better)
    """
    logger.info(f"Running evaluation benchmark for retrained {model_name}...")
    new_metrics = _mock_run_evaluation(model_name, task)
    baseline_metrics = _mock_get_baseline_metrics(task)
    
    # Comparison Logic
    is_better = False
    if task == "classification":
        is_better = new_metrics.get("f1", 0) > baseline_metrics.get("f1", 0)
    else:
        is_better = new_metrics.get("map", 0) > baseline_metrics.get("map", 0)
        
    logger.info(f"Evaluation complete. Baseline: {baseline_metrics} | New: {new_metrics} | Is Better: {is_better}")
    
    return baseline_metrics, new_metrics, is_better
