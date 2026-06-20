import logging
from typing import Any, Dict, List
import numpy as np

logger = logging.getLogger(__name__)


def run_detection_inference(model: Any, image: np.ndarray) -> List[Dict[str, Any]]:
    """
    Runs raw object detection inference on the given image using the loaded model.

    In production this would feed the image through an ONNX Runtime session
    or Ultralytics model and return the raw output tensor rows.

    Currently returns stub detections for development.

    Args:
        model: The loaded detection model (from model_loader).
        image: A preprocessed image as a NumPy array (BGR uint8 or float32 RGB).

    Returns:
        A list of raw detection dicts, each containing:
          - class_index: int
          - class_name: str
          - confidence: float
          - bbox: [x1, y1, x2, y2] in pixel coordinates
    """
    classes = model.get("classes", [])
    input_size = model.get("input_size", (640, 640))

    logger.info(
        "Running detection inference | model_type=%s | image_shape=%s | input_size=%s",
        model.get("type", "unknown"),
        image.shape,
        input_size,
    )

    # TODO: Replace stub with actual inference
    # Example with ONNX Runtime:
    #   session = model["session"]
    #   input_name = session.get_inputs()[0].name
    #   blob = cv2.dnn.blobFromImage(image, ...)
    #   outputs = session.run(None, {input_name: blob})
    #   return _parse_raw_outputs(outputs, classes)

    # Stub: return synthetic detections for development
    raw_detections = [
        {
            "class_index": 0,
            "class_name": "car",
            "confidence": 0.92,
            "bbox": [120.0, 200.0, 320.0, 350.0],
        },
        {
            "class_index": 5,
            "class_name": "person",
            "confidence": 0.87,
            "bbox": [400.0, 180.0, 450.0, 340.0],
        },
    ]

    logger.info("Inference complete | detections_count=%d", len(raw_detections))

    return raw_detections
