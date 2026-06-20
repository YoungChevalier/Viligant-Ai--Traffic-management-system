from typing import Any, Dict, List

from libs.vision_utils.bbox_utils import xyxy_to_bbox_dict


def extract_detection_items(raw_result: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms raw inference output rows into structured detection items.
    Each item gets a standardised bbox dict via xyxy_to_bbox_dict.
    """
    items: List[Dict[str, Any]] = []

    for raw in raw_result:
        bbox_coords = raw.get("bbox", [0, 0, 0, 0])
        item = {
            "class_name": raw["class_name"],
            "confidence": raw["confidence"],
            "bbox": xyxy_to_bbox_dict(*bbox_coords),
        }
        items.append(item)

    return items


def filter_detection_items(
    items: List[Dict[str, Any]], min_confidence: float = 0.4
) -> List[Dict[str, Any]]:
    """
    Filters detection items by a minimum confidence threshold.
    Returns only items whose confidence >= min_confidence.
    """
    return [item for item in items if item["confidence"] >= min_confidence]


def build_detection_response(
    frame_id: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Assembles the final detection response payload.
    """
    return {
        "frame_id": frame_id,
        "detection_count": len(items),
        "detections": items,
    }
