from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import register_routes

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the Dashboard API FastAPI application.
    """
    app = FastAPI(
        title="Traffic Dashboard API",
        description="Serves incident data, evidence assets, and review actions to the frontend.",
        version="0.1.0",
    )

    import os
    cors_origin = os.getenv("CORS_ORIGIN", "*")
    origins = [origin.strip() for origin in cors_origin.split(",")] if cors_origin != "*" else ["*"]

    # Enable CORS for frontend clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.db.database import engine, Base
    from app.models import domain # ensure models are loaded
    
    # Create tables
    Base.metadata.create_all(bind=engine)

    register_routes(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "dashboard-api"}

    return app

app = create_app()
