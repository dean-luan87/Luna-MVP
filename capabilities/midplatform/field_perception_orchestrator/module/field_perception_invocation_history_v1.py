from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_invocation_history_assessment_v1(
    previous_invocation_history: tuple[Mapping[str, Any], ...],
    observation_goal: str,
) -> Dict[str, Any]:
    recent = None
    for item in reversed(previous_invocation_history):
        if (
            isinstance(item, Mapping)
            and str(item.get("observation_goal") or "") == observation_goal
        ):
            recent = item
            break
    recent_success = bool(recent and bool(recent.get("success", False)))
    recent_fresh = bool(recent and bool(recent.get("fresh", False)))
    return {
        "schema_version": "field_perception_invocation_history_v1",
        "recent_same_goal_present": bool(recent),
        "recent_same_goal_success": recent_success,
        "recent_same_goal_fresh": recent_fresh,
        "suppress_reinvocation": bool(recent_success and recent_fresh),
    }
