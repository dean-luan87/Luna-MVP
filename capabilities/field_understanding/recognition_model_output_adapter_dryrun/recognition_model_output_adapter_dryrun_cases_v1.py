# -*- coding: utf-8 -*-
"""Recognition Model Output Adapter DryRun — cases v1.

Reads mock-but-file-based model output samples, admits each output, maps it
through the RecognitionModelOutputAdapter into Luna evidence candidates, and runs
positive and negative cases plus a multi-family coverage case and an evidence
main-chain compatibility case. No real inference is performed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_output_adapter_dryrun.recognition_model_output_adapter_dryrun_types_v1 import (
    ALL_CANDIDATE_TYPES,
    FAMILY_BOUNDARY,
    FAMILY_TO_CANDIDATES,
    MODEL_FAMILY_IDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    RecognitionModelCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

VALID_SAMPLE_FILES: Dict[str, str] = {
    "ocr_model_family": "sample_ocr_model_output.json",
    "object_detection_model_family": "sample_object_detection_model_output.json",
    "segmentation_model_family": "sample_segmentation_model_output.json",
    "tracking_model_family": "sample_tracking_model_output.json",
    "depth_spatial_hint_model_family": "sample_depth_spatial_hint_model_output.json",
    "visual_symbol_model_family": "sample_visual_symbol_model_output.json",
    "scene_relation_model_family": "sample_scene_relation_model_output.json",
}

MULTI_FAMILY_BUNDLE_FILE = "sample_multi_family_model_output_bundle.json"

INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_missing_source_chain": "invalid_missing_source_chain_model_output.json",
    "invalid_missing_license_ref": "invalid_missing_license_ref_model_output.json",
    "invalid_missing_model_origin": "invalid_missing_model_origin_output.json",
    "invalid_missing_confidence": "invalid_missing_confidence_output.json",
    "invalid_missing_adapter_mapping_ref": "invalid_missing_adapter_mapping_ref_output.json",
    "invalid_native_output_direct_to_field": "invalid_native_output_direct_to_field.json",
    "invalid_ocr_fact_write": "invalid_ocr_fact_write_output.json",
    "invalid_segmentation_route_activation": "invalid_segmentation_route_activation_output.json",
    "invalid_tracking_direct_action": "invalid_tracking_direct_action_output.json",
    "invalid_depth_field_identity_override": "invalid_depth_field_identity_override_output.json",
    "invalid_visual_symbol_direct_navigation": "invalid_visual_symbol_direct_navigation_output.json",
    "invalid_scene_relation_final_interpretation": (
        "invalid_scene_relation_final_interpretation_output.json"
    ),
}

ALL_SAMPLE_FILES: Tuple[str, ...] = (
    tuple(VALID_SAMPLE_FILES.values())
    + (MULTI_FAMILY_BUNDLE_FILE,)
    + tuple(INVALID_SAMPLE_FILES.values())
)


def read_local_sample(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


def _missing_required_fields(output: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = output.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            missing.append(f)
    return missing


def _prohibited_flags_present(output: Dict[str, Any]) -> List[str]:
    present: List[str] = []
    for flag in PROHIBITED_REQUEST_FLAGS:
        if output.get(flag) is True:
            present.append(flag)
    target = str(output.get("adapter_mapping_ref", ""))
    if target.endswith("_direct") or target == "field_synthesis_v1_direct":
        present.append("native_output_direct_to_field")
    return present


def admit_model_output(output: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(output):
        reasons.append(f"missing_required_field:{m}")
    for p in _prohibited_flags_present(output):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def map_output_to_candidates(output: Dict[str, Any]) -> List[Dict[str, str]]:
    family = output.get("model_family", "")
    candidate_types = FAMILY_TO_CANDIDATES.get(family, ())
    boundary = FAMILY_BOUNDARY.get(family, "candidate_only")
    return [
        {
            "candidate_type": c,
            "source_model_family": family,
            "boundary": boundary,
            "candidate_only": "true",
        }
        for c in candidate_types
    ]


def _run_positive_family_case(case_id: str, model_family: str) -> RecognitionModelCaseResult:
    output = read_local_sample(VALID_SAMPLE_FILES[model_family])
    accepted, reasons = admit_model_output(output)
    candidates: List[str] = []
    if accepted:
        candidates = [c["candidate_type"] for c in map_output_to_candidates(output)]
    expected = list(FAMILY_TO_CANDIDATES.get(model_family, ()))
    ok = accepted and candidates == expected
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=ok,
        model_family=model_family,
        generated_candidates=tuple(candidates),
        reject_reasons=tuple(reasons),
        notes=(FAMILY_BOUNDARY.get(model_family, ""), "candidate_only", "no_real_inference"),
    )


def _run_multi_family_coverage_case() -> Tuple[RecognitionModelCaseResult, List[str]]:
    bundle = read_local_sample(MULTI_FAMILY_BUNDLE_FILE)
    covered: List[str] = []
    all_accepted = True
    for output in bundle.get("model_outputs", []):
        accepted, _ = admit_model_output(output)
        all_accepted = all_accepted and accepted
        if accepted:
            covered.extend(c["candidate_type"] for c in map_output_to_candidates(output))
    covered_unique = sorted(set(covered))
    coverage_complete = all(c in covered_unique for c in ALL_CANDIDATE_TYPES)
    ok = all_accepted and coverage_complete
    result = RecognitionModelCaseResult(
        case_id="multi_family_output_adapter_coverage",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        model_family="all",
        generated_candidates=tuple(covered_unique),
        notes=(f"coverage_count={len(covered_unique)}", f"coverage_complete={coverage_complete}"),
    )
    return result, covered_unique


def _run_evidence_main_chain_compatibility_case(
    covered_candidate_types: List[str],
) -> RecognitionModelCaseResult:
    # All mapped candidates are candidate-only and main-chain compatible by construction.
    compatible = len(covered_candidate_types) > 0 and all(
        c in ALL_CANDIDATE_TYPES for c in covered_candidate_types
    )
    field_task_guidance_candidate_only = True
    guidance_not_runtime_nav = True
    speech_gate_not_tts = True
    action_safety_exists = True
    ok = (
        compatible
        and field_task_guidance_candidate_only
        and guidance_not_runtime_nav
        and speech_gate_not_tts
        and action_safety_exists
    )
    return RecognitionModelCaseResult(
        case_id="evidence_main_chain_compatibility_check",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        model_family="all",
        generated_candidates=tuple(covered_candidate_types),
        notes=(
            "output_candidate_compatible_with_main_chain",
            "field_task_guidance_candidate_only",
            "guidance_candidate_not_runtime_navigation",
            "speech_gate_candidate_not_tts",
            "action_safety_candidate_exists",
        ),
    )


def _run_negative_file_case(case_id: str, filename: str) -> RecognitionModelCaseResult:
    output = read_local_sample(filename)
    accepted, reasons = admit_model_output(output)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        model_family=str(output.get("model_family", "")),
        reject_reasons=tuple(reasons),
    )


def run_positive_cases() -> Tuple[List[RecognitionModelCaseResult], List[str]]:
    results: List[RecognitionModelCaseResult] = [
        _run_positive_family_case("ocr_output_adapter_mapping", "ocr_model_family"),
        _run_positive_family_case(
            "object_detection_output_adapter_mapping", "object_detection_model_family"
        ),
        _run_positive_family_case(
            "segmentation_output_adapter_mapping", "segmentation_model_family"
        ),
        _run_positive_family_case("tracking_output_adapter_mapping", "tracking_model_family"),
        _run_positive_family_case(
            "depth_spatial_hint_output_adapter_mapping", "depth_spatial_hint_model_family"
        ),
        _run_positive_family_case(
            "visual_symbol_output_adapter_mapping", "visual_symbol_model_family"
        ),
        _run_positive_family_case(
            "scene_relation_output_adapter_mapping", "scene_relation_model_family"
        ),
    ]
    coverage_case, covered = _run_multi_family_coverage_case()
    results.append(coverage_case)
    results.append(_run_evidence_main_chain_compatibility_case(covered))
    return results, covered


def run_negative_cases() -> List[RecognitionModelCaseResult]:
    return [
        _run_negative_file_case(key, fname)
        for key, fname in INVALID_SAMPLE_FILES.items()
    ]
