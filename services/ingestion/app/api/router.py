from fastapi import APIRouter, FastAPI

router = APIRouter()

@router.post("/frames/ingest")
async def ingest_frame():
    """
    Endpoint to receive a raw camera frame for ingestion.
    Business logic will be wired in a later task.
    """
    return {"message": "frame accepted"}

@router.get("/frames/status")
async def ingestion_status():
    """
    Endpoint to check the current ingestion pipeline status.
    """
    return {"status": "idle"}

def register_routes(app: FastAPI) -> None:
    """
    Registers all ingestion API routes onto the given FastAPI application.
    """
    app.include_router(router, prefix="/api/v1", tags=["ingestion"])
