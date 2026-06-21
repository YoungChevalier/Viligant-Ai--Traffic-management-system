from fastapi import APIRouter, FastAPI, HTTPException
from app.api.endpoints_legacy import router as endpoints_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.cases import router as cases_router
from app.api.endpoints.dashboard import router as dashboard_router
from app.api.endpoints.cameras import router as cameras_router
from app.api.endpoints.alerts import router as alerts_router
from app.api.endpoints.settings import router as settings_router


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
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(cases_router, prefix="/api/cases", tags=["cases"])
    app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(cameras_router, prefix="/api/cameras", tags=["cameras"])
    app.include_router(alerts_router, prefix="/api/alerts", tags=["alerts"])
    app.include_router(settings_router, prefix="/api/settings", tags=["settings"])
