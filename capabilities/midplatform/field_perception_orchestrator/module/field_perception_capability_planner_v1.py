from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_capability_plan_v1(
    observation_goal: Mapping[str, Any],
    available_visual_capabilities: tuple[str, ...],
) -> Dict[str, Any]:
    goal = str(observation_goal.get("observation_goal") or "")
    intent_map = {
        "confirm_navigable_space_ahead": ("detection", "segmentation", "depth"),
        "locate_entrance": ("detection", "ocr", "region_intelligence"),
        "locate_exit": ("detection", "ocr", "region_intelligence"),
        "confirm_traffic_light_state": ("detection", "tracking"),
        "read_text_notice": ("roi_detection", "ocr", "layout_analysis"),
        "confirm_target_person_presence": ("detection", "tracking"),
        "confirm_target_object_location": (
            "detection",
            "grounding",
            "spatial_relation",
        ),
        "maintain_minimum_safety_observation": ("detection",),
        "no_additional_observation_required": tuple(),
    }
    requested = intent_map.get(goal, ("detection",))
    available = set(available_visual_capabilities)
    if available:
        requested = tuple(cap for cap in requested if cap in available)
    return {
        "schema_version": "field_perception_capability_planner_v1",
        "requested_visual_capabilities": requested,
        "capability_plan_generated": True,
    }
