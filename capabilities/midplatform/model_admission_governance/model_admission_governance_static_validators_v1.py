# -*- coding: utf-8 -*-
"""Model Admission Governance Standard — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import PHASE_TEMPLATE_ID
from capabilities.midplatform.model_admission_governance.model_admission_governance_types_v1 import (
    ADMISSION_GOVERNANCE_PRINCIPLE_ZH,
    DRYRUN_LIFECYCLE_TEMPLATE_REF,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    FORBIDDEN_DOMAIN_OVERRIDES,
    MODEL_ADAPTER_CONTRACT_REF_FIELDS,
    MODEL_ADMISSION_PLANNING_DECISION_FIELDS,
    MODEL_ADMISSION_STANDARD_FIELDS,
    MODEL_CAPABILITY_PROFILE_FIELDS,
    MODEL_OPERATIONS,
    MODEL_PROVIDER_ADMISSION_REF_FIELDS,
    MODEL_REGISTRY_ENTRY_FIELDS,
    MODEL_RUNTIME_GOVERNANCE_REF_FIELDS,
    MODEL_SOURCE_LICENSE_GATE_FIELDS,
    PHASE_ID,
    SHARED_ADMISSION_LIFECYCLE_CHAIN,
    SHARED_RUNTIME_GOVERNANCE_REF,
)
from capabilities.midplatform.model_admission_governance.model_admission_governance_registry_v1 import (
    build_model_admission_governance_matrix_v1,
    is_registered,
    validate_registry,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_model_must_not_bypass_model_registry",
    "rule_02_model_must_not_bypass_license_source_gate",
    "rule_03_model_must_not_bypass_adapter_contract",
    "rule_04_model_must_not_bypass_provider_admission",
    "rule_05_model_must_not_bypass_runtime_governance",
    "rule_06_model_must_not_direct_action_speech_fact_write",
    "rule_07_candidate_only_default_true",
    "rule_08_runtime_enabled_default_false",
    "rule_09_commercial_runtime_approved_default_false",
    "rule_10_domain_specific_lifecycle_must_not_override_shared",
    "rule_11_update_replace_remove_requires_lineage",
    "rule_12_remove_must_use_deprecate_disable_remove_not_hard_delete",
    "rule_13_capability_change_requires_capability_profile",
    "rule_14_output_change_requires_output_candidate_contract",
    "rule_15_new_phase_must_reference_dryrun_lifecycle_template",
    "rule_16_registry_entry_required_fields_present",
    "rule_17_shared_lifecycle_chain_complete",
    "rule_18_model_type_registered",
    "rule_19_domain_profile_allowed_adapter_profile_only_delta",
    "rule_20_all_sample_models_share_same_admission_standard",
    "rule_21_license_gate_required_true",
    "rule_22_adapter_contract_required_true",
    "rule_23_provider_admission_required_true",
    "rule_24_runtime_governance_required_true",
    "rule_25_source_chain_required",
    "rule_26_planning_final_decision_ready_for_dryrun_cases",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{field_name}" for field_name in fields if field_name not in data]


def validate_candidate_only_default(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only_default") is not True and data.get("candidate_only") is not True:
        return False, ["candidate_only_default_required"]
    return True, []


def validate_runtime_enabled_default_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_enabled_default") is True:
        return False, ["runtime_enabled_default_must_be_false"]
    return True, []


def validate_commercial_runtime_approved_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("commercial_runtime_approved") is True:
        return False, ["commercial_runtime_approved_must_be_false"]
    return True, []


def validate_model_registry_entry(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_REGISTRY_ENTRY_FIELDS)
    for validator in (
        validate_candidate_only_default,
        validate_runtime_enabled_default_false,
        validate_commercial_runtime_approved_false,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    if not data.get("source_chain"):
        issues.append("source_chain_required")
    if not data.get("model_id"):
        issues.append("model_id_required")
    model_type = data.get("model_type")
    if model_type and not is_registered("model_types", str(model_type)):
        issues.append(f"model_type_not_registered:{model_type}")
    if not data.get("lineage_ref"):
        issues.append("lineage_ref_required")
    if not data.get("capability_profile_ref"):
        issues.append("capability_profile_ref_required")
    if not data.get("output_candidate_contract_ref"):
        issues.append("output_candidate_contract_ref_required")
    return len(issues) == 0, issues


def validate_capability_profile(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_CAPABILITY_PROFILE_FIELDS)
    ok, part = validate_candidate_only_default(data)
    if not ok:
        issues.extend(part)
    if not data.get("output_candidate_types"):
        issues.append("output_candidate_types_required")
    return len(issues) == 0, issues


def validate_license_gate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_SOURCE_LICENSE_GATE_FIELDS)
    for validator in (
        validate_candidate_only_default,
        validate_commercial_runtime_approved_false,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    if data.get("license_gate_required") is not True:
        issues.append("license_gate_required_must_be_true")
    return len(issues) == 0, issues


def validate_adapter_contract_ref(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_ADAPTER_CONTRACT_REF_FIELDS)
    ok, part = validate_candidate_only_default(data)
    if not ok:
        issues.extend(part)
    if data.get("adapter_contract_required") is not True:
        issues.append("adapter_contract_required_must_be_true")
    if data.get("bypass_forbidden") is not True:
        issues.append("adapter_contract_bypass_forbidden")
    return len(issues) == 0, issues


def validate_provider_admission_ref(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_PROVIDER_ADMISSION_REF_FIELDS)
    for validator in (
        validate_candidate_only_default,
        validate_runtime_enabled_default_false,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    if data.get("provider_admission_required") is not True:
        issues.append("provider_admission_required_must_be_true")
    if data.get("bypass_forbidden") is not True:
        issues.append("provider_admission_bypass_forbidden")
    return len(issues) == 0, issues


def validate_runtime_governance_ref(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_RUNTIME_GOVERNANCE_REF_FIELDS)
    for validator in (
        validate_candidate_only_default,
        validate_runtime_enabled_default_false,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    if data.get("runtime_governance_required") is not True:
        issues.append("runtime_governance_required_must_be_true")
    if data.get("shared_runtime_governance_ref") != SHARED_RUNTIME_GOVERNANCE_REF:
        issues.append(f"shared_runtime_governance_ref_must_be_{SHARED_RUNTIME_GOVERNANCE_REF}")
    if data.get("bypass_forbidden") is not True:
        issues.append("runtime_governance_bypass_forbidden")
    return len(issues) == 0, issues


def validate_admission_standard(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_ADMISSION_STANDARD_FIELDS)
    if data.get("domain_specific_lifecycle_forbidden") is not True:
        issues.append("domain_specific_lifecycle_forbidden_required")
    if data.get("lineage_required_for_update_replace_remove") is not True:
        issues.append("lineage_required_for_update_replace_remove")
    if data.get("dryrun_lifecycle_template_ref") != DRYRUN_LIFECYCLE_TEMPLATE_REF:
        issues.append("dryrun_lifecycle_template_ref_mismatch")
    if tuple(data.get("lifecycle_chain") or ()) != SHARED_ADMISSION_LIFECYCLE_CHAIN:
        issues.append("shared_lifecycle_chain_mismatch")
    if tuple(data.get("supported_operations") or ()) != MODEL_OPERATIONS:
        issues.append("supported_operations_mismatch")
    return len(issues) == 0, issues


def validate_planning_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MODEL_ADMISSION_PLANNING_DECISION_FIELDS)
    ok, part = validate_candidate_only_default(data)
    if not ok:
        issues.extend(part)
    for flag in (
        "shared_lifecycle_required",
        "domain_profile_allowed",
        "domain_specific_lifecycle_forbidden",
        "lineage_required_for_update_replace_remove",
        "dryrun_lifecycle_template_required",
    ):
        if data.get(flag) is not True:
            issues.append(f"{flag}_must_be_true")
    ok2, part2 = validate_runtime_enabled_default_false(data)
    if not ok2:
        issues.extend(part2)
    ok3, part3 = validate_commercial_runtime_approved_false(
        {
            "commercial_runtime_approved": data.get("commercial_runtime_approved_default"),
        }
    )
    if not ok3:
        issues.extend(part3)
    if data.get("dryrun_lifecycle_template_ref") != DRYRUN_LIFECYCLE_TEMPLATE_REF:
        issues.append("planning_dryrun_lifecycle_template_ref_mismatch")
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DRYRUN_CASES:
        issues.append("planning_final_decision_not_ready_for_dryrun_cases")
    return len(issues) == 0, issues


LINEAGE_REQUIRED_OPERATIONS: Tuple[str, ...] = (
    "update_model",
    "replace_model",
    "remove_model",
    "deprecate_model",
    "rollback_model",
)


def validate_model_admission_governance_case_bundle(
    bundle: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Minimal case-bundle validator for admission governance cases + runner."""
    issues: List[str] = []

    if bundle.get("registry_bypass") is True:
        issues.append("model_bypasses_registry")

    standard = bundle.get("model_admission_standard") or {}
    registry_entry = bundle.get("registry_entry") or {}
    license_gate = bundle.get("license_gate") or {}
    adapter_contract_ref = bundle.get("adapter_contract_ref") or {}
    provider_admission_ref = bundle.get("provider_admission_ref") or {}
    runtime_governance_ref = bundle.get("runtime_governance_ref") or {}
    model_operation = bundle.get("model_operation", "add_model")

    if standard.get("domain_specific_lifecycle_forbidden") is not True:
        issues.append("domain_specific_lifecycle_forbidden_required")

    if bundle.get("domain_specific_lifecycle_override") is True:
        issues.append("domain_specific_lifecycle_overrides_shared_lifecycle")

    lifecycle_variant = registry_entry.get("lifecycle_variant")
    if lifecycle_variant == "domain_specific_override":
        issues.append("domain_specific_lifecycle_variant_forbidden")

    if not bundle.get("registry_bypass"):
        ok, part = validate_model_registry_entry(registry_entry)
        if not ok:
            issues.extend(part)

    if bundle.get("license_gate_bypass") is True or license_gate.get("license_gate_required") is False:
        issues.append("model_bypasses_license_source_gate")
    else:
        ok, part = validate_license_gate(license_gate)
        if not ok:
            issues.extend(part)

    if not bundle.get("registry_bypass"):
        ok, part = validate_adapter_contract_ref(adapter_contract_ref)
        if not ok:
            issues.extend(part)
        ok, part = validate_provider_admission_ref(provider_admission_ref)
        if not ok:
            issues.extend(part)
        ok, part = validate_runtime_governance_ref(runtime_governance_ref)
        if not ok:
            issues.extend(part)

    profile = bundle.get("capability_profile") or {}
    if profile:
        ok, part = validate_capability_profile(profile)
        if not ok:
            issues.extend(part)

    if model_operation in LINEAGE_REQUIRED_OPERATIONS and not registry_entry.get("lineage_ref"):
        issues.append("lineage_missing_for_update_replace_remove")

    if registry_entry.get("runtime_enabled_default") is True:
        issues.append("runtime_enabled_default_must_be_false")
    if registry_entry.get("commercial_runtime_approved") is True:
        issues.append("commercial_runtime_approved_must_be_false")

    return len(issues) == 0, issues


def validate_model_admission_governance_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_model_admission_governance_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    ok, part = validate_admission_standard(matrix.get("model_admission_standard") or {})
    if not ok:
        issues.extend([f"model_admission_standard.{err}" for err in part])

    for entry in matrix.get("registry_entries") or ():
        ok, part = validate_model_registry_entry(entry)
        if not ok:
            issues.extend([f"registry_entry.{entry.get('model_id')}.{err}" for err in part])

    for profile in matrix.get("capability_profiles") or ():
        ok, part = validate_capability_profile(profile)
        if not ok:
            issues.extend([f"capability_profile.{profile.get('model_id')}.{err}" for err in part])

    for gate in matrix.get("license_gates") or ():
        ok, part = validate_license_gate(gate)
        if not ok:
            issues.extend([f"license_gate.{gate.get('model_id')}.{err}" for err in part])

    for ref in matrix.get("adapter_contract_refs") or ():
        ok, part = validate_adapter_contract_ref(ref)
        if not ok:
            issues.extend([f"adapter_contract_ref.{ref.get('model_id')}.{err}" for err in part])

    for ref in matrix.get("provider_admission_refs") or ():
        ok, part = validate_provider_admission_ref(ref)
        if not ok:
            issues.extend([f"provider_admission_ref.{ref.get('model_id')}.{err}" for err in part])

    for ref in matrix.get("runtime_governance_refs") or ():
        ok, part = validate_runtime_governance_ref(ref)
        if not ok:
            issues.extend([f"runtime_governance_ref.{ref.get('model_id')}.{err}" for err in part])

    ok, part = validate_planning_decision(matrix.get("planning_decision") or {})
    if not ok:
        issues.extend([f"planning_decision.{err}" for err in part])

    if matrix.get("dryrun_lifecycle_template_ref") != PHASE_TEMPLATE_ID:
        issues.append("matrix_dryrun_lifecycle_template_ref_mismatch")

    return len(issues) == 0 and registry_ok, issues


def summarize_model_admission_governance_planning_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.midplatform.model_admission_governance import (  # noqa: F401
            model_admission_governance_registry_v1,
            model_admission_governance_types_v1,
        )
        from capabilities.midplatform.core import dryrun_lifecycle_template_v1  # noqa: F401
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_model_admission_governance_matrix_v1()
    matrix_ok, matrix_issues = validate_model_admission_governance_matrix_v1(matrix)
    standard = matrix.get("model_admission_standard") or {}
    planning = matrix.get("planning_decision") or {}

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) >= 20
        and bool(standard)
        and len(matrix.get("registry_entries") or ()) >= 6
        and len(matrix.get("capability_profiles") or ()) >= 6
        and len(matrix.get("license_gates") or ()) >= 6
        and len(matrix.get("adapter_contract_refs") or ()) >= 6
        and len(matrix.get("provider_admission_refs") or ()) >= 6
        and len(matrix.get("runtime_governance_refs") or ()) >= 6
        and standard.get("domain_specific_lifecycle_forbidden") is True
        and planning.get("shared_lifecycle_required") is True
        and planning.get("domain_profile_allowed") is True
        and planning.get("candidate_only_default") is True
        and planning.get("runtime_enabled_default") is False
        and planning.get("commercial_runtime_approved_default") is False
        and planning.get("lineage_required_for_update_replace_remove") is True
        and planning.get("dryrun_lifecycle_template_required") is True
        and planning.get("dryrun_lifecycle_template_ref") == DRYRUN_LIFECYCLE_TEMPLATE_REF
        and planning.get("final_decision") == FINAL_DECISION_READY_FOR_DRYRUN_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Model Admission Governance Static Baseline",
        "admission_governance_principle_zh": ADMISSION_GOVERNANCE_PRINCIPLE_ZH,
        "import_ok": import_ok,
        "model_admission_standard_count": 1 if standard else 0,
        "registry_entry_count": len(matrix.get("registry_entries") or ()),
        "capability_profile_count": len(matrix.get("capability_profiles") or ()),
        "license_gate_count": len(matrix.get("license_gates") or ()),
        "adapter_contract_ref_count": len(matrix.get("adapter_contract_refs") or ()),
        "provider_admission_ref_count": len(matrix.get("provider_admission_refs") or ()),
        "runtime_governance_ref_count": len(matrix.get("runtime_governance_refs") or ()),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "shared_lifecycle_chain": matrix.get("shared_lifecycle_chain") or [],
        "shared_lifecycle_required": planning.get("shared_lifecycle_required"),
        "domain_profile_allowed": planning.get("domain_profile_allowed"),
        "domain_specific_lifecycle_forbidden": planning.get("domain_specific_lifecycle_forbidden"),
        "candidate_only_default": planning.get("candidate_only_default"),
        "runtime_enabled_default": planning.get("runtime_enabled_default"),
        "commercial_runtime_approved_default": planning.get("commercial_runtime_approved_default"),
        "lineage_required_for_update_replace_remove": planning.get(
            "lineage_required_for_update_replace_remove"
        ),
        "dryrun_lifecycle_template_required": planning.get("dryrun_lifecycle_template_required"),
        "dryrun_lifecycle_template_ref": planning.get("dryrun_lifecycle_template_ref"),
        "sample_model_ids": [entry.get("model_id") for entry in matrix.get("registry_entries") or ()],
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES
            if ready
            else "MODEL_ADMISSION_GOVERNANCE_STANDARD_PLANNING_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_model_admission_governance_planning_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
