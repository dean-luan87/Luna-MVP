from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def bind_observation_task_context_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    task_id = str(input_candidate.get("task_id") or "")
    task_context = dict(input_candidate.get("task_context") or {})
    return {
        "schema_version": "observation_manager_task_context_binder_v1",
        "task_id": task_id,
        "task_context_ref": task_context.get("task_context_ref")
        or f"task_ctx_{task_id}"
        if task_id
        else "",
        "task_context": task_context,
        "task_context_present": bool(task_context),
        **not_fact(),
    }
