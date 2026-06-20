from datetime import datetime

def build_raw_frame_object_key(camera_id: str, captured_at: datetime) -> str:
    """
    Builds the storage object key for a raw frame.
    Uses date partitioning for optimized storage.
    """
    date_path = captured_at.strftime("%Y/%m/%d")
    time_str = captured_at.strftime("%H%M%S_%f")
    return f"raw_frames/{date_path}/{camera_id}/{time_str}.jpg"

def build_plate_crop_object_key(track_id: str, captured_at: datetime) -> str:
    """
    Builds the storage object key for a cropped license plate image.
    Uses date partitioning for optimized storage.
    """
    date_path = captured_at.strftime("%Y/%m/%d")
    time_str = captured_at.strftime("%H%M%S_%f")
    return f"plate_crops/{date_path}/{track_id}/{time_str}.jpg"

def build_evidence_object_key(incident_id: str, asset_type: str) -> str:
    """
    Builds the storage object key for an incident evidence asset.
    Groups all assets for a specific incident together.
    """
    # Assuming standard extensions based on asset type, or keeping it extension-agnostic
    return f"evidence/incidents/{incident_id}/{asset_type}"
