# -*- coding: utf-8 -*-
"""Recognition Model Evidence Main Chain Integration DryRun — cases v1.

Reuses sealed real-model output candidates and drives them through the Phase-One
evidence main chain ingress along the Field / Task / Guidance candidate path.
Everything stays candidate-only. No re-inference, no download, no action/speech/
navigation/fact_write, no VLA action chain.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_evidence_main_chain_integration_dryrun.recognition_model_evidence_main_chain_integration_dryrun_types_v1 import (
    AVAILABILITY_RECORD_KIND,
    PROHIBITED_REQUEST_FLAGS,
    MainChainIntegrationCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

OCR_CANDIDATE_FILE = "sample_real_ocr_text_evidence_candidate.json"
VISUAL_SYMBOL_CANDIDATES_FILE = "sample_real_visual_symbol_candidates.json"
YOLO_UNAVAILABLE_FILE = "sample_yolo_declared_unavailable_record.json"
BUNDLE_FILE = "sample_real_p0_candidate_bundle.json"

INVALID_FILES: Dict[str, str] = {
    "invalid_candidate_missing_source_chain": "invalid_candidate_missing_source_chain.json",
    "invalid_candidate_missing_confidence": "invalid_candidate_missing_confidence.json",
    "invalid_candidate_direct_fact_write": "invalid_candidate_direct_fact_write.json",
    "invalid_visual_symbol_direct_navigation": "invalid_visual_symbol_direct_navigation.json",
    "invalid_guidance_candidate_runtime_navigation": "invalid_guidance_candidate_runtime_navigation.json",
    "invalid_speech_gate_tts_activation": "invalid_speech_gate_tts_activation.json",
    "invalid_action_trigger_from_candidate": "invalid_action_trigger_from_candidate.json",
    "invalid_yolo_unavailable_treated_as_blocker": "invalid_yolo_unavailable_treated_as_blocker.json",
    "invalid_vla_action_chain_injected": "invalid_vla_action_chain_injected.json",
}

VALID_SAMPLE_FILES: Tuple[str, ...] = (
    OCR_CANDIDATE_FILE,
    VISUAL_SYMBOL_CANDIDATES_FILE,
    YOLO_UNAVAILABLE_FILE,
    BUNDLE_FILE,
)
ALL_SAMPLE_FILES: Tuple[str, ...] = VALID_SAMPLE_FILES + tuple(INVALID_FILES.values())


def read_local(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Admission
# --------------------------------------------------------------------------- #
def _prohibited_flags_present(record: Dict[str, Any]) -> List[str]:
    return [flag for flag in PROHIBITED_REQUEST_FLAGS if record.get(flag) is True]


def _is_availability_record(record: Dict[str, Any]) -> bool:
    return record.get("record_kind") == AVAILABILITY_RECORD_KIND


def admit_candidate(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    sc = record.get("source_chain")
    if not (isinstance(sc, str) and sc.strip()):
        reasons.append("missing_required_field:source_chain")
    if _is_availability_record(record):
        # availability records skip confidence; must stay declared non-blocker.
        if not (isinstance(record.get("availability_state"), str) and record["availability_state"]):
            reasons.append("missing_required_field:availability_state")
        if record.get("non_blocker") is not True:
            reasons.append("availability_record_must_be_declared_non_blocker")
    else:
        conf = record.get("confidence")
        if not isinstance(conf, (int, float)):
            reasons.append("missing_required_field:confidence")
    for p in _prohibited_flags_present(record):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


# --------------------------------------------------------------------------- #
# Main chain ingress
# --------------------------------------------------------------------------- #
def _candidate_list(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "candidates" in payload:
        items = list(payload["candidates"])
    elif payload.get("candidate_type"):
        items = [payload]
    else:
        items = []
    items.extend(payload.get("availability_records", []))
    return items


def ingress_main_chain(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Admit records and derive Field/Task/Guidance candidate-path outputs."""
    admitted_types: List[str] = []
    generated: List[str] = []
    all_admitted = True
    has_exit_text = False
    has_direction_symbol = False
    has_availability = False

    for rec in records:
        ok, _ = admit_candidate(rec)
        all_admitted = all_admitted and ok
        if not ok:
            continue
        ctype = rec.get("candidate_type", "")
        admitted_types.append(ctype)
        if ctype == "text_evidence_candidate":
            generated += [
                "text_observation_candidate",
                "facility_text_hint_candidate",
            ]
            if str(rec.get("text", "")).strip().upper() == "EXIT":
                has_exit_text = True
                generated.append("exit_text_hint_candidate")
        elif ctype == "visual_symbol_candidate":
            generated += ["visual_symbol_observation_candidate", "direction_hint_candidate"]
            if str(rec.get("direction", "")).lower() in ("right", "left"):
                has_direction_symbol = True
                generated.append("exit_direction_candidate")
        elif ctype == "model_availability_state_candidate" or _is_availability_record(rec):
            has_availability = True
            generated += [
                "model_availability_state_candidate",
                "object_detection_unavailable_record",
            ]

    # cross-modal hypothesis (OCR EXIT + directional symbol)
    if has_exit_text and has_direction_symbol:
        generated += [
            "cross_modal_consistency_candidate",
            "exit_sign_hypothesis_candidate",
            "field_affordance_hint_candidate",
        ]

    # Field / Task / Guidance candidate path (candidate-only).
    if admitted_types:
        generated.append("FieldSynthesisCandidate")
    if has_direction_symbol or has_exit_text:
        generated += ["TaskContextCandidate", "TaskRiskCandidate"]
    if has_direction_symbol or has_exit_text:
        generated += ["GuidanceCandidate", "SpeechGateCandidate"]
    # ActionSafetyCandidate always exists as a safety candidate (never triggers action).
    generated.append("ActionSafetyCandidate")

    generated_unique = sorted(set(generated))
    return {
        "all_admitted": all_admitted,
        "admitted_types": sorted(set(admitted_types)),
        "generated": generated_unique,
        "has_exit_text": has_exit_text,
        "has_direction_symbol": has_direction_symbol,
        "has_availability": has_availability,
    }


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def _case_real_ocr_ingress() -> MainChainIntegrationCaseResult:
    rec = read_local(OCR_CANDIDATE_FILE)
    res = ingress_main_chain([rec])
    ok = (
        res["all_admitted"]
        and "text_evidence_candidate" in res["admitted_types"]
        and "FieldSynthesisCandidate" in res["generated"]
    )
    return MainChainIntegrationCaseResult(
        case_id="real_ocr_candidate_main_chain_ingress",
        case_kind="positive",
        accepted=res["all_admitted"],
        expected_result="accepted",
        passed=ok,
        admitted_candidates=tuple(res["admitted_types"]),
        generated_candidates=tuple(res["generated"]),
        notes=("source_chain_preserved", "ocr_text_is_not_fact"),
    )


def _case_real_visual_symbol_ingress() -> MainChainIntegrationCaseResult:
    payload = read_local(VISUAL_SYMBOL_CANDIDATES_FILE)
    res = ingress_main_chain(_candidate_list(payload))
    ok = (
        res["all_admitted"]
        and {"color_evidence_candidate", "shape_evidence_candidate", "visual_symbol_candidate", "symbol_meaning_candidate"}.issubset(
            set(res["admitted_types"])
        )
        and "direction_hint_candidate" in res["generated"]
    )
    return MainChainIntegrationCaseResult(
        case_id="real_visual_symbol_candidate_main_chain_ingress",
        case_kind="positive",
        accepted=res["all_admitted"],
        expected_result="accepted",
        passed=ok,
        admitted_candidates=tuple(res["admitted_types"]),
        generated_candidates=tuple(res["generated"]),
        notes=("symbol_meaning_requires_context_validation", "candidate_only"),
    )


def _case_cross_validation() -> MainChainIntegrationCaseResult:
    ocr = read_local(OCR_CANDIDATE_FILE)
    symbols = _candidate_list(read_local(VISUAL_SYMBOL_CANDIDATES_FILE))
    res = ingress_main_chain([ocr] + symbols)
    ok = (
        res["all_admitted"]
        and "cross_modal_consistency_candidate" in res["generated"]
        and "exit_sign_hypothesis_candidate" in res["generated"]
    )
    return MainChainIntegrationCaseResult(
        case_id="real_ocr_visual_symbol_cross_validation",
        case_kind="positive",
        accepted=res["all_admitted"],
        expected_result="accepted",
        passed=ok,
        admitted_candidates=tuple(res["admitted_types"]),
        generated_candidates=tuple(res["generated"]),
        notes=("hypothesis_only", "not_route_activation", "not_runtime_navigation"),
    )


def _case_yolo_unavailable_ingress() -> MainChainIntegrationCaseResult:
    rec = read_local(YOLO_UNAVAILABLE_FILE)
    ok_admit, reasons = admit_candidate(rec)
    res = ingress_main_chain([rec])
    ok = (
        ok_admit
        and rec.get("non_blocker") is True
        and rec.get("model_download_triggered") is False
        and "model_availability_state_candidate" in res["generated"]
        and "object_detection_unavailable_record" in res["generated"]
    )
    return MainChainIntegrationCaseResult(
        case_id="yolo_declared_unavailable_non_blocker_ingress",
        case_kind="positive",
        accepted=ok_admit,
        expected_result="accepted",
        passed=ok,
        admitted_candidates=tuple(res["admitted_types"]),
        generated_candidates=tuple(res["generated"]),
        reject_reasons=tuple(reasons),
        notes=("unavailable_is_non_blocker_if_declared", "no_model_download_triggered"),
    )


def _case_bundle_path() -> MainChainIntegrationCaseResult:
    payload = read_local(BUNDLE_FILE)
    res = ingress_main_chain(_candidate_list(payload))
    required = {
        "FieldSynthesisCandidate",
        "TaskContextCandidate",
        "GuidanceCandidate",
        "SpeechGateCandidate",
        "ActionSafetyCandidate",
    }
    ok = res["all_admitted"] and required.issubset(set(res["generated"]))
    return MainChainIntegrationCaseResult(
        case_id="real_p0_candidate_bundle_main_chain_path",
        case_kind="positive",
        accepted=res["all_admitted"],
        expected_result="accepted",
        passed=ok,
        admitted_candidates=tuple(res["admitted_types"]),
        generated_candidates=tuple(res["generated"]),
        notes=(
            "guidance_candidate_only_not_runtime_navigation",
            "speech_gate_candidate_not_tts",
            "action_safety_candidate_exists",
            "luna_brain_cognition_first_preserved",
        ),
    )


def run_positive_cases() -> Tuple[List[MainChainIntegrationCaseResult], Dict[str, Any]]:
    results = [
        _case_real_ocr_ingress(),
        _case_real_visual_symbol_ingress(),
        _case_cross_validation(),
        _case_yolo_unavailable_ingress(),
        _case_bundle_path(),
    ]
    # Aggregate ingress over the full bundle for GO-condition coverage.
    bundle_res = ingress_main_chain(_candidate_list(read_local(BUNDLE_FILE)))
    return results, bundle_res


# --------------------------------------------------------------------------- #
# Negative cases (9 files + 1 tampered)
# --------------------------------------------------------------------------- #
def _run_negative_file_case(case_id: str, filename: str) -> MainChainIntegrationCaseResult:
    rec = read_local(filename)
    accepted, reasons = admit_candidate(rec)
    return MainChainIntegrationCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        reject_reasons=tuple(reasons),
    )


def _run_negative_tampered_case(case_id: str, mutate) -> MainChainIntegrationCaseResult:
    rec = copy.deepcopy(read_local(OCR_CANDIDATE_FILE))
    mutate(rec)
    accepted, reasons = admit_candidate(rec)
    return MainChainIntegrationCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        reject_reasons=tuple(reasons),
    )


def run_negative_cases() -> List[MainChainIntegrationCaseResult]:
    results = [_run_negative_file_case(key, fname) for key, fname in INVALID_FILES.items()]
    results.append(
        _run_negative_tampered_case(
            "invalid_model_tuning_dataset_usage",
            lambda r: (
                r.__setitem__("model_tuning_requested", True),
                r.__setitem__("dataset_usage_requested", True),
            ),
        )
    )
    return results
