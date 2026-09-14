# -*- coding: utf-8 -*-
"""Field assembly static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_assembly_types_v1 import (
    ASSEMBLY_INPUT_FIELDS,
    ASSEMBLY_RESULT_FIELDS,
    DRYRUN_RESULT_FIELDS,
    ENHANCED_ENTITY_FIELDS,
    ENHANCED_SCENE_FIELDS,
    NON_EXECUTION_FLAGS,
)


def validate_assembly_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ASSEMBLY_INPUT_FIELDS if f not in pkg]
    return len(issues) == 0, issues


def validate_enhanced_field_entity_candidate(entity: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ENHANCED_ENTITY_FIELDS if f not in entity]
    if entity.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if entity.get("fact_status") != "candidate":
        issues.append("fact_status_must_be_candidate")
    if entity.get("depth_source") == "hardware" and entity.get("depth_error_expected") is not True:
        issues.append("estimated_depth_error_expected_required")
    return len(issues) == 0, issues


def validate_enhanced_field_scene_candidate(scene: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ENHANCED_SCENE_FIELDS if f not in scene]
    if scene.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if scene.get("field_origin") != "self_centered":
        issues.append("field_origin_self_centered_required")
    flags = scene.get("non_execution_flags") or {}
    if flags.get("no_scene_relation_generation") is not True:
        issues.append("no_scene_relation_required")
    if scene.get("scene_relation_candidates"):
        issues.append("scene_relation_must_not_exist")
    return len(issues) == 0, issues


def validate_field_assembly_result_candidate(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ASSEMBLY_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    flags = result.get("non_execution_flags") or {}
    if flags.get("no_field_simulation") is not True:
        issues.append("no_field_simulation_required")
    if flags.get("no_world_model_fact") is not True:
        issues.append("no_world_model_fact_required")
    return len(issues) == 0, issues


def validate_zone_summary(summary: Dict[str, Any]) -> Tuple[bool, List[str]]:
    keys = (
        "inner_zone_entity_count", "working_zone_entity_count",
        "forecast_zone_entity_count", "unknown_zone_entity_count",
    )
    issues = [f"missing_{k}" for k in keys if k not in summary]
    return len(issues) == 0, issues


def validate_quality_summaries(
    scene: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    issues = []
    for k in ("scene_quality_summary", "depth_quality_summary", "geometry_quality_summary"):
        if k not in scene:
            issues.append(f"missing_{k}")
    return len(issues) == 0, issues


def validate_assembly_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DRYRUN_RESULT_FIELDS if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
