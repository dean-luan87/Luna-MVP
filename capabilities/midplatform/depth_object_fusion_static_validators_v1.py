# -*- coding: utf-8 -*-
"""Depth-Object fusion static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_object_fusion_types_v1 import (
    BBOX_DEPTH_SAMPLING_POLICY_FIELDS,
    DRYRUN_RESULT_FIELDS,
    FUSION_INPUT_FIELDS,
    FUSION_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
    OBJECT_DEPTH_HINT_FIELDS,
)


def validate_depth_object_fusion_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in FUSION_INPUT_FIELDS if f not in pkg]
    return len(issues) == 0, issues


def validate_bbox_depth_sampling_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in BBOX_DEPTH_SAMPLING_POLICY_FIELDS if f not in policy]
    return len(issues) == 0, issues


def validate_object_depth_hint_candidate(hint: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_DEPTH_HINT_FIELDS if f not in hint]
    if hint.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if hint.get("depth_error_expected") is not True:
        issues.append("depth_error_expected_required")
    if hint.get("fusion_confidence") == "high" and "relative_depth_not_metric" in (hint.get("depth_reliability_reasons") or []):
        issues.append("relative_depth_fusion_confidence_not_high")
    return len(issues) == 0, issues


def validate_depth_object_fusion_result_candidate(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in FUSION_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    flags = result.get("non_execution_flags") or {}
    if flags.get("no_field_geometry_generation") is not True:
        issues.append("no_field_geometry_flag_required")
    if flags.get("no_pseudo_3d_position_generation") is not True:
        issues.append("no_pseudo_3d_flag_required")
    return len(issues) == 0, issues


def validate_fusion_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DRYRUN_RESULT_FIELDS if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
