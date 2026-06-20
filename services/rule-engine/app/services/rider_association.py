from typing import Dict, List, Any, Tuple


def _compute_iou(bbox_a: Dict[str, float], bbox_b: Dict[str, float]) -> float:
    """
    Computes Intersection over Union (IoU) between two bbox dicts.
    """
    x1 = max(bbox_a["x1"], bbox_b["x1"])
    y1 = max(bbox_a["y1"], bbox_b["y1"])
    x2 = min(bbox_a["x2"], bbox_b["x2"])
    y2 = min(bbox_a["y2"], bbox_b["y2"])

    inter_w = max(0.0, x2 - x1)
    inter_h = max(0.0, y2 - y1)
    intersection = inter_w * inter_h

    area_a = (bbox_a["x2"] - bbox_a["x1"]) * (bbox_a["y2"] - bbox_a["y1"])
    area_b = (bbox_b["x2"] - bbox_b["x1"]) * (bbox_b["y2"] - bbox_b["y1"])
    union = area_a + area_b - intersection

    if union <= 0:
        return 0.0

    return intersection / union


def _person_overlaps_motorcycle(
    person_bbox: Dict[str, float],
    motorcycle_bbox: Dict[str, float],
) -> float:
    """
    Computes the fraction of the person bbox that overlaps with the motorcycle bbox.
    """
    x1 = max(person_bbox["x1"], motorcycle_bbox["x1"])
    y1 = max(person_bbox["y1"], motorcycle_bbox["y1"])
    x2 = min(person_bbox["x2"], motorcycle_bbox["x2"])
    y2 = min(person_bbox["y2"], motorcycle_bbox["y2"])

    inter_w = max(0.0, x2 - x1)
    inter_h = max(0.0, y2 - y1)
    intersection = inter_w * inter_h

    person_area = (person_bbox["x2"] - person_bbox["x1"]) * (person_bbox["y2"] - person_bbox["y1"])
    if person_area <= 0:
        return 0.0

    return intersection / person_area


# Thresholds for association
IOU_THRESHOLD = 0.15
OVERLAP_THRESHOLD = 0.3


def is_person_associated_with_motorcycle(
    person_bbox: Dict[str, float],
    motorcycle_bbox: Dict[str, float],
) -> bool:
    """
    Determines whether a detected person is likely riding the given motorcycle.

    Uses two heuristics:
      1. IoU between the person and motorcycle bboxes exceeds a threshold.
      2. A significant fraction of the person bbox overlaps the motorcycle bbox.

    Returns True if either condition is met.
    """
    iou = _compute_iou(person_bbox, motorcycle_bbox)
    overlap = _person_overlaps_motorcycle(person_bbox, motorcycle_bbox)

    return iou >= IOU_THRESHOLD or overlap >= OVERLAP_THRESHOLD


def associate_riders_to_motorcycles(
    person_tracks: List[Dict[str, Any]],
    motorcycle_tracks: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Associates person tracks with motorcycle tracks to identify riders.

    Each person is matched to the motorcycle with the highest overlap.
    Unmatched persons are ignored (they are likely pedestrians).

    Args:
        person_tracks: List of tracked objects with class_name == 'person'.
        motorcycle_tracks: List of tracked objects with class_name == 'motorcycle'.

    Returns:
        A list of association dicts:
          - rider_track_id: str
          - motorcycle_track_id: str
          - rider_bbox: dict
          - motorcycle_bbox: dict
    """
    associations: List[Dict[str, Any]] = []

    for person in person_tracks:
        best_match = None
        best_overlap = 0.0

        for moto in motorcycle_tracks:
            if is_person_associated_with_motorcycle(person["bbox"], moto["bbox"]):
                overlap = _person_overlaps_motorcycle(person["bbox"], moto["bbox"])
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_match = moto

        if best_match is not None:
            associations.append({
                "rider_track_id": person["track_id"],
                "motorcycle_track_id": best_match["track_id"],
                "rider_bbox": person["bbox"],
                "motorcycle_bbox": best_match["bbox"],
            })

    return associations
