# -*- coding: utf-8 -*-
"""Field geometry candidate core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_geometry_candidate_builder_v1 import build_field_geometry_from_input
from capabilities.midplatform.field_geometry_candidate_static_validators_v1 import (
    validate_field_geometry_candidate,
    validate_field_geometry_generation_result_candidate,
    validate_geometry_dryrun_result,
    validate_geometry_input_package,
    validate_object_spatial_state_candidate,
)
from capabilities.midplatform.field_geometry_generation_result_assembler_v1 import (
    assemble_field_geometry_generation_result,
)


def run_field_geometry_generation(geometry_input: Dict[str, Any]) -> Dict[str, Any]:
    validate_geometry_input_package(geometry_input)
    spatials, geometries, rejected = build_field_geometry_from_input(geometry_input)
    for s in spatials:
        validate_object_spatial_state_candidate(s)
    for g in geometries:
        validate_field_geometry_candidate(g)
    result = assemble_field_geometry_generation_result(
        object_spatial_state_candidates=spatials,
        field_geometry_candidates=geometries,
        rejected_geometry_items=rejected,
        depth_object_fusion_result_ref=geometry_input.get("depth_object_fusion_result_ref"),
    )
    validate_field_geometry_generation_result_candidate(result)
    return result


def run_geometry_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    result = run_field_geometry_generation(case["geometry_input"])
    spatials = result.get("object_spatial_state_candidates") or []
    geometries = result.get("field_geometry_candidates") or []
    rejected = result.get("rejected_geometry_count", 0)
    passed = True

    if len(spatials) != case.get("expected_spatial_count", len(spatials)):
        passed = False
    if len(geometries) != case.get("expected_geometry_count", len(geometries)):
        passed = False
    if rejected != case.get("expected_rejected_count", rejected):
        passed = False

    if case.get("expect_inner_zone"):
        if not any(g.get("field_zone") == "inner_zone" and g.get("geometry_status") == "geometry_estimated" for g in geometries):
            passed = False
    if case.get("expect_working_zone"):
        if not any(g.get("field_zone") == "working_zone" for g in geometries):
            passed = False
    if case.get("expect_forecast_zone"):
        if not any(g.get("field_zone") == "forecast_zone" for g in geometries):
            passed = False
    if case.get("expect_weak_geometry"):
        if not any(g.get("geometry_status") == "geometry_weak_estimated" for g in geometries):
            passed = False
        if any(g.get("geometry_confidence") == "high" for g in geometries):
            passed = False
    if case.get("expect_geometry_unknown"):
        if not any(g.get("geometry_status") == "geometry_unknown" for g in geometries):
            passed = False
        if not any(s.get("pseudo_3d_status") == "pseudo_3d_unknown" for s in spatials):
            passed = False
    if case.get("expect_geometry_rejected"):
        if rejected < 1:
            passed = False
        if len(geometries) > case.get("expected_geometry_count", 0):
            passed = False
    if case.get("expect_confidence_low"):
        if not any(g.get("geometry_confidence") == "low" for g in geometries):
            passed = False
    if case.get("expect_out_of_range"):
        if not any("depth_out_of_range" in (g.get("warning_codes") or []) for g in geometries):
            passed = False
    if case.get("expect_multiple"):
        if len(geometries) < case.get("expected_geometry_count", 2):
            passed = False
    if case.get("expect_spatial_unknown_kept"):
        if len(spatials) < case.get("expected_spatial_count", 1):
            passed = False
        if not any(s.get("pseudo_3d_status") == "pseudo_3d_unknown" for s in spatials):
            passed = False
    if case.get("expect_readiness"):
        if not result.get("readiness_for_field_assembly"):
            passed = False

    prohibited_absent = True
    if case.get("prohibited_field_scene"):
        if result.get("field_scene_candidate"):
            prohibited_absent = False
    if case.get("prohibited_scene_relation"):
        if result.get("scene_relation_candidates"):
            prohibited_absent = False
    if any(g.get("candidate_only") is not True for g in geometries):
        prohibited_absent = False

    dry = {
        "case_id": case["case_id"],
        "expected_spatial_count": case.get("expected_spatial_count", len(spatials)),
        "actual_spatial_count": len(spatials),
        "expected_geometry_count": case.get("expected_geometry_count", len(geometries)),
        "actual_geometry_count": len(geometries),
        "expected_rejected_count": case.get("expected_rejected_count", rejected),
        "actual_rejected_count": rejected,
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": ["geometry_generation_complete"],
        "geometry_result": result,
    }
    validate_geometry_dryrun_result(dry)
    return dry


def run_all_geometry_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_geometry_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
