from fastapi import FastAPI
from app.api.endpoints import router as eval_router
import logging

logging.basicConfig(level=logging.INFO)

def create_app() -> FastAPI:
    """
    Factory function to create the evaluation service FastAPI application.
    """
    app = FastAPI(
        title="Performance Evaluation Service",
        description="Traffic Violation Evaluation and Benchmarking API",
        version="1.0.0",
    )

    app.include_router(eval_router, prefix="/api/v1")

    return app

app = create_app()
