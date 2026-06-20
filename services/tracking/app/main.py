from fastapi import FastAPI
from app.api.router import register_routes

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the Tracking Service FastAPI application.
    """
    app = FastAPI(
        title="Traffic Tracking Service",
        description="Maintains object tracks across consecutive frames using detection results.",
        version="0.1.0",
    )

    register_routes(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "tracking"}

    return app

app = create_app()
