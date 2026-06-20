import re
from typing import Dict, Any, List, Optional


# Indian plate format: XX 00 XX 0000
# Examples: KA01AB1234, MH12DE5678, DL8CAF0123
INDIAN_PLATE_PATTERN = re.compile(
    r'^[A-Z]{2}\d{1,2}[A-Z]{0,3}\d{4}$'
)


def normalize_plate_text(text: str) -> str:
    """
    Normalizes raw OCR text for plate comparison:
      - Strips whitespace and special characters
      - Converts to uppercase
      - Applies common OCR substitutions (0/O, 1/I, 8/B, 5/S)
    """
    # Remove all non-alphanumeric characters
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text).upper()

    # Common OCR misread corrections for Indian plates
    # Position-aware: first 2 chars are letters, then digits, then letters, then digits
    # Apply simple global substitutions as a baseline
    substitutions = {
        'O': '0',  # in digit positions O → 0
        'I': '1',  # in digit positions I → 1
        'S': '5',  # in digit positions S → 5
        'B': '8',  # in digit positions B → 8
        'Z': '2',  # in digit positions Z → 2
        'G': '6',  # in digit positions G → 6
    }

    # Only apply substitutions to positions expected to be digits
    # Indian format: LL DD LLL DDDD (L=letter, D=digit)
    if len(cleaned) >= 4:
        # Positions 2-3 should be digits
        chars = list(cleaned)
        for i in range(2, min(4, len(chars))):
            if chars[i] in substitutions:
                chars[i] = substitutions[chars[i]]

        # Last 4 characters should be digits
        if len(chars) >= 4:
            for i in range(len(chars) - 4, len(chars)):
                if chars[i] in substitutions:
                    chars[i] = substitutions[chars[i]]

        cleaned = ''.join(chars)

    return cleaned


def validate_indian_plate_format(text: str) -> bool:
    """
    Checks whether the normalized plate text matches a valid Indian
    vehicle registration format.

    Returns True if the text matches the expected pattern.
    """
    return bool(INDIAN_PLATE_PATTERN.match(text))


def rank_plate_candidates(
    candidates: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Ranks plate text candidates by a composite score:
      1. Format validity (valid Indian plates scored higher)
      2. OCR confidence

    Returns the candidates sorted best-first.
    """
    scored = []
    for c in candidates:
        text = c.get("text", "")
        confidence = c.get("confidence", 0.0)

        normalized = normalize_plate_text(text)
        is_valid = validate_indian_plate_format(normalized)

        # Composite score: format validity bonus + confidence
        format_bonus = 0.2 if is_valid else 0.0
        composite_score = confidence + format_bonus

        scored.append({
            **c,
            "normalized_text": normalized,
            "format_valid": is_valid,
            "composite_score": composite_score,
        })

    scored.sort(key=lambda x: x["composite_score"], reverse=True)
    return scored
