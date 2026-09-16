from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence, Tuple

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


def _text_or_empty(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def adapt_task_manager_input_v1(raw: Mapping[str, Any]) -> Dict[str, Any]:
    missing_inputs: List[str] = []
    rejection_reasons: List[str] = []

    if not isinstance(raw, Mapping):
        return {
            "task_request_id": "", "task_type": "", "task_goal": "",
            "requester_ref": "", "priority": "", "context_snapshot": {},
            "dependency_refs": (), "resource_constraints": {},
            "permission_snapshot": {}, "capability_requirements": (),
            "deadline_or_timeout": "", "interruption_policy": {},
            "recovery_policy": {}, "version_snapshots": {},
            "trace_ref": "task_manager_trace_missing", "missing_inputs": (),
            "rejection_reasons": ("invalid_input_mapping",),
            "adapted_input_ok": False,
        }

    for name in ("task_request_id", "task_type", "priority", "task_goal", "requester_ref", "deadline_or_timeout", "trace_ref"):
        value = raw.get(name)
        if value is not None and not isinstance(value, str):
            rejection_reasons.append(f"{name}_invalid_field_type")

    task_request_id = _text_or_empty(raw.get("task_request_id", ""))
    if not task_request_id:
        missing_inputs.append("task_request_id")
        rejection_reasons.append("missing_task_request_id")

    task_type = _text_or_empty(raw.get("task_type", ""))
    if task_type not in TASK_MANAGER_SUPPORTED_TYPES_V1:
        rejection_reasons.append("unsupported_task_type")

    priority = _text_or_empty(raw.get("priority", "")).lower()
    if priority not in _ALLOWED_PRIORITIES:
        rejection_reasons.append("invalid_priority")

    permission_snapshot = raw.get("permission_snapshot")
    if not isinstance(permission_snapshot, Mapping) or not permission_snapshot:
        rejection_reasons.append("missing_permission_snapshot")
        permission_snapshot = {}
    else:
        permission_snapshot = dict(permission_snapshot)

    context_snapshot = raw.get("context_snapshot")
    if context_snapshot is None:
        context_snapshot = {}
    elif not isinstance(context_snapshot, Mapping):
        rejection_reasons.append("context_snapshot_invalid_field_type")
        context_snapshot = {}

    if bool(context_snapshot.get("request_direct_action_execution", False)):
        rejection_reasons.append("direct_action_execution_forbidden")
    if bool(context_snapshot.get("request_direct_model_call", False)):
        rejection_reasons.append("direct_model_call_forbidden")
    if bool(context_snapshot.get("request_direct_field_state_write", False)):
        rejection_reasons.append("direct_field_state_write_forbidden")
    if bool(context_snapshot.get("request_bypass_capability_module_api", False)):
        rejection_reasons.append("bypass_capability_module_api_forbidden")

    dependency_refs = raw.get("dependency_refs")
    if dependency_refs is None:
        dependency_refs = ()
    elif not isinstance(dependency_refs, tuple):
        rejection_reasons.append("dependency_refs_invalid_field_type")
        dependency_refs = ()
    if any(not isinstance(item, str) or not item.strip() for item in dependency_refs):
        rejection_reasons.append("dependency_refs_invalid_member_type")
    dependency_refs = tuple(dependency_refs)

    dependency_graph = raw.get("dependency_graph")
    if dependency_graph is None:
        dependency_graph = {}
    elif not isinstance(dependency_graph, Mapping):
        rejection_reasons.append("dependency_graph_invalid_field_type")
        dependency_graph = {}
    elif any(
        not isinstance(node, str) or not node.strip()
        or not isinstance(dependencies, (list, tuple))
        or any(not isinstance(item, str) or not item.strip() for item in dependencies)
        for node, dependencies in dependency_graph.items()
    ):
        rejection_reasons.append("dependency_graph_invalid_nested_shape")
    if isinstance(dependency_graph, Mapping) and _has_cycle(dependency_graph):
        rejection_reasons.append("cyclic_dependency")

    mapping_fields = ("resource_constraints", "interruption_policy", "recovery_policy", "version_snapshots")
    normalized_mappings = {}
    for name in mapping_fields:
        value = raw.get(name)
        if value is None:
            normalized_mappings[name] = {}
        elif isinstance(value, Mapping):
            normalized_mappings[name] = dict(value)
        else:
            rejection_reasons.append(f"{name}_invalid_field_type")
            normalized_mappings[name] = {}

    capability_requirements = raw.get("capability_requirements")
    if capability_requirements is None:
        capability_requirements = ()
    if not isinstance(capability_requirements, (list, tuple)) or any(
        not isinstance(item, str) or not item.strip() for item in capability_requirements
    ):
        rejection_reasons.append("capability_requirements_invalid_shape")
        capability_requirements = ()

    adapted = {
        "task_request_id": task_request_id,
        "task_type": task_type,
        "task_goal": _text_or_empty(raw.get("task_goal", "")),
        "requester_ref": _text_or_empty(raw.get("requester_ref", "")),
        "priority": priority,
        "context_snapshot": dict(context_snapshot),
        "dependency_refs": dependency_refs,
        "resource_constraints": normalized_mappings["resource_constraints"],
        "permission_snapshot": permission_snapshot,
        "capability_requirements": tuple(capability_requirements),
        "deadline_or_timeout": _text_or_empty(raw.get("deadline_or_timeout", "")),
        "interruption_policy": normalized_mappings["interruption_policy"],
        "recovery_policy": normalized_mappings["recovery_policy"],
        "version_snapshots": normalized_mappings["version_snapshots"],
        "trace_ref": _text_or_empty(raw.get("trace_ref")) or f"task_manager_trace_{task_request_id or 'missing'}",
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
