# -*- coding: utf-8 -*-
"""Execution path hardening static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_model_field_construction_execution_path_hardening_types_v1 import (
    EXECUTION_PATH_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
    QUALITY_REPORT_FIELDS,
)


def validate_execution_path_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in EXECUTION_PATH_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if result.get("depth_execution_mode") == "mock_adapter_with_real_frame_alignment":
        if result.get("execution_path_status") == "pass_real_yolo_real_depth":
            issues.append("mock_depth_marked_as_real")
    return len(issues) == 0, issues


def validate_quality_report(report: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in QUALITY_REPORT_FIELDS if f not in report]
    if report.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if report.get("mock_depth_marked_as_real") is True:
        issues.append("mock_depth_marked_as_real")
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
