from fastapi import FastAPI
from app.api.router import register_routes

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the Ingestion Service FastAPI application.
    """
    app = FastAPI(
        title="Traffic Ingestion Service",
        description="Receives raw camera frames and publishes them to the processing pipeline.",
        version="0.1.0",
    )

    register_routes(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "ingestion"}

    return app

app = create_app()
