from typing import Dict, Any, List
from collections import defaultdict

# Priority order for violation types (higher index = higher severity)
VIOLATION_PRIORITY = [
    "SPEED_LIMIT",
    "WRONG_WAY",
    "NO_HELMET",
    "RED_LIGHT",
    "HIT_AND_RUN",
]


def group_candidates_by_track(
    candidate_events: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Groups violation candidate events by their track_id.

    Candidates without a track_id are grouped under the key '_untracked'.

    Returns a dict mapping track_id → list of candidate events.
    """
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for event in candidate_events:
        track_id = event.get("track_id", "_untracked")
        groups[track_id].append(event)

    return dict(groups)


def merge_violation_labels(
    candidate_group: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Merges duplicate violation types within a single track's candidate group.

    For each unique violation_type, keeps the candidate with the highest
    confidence. Returns a deduplicated list.
    """
    best_by_type: Dict[str, Dict[str, Any]] = {}

    for candidate in candidate_group:
        vtype = candidate.get("violation_type", "UNKNOWN")
        confidence = candidate.get("confidence", 0.0)

        existing = best_by_type.get(vtype)
        if existing is None or confidence > existing.get("confidence", 0.0):
            best_by_type[vtype] = candidate

    return list(best_by_type.values())


def select_primary_violation(
    violation_labels: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Selects the primary (most severe) violation from a list of merged labels.

    Uses VIOLATION_PRIORITY for severity ranking. If a violation type is not
    in the priority list, it is treated as lowest priority.
    Falls back to highest confidence if priorities are equal.

    Returns the selected primary violation dict.
    """
    if not violation_labels:
        return {}

    if len(violation_labels) == 1:
        return violation_labels[0]

    def sort_key(v: Dict[str, Any]):
        vtype = v.get("violation_type", "")
        priority = (
            VIOLATION_PRIORITY.index(vtype)
            if vtype in VIOLATION_PRIORITY
            else -1
        )
        confidence = v.get("confidence", 0.0)
        return (priority, confidence)

    sorted_labels = sorted(violation_labels, key=sort_key, reverse=True)
    return sorted_labels[0]
