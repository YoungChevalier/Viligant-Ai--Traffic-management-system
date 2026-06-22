import logging
from typing import Any, Dict
import numpy as np

logger = logging.getLogger(__name__)


def classify_helmet_crop(model: Any, crop_image: np.ndarray) -> Dict[str, Any]:
    """
    Runs helmet classification inference on a cropped head region.

    In production this would feed the crop through an ONNX Runtime session
    and return the predicted class with confidence.
    Currently returns a stub prediction for development.

    Args:
        model: The loaded helmet classification model (from helmet_model_loader).
        crop_image: Cropped head region as a NumPy array (BGR).

    Returns:
        A dict with:
          - label: str ('helmet' or 'no_helmet')
          - confidence: float (0.0 to 1.0)
    """
    classes = model.get("classes", ["helmet", "no_helmet"])

    logger.info(
        "Classifying helmet crop | crop_shape=%s | model_type=%s",
        crop_image.shape, model.get("type", "unknown"),
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

    # Stub prediction
    result = {
        "label": "no_helmet",
        "confidence": 0.85,
    }

    logger.info("Helmet classification result: %s", result)
    return result


def build_helmet_candidate(
    track_id: str, frame_id: str, score: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Builds a violation candidate dict for a no-helmet detection.

    Args:
        track_id: The track ID of the rider.
        frame_id: The frame ID where the violation was detected.
        score: The classification result from classify_helmet_crop.

    Returns:
        A violation candidate dict ready for the incident fusion service.
    """
    return {
        "violation_type": "NO_HELMET",
        "confidence": score["confidence"],
        "track_id": track_id,
        "frame_id": frame_id,
        "label": score["label"],
    }
