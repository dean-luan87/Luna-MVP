# -*- coding: utf-8 -*-
"""Depth execution path bridge v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.depth_real_output_bridge_v1 import run_or_load_depth_output


def execute_or_load_depth_output_for_frame(
    *,
    frame_pkg: Dict[str, Any],
    authorization: Dict[str, Any],
    depth_mode: str = "auto",
    depth_samples: Optional[Dict[str, float]] = None,
    timestamp_override: str | None = None,
    use_stub: bool = False,
) -> Tuple[Optional[Dict[str, Any]], str, List[str], List[str]]:
    """Execute or load depth with explicit real / stub / mock / blocked / missing classification."""
    warnings: List[str] = []
    failure_points: List[str] = []
    auth = dict(authorization)

    if depth_mode == "missing":
        warnings.append("depth_missing_explicit")
        return None, "missing", warnings, failure_points

    if auth.get("depth_path") == "blocked":
        failure_points.append("blocked_by_authorization_depth")
        return None, "blocked_depth_authorization", warnings, failure_points

    depth_pkg, depth_warn, depth_fps = run_or_load_depth_output(
        frame_pkg=frame_pkg,
        authorization=auth,
        depth_mode=depth_mode,
        depth_samples=depth_samples,
        timestamp_override=timestamp_override,
    )
    warnings.extend(depth_warn)
    failure_points.extend(depth_fps)

    if not depth_pkg:
        return None, "missing", warnings, failure_points

    raw_mode = depth_pkg.get("execution_mode", "missing")
    model_ref = depth_pkg.get("model_ref", "")

    if raw_mode == "authorized_model":
        classified = "authorized_model"
    elif raw_mode == "real_adapter" and (use_stub or not auth.get("local_depth_adapter_available")):
        classified = "stub_depth"
        depth_pkg["execution_mode"] = "stub_depth"
        depth_pkg["depth_source_class"] = "stub"
        warnings.append("stub_depth_not_full_real_model")
    elif raw_mode == "real_adapter":
        classified = "real_adapter"
        depth_pkg["depth_source_class"] = "real_adapter"
    elif raw_mode == "mock_adapter_with_real_frame_alignment":
        classified = "mock_adapter_with_real_frame_alignment"
        depth_pkg["depth_source_class"] = "mock"
        warnings.append("mock_depth_not_real_metric")
    else:
        classified = raw_mode
    depth_pkg["execution_mode"] = classified
    return depth_pkg, classified, warnings, failure_points
