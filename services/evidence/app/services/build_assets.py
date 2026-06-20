import cv2
import numpy as np
from typing import Dict, Any, List

from libs.common_utils.id_utils import build_asset_id
from libs.common_utils.time_utils import utc_now
from libs.common_utils.path_utils import build_evidence_object_key
from app.services.draw_annotations import draw_bbox, draw_incident_header, draw_plate_text


THUMBNAIL_SIZE = (320, 180)


def build_thumbnail(image: np.ndarray) -> np.ndarray:
    """
    Creates a small thumbnail from the source image for quick preview.

    Returns a resized image of THUMBNAIL_SIZE dimensions.
    """
    return cv2.resize(image, THUMBNAIL_SIZE, interpolation=cv2.INTER_AREA)


def build_annotated_frame(
    image: np.ndarray,
    incident_data: Dict[str, Any],
) -> np.ndarray:
    """
    Produces a fully annotated evidence frame by composing all relevant
    visual overlays onto the source image.

    Draws:
      - Incident header bar (violation type, score, ID)
      - Bounding boxes for tracked objects involved
      - Plate text overlay if available

    Args:
        image: Source frame image (BGR).
        incident_data: Dict with incident details including bboxes, plate, and summary.

    Returns:
        The fully annotated image.
    """
    annotated = image.copy()

    # Draw header
    summary = {
        "incident_id": incident_data.get("incident_id", ""),
        "primary_violation": incident_data.get("primary_violation", ""),
        "confidence_score": incident_data.get("confidence_score", 0.0),
    }
    annotated = draw_incident_header(annotated, summary)

    # Draw bounding boxes for involved objects
    bboxes = incident_data.get("bboxes", [])
    for bbox_info in bboxes:
        label = f"{bbox_info.get('class_name', '')} {bbox_info.get('confidence', 0.0):.2f}"
        annotated = draw_bbox(annotated, bbox_info["bbox"], label)

    # Draw plate text if available
    plate_text = incident_data.get("plate_text")
    if plate_text:
        annotated = draw_plate_text(annotated, plate_text)

    return annotated


def build_evidence_manifest(
    incident_data: Dict[str, Any],
    asset_refs: List[Dict[str, str]],
) -> Dict[str, Any]:
    """
    Builds the evidence manifest that ties all generated assets
    to a single incident.

    Args:
        incident_data: The incident record dict.
        asset_refs: A list of dicts, each with 'asset_type' and 'storage_path'.

    Returns:
        A manifest dict containing incident metadata and asset references.
    """
    incident_id = incident_data.get("incident_id", "")

    manifest_assets = []
    for ref in asset_refs:
        manifest_assets.append({
            "asset_id": build_asset_id(),
            "asset_type": ref["asset_type"],
            "storage_path": ref["storage_path"],
        })

    return {
        "incident_id": incident_id,
        "primary_violation": incident_data.get("primary_violation", ""),
        "confidence_score": incident_data.get("confidence_score", 0.0),
        "track_id": incident_data.get("track_id", ""),
        "plate_text": incident_data.get("plate_text"),
        "assets": manifest_assets,
        "created_at": utc_now().isoformat(),
    }
