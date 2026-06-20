"""
feedback_collector.py
Collects false positives and false negatives from the human review workflow.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# MOCK: This simulates calling the dashboard-api to get recent audit logs
# where the reviewer REJECTED (False Positive) or MODIFIED (False Negative) the case.
def _mock_fetch_review_audit_logs(task: str) -> List[Dict[str, Any]]:
    # Simulated response from Dashboard API
    return [
        {
            "incident_id": f"inc-{task}-001",
            "action_type": "DECISION_REJECT",
            "metadata": {"notes": "False positive, not a violation"}
        },
        {
            "incident_id": f"inc-{task}-002",
            "action_type": "DECISION_MODIFY",
            "metadata": {"notes": "Incorrect class, updating label"}
        }
    ]

def collect_feedback_candidates(task: str) -> List[Dict[str, Any]]:
    """
    Polls the review system for cases that contradict the model's prediction.
    Converts them into retraining candidates.
    """
    logger.info(f"Querying dashboard-api for {task} feedback cases...")
    logs = _mock_fetch_review_audit_logs(task)
    
    candidates = []
    for log in logs:
        action = log.get("action_type")
        if action in ["DECISION_REJECT", "DECISION_MODIFY"]:
            # Determine reason
            reason = "FALSE_POSITIVE" if action == "DECISION_REJECT" else "FALSE_NEGATIVE"
            
            # Reconstruct candidate
            candidate = {
                "trace_id": log["incident_id"],
                "service_name": task,
                "reason": reason,
                "artifact_path": f"s3://storage/{log['incident_id']}/crop.jpg",
                "ground_truth": "NEGATIVE" if action == "DECISION_REJECT" else "CORRECTED_CLASS"
            }
            candidates.append(candidate)
            
    logger.info(f"Collected {len(candidates)} new feedback candidates for {task}.")
    return candidates
