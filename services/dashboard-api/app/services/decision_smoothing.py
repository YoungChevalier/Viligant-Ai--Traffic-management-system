"""
decision_smoothing.py
Analyzes review decisions to detect patterns (e.g., repeated false positives)
and applies smoothing logic (like recommending threshold adjustments).
"""

import logging
from typing import Dict, Any, List
from collections import defaultdict

logger = logging.getLogger(__name__)

# State for mocked pattern tracking: reviewer_id -> violation_type -> reject_count
_rejection_history = defaultdict(lambda: defaultdict(int))

# If a reviewer rejects the same violation type this many times, flag it.
REJECTION_FLAG_THRESHOLD = 5

def record_decision_for_smoothing(reviewer_id: str, violation_type: str, action: str):
    """
    Updates the running history of decisions to detect systemic issues.
    """
    if action == "REJECT":
        _rejection_history[reviewer_id][violation_type] += 1
        count = _rejection_history[reviewer_id][violation_type]
        
        if count >= REJECTION_FLAG_THRESHOLD:
            logger.warning(
                "SMOOTHING ALERT: Reviewer %s has rejected %s %d times recently. "
                "Consider increasing the confidence threshold or retraining the model.",
                reviewer_id, violation_type, count
            )
            # In a real system, we might emit an event to the model-monitoring service here.
            
    elif action == "APPROVE":
        # Reset or decrease the counter on approval
        current = _rejection_history[reviewer_id][violation_type]
        _rejection_history[reviewer_id][violation_type] = max(0, current - 1)


def get_recommended_threshold(violation_type: str, current_threshold: float) -> float:
    """
    Suggests a new confidence threshold based on aggregate rejection patterns.
    (Simplified mock logic)
    """
    total_rejects = sum(_rejection_history[rev][violation_type] for rev in _rejection_history)
    if total_rejects > 10:
        suggested = min(0.95, current_threshold + 0.05)
        logger.info("Suggesting threshold increase for %s to %.2f", violation_type, suggested)
        return suggested
    return current_threshold
