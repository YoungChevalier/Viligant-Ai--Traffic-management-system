import os
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Module-level singleton for the loaded helmet model
_loaded_model: Optional[Any] = None
_loaded_model_path: Optional[str] = None

# Default model path (overridable via env var)
DEFAULT_MODEL_PATH = os.getenv("HELMET_MODEL_PATH", "./models/helmet_classifier.onnx")


def load_helmet_model(model_path: str = DEFAULT_MODEL_PATH) -> Any:
    """
    Loads a helmet classification model from disk and caches it as a
    module-level singleton.

    In production this would load via ONNX Runtime or TorchScript.
    Currently returns a stub model dict for development.
    """
    global _loaded_model, _loaded_model_path

    resolved = Path(model_path)

    logger.info("Loading helmet classification model from: %s", resolved)

    # TODO: Replace stub with actual model loading
    # Example with ONNX Runtime:
    #   import onnxruntime as ort
    #   session = ort.InferenceSession(str(resolved))
    _loaded_model = {
        "type": "stub",
        "path": str(resolved),
        "input_size": (64, 64),
        "classes": ["helmet", "no_helmet"],
    }
    _loaded_model_path = str(resolved)

    logger.info("Helmet model loaded successfully (stub mode)")
    return _loaded_model


def get_loaded_helmet_model() -> Any:
    """
    Returns the cached helmet model singleton.
    If no model has been loaded yet, loads from the default path.
    """
    global _loaded_model

    if _loaded_model is None:
        load_helmet_model()

    return _loaded_model
