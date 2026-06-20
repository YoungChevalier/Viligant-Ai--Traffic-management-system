from fastapi import FastAPI
from app.api.router import register_routes

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the Preprocessing Service FastAPI application.
    """
    app = FastAPI(
        title="Traffic Preprocessing Service",
        description="Performs frame quality checks, normalization, and enhancement before detection.",
        version="0.1.0",
    )

    register_routes(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "preprocessing"}

    return app

app = create_app()
