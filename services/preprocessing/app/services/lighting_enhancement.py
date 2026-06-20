import cv2
import numpy as np

# Brightness threshold below which low-light enhancement is triggered
LOW_LIGHT_THRESHOLD = 0.35
EXTREME_LOW_LIGHT_THRESHOLD = 0.15

def needs_low_light_enhancement(brightness_score: float) -> bool:
    """
    Determines whether a frame requires low-light enhancement
    based on its brightness score (0.0 to 1.0).
    Returns True if the brightness is below the configured threshold.
    """
    return brightness_score < LOW_LIGHT_THRESHOLD

def needs_gamma_correction(brightness_score: float) -> bool:
    """
    Determines if extreme low light requires gamma correction before CLAHE.
    """
    return brightness_score < EXTREME_LOW_LIGHT_THRESHOLD

def apply_gamma_correction(image: np.ndarray, gamma: float = 2.0) -> np.ndarray:
    """
    Applies gamma correction to boost extremely dark images.
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def apply_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)) -> np.ndarray:
    """
    Applies Contrast Limited Adaptive Histogram Equalization (CLAHE)
    to enhance visibility in low-light or low-contrast frames.
    """
    if len(image.shape) == 2 or image.shape[2] == 1:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(image)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    enhanced_l = clahe.apply(l_channel)

    enhanced_lab = cv2.merge([enhanced_l, a_channel, b_channel])
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
