import uuid

def build_frame_id() -> str:
    """
    Generates a unique identifier for a video frame.
    """
    return f"frm_{uuid.uuid4().hex}"

def build_track_id() -> str:
    """
    Generates a unique identifier for a tracked object.
    """
    return f"trk_{uuid.uuid4().hex}"

def build_incident_id() -> str:
    """
    Generates a unique identifier for a traffic incident.
    """
    return f"inc_{uuid.uuid4().hex}"

def build_asset_id() -> str:
    """
    Generates a unique identifier for an evidence asset.
    """
    return f"ast_{uuid.uuid4().hex}"
