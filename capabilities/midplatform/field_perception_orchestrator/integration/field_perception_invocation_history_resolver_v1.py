from __future__ import annotations

from typing import Any, Dict, Mapping


def resolve_invocation_history_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    task_id = str(input_candidate.get("task_id") or "")
    field_snapshot_ref = str(input_candidate.get("field_snapshot_ref") or "")
    information_gap_ref = str(input_candidate.get("information_gap_ref") or "")
    observation_goal = str(input_candidate.get("observation_goal") or "")
    target_region = str(input_candidate.get("target_region") or "")
    capability_set = tuple(
        sorted(tuple(input_candidate.get("requested_visual_capabilities") or ()))
    )

    matched = []
    for item in tuple(input_candidate.get("invocation_history") or ()):
        if not isinstance(item, Mapping):
            continue
        same = (
            str(item.get("task_id") or "") == task_id
            and str(item.get("field_snapshot_ref") or "") == field_snapshot_ref
            and str(item.get("information_gap_ref") or "") == information_gap_ref
            and str(item.get("observation_goal") or "") == observation_goal
            and str(item.get("target_region") or "") == target_region
            and tuple(sorted(tuple(item.get("requested_visual_capabilities") or ())))
            == capability_set
        )
        if same:
            matched.append(dict(item))

    active = next((m for m in matched if bool(m.get("active", False))), None)
    fresh = next(
        (m for m in matched if bool(m.get("fresh_evidence_available", False))), None
    )
    recent = matched[-1] if matched else None
    return {
        "matched_history": tuple(matched),
        "active_match": active,
        "fresh_match": fresh,
        "recent_match": recent,
    }
