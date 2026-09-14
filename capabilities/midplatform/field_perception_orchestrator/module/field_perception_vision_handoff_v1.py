from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_types_v1 import (
    not_fact,
)


def build_field_perception_vision_handoff_candidate_v1(
    field_perception_plan: Mapping[str, Any],
    need_visual_invocation: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": "field_perception_vision_handoff_v1",
        "vision_handoff_candidate": {
            "handoff_required": bool(need_visual_invocation),
            "vision_request_id": f"vision_req::{field_perception_plan.get('plan_id')}",
            "observation_goal": field_perception_plan.get("observation_goal"),
            "target_region": field_perception_plan.get("target_region"),
            "requested_visual_capabilities": tuple(
                field_perception_plan.get("requested_visual_capabilities") or ()
            ),
            "model_requirements": {
                "preferred_model_candidates": tuple(
                    field_perception_plan.get("preferred_model_candidates") or ()
                ),
                "fallback_model_candidates": tuple(
                    field_perception_plan.get("fallback_model_candidates") or ()
                ),
                "resolution_level": field_perception_plan.get("resolution_level"),
                "temporal_window": field_perception_plan.get("temporal_window"),
            },
            **not_fact(),
        },
        **not_fact(),
    }
