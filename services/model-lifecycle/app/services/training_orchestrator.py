"""
training_orchestrator.py
Simulates queuing and tracking GPU model retraining jobs.
"""

import uuid
import logging
import asyncio
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Mock job registry
_job_store: Dict[str, Dict[str, Any]] = {}

async def queue_retraining_job(task: str, model_name: str, dataset_id: str) -> str:
    """
    Submits a training job to the GPU cluster queue.
    """
    job_id = f"job-{uuid.uuid4().hex[:6]}"
    
    _job_store[job_id] = {
        "job_id": job_id,
        "task": task,
        "model_name": model_name,
        "dataset_id": dataset_id,
        "status": "PENDING"
    }
    
    logger.info(f"Retraining job {job_id} queued for model {model_name} on dataset {dataset_id}.")
    
    # Simulate async training taking place in background
    asyncio.create_task(_simulate_training_run(job_id))
    
    return job_id

def get_job_status(job_id: str) -> str:
    job = _job_store.get(job_id)
    if not job:
        return "UNKNOWN"
    return job["status"]

async def _simulate_training_run(job_id: str):
    """Mocks the time delay and state transitions of a GPU training run."""
    job = _job_store.get(job_id)
    if not job:
        return
        
    await asyncio.sleep(1) # Simulated delay
    job["status"] = "RUNNING"
    logger.info(f"Job {job_id} is now RUNNING.")
    
    await asyncio.sleep(2) # Simulated delay
    job["status"] = "COMPLETED"
    logger.info(f"Job {job_id} is now COMPLETED.")
