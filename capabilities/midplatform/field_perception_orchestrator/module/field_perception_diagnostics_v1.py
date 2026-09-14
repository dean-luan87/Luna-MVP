from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_types_v1 import (
    not_fact,
)


def build_field_perception_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    information_gap: Mapping[str, Any],
    capability_plan: Mapping[str, Any],
    resource_plan: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "field_perception_diagnostics_v1",
        "task_id": input_candidate.get("task_id"),
        "module_status": module_status,
        "need_visual_invocation": bool(
            information_gap.get("need_visual_invocation", False)
        ),
        "information_gap_count": len(
            tuple(information_gap.get("information_gap") or ())
        ),
        "requested_visual_capability_count": len(
            tuple(capability_plan.get("requested_visual_capabilities") or ())
        ),
        "resource_degraded": bool(resource_plan.get("resource_degraded", False)),
        **not_fact(),
    }
