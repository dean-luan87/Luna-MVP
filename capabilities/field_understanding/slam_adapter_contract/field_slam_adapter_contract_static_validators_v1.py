# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_registry_v1 import (
    BLOCKED_RUNTIME_BACKEND_REFS,
    FORBIDDEN_ADAPTER_POLICIES,
    GPL_LICENSE_TYPES,
    OBSERVATION_BACKEND_REFS,
    build_adapter_planning_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_types_v1 import (
    ADAPTER_PLANNING_DECISION_FIELDS,
    BACKEND_ADMISSION_CANDIDATE_FIELDS,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    GENERIC_SLAM_ADAPTER_CONTRACT_FIELDS,
    LICENSE_GATE_POLICY_FIELDS,
    PHASE_ID,
    RUNTIME_ISOLATION_POLICY_FIELDS,
    SLAM_BACKEND_OUTPUT_MAPPING_FIELDS,
    SPATIAL_EVIDENCE_PROVIDER_REGISTRATION_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_adapter_contract_candidate_only_required",
    "rule_02_backend_role_registered",
    "rule_03_supported_output_candidates_registered",
    "rule_04_required_outputs_subset_of_supported",
    "rule_05_field_synthesis_entrypoint_required",
    "rule_06_adapter_license_gate_ref_required",
    "rule_07_adapter_runtime_isolation_ref_required",
    "rule_08_gpl_backend_not_commercial_runtime_allowed",
    "rule_09_gpl_backend_blocks_commercial_usage_modes",
    "rule_10_output_mapping_candidate_only_enforced",
    "rule_11_output_mapping_source_refs_required",
    "rule_12_runtime_admission_requires_all_gates_passed",
    "rule_13_commercial_runtime_requires_license_gate_passed",
    "rule_14_observation_backend_no_runtime_admission",
    "rule_15_provider_supported_candidate_types_required",
    "rule_16_health_signal_requires_slam_health_candidate",
    "rule_17_forbidden_adapter_policies_absent",
    "rule_18_final_decision_ready_for_dryrun_cases",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _policy_text_fields(data: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for key in ("notes", "blocked_usage_modes", "required_actions", "blocked_reasons"):
        val = data.get(key)
        if isinstance(val, str):
            texts.append(val)
        elif isinstance(val, (list, tuple)):
            texts.extend(str(v) for v in val)
    for key in ("confidence_policy", "degradation_policy", "disable_policy"):
        val = data.get(key)
        if val:
            texts.append(str(val))
    return texts


def validate_adapter_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if data.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_generic_slam_adapter_contract(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, GENERIC_SLAM_ADAPTER_CONTRACT_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)

    ok2, i2 = validate_backend_role_registered(data)
    ok3, i3 = validate_supported_output_candidates_registered(data)
    ok4, i4 = validate_required_outputs_subset_of_supported(data)
    ok5, i5 = validate_field_synthesis_entrypoint_required(data)
    ok6, i6 = validate_adapter_license_gate_ref_required(data)
    ok7, i7 = validate_adapter_runtime_isolation_ref_required(data)
    ok17, i17 = validate_forbidden_adapter_policies_absent(data)

    for ok_part, part_issues in ((ok2, i2), (ok3, i3), (ok4, i4), (ok5, i5), (ok6, i6), (ok7, i7), (ok17, i17)):
        if not ok_part:
            issues.extend(part_issues)

    if data.get("adapter_status") and not is_registered("adapter_statuses", data["adapter_status"]):
        issues.append("adapter_status_not_registered")
    for mode in data.get("supported_input_modes") or ():
        if not is_registered("input_modes", mode):
            issues.append(f"supported_input_mode_not_registered:{mode}")

    return len(issues) == 0, issues


def validate_slam_backend_output_mapping(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_BACKEND_OUTPUT_MAPPING_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)

    ok10, i10 = validate_output_mapping_candidate_only_enforced(data)
    ok11, i11 = validate_output_mapping_source_refs_required(data)
    ok17, i17 = validate_forbidden_adapter_policies_absent(data)
    if not ok10:
        issues.extend(i10)
    if not ok11:
        issues.extend(i11)
    if not ok17:
        issues.extend(i17)

    candidate_type = data.get("luna_candidate_type")
    if candidate_type and not is_registered("output_candidate_types", candidate_type):
        issues.append("luna_candidate_type_not_registered")
    if data.get("mapping_status") and not is_registered("mapping_statuses", data["mapping_status"]):
        issues.append("mapping_status_not_registered")
    if data.get("confidence_policy") and not is_registered("confidence_policies", data["confidence_policy"]):
        issues.append("confidence_policy_not_registered")
    if data.get("degradation_policy") and not is_registered("degradation_policies", data["degradation_policy"]):
        issues.append("degradation_policy_not_registered")

    return len(issues) == 0, issues


def validate_license_gate_policy(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, LICENSE_GATE_POLICY_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)

    ok8, i8 = validate_gpl_backend_not_commercial_runtime_allowed(data)
    ok9, i9 = validate_gpl_backend_blocks_commercial_usage_modes(data)
    ok17, i17 = validate_forbidden_adapter_policies_absent(data)
    if not ok8:
        issues.extend(i8)
    if not ok9:
        issues.extend(i9)
    if not ok17:
        issues.extend(i17)

    if data.get("license_type") and not is_registered("license_types", data["license_type"]):
        issues.append("license_type_not_registered")
    if data.get("license_risk") and not is_registered("license_risks", data["license_risk"]):
        issues.append("license_risk_not_registered")
    if data.get("review_status") and not is_registered("license_review_statuses", data["review_status"]):
        issues.append("review_status_not_registered")

    return len(issues) == 0, issues


def validate_runtime_isolation_policy(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, RUNTIME_ISOLATION_POLICY_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)
    ok17, i17 = validate_forbidden_adapter_policies_absent(data)
    if not ok17:
        issues.extend(i17)

    if data.get("isolation_mode") and not is_registered("isolation_modes", data["isolation_mode"]):
        issues.append("isolation_mode_not_registered")
    if data.get("data_exchange_mode") and not is_registered("data_exchange_modes", data["data_exchange_mode"]):
        issues.append("data_exchange_mode_not_registered")
    if data.get("source_code_contamination_risk") and not is_registered(
        "contamination_risks", data["source_code_contamination_risk"]
    ):
        issues.append("source_code_contamination_risk_not_registered")
    if data.get("runtime_dependency_risk") and not is_registered(
        "contamination_risks", data["runtime_dependency_risk"]
    ):
        issues.append("runtime_dependency_risk_not_registered")

    backend_ref = data.get("backend_ref")
    if backend_ref in GPL_LICENSE_TYPES or backend_ref in BLOCKED_RUNTIME_BACKEND_REFS:
        pass
    if backend_ref in {"openvins", "vins_fusion", "orb_slam3"} and data.get("allowed_for_commercial_runtime") is True:
        issues.append("gpl_backend_isolation_commercial_runtime_not_allowed")

    return len(issues) == 0, issues


def validate_backend_admission_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, BACKEND_ADMISSION_CANDIDATE_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)

    ok12, i12 = validate_runtime_admission_requires_all_gates_passed(data)
    ok13, i13 = validate_commercial_runtime_requires_license_gate_passed(data)
    ok14, i14 = validate_observation_backend_no_runtime_admission(data)
    ok17, i17 = validate_forbidden_adapter_policies_absent(data)
    if not ok12:
        issues.extend(i12)
    if not ok13:
        issues.extend(i13)
    if not ok14:
        issues.extend(i14)
    if not ok17:
        issues.extend(i17)

    if data.get("admission_stage") and not is_registered("admission_stages", data["admission_stage"]):
        issues.append("admission_stage_not_registered")

    return len(issues) == 0, issues


def validate_spatial_evidence_provider_registration(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SPATIAL_EVIDENCE_PROVIDER_REGISTRATION_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)

    ok15, i15 = validate_provider_supported_candidate_types_required(data)
    ok16, i16 = validate_health_signal_requires_slam_health_candidate(data)
    ok17, i17 = validate_forbidden_adapter_policies_absent(data)
    if not ok15:
        issues.extend(i15)
    if not ok16:
        issues.extend(i16)
    if not ok17:
        issues.extend(i17)

    if data.get("provider_role") and not is_registered("provider_roles", data["provider_role"]):
        issues.append("provider_role_not_registered")
    if data.get("disable_policy") and not is_registered("disable_policies", data["disable_policy"]):
        issues.append("disable_policy_not_registered")
    for ctype in data.get("supported_candidate_types") or ():
        if not is_registered("output_candidate_types", ctype):
            issues.append(f"supported_candidate_type_not_registered:{ctype}")

    return len(issues) == 0, issues


def validate_adapter_planning_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, ADAPTER_PLANNING_DECISION_FIELDS)
    ok1, i1 = validate_adapter_candidate_only(data)
    issues.extend(i1)
    ok18, i18 = validate_final_decision_ready_for_dryrun_cases(data)
    if not ok18:
        issues.extend(i18)

    if not data.get("license_gate_required"):
        issues.append("license_gate_required_must_be_true")
    if not data.get("runtime_isolation_required"):
        issues.append("runtime_isolation_required_must_be_true")
    if not data.get("output_mapping_required"):
        issues.append("output_mapping_required_must_be_true")
    if not data.get("dryrun_required_next"):
        issues.append("dryrun_required_next_must_be_true")
    if data.get("commercial_runtime_backends"):
        for backend in data["commercial_runtime_backends"]:
            if backend in BLOCKED_RUNTIME_BACKEND_REFS:
                issues.append(f"blocked_backend_in_commercial_runtime:{backend}")

    return len(issues) == 0, issues


def validate_backend_role_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    role = data.get("backend_role")
    if not role:
        return False, ["backend_role_required"]
    if not is_registered("backend_roles", role):
        return False, ["backend_role_not_registered"]
    return True, []


def validate_supported_output_candidates_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    outputs = data.get("supported_output_candidates") or ()
    if not outputs:
        return False, ["supported_output_candidates_required"]
    issues: List[str] = []
    for out in outputs:
        if not is_registered("output_candidate_types", out):
            issues.append(f"supported_output_candidate_not_registered:{out}")
    return len(issues) == 0, issues


def validate_required_outputs_subset_of_supported(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    supported = set(data.get("supported_output_candidates") or ())
    required = data.get("required_output_candidates") or ()
    if not required:
        return False, ["required_output_candidates_required"]
    issues = [f"required_output_not_supported:{r}" for r in required if r not in supported]
    return len(issues) == 0, issues


def validate_field_synthesis_entrypoint_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    entry = data.get("field_synthesis_entrypoint")
    if not entry:
        return False, ["field_synthesis_entrypoint_required"]
    if entry != FIELD_SYNTHESIS_ENTRYPOINT:
        return False, [f"field_synthesis_entrypoint_must_be_{FIELD_SYNTHESIS_ENTRYPOINT}"]
    return True, []


def validate_adapter_license_gate_ref_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not data.get("license_gate_ref"):
        return False, ["license_gate_ref_required"]
    return True, []


def validate_adapter_runtime_isolation_ref_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not data.get("runtime_isolation_ref"):
        return False, ["runtime_isolation_ref_required"]
    return True, []


def validate_gpl_backend_not_commercial_runtime_allowed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("license_type") in GPL_LICENSE_TYPES and data.get("commercial_runtime_allowed") is True:
        return False, ["gpl_backend_commercial_runtime_not_allowed"]
    return True, []


def validate_gpl_backend_blocks_commercial_usage_modes(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("license_type") not in GPL_LICENSE_TYPES:
        return True, []
    blocked = set(data.get("blocked_usage_modes") or ())
    required = {"closed_source_embedded_runtime", "commercial_distribution"}
    missing = required - blocked
    if missing:
        return False, [f"gpl_blocked_usage_modes_missing:{sorted(missing)}"]
    return True, []


def validate_output_mapping_candidate_only_enforced(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only_enforced") is not True:
        return False, ["candidate_only_enforced_required"]
    return True, []


def validate_output_mapping_source_refs_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("source_refs_required") is not True:
        return False, ["source_refs_required_must_be_true"]
    return True, []


def validate_runtime_admission_requires_all_gates_passed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_admission_allowed") is not True:
        return True, []
    issues: List[str] = []
    for gate in (
        "license_gate_passed",
        "adapter_contract_passed",
        "output_mapping_passed",
        "static_validation_passed",
    ):
        if data.get(gate) is not True:
            issues.append(f"runtime_admission_requires_{gate}")
    return len(issues) == 0, issues


def validate_commercial_runtime_requires_license_gate_passed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("admission_stage") != "commercial_runtime_candidate":
        return True, []
    if data.get("license_gate_passed") is not True:
        return False, ["commercial_runtime_requires_license_gate_passed"]
    return True, []


def validate_observation_backend_no_runtime_admission(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    backend = data.get("backend_ref")
    if backend not in OBSERVATION_BACKEND_REFS:
        return True, []
    if data.get("runtime_admission_allowed") is True:
        return False, ["observation_backend_runtime_admission_not_allowed"]
    return True, []


def validate_provider_supported_candidate_types_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not (data.get("supported_candidate_types") or ()):
        return False, ["supported_candidate_types_required"]
    return True, []


def validate_health_signal_requires_slam_health_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("health_signal_required") is not True:
        return True, []
    supported = set(data.get("supported_candidate_types") or ())
    if "SLAMHealthCandidate" not in supported:
        return False, ["health_signal_requires_slam_health_candidate"]
    return True, []


def validate_forbidden_adapter_policies_absent(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for text in _policy_text_fields(data):
        for policy in FORBIDDEN_ADAPTER_POLICIES:
            if policy == text or policy in text:
                issues.append(f"forbidden_adapter_policy_present:{policy}")
    return len(issues) == 0, issues


def validate_final_decision_ready_for_dryrun_cases(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DRYRUN_CASES:
        return False, [f"final_decision_must_be_{FINAL_DECISION_READY_FOR_DRYRUN_CASES}"]
    return True, []


def validate_adapter_contract_case_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a single dry-run case bundle (shared by cases and runner)."""
    return _validate_adapter_contract_bundle_core(
        bundle,
        validate_decision=False,
        enforce_full_counts=False,
    )


def _validate_adapter_contract_bundle_core(
    bundle: Dict[str, Any],
    *,
    validate_decision: bool,
    enforce_full_counts: bool,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    if not registry_ok:
        issues.extend(registry_issues)

    adapters = bundle.get("adapter_contracts") or []
    mappings = bundle.get("output_mappings") or []
    license_gates = bundle.get("license_gates") or []
    isolations = bundle.get("runtime_isolations") or []
    admissions = bundle.get("backend_admissions") or []
    providers = bundle.get("provider_registrations") or []
    decision = bundle.get("decision") or {}

    adapter_refs = {a.get("adapter_ref") for a in adapters}
    backend_refs = {a.get("backend_ref") for a in adapters}

    for idx, item in enumerate(adapters):
        ok, item_issues = validate_generic_slam_adapter_contract(item)
        if not ok:
            issues.extend([f"adapter_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(mappings):
        ok, item_issues = validate_slam_backend_output_mapping(item)
        if not ok:
            issues.extend([f"mapping_{idx}:{i}" for i in item_issues])
        if item.get("adapter_ref") not in adapter_refs:
            issues.append(f"mapping_{idx}:adapter_ref_not_in_adapters")

    for idx, item in enumerate(license_gates):
        ok, item_issues = validate_license_gate_policy(item)
        if not ok:
            issues.extend([f"license_gate_{idx}:{i}" for i in item_issues])
        if item.get("backend_ref") not in backend_refs:
            issues.append(f"license_gate_{idx}:backend_ref_not_in_adapters")

    for idx, item in enumerate(isolations):
        ok, item_issues = validate_runtime_isolation_policy(item)
        if not ok:
            issues.extend([f"isolation_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(admissions):
        ok, item_issues = validate_backend_admission_candidate(item)
        if not ok:
            issues.extend([f"admission_{idx}:{i}" for i in item_issues])

    for idx, item in enumerate(providers):
        ok, item_issues = validate_spatial_evidence_provider_registration(item)
        if not ok:
            issues.extend([f"provider_{idx}:{i}" for i in item_issues])

    if validate_decision:
        ok_dec, dec_issues = validate_adapter_planning_decision(decision)
        if not ok_dec:
            issues.extend([f"decision:{i}" for i in dec_issues])

    for idx, adapter in enumerate(adapters):
        lg_ref = adapter.get("license_gate_ref")
        iso_ref = adapter.get("runtime_isolation_ref")
        if not any(l.get("license_gate_ref") == lg_ref for l in license_gates):
            issues.append(f"adapter_{idx}:license_gate_ref_not_found:{lg_ref}")
        if not any(i.get("isolation_ref") == iso_ref for i in isolations):
            issues.append(f"adapter_{idx}:runtime_isolation_ref_not_found:{iso_ref}")

    if enforce_full_counts:
        expected_counts = {
            "adapter_contracts": 7,
            "license_gates": 7,
            "runtime_isolations": 7,
            "backend_admissions": 7,
            "provider_registrations": 7,
        }
        for key, expected in expected_counts.items():
            actual = len(bundle.get(key) or [])
            if actual != expected:
                issues.append(f"{key}_count_expected_{expected}_actual_{actual}")

        if len(mappings) < 7:
            issues.append(f"output_mapping_count_below_minimum_7_actual_{len(mappings)}")

    return len(issues) == 0, issues


def validate_adapter_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_adapter_planning_matrix_v1()
    return _validate_adapter_contract_bundle_core(
        matrix,
        validate_decision=True,
        enforce_full_counts=True,
    )


def _gpl_runtime_blocked(matrix: Dict[str, Any]) -> bool:
    for gate in matrix.get("license_gates") or []:
        if gate.get("license_type") in GPL_LICENSE_TYPES and gate.get("commercial_runtime_allowed") is True:
            return False
    for admission in matrix.get("backend_admissions") or []:
        if admission.get("backend_ref") in GPL_LICENSE_TYPES:
            continue
        if admission.get("backend_ref") in {"openvins", "vins_fusion", "orb_slam3"}:
            if admission.get("runtime_admission_allowed") is True:
                return False
    return True


def _observation_runtime_blocked(matrix: Dict[str, Any]) -> bool:
    for admission in matrix.get("backend_admissions") or []:
        if admission.get("backend_ref") in OBSERVATION_BACKEND_REFS:
            if admission.get("runtime_admission_allowed") is True:
                return False
    return True


def _candidate_only_enforced(matrix: Dict[str, Any]) -> bool:
    buckets = (
        "adapter_contracts",
        "output_mappings",
        "license_gates",
        "runtime_isolations",
        "backend_admissions",
        "provider_registrations",
    )
    for bucket in buckets:
        for item in matrix.get(bucket) or []:
            if item.get("candidate_only") is not True:
                return False
    decision = matrix.get("decision") or {}
    if decision and decision.get("candidate_only") is not True:
        return False
    for mapping in matrix.get("output_mappings") or []:
        if mapping.get("candidate_only_enforced") is not True:
            return False
    return True


def summarize_step1_baseline_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.field_understanding.slam_adapter_contract import (  # noqa: F401
            field_slam_adapter_contract_registry_v1,
            field_slam_adapter_contract_types_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_adapter_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_adapter_planning_matrix_v1(matrix)
    decision = matrix.get("decision") or {}

    gpl_runtime_blocked = _gpl_runtime_blocked(matrix)
    observation_runtime_blocked = _observation_runtime_blocked(matrix)
    candidate_only_enforced = _candidate_only_enforced(matrix)

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) == 18
        and gpl_runtime_blocked
        and observation_runtime_blocked
        and candidate_only_enforced
        and decision.get("license_gate_required") is True
        and decision.get("runtime_isolation_required") is True
        and decision.get("final_decision") == FINAL_DECISION_READY_FOR_DRYRUN_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Types / Registry / Validators",
        "import_ok": import_ok,
        "adapter_contract_count": len(matrix.get("adapter_contracts") or []),
        "output_mapping_count": len(matrix.get("output_mappings") or []),
        "license_gate_count": len(matrix.get("license_gates") or []),
        "runtime_isolation_count": len(matrix.get("runtime_isolations") or []),
        "backend_admission_count": len(matrix.get("backend_admissions") or []),
        "provider_registration_count": len(matrix.get("provider_registrations") or []),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "validator_rule_ids": list(VALIDATOR_RULE_IDS),
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "gpl_runtime_blocked": gpl_runtime_blocked,
        "observation_runtime_blocked": observation_runtime_blocked,
        "candidate_only_enforced": candidate_only_enforced,
        "commercial_runtime_backends": list(decision.get("commercial_runtime_backends") or ()),
        "technical_reference_backends": list(decision.get("technical_reference_backends") or ()),
        "blocked_runtime_backends": list(decision.get("blocked_runtime_backends") or ()),
        "observation_backends": list(decision.get("observation_backends") or ()),
        "license_gate_required": decision.get("license_gate_required"),
        "runtime_isolation_required": decision.get("runtime_isolation_required"),
        "output_mapping_required": decision.get("output_mapping_required"),
        "dryrun_required_next": decision.get("dryrun_required_next"),
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES
            if ready
            else "FIELD_SLAM_ADAPTER_CONTRACT_PLANNING_STEP1_BLOCKED"
        ),
    }


def main() -> int:
    summary = summarize_step1_baseline_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
