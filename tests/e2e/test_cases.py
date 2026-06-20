import uuid
from typing import Dict, Any

def generate_helmet_violation_case() -> Dict[str, Any]:
    """Generates a synthetic payload mimicking an ingestion request for a helmet violation."""
    return {
        "frame_id": f"frame-{uuid.uuid4().hex[:8]}",
        "camera_id": "cam-northex-01",
        "timestamp": "2026-06-19T10:00:00Z",
        "image_data_base64": "MOCKED_BASE64_IMAGE_DATA_WITH_NO_HELMET_RIDER",
        "expected_violation": "NO_HELMET",
        "expected_plate": "DL-12-AB-3456"
    }

def generate_clean_compliance_case() -> Dict[str, Any]:
    """Generates a synthetic payload mimicking a compliant rider."""
    return {
        "frame_id": f"frame-{uuid.uuid4().hex[:8]}",
        "camera_id": "cam-northex-01",
        "timestamp": "2026-06-19T10:05:00Z",
        "image_data_base64": "MOCKED_BASE64_IMAGE_DATA_WITH_HELMET_RIDER",
        "expected_violation": None,
        "expected_plate": "DL-99-ZZ-9999"
    }
