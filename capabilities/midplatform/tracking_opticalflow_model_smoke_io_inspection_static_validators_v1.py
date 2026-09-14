# -*- coding: utf-8 -*-
"""Tracking / Optical Flow model smoke IO inspection static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_types_v1 import (
    EXECUTION_MODES,
    MAPPING_FEASIBILITY_FIELDS,
    MODEL_IO_INSPECTION_FIELDS,
    MODEL_SMOKE_RUN_FIELDS,
    NON_EXECUTION_FLAGS,
)


def validate_model_smoke_run_candidate(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in MODEL_SMOKE_RUN_FIELDS:
        if f not in candidate:
            issues.append(f"missing_field:{f}")
    if candidate.get("model_role") != "tracking_optical_flow":
        issues.append("model_role_must_be_tracking_optical_flow")
    if candidate.get("execution_mode") not in EXECUTION_MODES:
        issues.append("invalid_execution_mode")
    if candidate.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    runtime = candidate.get("runtime_environment_summary") or {}
    if runtime.get("download_attempted") or runtime.get("dependency_install_attempted"):
        issues.append("download_or_install_not_allowed")
    return len(issues) == 0, issues


def validate_model_io_inspection_candidate(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MODEL_IO_INSPECTION_FIELDS if f not in candidate]
    if candidate.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_mapping_feasibility_candidate(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in MAPPING_FEASIBILITY_FIELDS if f not in candidate]
    if candidate.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if candidate.get("model_role") != "tracking_optical_flow":
        issues.append("model_role_must_be_tracking_optical_flow")
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    required = (
        "no_field_simulation", "no_adapter_skeleton_yet", "no_world_model_assembly",
        "no_unauthorized_download", "no_camera_runtime", "no_production_runtime",
    )
    issues = [k for k in required if flags.get(k) is not True]
    return len(issues) == 0, issues


def validate_no_protocol_overreach(new_protocol_count: int) -> Tuple[bool, List[str]]:
    return new_protocol_count == 0, (["new_protocol_without_owner_approval"] if new_protocol_count else [])
