# -*- coding: utf-8 -*-
"""Depth observation candidate ingestion core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_fallback_policy_v1 import (
    apply_depth_estimated_hint,
    apply_depth_missing_fallback,
    apply_depth_unreliable_fallback,
)
from capabilities.midplatform.depth_ingestion_result_assembler_v1 import assemble_depth_ingestion_result
from capabilities.midplatform.depth_observation_candidate_builder_v1 import build_depth_observation_candidate
from capabilities.midplatform.depth_observation_candidate_ingestion_static_validators_v1 import (
    validate_depth_model_output_mock,
    validate_depth_observation_candidate,
    validate_depth_ingestion_result_candidate,
    validate_ingestion_dryrun_result,
    validate_object_depth_hint_candidate,
)
from capabilities.midplatform.object_depth_hint_extractor_v1 import extract_object_depth_hint_candidates


def run_depth_observation_candidate_ingestion(
    depth_output: Dict[str, Any],
    object_observations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    validate_depth_model_output_mock(depth_output)
    depth_obs, build_warnings = build_depth_observation_candidate(depth_output)
    validate_depth_observation_candidate(depth_obs)
    hints, rejected, extract_warnings = extract_object_depth_hint_candidates(
        depth_obs, object_observations, depth_output=depth_output,
    )
    missing_info: List[str] = list(depth_obs.get("missing_information") or [])
    all_warnings = list(build_warnings) + list(extract_warnings)
    for h in hints:
        validate_object_depth_hint_candidate(h)
        missing_info.extend(h.get("missing_information") or [])
        all_warnings.extend(h.get("warning_codes") or [])
    result = assemble_depth_ingestion_result(
        depth_observation_candidate=depth_obs,
        object_depth_hint_candidates=hints,
        rejected_objects=rejected,
        warning_summary=all_warnings,
        missing_information=sorted(set(missing_info)),
    )
    validate_depth_ingestion_result_candidate(result)
    return result


def run_depth_ingestion_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    result = run_depth_observation_candidate_ingestion(
        case["depth_output"],
        case["object_observations"],
    )
    hints = result.get("object_depth_hint_candidates") or []
    rejected = result.get("rejected_object_count", 0)
    passed = True

    if len(hints) != case.get("expected_hint_count", len(hints)):
        passed = False
    if rejected != case.get("expected_rejected_count", rejected):
        passed = False
    if case.get("expect_readiness") and not result.get("readiness_for_field_geometry"):
        passed = False
    if case.get("expect_depth_missing"):
        if not any(h.get("depth_bucket") == "unknown" for h in hints):
            passed = False
    if case.get("expect_relative_warning"):
        if "depth_value_unit_unknown" not in (result["depth_observation_candidate"].get("warning_codes") or []):
            if "relative_depth_confidence_capped" not in (result["depth_observation_candidate"].get("warning_codes") or []):
                w = result["depth_observation_candidate"].get("depth_value_unit")
                if w != "relative" or result["depth_observation_candidate"].get("depth_confidence") == "high":
                    passed = False
    if case.get("expect_metric_estimated"):
        dobs = result["depth_observation_candidate"]
        if dobs.get("depth_value_unit") != "metric" or dobs.get("depth_error_expected") is not True:
            passed = False
    if case.get("expect_rejected"):
        if rejected < 1:
            passed = False
    if case.get("expect_frame_mismatch"):
        if rejected < 1:
            passed = False
    if case.get("expect_timestamp_warning"):
        if not any("timestamp_gap_warning" in (h.get("warning_codes") or []) for h in hints):
            passed = False
    if case.get("expect_unreliable_downgrade"):
        if not any(h.get("depth_confidence") == "low" for h in hints):
            passed = False
    if case.get("expect_field_zone"):
        expected_zone = case.get("expect_field_zone")
        if not any(h.get("field_zone_hint") == expected_zone for h in hints):
            passed = False
    if case.get("expect_depth_bucket"):
        if not any(h.get("depth_bucket") == case["expect_depth_bucket"] for h in hints):
            passed = False
    if case.get("expect_object_not_blocked"):
        if len(hints) < case.get("expected_hint_count", 1):
            passed = False
    if case.get("expect_no_hardware_fact"):
        dobs = result["depth_observation_candidate"]
        if dobs.get("depth_source") == "hardware":
            passed = False
        if any(h.get("depth_source") == "hardware" for h in hints):
            passed = False

    prohibited_absent = True
    if case.get("prohibited_drop_on_unknown") and case.get("expect_object_not_blocked"):
        if len(hints) == 0:
            prohibited_absent = False
    if any(h.get("candidate_only") is not True for h in hints):
        prohibited_absent = False
    if result["depth_observation_candidate"].get("candidate_only") is not True:
        prohibited_absent = False

    dry = {
        "case_id": case["case_id"],
        "expected_hint_count": case.get("expected_hint_count", len(hints)),
        "actual_hint_count": len(hints),
        "expected_rejected_count": case.get("expected_rejected_count", rejected),
        "actual_rejected_count": rejected,
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": ["depth_ingestion_complete"],
        "ingestion_result": result,
    }
    validate_ingestion_dryrun_result(dry)
    return dry


def run_all_depth_ingestion_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_depth_ingestion_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
