# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    FORBIDDEN_PROVIDER_ADMISSION_POLICIES,
    GPL_BACKEND_REFS,
    OBSERVATION_ONLY_PROVIDER_REFS,
    build_provider_admission_planning_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    PHASE_ID,
    PROVIDER_ADMISSION_PLANNING_DECISION_FIELDS,
    PROVIDER_CAPABILITY_PROFILE_FIELDS,
    PROVIDER_FALLBACK_POLICY_FIELDS,
    PROVIDER_HEALTH_GATE_FIELDS,
    PROVIDER_RUNTIME_ADMISSION_CANDIDATE_FIELDS,
    SPATIAL_EVIDENCE_PROVIDER_ADMISSION_POLICY_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_provider_admission_candidate_only_required",
    "rule_02_provider_role_registered",
    "rule_03_admission_mode_registered",
    "rule_04_allowed_runtime_scope_registered",
    "rule_05_required_candidate_types_registered",
    "rule_06_field_synthesis_entrypoint_required",
    "rule_07_field_synthesis_entrypoint_must_be_v1",
    "rule_08_runtime_admission_requires_all_gates_passed",
    "rule_09_commercial_runtime_requires_license_gate_passed",
    "rule_10_gpl_provider_not_commercial_runtime_allowed",
    "rule_11_observation_provider_no_runtime_admission",
    "rule_12_capability_profile_supported_candidate_types_required",
    "rule_13_required_candidates_subset_of_supported",
    "rule_14_health_gate_confidence_floor_range",
    "rule_15_tracking_lost_must_block_or_disable",
    "rule_16_high_drift_must_degrade_or_block",
    "rule_17_fallback_required_must_have_fallback_policy_ref",
    "rule_18_fallback_policy_preserve_source_chain",
    "rule_19_forbidden_provider_admission_policies_absent",
    "rule_20_final_decision_ready_for_dryrun_cases",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _policy_text_fields(data: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for key in (
        "admission_reasons",
        "blocked_reasons",
        "disable_conditions",
        "fallback_trigger_conditions",
        "disable_reason",
    ):
        val = data.get(key)
        if isinstance(val, str):
            texts.append(val)
        elif isinstance(val, (list, tuple)):
            texts.extend(str(v) for v in val)
    return texts


def validate_provider_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only") is not True:
        return False, ["candidate_only_required"]
    return True, []


def validate_spatial_evidence_provider_admission_policy(
    data: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SPATIAL_EVIDENCE_PROVIDER_ADMISSION_POLICY_FIELDS)
    ok1, i1 = validate_provider_candidate_only(data)
    issues.extend(i1)

    ok2, i2 = validate_provider_role_registered(data)
    ok3, i3 = validate_admission_mode_registered(data)
    ok4, i4 = validate_allowed_runtime_scope_registered(data)
    ok5, i5 = validate_required_candidate_types_registered(data)
    ok6, i6 = validate_field_synthesis_entrypoint_required(data)
    ok7, i7 = validate_field_synthesis_entrypoint_must_be_v1(data)
    ok10, i10 = validate_gpl_provider_not_commercial_runtime_allowed(data)
    ok11, i11 = validate_observation_provider_no_runtime_admission(data)
    ok17, i17 = validate_fallback_required_must_have_fallback_policy_ref(data)
    ok19, i19 = validate_forbidden_provider_admission_policies_absent(data)

    for ok_part, part_issues in (
        (ok2, i2),
        (ok3, i3),
        (ok4, i4),
        (ok5, i5),
        (ok6, i6),
        (ok7, i7),
        (ok10, i10),
        (ok11, i11),
        (ok17, i17),
        (ok19, i19),
    ):
        if not ok_part:
            issues.extend(part_issues)

    return len(issues) == 0, issues


def validate_provider_capability_profile(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_CAPABILITY_PROFILE_FIELDS)
    ok1, i1 = validate_provider_candidate_only(data)
    issues.extend(i1)

    ok12, i12 = validate_capability_profile_supported_candidate_types_required(data)
    ok19, i19 = validate_forbidden_provider_admission_policies_absent(data)
    if not ok12:
        issues.extend(i12)
    if not ok19:
        issues.extend(i19)

    for field in ("latency_class", "compute_class", "reliability_class"):
        val = data.get(field)
        if val and not is_registered(f"{field}s".replace("latency_classes", "latency_classes"), val):
            domain = {
                "latency_class": "latency_classes",
                "compute_class": "compute_classes",
                "reliability_class": "reliability_classes",
            }[field]
            if not is_registered(domain, val):
                issues.append(f"{field}_not_registered")

    for fit_field in ("wearable_fit", "offline_fit", "semantic_extension_fit"):
        val = data.get(fit_field)
        if val and not is_registered("fit_levels", val):
            issues.append(f"{fit_field}_not_registered")

    return len(issues) == 0, issues


def validate_provider_health_gate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_HEALTH_GATE_FIELDS)
    ok1, i1 = validate_provider_candidate_only(data)
    issues.extend(i1)

    ok14, i14 = validate_health_gate_confidence_floor_range(data)
    ok15, i15 = validate_tracking_lost_must_block_or_disable(data)
    ok16, i16 = validate_high_drift_must_degrade_or_block(data)
    ok19, i19 = validate_forbidden_provider_admission_policies_absent(data)
    if not ok14:
        issues.extend(i14)
    if not ok15:
        issues.extend(i15)
    if not ok16:
        issues.extend(i16)
    if not ok19:
        issues.extend(i19)

    return len(issues) == 0, issues


def validate_provider_fallback_policy(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_FALLBACK_POLICY_FIELDS)
    ok1, i1 = validate_provider_candidate_only(data)
    issues.extend(i1)

    ok18, i18 = validate_fallback_policy_preserve_source_chain(data)
    ok19, i19 = validate_forbidden_provider_admission_policies_absent(data)
    if not ok18:
        issues.extend(i18)
    if not ok19:
        issues.extend(i19)

    if data.get("fallback_mode") and not is_registered("fallback_modes", data["fallback_mode"]):
        issues.append("fallback_mode_not_registered")

    return len(issues) == 0, issues


def validate_provider_runtime_admission_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_ADMISSION_CANDIDATE_FIELDS)
    ok1, i1 = validate_provider_candidate_only(data)
    issues.extend(i1)

    ok8, i8 = validate_runtime_admission_requires_all_gates_passed(data)
    ok9, i9 = validate_commercial_runtime_requires_license_gate_passed(data)
    ok11, i11 = validate_observation_provider_no_runtime_admission(data)
    ok19, i19 = validate_forbidden_provider_admission_policies_absent(data)
    if not ok8:
        issues.extend(i8)
    if not ok9:
        issues.extend(i9)
    if not ok11:
        issues.extend(i11)
    if not ok19:
        issues.extend(i19)

    if data.get("admission_stage") and not is_registered("admission_stages", data["admission_stage"]):
        issues.append("admission_stage_not_registered")

    return len(issues) == 0, issues


def validate_provider_admission_planning_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_ADMISSION_PLANNING_DECISION_FIELDS)
    ok1, i1 = validate_provider_candidate_only(data)
    issues.extend(i1)
    ok20, i20 = validate_final_decision_ready_for_dryrun_cases(data)
    if not ok20:
        issues.extend(i20)

    if not data.get("fallback_required"):
        issues.append("fallback_required_must_be_true")
    if not data.get("health_gate_required"):
        issues.append("health_gate_required_must_be_true")
    if not data.get("provider_replaceability_required"):
        issues.append("provider_replaceability_required_must_be_true")
    if data.get("runtime_admission_candidates"):
        issues.append("runtime_admission_candidates_must_be_empty_in_planning_v1")
    if data.get("commercial_runtime_candidates"):
        issues.append("commercial_runtime_candidates_must_be_empty_in_planning_v1")

    return len(issues) == 0, issues


def validate_provider_role_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    role = data.get("provider_role")
    if not role:
        return False, ["provider_role_required"]
    if not is_registered("provider_roles", role):
        return False, ["provider_role_not_registered"]
    return True, []


def validate_admission_mode_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    mode = data.get("admission_mode")
    if not mode:
        return False, ["admission_mode_required"]
    if not is_registered("admission_modes", mode):
        return False, ["admission_mode_not_registered"]
    return True, []


def validate_allowed_runtime_scope_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    scope = data.get("allowed_runtime_scope")
    if not scope:
        return False, ["allowed_runtime_scope_required"]
    if not is_registered("runtime_scopes", scope):
        return False, ["allowed_runtime_scope_not_registered"]
    return True, []


def validate_required_candidate_types_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    required = data.get("required_candidate_types") or ()
    if not required:
        return False, ["required_candidate_types_required"]
    issues: List[str] = []
    for ctype in required:
        if not is_registered("output_candidate_types", ctype):
            issues.append(f"required_candidate_type_not_registered:{ctype}")
    return len(issues) == 0, issues


def validate_field_synthesis_entrypoint_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not data.get("field_synthesis_entrypoint"):
        return False, ["field_synthesis_entrypoint_required"]
    return True, []


def validate_field_synthesis_entrypoint_must_be_v1(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        return False, [f"field_synthesis_entrypoint_must_be_{FIELD_SYNTHESIS_ENTRYPOINT}"]
    return True, []


def validate_runtime_admission_requires_all_gates_passed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_admission_allowed") is not True:
        return True, []
    issues: List[str] = []
    for gate in (
        "license_gate_passed",
        "adapter_contract_passed",
        "provider_policy_passed",
        "capability_profile_passed",
        "health_gate_passed",
        "fallback_policy_passed",
        "static_validation_passed",
    ):
        if data.get(gate) is not True:
            issues.append(f"runtime_admission_requires_{gate}")
    return len(issues) == 0, issues


def validate_commercial_runtime_requires_license_gate_passed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("commercial_runtime_allowed") is not True:
        return True, []
    if data.get("license_gate_passed") is not True:
        return False, ["commercial_runtime_requires_license_gate_passed"]
    return True, []


def validate_gpl_provider_not_commercial_runtime_allowed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    backend = data.get("backend_ref")
    if backend in GPL_BACKEND_REFS and data.get("commercial_runtime_allowed") is True:
        return False, ["gpl_provider_commercial_runtime_not_allowed"]
    return True, []


def validate_observation_provider_no_runtime_admission(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    provider_ref = data.get("provider_ref")
    admission_mode = data.get("admission_mode")
    if provider_ref in OBSERVATION_ONLY_PROVIDER_REFS or admission_mode == "observation_only":
        if data.get("runtime_admission_allowed") is True:
            return False, ["observation_provider_runtime_admission_not_allowed"]
    return True, []


def validate_capability_profile_supported_candidate_types_required(
    data: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    if not (data.get("supported_candidate_types") or ()):
        return False, ["supported_candidate_types_required"]
    return True, []


def validate_required_candidates_subset_of_supported(
    policy: Dict[str, Any],
    profile: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    supported = set(profile.get("supported_candidate_types") or ())
    required = policy.get("required_candidate_types") or ()
    issues = [f"required_not_supported:{r}" for r in required if r not in supported]
    return len(issues) == 0, issues


def validate_health_gate_confidence_floor_range(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    floor = data.get("confidence_floor")
    if not isinstance(floor, (int, float)) or not 0.0 <= float(floor) <= 1.0:
        return False, ["confidence_floor_out_of_range"]
    return True, []


def validate_tracking_lost_must_block_or_disable(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    blocked = set(data.get("blocked_conditions") or ())
    disabled = set(data.get("disable_conditions") or ())
    if "tracking_lost" in blocked or "tracking_lost" in disabled:
        return True, []
    tracking_policy = data.get("tracking_lost_policy")
    if tracking_policy in ("disable_provider", "fallback_to_mock", "needs_more_observation"):
        return True, []
    return False, ["tracking_lost_must_block_or_disable"]


def validate_high_drift_must_degrade_or_block(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    degraded = set(data.get("degraded_conditions") or ())
    blocked = set(data.get("blocked_conditions") or ())
    disabled = set(data.get("disable_conditions") or ())
    if "high_drift" in degraded or "high_drift" in blocked or "high_drift" in disabled:
        return True, []
    drift_policy = data.get("drift_policy")
    if drift_policy in ("downweight_evidence", "request_relocalization", "disable_provider", "needs_more_observation"):
        return True, []
    return False, ["high_drift_must_degrade_or_block"]


def validate_fallback_required_must_have_fallback_policy_ref(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    ref = data.get("fallback_policy_ref")
    if not ref:
        return False, ["fallback_policy_ref_required"]
    return True, []


def validate_fallback_policy_preserve_source_chain(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("preserve_source_chain") is not True:
        return False, ["preserve_source_chain_required"]
    return True, []


def validate_forbidden_provider_admission_policies_absent(
    data: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for text in _policy_text_fields(data):
        for policy in FORBIDDEN_PROVIDER_ADMISSION_POLICIES:
            if policy == text or policy in text:
                issues.append(f"forbidden_provider_admission_policy_present:{policy}")
    return len(issues) == 0, issues


def validate_final_decision_ready_for_dryrun_cases(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DRYRUN_CASES:
        return False, [f"final_decision_must_be_{FINAL_DECISION_READY_FOR_DRYRUN_CASES}"]
    return True, []


def validate_provider_admission_case_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a single dry-run case bundle (shared by cases and runner)."""
    return _validate_provider_admission_bundle_core(
        bundle,
        validate_decision=False,
        enforce_planning_runtime_block=False,
    )


def _validate_provider_admission_bundle_core(
    bundle: Dict[str, Any],
    *,
    validate_decision: bool,
    enforce_planning_runtime_block: bool,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    if not registry_ok:
        issues.extend(registry_issues)

    policies = bundle.get("admission_policies") or []
    profiles = bundle.get("capability_profiles") or []
    health_gates = bundle.get("health_gates") or []
    fallbacks = bundle.get("fallback_policies") or []
    admissions = bundle.get("runtime_admission_candidates") or []
    decision = bundle.get("decision") or {}

    profile_by_provider = {p.get("provider_ref"): p for p in profiles}
    policy_by_provider = {p.get("provider_ref"): p for p in policies}

    for idx, item in enumerate(policies):
        ok, item_issues = validate_spatial_evidence_provider_admission_policy(item)
        if not ok:
            issues.extend([f"policy_{idx}:{i}" for i in item_issues])
        profile = profile_by_provider.get(item.get("provider_ref"))
        if profile:
            ok13, i13 = validate_required_candidates_subset_of_supported(item, profile)
            if not ok13:
                issues.extend([f"policy_{idx}:{i}" for i in i13])

    for idx, item in enumerate(profiles):
        ok, item_issues = validate_provider_capability_profile(item)
        if not ok:
            issues.extend([f"profile_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(health_gates):
        ok, item_issues = validate_provider_health_gate(item)
        if not ok:
            issues.extend([f"health_gate_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(fallbacks):
        ok, item_issues = validate_provider_fallback_policy(item)
        if not ok:
            issues.extend([f"fallback_{idx}:{i}" for i in item_issues])
        policy = policy_by_provider.get(item.get("provider_ref"))
        if policy and policy.get("fallback_policy_ref") != item.get("fallback_policy_ref"):
            issues.append(f"fallback_{idx}:fallback_policy_ref_mismatch")

    for idx, item in enumerate(admissions):
        ok, item_issues = validate_provider_runtime_admission_candidate(item)
        if not ok:
            issues.extend([f"admission_{idx}:{i}" for i in item_issues])
        policy = policy_by_provider.get(item.get("provider_ref"))
        if policy and policy.get("commercial_runtime_allowed") is True:
            if item.get("license_gate_passed") is not True:
                issues.append(f"admission_{idx}:commercial_runtime_requires_license_gate_passed")

    if validate_decision:
        ok_dec, dec_issues = validate_provider_admission_planning_decision(decision)
        if not ok_dec:
            issues.extend([f"decision:{i}" for i in dec_issues])

    if enforce_planning_runtime_block:
        for admission in admissions:
            if admission.get("runtime_admission_allowed") is True:
                issues.append(
                    f"planning_runtime_admission_not_allowed:{admission.get('provider_ref')}"
                )

    return len(issues) == 0, issues


def validate_provider_admission_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_provider_admission_planning_matrix_v1()
    issues: List[str] = []

    ok, core_issues = _validate_provider_admission_bundle_core(
        matrix,
        validate_decision=True,
        enforce_planning_runtime_block=True,
    )
    issues.extend(core_issues)

    expected_counts = {
        "admission_policies": 7,
        "capability_profiles": 7,
        "health_gates": 7,
        "fallback_policies": 7,
        "runtime_admission_candidates": 7,
    }
    for key, expected in expected_counts.items():
        actual = len(matrix.get(key) or [])
        if actual != expected:
            issues.append(f"{key}_count_expected_{expected}_actual_{actual}")

    return len(issues) == 0, issues


def _gpl_commercial_blocked(matrix: Dict[str, Any]) -> bool:
    for policy in matrix.get("admission_policies") or []:
        if policy.get("backend_ref") in GPL_BACKEND_REFS:
            if policy.get("commercial_runtime_allowed") is True:
                return False
    return True


def _observation_runtime_blocked(matrix: Dict[str, Any]) -> bool:
    for item in matrix.get("runtime_admission_candidates") or []:
        if item.get("provider_ref") in OBSERVATION_ONLY_PROVIDER_REFS:
            if item.get("runtime_admission_allowed") is True:
                return False
    return True


def summarize_step1_baseline_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.field_understanding.spatial_evidence_provider_admission import (  # noqa: F401
            field_spatial_evidence_provider_admission_registry_v1,
            field_spatial_evidence_provider_admission_types_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_provider_admission_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_provider_admission_planning_matrix_v1(matrix)
    decision = matrix.get("decision") or {}

    gpl_blocked = _gpl_commercial_blocked(matrix)
    observation_blocked = _observation_runtime_blocked(matrix)

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) == 20
        and gpl_blocked
        and observation_blocked
        and not decision.get("runtime_admission_candidates")
        and not decision.get("commercial_runtime_candidates")
        and decision.get("fallback_required") is True
        and decision.get("health_gate_required") is True
        and decision.get("provider_replaceability_required") is True
        and decision.get("final_decision") == FINAL_DECISION_READY_FOR_DRYRUN_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Types / Registry / Validators",
        "import_ok": import_ok,
        "provider_policy_count": len(matrix.get("admission_policies") or []),
        "capability_profile_count": len(matrix.get("capability_profiles") or []),
        "health_gate_count": len(matrix.get("health_gates") or []),
        "fallback_policy_count": len(matrix.get("fallback_policies") or []),
        "runtime_admission_candidate_count": len(matrix.get("runtime_admission_candidates") or []),
        "disable_decision_count": len(matrix.get("disable_decisions") or []),
        "planning_decision_count": 1 if decision else 0,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "validator_rule_ids": list(VALIDATOR_RULE_IDS),
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "runtime_admission_candidates_empty": not decision.get("runtime_admission_candidates"),
        "commercial_runtime_candidates_empty": not decision.get("commercial_runtime_candidates"),
        "gpl_commercial_blocked": gpl_blocked,
        "observation_runtime_blocked": observation_blocked,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT == "field_synthesis_v1",
        "health_gate_required": decision.get("health_gate_required"),
        "fallback_required": decision.get("fallback_required"),
        "provider_replaceability_required": decision.get("provider_replaceability_required"),
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES
            if ready
            else "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_PLANNING_STEP1_BLOCKED"
        ),
    }


def main() -> int:
    summary = summarize_step1_baseline_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
