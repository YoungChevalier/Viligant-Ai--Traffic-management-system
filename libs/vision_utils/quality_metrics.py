import cv2
import numpy as np

def compute_blur_score(image: np.ndarray) -> float:
    """
    Computes a blur score for the given image using the variance of the Laplacian.
    A higher score indicates a sharper image; a lower score indicates more blur.
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return float(laplacian.var())

def compute_brightness_score(image: np.ndarray) -> float:
    """
    Computes the average brightness of the image on a 0.0 to 1.0 scale.
    """
    if len(image.shape) == 2 or image.shape[2] == 1:
        return float(image.mean()) / 255.0
    else:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:, :, 2]
        return float(v_channel.mean()) / 255.0

def compute_noise_score(image: np.ndarray) -> float:
    """
    Estimates the noise level using the Median Absolute Deviation (MAD) of the Laplacian.
    A higher score indicates more noise.
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    median_abs_deviation = float(np.median(np.abs(laplacian - np.median(laplacian))))
    return median_abs_deviation * 1.4826

def compute_rain_score(image: np.ndarray) -> float:
    """
    Stubs a rain streak score.
    In a real pipeline, we'd use directional Gabor filters or edge density 
    in the vertical/diagonal directions.
    Here we mock it by calculating vertical gradient energy.
    Higher score indicates possible rain or strong vertical texture.
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # Energy in vertical edges
    return float(np.mean(np.abs(sobel_y))) / 255.0

def compute_shadow_score(image: np.ndarray) -> float:
    """
    Stubs a shadow score by detecting bimodal distribution or stark contrast.
    We compute the difference between the 90th percentile and 10th percentile 
    brightness. A very high difference *might* indicate heavy shadowing in sunlight.
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
    else:
        v = image
        
    p10 = np.percentile(v, 10)
    p90 = np.percentile(v, 90)
    
    # Simple metric: contrast width
    return float(p90 - p10) / 255.0
