# -*- coding: utf-8 -*-
"""Recognition Model Multi-Model Interaction DryRun — cases v1.

Reads mock file-based multi-model candidate bundles, admits each interaction
bundle, maps it into Luna cross-model interaction evidence candidates, and runs
9 positive interaction cases and 12 negative cases. No real inference is
performed; all interaction outputs are candidate-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_multi_model_interaction_dryrun.recognition_model_multi_model_interaction_dryrun_types_v1 import (
    ALL_CANDIDATE_TYPES,
    INTERACTION_BOUNDARY,
    INTERACTION_CASE_IDS,
    INTERACTION_IDS,
    INTERACTION_TO_CANDIDATES,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    RESERVED_INTERACTIONS,
    RecognitionModelCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

VALID_SAMPLE_FILES: Dict[str, str] = {
    "object_segmentation_alignment": "sample_object_segmentation_alignment_bundle.json",
    "object_tracking_temporal": "sample_object_tracking_temporal_bundle.json",
    "tracking_depth_dynamic_risk": "sample_tracking_depth_dynamic_risk_bundle.json",
    "ocr_segmentation_text_region": "sample_ocr_segmentation_text_region_bundle.json",
    "visual_symbol_scene_context": "sample_visual_symbol_scene_context_bundle.json",
    "scene_relation_object_region": "sample_scene_relation_object_region_bundle.json",
    "audio_emotion_reserved_bridge": "sample_audio_emotion_reserved_bridge_bundle.json",
    "conflict_uncertainty_propagation": "sample_conflict_uncertainty_bundle.json",
    "full_multi_model_interaction_bundle": "sample_multi_model_full_interaction_bundle.json",
}

# negative case_id -> sample file (11 file-based; missing_candidate_refs is tampered).
INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_missing_source_chain": "invalid_missing_source_chain_interaction.json",
    "invalid_cross_model_fact_write": "invalid_cross_model_fact_write.json",
    "invalid_segmentation_route_activation_from_alignment": "invalid_segmentation_route_activation_from_alignment.json",
    "invalid_tracking_depth_direct_action": "invalid_tracking_depth_direct_action.json",
    "invalid_visual_symbol_direct_navigation_from_context": "invalid_visual_symbol_direct_navigation_from_context.json",
    "invalid_scene_relation_final_interpretation": "invalid_scene_relation_final_interpretation.json",
    "invalid_audio_identity_without_consent": "invalid_audio_identity_without_consent.json",
    "invalid_emotion_bridge_psychological_fact_write": "invalid_emotion_bridge_psychological_fact_write.json",
    "invalid_conflict_resolved_as_fact_without_admission": "invalid_conflict_resolved_as_fact_without_admission.json",
    "invalid_vla_action_chain_injected": "invalid_vla_action_chain_injected.json",
    "invalid_guidance_runtime_navigation_from_interaction": "invalid_guidance_runtime_navigation_from_interaction.json",
}

ALL_SAMPLE_FILES: Tuple[str, ...] = (
    tuple(VALID_SAMPLE_FILES.values()) + tuple(INVALID_SAMPLE_FILES.values())
)


def read_local_sample(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


def _missing_required_fields(bundle: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = bundle.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, (list, tuple)) and len(v) == 0):
            missing.append(f)
    return missing


def _prohibited_flags_present(bundle: Dict[str, Any]) -> List[str]:
    present: List[str] = []
    for flag in PROHIBITED_REQUEST_FLAGS:
        if bundle.get(flag) is True:
            present.append(flag)
    return present


def admit_interaction_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(bundle):
        reasons.append(f"missing_required_field:{m}")
    for p in _prohibited_flags_present(bundle):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def map_interaction_to_candidates(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    interaction_id = bundle.get("interaction_id", "")
    candidate_types = INTERACTION_TO_CANDIDATES.get(interaction_id, ())
    boundary = INTERACTION_BOUNDARY.get(interaction_id, "candidate_only")
    reserved_only = interaction_id in RESERVED_INTERACTIONS or bundle.get("reserved_only") is True
    return [
        {
            "candidate_type": c,
            "source_interaction_id": interaction_id,
            "boundary": boundary,
            "candidate_only": True,
            "reserved_only": reserved_only,
        }
        for c in candidate_types
    ]


def _run_positive_interaction_case(interaction_id: str) -> RecognitionModelCaseResult:
    case_id = INTERACTION_CASE_IDS[interaction_id]
    bundle = read_local_sample(VALID_SAMPLE_FILES[interaction_id])
    accepted, reasons = admit_interaction_bundle(bundle)
    candidates: List[str] = []
    if accepted:
        candidates = [c["candidate_type"] for c in map_interaction_to_candidates(bundle)]
    expected = list(INTERACTION_TO_CANDIDATES.get(interaction_id, ()))
    ok = accepted and candidates == expected
    notes = [INTERACTION_BOUNDARY.get(interaction_id, ""), "candidate_only", "no_real_inference"]
    if interaction_id in RESERVED_INTERACTIONS:
        notes.append("reserved_only_no_execution")
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=ok,
        interaction_id=interaction_id,
        generated_candidates=tuple(candidates),
        reject_reasons=tuple(reasons),
        notes=tuple(notes),
    )


def _run_negative_file_case(case_id: str, filename: str) -> RecognitionModelCaseResult:
    bundle = read_local_sample(filename)
    accepted, reasons = admit_interaction_bundle(bundle)
    return RecognitionModelCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        interaction_id=str(bundle.get("interaction_id", "")),
        reject_reasons=tuple(reasons),
    )


def _run_negative_missing_candidate_refs_case() -> RecognitionModelCaseResult:
    bundle = dict(read_local_sample(VALID_SAMPLE_FILES["object_segmentation_alignment"]))
    bundle.pop("candidate_refs", None)
    accepted, reasons = admit_interaction_bundle(bundle)
    return RecognitionModelCaseResult(
        case_id="invalid_missing_candidate_refs",
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        interaction_id=str(bundle.get("interaction_id", "")),
        reject_reasons=tuple(reasons),
        notes=("in_memory_tampered_bundle", "removed=candidate_refs"),
    )


def run_positive_cases() -> Tuple[List[RecognitionModelCaseResult], List[str]]:
    results: List[RecognitionModelCaseResult] = [
        _run_positive_interaction_case(iid) for iid in INTERACTION_IDS
    ]
    covered: List[str] = []
    for r in results:
        if r.passed:
            covered.extend(r.generated_candidates)
    return results, sorted(set(covered))


def run_negative_cases() -> List[RecognitionModelCaseResult]:
    results: List[RecognitionModelCaseResult] = [
        _run_negative_file_case("invalid_missing_source_chain", INVALID_SAMPLE_FILES["invalid_missing_source_chain"]),
        _run_negative_missing_candidate_refs_case(),
        _run_negative_file_case("invalid_cross_model_fact_write", INVALID_SAMPLE_FILES["invalid_cross_model_fact_write"]),
        _run_negative_file_case(
            "invalid_segmentation_route_activation_from_alignment",
            INVALID_SAMPLE_FILES["invalid_segmentation_route_activation_from_alignment"],
        ),
        _run_negative_file_case(
            "invalid_tracking_depth_direct_action",
            INVALID_SAMPLE_FILES["invalid_tracking_depth_direct_action"],
        ),
        _run_negative_file_case(
            "invalid_visual_symbol_direct_navigation_from_context",
            INVALID_SAMPLE_FILES["invalid_visual_symbol_direct_navigation_from_context"],
        ),
        _run_negative_file_case(
            "invalid_scene_relation_final_interpretation",
            INVALID_SAMPLE_FILES["invalid_scene_relation_final_interpretation"],
        ),
        _run_negative_file_case(
            "invalid_audio_identity_without_consent",
            INVALID_SAMPLE_FILES["invalid_audio_identity_without_consent"],
        ),
        _run_negative_file_case(
            "invalid_emotion_bridge_psychological_fact_write",
            INVALID_SAMPLE_FILES["invalid_emotion_bridge_psychological_fact_write"],
        ),
        _run_negative_file_case(
            "invalid_conflict_resolved_as_fact_without_admission",
            INVALID_SAMPLE_FILES["invalid_conflict_resolved_as_fact_without_admission"],
        ),
        _run_negative_file_case(
            "invalid_vla_action_chain_injected",
            INVALID_SAMPLE_FILES["invalid_vla_action_chain_injected"],
        ),
        _run_negative_file_case(
            "invalid_guidance_runtime_navigation_from_interaction",
            INVALID_SAMPLE_FILES["invalid_guidance_runtime_navigation_from_interaction"],
        ),
    ]
    return results
