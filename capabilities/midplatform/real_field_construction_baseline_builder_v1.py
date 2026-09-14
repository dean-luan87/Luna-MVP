# -*- coding: utf-8 -*-
"""Real field construction baseline builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List


def _baseline_type(exec_result: Dict[str, Any]) -> str:
    ym = exec_result.get("yolo_execution_mode", "")
    dm = exec_result.get("depth_execution_mode", "")
    status = exec_result.get("execution_status", "")

    if status in ("failed_no_detection", "failed_field_assembly"):
        return "failure_localization_baseline"
    if "invalid_bbox" in " ".join(exec_result.get("failure_points") or []):
        return "failure_localization_baseline"
    if dm in ("missing", "blocked_depth_authorization"):
        return "missing_depth_fallback_baseline"
    if ym == "real_runner" and dm == "real_adapter":
        return "real_yolo_real_depth_baseline"
    if ym == "real_runner" and dm in ("stub_depth", "real_adapter_stub"):
        return "real_yolo_stub_depth_baseline"
    if ym == "cached_output" and dm == "real_adapter":
        return "cached_yolo_real_depth_baseline"
    if dm == "mock_adapter_with_real_frame_alignment":
        return "cached_yolo_mock_depth_degraded_baseline"
    return "cached_yolo_mock_depth_degraded_baseline"


def _limitations(baseline_type: str, exec_result: Dict[str, Any]) -> List[str]:
    lim: List[str] = []
    if baseline_type == "real_yolo_stub_depth_baseline":
        lim.append("stub_depth_not_full_real_model")
    if baseline_type == "cached_yolo_mock_depth_degraded_baseline":
        lim.extend(["mock_depth_not_real", "cached_yolo_not_live_runner"])
    if baseline_type == "missing_depth_fallback_baseline":
        lim.append("geometry_unknown_without_depth")
    if baseline_type == "failure_localization_baseline":
        lim.append("not_success_baseline")
    if exec_result.get("yolo_execution_mode") == "cached_output":
        lim.append("yolo_cached_output_fallback")
    return sorted(set(lim))


def build_real_field_construction_baselines(
    *,
    execution_results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Build reusable baseline candidates from execution path results."""
    baselines: List[Dict[str, Any]] = []
    for r in execution_results:
        bt = _baseline_type(r)
        quality = "strong" if bt == "real_yolo_real_depth_baseline" else (
            "degraded" if "degraded" in bt or "stub" in bt or "mock" in bt or "missing" in bt else "failed"
        )
        baselines.append({
            "baseline_id": f"bl_{uuid.uuid4().hex[:12]}",
            "source_execution_result_ref": r.get("execution_path_result_id"),
            "baseline_type": bt,
            "input_frame_ref": r.get("frame_input_ref"),
            "enhanced_field_scene_ref": r.get("enhanced_field_scene_ref"),
            "quality_status": quality,
            "limitations": _limitations(bt, r),
            "reusable_for": (
                "real_field_quality_evaluation" if quality != "failed"
                else "failure_localization_regression"
            ),
            "required_execution_mode": {
                "yolo": r.get("yolo_execution_mode"),
                "depth": r.get("depth_execution_mode"),
            },
            "candidate_only": True,
        })
    return baselines
