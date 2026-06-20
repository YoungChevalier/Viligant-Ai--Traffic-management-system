from typing import Dict, Any, List

from libs.common_utils.id_utils import build_incident_id
from libs.common_utils.time_utils import utc_now
from app.services.score_fusion import (
    compute_track_stability_score,
    compute_ocr_reliability_score,
    compute_final_incident_score,
)
from app.services.merge_candidates import (
    group_candidates_by_track,
    merge_violation_labels,
    select_primary_violation,
)


def fuse_incident(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full incident fusion orchestrator:
      1. Group violation candidates by track
      2. Merge duplicate violation labels per track
      3. Select the primary violation for each track
      4. Compute component scores (detection, tracking, ANPR, rule)
      5. Compute the final weighted incident score
      6. Build and return incident records

    All steps delegate to already-separated helpers.
    """
    candidate_events = request.get("candidate_events", [])
    track_history = request.get("track_history", [])
    plate_candidates = request.get("plate_candidates", [])
    detection_confidence = request.get("detection_confidence", 0.0)
    rule_confidence = request.get("rule_confidence", 0.0)

    # Step 1–3: Group, merge, and select primary violations
    groups = group_candidates_by_track(candidate_events)

    incidents: List[Dict[str, Any]] = []

    for track_id, group in groups.items():
        merged = merge_violation_labels(group)
        primary = select_primary_violation(merged)

        if not primary:
            continue

        # Step 4: Compute component scores
        tracking_score = compute_track_stability_score(track_history)
        anpr_score = compute_ocr_reliability_score(plate_candidates)

        component_scores = {
            "detection_score": detection_confidence,
            "tracking_score": tracking_score,
            "anpr_score": anpr_score,
            "rule_score": rule_confidence,
        }

        # Step 5: Compute final score
        final_score = compute_final_incident_score(component_scores)

        # Step 6: Build incident record
        incident = {
            "incident_id": build_incident_id(),
            "track_id": track_id,
            "status": "OPEN",
            "primary_violation": primary.get("violation_type", "UNKNOWN"),
            "confidence_score": final_score,
            "score_breakdown": component_scores,
            "all_violations": [v.get("violation_type") for v in merged],
            "created_at": utc_now().isoformat(),
        }

        incidents.append(incident)

    return {
        "incidents_created": len(incidents),
        "incidents": incidents,
    }
