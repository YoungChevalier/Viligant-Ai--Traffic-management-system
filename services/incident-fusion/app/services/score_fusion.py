from typing import Dict, Any, List


def compute_track_stability_score(track_history: List[Dict[str, Any]]) -> float:
    """
    Computes a stability score for a track based on its history length
    and consistency of observations.

    A longer, more consistent track yields a higher score (0.0 to 1.0).
    Short or erratic tracks score lower, indicating less reliable evidence.
    """
    if not track_history:
        return 0.0

    num_points = len(track_history)

    # Base score from observation count (saturates at 20 points)
    length_score = min(num_points / 20.0, 1.0)

    # Consistency bonus: check if track has no large gaps
    gap_penalty = 0.0
    if num_points >= 2:
        gaps = 0
        for i in range(1, num_points):
            prev = track_history[i - 1]
            curr = track_history[i]
            # If positions jump more than 50% of image width, penalise
            if "x" in prev and "x" in curr:
                dx = abs(curr["x"] - prev["x"])
                dy = abs(curr["y"] - prev["y"])
                if dx > 500 or dy > 500:
                    gaps += 1

        gap_penalty = min(gaps * 0.15, 0.5)

    return max(0.0, min(1.0, length_score - gap_penalty))


def compute_ocr_reliability_score(plate_candidates: List[Dict[str, Any]]) -> float:
    """
    Computes a reliability score for OCR results based on candidate
    agreement and confidence levels.

    Multiple candidates with similar text yield a higher score.
    A single low-confidence result yields a lower score.

    Returns a score from 0.0 to 1.0.
    """
    if not plate_candidates:
        return 0.0

    # Average confidence across all candidates
    confidences = [c.get("confidence", 0.0) for c in plate_candidates]
    avg_confidence = sum(confidences) / len(confidences)

    # Agreement bonus: if multiple reads produce the same normalized text
    texts = [c.get("normalized_text", c.get("text", "")) for c in plate_candidates]
    unique_texts = set(texts)

    if len(plate_candidates) >= 2 and len(unique_texts) == 1:
        agreement_bonus = 0.2
    elif len(plate_candidates) >= 3 and len(unique_texts) <= 2:
        agreement_bonus = 0.1
    else:
        agreement_bonus = 0.0

    # Format validity bonus
    format_bonus = 0.0
    for c in plate_candidates:
        if c.get("format_valid", False):
            format_bonus = 0.1
            break

    return min(1.0, avg_confidence + agreement_bonus + format_bonus)


def compute_final_incident_score(component_scores: Dict[str, float]) -> float:
    """
    Computes a weighted final incident score from individual component scores.

    Component keys and their weights:
      - detection_score:  0.25
      - tracking_score:   0.20
      - anpr_score:       0.30
      - rule_score:       0.25

    Returns a final composite score from 0.0 to 1.0.
    """
    weights = {
        "detection_score": 0.25,
        "tracking_score": 0.20,
        "anpr_score": 0.30,
        "rule_score": 0.25,
    }

    total = 0.0
    for key, weight in weights.items():
        total += component_scores.get(key, 0.0) * weight

    return max(0.0, min(1.0, total))
