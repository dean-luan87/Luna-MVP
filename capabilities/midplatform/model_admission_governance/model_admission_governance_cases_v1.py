# -*- coding: utf-8 -*-
"""Model Admission Governance Standard — cases v1 (compressed)."""

from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_admission_governance.model_admission_governance_registry_v1 import (
    SAMPLE_MODEL_IDS,
    build_model_admission_governance_matrix_v1,
)
from capabilities.midplatform.model_admission_governance.model_admission_governance_static_validators_v1 import (
    validate_model_admission_governance_case_bundle,
)
from capabilities.midplatform.model_admission_governance.model_admission_governance_types_v1 import (
    ADMISSION_GOVERNANCE_PRINCIPLE_ZH,
    FINAL_DECISION_CASES_READY_FOR_RUNNER,
    PHASE_ID,
)

POSITIVE_CASE_SPECS: Tuple[Tuple[str, str, str, str, str], ...] = (
    (
        "case_pos_01_sample_slam_spatial_evidence_model",
        "sample_slam_spatial_evidence_model",
        "slam",
        "spatial_evidence",
        "slam_spatial_evidence_adapter",
    ),
    (
        "case_pos_02_sample_supervision_detection_model",
        "sample_supervision_detection_model",
        "vision",
        "vision",
        "supervision_detection_adapter",
    ),
    (
        "case_pos_03_sample_viewpoint_search_model",
        "sample_viewpoint_search_model",
        "search",
        "vision",
        "viewpoint_search_adapter",
    ),
    (
        "case_pos_04_sample_ocr_text_evidence_model",
        "sample_ocr_text_evidence_model",
        "ocr",
        "vision_ocr",
        "ocr_text_evidence_adapter",
    ),
    (
        "case_pos_05_sample_asr_speech_evidence_model",
        "sample_asr_speech_evidence_model",
        "asr",
        "asr",
        "asr_speech_evidence_adapter",
    ),
    (
        "case_pos_06_sample_world_model_prediction_model",
        "sample_world_model_prediction_model",
        "world_model",
        "shared",
        "world_model_prediction_adapter",
    ),
)


@dataclass(frozen=True)
class ModelAdmissionGovernanceCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    model_id: str
    model_family: str
    domain_id: str
    adapter_profile_ref: str
    model_operation: str
    model_admission_standard: Dict[str, Any]
    registry_entry: Dict[str, Any]
    capability_profile: Dict[str, Any]
    license_gate: Dict[str, Any]
    adapter_contract_ref: Dict[str, Any]
    provider_admission_ref: Dict[str, Any]
    runtime_governance_ref: Dict[str, Any]
    registry_bypass: bool = False
    license_gate_bypass: bool = False
    domain_specific_lifecycle_override: bool = False
    expected_validation_ok: bool = True


def _matrix() -> Dict[str, Any]:
    return build_model_admission_governance_matrix_v1()


def _by_model_id(items: List[Dict[str, Any]], model_id: str) -> Dict[str, Any]:
    for item in items:
        if item.get("model_id") == model_id:
            return copy.deepcopy(item)
    raise KeyError(f"model_id_not_found:{model_id}")


def _bundle_parts_for_model(model_id: str) -> Dict[str, Dict[str, Any]]:
    matrix = _matrix()
    return {
        "model_admission_standard": copy.deepcopy(matrix["model_admission_standard"]),
        "registry_entry": _by_model_id(matrix.get("registry_entries") or [], model_id),
        "capability_profile": _by_model_id(matrix.get("capability_profiles") or [], model_id),
        "license_gate": _by_model_id(matrix.get("license_gates") or [], model_id),
        "adapter_contract_ref": _by_model_id(matrix.get("adapter_contract_refs") or [], model_id),
        "provider_admission_ref": _by_model_id(matrix.get("provider_admission_refs") or [], model_id),
        "runtime_governance_ref": _by_model_id(matrix.get("runtime_governance_refs") or [], model_id),
    }


def _positive_case(
    *,
    case_id: str,
    model_id: str,
    model_family: str,
    domain_id: str,
    adapter_profile_ref: str,
) -> ModelAdmissionGovernanceCase:
    parts = _bundle_parts_for_model(model_id)
    profile = parts["capability_profile"]
    return ModelAdmissionGovernanceCase(
        case_id=case_id,
        case_name=f"{model_id} shared admission flow",
        case_type="positive",
        case_goal=(
            f"Validate {model_id} follows shared model admission governance "
            f"for {model_family}/{domain_id} via {adapter_profile_ref}."
        ),
        model_id=model_id,
        model_family=model_family,
        domain_id=domain_id,
        adapter_profile_ref=adapter_profile_ref,
        model_operation="add_model",
        model_admission_standard=parts["model_admission_standard"],
        registry_entry=parts["registry_entry"],
        capability_profile=profile,
        license_gate=parts["license_gate"],
        adapter_contract_ref=parts["adapter_contract_ref"],
        provider_admission_ref=parts["provider_admission_ref"],
        runtime_governance_ref=parts["runtime_governance_ref"],
    )


def build_positive_model_admission_governance_cases_v1() -> Tuple[ModelAdmissionGovernanceCase, ...]:
    return tuple(
        _positive_case(
            case_id=case_id,
            model_id=model_id,
            model_family=model_family,
            domain_id=domain_id,
            adapter_profile_ref=adapter_profile_ref,
        )
        for case_id, model_id, model_family, domain_id, adapter_profile_ref in POSITIVE_CASE_SPECS
    )


def _invalid_from_base(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    mutate,
) -> ModelAdmissionGovernanceCase:
    base = _positive_case(
        case_id=case_id,
        model_id="sample_slam_spatial_evidence_model",
        model_family="slam",
        domain_id="spatial_evidence",
        adapter_profile_ref="slam_spatial_evidence_adapter",
    )
    parts = {
        "model_admission_standard": copy.deepcopy(base.model_admission_standard),
        "registry_entry": copy.deepcopy(base.registry_entry),
        "capability_profile": copy.deepcopy(base.capability_profile),
        "license_gate": copy.deepcopy(base.license_gate),
        "adapter_contract_ref": copy.deepcopy(base.adapter_contract_ref),
        "provider_admission_ref": copy.deepcopy(base.provider_admission_ref),
        "runtime_governance_ref": copy.deepcopy(base.runtime_governance_ref),
        "model_operation": base.model_operation,
        "registry_bypass": base.registry_bypass,
        "license_gate_bypass": base.license_gate_bypass,
        "domain_specific_lifecycle_override": base.domain_specific_lifecycle_override,
    }
    mutated = mutate(parts)
    return ModelAdmissionGovernanceCase(
        case_id=case_id,
        case_name=case_name,
        case_type="invalid",
        case_goal=case_goal,
        model_id=base.model_id,
        model_family=base.model_family,
        domain_id=base.domain_id,
        adapter_profile_ref=base.adapter_profile_ref,
        model_operation=mutated.get("model_operation", base.model_operation),
        model_admission_standard=mutated["model_admission_standard"],
        registry_entry=mutated["registry_entry"],
        capability_profile=mutated["capability_profile"],
        license_gate=mutated["license_gate"],
        adapter_contract_ref=mutated["adapter_contract_ref"],
        provider_admission_ref=mutated["provider_admission_ref"],
        runtime_governance_ref=mutated["runtime_governance_ref"],
        registry_bypass=mutated.get("registry_bypass", False),
        license_gate_bypass=mutated.get("license_gate_bypass", False),
        domain_specific_lifecycle_override=mutated.get("domain_specific_lifecycle_override", False),
        expected_validation_ok=False,
    )


def build_invalid_model_admission_governance_cases_v1() -> Tuple[ModelAdmissionGovernanceCase, ...]:
    def mutate_registry_bypass(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["registry_bypass"] = True
        parts["registry_entry"] = {}
        return parts

    def mutate_license_bypass(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["license_gate_bypass"] = True
        parts["license_gate"]["license_gate_required"] = False
        return parts

    def mutate_domain_lifecycle_override(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["domain_specific_lifecycle_override"] = True
        parts["registry_entry"]["lifecycle_variant"] = "domain_specific_override"
        return parts

    def mutate_missing_lineage(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["model_operation"] = "replace_model"
        parts["registry_entry"]["lineage_ref"] = ""
        return parts

    return (
        _invalid_from_base(
            case_id="invalid_a_model_bypasses_registry",
            case_name="model bypasses registry",
            case_goal="Reject model admission when registry is bypassed.",
            mutate=mutate_registry_bypass,
        ),
        _invalid_from_base(
            case_id="invalid_b_model_bypasses_license_gate",
            case_name="model bypasses license/source gate",
            case_goal="Reject model admission when license/source gate is bypassed.",
            mutate=mutate_license_bypass,
        ),
        _invalid_from_base(
            case_id="invalid_c_domain_specific_lifecycle_override",
            case_name="domain-specific lifecycle overrides shared lifecycle",
            case_goal="Reject when domain-specific lifecycle overrides shared admission flow.",
            mutate=mutate_domain_lifecycle_override,
        ),
        _invalid_from_base(
            case_id="invalid_d_update_replace_remove_missing_lineage",
            case_name="update/replace/remove missing lineage",
            case_goal="Reject update/replace/remove when lineage_ref is missing.",
            mutate=mutate_missing_lineage,
        ),
    )


def build_all_model_admission_governance_cases_v1() -> Tuple[ModelAdmissionGovernanceCase, ...]:
    return (
        build_positive_model_admission_governance_cases_v1()
        + build_invalid_model_admission_governance_cases_v1()
    )


def bundle_from_model_admission_governance_case(
    case: ModelAdmissionGovernanceCase,
) -> Dict[str, Any]:
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "model_id": case.model_id,
        "model_family": case.model_family,
        "domain_id": case.domain_id,
        "adapter_profile_ref": case.adapter_profile_ref,
        "model_operation": case.model_operation,
        "model_admission_standard": case.model_admission_standard,
        "registry_entry": case.registry_entry,
        "capability_profile": case.capability_profile,
        "license_gate": case.license_gate,
        "adapter_contract_ref": case.adapter_contract_ref,
        "provider_admission_ref": case.provider_admission_ref,
        "runtime_governance_ref": case.runtime_governance_ref,
        "registry_bypass": case.registry_bypass,
        "license_gate_bypass": case.license_gate_bypass,
        "domain_specific_lifecycle_override": case.domain_specific_lifecycle_override,
    }


def _validate_case(case: ModelAdmissionGovernanceCase) -> Tuple[bool, List[str]]:
    return validate_model_admission_governance_case_bundle(
        bundle_from_model_admission_governance_case(case)
    )


def _check_cases(
    cases: Tuple[ModelAdmissionGovernanceCase, ...],
    *,
    expect_valid: bool,
) -> Tuple[int, List[str]]:
    ok_count = 0
    mismatches: List[str] = []
    for case in cases:
        valid, issues = _validate_case(case)
        if valid == expect_valid:
            ok_count += 1
        else:
            mismatches.append(
                f"{case.case_id}:expected_valid={expect_valid}:actual_valid={valid}:issues={issues}"
            )
    return ok_count, mismatches


def summarize_model_admission_governance_cases_v1() -> Dict[str, Any]:
    positive = build_positive_model_admission_governance_cases_v1()
    invalid = build_invalid_model_admission_governance_cases_v1()
    all_cases = build_all_model_admission_governance_cases_v1()

    case_ids = [case.case_id for case in all_cases]
    unique_ok = len(case_ids) == len(set(case_ids))
    pos_ok, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, inv_mismatches = _check_cases(invalid, expect_valid=False)

    sample_positive_ok = False
    sample_invalid_rejected = False
    if positive:
        sample_positive_ok, _ = _validate_case(positive[0])
    if invalid:
        invalid_ok, _ = _validate_case(invalid[0])
        sample_invalid_rejected = not invalid_ok

    standard = _matrix().get("model_admission_standard") or {}
    planning = _matrix().get("planning_decision") or {}

    ready = (
        len(positive) == 6
        and len(invalid) == 4
        and len(all_cases) == 10
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and sample_positive_ok
        and sample_invalid_rejected
        and standard.get("domain_specific_lifecycle_forbidden") is True
        and planning.get("shared_lifecycle_required") is True
        and planning.get("lineage_required_for_update_replace_remove") is True
        and planning.get("runtime_enabled_default") is False
        and planning.get("commercial_runtime_approved_default") is False
        and set(SAMPLE_MODEL_IDS) == {case.model_id for case in positive}
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Model Admission Governance Cases",
        "admission_governance_principle_zh": ADMISSION_GOVERNANCE_PRINCIPLE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": [case.case_id for case in positive],
        "invalid_case_ids": [case.case_id for case in invalid],
        "case_ids_unique": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "shared_lifecycle_required": planning.get("shared_lifecycle_required"),
        "domain_specific_lifecycle_forbidden": standard.get("domain_specific_lifecycle_forbidden"),
        "lineage_required_for_update_replace_remove": planning.get(
            "lineage_required_for_update_replace_remove"
        ),
        "runtime_enabled_default": planning.get("runtime_enabled_default"),
        "commercial_runtime_approved_default": planning.get("commercial_runtime_approved_default"),
        "sample_model_ids": list(SAMPLE_MODEL_IDS),
        "final_decision": (
            FINAL_DECISION_CASES_READY_FOR_RUNNER
            if ready
            else "MODEL_ADMISSION_GOVERNANCE_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_model_admission_governance_cases_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_CASES_READY_FOR_RUNNER else 1


if __name__ == "__main__":
    raise SystemExit(main())
