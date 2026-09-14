# -*- coding: utf-8 -*-
"""YOLO execution path bridge v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.yolo_real_output_bridge_v1 import run_or_load_yolo_real_output


def execute_or_load_yolo_output_for_frame(
    *,
    frame_pkg: Dict[str, Any],
    authorization: Dict[str, Any],
    cached_detections: Optional[List[Dict[str, Any]]] = None,
    prefer_real_runner: bool = False,
) -> Tuple[Dict[str, Any], str, List[str], List[str]]:
    """Execute or load YOLO output with explicit execution_mode classification."""
    auth = dict(authorization)
    if prefer_real_runner and auth.get("yolo_local_runner_available"):
        auth["yolo_path"] = "real_runner"
    elif not auth.get("yolo_local_runner_available"):
        auth["yolo_path"] = "cached_output"

    yolo_pkg, warnings, failure_points = run_or_load_yolo_real_output(
        frame_pkg=frame_pkg,
        authorization=auth,
        cached_detections=cached_detections,
    )
    if not yolo_pkg:
        return {}, "blocked_yolo_runner_missing", warnings, failure_points + ["blocked_yolo_runner_missing"]

    mode = yolo_pkg.get("execution_mode", "cached_output")
    if mode == "real_runner":
        classified = "real_runner"
    else:
        classified = "cached_output"
        if mode != "cached_output":
            warnings.append("yolo_execution_mode_normalized_to_cached_output")
    yolo_pkg["execution_mode"] = classified
    return yolo_pkg, classified, warnings, failure_points
