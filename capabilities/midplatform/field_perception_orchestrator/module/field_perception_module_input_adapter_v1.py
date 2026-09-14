from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    not_fact,
)


def _tuple_str(value: Any) -> Tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    return tuple(str(x) for x in value)


def adapt_field_perception_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(payload)
    task_context = dict(data.get("task_context") or {})
    current_field_state = dict(data.get("current_field_state") or {})

    adapted = {
        "schema_version": MODULE_SCHEMA_VERSION,
        "task_context": task_context,
        "task_id": str(
            task_context.get("task_id") or data.get("task_id") or ""
        ).strip(),
        "task_goal": str(
            task_context.get("goal") or task_context.get("objective") or ""
        ).strip(),
        "current_field_state": current_field_state,
        "recent_observation_summary": dict(
            data.get("recent_observation_summary") or {}
        ),
        "available_visual_capabilities": _tuple_str(
            data.get("available_visual_capabilities")
        ),
        "available_model_assets": tuple(data.get("available_model_assets") or ()),
        "resource_budget": dict(data.get("resource_budget") or {}),
        "temporal_context": dict(data.get("temporal_context") or {}),
        "uncertainty_state": dict(data.get("uncertainty_state") or {}),
        "conflict_state": dict(data.get("conflict_state") or {}),
        "previous_invocation_history": tuple(
            data.get("previous_invocation_history") or ()
        ),
    }
    adapted["input_valid"] = bool(adapted["task_id"]) and isinstance(
        current_field_state, dict
    )
    adapted["rejection_reasons"] = tuple(
        reason
        for reason, failed in (
            ("missing_task_id", not bool(adapted["task_id"])),
            ("missing_current_field_state", not bool(current_field_state)),
        )
        if failed
    )
    adapted.update(not_fact())
    return adapted
