# -*- coding: utf-8 -*-
"""Multi-Model alignment core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.multi_model_alignment_builder_v1 import build_multi_model_aligned_observation_candidates
from capabilities.midplatform.multi_model_alignment_result_assembler_v1 import assemble_multi_model_alignment_result
from capabilities.midplatform.multi_model_alignment_static_validators_v1 import (
    validate_aligned_observation_candidate,
    validate_alignment_dryrun_result,
    validate_alignment_input_package,
    validate_alignment_result_candidate,
)


def run_multi_model_alignment(input_pkg: Dict[str, Any]) -> Dict[str, Any]:
    validate_alignment_input_package(input_pkg)
    aligned, rejected = build_multi_model_aligned_observation_candidates(
        object_observations=input_pkg.get("object_observations") or [],
        depth_observation=input_pkg.get("depth_observation"),
        optional_observations=input_pkg.get("optional_observations") or [],
        alignment_group_id=input_pkg.get("alignment_group_id"),
    )
    for c in aligned:
        validate_aligned_observation_candidate(c)
    result = assemble_multi_model_alignment_result(
        aligned_candidates=aligned,
        rejected_outputs=rejected,
    )
    validate_alignment_result_candidate(result)
    return result


def run_alignment_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    result = run_multi_model_alignment(case["input_package"])
    aligned = result.get("aligned_candidates") or []
    rejected = result.get("rejected_outputs") or []
    passed = True

    if len(aligned) != case.get("expected_aligned_count", len(aligned)):
        passed = False
    if len(rejected) != case.get("expected_rejected_count", len(rejected)):
        passed = False
    if case.get("expect_strong") and not any(c.get("alignment_status") == "aligned_strong" for c in aligned):
        passed = False
    if case.get("expect_frame_reject"):
        if not any(c.get("alignment_status") == "rejected_frame_mismatch" for c in aligned + [{"alignment_status": r.get("reason")} for r in rejected]):
            if len(rejected) < 1 and not any("frame" in str(c.get("alignment_status", "")) for c in aligned):
                passed = False
        if len(rejected) < 1:
            passed = False
    if case.get("expect_ts_weak"):
        if not any(c.get("alignment_status") in ("aligned_weak", "aligned_degraded") for c in aligned):
            passed = False
    if case.get("expect_ts_reject"):
        if len(rejected) < 1:
            passed = False
    if case.get("expect_camera_degraded"):
        if not any("camera" in str(d) for c in aligned for d in (c.get("degradation_reason_codes") or [])):
            if not any("camera" in str(w) for c in aligned for w in (c.get("warning_codes") or [])):
                passed = False
    if case.get("expect_frame_size_warning"):
        if not any("frame_size" in str(w) for c in aligned for w in (c.get("warning_codes") or [])):
            passed = False
    if case.get("expect_missing_depth"):
        if not any("depth_model" in (c.get("missing_model_roles") or []) for c in aligned):
            passed = False
        if not any(c.get("primary_object_observation_ref") for c in aligned):
            passed = False
    if case.get("expect_depth_only_insufficient"):
        if not any(c.get("alignment_status") == "insufficient_alignment" for c in aligned):
            passed = False
        if any(c.get("primary_object_observation_ref") for c in aligned):
            passed = False
    if case.get("expect_multiple_aligned"):
        if len(aligned) < case.get("expected_aligned_count", 2):
            passed = False
    if case.get("expect_optional_tracking"):
        if not any("optional_model" in (c.get("aligned_model_roles") or []) for c in aligned):
            passed = False
    if case.get("expect_optional_ocr"):
        if not any(c.get("optional_observation_refs") for c in aligned):
            passed = False
    if case.get("expect_conflict_summary"):
        if (result.get("conflict_summary") or {}).get("conflict_count", 0) < 1:
            passed = False
    if case.get("expect_readiness"):
        if not result.get("readiness_for_depth_object_fusion"):
            passed = False

    prohibited_absent = True
    if case.get("prohibited_fusion") and any(c.get("object_depth_hint") for c in aligned):
        prohibited_absent = False
    if any(c.get("candidate_only") is not True for c in aligned):
        prohibited_absent = False

    dry = {
        "case_id": case["case_id"],
        "expected_aligned_count": case.get("expected_aligned_count", len(aligned)),
        "actual_aligned_count": len(aligned),
        "expected_rejected_count": case.get("expected_rejected_count", len(rejected)),
        "actual_rejected_count": len(rejected),
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": ["alignment_complete"],
        "alignment_result": result,
    }
    validate_alignment_dryrun_result(dry)
    return dry


def run_all_alignment_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_alignment_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
