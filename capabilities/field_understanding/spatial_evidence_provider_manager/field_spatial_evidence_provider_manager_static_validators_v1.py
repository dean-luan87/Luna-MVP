# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Manager Skeleton Planning — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    PROVIDER_ROLES as ADMISSION_PROVIDER_ROLES,
)
from capabilities.field_understanding.spatial_evidence_provider_manager.field_spatial_evidence_provider_manager_registry_v1 import (
    FORBIDDEN_PROVIDER_MANAGER_POLICIES,
    build_provider_manager_planning_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.spatial_evidence_provider_manager.field_spatial_evidence_provider_manager_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    PHASE_ID,
    PROVIDER_DISABLE_REQUEST_FIELDS,
    PROVIDER_ENABLE_REQUEST_FIELDS,
    PROVIDER_FALLBACK_ROUTE_FIELDS,
    PROVIDER_HEALTH_SNAPSHOT_FIELDS,
    PROVIDER_MANAGER_PLANNING_DECISION_FIELDS,
    PROVIDER_REGISTRY_ENTRY_FIELDS,
    PROVIDER_RUNTIME_STATE_FIELDS,
    SPATIAL_EVIDENCE_PROVIDER_MANAGER_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_manager_skeleton_candidate_only_required",
    "rule_02_manager_status_registered",
    "rule_03_field_synthesis_entrypoint_must_be_v1",
    "rule_04_runtime_activation_allowed_must_be_false_in_planning",
    "rule_05_provider_runtime_enabled_must_be_false_in_planning",
    "rule_06_default_enabled_provider_refs_must_be_empty_in_planning",
    "rule_07_provider_role_registered",
    "rule_08_registry_entry_enabled_by_default_must_be_false",
    "rule_09_registry_entry_runtime_enable_allowed_must_be_false",
    "rule_10_registry_entry_must_reference_admission_artifacts",
    "rule_11_enable_request_execution_allowed_must_be_false",
    "rule_12_commercial_runtime_enable_request_guarded",
    "rule_13_runtime_state_status_disabled_or_blocked_in_planning",
    "rule_14_health_snapshot_confidence_range",
    "rule_15_tracking_lost_requires_disable_required",
    "rule_16_high_drift_requires_degrade_or_disable",
    "rule_17_fallback_route_preserve_source_chain",
    "rule_18_fallback_route_preserve_conflict_refs",
    "rule_19_runtime_enabled_provider_refs_must_be_empty_in_planning",
    "rule_20_output_candidate_only_no_direct_paths",
    "rule_21_forbidden_provider_manager_policies_absent",
    "rule_22_final_decision_ready_for_dryrun_cases",
)

PLANNING_RUNTIME_STATUSES = frozenset({"disabled", "blocked"})


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _text_fields(data: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for key in (
        "reason",
        "disable_reason",
        "trigger_conditions",
        "required_checks",
    ):
        val = data.get(key)
        if isinstance(val, str):
            texts.append(val)
        elif isinstance(val, (list, tuple)):
            texts.extend(str(v) for v in val)
    return texts


def validate_manager_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only") is not True:
        return False, ["candidate_only_required"]
    return True, []


def validate_manager_status_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    status = data.get("manager_status")
    if not status:
        return False, ["manager_status_required"]
    if not is_registered("manager_statuses", status):
        return False, ["manager_status_not_registered"]
    return True, []


def validate_field_synthesis_entrypoint_must_be_v1(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        return False, [f"field_synthesis_entrypoint_must_be_{FIELD_SYNTHESIS_ENTRYPOINT}"]
    return True, []


def validate_runtime_activation_allowed_must_be_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_activation_allowed") is True:
        return False, ["runtime_activation_allowed_must_be_false_in_planning"]
    return True, []


def validate_provider_runtime_enabled_must_be_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("provider_runtime_enabled") is True:
        return False, ["provider_runtime_enabled_must_be_false_in_planning"]
    return True, []


def validate_default_enabled_provider_refs_empty(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("default_enabled_provider_refs"):
        return False, ["default_enabled_provider_refs_must_be_empty_in_planning"]
    return True, []


def validate_provider_role_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    role = data.get("provider_role")
    if not role:
        return False, ["provider_role_required"]
    if role not in ADMISSION_PROVIDER_ROLES and not is_registered("provider_roles", role):
        return False, ["provider_role_not_registered"]
    return True, []


def validate_registry_entry_enabled_by_default_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("enabled_by_default") is True:
        return False, ["registry_entry_enabled_by_default_must_be_false"]
    return True, []


def validate_registry_entry_runtime_enable_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_enable_allowed") is True:
        return False, ["registry_entry_runtime_enable_allowed_must_be_false"]
    return True, []


def validate_registry_entry_references(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for field in ("admission_policy_ref", "health_gate_ref", "fallback_policy_ref"):
        if not data.get(field):
            issues.append(f"{field}_required")
    return len(issues) == 0, issues


def validate_enable_request_execution_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("execution_allowed") is True:
        return False, ["enable_request_execution_allowed_must_be_false"]
    return True, []


def validate_commercial_runtime_enable_request_guarded(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("requested_scope") != "commercial_runtime":
        return True, []
    if data.get("execution_allowed") is True:
        return False, ["commercial_runtime_enable_request_execution_not_allowed"]
    if data.get("approval_required") is not True:
        return False, ["commercial_runtime_enable_request_requires_approval"]
    return True, []


def validate_runtime_state_status_planning(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    status = data.get("runtime_status")
    if status not in PLANNING_RUNTIME_STATUSES:
        return False, ["runtime_state_status_must_be_disabled_or_blocked_in_planning"]
    if not is_registered("runtime_statuses", status):
        return False, ["runtime_status_not_registered"]
    return True, []


def validate_health_snapshot_confidence_range(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    confidence = data.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
        return False, ["health_snapshot_confidence_out_of_range"]
    return True, []


def validate_tracking_lost_requires_disable_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("tracking_status") == "tracking_lost" and data.get("disable_required") is not True:
        return False, ["tracking_lost_requires_disable_required"]
    return True, []


def validate_high_drift_requires_degrade_or_disable(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("drift_risk") != "high":
        return True, []
    if data.get("degradation_required") is True or data.get("disable_required") is True:
        return True, []
    return False, ["high_drift_requires_degradation_or_disable"]


def validate_fallback_route_preserve_source_chain(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("preserve_source_chain") is not True:
        return False, ["fallback_route_preserve_source_chain_required"]
    return True, []


def validate_fallback_route_preserve_conflict_refs(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("preserve_conflict_refs") is not True:
        return False, ["fallback_route_preserve_conflict_refs_required"]
    return True, []


def validate_runtime_enabled_provider_refs_empty(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_enabled_provider_refs"):
        return False, ["runtime_enabled_provider_refs_must_be_empty_in_planning"]
    return True, []


def validate_output_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    output_status = data.get("output_status")
    if output_status and not is_registered("output_statuses", output_status):
        return False, ["output_status_not_registered"]
    if output_status not in ("no_output", "candidate_output_only", "degraded_candidate_output", "blocked"):
        return False, ["output_status_must_be_candidate_only_path"]
    return True, []


def validate_forbidden_provider_manager_policies_absent(
    data: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for text in _text_fields(data):
        for policy in FORBIDDEN_PROVIDER_MANAGER_POLICIES:
            if policy == text or policy in text:
                issues.append(f"forbidden_provider_manager_policy_present:{policy}")
    return len(issues) == 0, issues


def validate_final_decision_ready_for_dryrun_cases(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DRYRUN_CASES:
        return False, [f"final_decision_must_be_{FINAL_DECISION_READY_FOR_DRYRUN_CASES}"]
    return True, []


def validate_spatial_evidence_provider_manager(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SPATIAL_EVIDENCE_PROVIDER_MANAGER_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    for validator in (
        validate_manager_status_registered,
        validate_field_synthesis_entrypoint_must_be_v1,
        validate_runtime_activation_allowed_must_be_false,
        validate_provider_runtime_enabled_must_be_false,
        validate_default_enabled_provider_refs_empty,
        validate_forbidden_provider_manager_policies_absent,
    ):
        ok, part_issues = validator(data)
        if not ok:
            issues.extend(part_issues)
    return len(issues) == 0, issues


def validate_provider_registry_entry(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_REGISTRY_ENTRY_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    for validator in (
        validate_provider_role_registered,
        validate_registry_entry_enabled_by_default_false,
        validate_registry_entry_runtime_enable_allowed_false,
        validate_registry_entry_references,
        validate_forbidden_provider_manager_policies_absent,
    ):
        ok, part_issues = validator(data)
        if not ok:
            issues.extend(part_issues)
    reg_status = data.get("registration_status")
    if reg_status and not is_registered("registration_statuses", reg_status):
        issues.append("registration_status_not_registered")
    return len(issues) == 0, issues


def validate_provider_enable_request(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_ENABLE_REQUEST_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    for validator in (
        validate_enable_request_execution_allowed_false,
        validate_commercial_runtime_enable_request_guarded,
        validate_forbidden_provider_manager_policies_absent,
    ):
        ok, part_issues = validator(data)
        if not ok:
            issues.extend(part_issues)
    scope = data.get("requested_scope")
    if scope and not is_registered("request_scopes", scope):
        issues.append("requested_scope_not_registered")
    requested_by = data.get("requested_by")
    if requested_by and not is_registered("requested_by", requested_by):
        issues.append("requested_by_not_registered")
    return len(issues) == 0, issues


def validate_provider_disable_request(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_DISABLE_REQUEST_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    if data.get("execution_allowed") is True:
        issues.append("disable_request_execution_allowed_must_be_false_in_planning")
    ok19, i19 = validate_forbidden_provider_manager_policies_absent(data)
    if not ok19:
        issues.extend(i19)
    return len(issues) == 0, issues


def validate_provider_runtime_state(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_STATE_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    ok13, i13 = validate_runtime_state_status_planning(data)
    ok20, i20 = validate_output_candidate_only(data)
    ok21, i21 = validate_forbidden_provider_manager_policies_absent(data)
    if not ok13:
        issues.extend(i13)
    if not ok20:
        issues.extend(i20)
    if not ok21:
        issues.extend(i21)
    for field, domain in (
        ("health_status", "health_statuses"),
        ("fallback_status", "fallback_statuses"),
    ):
        val = data.get(field)
        if val and not is_registered(domain, val):
            issues.append(f"{field}_not_registered")
    return len(issues) == 0, issues


def validate_provider_health_snapshot(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_HEALTH_SNAPSHOT_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    for validator in (
        validate_health_snapshot_confidence_range,
        validate_tracking_lost_requires_disable_required,
        validate_high_drift_requires_degrade_or_disable,
        validate_forbidden_provider_manager_policies_absent,
    ):
        ok, part_issues = validator(data)
        if not ok:
            issues.extend(part_issues)
    for field, domain in (
        ("tracking_status", "tracking_statuses"),
        ("drift_risk", "drift_risk_levels"),
        ("source_freshness", "source_freshness_levels"),
        ("health_decision", "health_decisions"),
    ):
        val = data.get(field)
        if val and not is_registered(domain, val):
            issues.append(f"{field}_not_registered")
    return len(issues) == 0, issues


def validate_provider_fallback_route(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_FALLBACK_ROUTE_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    for validator in (
        validate_fallback_route_preserve_source_chain,
        validate_fallback_route_preserve_conflict_refs,
        validate_forbidden_provider_manager_policies_absent,
    ):
        ok, part_issues = validator(data)
        if not ok:
            issues.extend(part_issues)
    mode = data.get("fallback_mode")
    if mode and not is_registered("fallback_modes", mode):
        issues.append("fallback_mode_not_registered")
    return len(issues) == 0, issues


def validate_provider_manager_planning_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_MANAGER_PLANNING_DECISION_FIELDS)
    ok1, i1 = validate_manager_candidate_only(data)
    issues.extend(i1)
    for validator in (
        validate_runtime_activation_allowed_must_be_false,
        validate_provider_runtime_enabled_must_be_false,
        validate_runtime_enabled_provider_refs_empty,
        validate_final_decision_ready_for_dryrun_cases,
        validate_forbidden_provider_manager_policies_absent,
    ):
        ok, part_issues = validator(data)
        if not ok:
            issues.extend(part_issues)
    return len(issues) == 0, issues


def validate_provider_manager_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_provider_manager_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    if not registry_ok:
        issues.extend(registry_issues)

    manager = matrix.get("manager") or {}
    ok, item_issues = validate_spatial_evidence_provider_manager(manager)
    if not ok:
        issues.extend([f"manager:{i}" for i in item_issues])

    for idx, item in enumerate(matrix.get("registry_entries") or []):
        ok, item_issues = validate_provider_registry_entry(item)
        if not ok:
            issues.extend([f"registry_entry_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(matrix.get("enable_requests") or []):
        ok, item_issues = validate_provider_enable_request(item)
        if not ok:
            issues.extend([f"enable_request_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(matrix.get("disable_requests") or []):
        ok, item_issues = validate_provider_disable_request(item)
        if not ok:
            issues.extend([f"disable_request_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(matrix.get("runtime_states") or []):
        ok, item_issues = validate_provider_runtime_state(item)
        if not ok:
            issues.extend([f"runtime_state_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(matrix.get("health_snapshots") or []):
        ok, item_issues = validate_provider_health_snapshot(item)
        if not ok:
            issues.extend([f"health_snapshot_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(matrix.get("fallback_routes") or []):
        ok, item_issues = validate_provider_fallback_route(item)
        if not ok:
            issues.extend([f"fallback_route_{idx}:{i}" for i in item_issues])

    decision = matrix.get("decision") or {}
    ok_dec, dec_issues = validate_provider_manager_planning_decision(decision)
    if not ok_dec:
        issues.extend([f"decision:{i}" for i in dec_issues])

    expected_counts = {
        "registry_entries": 7,
        "runtime_states": 7,
        "health_snapshots": 7,
        "fallback_routes": 7,
    }
    for key, expected in expected_counts.items():
        actual = len(matrix.get(key) or [])
        if actual != expected:
            issues.append(f"{key}_count_expected_{expected}_actual_{actual}")

    if len(matrix.get("enable_requests") or []) < 1:
        issues.append("enable_request_count_below_minimum")
    if len(matrix.get("disable_requests") or []) < 1:
        issues.append("disable_request_count_below_minimum")

    return len(issues) == 0, issues


def summarize_step1_baseline_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.field_understanding.spatial_evidence_provider_manager import (  # noqa: F401
            field_spatial_evidence_provider_manager_registry_v1,
            field_spatial_evidence_provider_manager_types_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_provider_manager_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_provider_manager_planning_matrix_v1(matrix)
    manager = matrix.get("manager") or {}
    decision = matrix.get("decision") or {}

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) == 22
        and manager.get("runtime_activation_allowed") is False
        and manager.get("provider_runtime_enabled") is False
        and not manager.get("default_enabled_provider_refs")
        and not decision.get("runtime_enabled_provider_refs")
        and manager.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and decision.get("final_decision") == FINAL_DECISION_READY_FOR_DRYRUN_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Types / Registry / Validators",
        "import_ok": import_ok,
        "manager_count": 1 if manager else 0,
        "registry_entry_count": len(matrix.get("registry_entries") or []),
        "enable_request_count": len(matrix.get("enable_requests") or []),
        "disable_request_count": len(matrix.get("disable_requests") or []),
        "runtime_state_count": len(matrix.get("runtime_states") or []),
        "health_snapshot_count": len(matrix.get("health_snapshots") or []),
        "fallback_route_count": len(matrix.get("fallback_routes") or []),
        "planning_decision_count": 1 if decision else 0,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "validator_rule_ids": list(VALIDATOR_RULE_IDS),
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "runtime_activation_allowed": manager.get("runtime_activation_allowed"),
        "provider_runtime_enabled": manager.get("provider_runtime_enabled"),
        "default_enabled_provider_refs_empty": not manager.get("default_enabled_provider_refs"),
        "runtime_enabled_provider_refs_empty": not decision.get("runtime_enabled_provider_refs"),
        "field_synthesis_entrypoint_locked": manager.get("field_synthesis_entrypoint")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only_enforced": all(
            item.get("candidate_only") is True
            for collection_key in (
                "registry_entries",
                "enable_requests",
                "disable_requests",
                "runtime_states",
                "health_snapshots",
                "fallback_routes",
            )
            for item in (matrix.get(collection_key) or [])
        )
        and manager.get("candidate_only") is True
        and decision.get("candidate_only") is True,
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES
            if ready
            else "FIELD_SPATIAL_EVIDENCE_PROVIDER_MANAGER_SKELETON_PLANNING_STEP1_BLOCKED"
        ),
    }


def main() -> int:
    summary = summarize_step1_baseline_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
