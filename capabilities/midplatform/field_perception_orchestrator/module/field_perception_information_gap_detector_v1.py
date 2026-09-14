from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_information_gap_v1(
    task_goal_resolution: Mapping[str, Any],
    field_snapshot: Mapping[str, Any],
    uncertainty_state: Mapping[str, Any],
    conflict_state: Mapping[str, Any],
    recent_observation_summary: Mapping[str, Any],
) -> Dict[str, Any]:
    missing = tuple(field_snapshot.get("missing_information") or ())
    stale = tuple(field_snapshot.get("stale_evidence") or ())
    uncertainties = tuple(field_snapshot.get("uncertainties") or ())
    conflicts = tuple(field_snapshot.get("conflicts") or ())
    expired = bool(recent_observation_summary.get("expired", False))
    sufficient = bool(recent_observation_summary.get("sufficient_for_decision", False))
    explicit_gap = tuple(uncertainty_state.get("information_gap") or ())
    conflict_gap = tuple(conflict_state.get("conflicting_claims") or ())

    gap_items = tuple(
        dict.fromkeys(
            [
                *(str(x) for x in missing),
                *(str(x) for x in stale),
                *(str(x) for x in uncertainties),
                *(str(x) for x in conflicts),
                *(str(x) for x in explicit_gap),
                *(str(x) for x in conflict_gap),
            ]
        )
    )
    goal_class = str(
        task_goal_resolution.get("task_goal_class") or "minimum_safety_observation"
    )

    need_visual = bool(gap_items) or expired
    if sufficient and not bool(gap_items):
        need_visual = False
    if (
        goal_class
        in {
            "find_exit",
            "find_entrance",
            "read_notice",
            "track_person",
            "locate_target_object",
            "traffic_light_state",
            "navigable_space_check",
        }
        and not sufficient
    ):
        need_visual = True

    return {
        "schema_version": "field_perception_information_gap_detector_v1",
        "information_gap": gap_items,
        "need_visual_invocation": need_visual,
        "gap_severity": "high"
        if len(gap_items) >= 2 or expired
        else ("low" if not gap_items else "medium"),
        "evidence_sufficient": sufficient,
    }
