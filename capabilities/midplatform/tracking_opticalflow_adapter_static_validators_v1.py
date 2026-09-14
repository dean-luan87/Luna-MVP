# -*- coding: utf-8 -*-
"""Tracking / Optical Flow adapter static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.tracking_opticalflow_adapter_types_v1 import (
    ADAPTER_INPUT_FIELDS,
    ADAPTER_RESULT_FIELDS,
    EXECUTION_MODES,
    MOTION_FIELDS,
    NON_EXECUTION_FLAGS,
    OBJECT_PERSISTENCE_FIELDS,
    OBJECT_TRACK_FIELDS,
    RAW_OUTPUT_FIELDS,
    TRACKING_QUALITY_FIELDS,
)


def validate_tracking_opticalflow_adapter_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_INPUT_FIELDS if f not in pkg]
    if pkg.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if pkg.get("model_role") != "tracking_optical_flow":
        issues.append("model_role_must_be_tracking_optical_flow")
    mode = pkg.get("execution_mode")
    if mode not in EXECUTION_MODES:
        issues.append("invalid_execution_mode")
    if mode in ("cached_output", "adapter_stub") and pkg.get("_marked_as_real_run"):
        issues.append("non_real_mode_marked_as_real_run")
    return len(issues) == 0, issues


def validate_tracking_opticalflow_raw_output_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in RAW_OUTPUT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    mode = c.get("execution_mode", "")
    if mode.startswith("blocked") and c.get("raw_track_payload"):
        issues.append("blocked_must_not_fabricate_track")
    if mode.startswith("blocked") and c.get("raw_motion_payload"):
        issues.append("blocked_must_not_fabricate_motion")
    return len(issues) == 0, issues


def validate_object_track_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_TRACK_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_object_persistence_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_PERSISTENCE_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("observation_count", 0) < 2 and c.get("persistence_status") == "persistent_candidate":
        issues.append("short_track_not_persistent")
    if c.get("lifecycle_status") == "lost" and c.get("persistence_status") == "persistent_candidate":
        issues.append("lost_track_not_persistent")
    return len(issues) == 0, issues


def validate_motion_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MOTION_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("navigation_suggestion"):
        issues.append("navigation_suggestion_not_allowed")
    return len(issues) == 0, issues


def validate_tracking_quality_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TRACKING_QUALITY_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_tracking_opticalflow_adapter_result_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_RESULT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("world_model_candidate_generated"):
        issues.append("world_model_candidate_not_allowed")
    if c.get("world_model_entry_created"):
        issues.append("world_model_entry_not_allowed")
    if c.get("world_entity_candidate_generated"):
        issues.append("world_entity_candidate_not_allowed")
    if c.get("fact_admission_executed"):
        issues.append("fact_admission_not_allowed")
    if c.get("task_action_output"):
        issues.append("task_action_output_not_allowed")
    return len(issues) == 0, issues


def validate_no_protocol_overreach(new_protocol_count: int) -> Tuple[bool, List[str]]:
    return new_protocol_count == 0, (["protocol_overreach"] if new_protocol_count else [])


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues


def validate_no_task_action_boundary(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if result.get("task_action_output"):
        issues.append("task_action_output")
    if result.get("navigation_suggestion_output"):
        issues.append("navigation_suggestion_output")
    return len(issues) == 0, issues


def validate_no_world_model_assembly_boundary(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if result.get("world_model_candidate_generated"):
        issues.append("world_model_candidate_generated")
    if result.get("world_model_entry_created"):
        issues.append("world_model_entry_created")
    if result.get("world_entity_candidate_generated"):
        issues.append("world_entity_candidate_generated")
    return len(issues) == 0, issues
