from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_vision_request_candidate_v1(
    input_candidate: Mapping[str, Any],
    task_context: Mapping[str, Any],
    scene_context: Mapping[str, Any],
    attention_plan: Mapping[str, Any],
    region_plan: Mapping[str, Any],
) -> Dict[str, Any]:
    requested = bool(input_candidate.get("vision_requested", True))
    candidate = {
        "schema_version": "observation_manager_vision_request_candidate_v1",
        "vision_request_id": f"vision_req_{input_candidate.get('observation_request_id')}",
        "task_id": input_candidate.get("task_id"),
        "task_context_ref": task_context.get("task_context_ref"),
        "scene_context_ref": scene_context.get("scene_context_ref"),
        "attention_targets": tuple(
            (attention_plan.get("attention_plan") or {}).get("targets") or ()
        ),
        "region_refs": tuple(
            (region_plan.get("region_plan") or {}).get("region_refs") or ()
        ),
        "candidate_only": True,
        **not_fact(),
    }
    return {
        "schema_version": "observation_manager_vision_adapter_v1",
        "vision_request_candidate": candidate if requested else None,
        "vision_request_candidate_present": requested,
        **not_fact(),
    }
