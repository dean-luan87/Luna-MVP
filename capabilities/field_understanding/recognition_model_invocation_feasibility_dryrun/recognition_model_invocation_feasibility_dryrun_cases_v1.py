# -*- coding: utf-8 -*-
"""Recognition Model Invocation Feasibility DryRun — cases v1.

Reads local controlled callable-contract samples, admits each contract through a
feasibility-only check (NO real inference / download / build), and runs positive
and negative cases. Stub invocation, import/command availability and placeholder
output schema checks are simulated at the contract level only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_invocation_feasibility_dryrun.recognition_model_invocation_feasibility_dryrun_types_v1 import (
    ALLOWED_INVOCATION_MODES,
    MODEL_FAMILY_IDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_CONTRACT_FIELDS,
    RecognitionModelCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

VALID_SAMPLE_FILES: Dict[str, str] = {
    "ocr_model_family": "sample_ocr_callable_contract.json",
    "object_detection_model_family": "sample_object_detection_callable_contract.json",
    "segmentation_model_family": "sample_segmentation_callable_contract.json",
    "tracking_model_family": "sample_tracking_callable_contract.json",
    "depth_spatial_hint_model_family": "sample_depth_spatial_hint_callable_contract.json",
    "visual_symbol_model_family": "sample_visual_symbol_callable_contract.json",
    "scene_relation_model_family": "sample_scene_relation_callable_contract.json",
}

INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_missing_model_origin": "invalid_missing_model_origin_contract.json",
    "invalid_missing_license_ref": "invalid_missing_license_ref_contract.json",
    "invalid_missing_output_schema_ref": "invalid_missing_output_schema_contract.json",
    "invalid_real_inference_requested": "invalid_real_inference_requested_contract.json",
    "invalid_model_download_requested": "invalid_model_download_requested_contract.json",
    "invalid_native_output_direct_to_field": "invalid_native_output_direct_to_field_contract.json",
}


def read_local_sample(filename: str) -> Dict[str, Any]:
    path = _SAMPLES_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_required_fields(contract: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = contract.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            missing.append(f)
    return missing


def _prohibited_flags_present(contract: Dict[str, Any]) -> List[str]:
    present: List[str] = []
    for flag in PROHIBITED_REQUEST_FLAGS:
        if contract.get(flag) is True:
            present.append(flag)
    # adapter_mapping_target must not be a direct field-synthesis target.
    target = str(contract.get("adapter_mapping_target", ""))
    if target.endswith("_direct") or target == "field_synthesis_v1_direct":
        present.append("native_output_direct_to_field")
    return present


def admit_callable_contract(contract: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Feasibility-only admission. Returns (accepted, reject_reasons)."""
    reasons: List[str] = []

    missing = _missing_required_fields(contract)
    for m in missing:
        reasons.append(f"missing_required_field:{m}")

    invocation_mode = contract.get("invocation_mode")
    if invocation_mode not in ALLOWED_INVOCATION_MODES:
        reasons.append(f"invalid_invocation_mode:{invocation_mode!r}")

    prohibited = _prohibited_flags_present(contract)
    for p in prohibited:
        reasons.append(f"prohibited_request:{p}")

    return (len(reasons) == 0), reasons


def _run_positive_family_case(case_id: str, model_family: str) -> RecognitionModelCaseResult:
    contract = read_local_sample(VALID_SAMPLE_FILES[model_family])
    accepted, reasons = admit_callable_contract(contract)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=accepted is True,
        model_family=model_family,
        reject_reasons=tuple(reasons),
        notes=("feasibility_only", "no_real_inference", f"invocation_mode={contract.get('invocation_mode')}"),
    )


def _run_multi_family_matrix_case() -> RecognitionModelCaseResult:
    families_covered: List[str] = []
    adapter_targets_declared = True
    all_accepted = True
    for fam in MODEL_FAMILY_IDS:
        contract = read_local_sample(VALID_SAMPLE_FILES[fam])
        accepted, _ = admit_callable_contract(contract)
        all_accepted = all_accepted and accepted
        families_covered.append(fam)
        if not str(contract.get("adapter_mapping_target", "")).strip():
            adapter_targets_declared = False
    ok = all_accepted and len(families_covered) == 7 and adapter_targets_declared
    return RecognitionModelCaseResult(
        case_id="multi_family_invocation_feasibility_matrix",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        model_family="all",
        notes=(
            f"families_covered={len(families_covered)}",
            f"adapter_mapping_target_declared_for_all={adapter_targets_declared}",
        ),
    )


def _run_negative_file_case(case_id: str, filename: str) -> RecognitionModelCaseResult:
    contract = read_local_sample(filename)
    accepted, reasons = admit_callable_contract(contract)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        model_family=str(contract.get("model_family", "")),
        reject_reasons=tuple(reasons),
    )


def _run_negative_tampered_case(
    case_id: str, base_family: str, injected_flags: Tuple[str, ...]
) -> RecognitionModelCaseResult:
    contract = dict(read_local_sample(VALID_SAMPLE_FILES[base_family]))
    for flag in injected_flags:
        contract[flag] = True
    accepted, reasons = admit_callable_contract(contract)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        model_family=base_family,
        reject_reasons=tuple(reasons),
        notes=("in_memory_tampered_contract", f"injected={','.join(injected_flags)}"),
    )


def run_positive_cases() -> List[RecognitionModelCaseResult]:
    results: List[RecognitionModelCaseResult] = [
        _run_positive_family_case("ocr_invocation_feasibility_contract_check", "ocr_model_family"),
        _run_positive_family_case(
            "object_detection_invocation_feasibility_contract_check",
            "object_detection_model_family",
        ),
        _run_positive_family_case(
            "segmentation_invocation_feasibility_contract_check", "segmentation_model_family"
        ),
        _run_positive_family_case(
            "tracking_invocation_feasibility_contract_check", "tracking_model_family"
        ),
        _run_positive_family_case(
            "depth_spatial_hint_invocation_feasibility_contract_check",
            "depth_spatial_hint_model_family",
        ),
        _run_positive_family_case(
            "visual_symbol_invocation_feasibility_contract_check", "visual_symbol_model_family"
        ),
        _run_positive_family_case(
            "scene_relation_invocation_feasibility_contract_check", "scene_relation_model_family"
        ),
        _run_multi_family_matrix_case(),
    ]
    return results


def run_negative_cases() -> List[RecognitionModelCaseResult]:
    results: List[RecognitionModelCaseResult] = [
        _run_negative_file_case(
            "invalid_missing_model_origin", INVALID_SAMPLE_FILES["invalid_missing_model_origin"]
        ),
        _run_negative_file_case(
            "invalid_missing_license_ref", INVALID_SAMPLE_FILES["invalid_missing_license_ref"]
        ),
        _run_negative_file_case(
            "invalid_missing_output_schema_ref",
            INVALID_SAMPLE_FILES["invalid_missing_output_schema_ref"],
        ),
        _run_negative_file_case(
            "invalid_real_inference_requested",
            INVALID_SAMPLE_FILES["invalid_real_inference_requested"],
        ),
        _run_negative_file_case(
            "invalid_model_download_requested",
            INVALID_SAMPLE_FILES["invalid_model_download_requested"],
        ),
        _run_negative_file_case(
            "invalid_native_output_direct_to_field",
            INVALID_SAMPLE_FILES["invalid_native_output_direct_to_field"],
        ),
        _run_negative_tampered_case(
            "invalid_dataset_usage_or_training_requested",
            "ocr_model_family",
            ("dataset_usage_requested", "training_requested"),
        ),
        _run_negative_tampered_case(
            "invalid_runtime_activation_or_live_sensor_requested",
            "object_detection_model_family",
            ("runtime_activation_requested", "live_camera_requested", "live_sensor_requested"),
        ),
    ]
    return results
