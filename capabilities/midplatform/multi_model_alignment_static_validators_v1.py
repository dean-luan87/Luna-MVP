# -*- coding: utf-8 -*-
"""Multi-Model alignment static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.multi_model_alignment_types_v1 import (
    ALIGNED_OBSERVATION_FIELDS,
    ALIGNMENT_INPUT_FIELDS,
    ALIGNMENT_RESULT_FIELDS,
    ALIGNMENT_SIGNAL_FIELDS,
    DRYRUN_RESULT_FIELDS,
    NON_EXECUTION_FLAGS,
)


def validate_alignment_input_package(pkg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ALIGNMENT_INPUT_FIELDS if f not in pkg]
    return len(issues) == 0, issues


def validate_alignment_signal_result(signal: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ALIGNMENT_SIGNAL_FIELDS if f not in signal]
    if "alignment_status" not in signal:
        issues.append("missing_alignment_status")
    return len(issues) == 0, issues


def validate_aligned_observation_candidate(cand: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ALIGNED_OBSERVATION_FIELDS if f not in cand]
    if cand.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_alignment_result_candidate(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in ALIGNMENT_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    flags = result.get("non_execution_flags") or {}
    if flags.get("no_depth_object_fusion") is not True:
        issues.append("no_depth_object_fusion_flag_required")
    return len(issues) == 0, issues


def validate_alignment_dryrun_result(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DRYRUN_RESULT_FIELDS if f not in res]
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
