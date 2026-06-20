"""
triple_riding_rule.py
Orchestrator for triple-riding violation detection.

Reuses the existing rider_association.py module to associate persons with
motorcycles, then groups by motorcycle and flags any with ≥3 riders.

Flow:
  1. Accept tracked-object payload
  2. Separate person and motorcycle tracks
  3. Associate riders to motorcycles (reuses rider_association.py)
  4. Group associations by motorcycle
  5. Flag motorcycles with ≥3 riders as triple-riding violations
  6. Build violation candidates
  7. Persist candidates (mocked DB)
  8. Publish downstream event (mocked queue)
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List

from app.services.rider_association import associate_riders_to_motorcycles
from app.services.triple_riding_candidate import build_triple_riding_candidate

# MOCK: If DB is not ready, we mock the persistence dependency here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Minimum number of riders to constitute a triple-riding violation
TRIPLE_RIDING_THRESHOLD = 3

# Confidence scoring
BASE_CONFIDENCE = 0.85
# Each additional rider beyond the threshold adds confidence
PER_EXTRA_RIDER_BONUS = 0.04


def _compute_triple_riding_confidence(rider_count: int) -> float:
    """
    Computes confidence for a triple-riding violation.

    Higher rider count → higher confidence (more certain it's a violation).

    Args:
        rider_count: Number of riders detected on one motorcycle.

    Returns:
        Confidence score [0.0, 1.0].
    """
    extra = rider_count - TRIPLE_RIDING_THRESHOLD
    confidence = BASE_CONFIDENCE + extra * PER_EXTRA_RIDER_BONUS
    return round(min(0.98, confidence), 3)


def _group_riders_by_motorcycle(
    associations: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Groups rider associations by motorcycle track ID.

    Args:
        associations: Output from associate_riders_to_motorcycles().

    Returns:
        Dict mapping motorcycle_track_id → list of association dicts.
    """
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for assoc in associations:
        moto_id = assoc["motorcycle_track_id"]
        grouped[moto_id].append(assoc)
    return dict(grouped)


async def run_triple_riding_rule(request_data: Any) -> Dict[str, Any]:
    """
    Full triple-riding rule orchestrator:
      1. Separate person and motorcycle tracks
      2. Associate riders to motorcycles (reuses existing module)
      3. Group associations by motorcycle
      4. Flag motorcycles with ≥3 riders
      5. Build violation candidates
      6. Persist violation candidates (Mocked DB)
      7. Publish downstream event (Mocked Queue)

    Args:
        request_data: TripleRidingRuleRequest Pydantic model.

    Returns:
        Result dict with frame info, violation candidates, and queue status.
    """
    frame_id = request_data.frame_id
    camera_id = request_data.camera_id
    timestamp = request_data.timestamp

    # Serialize Pydantic models to dicts
    tracked_objects = [t.model_dump() for t in request_data.tracked_objects]

    # 1. Separate person and motorcycle tracks
    person_tracks = [t for t in tracked_objects if t["class_name"] == "person"]
    motorcycle_tracks = [t for t in tracked_objects if t["class_name"] == "motorcycle"]

    logger.info(
        "Frame %s: %d person tracks, %d motorcycle tracks",
        frame_id, len(person_tracks), len(motorcycle_tracks),
    )

    if not person_tracks or not motorcycle_tracks:
        logger.info("Frame %s: Insufficient tracks for triple-riding check", frame_id)
        return {
            "frame_id": frame_id,
            "rule": "TRIPLE_RIDING",
            "persons_found": len(person_tracks),
            "motorcycles_found": len(motorcycle_tracks),
            "associations_found": 0,
            "violations": [],
            "queue_status": "none",
        }

    # 2. Associate riders to motorcycles (reuses existing module)
    associations = associate_riders_to_motorcycles(person_tracks, motorcycle_tracks)

    logger.info(
        "Frame %s: %d rider-motorcycle associations found",
        frame_id, len(associations),
    )

    # 3. Group by motorcycle
    grouped = _group_riders_by_motorcycle(associations)

    # 4 & 5. Evaluate each motorcycle
    candidates: List[Dict[str, Any]] = []
    for moto_id, riders in grouped.items():
        rider_count = len(riders)

        if rider_count < TRIPLE_RIDING_THRESHOLD:
            continue  # Legal — 1 or 2 riders

        confidence = _compute_triple_riding_confidence(rider_count)
        rider_track_ids = [r["rider_track_id"] for r in riders]
        motorcycle_bbox = riders[0].get("motorcycle_bbox")

        logger.info(
            "Triple riding detected | motorcycle=%s | riders=%d | ids=%s | confidence=%.3f",
            moto_id, rider_count, rider_track_ids, confidence,
        )

        candidate = build_triple_riding_candidate(
            motorcycle_track_id=moto_id,
            frame_id=frame_id,
            confidence=confidence,
            rider_count=rider_count,
            rider_track_ids=rider_track_ids,
            motorcycle_bbox=motorcycle_bbox,
        )
        candidate["camera_id"] = camera_id
        candidate["timestamp"] = timestamp
        candidates.append(candidate)

    logger.info(
        "Frame %s: Evaluated %d motorcycles, found %d triple-riding violations",
        frame_id, len(grouped), len(candidates),
    )

    # 6. Persist Violation Candidates (MOCKED DB)
    # db = next(get_db())
    # db.commit()
    logger.info("Saved %d triple-riding violation candidates to database (Mocked)", len(candidates))

    # 7. Publish to Downstream Queue (MOCKED)
    if candidates:
        downstream_job = {
            "frame_id": frame_id,
            "camera_id": camera_id,
            "timestamp": timestamp,
            "violations": candidates,
        }
        logger.info("Frame %s published to downstream fusion queue: %s", frame_id, downstream_job)
    else:
        logger.info("Frame %s has no triple-riding violations. Pipeline terminates here.", frame_id)

    return {
        "frame_id": frame_id,
        "rule": "TRIPLE_RIDING",
        "persons_found": len(person_tracks),
        "motorcycles_found": len(motorcycle_tracks),
        "associations_found": len(associations),
        "violations": candidates,
        "queue_status": "published" if candidates else "none",
    }
