"""
weather_robustness.py
Handles rain streak removal and shadow compensation algorithms.
"""

import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def needs_rain_removal(rain_score: float) -> bool:
    """Threshold to decide if we should attempt rain removal."""
    # Mock threshold: if vertical energy > 0.15, assume heavy rain streaks
    return rain_score > 0.15

def apply_rain_removal(image: np.ndarray) -> np.ndarray:
    """
    Applies a classic computer vision approach to mitigate rain streaks.
    Uses a bilateral filter to smooth out thin streaks while preserving edges.
    In production, this could be replaced with an ONNX CNN like DerainNet.
    """
    logger.info("Applying rain removal (bilateral filter stub).")
    # Bilateral filter is computationally heavier but preserves sharp edges (like license plates)
    # better than standard Gaussian blur.
    return cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

def needs_shadow_compensation(shadow_score: float) -> bool:
    """Threshold to decide if we should attempt shadow compensation."""
    # Mock threshold: if p90-p10 contrast > 0.7, assume stark harsh shadows
    return shadow_score > 0.7

def apply_shadow_compensation(image: np.ndarray) -> np.ndarray:
    """
    Compensates for stark shadows by illuminating dark areas.
    Uses a masked inverted gamma approach to brighten only the darkest pixels.
    """
    logger.info("Applying shadow compensation.")
    
    if len(image.shape) == 3 and image.shape[2] == 3:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2].astype(np.float32) / 255.0
        
        # Shadow mask: pixels darker than 0.3
        shadow_mask = (v < 0.3).astype(np.float32)
        
        # Smooth mask to avoid harsh boundaries
        mask_blurred = cv2.GaussianBlur(shadow_mask, (21, 21), 0)
        
        # Boost V channel where mask is active
        # v_new = v + (mask_blurred * (0.5 - v)*0.5)  # boost logic
        boosted_v = np.clip(v + mask_blurred * 0.3, 0, 1.0)
        
        hsv[:, :, 2] = (boosted_v * 255.0).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    else:
        return image
