import logging
from typing import Dict, Any, Optional, List

from libs.common_utils.id_utils import build_incident_id
from libs.common_utils.time_utils import utc_now

logger = logging.getLogger(__name__)

# In-memory store for development (replaced by DB queries in production)
_incident_store: Dict[str, Dict[str, Any]] = {}
_review_store: List[Dict[str, Any]] = []


async def list_incidents(status: Optional[str], violation_type: Optional[str], limit: int, offset: int) -> Dict[str, Any]:
    # (Keep your existing list_incidents implementation here, just make it async)
    results = list(_incident_store.values())
    if status:
        results = [r for r in results if r.get("status") == status]
    if violation_type:
        results = [r for r in results if r.get("primary_violation") == violation_type]
    results.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    page = results[offset : offset + limit]
    return {"total": len(results), "limit": limit, "offset": offset, "incidents": page}

async def load_incident_detail(incident_id: str) -> Optional[Dict[str, Any]]:
    # (Keep your existing load_incident_detail implementation here, just make it async)
    incident = _incident_store.get(incident_id)
    if not incident:
        return None
    reviews = [r for r in _review_store if r.get("incident_id") == incident_id]
    return {**incident, "reviews": reviews}

async def save_review_action(incident_id: str, request_data: Any) -> Dict[str, Any]:
    """
    Records a review action, updates incident status, and publishes downstream.
    """
    action = request_data.action
    reviewer_id = request_data.reviewer_id
    notes = request_data.notes

    # 1. Record the review action
    review_record = {
        "incident_id": incident_id,
        "reviewer_id": reviewer_id,
        "action": action,
        "notes": notes,
        "created_at": utc_now().isoformat(),
    }
    _review_store.append(review_record)

    # 2. Update incident status
    status_map = {
        "APPROVE": "APPROVED",
        "REJECT": "REJECTED",
        "ESCALATE": "ESCALATED",
    }
    new_status = status_map.get(action, "OPEN")
    
    incident = _incident_store.get(incident_id)
    if incident:
        incident["status"] = new_status
        incident["updated_at"] = utc_now().isoformat()
    else:
        # Mocking creation if we are testing the endpoint directly without full pipeline
        _incident_store[incident_id] = {"incident_id": incident_id, "status": new_status}

    # 3. Persist State (MOCKED DB)
    # db = next(get_db())
    # # Save review to review_actions table and update incidents table
    # db.commit()
    logger.info(f"Review action recorded | incident_id={incident_id} | action={action} | reviewer={reviewer_id}")

    # 4. Publish to Downstream Queue (MOCKED)
    # In production, ONLY publish to the enforcement/challan queue if APPROVED.
    if new_status == "APPROVED":
        downstream_job = {
            "incident_id": incident_id,
            "status": new_status,
            "reviewer_id": reviewer_id
        }
        logger.info(f"Incident {incident_id} published to downstream enforcement queue: {downstream_job}")
    else:
        logger.info(f"Incident {incident_id} status is {new_status}. No enforcement action required.")

    return {
        "incident_id": incident_id,
        "action": action,
        "new_status": new_status,
        "queue_status": "published" if new_status == "APPROVED" else "none"
    }


async def get_incident_stats() -> Dict[str, Any]:
    """
    Aggregates dashboard KPI statistics from the incident store:
    total count, breakdown by status, violation type, camera, and daily trend.
    """
    all_incidents = list(_incident_store.values())

    by_status: Dict[str, int] = {}
    by_violation: Dict[str, int] = {}
    by_camera: Dict[str, int] = {}
    by_day: Dict[str, int] = {}

    for inc in all_incidents:
        # Status counts
        status = inc.get("status", "UNKNOWN")
        by_status[status] = by_status.get(status, 0) + 1

        # Violation type counts
        v_type = inc.get("primary_violation", "UNKNOWN")
        by_violation[v_type] = by_violation.get(v_type, 0) + 1

        # Camera counts
        cam = inc.get("camera_id", "UNKNOWN")
        by_camera[cam] = by_camera.get(cam, 0) + 1

        # Daily trend (extract date from ISO timestamp)
        ts = inc.get("timestamp") or inc.get("created_at", "")
        day = ts[:10] if len(ts) >= 10 else "UNKNOWN"
        by_day[day] = by_day.get(day, 0) + 1

    # Sort cameras by count descending, keep top 10
    top_cameras = dict(sorted(by_camera.items(), key=lambda x: x[1], reverse=True)[:10])
    # Sort days chronologically
    sorted_days = dict(sorted(by_day.items()))

    return {
        "total": len(all_incidents),
        "by_status": by_status,
        "by_violation_type": by_violation,
        "by_camera": top_cameras,
        "by_day": sorted_days,
    }
