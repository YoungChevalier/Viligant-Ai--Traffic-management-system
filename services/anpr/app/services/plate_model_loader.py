import os
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Module-level singleton for the loaded plate detector
_loaded_model: Optional[Any] = None
_loaded_model_path: Optional[str] = None

# Default model path (overridable via env var)
DEFAULT_MODEL_PATH = os.getenv("PLATE_DETECTOR_MODEL_PATH", "./models/plate_detector.onnx")


def load_plate_detector(model_path: str = DEFAULT_MODEL_PATH) -> Any:
    """
    Loads a license plate detection model from disk and caches it as a
    module-level singleton.

    In production this would load via ONNX Runtime or a YOLO variant
    fine-tuned for plate localisation.
    Currently returns a stub model dict for development.
    """
    global _loaded_model, _loaded_model_path

    resolved = Path(model_path)

    logger.info("Loading plate detector model from: %s", resolved)

    # TODO: Replace stub with actual model loading
    _loaded_model = {
        "type": "stub",
        "path": str(resolved),
        "input_size": (320, 320),
        "classes": ["license_plate"],
    }
    _loaded_model_path = str(resolved)

    logger.info("Plate detector loaded successfully (stub mode)")
    return _loaded_model


def get_loaded_plate_detector() -> Any:
    """
    Returns the cached plate detector singleton.
    If no model has been loaded yet, loads from the default path.
    """
    global _loaded_model

    if _loaded_model is None:
        load_plate_detector()

    return _loaded_model
