# -*- coding: utf-8 -*-
"""Recognition Model P1 Invocation And Local Availability DryRun — cases v1.

Reads local controlled P1/P2 family availability-contract samples, admits each
contract through an availability-only check (NON-invasive probes only; NO real
inference / download / build / tuning / dataset), and runs the 8 positive family
checks (+ matrix generation) and the 10 negative cases. All probes are simulated
at the contract level only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_p1_invocation_and_local_availability_dryrun.recognition_model_p1_invocation_and_local_availability_dryrun_types_v1 import (
    ALLOWED_AVAILABILITY_STATUSES,
    ALLOWED_PROBE_MODES,
    MODEL_FAMILY_IDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    RecognitionModelCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

VALID_SAMPLE_FILES: Dict[str, str] = {
    "segmentation_family": "sample_segmentation_family_availability_contract.json",
    "tracking_family": "sample_tracking_family_availability_contract.json",
    "depth_spatial_hint_family": "sample_depth_spatial_hint_family_availability_contract.json",
    "object_detection_completion_family": "sample_object_detection_completion_family_availability_contract.json",
    "scene_relation_vlm_family": "sample_scene_relation_vlm_family_availability_contract.json",
    "audio_speech_family": "sample_audio_speech_family_reserved_contract.json",
    "emotion_multimodal_bridge_family": "sample_emotion_multimodal_bridge_reserved_contract.json",
}

MATRIX_SAMPLE_FILE = "sample_p1_p2_family_availability_matrix.json"

INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_missing_license_ref": "invalid_missing_license_ref_availability_contract.json",
    "invalid_missing_fallback_plan": "invalid_missing_fallback_plan_availability_contract.json",
    "invalid_missing_unavailable_record_policy": "invalid_missing_unavailable_record_policy.json",
    "invalid_real_inference_requested": "invalid_real_inference_requested.json",
    "invalid_new_model_download_requested": "invalid_model_download_requested.json",
    "invalid_single_model_debugging_requested": "invalid_single_model_debug_requested.json",
    "invalid_live_camera_sensor_requested": "invalid_live_camera_sensor_requested.json",
    "invalid_vla_action_chain_requested": "invalid_vla_action_chain_requested.json",
}

# Reserved-only families accept the reserved_only_contract probe mode.
RESERVED_FAMILIES: Tuple[str, ...] = (
    "audio_speech_family",
    "emotion_multimodal_bridge_family",
)


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
    # adapter_mapping_ref must remain an evidence-candidate target, never a direct
    # field-synthesis sink.
    target = str(contract.get("adapter_mapping_ref", ""))
    if target.endswith("_direct") or target == "field_synthesis_v1_direct":
        present.append("native_output_direct_to_field")
    return present


def admit_availability_contract(contract: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Availability-only admission. Returns (accepted, reject_reasons)."""
    reasons: List[str] = []

    for m in _missing_required_fields(contract):
        reasons.append(f"missing_required_field:{m}")

    probe_mode = contract.get("availability_probe_mode")
    if probe_mode not in ALLOWED_PROBE_MODES:
        reasons.append(f"invalid_availability_probe_mode:{probe_mode!r}")

    status = contract.get("availability_status")
    if status not in ALLOWED_AVAILABILITY_STATUSES:
        reasons.append(f"invalid_availability_status:{status!r}")

    for p in _prohibited_flags_present(contract):
        reasons.append(f"prohibited_request:{p}")

    return (len(reasons) == 0), reasons


def _run_positive_family_case(case_id: str, model_family: str) -> RecognitionModelCaseResult:
    contract = read_local_sample(VALID_SAMPLE_FILES[model_family])
    accepted, reasons = admit_availability_contract(contract)
    notes = [
        "availability_only",
        "non_invasive_probe",
        "no_real_inference",
        f"probe_mode={contract.get('availability_probe_mode')}",
        f"candidate_models={','.join(contract.get('candidate_models', []))}",
    ]
    if model_family in RESERVED_FAMILIES:
        notes.append("reserved_only_no_execution")
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=accepted is True,
        model_family=model_family,
        availability_status=str(contract.get("availability_status", "")),
        reject_reasons=tuple(reasons),
        notes=tuple(notes),
    )


def _run_matrix_generation_case() -> RecognitionModelCaseResult:
    matrix = read_local_sample(MATRIX_SAMPLE_FILE)
    families = matrix.get("families", [])
    covered = [str(e.get("model_family", "")) for e in families]
    statuses_ok = all(
        e.get("availability_status") in ALLOWED_AVAILABILITY_STATUSES for e in families
    )
    all_families_present = set(covered) == set(MODEL_FAMILY_IDS)
    count_ok = len(families) == 7
    ok = count_ok and all_families_present and statuses_ok
    return RecognitionModelCaseResult(
        case_id="p1_p2_family_availability_matrix_generation",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        model_family="all",
        availability_status="matrix",
        notes=(
            f"families_in_matrix={len(families)}",
            f"all_7_families_present={all_families_present}",
            f"all_statuses_allowed={statuses_ok}",
        ),
    )


def _run_negative_file_case(case_id: str, filename: str) -> RecognitionModelCaseResult:
    contract = read_local_sample(filename)
    accepted, reasons = admit_availability_contract(contract)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        model_family=str(contract.get("model_family", "")),
        availability_status=str(contract.get("availability_status", "")),
        reject_reasons=tuple(reasons),
    )


def _run_negative_tampered_case(
    case_id: str, base_family: str, injected_flags: Tuple[str, ...]
) -> RecognitionModelCaseResult:
    contract = dict(read_local_sample(VALID_SAMPLE_FILES[base_family]))
    for flag in injected_flags:
        contract[flag] = True
    accepted, reasons = admit_availability_contract(contract)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        model_family=base_family,
        availability_status=str(contract.get("availability_status", "")),
        reject_reasons=tuple(reasons),
        notes=("in_memory_tampered_contract", f"injected={','.join(injected_flags)}"),
    )


def run_positive_cases() -> List[RecognitionModelCaseResult]:
    return [
        _run_positive_family_case(
            "segmentation_family_local_availability_check", "segmentation_family"
        ),
        _run_positive_family_case(
            "tracking_family_local_availability_check", "tracking_family"
        ),
        _run_positive_family_case(
            "depth_spatial_hint_family_local_availability_check", "depth_spatial_hint_family"
        ),
        _run_positive_family_case(
            "object_detection_completion_family_local_availability_check",
            "object_detection_completion_family",
        ),
        _run_positive_family_case(
            "scene_relation_vlm_family_local_availability_check", "scene_relation_vlm_family"
        ),
        _run_positive_family_case(
            "audio_speech_reserved_family_check", "audio_speech_family"
        ),
        _run_positive_family_case(
            "emotion_multimodal_bridge_reserved_check", "emotion_multimodal_bridge_family"
        ),
        _run_matrix_generation_case(),
    ]


def run_negative_cases() -> List[RecognitionModelCaseResult]:
    return [
        _run_negative_file_case(
            "invalid_missing_license_ref",
            INVALID_SAMPLE_FILES["invalid_missing_license_ref"],
        ),
        _run_negative_file_case(
            "invalid_missing_fallback_plan",
            INVALID_SAMPLE_FILES["invalid_missing_fallback_plan"],
        ),
        _run_negative_file_case(
            "invalid_missing_unavailable_record_policy",
            INVALID_SAMPLE_FILES["invalid_missing_unavailable_record_policy"],
        ),
        _run_negative_file_case(
            "invalid_real_inference_requested",
            INVALID_SAMPLE_FILES["invalid_real_inference_requested"],
        ),
        _run_negative_file_case(
            "invalid_new_model_download_requested",
            INVALID_SAMPLE_FILES["invalid_new_model_download_requested"],
        ),
        _run_negative_file_case(
            "invalid_single_model_debugging_requested",
            INVALID_SAMPLE_FILES["invalid_single_model_debugging_requested"],
        ),
        _run_negative_tampered_case(
            "invalid_dataset_training_requested",
            "segmentation_family",
            ("dataset_usage_requested", "training_requested", "dataset_download_requested"),
        ),
        _run_negative_file_case(
            "invalid_live_camera_sensor_requested",
            INVALID_SAMPLE_FILES["invalid_live_camera_sensor_requested"],
        ),
        _run_negative_tampered_case(
            "invalid_direct_action_speech_fact_write_requested",
            "tracking_family",
            ("direct_action_requested", "direct_speech_requested", "direct_fact_write_requested"),
        ),
        _run_negative_file_case(
            "invalid_vla_action_chain_requested",
            INVALID_SAMPLE_FILES["invalid_vla_action_chain_requested"],
        ),
    ]
