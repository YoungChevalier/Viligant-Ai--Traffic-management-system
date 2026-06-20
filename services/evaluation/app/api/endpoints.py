from fastapi import APIRouter, HTTPException
from app.api.schemas import EvaluationRequest, EvaluationResult
from app.services.evaluation_service import run_evaluation
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/evaluate", response_model=EvaluationResult)
async def post_evaluate(request: EvaluationRequest):
    """
    Runs performance evaluation and benchmarking.
    
    Accepts predictions and ground truth, computes accuracy, precision,
    recall, F1, mAP, and efficiency metrics. Returns structured results.
    """
    try:
        logger.info("Received evaluation request for dataset: %s", request.dataset_name)
        result = await run_evaluation(request)
        return result
    except ValueError as ve:
        logger.error("Validation error during evaluation: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("Unexpected error during evaluation")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
