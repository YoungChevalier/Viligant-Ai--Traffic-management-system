import cv2
import numpy as np
from pathlib import Path


def load_image_from_bytes(data: bytes) -> np.ndarray:
    """
    Decodes raw image bytes into a NumPy BGR image array.
    Raises ValueError if decoding fails.
    """
    if not data:
        raise ValueError("Image data must not be empty")

    np_arr = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Failed to decode image from bytes")

    return image


def load_image_from_path(path: str) -> np.ndarray:
    """
    Reads an image from the filesystem into a NumPy BGR image array.
    Raises FileNotFoundError if the path does not exist.
    Raises ValueError if the file cannot be decoded as an image.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    image = cv2.imread(str(file_path), cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(f"Failed to decode image at: {path}")

    return image


def encode_image_to_jpg_bytes(image: np.ndarray, quality: int = 95) -> bytes:
    """
    Encodes a NumPy BGR image array to JPEG bytes.
    Quality ranges from 0 (worst) to 100 (best).
    """
    success, encoded = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])

    if not success:
        raise RuntimeError("Failed to encode image to JPEG")

    return encoded.tobytes()


def encode_image_to_png_bytes(image: np.ndarray, compression: int = 3) -> bytes:
    """
    Encodes a NumPy BGR image array to PNG bytes.
    Compression ranges from 0 (no compression) to 9 (max compression).
    """
    success, encoded = cv2.imencode(".png", image, [cv2.IMWRITE_PNG_COMPRESSION, compression])

    if not success:
        raise RuntimeError("Failed to encode image to PNG")

    return encoded.tobytes()
