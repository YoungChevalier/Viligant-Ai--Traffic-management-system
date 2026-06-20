import logging
from typing import Any, Dict, List, Optional
import numpy as np

logger = logging.getLogger(__name__)


def run_paddle_ocr(image: np.ndarray) -> List[Dict[str, Any]]:
    """
    Runs PaddleOCR on the given plate image and returns raw OCR results.

    In production this would initialise PaddleOCR and call ocr() on the image.
    Currently returns stub results for development.

    Args:
        image: A rectified plate image (BGR) as a NumPy array.

    Returns:
        A list of raw OCR result dicts, each containing:
          - text: str (recognised characters)
          - confidence: float (0.0 to 1.0)
          - bbox: list of point tuples (text region polygon)
    """
    logger.info("Running PaddleOCR | image_shape=%s", image.shape)

    # TODO: Replace stub with actual PaddleOCR
    # from paddleocr import PaddleOCR
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')
    # result = ocr.ocr(image, cls=True)
    # return _parse_paddle_result(result)

    # Stub result
    raw_results = [
        {
            "text": "KA01AB1234",
            "confidence": 0.93,
            "bbox": [(0, 0), (200, 0), (200, 60), (0, 60)],
        },
    ]

    logger.info("PaddleOCR complete | lines_detected=%d", len(raw_results))
    return raw_results


def extract_best_ocr_text(
    raw_ocr_result: List[Dict[str, Any]],
    min_confidence: float = 0.5,
) -> Optional[Dict[str, Any]]:
    """
    Selects the highest-confidence OCR text line from the raw results.

    Filters out results below min_confidence before selecting.

    Returns a dict with 'text' and 'confidence', or None if no valid results.
    """
    valid = [r for r in raw_ocr_result if r["confidence"] >= min_confidence]

    if not valid:
        return None

    best = max(valid, key=lambda r: r["confidence"])

    return {
        "text": best["text"],
        "confidence": best["confidence"],
    }
