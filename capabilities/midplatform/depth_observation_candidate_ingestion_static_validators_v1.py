# -*- coding: utf-8 -*-
"""Depth observation candidate ingestion static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_observation_candidate_ingestion_types_v1 import (
    DEPTH_INGESTION_RESULT_FIELDS,
    DEPTH_MODEL_OUTPUT_MOCK_FIELDS,
    DEPTH_OBSERVATION_CANDIDATE_FIELDS,
    DEPTH_RELIABILITY_POLICY_FIELDS,
    DEPTH_SAMPLING_POLICY_FIELDS,
    DRYRUN_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
    OBJECT_DEPTH_HINT_CANDIDATE_FIELDS,
)


def validate_depth_model_output_mock(output: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DEPTH_MODEL_OUTPUT_MOCK_FIELDS if f not in output]
    if output.get("source_type") != "model_depth_estimator":
        issues.append("source_type_not_model_depth_estimator")
    if output.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_depth_observation_candidate(obs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DEPTH_OBSERVATION_CANDIDATE_FIELDS if f not in obs]
    if obs.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if obs.get("depth_error_expected") is not True:
        issues.append("depth_error_expected_required")
    if obs.get("depth_source") == "hardware":
        issues.append("no_hardware_depth_fact")
    return len(issues) == 0, issues


def validate_object_depth_hint_candidate(hint: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_DEPTH_HINT_CANDIDATE_FIELDS if f not in hint]
    if hint.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if hint.get("depth_error_expected") is not True:
        issues.append("depth_error_expected_required")
    if hint.get("depth_source") == "hardware":
        issues.append("no_hardware_depth_fact")
    return len(issues) == 0, issues


def validate_depth_ingestion_result_candidate(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DEPTH_INGESTION_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    flags = result.get("non_execution_flags") or {}
    if flags.get("no_hardware_depth_fact") is not True:
        issues.append("no_hardware_depth_fact_flag_required")
    return len(issues) == 0, issues


def validate_depth_sampling_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DEPTH_SAMPLING_POLICY_FIELDS if f not in policy]
    return len(issues) == 0, issues


def validate_depth_reliability_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DEPTH_RELIABILITY_POLICY_FIELDS if f not in policy]
    if policy.get("estimated_depth_error_expected") is not True:
        issues.append("estimated_depth_error_expected_required")
    if policy.get("no_hardware_fact") is not True:
        issues.append("no_hardware_fact_required")
    return len(issues) == 0, issues


def validate_depth_fallback_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if "when_depth_missing" not in policy:
        issues.append("missing_when_depth_missing")
    if "when_depth_unreliable" not in policy:
        issues.append("missing_when_depth_unreliable")
    return len(issues) == 0, issues


def validate_ingestion_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DRYRUN_RESULT_FIELDS if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
