# -*- coding: utf-8 -*-
"""Real observation candidate ingestion static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_observation_candidate_ingestion_types_v1 import (
    DETECTOR_OUTPUT_MOCK_FIELDS,
    DRYRUN_RESULT_FIELDS,
    INGESTION_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
    NORMALIZED_DETECTION_FIELDS,
    OBJECT_OBSERVATION_CANDIDATE_FIELDS,
)


def validate_detector_output_mock(output: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DETECTOR_OUTPUT_MOCK_FIELDS if f not in output]
    if output.get("source_type") != "model_detector":
        issues.append("source_type_not_model_detector")
    return len(issues) == 0, issues


def validate_normalized_detection_candidate(det: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in NORMALIZED_DETECTION_FIELDS if f not in det]
    if det.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_object_observation_candidate(obs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in OBJECT_OBSERVATION_CANDIDATE_FIELDS if f not in obs]
    if obs.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if obs.get("tracker_id_is_hint_not_fact") is not True:
        issues.append("tracker_id_is_hint_not_fact_required")
    if obs.get("source_type") != "model_detector":
        issues.append("source_type_not_model_detector")
    return len(issues) == 0, issues


def validate_ingestion_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in INGESTION_RESULT_FIELDS if f not in result]
    flags = result.get("non_execution_flags") or {}
    if flags.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_depth_missing_fallback(obs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if obs.get("depth_source") == "unknown" and obs.get("depth_error_expected") is not True:
        issues.append("unknown_depth_must_mark_error_expected")
    if obs.get("depth_source") == "estimated" and obs.get("depth_error_expected") is not True:
        issues.append("estimated_depth_must_mark_error_expected")
    return len(issues) == 0, issues


def validate_ingestion_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DRYRUN_RESULT_FIELDS if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
