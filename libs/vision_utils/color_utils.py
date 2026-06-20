import cv2
import numpy as np


def bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Converts a BGR image (OpenCV default) to RGB color space.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    """
    Converts an RGB image to BGR color space (OpenCV default).
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Converts a BGR or RGB color image to single-channel grayscale.
    If the image is already single-channel, returns it unchanged.
    """
    if len(image.shape) == 2 or image.shape[2] == 1:
        return image

    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
