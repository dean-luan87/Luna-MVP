from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_region_plan_v1(
    observation_goal: Mapping[str, Any],
    field_snapshot: Mapping[str, Any],
) -> Dict[str, Any]:
    known_regions = tuple(field_snapshot.get("known_regions") or ())
    goal = str(observation_goal.get("observation_goal") or "")
    if goal in {"confirm_traffic_light_state", "confirm_navigable_space_ahead"}:
        target_region = "front_corridor"
    elif goal in {"locate_exit", "locate_entrance"}:
        target_region = "candidate_access_regions"
    elif goal == "read_text_notice":
        target_region = "text_bearing_regions"
    elif goal == "confirm_target_person_presence":
        target_region = "last_known_person_region"
    elif goal == "confirm_target_object_location":
        target_region = "target_search_region"
    else:
        target_region = str(known_regions[0]) if known_regions else "safety_scan_region"

    return {
        "schema_version": "field_perception_region_planner_v1",
        "target_region": target_region,
        "target_entity_types": (
            "traffic_light",
            "entrance",
            "exit",
            "person",
            "obstacle",
            "text_notice",
            "target_object",
        ),
    }
