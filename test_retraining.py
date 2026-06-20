import sys
import asyncio
sys.path.insert(0, r'services\model-lifecycle')

from app.services.lifecycle_service import trigger_end_to_end_retraining, get_retraining_job_status

async def run_test():
    print("Triggering retraining pipeline for 'classification' task...")
    job_id = await trigger_end_to_end_retraining(task="classification", base_model_name="helmet-classifier-v1")
    print(f"Job queued with ID: {job_id}")
    
    status = "PENDING"
    while status not in ["COMPLETED_PROMOTED", "COMPLETED_REJECTED", "FAILED_AT_TRAINING"] and not status.startswith("FAILED"):
        job = get_retraining_job_status(job_id)
        status = job["status"]
        print(f"[{job['status']}] Dataset: {job.get('dataset_id', 'N/A')}")
        await asyncio.sleep(1)
        
    print("\n--- FINAL RESULTS ---")
    job = get_retraining_job_status(job_id)
    print(f"Deployment Decision: {job.get('deployment_decision')}")
    print(f"Baseline Metrics: {job.get('baseline_metrics')}")
    print(f"New Metrics: {job.get('new_metrics')}")
    print(f"New Version: {job.get('new_version', 'N/A')}")

asyncio.run(run_test())
