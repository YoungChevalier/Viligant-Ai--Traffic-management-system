import cv2
import numpy as np

# Noise sigma threshold above which denoising is triggered
NOISE_THRESHOLD = 15.0


def needs_denoise(noise_score: float) -> bool:
    """
    Determines whether a frame requires denoising
    based on its noise score (robust sigma estimate).

    Returns True if the noise score exceeds the configured threshold.
    """
    return noise_score > NOISE_THRESHOLD


def apply_basic_denoise(image: np.ndarray, h: int = 10) -> np.ndarray:
    """
    Applies Non-Local Means Denoising to reduce noise while preserving edges.

    For BGR images uses fastNlMeansDenoisingColored.
    For grayscale images uses fastNlMeansDenoising.

    The 'h' parameter controls filter strength; higher values remove
    more noise but may also remove fine detail.

    Returns the denoised image in the same color space as the input.
    """
    if len(image.shape) == 2 or image.shape[2] == 1:
        return cv2.fastNlMeansDenoising(image, None, h)

    return cv2.fastNlMeansDenoisingColored(image, None, h, h)
