# -*- coding: utf-8 -*-
"""Trajectory analysis static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.trajectory_analysis_task_impact_types_v1 import (
    ANALYSIS_RESULT_FIELDS,
    MISSING_INFO_FIELDS,
    NON_EXECUTION_FLAGS,
    RISK_PROJECTION_FIELDS,
    TASK_IMPACT_ANALYSIS_FIELDS,
    TRAJECTORY_FIELDS,
)


def validate_trajectory_candidate(traj: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TRAJECTORY_FIELDS if f not in traj]
    if traj.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if traj.get("tracker_id_is_hint_not_fact") is not True:
        issues.append("tracker_id_is_hint_not_fact_required")
    return len(issues) == 0, issues


def validate_task_impact_analysis_candidate(impact: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in TASK_IMPACT_ANALYSIS_FIELDS if f not in impact]
    if impact.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_risk_projection_candidate(risk: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in RISK_PROJECTION_FIELDS if f not in risk]
    if risk.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_missing_information_candidate(missing: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MISSING_INFO_FIELDS if f not in missing]
    if missing.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_analysis_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ANALYSIS_RESULT_FIELDS if f not in result]
    flags = result.get("non_execution_flags") or {}
    if flags.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if flags.get("no_final_action_output") is not True:
        issues.append("no_final_action_output_required")
    return len(issues) == 0, issues


def validate_trajectory_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    required = (
        "case_id", "expected_trajectory_count", "actual_trajectory_count",
        "expected_task_impact_count", "actual_task_impact_count",
        "prohibited_behavior_absent", "case_passed", "reason_codes",
    )
    issues = [f"missing_{f}" for f in required if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
