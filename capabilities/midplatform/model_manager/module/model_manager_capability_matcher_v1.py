from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.model_manager.model_manager_dryrun.capability_matching_processor_v1 import (
    match_capability_need,
)


def build_capability_match_v1(
    *,
    requested_capability: str,
    trace_context: Mapping[str, Any],
    task_ref: str,
) -> Dict[str, Any]:
    if requested_capability:
        return {
            "required_capability": requested_capability,
            "capability_first": True,
            "source": "request",
            "task_ref": task_ref,
        }

    matched = match_capability_need(
        situation_understanding_candidate=dict(
            trace_context.get("situation_understanding_candidate") or {}
        ),
        agent_plan_candidate=dict(trace_context.get("agent_plan_candidate") or {}),
        decision_validation_candidate=dict(
            trace_context.get("decision_validation_candidate") or {}
        ),
        need_capability=None,
    )
    return {
        "required_capability": str(matched.get("required_capability", "")),
        "capability_first": True,
        "source": "trace_context",
        "task_ref": task_ref,
    }
