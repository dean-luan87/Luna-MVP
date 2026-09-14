# -*- coding: utf-8 -*-
"""OCR / Text adapter static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.ocr_text_adapter_types_v1 import (
    ADAPTER_INPUT_FIELDS,
    ADAPTER_RESULT_FIELDS,
    EXECUTION_MODES,
    NON_EXECUTION_FLAGS,
    RAW_OUTPUT_FIELDS,
    TEXT_ANCHOR_FIELDS,
    TEXT_NORMALIZATION_FIELDS,
    TEXT_OBSERVATION_FIELDS,
    TEXT_QUALITY_FIELDS,
    TEXT_REGION_FIELDS,
)


def validate_ocr_text_adapter_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_INPUT_FIELDS if f not in pkg]
    if pkg.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if pkg.get("model_role") != "ocr_text_model":
        issues.append("model_role_must_be_ocr_text_model")
    if pkg.get("execution_mode") not in EXECUTION_MODES:
        issues.append("invalid_execution_mode")
    return len(issues) == 0, issues


def validate_ocr_text_raw_output_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in RAW_OUTPUT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("execution_mode", "").startswith("blocked") and c.get("raw_text_payload"):
        issues.append("blocked_must_not_fabricate_text")
    return len(issues) == 0, issues


def validate_text_observation_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TEXT_OBSERVATION_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_text_region_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TEXT_REGION_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_text_anchor_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TEXT_ANCHOR_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("spatial_reliability") == "unreliable" and c.get("anchor_confidence") == "high":
        issues.append("unreliable_spatial_high_confidence_not_allowed")
    return len(issues) == 0, issues


def validate_text_normalization_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TEXT_NORMALIZATION_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_text_quality_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TEXT_QUALITY_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_ocr_text_adapter_result_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ADAPTER_RESULT_FIELDS if f not in c]
    if c.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if c.get("world_model_candidate_generated"):
        issues.append("world_model_candidate_not_allowed")
    if c.get("world_model_entry_created"):
        issues.append("world_model_entry_not_allowed")
    if c.get("world_entity_candidate_generated"):
        issues.append("world_entity_candidate_not_allowed")
    if c.get("llm_text_correction_executed"):
        issues.append("llm_text_correction_not_allowed")
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
    if result.get("llm_text_correction_executed"):
        issues.append("llm_text_correction_executed")
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
