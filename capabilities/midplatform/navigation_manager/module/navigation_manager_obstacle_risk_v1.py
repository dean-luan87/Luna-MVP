from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_obstacle_risk_assessment_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    obstacles = tuple(input_candidate.get("obstacle_candidates") or ())
    collision_risk = any("collision" in str(item).lower() for item in obstacles)
    attention_required = bool(obstacles)
    return {
        "schema_version": "navigation_manager_obstacle_risk_v1",
        "obstacle_risk_assessment": {
            "obstacle_candidates": obstacles,
            "collision_risk": collision_risk,
            "attention_required": attention_required,
        },
        **not_fact(),
    }
