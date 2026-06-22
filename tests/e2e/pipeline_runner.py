import logging
import time
from typing import Dict, Any, Tuple

# Note: In a production Kubernetes environment, this runner would use `httpx` 
# to hit real HTTP boundaries or push to a live Redis Stream.
# Here, we import the orchestrators directly for fast, mocked integration testing.

from services.ingestion.app.services.ingestion_service import ingest_frame
from services.preprocessing.app.services.preprocess_service import preprocess_frame
from services.detection.app.services.detection_service import detect_frame
from services.tracking.app.services.tracking_service import track_frame
from services.rule_engine.app.services.helmet_rule import run_helmet_rule
from services.anpr.app.services.anpr_service import read_plate_batch
from services.evidence.app.services.evidence_service import generate_evidence

logger = logging.getLogger(__name__)

class DotDict(dict):
    """Utility to allow dot notation access for mocked Pydantic models."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def model_dump(self):
        return dict(self)

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
        import datetime
        timestamp = datetime.datetime.fromisoformat(ingest_req.timestamp.replace("Z", "+00:00")) if isinstance(ingest_req.timestamp, str) else ingest_req.timestamp
        ingest_res = await ingest_frame(ingest_req.camera_id, timestamp, b"mock_image_bytes")
        metrics["ingestion_ms"] = (time.time() - start) * 1000
        context["ingestion"] = ingest_res

        # 2. Preprocessing
        start = time.time()
        prep_req = DotDict({"frame_id": test_case["frame_id"], "storage_path": "./mock_raw.jpg"}) 
        prep_res = await preprocess_frame(prep_req)
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
        trk_req = DotDict({"frame_id": test_case["frame_id"], "camera_id": test_case.get("camera_id", "cam-1"), "timestamp": test_case.get("timestamp", "2023-01-01T00:00:00Z"), "processed_storage_path": "./mock_prep.jpg", "detections": [DotDict(d) for d in det_res["detections"]]})
        trk_res = await track_frame(trk_req)
        metrics["tracking_ms"] = (time.time() - start) * 1000
        context["tracking"] = trk_res

        # 5. Rule Engine (Helmet)
        start = time.time()
        rule_req = DotDict({"frame_id": test_case["frame_id"], "tracked_objects": [DotDict(t) for t in trk_res.get("tracked_objects", [])], "processed_storage_path": "./mock_prep.jpg"})
        rule_res = await run_helmet_rule(rule_req)
        metrics["rule_engine_ms"] = (time.time() - start) * 1000
        context["rule_engine"] = rule_res

        # Short-circuit logic: Stop pipeline if no violations were detected
        if not rule_res.get("violations"):
            logger.info("Pipeline terminated early: No violations detected.")
            return context, metrics

        # 6. ANPR
        start = time.time()
        anpr_req = DotDict({"frame_id": test_case["frame_id"], "camera_id": test_case.get("camera_id", "cam-1"), "timestamp": test_case.get("timestamp", "2023-01-01T00:00:00Z"), "violations": [DotDict(v) for v in rule_res.get("violations", [])], "processed_storage_path": "./mock_prep.jpg"})
        anpr_res = await read_plate_batch(anpr_req)
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
