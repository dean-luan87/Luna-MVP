# -*- coding: utf-8 -*-
"""Field simulation static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_simulation_types_v1 import (
    ELIGIBILITY_FIELDS,
    INPUT_VIEW_FIELDS,
    NON_EXECUTION_FLAGS,
    PLAN_FIELDS,
    READINESS_FIELDS,
    SIMULATION_CANDIDATE_FIELDS,
)


def validate_field_simulation_input_view(view: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in INPUT_VIEW_FIELDS if f not in view]
    if view.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_simulation_eligibility_candidate(elig: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ELIGIBILITY_FIELDS if f not in elig]
    if elig.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_field_simulation_plan_candidate(plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in PLAN_FIELDS if f not in plan]
    if plan.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_field_simulation_candidate(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in SIMULATION_CANDIDATE_FIELDS if f not in candidate]
    if candidate.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if candidate.get("no_action_output") is not True:
        issues.append("no_action_output_required")
    if candidate.get("no_fact_output") is not True:
        issues.append("no_fact_output_required")
    return len(issues) == 0, issues


def validate_field_simulation_readiness_candidate(readiness: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in READINESS_FIELDS if f not in readiness]
    if readiness.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_no_action_no_fact_boundary(candidates: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for c in candidates:
        if c.get("no_action_output") is not True:
            issues.append(f"action_output_{c.get('simulation_candidate_id')}")
        if c.get("no_fact_output") is not True:
            issues.append(f"fact_output_{c.get('simulation_candidate_id')}")
        for forbidden in ("navigation_action", "action_recommendation", "world_model_entry"):
            if forbidden in str(c).lower():
                issues.append(f"forbidden_{forbidden}")
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
