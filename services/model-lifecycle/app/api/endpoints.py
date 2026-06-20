from fastapi import APIRouter, HTTPException
from app.api.schemas import (
    RetrainingCandidate, 
    ModelRegistration, 
    ModelStatusUpdate,
    RetrainingJobRequest,
    RetrainingJobResponse
)

router = APIRouter()

# --- Legacy Model Lifecycle Endpoints ---

@router.post("/lifecycle/candidates/intake")
async def post_intake_candidate(candidate: RetrainingCandidate):
    from app.services.lifecycle_service import intake_candidate
    try:
        result = await intake_candidate(candidate)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lifecycle/datasets/create")
async def post_create_dataset(task: str):
    from app.services.lifecycle_service import create_dataset_version
    try:
        return await create_dataset_version(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lifecycle/models/register")
async def post_register_model(model: ModelRegistration):
    from app.services.lifecycle_service import register_model
    try:
        return await register_model(model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/lifecycle/models/{model_name}/{version}/status")
async def put_model_status(model_name: str, version: str, update: ModelStatusUpdate):
    from app.services.lifecycle_service import promote_model
    try:
        result = await promote_model(model_name, version, update.status)
        return {"status": "success", "data": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NEW: End-to-End Retraining Loop Endpoints ---

@router.post("/lifecycle/retrain/trigger")
async def trigger_retraining_loop(request: RetrainingJobRequest):
    """
    Kicks off an async retraining pipeline: 
    feedback collection -> dataset -> training -> evaluation -> promotion
    """
    from app.services.lifecycle_service import trigger_end_to_end_retraining
    try:
        job_id = await trigger_end_to_end_retraining(request.task, request.model_name)
        return {"status": "success", "job_id": job_id, "message": "Retraining job queued asynchronously."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lifecycle/retrain/{job_id}/status", response_model=RetrainingJobResponse)
async def get_retraining_status(job_id: str):
    """
    Polls the status and eventual evaluation results of a retraining pipeline.
    """
    from app.services.lifecycle_service import get_retraining_job_status
    try:
        job_data = get_retraining_job_status(job_id)
        
        # Map raw dictionary to Response Schema
        return RetrainingJobResponse(
            job_id=job_data["job_id"],
            status=job_data["status"],
            dataset_id=job_data.get("dataset_id", "PENDING"),
            baseline_metrics=job_data.get("baseline_metrics"),
            new_metrics=job_data.get("new_metrics"),
            deployment_decision=job_data.get("deployment_decision"),
            new_version=job_data.get("new_version")
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
