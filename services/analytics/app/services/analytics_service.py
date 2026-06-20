import logging
from typing import Dict, Any, Optional, List

# MOCK: If DB (e.g. ElasticSearch/ClickHouse) is not ready, we mock the projection store.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Mocked read-model projection store
_projection_store: Dict[str, Dict[str, Any]] = {}

async def project_case_event(event_data: Any) -> Dict[str, Any]:
    """
    Projects a reviewed-case event into the searchable read model.
    """
    case_id = event_data.incident_id
    
    # In production, this would upsert into ElasticSearch, ClickHouse, or a PostgreSQL JSONB column.
    projection_record = event_data.model_dump()
    _projection_store[case_id] = projection_record
    
    logger.info(f"Projected case {case_id} into analytics read model (Mocked)")
    
    return {"incident_id": case_id, "projection_status": "saved"}

async def search_cases(
    plate: Optional[str],
    violation_type: Optional[str],
    status: Optional[str],
    camera_id: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
    limit: int,
    offset: int
) -> Dict[str, Any]:
    """
    Searches the projected cases based on multiple filters.
    """
    results = list(_projection_store.values())

    # Apply filters
    if plate:
        results = [r for r in results if plate.upper() in (r.get("plate_text") or "").upper()]
    if violation_type:
        results = [r for r in results if r.get("primary_violation") == violation_type]
    if status:
        results = [r for r in results if r.get("status") == status]
    if camera_id:
        results = [r for r in results if r.get("camera_id") == camera_id]
    if start_date:
        results = [r for r in results if r.get("timestamp") >= start_date]
    if end_date:
        results = [r for r in results if r.get("timestamp") <= end_date]

    # Sort descending by timestamp
    results.sort(key=lambda r: r.get("timestamp", ""), reverse=True)

    total = len(results)
    page = results[offset: offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": page
    }

async def get_case(case_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single projected case."""
    return _projection_store.get(case_id)

async def generate_summary() -> Dict[str, Any]:
    """
    Generates analytics aggregations (counts by type, status, top cameras).
    """
    all_cases = list(_projection_store.values())
    
    by_violation = {}
    by_status = {}
    by_camera = {}

    for c in all_cases:
        v_type = c.get("primary_violation", "UNKNOWN")
        stat = c.get("status", "UNKNOWN")
        cam = c.get("camera_id", "UNKNOWN")

        by_violation[v_type] = by_violation.get(v_type, 0) + 1
        by_status[stat] = by_status.get(stat, 0) + 1
        by_camera[cam] = by_camera.get(cam, 0) + 1

    # Top cameras (sort dict by value descending and take top 5)
    top_cameras_list = sorted(by_camera.items(), key=lambda item: item[1], reverse=True)[:5]
    top_cameras = {k: v for k, v in top_cameras_list}

    return {
        "total_cases": len(all_cases),
        "by_violation_type": by_violation,
        "by_status": by_status,
        "top_cameras": top_cameras
    }
