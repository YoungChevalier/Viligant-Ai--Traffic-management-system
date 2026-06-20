import logging
from typing import Dict, Any, List, Tuple
import numpy as np
from pathlib import Path

from libs.vision_utils.image_io import load_image_from_path, encode_image_to_jpg_bytes
from libs.vision_utils.quality_metrics import (
    compute_blur_score,
    compute_brightness_score,
    compute_noise_score,
    compute_rain_score,
    compute_shadow_score
)

from app.services.lighting_enhancement import apply_clahe, apply_gamma_correction, needs_low_light_enhancement, needs_gamma_correction
from app.services.denoise_enhancement import apply_basic_denoise, needs_denoise
from app.services.deblur_enhancement import apply_motion_deblur, needs_deblurring
from app.services.weather_robustness import apply_rain_removal, needs_rain_removal, apply_shadow_compensation, needs_shadow_compensation
from app.services.normalize_frame import resize_with_letterbox, normalize_color_space

logger = logging.getLogger(__name__)

def analyze_frame_quality(image: np.ndarray) -> Dict[str, float]:
    return {
        "blur_score": compute_blur_score(image),
        "brightness_score": compute_brightness_score(image),
        "noise_score": compute_noise_score(image),
        "rain_score": compute_rain_score(image),
        "shadow_score": compute_shadow_score(image)
    }

def build_preprocess_plan(metrics: Dict[str, float]) -> Tuple[List[str], List[str]]:
    """
    Intelligently chains enhancement algorithms based on environmental conditions.
    Returns:
       conditions_detected: List of string labels for detected bad conditions
       plan: Ordered list of algorithms to apply
    """
    conditions_detected = []
    plan = []
    
    # 1. Rain Removal (Apply first so rain streaks aren't sharpened by deblur)
    if needs_rain_removal(metrics["rain_score"]):
        conditions_detected.append("HEAVY_RAIN")
        plan.append("rain_removal")
        
    # 2. Lighting Enhancements
    if needs_gamma_correction(metrics["brightness_score"]):
        conditions_detected.append("EXTREME_LOW_LIGHT")
        plan.append("gamma_correction")
    elif needs_low_light_enhancement(metrics["brightness_score"]):
        conditions_detected.append("LOW_LIGHT")
        plan.append("clahe")
        
    # 3. Shadow Handling
    if needs_shadow_compensation(metrics["shadow_score"]):
        conditions_detected.append("HARSH_SHADOWS")
        if "gamma_correction" not in plan: # Don't stack gamma and shadow boost
            plan.append("shadow_compensation")

    # 4. Deblurring (Avoid sharpening if image is very noisy or heavily rained)
    if needs_deblurring(metrics["blur_score"]):
        conditions_detected.append("MOTION_BLUR")
        if "rain_removal" not in plan and metrics["noise_score"] < 20.0:
            plan.append("motion_deblur")
            
    # 5. Denoise (Clean up artifacts from gamma/clahe)
    if needs_denoise(metrics["noise_score"]) or "gamma_correction" in plan:
        # Don't add denoise if we already did rain removal (bilateral filter already smooths)
        if "rain_removal" not in plan:
            conditions_detected.append("HIGH_NOISE")
            plan.append("denoise")
            
    # 6. Standard Normalization
    plan.append("letterbox")
    plan.append("normalize_color")
    
    return conditions_detected, plan


def run_preprocess_plan(image: np.ndarray, plan: List[str]) -> np.ndarray:
    result = image.copy()
    for step in plan:
        if step == "rain_removal":
            result = apply_rain_removal(result)
        elif step == "gamma_correction":
            result = apply_gamma_correction(result)
        elif step == "clahe":
            result = apply_clahe(result)
        elif step == "shadow_compensation":
            result = apply_shadow_compensation(result)
        elif step == "motion_deblur":
            result = apply_motion_deblur(result)
        elif step == "denoise":
            result = apply_basic_denoise(result)
        elif step == "letterbox":
            result = resize_with_letterbox(result)
        elif step == "normalize_color":
            result = normalize_color_space(result)
    return result

async def preprocess_frame(request_data: Any) -> Dict[str, Any]:
    """
    Full preprocessing orchestrator integrating environmental robustness.
    """
    frame_id = request_data.frame_id
    storage_path = request_data.storage_path

    # 1. Load Raw Frame
    image = load_image_from_path(storage_path)

    # 2. Analyze & Plan
    metrics = analyze_frame_quality(image)
    conditions_detected, plan = build_preprocess_plan(metrics)

    # 3. Execute Plan
    processed_image = run_preprocess_plan(image, plan)

    # 4. Save Processed Frame (MOCKED LOCAL STORAGE)
    processed_uri = storage_path.replace("raw_frames", "processed_frames")
    dest_path = Path("./object_storage") / processed_uri
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_bytes(encode_image_to_jpg_bytes(processed_image))
    logger.info(f"Processed frame {frame_id} saved to {processed_uri}. Plan: {plan}")

    # 5. Publish to Downstream Queue (MOCKED)
    downstream_job = {
        "frame_id": frame_id,
        "camera_id": request_data.camera_id,
        "timestamp": request_data.timestamp,
        "processed_storage_path": processed_uri,
        "quality_metrics": metrics,
        "conditions_detected": conditions_detected
    }
    logger.info(f"Frame {frame_id} published to downstream detection queue: {downstream_job}")

    return {
        "frame_id": frame_id,
        "processed_storage_path": processed_uri,
        "metrics": metrics,
        "conditions_detected": conditions_detected,
        "plan_applied": plan,
        "queue_status": "published"
    }
