# -*- coding: utf-8 -*-
"""Field geometry candidate static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_geometry_candidate_types_v1 import (
    DRYRUN_RESULT_FIELDS,
    FIELD_GEOMETRY_CANDIDATE_FIELDS,
    GEOMETRY_GENERATION_RESULT_FIELDS,
    GEOMETRY_INPUT_FIELDS,
    NON_EXECUTION_FLAGS,
    OBJECT_SPATIAL_STATE_FIELDS,
)
from capabilities.midplatform.geometry_confidence_policy_v1 import GEOMETRY_CONFIDENCE_POLICY
from capabilities.midplatform.pseudo_3d_projection_policy_v1 import PSEUDO_3D_PROJECTION_POLICY


def validate_geometry_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in GEOMETRY_INPUT_FIELDS if f not in pkg]
    return len(issues) == 0, issues


def validate_object_spatial_state_candidate(state: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_SPATIAL_STATE_FIELDS if f not in state]
    if state.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if state.get("spatial_confidence") == "high":
        issues.append("spatial_confidence_not_high_allowed")
    return len(issues) == 0, issues


def validate_field_geometry_candidate(geom: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in FIELD_GEOMETRY_CANDIDATE_FIELDS if f not in geom]
    if geom.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if geom.get("geometry_confidence") == "high":
        issues.append("geometry_confidence_not_high_allowed")
    if geom.get("depth_error_expected") is not True:
        issues.append("depth_error_expected_required")
    return len(issues) == 0, issues


def validate_field_geometry_generation_result_candidate(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in GEOMETRY_GENERATION_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    flags = result.get("non_execution_flags") or {}
    if flags.get("no_field_scene_assembly") is not True:
        issues.append("no_field_scene_assembly_required")
    if flags.get("no_world_model_fact") is not True:
        issues.append("no_world_model_fact_required")
    return len(issues) == 0, issues


def validate_pseudo_3d_projection_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = []
    if policy.get("policy_id") != "pseudo_3d_projection_policy_v1":
        issues.append("policy_id_mismatch")
    if policy.get("coordinate_mode") != "normalized_image_depth_hint":
        issues.append("coordinate_mode_mismatch")
    return len(issues) == 0, issues


def validate_geometry_confidence_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = []
    if policy.get("policy_id") != "geometry_confidence_policy_v1":
        issues.append("policy_id_mismatch")
    return len(issues) == 0, issues


def validate_geometry_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DRYRUN_RESULT_FIELDS if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
