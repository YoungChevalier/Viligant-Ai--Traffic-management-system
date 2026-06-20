import logging
import uuid
import asyncio
from typing import Dict, Any, List
from libs.common_utils.time_utils import utc_now

from app.api.schemas import RetrainingJobResponse, ModelRegistration
from app.services.feedback_collector import collect_feedback_candidates
from app.services.dataset_builder import build_stratified_dataset
from app.services.training_orchestrator import queue_retraining_job, get_job_status
from app.services.evaluation_comparator import evaluate_and_compare

logger = logging.getLogger(__name__)

# Mocked stores for ML Lifecycle
_candidates_store: List[Dict[str, Any]] = []
_datasets_store: Dict[str, Dict[str, Any]] = {}
_model_registry: Dict[str, Dict[str, Any]] = {}

# Retraining Jobs store
_retraining_jobs: Dict[str, Dict[str, Any]] = {}

# Simple Promotion Gates
PROMOTION_GATES = {
    "classification": {"min_f1": 0.85},
    "detection": {"min_map": 0.75}
}

async def intake_candidate(candidate_data: Any) -> Dict[str, Any]:
    """Saves a challenging example to the retraining backlog."""
    record = candidate_data.model_dump()
    record["ingested_at"] = utc_now().isoformat()
    _candidates_store.append(record)
    return {"trace_id": candidate_data.trace_id, "status": "QUEUED_FOR_RETRAINING"}

async def create_dataset_version(task: str) -> Dict[str, Any]:
    """Abstracts queued candidates into an immutable dataset for training."""
    dataset_id = f"ds-{task}-{uuid.uuid4().hex[:6]}"
    relevant_candidates = [c for c in _candidates_store if c.get("service_name") == task]
    
    dataset_record = {
        "dataset_id": dataset_id,
        "task": task,
        "candidate_count": len(relevant_candidates),
        "created_at": utc_now().isoformat(),
        "status": "READY_FOR_TRAINING"
    }
    
    _datasets_store[dataset_id] = dataset_record
    return dataset_record

async def register_model(registration: Any) -> Dict[str, Any]:
    """Registers metadata for a newly trained model candidate."""
    registry_key = f"{registration.model_name}_{registration.version}"
    record = registration.model_dump()
    record["status"] = "EXPERIMENTAL"
    record["registered_at"] = utc_now().isoformat()
    
    _model_registry[registry_key] = record
    return {"registry_key": registry_key, "status": "EXPERIMENTAL"}

async def promote_model(model_name: str, version: str, target_status: str) -> Dict[str, Any]:
    """Evaluates validation gates before allowing promotion."""
    registry_key = f"{model_name}_{version}"
    model = _model_registry.get(registry_key)
    
    if not model:
        raise ValueError(f"Model {registry_key} not found in registry.")
        
    task = model["task"]
    metrics = model["metrics"]
    
    if target_status in ["STAGING", "PRODUCTION"]:
        gates = PROMOTION_GATES.get(task, {})
        if task == "classification" and metrics.get("f1", 0) < gates.get("min_f1", 0):
            raise ValueError("Promotion rejected: F1 Score too low.")
        if task == "detection" and metrics.get("map", 0) < gates.get("min_map", 0):
            raise ValueError("Promotion rejected: mAP too low.")
            
    model["status"] = target_status
    return {"registry_key": registry_key, "new_status": target_status}


# --- NEW: END-TO-END RETRAINING LOOP ---

async def trigger_end_to_end_retraining(task: str, base_model_name: str) -> str:
    """
    Kicks off the end-to-end retraining pipeline.
    Returns the Job ID immediately while processing happens asynchronously.
    """
    job_id = f"retrain-{uuid.uuid4().hex[:6]}"
    _retraining_jobs[job_id] = {
        "job_id": job_id,
        "status": "INITIALIZING",
        "task": task,
        "base_model": base_model_name
    }
    
    # Run async pipeline in background
    asyncio.create_task(_run_retraining_pipeline(job_id, task, base_model_name))
    
    return job_id

async def _run_retraining_pipeline(job_id: str, task: str, base_model_name: str):
    """The core pipeline executing the 5 steps."""
    job = _retraining_jobs[job_id]
    try:
        # Step 1: Collect Feedback
        job["status"] = "COLLECTING_FEEDBACK"
        candidates = collect_feedback_candidates(task)
        
        # Step 2: Build Dataset
        job["status"] = "BUILDING_DATASET"
        dataset_record = build_stratified_dataset(task, candidates)
        _datasets_store[dataset_record["dataset_id"]] = dataset_record
        job["dataset_id"] = dataset_record["dataset_id"]
        job["dataset_stratification"] = dataset_record.get("stratification")
        
        # Step 3: Trigger Training (Wait for completion)
        job["status"] = "TRAINING"
        gpu_job_id = await queue_retraining_job(task, base_model_name, dataset_record["dataset_id"])
        
        # Poll for training completion
        while get_job_status(gpu_job_id) in ["PENDING", "RUNNING"]:
            await asyncio.sleep(0.5)
            
        if get_job_status(gpu_job_id) == "FAILED":
            job["status"] = "FAILED_AT_TRAINING"
            return
            
        # Step 4: Evaluate and Compare
        job["status"] = "EVALUATING"
        new_version = f"v_retrained_{uuid.uuid4().hex[:4]}"
        baseline_metrics, new_metrics, is_better = evaluate_and_compare(base_model_name, task)
        
        job["baseline_metrics"] = baseline_metrics
        job["new_metrics"] = new_metrics
        
        # Step 5: Conditional Promotion
        if is_better:
            job["status"] = "COMPLETED_PROMOTED"
            job["deployment_decision"] = "PROMOTED_TO_PRODUCTION"
            job["new_version"] = new_version
            
            # Register new model
            reg = ModelRegistration(
                model_name=base_model_name,
                version=new_version,
                task=task,
                dataset_id=dataset_record["dataset_id"],
                metrics=new_metrics,
                artifact_path=f"s3://models/{base_model_name}/{new_version}/weights.pt"
            )
            await register_model(reg)
            
            # Promote directly to production
            await promote_model(base_model_name, new_version, "PRODUCTION")
            logger.info(f"End-to-End Retraining Success! Model {new_version} promoted to production.")
        else:
            job["status"] = "COMPLETED_REJECTED"
            job["deployment_decision"] = "REJECTED_LOWER_PERFORMANCE"
            logger.info(f"Retrained model underperformed baseline. Discarded.")

    except Exception as e:
        logger.error(f"Retraining pipeline failed: {e}")
        job["status"] = f"FAILED: {str(e)}"

def get_retraining_job_status(job_id: str) -> Dict[str, Any]:
    """Fetches the current state and results of a retraining pipeline."""
    job = _retraining_jobs.get(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found.")
    return job
