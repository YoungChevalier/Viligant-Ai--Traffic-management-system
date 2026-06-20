from fastapi import APIRouter, FastAPI, HTTPException
from app.api.endpoints import router as endpoints_router


stats_router = APIRouter()


@stats_router.get("/incidents/stats")
async def get_incident_stats():
    """
    Returns aggregated KPI statistics for the dashboard:
    total count, breakdown by status, violation type, camera, and daily trend.
    """
    from app.services.incident_queries import get_incident_stats as _get_stats
    try:
        return await _get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def register_routes(app: FastAPI) -> None:
    """
    Registers all dashboard-api routes onto the given FastAPI application.
    """
    app.include_router(endpoints_router, tags=["incidents"])
    app.include_router(stats_router, tags=["stats"])
