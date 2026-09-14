# -*- coding: utf-8 -*-
"""Field State Reducer controlled skeleton static validators v1."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _event_id(event: Dict[str, Any]) -> str:
    return str(event.get("event_id", ""))


def validate_reducer_input_contract(reducer_input: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    required = (
        "admitted_field_events",
        "temporal_validity_snapshot",
        "reducer_config_snapshot",
        "reducer_version_snapshot",
    )
    for name in required:
        if not hasattr(reducer_input, name):
            issues.append(f"missing_{name}")
    return len(issues) == 0, tuple(issues)


def validate_admitted_events_only(
    events: Iterable[Dict[str, Any]],
) -> Tuple[bool, Tuple[str, ...]]:
    issues = [
        f"event_not_admitted:{_event_id(e)}"
        for e in events
        if e.get("admitted") is not True
    ]
    return len(issues) == 0, tuple(issues)


def validate_no_raw_observation(
    events: Iterable[Dict[str, Any]],
) -> Tuple[bool, Tuple[str, ...]]:
    issues = [
        f"raw_observation_not_allowed:{_event_id(e)}"
        for e in events
        if e.get("raw_observation") is True
    ]
    return len(issues) == 0, tuple(issues)


def validate_temporal_snapshot_present(
    snapshot: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    ok = bool(snapshot) and bool(snapshot.get("snapshot_id"))
    return ok, tuple() if ok else ("missing_temporal_snapshot",)


def validate_version_snapshot_present(
    version_snapshot: Any,
) -> Tuple[bool, Tuple[str, ...]]:
    required = ("reducer_version", "reduction_policy_version", "registry_version")
    issues = tuple(
        f"missing_{f}" for f in required if not getattr(version_snapshot, f, None)
    )
    return len(issues) == 0, issues


def validate_stable_event_ids(
    events: Iterable[Dict[str, Any]],
) -> Tuple[bool, Tuple[str, ...]]:
    ids = [_event_id(e) for e in events]
    if any(not i for i in ids):
        return False, ("missing_event_id",)
    if len(ids) != len(set(ids)):
        return False, ("duplicate_event_id",)
    return True, tuple()


def validate_no_direct_mutation_request(
    reducer_input: Any,
) -> Tuple[bool, Tuple[str, ...]]:
    if getattr(reducer_input, "direct_state_mutation_requested", False):
        return False, ("direct_state_mutation_forbidden",)
    return True, tuple()


def validate_replay_boundary(reducer_input: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    if getattr(reducer_input, "no_provider_recall", True) is not True:
        issues.append("provider_recall_forbidden")
    if getattr(reducer_input, "no_external_lookup", True) is not True:
        issues.append("external_lookup_forbidden")
    if getattr(reducer_input, "no_action_trigger", True) is not True:
        issues.append("action_trigger_forbidden")
    return len(issues) == 0, tuple(issues)


def validate_skeleton_output_boundary(output_obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    if getattr(output_obj, "state_mutation_executed", True):
        issues.append("state_mutation_executed_forbidden")
    if getattr(output_obj, "runtime_executed", True):
        issues.append("runtime_execution_forbidden")
    if getattr(output_obj, "reduction_decision", "") == "real_reduction_executed":
        issues.append("real_reduction_forbidden")
    return len(issues) == 0, tuple(issues)


def validate_no_runtime_capabilities(skeleton_obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    checks = {
        "runtime_implemented": False,
        "production_enabled": False,
        "database_access_allowed": False,
        "scheduler_access_allowed": False,
        "provider_recall_allowed": False,
        "external_lookup_allowed": False,
        "action_trigger_allowed": False,
        "direct_state_write_allowed": False,
        "event_mutation_allowed": False,
    }
    for name, expected in checks.items():
        if getattr(skeleton_obj, name, None) is not expected:
            issues.append(f"{name}_invalid")
    return len(issues) == 0, tuple(issues)
