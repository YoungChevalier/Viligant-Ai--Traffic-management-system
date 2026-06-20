import os
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Module-level singleton for the loaded model
_loaded_model: Optional[Any] = None
_loaded_model_path: Optional[str] = None

# Default model path (overridable via env var)
DEFAULT_MODEL_PATH = os.getenv("DETECTION_MODEL_PATH", "./models/yolov8n.onnx")


def load_detection_model(model_path: str = DEFAULT_MODEL_PATH) -> Any:
    """
    Loads an ONNX detection model from disk and caches it as a module-level singleton.

    In production this would load via ONNX Runtime, TensorRT, or Ultralytics.
    Currently returns a stub model dict for development.

    Raises FileNotFoundError if the model file does not exist
    (skipped in stub mode for convenience).
    """
    global _loaded_model, _loaded_model_path

    resolved = Path(model_path)

    # In production, uncomment:
    # if not resolved.exists():
    #     raise FileNotFoundError(f"Detection model not found: {model_path}")

    logger.info("Loading detection model from: %s", resolved)

    # TODO: Replace stub with actual model loading
    # Example with ONNX Runtime:
    #   import onnxruntime as ort
    #   session = ort.InferenceSession(str(resolved))
    _loaded_model = {
        "type": "stub",
        "path": str(resolved),
        "input_size": (640, 640),
        "classes": [
            "car", "truck", "bus", "motorcycle", "bicycle",
            "person", "traffic_light", "stop_sign",
        ],
    }
    _loaded_model_path = str(resolved)

    logger.info("Detection model loaded successfully (stub mode)")
    return _loaded_model


def get_loaded_detection_model() -> Any:
    """
    Returns the cached detection model singleton.
    If no model has been loaded yet, loads from the default path.
    """
    global _loaded_model

    if _loaded_model is None:
        load_detection_model()

    return _loaded_model
