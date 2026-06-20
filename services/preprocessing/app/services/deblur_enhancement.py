"""
deblur_enhancement.py
Handles motion blur mitigation.
"""

import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def needs_deblurring(blur_score: float) -> bool:
    """Threshold to decide if we should attempt motion deblurring."""
    # Laplacian variance < 100 usually means blurry. 
    # But we don't want to over-sharpen a completely useless image (e.g., < 10)
    return 10 < blur_score < 100

def apply_motion_deblur(image: np.ndarray) -> np.ndarray:
    """
    Applies a sharpening filter (Unsharp Masking) to recover edges lost to motion blur.
    In production, this could be replaced with a learned Wiener filter or CNN deblurrer.
    """
    logger.info("Applying motion deblur (Unsharp Mask stub).")
    
    # Gaussian blur to create a smoothed version
    gaussian = cv2.GaussianBlur(image, (9, 9), 10.0)
    
    # AddWeighted applies the formula: original * alpha + smoothed * beta + gamma
    # To sharpen, we subtract the smoothed version from the original:
    # sharpened = original + (original - smoothed) * amount
    
    sharpened = cv2.addWeighted(image, 1.5, gaussian, -0.5, 0)
    return sharpened
