# -*- coding: utf-8 -*-
"""SLAM spatial mapping adapter static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.slam_spatial_mapping_adapter_types_v1 import (
    ADAPTER_INPUT_FIELDS,
    ADAPTER_RESULT_FIELDS,
    CAMERA_POSE_FIELDS,
    CAMERA_TRAJECTORY_FIELDS,
    EXECUTION_MODES,
    LOCAL_MAP_FIELDS,
    MAP_QUALITY_FIELDS,
    NON_EXECUTION_FLAGS,
    RAW_OUTPUT_FIELDS,
    SPATIAL_ANCHOR_FIELDS,
)


def validate_spatial_mapping_adapter_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_INPUT_FIELDS if f not in pkg]
    if pkg.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if pkg.get("model_role") != "slam_spatial_mapping":
        issues.append("model_role_must_be_slam_spatial_mapping")
    mode = pkg.get("execution_mode")
    if mode not in EXECUTION_MODES:
        issues.append("invalid_execution_mode")
    if mode in ("cached_output", "adapter_stub") and pkg.get("_marked_as_real_run"):
        issues.append("non_real_mode_marked_as_real_run")
    return len(issues) == 0, issues


def validate_spatial_mapping_raw_output_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in RAW_OUTPUT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    mode = c.get("execution_mode", "")
    if mode.startswith("blocked") and c.get("raw_pose_payload"):
        issues.append("blocked_must_not_fabricate_pose")
    return len(issues) == 0, issues


def validate_camera_pose_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in CAMERA_POSE_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("scale_status") == "scale_unknown" and c.get("pose_confidence") == "high":
        issues.append("scale_unknown_high_confidence_not_allowed")
    return len(issues) == 0, issues


def validate_camera_trajectory_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in CAMERA_TRAJECTORY_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_spatial_anchor_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in SPATIAL_ANCHOR_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("observation_count", 0) < 2 and c.get("stability_score") == "high":
        issues.append("insufficient_observations_for_high_stability")
    return len(issues) == 0, issues


def validate_local_map_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in LOCAL_MAP_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_map_quality_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MAP_QUALITY_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("scale_reliability") == "unreliable" and c.get("quality_status") == "high":
        issues.append("scale_unknown_high_quality_not_allowed")
    return len(issues) == 0, issues


def validate_spatial_mapping_adapter_result_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_RESULT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("world_model_candidate_generated"):
        issues.append("world_model_candidate_not_allowed")
    if c.get("world_model_entry_created"):
        issues.append("world_model_entry_not_allowed")
    if c.get("fact_admission_executed"):
        issues.append("fact_admission_not_allowed")
    return len(issues) == 0, issues


def validate_no_protocol_overreach(new_protocol_count: int) -> Tuple[bool, List[str]]:
    return new_protocol_count == 0, (["protocol_overreach"] if new_protocol_count else [])


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues


def validate_no_world_model_assembly_boundary(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if result.get("world_model_candidate_generated"):
        issues.append("world_model_candidate_generated")
    if result.get("world_model_entry_created"):
        issues.append("world_model_entry_created")
    return len(issues) == 0, issues
