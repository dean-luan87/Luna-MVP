from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from .field_state_reducer_behavior_policy_registry_skeleton_v1 import (
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1,
    policy_ids_v1,
)


def validate_policy_registry_complete(
    registry: Iterable[Dict[str, Any]],
) -> Tuple[bool, Tuple[str, ...]]:
    rows = tuple(registry)
    return (len(rows) == 11, tuple() if len(rows) == 11 else ("policy_count_not_11",))


def validate_policy_ids_known(
    policy_ids: Iterable[str],
) -> Tuple[bool, Tuple[str, ...]]:
    known = set(policy_ids_v1())
    incoming = set(str(x) for x in policy_ids)
    unknown = sorted(list(incoming - known))
    return len(unknown) == 0, tuple(f"unknown_policy_id:{u}" for u in unknown)


def validate_state_type_known(state_type: str) -> Tuple[bool, Tuple[str, ...]]:
    known = {
        "presence_state",
        "accessibility_state",
        "path_state",
        "obstruction_state",
        "facility_state",
        "service_state",
        "environmental_condition_state",
        "human_activity_state",
        "navigation_relevance_state",
        "temporary_overlay_state",
        "uncertainty_state",
        "conflict_state",
        "entity_field_observation_relation_state",
    }
    return state_type in known, tuple() if state_type in known else (
        "unknown_state_type",
    )


def validate_policy_snapshots_present(
    snapshot: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    required = (
        "policy_registry_snapshot",
        "eligibility_matrix_snapshot",
        "precedence_snapshot",
        "composition_snapshot",
    )
    missing = tuple(
        f"missing_{k}" for k in required if k not in snapshot or not snapshot[k]
    )
    return len(missing) == 0, missing


def validate_no_runtime_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("runtime_requested", False) is False, (
        tuple()
        if payload.get("runtime_requested", False) is False
        else ("runtime_execution_forbidden",)
    )


def validate_no_state_write_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("state_write_requested", False) is False, (
        tuple()
        if payload.get("state_write_requested", False) is False
        else ("direct_state_write_forbidden",)
    )


def validate_no_fact_promotion_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("fact_promotion_requested", False) is False, (
        tuple()
        if payload.get("fact_promotion_requested", False) is False
        else ("fact_promotion_forbidden",)
    )


def validate_no_action_trigger_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("action_trigger_requested", False) is False, (
        tuple()
        if payload.get("action_trigger_requested", False) is False
        else ("action_trigger_forbidden",)
    )


def validate_no_provider_recall_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("provider_recall_requested", False) is False, (
        tuple()
        if payload.get("provider_recall_requested", False) is False
        else ("provider_recall_forbidden",)
    )


def validate_no_external_lookup_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("external_lookup_requested", False) is False, (
        tuple()
        if payload.get("external_lookup_requested", False) is False
        else ("external_lookup_forbidden",)
    )


def validate_no_model_call_request(
    payload: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    return payload.get("model_call_requested", False) is False, (
        tuple()
        if payload.get("model_call_requested", False) is False
        else ("model_call_forbidden",)
    )


def validate_skeleton_decision_boundary(
    decision: Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    if decision.get("skeleton_only") is not True:
        issues.append("skeleton_only_required")
    if decision.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if decision.get("policy_execution_executed") is not False:
        issues.append("policy_execution_forbidden")
    if decision.get("state_mutation_executed") is not False:
        issues.append("state_mutation_forbidden")
    if decision.get("fact_promotion_executed") is not False:
        issues.append("fact_promotion_forbidden")
    if decision.get("action_trigger_executed") is not False:
        issues.append("action_trigger_forbidden")
    if decision.get("runtime_execution") is not False:
        issues.append("runtime_execution_forbidden")
    return len(issues) == 0, tuple(issues)


def default_registry() -> Tuple[Dict[str, Any], ...]:
    return FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
