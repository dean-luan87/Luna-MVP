# -*- coding: utf-8 -*-
"""Field construction reusable case builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

PASS_STATUSES = frozenset({
    "pass_real_yolo_real_depth",
    "pass_real_yolo_mock_depth_alignment",
    "pass_real_yolo_depth_fallback",
})
DEGRADED_STATUSES = frozenset({
    "degraded_missing_depth",
    "degraded_low_depth_confidence",
})
FAILED_STATUSES = frozenset({
    "failed_no_yolo_detection",
    "failed_alignment",
    "failed_field_assembly",
    "blocked_by_authorization",
})


def build_reusable_field_construction_case(
    *,
    hardening_case_id: str,
    source_case_id: str,
    dryrun_result: Dict[str, Any],
    quality_assessment: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Build ReusableFieldConstructionCaseCandidate per hardening rules."""
    status = dryrun_result.get("success_path_status", "unknown")
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    exec_boundary = dryrun_result.get("execution_boundary_summary") or {}

    failure_points = list(dryrun_result.get("failure_points") or [])
    if any("invalid_bbox" in fp for fp in failure_points):
        return {
            "reusable_case_id": f"rfc_{uuid.uuid4().hex[:10]}",
            "source_case_id": source_case_id,
            "frame_input_ref": dryrun_result.get("frame_input_ref"),
            "yolo_output_ref": dryrun_result.get("yolo_output_ref"),
            "depth_output_ref": dryrun_result.get("depth_output_ref"),
            "enhanced_field_scene_ref": scene.get("field_scene_id"),
            "case_type": "failure_localization_baseline",
            "reusable_for": ["adapter_validation", "regression_test"],
            "limitations": ["invalid_bbox_rejected", "not_success_baseline"],
            "required_authorization": {
                "yolo_path": exec_boundary.get("yolo_execution_mode", "cached_output"),
                "depth_path": exec_boundary.get("depth_path", "mock_adapter_with_real_frame_alignment"),
                "no_real_model_rerun": True,
            },
            "hardening_case_id": hardening_case_id,
            "candidate_only": True,
        }

    if status in PASS_STATUSES and not any("invalid_bbox" in fp for fp in failure_points):
        case_type = "success_baseline"
        reusable_for = ["core_success_path", "regression_test", "adapter_validation"]
        limitations: List[str] = []
        if status == "pass_real_yolo_mock_depth_alignment":
            limitations.append("mock_depth_not_real_metric_depth")
            reusable_for.append("field_simulation_planning")
        elif status == "pass_real_yolo_real_depth":
            reusable_for.extend(["field_simulation_planning", "task_reasoning_planning"])
        if "image_path_materialized" in " ".join(dryrun_result.get("failure_points") or []):
            limitations.append("minimal_fixture_image_not_production_frame")
    elif status in DEGRADED_STATUSES:
        case_type = "degraded_baseline"
        reusable_for = ["core_success_path", "regression_test"]
        limitations = [status, "geometry_may_be_unknown"]
        if status == "degraded_missing_depth":
            limitations.append("depth_output_missing")
    elif status in FAILED_STATUSES or "invalid_bbox" in hardening_case_id:
        case_type = "failure_localization_baseline"
        reusable_for = ["adapter_validation", "regression_test"]
        limitations = [status, "not_success_baseline"]
    else:
        case_type = "observational_baseline"
        reusable_for = ["regression_test"]
        limitations = [status]

    if quality_assessment.get("quality_score_discrete") == "blocked":
        reusable_for = [r for r in reusable_for if r != "core_success_path"]

    return {
        "reusable_case_id": f"rfc_{uuid.uuid4().hex[:10]}",
        "source_case_id": source_case_id,
        "frame_input_ref": dryrun_result.get("frame_input_ref"),
        "yolo_output_ref": dryrun_result.get("yolo_output_ref"),
        "depth_output_ref": dryrun_result.get("depth_output_ref"),
        "enhanced_field_scene_ref": scene.get("field_scene_id"),
        "case_type": case_type,
        "reusable_for": reusable_for,
        "limitations": limitations,
        "required_authorization": {
            "yolo_path": exec_boundary.get("yolo_execution_mode", "cached_output"),
            "depth_path": exec_boundary.get("depth_path", "mock_adapter_with_real_frame_alignment"),
            "no_real_model_rerun": True,
        },
        "hardening_case_id": hardening_case_id,
        "candidate_only": True,
    }
