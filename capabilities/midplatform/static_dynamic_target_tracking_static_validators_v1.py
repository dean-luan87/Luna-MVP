# -*- coding: utf-8 -*-
"""Static/Dynamic target tracking static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.static_dynamic_target_locking_tracking_types_v1 import (
    DYNAMIC_TRACK_FIELDS,
    IMPACT_FIELDS,
    NON_EXECUTION_FLAGS,
    PLAN_FIELDS,
    STATIC_LOCK_FIELDS,
)


def validate_static_target_lock_candidate(lock: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in STATIC_LOCK_FIELDS if f not in lock]
    if lock.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_dynamic_target_track_candidate(track: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DYNAMIC_TRACK_FIELDS if f not in track]
    if track.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if track.get("tracker_id_is_hint_not_fact") is not True:
        issues.append("tracker_id_is_hint_not_fact_required")
    return len(issues) == 0, issues


def validate_target_impact_candidate(impact: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in IMPACT_FIELDS if f not in impact]
    if impact.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_target_tracking_plan_candidate(plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in PLAN_FIELDS if f not in plan]
    flags = plan.get("non_execution_flags") or {}
    if flags.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_dryrun_result_candidate(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    required = (
        "case_id", "expected_static_lock_count", "actual_static_lock_count",
        "expected_dynamic_track_count", "actual_dynamic_track_count",
        "expected_task_impact_hints", "actual_task_impact_hints",
        "prohibited_behavior_absent", "case_passed", "reason_codes",
    )
    issues = [f"missing_{f}" for f in required if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
