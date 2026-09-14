# -*- coding: utf-8 -*-
"""Recognition Model P1 Output Adapter DryRun — cases v1.

Reads mock-but-file-based P1/P2 model output samples, admits each output,
maps it through the RecognitionModelOutputAdapter into Luna evidence candidates,
and runs 8 positive and 12 negative cases. No real inference is performed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_p1_output_adapter_dryrun.recognition_model_p1_output_adapter_dryrun_types_v1 import (
    ALL_CANDIDATE_TYPES,
    FAMILY_BOUNDARY,
    FAMILY_TO_CANDIDATES,
    MODEL_FAMILY_IDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    RESERVED_FAMILIES,
    RecognitionModelCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

VALID_SAMPLE_FILES: Dict[str, str] = {
    "segmentation_family": "sample_segmentation_model_output.json",
    "tracking_family": "sample_tracking_model_output.json",
    "depth_spatial_hint_family": "sample_depth_spatial_hint_model_output.json",
    "object_detection_completion_family": "sample_object_detection_completion_output.json",
    "scene_relation_vlm_family": "sample_scene_relation_vlm_structured_output.json",
    "audio_speech_family": "sample_audio_speech_reserved_output_contract.json",
    "emotion_multimodal_bridge_family": "sample_emotion_multimodal_bridge_reserved_output_contract.json",
}

MULTI_FAMILY_BUNDLE_FILE = "sample_p1_p2_multi_family_output_bundle.json"

INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_missing_source_chain": "invalid_missing_source_chain_output.json",
    "invalid_missing_license_ref": "invalid_missing_license_ref_output.json",
    "invalid_missing_model_origin": "invalid_missing_model_origin_output.json",
    "invalid_missing_confidence": "invalid_missing_confidence_output.json",
    "invalid_missing_adapter_mapping_ref": "invalid_missing_adapter_mapping_ref_output.json",
    "invalid_segmentation_route_activation": "invalid_segmentation_route_activation_output.json",
    "invalid_tracking_action_trigger": "invalid_tracking_action_trigger_output.json",
    "invalid_depth_navigation_activation": "invalid_depth_navigation_activation_output.json",
    "invalid_scene_relation_final_interpretation": "invalid_scene_relation_final_interpretation_output.json",
    "invalid_audio_identity_without_consent": "invalid_audio_identity_without_consent_output.json",
    "invalid_emotion_psychological_fact_write": "invalid_emotion_psychological_fact_write_output.json",
    "invalid_vla_action_chain": "invalid_vla_action_chain_output.json",
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


def map_output_to_candidates(output: Dict[str, Any]) -> List[Dict[str, Any]]:
    family = output.get("model_family", "")
    candidate_types = FAMILY_TO_CANDIDATES.get(family, ())
    boundary = FAMILY_BOUNDARY.get(family, "candidate_only")
    reserved_only = family in RESERVED_FAMILIES or output.get("reserved_only") is True
    return [
        {
            "candidate_type": c,
            "source_model_family": family,
            "boundary": boundary,
            "candidate_only": True,
            "reserved_only": reserved_only,
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
    notes = [FAMILY_BOUNDARY.get(model_family, ""), "candidate_only", "no_real_inference"]
    if model_family in RESERVED_FAMILIES:
        notes.append("reserved_only_no_execution")
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=ok,
        model_family=model_family,
        generated_candidates=tuple(candidates),
        reject_reasons=tuple(reasons),
        notes=tuple(notes),
    )


def _run_multi_family_bundle_case() -> Tuple[RecognitionModelCaseResult, List[str]]:
    bundle = read_local_sample(MULTI_FAMILY_BUNDLE_FILE)
    covered: List[str] = []
    all_accepted = True
    families_in_bundle: List[str] = []
    reserved_preserved = True
    for output in bundle.get("model_outputs", []):
        fam = str(output.get("model_family", ""))
        families_in_bundle.append(fam)
        accepted, _ = admit_model_output(output)
        all_accepted = all_accepted and accepted
        if accepted:
            covered.extend(c["candidate_type"] for c in map_output_to_candidates(output))
        if fam in RESERVED_FAMILIES and not output.get("reserved_only"):
            reserved_preserved = False
    covered_unique = sorted(set(covered))
    coverage_complete = all(c in covered_unique for c in ALL_CANDIDATE_TYPES)
    families_complete = set(families_in_bundle) == set(MODEL_FAMILY_IDS)
    ok = all_accepted and coverage_complete and families_complete and reserved_preserved
    result = RecognitionModelCaseResult(
        case_id="p1_p2_multi_family_output_bundle_mapping",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        model_family="all",
        generated_candidates=tuple(covered_unique),
        notes=(
            f"coverage_count={len(covered_unique)}",
            f"coverage_complete={coverage_complete}",
            f"families_complete={families_complete}",
            f"reserved_families_preserved={reserved_preserved}",
            "all_outputs_candidate_only",
        ),
    )
    return result, covered_unique


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
        _run_positive_family_case(
            "segmentation_output_adapter_mapping", "segmentation_family"
        ),
        _run_positive_family_case("tracking_output_adapter_mapping", "tracking_family"),
        _run_positive_family_case(
            "depth_spatial_hint_output_adapter_mapping", "depth_spatial_hint_family"
        ),
        _run_positive_family_case(
            "object_detection_completion_output_adapter_mapping",
            "object_detection_completion_family",
        ),
        _run_positive_family_case(
            "scene_relation_vlm_structured_output_adapter_mapping",
            "scene_relation_vlm_family",
        ),
        _run_positive_family_case(
            "audio_speech_reserved_output_contract_mapping", "audio_speech_family"
        ),
        _run_positive_family_case(
            "emotion_multimodal_bridge_reserved_output_contract_mapping",
            "emotion_multimodal_bridge_family",
        ),
    ]
    bundle_case, covered = _run_multi_family_bundle_case()
    results.append(bundle_case)
    return results, covered


def run_negative_cases() -> List[RecognitionModelCaseResult]:
    return [
        _run_negative_file_case(case_id, INVALID_SAMPLE_FILES[case_id])
        for case_id in INVALID_SAMPLE_FILES
    ]
