import os
import shutil
from pathlib import Path

# Base directory for local object storage (overridable via env var)
STORAGE_ROOT = os.getenv("OBJECT_STORAGE_ROOT", "./object_storage")


def _ensure_parent_dir(object_key: str) -> Path:
    """
    Ensures the parent directory for the given object key exists.
    Returns the full resolved file path.
    """
    full_path = Path(STORAGE_ROOT) / object_key
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path


def save_frame_from_uri(frame_uri: str, object_key: str) -> str:
    """
    Copies a frame from a local file URI into object storage at the given key.
    In production this would upload to S3/GCS; here it copies locally.

    Returns the stored object path.
    """
    dest = _ensure_parent_dir(object_key)
    source = Path(frame_uri)

    if not source.exists():
        raise FileNotFoundError(f"Source frame not found: {frame_uri}")

    shutil.copy2(str(source), str(dest))
    return str(dest)


def save_uploaded_frame(file_bytes: bytes, object_key: str) -> str:
    """
    Writes raw frame bytes directly into object storage at the given key.
    In production this would stream to S3/GCS; here it writes locally.

    Returns the stored object path.
    """
    if not file_bytes:
        raise ValueError("file_bytes must not be empty")

    dest = _ensure_parent_dir(object_key)
    dest.write_bytes(file_bytes)
    return str(dest)
