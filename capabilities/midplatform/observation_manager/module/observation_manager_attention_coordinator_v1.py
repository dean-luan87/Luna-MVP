from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_attention_plan_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    attention_targets = tuple(input_candidate.get("attention_targets") or ())
    request_type = str(input_candidate.get("request_type") or "")
    if not attention_targets:
        default_targets = {
            "baseline_safety": ("forward_path", "hazard_zone"),
            "navigation_support": ("route_hint", "crossing_zone"),
            "find_text": ("text_regions",),
            "read_text": ("text_regions",),
            "scene_understanding": ("scene_entities", "spatial_layout"),
            "verification_observation": ("verification_targets",),
        }
        attention_targets = default_targets.get(request_type, ("general_observation",))

    return {
        "schema_version": "observation_manager_attention_coordinator_v1",
        "attention_plan": {
            "plan_id": f"attn_{input_candidate.get('observation_request_id')}",
            "targets": attention_targets,
            "focus_mode": "balanced" if len(attention_targets) > 1 else "single_focus",
        },
        "attention_plan_present": bool(attention_targets),
        **not_fact(),
    }
