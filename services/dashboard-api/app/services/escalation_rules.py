"""
escalation_rules.py
Handles automatic and manual escalation of review cases.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Configurable thresholds
AUTO_ESCALATE_CONFIDENCE_THRESHOLD = 0.60
HIGH_PRIORITY_VIOLATIONS = ["RED_LIGHT", "WRONG_WAY"]

def check_auto_escalation(incident: Dict[str, Any]) -> str:
    """
    Evaluates an incident to see if it should bypass standard review and
    be escalated immediately.
    
    Returns the target tier (e.g., "TIER_2", "ADMIN"), or None if no escalation needed.
    """
    confidence = incident.get("confidence", 1.0)
    violation_type = incident.get("primary_violation", "")
    
    # Low confidence predictions require Senior Review (Tier 2)
    if confidence < AUTO_ESCALATE_CONFIDENCE_THRESHOLD:
        logger.info("Auto-escalating to TIER_2 due to low confidence (%.2f)", confidence)
        return "TIER_2"
        
    # Certain high priority or complex violations might go straight to Admin
    # (Just an example rule)
    if violation_type in HIGH_PRIORITY_VIOLATIONS and confidence < 0.70:
        logger.info("Auto-escalating to ADMIN due to high-priority violation with moderate confidence")
        return "ADMIN"
        
    return None

def process_manual_escalation(incident_id: str, current_tier: str, target_tier: str, reason: str) -> bool:
    """
    Processes a manual escalation request from a reviewer.
    """
    # In production, we'd update the incident's routing tier in the DB.
    logger.info("Manual escalation for %s: %s -> %s (Reason: %s)", incident_id, current_tier, target_tier, reason)
    return True
