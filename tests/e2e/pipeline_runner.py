import logging
import time
from typing import Dict, Any, Tuple

# Note: In a production Kubernetes environment, this runner would use `httpx` 
# to hit real HTTP boundaries or push to a live Redis Stream.
# Here, we import the orchestrators directly for fast, mocked integration testing.

from services.ingestion.app.services.ingestion_service import process_ingestion
from services.preprocessing.app.services.preprocess_service import run_preprocessing_pipeline
from services.detection.app.services.detection_service import detect_frame
from services.tracking.app.services.tracking_service import track_frame
from services.rule_engine.app.services.helmet_rule import evaluate_helmet_compliance
from services.anpr.app.services.anpr_service import read_plates
from services.evidence.app.services.evidence_service import generate_evidence

logger = logging.getLogger(__name__)

class DotDict(dict):
    """Utility to allow dot notation access for mocked Pydantic models."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

async def run_pipeline(test_case: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Feeds a test case through all pipeline stages sequentially, 
    capturing outputs and execution times for each stage.
    """
    metrics = {}
    context = {}

    try:
        # 1. Ingestion
        start = time.time()
        # Wrap dict in DotDict to simulate FastAPI object access
        ingest_req = DotDict(test_case)
        ingest_res = await process_ingestion(ingest_req)
        metrics["ingestion_ms"] = (time.time() - start) * 1000
        context["ingestion"] = ingest_res

        # 2. Preprocessing
        start = time.time()
        prep_req = DotDict({"frame_id": test_case["frame_id"], "storage_path": "./mock_raw.jpg"}) 
        prep_res = await run_preprocessing_pipeline(prep_req)
        metrics["preprocessing_ms"] = (time.time() - start) * 1000
        context["preprocessing"] = prep_res

        # 3. Detection
        start = time.time()
        det_req = DotDict({"frame_id": test_case["frame_id"], "processed_storage_path": "./mock_prep.jpg"})
        det_res = await detect_frame(det_req)
        metrics["detection_ms"] = (time.time() - start) * 1000
        context["detection"] = det_res

        # 4. Tracking
        start = time.time()
        trk_req = DotDict({"frame_id": test_case["frame_id"], "detections": det_res["detections"]})
        trk_res = await track_frame(trk_req)
        metrics["tracking_ms"] = (time.time() - start) * 1000
        context["tracking"] = trk_res

        # 5. Rule Engine (Helmet)
        start = time.time()
        rule_req = DotDict({"frame_id": test_case["frame_id"], "tracks": trk_res["tracks"], "processed_storage_path": "./mock_prep.jpg"})
        rule_res = await evaluate_helmet_compliance(rule_req)
        metrics["rule_engine_ms"] = (time.time() - start) * 1000
        context["rule_engine"] = rule_res

        # Short-circuit logic: Stop pipeline if no violations were detected
        if not rule_res.get("violations"):
            logger.info("Pipeline terminated early: No violations detected.")
            return context, metrics

        # 6. ANPR
        start = time.time()
        anpr_req = DotDict({"frame_id": test_case["frame_id"], "violation_candidates": rule_res["violations"], "processed_storage_path": "./mock_prep.jpg"})
        anpr_res = await read_plates(anpr_req)
        metrics["anpr_ms"] = (time.time() - start) * 1000
        context["anpr"] = anpr_res

        # 7. Evidence Generation
        start = time.time()
        ev_req = DotDict({
            "frame_id": test_case["frame_id"], 
            "camera_id": test_case["camera_id"], 
            "timestamp": test_case["timestamp"], 
            "processed_storage_path": "./mock_prep.jpg", 
            "candidates_with_plates": anpr_res.get("candidates", [])
        })
        ev_res = await generate_evidence(ev_req)
        metrics["evidence_ms"] = (time.time() - start) * 1000
        context["evidence"] = ev_res

        metrics["total_ms"] = sum(metrics.values())
        return context, metrics

    except Exception as e:
        logger.error(f"Pipeline failed at trace {test_case['frame_id']}: {str(e)}")
        context["error"] = str(e)
        return context, metrics
