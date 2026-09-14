from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from capabilities.midplatform.core.task_manager_skeleton_v1 import (
    validate_task_manager_input,
)
from capabilities.midplatform.core.task_manager_static_validators_v1 import (
    validate_tm_input_contract,
)

from .task_manager_module_types_v1 import TASK_MANAGER_SUPPORTED_TYPES_V1

_ALLOWED_PRIORITIES = {"low", "normal", "high", "critical"}


def _has_cycle(edges: Mapping[str, Sequence[str]]) -> bool:
    visiting = set()
    visited = set()

    def dfs(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in edges.get(node, ()):
            if dfs(str(nxt)):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(dfs(str(k)) for k in edges.keys())


def _tuple_str(values: Iterable[Any]) -> Tuple[str, ...]:
    return tuple(str(v) for v in values)


def adapt_task_manager_input_v1(raw: Mapping[str, Any]) -> Dict[str, Any]:
    missing_inputs: List[str] = []
    rejection_reasons: List[str] = []

    task_request_id = str(raw.get("task_request_id", "")).strip()
    if not task_request_id:
        missing_inputs.append("task_request_id")
        rejection_reasons.append("missing_task_request_id")

    task_type = str(raw.get("task_type", "")).strip()
    if task_type not in TASK_MANAGER_SUPPORTED_TYPES_V1:
        rejection_reasons.append("unsupported_task_type")

    priority = str(raw.get("priority", "")).strip().lower()
    if priority not in _ALLOWED_PRIORITIES:
        rejection_reasons.append("invalid_priority")

    permission_snapshot = raw.get("permission_snapshot")
    if not isinstance(permission_snapshot, Mapping) or not permission_snapshot:
        rejection_reasons.append("missing_permission_snapshot")

    context_snapshot = raw.get("context_snapshot") or {}
    if not isinstance(context_snapshot, Mapping):
        context_snapshot = {}

    if bool(context_snapshot.get("request_direct_action_execution", False)):
        rejection_reasons.append("direct_action_execution_forbidden")
    if bool(context_snapshot.get("request_direct_model_call", False)):
        rejection_reasons.append("direct_model_call_forbidden")
    if bool(context_snapshot.get("request_direct_field_state_write", False)):
        rejection_reasons.append("direct_field_state_write_forbidden")
    if bool(context_snapshot.get("request_bypass_capability_module_api", False)):
        rejection_reasons.append("bypass_capability_module_api_forbidden")

    dependency_refs = raw.get("dependency_refs") or ()
    if isinstance(dependency_refs, str):
        dependency_refs = (dependency_refs,)
    dependency_refs = _tuple_str(dependency_refs)

    dependency_graph = raw.get("dependency_graph") or {}
    if isinstance(dependency_graph, Mapping) and _has_cycle(dependency_graph):
        rejection_reasons.append("cyclic_dependency")

    adapted = {
        "task_request_id": task_request_id,
        "task_type": task_type,
        "task_goal": str(raw.get("task_goal", "")).strip(),
        "requester_ref": str(raw.get("requester_ref", "")).strip(),
        "priority": priority,
        "context_snapshot": dict(context_snapshot),
        "dependency_refs": dependency_refs,
        "resource_constraints": dict(raw.get("resource_constraints") or {}),
        "permission_snapshot": dict(permission_snapshot or {}),
        "capability_requirements": _tuple_str(raw.get("capability_requirements") or ()),
        "deadline_or_timeout": str(raw.get("deadline_or_timeout", "")).strip(),
        "interruption_policy": dict(raw.get("interruption_policy") or {}),
        "recovery_policy": dict(raw.get("recovery_policy") or {}),
        "version_snapshots": dict(raw.get("version_snapshots") or {}),
        "trace_ref": str(raw.get("trace_ref") or f"task_manager_trace_{task_request_id or 'missing'}").strip(),
        "missing_inputs": tuple(missing_inputs),
        "rejection_reasons": tuple(rejection_reasons),
    }

    # Reuse existing static input checks from core skeleton/validators.
    bridge_candidate = {
        "candidate_id": f"tm_input_{task_request_id or 'missing'}",
        "trace_ref": adapted["trace_ref"],
        "fact_status": "not_fact",
        "candidate_not_fact": True,
        "source_chain": task_request_id or "missing",
        "high_risk": priority == "critical",
        "governance_ref": adapted["permission_snapshot"].get("governance_ref"),
    }
    v1 = validate_tm_input_contract(bridge_candidate)
    v2 = validate_task_manager_input(bridge_candidate)
    if not v1.valid:
        adapted["rejection_reasons"] = tuple(
            list(adapted["rejection_reasons"]) + list(v1.issues)
        )
    if not v2.valid:
        adapted["rejection_reasons"] = tuple(
            list(adapted["rejection_reasons"]) + list(v2.issues)
        )

    adapted["adapted_input_ok"] = len(adapted["rejection_reasons"]) == 0
    return adapted
