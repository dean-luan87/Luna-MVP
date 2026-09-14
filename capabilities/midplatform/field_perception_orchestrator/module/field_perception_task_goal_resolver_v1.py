from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_task_goal_resolution_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    goal_text = str(input_candidate.get("task_goal") or "").lower()
    mapping = {
        "exit": "find_exit",
        "entrance": "find_entrance",
        "traffic": "traffic_light_state",
        "light": "traffic_light_state",
        "notice": "read_notice",
        "read": "read_notice",
        "person": "track_person",
        "target": "locate_target_object",
        "walk": "navigable_space_check",
        "path": "navigable_space_check",
        "safe": "minimum_safety_observation",
    }
    goal_class = "minimum_safety_observation"
    for token, klass in mapping.items():
        if token in goal_text:
            goal_class = klass
            break
    return {
        "schema_version": "field_perception_task_goal_resolver_v1",
        "task_goal_class": goal_class,
        "task_goal_resolved": bool(goal_text),
    }
