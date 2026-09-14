# -*- coding: utf-8 -*-
"""Real model execution path hardening static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_model_execution_path_hardening_types_v1 import (
    AUTHORIZATION_FIELDS,
    BASELINE_FIELDS,
    EXECUTION_PATH_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
    QUALITY_REPORT_FIELDS,
)


def validate_real_model_execution_path_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in EXECUTION_PATH_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    dm = result.get("depth_execution_mode", "")
    if dm == "mock_adapter_with_real_frame_alignment" and result.get("execution_status") == "pass_real_yolo_real_depth":
        issues.append("mock_depth_marked_as_real")
    if dm == "stub_depth" and result.get("execution_status") == "pass_real_yolo_real_depth":
        issues.append("stub_depth_marked_as_full_real")
    return len(issues) == 0, issues


def validate_real_field_construction_quality_report(report: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in QUALITY_REPORT_FIELDS if f not in report]
    if report.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if report.get("mock_depth_marked_as_real") is True:
        issues.append("mock_depth_marked_as_real")
    if report.get("stub_depth_marked_as_full_real") is True:
        issues.append("stub_depth_marked_as_full_real")
    return len(issues) == 0, issues


def validate_real_field_construction_baseline(baseline: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in BASELINE_FIELDS if f not in baseline]
    if baseline.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if baseline.get("baseline_type") != "failure_localization_baseline" and not baseline.get("limitations"):
        issues.append("limitations_required_for_non_failure_baseline")
    return len(issues) == 0, issues


def validate_authorization_boundary(auth: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in AUTHORIZATION_FIELDS if f not in auth]
    if auth.get("model_download_allowed") is not False:
        issues.append("model_download_must_be_false")
    if auth.get("weight_download_allowed") is not False:
        issues.append("weight_download_must_be_false")
    if auth.get("camera_runtime_allowed") is not False:
        issues.append("camera_runtime_must_be_false")
    return len(issues) == 0, issues


def validate_no_simulation_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    required = ("no_field_simulation", "route_switched_from_simulation_to_real_content", "field_simulation_deferred")
    issues = [k for k in required if flags.get(k) is not True]
    return len(issues) == 0, issues


def validate_candidate_only_boundary(obj: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [] if obj.get("candidate_only") is True else ["candidate_only_required"]
    return len(issues) == 0, issues
