# -*- coding: utf-8 -*-
"""Segmentation / Mask adapter static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.segmentation_mask_adapter_types_v1 import (
    ADAPTER_INPUT_FIELDS,
    ADAPTER_RESULT_FIELDS,
    EXECUTION_MODES,
    FREESPACE_FIELDS,
    MASK_OBSERVATION_FIELDS,
    MASK_QUALITY_FIELDS,
    NON_EXECUTION_FLAGS,
    OBJECT_BOUNDARY_FIELDS,
    RAW_OUTPUT_FIELDS,
    REGION_OBSERVATION_FIELDS,
)


def validate_segmentation_mask_adapter_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_INPUT_FIELDS if f not in pkg]
    if pkg.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if pkg.get("model_role") != "segmentation_mask_model":
        issues.append("model_role_must_be_segmentation_mask_model")
    if pkg.get("execution_mode") not in EXECUTION_MODES:
        issues.append("invalid_execution_mode")
    return len(issues) == 0, issues


def validate_segmentation_mask_raw_output_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in RAW_OUTPUT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("execution_mode", "").startswith("blocked") and c.get("raw_mask_payload"):
        issues.append("blocked_must_not_fabricate_mask")
    return len(issues) == 0, issues


def validate_mask_observation_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MASK_OBSERVATION_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_object_boundary_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_BOUNDARY_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if not c.get("associated_object_observation_refs") and c.get("boundary_confidence") == "high":
        issues.append("no_object_ref_high_confidence_not_allowed")
    return len(issues) == 0, issues


def validate_freespace_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in FREESPACE_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_region_observation_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in REGION_OBSERVATION_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_mask_quality_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MASK_QUALITY_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_segmentation_mask_adapter_result_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_RESULT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("world_model_candidate_generated"):
        issues.append("world_model_candidate_not_allowed")
    if c.get("world_model_entry_created"):
        issues.append("world_model_entry_not_allowed")
    if c.get("world_entity_candidate_generated"):
        issues.append("world_entity_candidate_not_allowed")
    if c.get("world_geometry_candidate_generated"):
        issues.append("world_geometry_candidate_not_allowed")
    if c.get("task_action_output"):
        issues.append("task_action_output_not_allowed")
    if c.get("navigation_suggestion_output"):
        issues.append("navigation_suggestion_not_allowed")
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
    if result.get("world_geometry_candidate_generated"):
        issues.append("world_geometry_candidate_generated")
    return len(issues) == 0, issues
