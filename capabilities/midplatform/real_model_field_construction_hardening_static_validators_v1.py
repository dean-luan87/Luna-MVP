# -*- coding: utf-8 -*-
"""Real model field construction hardening static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_model_field_construction_hardening_types_v1 import (
    HARDENED_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
    QUALITY_ASSESSMENT_FIELDS,
    REUSABLE_CASE_FIELDS,
)


def validate_hardened_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in HARDENED_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_quality_assessment(assessment: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in QUALITY_ASSESSMENT_FIELDS if f not in assessment]
    if assessment.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_reusable_case(case: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in REUSABLE_CASE_FIELDS if f not in case]
    if case.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
