"""
review_assignment.py
Handles the assignment of review cases to human operators.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Mocked state: Mapping of incident_id -> assigned reviewer_id
_assignments: Dict[str, str] = {}

# Mocked list of available reviewers
AVAILABLE_REVIEWERS = ["reviewer_01", "reviewer_02", "reviewer_admin"]

# Simple counter for round-robin assignment
_round_robin_index = 0

def get_assignment(incident_id: str) -> Optional[str]:
    """Returns the currently assigned reviewer ID, or None."""
    return _assignments.get(incident_id)

def assign_case(incident_id: str, reviewer_id: Optional[str] = None, force: bool = False) -> str:
    """
    Assigns an incident to a reviewer.
    If no reviewer_id is provided, auto-assigns using round-robin.
    If already assigned, respects the lock unless force=True.
    """
    global _round_robin_index
    
    current_assignee = _assignments.get(incident_id)
    if current_assignee and not force:
        logger.info("Incident %s is already assigned to %s. Use force=True to reassign.", incident_id, current_assignee)
        return current_assignee

    if not reviewer_id:
        # Auto-assign (Round Robin)
        reviewer_id = AVAILABLE_REVIEWERS[_round_robin_index % len(AVAILABLE_REVIEWERS)]
        _round_robin_index += 1

    _assignments[incident_id] = reviewer_id
    logger.info("Assigned incident %s to reviewer %s", incident_id, reviewer_id)
    
    return reviewer_id
