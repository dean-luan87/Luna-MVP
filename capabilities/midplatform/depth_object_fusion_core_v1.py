# -*- coding: utf-8 -*-
"""Depth-Object fusion core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_object_fusion_result_assembler_v1 import assemble_depth_object_fusion_result
from capabilities.midplatform.depth_object_fusion_static_validators_v1 import (
    validate_depth_object_fusion_input_package,
    validate_depth_object_fusion_result_candidate,
    validate_fusion_dryrun_result,
    validate_object_depth_hint_candidate,
)
from capabilities.midplatform.object_depth_hint_candidate_builder_v1 import build_object_depth_hints_from_fusion_input


def run_depth_object_fusion(fusion_input: Dict[str, Any]) -> Dict[str, Any]:
    validate_depth_object_fusion_input_package(fusion_input)
    hints, rejected = build_object_depth_hints_from_fusion_input(fusion_input)
    for h in hints:
        validate_object_depth_hint_candidate(h)
    result = assemble_depth_object_fusion_result(
        object_depth_hint_candidates=hints,
        rejected_fusion_items=rejected,
        alignment_result_ref=fusion_input.get("alignment_result_ref"),
    )
    validate_depth_object_fusion_result_candidate(result)
    return result


def run_fusion_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    result = run_depth_object_fusion(case["fusion_input"])
    hints = result.get("object_depth_hint_candidates") or []
    rejected = result.get("rejected_fusion_count", 0)
    passed = True

    if len(hints) != case.get("expected_hint_count", len(hints)):
        passed = False
    if rejected != case.get("expected_rejected_count", rejected):
        passed = False
    if case.get("expect_near") and not any(h.get("depth_bucket") == "near" and h.get("field_zone_hint") == "inner_zone" for h in hints):
        passed = False
    if case.get("expect_middle") and not any(h.get("depth_bucket") == "middle" and h.get("field_zone_hint") == "working_zone" for h in hints):
        passed = False
    if case.get("expect_far") and not any(h.get("depth_bucket") == "far" and h.get("field_zone_hint") == "forecast_zone" for h in hints):
        passed = False
    if case.get("expect_relative_weak"):
        if not any("relative_depth_not_metric" in (h.get("warning_codes") or []) for h in hints):
            passed = False
        if any(h.get("fusion_confidence") == "high" for h in hints):
            passed = False
    if case.get("expect_missing_unknown"):
        if not any(h.get("depth_bucket") == "unknown" for h in hints):
            passed = False
    if case.get("expect_rejected_alignment"):
        if len(hints) > 0:
            passed = False
        if rejected < 1:
            passed = False
    if case.get("expect_degraded_fusion"):
        if not any(h.get("fusion_confidence") == "low" for h in hints):
            passed = False
    if case.get("expect_invalid_bbox"):
        if rejected < 1:
            passed = False
    if case.get("expect_shape_mismatch"):
        if not any("depth_map_shape_mismatch" in (h.get("warning_codes") or []) for h in hints):
            passed = False
    if case.get("expect_low_confidence"):
        if not any(h.get("fusion_confidence") == "low" for h in hints):
            passed = False
    if case.get("expect_multiple"):
        if len(hints) < case.get("expected_hint_count", 2):
            passed = False
    if case.get("expect_readiness"):
        if not result.get("readiness_for_field_geometry"):
            passed = False
    if case.get("expect_not_ready"):
        if result.get("readiness_for_field_geometry"):
            passed = False

    prohibited_absent = True
    if case.get("prohibited_geometry"):
        if any(h.get("pseudo_3d_position") for h in hints):
            prohibited_absent = False
    if any(h.get("candidate_only") is not True for h in hints):
        prohibited_absent = False

    dry = {
        "case_id": case["case_id"],
        "expected_hint_count": case.get("expected_hint_count", len(hints)),
        "actual_hint_count": len(hints),
        "expected_rejected_count": case.get("expected_rejected_count", rejected),
        "actual_rejected_count": rejected,
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": ["fusion_complete"],
        "fusion_result": result,
    }
    validate_fusion_dryrun_result(dry)
    return dry


def run_all_fusion_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_fusion_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
