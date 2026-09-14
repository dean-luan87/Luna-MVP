from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_observation_goal_v1(
    task_goal_resolution: Mapping[str, Any],
    information_gap: Mapping[str, Any],
) -> Dict[str, Any]:
    goal_class = str(
        task_goal_resolution.get("task_goal_class") or "minimum_safety_observation"
    )
    if not bool(information_gap.get("need_visual_invocation", False)):
        goal = "no_additional_observation_required"
    else:
        mapping = {
            "navigable_space_check": "confirm_navigable_space_ahead",
            "find_exit": "locate_exit",
            "find_entrance": "locate_entrance",
            "read_notice": "read_text_notice",
            "traffic_light_state": "confirm_traffic_light_state",
            "track_person": "confirm_target_person_presence",
            "locate_target_object": "confirm_target_object_location",
            "minimum_safety_observation": "maintain_minimum_safety_observation",
        }
        goal = mapping.get(goal_class, "maintain_minimum_safety_observation")
    return {
        "schema_version": "field_perception_observation_goal_builder_v1",
        "observation_goal": goal,
    }
