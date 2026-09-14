from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_region_plan_v1(
    input_candidate: Mapping[str, Any],
    attention_plan: Mapping[str, Any],
) -> Dict[str, Any]:
    region_hints = tuple(input_candidate.get("region_hints") or ())
    attention_targets = tuple(
        (attention_plan.get("attention_plan") or {}).get("targets") or ()
    )
    if not region_hints:
        region_hints = tuple(f"region_for_{target}" for target in attention_targets)
    return {
        "schema_version": "observation_manager_region_coordinator_v1",
        "region_plan": {
            "plan_id": f"region_{input_candidate.get('observation_request_id')}",
            "region_refs": region_hints,
        },
        "region_plan_present": bool(region_hints),
        **not_fact(),
    }
