# -*- coding: utf-8 -*-
"""Controlled real dryrun static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.yolo_depth_controlled_real_dryrun_types_v1 import (
    NON_EXECUTION_FLAGS,
    REAL_DRYRUN_RESULT_FIELDS,
)


def validate_real_dryrun_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in REAL_DRYRUN_RESULT_FIELDS if f not in result]
    if result.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    flags = result.get("non_execution_flags") or {}
    for k in ("no_unauthorized_download", "no_camera_runtime", "no_video_stream_runtime"):
        if flags.get(k) is not True and NON_EXECUTION_FLAGS.get(k):
            issues.append(f"flag_{k}")
    depth_pkg_mode = (result.get("execution_boundary_summary") or {}).get("depth_execution_mode")
    if depth_pkg_mode == "mock_adapter_with_real_frame_alignment":
        if result.get("success_path_status") == "pass_real_yolo_real_depth":
            issues.append("mock_depth_not_marked_as_real")
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, bool]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
