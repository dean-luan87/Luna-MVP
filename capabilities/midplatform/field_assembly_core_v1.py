# -*- coding: utf-8 -*-
"""Field assembly core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.enhanced_field_entity_builder_v1 import build_enhanced_field_entity_candidates
from capabilities.midplatform.enhanced_field_scene_assembler_v1 import assemble_enhanced_field_scene_candidate
from capabilities.midplatform.field_assembly_result_assembler_v1 import assemble_field_assembly_result
from capabilities.midplatform.field_assembly_static_validators_v1 import (
    validate_assembly_dryrun_result,
    validate_assembly_input_package,
    validate_enhanced_field_entity_candidate,
    validate_enhanced_field_scene_candidate,
    validate_field_assembly_result_candidate,
    validate_quality_summaries,
    validate_zone_summary,
)


def run_field_assembly(assembly_input: Dict[str, Any]) -> Dict[str, Any]:
    validate_assembly_input_package(assembly_input)
    entities, rejected = build_enhanced_field_entity_candidates(assembly_input)
    for e in entities:
        validate_enhanced_field_entity_candidate(e)
    scene = assemble_enhanced_field_scene_candidate(
        entities=entities,
        geometry_candidates=list(assembly_input.get("field_geometry_candidates") or []),
        hints=list(assembly_input.get("object_depth_hints") or []),
        assembly_input=assembly_input,
    )
    validate_enhanced_field_scene_candidate(scene)
    validate_zone_summary(scene.get("zone_summary") or {})
    validate_quality_summaries(scene)
    result = assemble_field_assembly_result(
        enhanced_field_scene=scene,
        enhanced_entities=entities,
        rejected_items=rejected,
        alignment_result_ref=assembly_input.get("alignment_result_ref"),
        fusion_result_ref=assembly_input.get("fusion_result_ref"),
        geometry_result_ref=assembly_input.get("geometry_result_ref"),
    )
    validate_field_assembly_result_candidate(result)
    return result


def run_assembly_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    result = run_field_assembly(case["assembly_input"])
    entities = result.get("enhanced_entity_candidates") or []
    rejected = result.get("rejected_entity_count", 0)
    scene = result.get("enhanced_field_scene_candidate") or {}
    passed = True

    if len(entities) != case.get("expected_entity_count", len(entities)):
        passed = False
    if rejected != case.get("expected_rejected_count", rejected):
        passed = False

    if case.get("expect_geometry_enhanced"):
        if not any(e.get("entity_status") == "entity_geometry_enhanced" for e in entities):
            passed = False
    if case.get("expect_2d_only"):
        if not any(e.get("entity_status") == "entity_2d_only" for e in entities):
            passed = False
    if case.get("expect_geometry_unknown"):
        if not any(e.get("entity_status") == "entity_geometry_unknown" for e in entities):
            passed = False
    if case.get("expect_low_confidence_retained"):
        if not any(e.get("confidence", 1) < 0.5 for e in entities):
            passed = False
    if case.get("expect_duplicate_not_merged"):
        labels = [e.get("label") for e in entities]
        if labels.count("cup") < 2 or len(entities) < 2:
            passed = False
    if case.get("expect_depth_only_no_entity"):
        if len(entities) > 0:
            passed = False
    if case.get("expect_geometry_rejected"):
        if rejected < 1:
            passed = False
    if case.get("expect_estimated_depth_error"):
        if not all(e.get("depth_error_expected") is True for e in entities if e.get("depth_hint") is not None):
            passed = False
        if any(e.get("depth_source") == "hardware" for e in entities):
            passed = False
    if case.get("expect_zone_counts"):
        zs = scene.get("zone_summary") or {}
        for k, v in (case.get("expected_zone_counts") or {}).items():
            if zs.get(k) != v:
                passed = False
    if case.get("expect_geometry_quality_degraded"):
        gq = scene.get("geometry_quality_summary") or {}
        if gq.get("geometry_quality") != "degraded":
            passed = False
    if case.get("expect_readiness_core"):
        if not result.get("readiness_for_field_first_core"):
            passed = False
    if case.get("expect_readiness_real_path"):
        if not result.get("readiness_for_real_model_success_path"):
            passed = False
    if case.get("expect_multiple_zones"):
        zs = scene.get("zone_summary") or {}
        active = sum(1 for k in ("inner_zone_entity_count", "working_zone_entity_count", "forecast_zone_entity_count", "unknown_zone_entity_count") if zs.get(k, 0) > 0)
        if active < case.get("min_active_zones", 2):
            passed = False

    prohibited_absent = True
    if case.get("prohibited_scene_relation"):
        if scene.get("scene_relation_candidates"):
            prohibited_absent = False
    if result.get("scene_relation_candidates"):
        prohibited_absent = False
    if case.get("prohibited_simulation"):
        if result.get("field_simulation_result"):
            prohibited_absent = False
    if case.get("prohibited_world_model"):
        if any(e.get("fact_status") != "candidate" for e in entities):
            prohibited_absent = False

    dry = {
        "case_id": case["case_id"],
        "expected_entity_count": case.get("expected_entity_count", len(entities)),
        "actual_entity_count": len(entities),
        "expected_rejected_count": case.get("expected_rejected_count", rejected),
        "actual_rejected_count": rejected,
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": ["field_assembly_complete"],
        "assembly_result": result,
    }
    validate_assembly_dryrun_result(dry)
    return dry


def run_all_assembly_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_assembly_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
