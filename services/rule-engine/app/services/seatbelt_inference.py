"""
seatbelt_inference.py
Seatbelt classification inference module.

MOCKED: Returns stub predictions for development. In production, this
would load an ONNX/TensorRT seatbelt classifier model and run inference
on cabin crops.

Follows the same pattern as helmet_inference.py.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# ── Model Loader ───────────────────────────────────────────────────────────

_seatbelt_model: Optional[Dict[str, Any]] = None


def get_loaded_seatbelt_model() -> Dict[str, Any]:
    """
    Returns the loaded seatbelt classification model.

    MOCKED: Returns a stub model dict. In production, this would load
    an ONNX Runtime session or TensorRT engine on first call and cache it.
    """
    global _seatbelt_model
    if _seatbelt_model is None:
        logger.info("Loading seatbelt classification model (Mocked)")
        _seatbelt_model = {
            "type": "mock_seatbelt_classifier",
            "classes": ["seatbelt", "no_seatbelt"],
            "input_size": (224, 224),
            "version": "0.1.0-stub",
        }
    return _seatbelt_model


# ── Classifier ─────────────────────────────────────────────────────────────


def classify_seatbelt_crop(
    model: Dict[str, Any],
    crop_image: Any,
) -> Dict[str, Any]:
    """
    Runs seatbelt classification inference on a cropped cabin region.

    MOCKED: Returns a stub prediction. In production, this would:
      1. Resize crop to model input size
      2. Normalize pixel values
      3. Run through ONNX Runtime / TensorRT
      4. Return predicted class with confidence

    Args:
        model: The loaded seatbelt classification model.
        crop_image: Cropped cabin region (np.ndarray in production, Any for mock).

    Returns:
        A dict with:
          - label: str ('seatbelt' or 'no_seatbelt')
          - confidence: float (0.0 to 1.0)
    """
    classes = model.get("classes", ["seatbelt", "no_seatbelt"])

    # Log crop metadata if available
    crop_info = "unknown"
    if isinstance(crop_image, dict) and crop_image.get("_mock"):
        crop_info = f"{crop_image.get('width', '?')}x{crop_image.get('height', '?')}"
    elif hasattr(crop_image, "shape"):
        crop_info = str(crop_image.shape)

    logger.info(
        "Classifying seatbelt crop | crop=%s | model_type=%s",
        crop_info, model.get("type", "unknown"),
    )

    # TODO: Replace stub with actual inference
    # Example with ONNX Runtime:
    #   session = model["session"]
    #   input_name = session.get_inputs()[0].name
    #   resized = cv2.resize(crop_image, model["input_size"])
    #   blob = resized.astype(np.float32) / 255.0
    #   blob = np.expand_dims(blob.transpose(2, 0, 1), axis=0)
    #   outputs = session.run(None, {input_name: blob})
    #   class_idx = int(np.argmax(outputs[0]))
    #   confidence = float(outputs[0][0][class_idx])

    # Stub prediction — returns "no_seatbelt" for development
    result = {
        "label": "no_seatbelt",
        "confidence": 0.82,
    }

    logger.info("Seatbelt classification result: %s", result)
    return result
