# -*- coding: utf-8 -*-
"""Real observation candidate ingestion core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.object_observation_candidate_builder_v1 import build_object_observation_candidate
from capabilities.midplatform.real_observation_candidate_ingestion_static_validators_v1 import (
    validate_depth_missing_fallback,
    validate_detector_output_mock,
    validate_ingestion_dryrun_result,
    validate_ingestion_result,
    validate_normalized_detection_candidate,
    validate_object_observation_candidate,
)
from capabilities.midplatform.real_observation_detection_normalizer_v1 import normalize_detector_output_to_luna_detection
from capabilities.midplatform.real_observation_ingestion_result_assembler_v1 import assemble_real_observation_ingestion_result


def run_real_observation_candidate_ingestion(
    detector_output: Dict[str, Any],
    *,
    depth_source: str = "unknown",
) -> Dict[str, Any]:
    validate_detector_output_mock(detector_output)
    normalized, rejected, global_warnings = normalize_detector_output_to_luna_detection(detector_output)
    accepted: List[Dict[str, Any]] = []
    missing_info: List[str] = []
    all_warnings = list(global_warnings)
    for nd in normalized:
        validate_normalized_detection_candidate(nd)
        obs = build_object_observation_candidate(nd, detector_output=detector_output, depth_source=depth_source)
        validate_object_observation_candidate(obs)
        validate_depth_missing_fallback(obs)
        if obs.get("validation_status") == "valid":
            accepted.append(obs)
            missing_info.extend(obs.get("missing_information") or [])
        else:
            rejected.append({"normalized_detection_id": nd.get("normalized_detection_id"), "reason": "validation_failed"})
        all_warnings.extend(obs.get("warning_codes") or [])
    result = assemble_real_observation_ingestion_result(
        accepted_candidates=accepted,
        rejected_detections=rejected,
        warning_summary=all_warnings,
        missing_information=sorted(set(missing_info)),
    )
    validate_ingestion_result(result)
    return result


def run_ingestion_from_supervision_normalized(
    supervision_output: Dict[str, Any],
) -> Dict[str, Any]:
    """Accept pre-normalized supervision mock as detector-like input."""
    detector_like = {
        "detector_output_id": supervision_output.get("source_detector_output_ref", "sup_norm"),
        "model_ref": supervision_output.get("model_ref", "supervision_normalized_mock"),
        "source_type": "model_detector",
        "source_ref": "supervision_normalized",
        "frame_ref": supervision_output.get("frame_ref", "frame_0"),
        "timestamp": supervision_output.get("timestamp", "2026-06-11T00:00:00Z"),
        "frame_width": supervision_output.get("frame_width", 640),
        "frame_height": supervision_output.get("frame_height", 480),
        "detections": [{
            "bbox_xyxy": supervision_output.get("xyxy"),
            "class_name": supervision_output.get("label"),
            "confidence": supervision_output.get("confidence"),
            "class_id": supervision_output.get("class_id"),
            "tracker_hint_id": supervision_output.get("tracker_hint_id"),
        }],
    }
    return run_real_observation_candidate_ingestion(detector_like)


def run_ingestion_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    if case.get("use_supervision_normalized_path"):
        result = run_ingestion_from_supervision_normalized(case["supervision_output"])
    else:
        result = run_real_observation_candidate_ingestion(
            case["detector_output"],
            depth_source=case.get("depth_source", "unknown"),
        )
    accepted = result.get("accepted_candidates") or []
    rejected = result.get("rejected_detections") or []
    passed = True
    if len(accepted) != case.get("expected_accepted_count", len(accepted)):
        passed = False
    if len(rejected) != case.get("expected_rejected_count", len(rejected)):
        passed = False
    if case.get("expect_readiness") and not result.get("readiness_for_field_first_core"):
        passed = False
    if case.get("expect_low_confidence_retained"):
        if not any((c.get("confidence") or 1) < 0.4 for c in accepted):
            passed = False
    if case.get("expect_unknown_label"):
        if not any(c.get("label") == "unknown_object" for c in accepted):
            passed = False
    if case.get("expect_depth_unknown"):
        if not all(c.get("depth_source") == "unknown" for c in accepted):
            passed = False
    if case.get("expect_tracker_hint"):
        if not any(c.get("tracker_hint_id") and c.get("tracker_id_is_hint_not_fact") for c in accepted):
            passed = False
    if case.get("expect_rejected"):
        if len(rejected) < 1:
            passed = False
    prohibited_absent = True
    if case.get("prohibited_silent_drop") and case.get("expect_low_confidence_retained") and not accepted:
        prohibited_absent = False
    if any(c.get("candidate_only") is not True for c in accepted):
        prohibited_absent = False

    dry = {
        "case_id": case["case_id"],
        "expected_accepted_count": case.get("expected_accepted_count", len(accepted)),
        "actual_accepted_count": len(accepted),
        "expected_rejected_count": case.get("expected_rejected_count", len(rejected)),
        "actual_rejected_count": len(rejected),
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": ["ingestion_complete"],
        "ingestion_result": result,
    }
    validate_ingestion_dryrun_result(dry)
    return dry


def run_all_ingestion_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_ingestion_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
