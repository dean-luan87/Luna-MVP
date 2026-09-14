# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_runtime_governance.domain_profiles.vision_ocr_governance_compatibility_v1 import (
    verify_vision_ocr_compatibility_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    FORBIDDEN_PROVIDER_MANAGER_POLICIES,
    SYNTHESIS_ENTRYPOINTS,
    build_shared_provider_runtime_governance_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SPATIAL_EVIDENCE,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DOMAIN_PROFILES,
    PHASE_ID,
    PROVIDER_DISABLE_REQUEST_FIELDS,
    PROVIDER_DOMAIN_GOVERNANCE_PROFILE_FIELDS,
    PROVIDER_ENABLE_REQUEST_FIELDS,
    PROVIDER_FALLBACK_ROUTE_FIELDS,
    PROVIDER_HEALTH_SNAPSHOT_FIELDS,
    PROVIDER_MANAGER_DECISION_FIELDS,
    PROVIDER_REGISTRY_ENTRY_FIELDS,
    PROVIDER_RUNTIME_ADMISSION_CHECK_FIELDS,
    PROVIDER_RUNTIME_GOVERNANCE_MANAGER_FIELDS,
    PROVIDER_RUNTIME_STATE_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_shared_governance_candidate_only_required",
    "rule_02_manager_status_registered",
    "rule_03_synthesis_entrypoint_registered",
    "rule_04_runtime_activation_allowed_must_be_false_in_planning",
    "rule_05_provider_runtime_enabled_must_be_false_in_planning",
    "rule_06_default_enabled_provider_refs_must_be_empty_in_planning",
    "rule_07_domain_id_registered",
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
    "rule_22_final_decision_ready_for_domain_profiles",
)

PLANNING_RUNTIME_STATUSES = frozenset({"disabled", "blocked"})


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _text_fields(data: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for key in ("reason", "disable_reason", "trigger_conditions", "required_checks", "blocked_reasons"):
        val = data.get(key)
        if isinstance(val, str):
            texts.append(val)
        elif isinstance(val, (list, tuple)):
            texts.extend(str(v) for v in val)
    return texts


def validate_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only") is not True:
        return False, ["candidate_only_required"]
    return True, []


def validate_domain_id_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    domain_id = data.get("domain_id")
    if not domain_id:
        return False, ["domain_id_required"]
    if not is_registered("supported_domain_ids", domain_id):
        return False, ["domain_id_not_registered"]
    return True, []


def validate_synthesis_entrypoint_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    entrypoint = data.get("synthesis_entrypoint")
    if not entrypoint:
        return False, ["synthesis_entrypoint_required"]
    if entrypoint not in SYNTHESIS_ENTRYPOINTS:
        return False, ["synthesis_entrypoint_not_registered"]
    return True, []


def validate_runtime_activation_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_activation_allowed") is True:
        return False, ["runtime_activation_allowed_must_be_false_in_planning"]
    return True, []


def validate_provider_runtime_enabled_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("provider_runtime_enabled") is True:
        return False, ["provider_runtime_enabled_must_be_false_in_planning"]
    return True, []


def validate_default_enabled_refs_empty(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("default_enabled_provider_refs"):
        return False, ["default_enabled_provider_refs_must_be_empty_in_planning"]
    return True, []


def validate_enabled_by_default_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("enabled_by_default") is True:
        return False, ["enabled_by_default_must_be_false"]
    return True, []


def validate_runtime_enable_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_enable_allowed") is True:
        return False, ["runtime_enable_allowed_must_be_false"]
    return True, []


def validate_registry_entry_references(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ("admission_policy_ref", "health_gate_ref", "fallback_policy_ref") if not data.get(f)]
    return len(issues) == 0, issues


def validate_enable_execution_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("execution_allowed") is True:
        return False, ["enable_request_execution_allowed_must_be_false"]
    return True, []


def validate_commercial_runtime_guarded(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("requested_scope") != "commercial_runtime":
        return True, []
    if data.get("execution_allowed") is True:
        return False, ["commercial_runtime_enable_request_execution_not_allowed"]
    if data.get("approval_required") is not True:
        return False, ["commercial_runtime_enable_request_requires_approval"]
    return True, []


def validate_runtime_state_planning(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    status = data.get("runtime_status")
    if status not in PLANNING_RUNTIME_STATUSES:
        return False, ["runtime_state_status_must_be_disabled_or_blocked_in_planning"]
    return True, []


def validate_confidence_range(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    confidence = data.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
        return False, ["health_snapshot_confidence_out_of_range"]
    return True, []


def validate_tracking_lost_disable(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    lost = data.get("signal_name") == "tracking_status" and data.get("signal_value") == "tracking_lost"
    if lost and data.get("disable_required") is not True:
        return False, ["tracking_lost_requires_disable_required"]
    return True, []


def validate_high_drift_degrade_or_disable(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    high_drift = (
        data.get("signal_name") == "drift_risk" and data.get("signal_value") == "high"
    ) or data.get("signal_value") == "high_drift"
    if not high_drift:
        return True, []
    if data.get("degradation_required") is True or data.get("disable_required") is True:
        return True, []
    return False, ["high_drift_requires_degradation_or_disable"]


def validate_preserve_source_chain(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("preserve_source_chain") is not True:
        return False, ["preserve_source_chain_required"]
    return True, []


def validate_preserve_conflict_refs(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("preserve_conflict_refs") is not True:
        return False, ["preserve_conflict_refs_required"]
    return True, []


def validate_runtime_enabled_refs_empty(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
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


def validate_forbidden_policies_absent(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for text in _text_fields(data):
        for policy in FORBIDDEN_PROVIDER_MANAGER_POLICIES:
            if policy == text or policy in text:
                issues.append(f"forbidden_provider_manager_policy_present:{policy}")
    return len(issues) == 0, issues


def validate_final_decision_ready(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DOMAIN_PROFILES:
        return False, [f"final_decision_must_be_{FINAL_DECISION_READY_FOR_DOMAIN_PROFILES}"]
    return True, []


def validate_provider_runtime_governance_manager(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_GOVERNANCE_MANAGER_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_synthesis_entrypoint_registered,
        validate_runtime_activation_allowed_false,
        validate_provider_runtime_enabled_false,
        validate_default_enabled_refs_empty,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    status = data.get("manager_status")
    if status and not is_registered("manager_statuses", status):
        issues.append("manager_status_not_registered")
    return len(issues) == 0, issues


def validate_provider_registry_entry(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_REGISTRY_ENTRY_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_enabled_by_default_false,
        validate_runtime_enable_allowed_false,
        validate_registry_entry_references,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    reg_status = data.get("registration_status")
    if reg_status and not is_registered("registration_statuses", reg_status):
        issues.append("registration_status_not_registered")
    return len(issues) == 0, issues


def validate_provider_enable_request(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_ENABLE_REQUEST_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_enable_execution_false,
        validate_commercial_runtime_guarded,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_provider_disable_request(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_DISABLE_REQUEST_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    if data.get("execution_allowed") is True:
        issues.append("disable_request_execution_allowed_must_be_false")
    ok, part = validate_forbidden_policies_absent(data)
    if not ok:
        issues.extend(part)
    return len(issues) == 0, issues


def validate_provider_runtime_state(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_STATE_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_runtime_state_planning,
        validate_output_candidate_only,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_provider_health_snapshot(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_HEALTH_SNAPSHOT_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_confidence_range,
        validate_tracking_lost_disable,
        validate_high_drift_degrade_or_disable,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_provider_fallback_route(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_FALLBACK_ROUTE_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_preserve_source_chain,
        validate_preserve_conflict_refs,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_provider_runtime_admission_check(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_ADMISSION_CHECK_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    ok_domain, part = validate_domain_id_registered(data)
    if not ok_domain:
        issues.extend(part)
    if data.get("runtime_admission_allowed") is True:
        issues.append("runtime_admission_allowed_must_be_false_in_planning")
    ok_forbidden, part = validate_forbidden_policies_absent(data)
    if not ok_forbidden:
        issues.extend(part)
    return len(issues) == 0, issues


def validate_provider_domain_governance_profile(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_DOMAIN_GOVERNANCE_PROFILE_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    ok_domain, part = validate_domain_id_registered(data)
    if not ok_domain:
        issues.extend(part)
    if data.get("uses_shared_manager_skeleton") is not True:
        issues.append("uses_shared_manager_skeleton_required")
    entrypoint = data.get("synthesis_entrypoint")
    if entrypoint not in SYNTHESIS_ENTRYPOINTS:
        issues.append("domain_profile_synthesis_entrypoint_not_registered")
    return len(issues) == 0, issues


def validate_provider_manager_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_MANAGER_DECISION_FIELDS)
    issues.extend(validate_candidate_only(data)[1])
    for validator in (
        validate_domain_id_registered,
        validate_runtime_activation_allowed_false,
        validate_provider_runtime_enabled_false,
        validate_runtime_enabled_refs_empty,
        validate_final_decision_ready,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_case_bundle_domain_profile_binding(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    profiles = bundle.get("domain_profiles") or []
    entries = bundle.get("registry_entries") or []

    if entries and not profiles:
        issues.append("domain_profile_required_when_registry_entries_present")

    profile_by_domain = {p.get("domain_id"): p for p in profiles if p.get("domain_id")}
    for idx, entry in enumerate(entries):
        domain_id = entry.get("domain_id")
        profile = profile_by_domain.get(domain_id)
        if not profile:
            issues.append(f"registry_entry_{idx}:domain_profile_missing_for_{domain_id!r}")
            continue
        supported = set(profile.get("supported_output_candidate_types") or ())
        entry_types = entry.get("supported_output_candidate_types") or ()
        for ctype in entry_types:
            if ctype not in supported:
                issues.append(
                    f"registry_entry_{idx}:candidate_not_in_domain_profile:{ctype}"
                )
    return len(issues) == 0, issues


def _validate_provider_runtime_governance_bundle_core(
    bundle: Dict[str, Any],
    *,
    validate_decision: bool,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    if not registry_ok:
        issues.extend(registry_issues)

    for idx, item in enumerate(bundle.get("managers") or []):
        ok, item_issues = validate_provider_runtime_governance_manager(item)
        if not ok:
            issues.extend([f"manager_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("domain_profiles") or []):
        ok, item_issues = validate_provider_domain_governance_profile(item)
        if not ok:
            issues.extend([f"domain_profile_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("registry_entries") or []):
        ok, item_issues = validate_provider_registry_entry(item)
        if not ok:
            issues.extend([f"registry_entry_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("enable_requests") or []):
        ok, item_issues = validate_provider_enable_request(item)
        if not ok:
            issues.extend([f"enable_request_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("disable_requests") or []):
        ok, item_issues = validate_provider_disable_request(item)
        if not ok:
            issues.extend([f"disable_request_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("runtime_states") or []):
        ok, item_issues = validate_provider_runtime_state(item)
        if not ok:
            issues.extend([f"runtime_state_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("health_snapshots") or []):
        ok, item_issues = validate_provider_health_snapshot(item)
        if not ok:
            issues.extend([f"health_snapshot_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("fallback_routes") or []):
        ok, item_issues = validate_provider_fallback_route(item)
        if not ok:
            issues.extend([f"fallback_route_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(bundle.get("runtime_admission_checks") or []):
        ok, item_issues = validate_provider_runtime_admission_check(item)
        if not ok:
            issues.extend([f"admission_check_{idx}:{i}" for i in item_issues])

    if validate_decision:
        for idx, item in enumerate(bundle.get("manager_decisions") or []):
            ok, item_issues = validate_provider_manager_decision(item)
            if not ok:
                issues.extend([f"manager_decision_{idx}:{i}" for i in item_issues])

    ok_bind, bind_issues = validate_case_bundle_domain_profile_binding(bundle)
    if not ok_bind:
        issues.extend(bind_issues)

    return len(issues) == 0, issues


def validate_provider_runtime_governance_case_bundle(
    bundle: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Validate a single dry-run case bundle (shared by cases and runner)."""
    return _validate_provider_runtime_governance_bundle_core(
        bundle,
        validate_decision=False,
    )


def validate_shared_provider_runtime_governance_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_shared_provider_runtime_governance_matrix_v1()
    issues: List[str] = []

    spatial = matrix.get("spatial_evidence_catalog") or {}
    bundle = {
        "managers": [spatial.get("manager")],
        "domain_profiles": matrix.get("domain_profiles") or [],
        "registry_entries": spatial.get("registry_entries") or [],
        "enable_requests": matrix.get("enable_requests") or [],
        "disable_requests": matrix.get("disable_requests") or [],
        "runtime_states": spatial.get("runtime_states") or [],
        "health_snapshots": spatial.get("health_snapshots") or [],
        "fallback_routes": spatial.get("fallback_routes") or [],
        "runtime_admission_checks": spatial.get("admission_checks") or [],
        "manager_decisions": [matrix.get("decision")],
    }
    ok, core_issues = _validate_provider_runtime_governance_bundle_core(
        bundle,
        validate_decision=True,
    )
    issues.extend(core_issues)

    spatial_profile = next(
        (p for p in matrix.get("domain_profiles") or [] if p.get("domain_id") == DOMAIN_SPATIAL_EVIDENCE),
        {},
    )
    if len(spatial_profile.get("provider_refs") or []) != 7:
        issues.append("spatial_evidence_provider_refs_count_not_7")

    return len(issues) == 0, issues


def _no_domain_specific_manager_duplication() -> bool:
    legacy_path = (
        _REPO_ROOT
        / "capabilities/field_understanding/spatial_evidence_provider_manager"
        / "field_spatial_evidence_provider_manager_types_v1.py"
    )
    if not legacy_path.is_file():
        return True
    text = legacy_path.read_text(encoding="utf-8")
    return "SUPERSEDED_BY_SHARED_PROVIDER_RUNTIME_GOVERNANCE" in text


def summarize_extract_common_provider_manager_contract_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.midplatform.provider_runtime_governance import (  # noqa: F401
            provider_runtime_governance_registry_v1,
            provider_runtime_governance_types_v1,
        )
        from capabilities.midplatform.provider_runtime_governance.domain_profiles import (  # noqa: F401
            spatial_evidence_provider_governance_profile_v1,
            vision_ocr_governance_compatibility_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_shared_provider_runtime_governance_matrix_v1()
    matrix_ok, matrix_issues = validate_shared_provider_runtime_governance_matrix_v1(matrix)
    vision_ocr_ok, vision_ocr_issues, vision_ocr_doc = verify_vision_ocr_compatibility_v1()

    spatial = matrix.get("spatial_evidence_catalog") or {}
    manager = spatial.get("manager") or {}
    decision = matrix.get("decision") or {}
    spatial_profile = next(
        (p for p in matrix.get("domain_profiles") or [] if p.get("domain_id") == DOMAIN_SPATIAL_EVIDENCE),
        {},
    )

    no_dup = _no_domain_specific_manager_duplication()

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and vision_ocr_ok
        and len(VALIDATOR_RULE_IDS) == 22
        and manager.get("runtime_activation_allowed") is False
        and manager.get("provider_runtime_enabled") is False
        and spatial_profile.get("uses_shared_manager_skeleton") is True
        and spatial_profile.get("synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and not decision.get("runtime_enabled_provider_refs")
        and no_dup
        and decision.get("final_decision") == FINAL_DECISION_READY_FOR_DOMAIN_PROFILES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Extract Common Provider Manager Contract",
        "import_ok": import_ok,
        "shared_provider_runtime_governance_ready": ready,
        "vision_ocr_compatibility_preserved": vision_ocr_ok,
        "spatial_evidence_profile_supported": spatial_profile.get("domain_id") == DOMAIN_SPATIAL_EVIDENCE,
        "no_domain_specific_manager_duplication": no_dup,
        "manager_count": 1 if manager else 0,
        "domain_profile_count": len(matrix.get("domain_profiles") or []),
        "registry_entry_count": len(spatial.get("registry_entries") or []),
        "enable_request_count": len(matrix.get("enable_requests") or []),
        "disable_request_count": len(matrix.get("disable_requests") or []),
        "runtime_state_count": len(spatial.get("runtime_states") or []),
        "health_snapshot_count": len(spatial.get("health_snapshots") or []),
        "fallback_route_count": len(spatial.get("fallback_routes") or []),
        "admission_check_count": len(spatial.get("admission_checks") or []),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "vision_ocr_compatibility_issues": vision_ocr_issues,
        "vision_ocr_compatibility": vision_ocr_doc,
        "spatial_evidence_profile": spatial_profile,
        "runtime_activation_allowed": manager.get("runtime_activation_allowed"),
        "provider_runtime_enabled": manager.get("provider_runtime_enabled"),
        "field_synthesis_entrypoint_locked": spatial_profile.get("synthesis_entrypoint")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "route_note": matrix.get("route_note"),
        "final_decision": (
            FINAL_DECISION_READY_FOR_DOMAIN_PROFILES
            if ready
            else "SHARED_PROVIDER_RUNTIME_GOVERNANCE_SKELETON_STEP1_BLOCKED"
        ),
    }


def main() -> int:
    summary = summarize_extract_common_provider_manager_contract_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DOMAIN_PROFILES else 1


if __name__ == "__main__":
    raise SystemExit(main())
