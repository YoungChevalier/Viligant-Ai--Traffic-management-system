"""
audit_logger.py
Manages the immutable audit trail for review actions.
"""

import logging
from typing import Dict, Any, List
from libs.common_utils.time_utils import utc_now

logger = logging.getLogger(__name__)

# Mocked DB table for audit logs
_audit_logs: List[Dict[str, Any]] = []

def log_audit_action(incident_id: str, action_type: str, reviewer_id: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Records an immutable audit event for a given incident.
    """
    entry = {
        "incident_id": incident_id,
        "action_type": action_type,
        "reviewer_id": reviewer_id,
        "timestamp": utc_now().isoformat(),
        "metadata": metadata or {}
    }
    _audit_logs.append(entry)
    
    # In production:
    # db = next(get_db())
    # db.add(AuditLogModel(**entry))
    # db.commit()
    
    logger.info("AUDIT: [%s] %s by %s | %s", incident_id, action_type, reviewer_id, metadata)
    return entry

def get_audit_trail(incident_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves the full audit history for a specific incident.
    """
    # Sort chronologically (oldest first)
    logs = [log for log in _audit_logs if log["incident_id"] == incident_id]
    return sorted(logs, key=lambda x: x["timestamp"])
