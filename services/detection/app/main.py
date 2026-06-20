from fastapi import FastAPI
from app.api.router import register_routes

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the Detection Service FastAPI application.
    """
    app = FastAPI(
        title="Traffic Detection Service",
        description="Runs object detection inference on preprocessed frames.",
        version="0.1.0",
    )

    register_routes(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "detection"}

    return app

app = create_app()
