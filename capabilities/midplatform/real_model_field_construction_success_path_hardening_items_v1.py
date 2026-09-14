# -*- coding: utf-8 -*-
"""Real Model Field Construction Success Path Hardening — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Simulation-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Field Simulation Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_yolo_rerun", "real_depth_rerun", "model_download", "weight_download",
        "large_dependency_install", "real_camera_read", "real_video_stream",
        "production_runtime", "field_simulation", "task_reasoning", "world_model_entry",
        "memory_candidate", "integration_test", "candidate_lifecycle_manager",
        "module_handoff_contract",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "hardening_not_production_runtime",
    "hardening_not_field_simulation",
    "reusable_case_not_world_model_fact",
    "quality_assessment_not_task_execution",
)

HARDENING_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "harden_real_yolo_real_depth_success",
        "source_case_id": "real_image_yolo_with_depth_available",
        "case_category": "pass",
        "expected_success_path_status": "pass_real_yolo_real_depth",
        "expect_real_adapter": True,
        "expect_entity_count": 1,
        "repeatability_notes": "local_depth_adapter_stub_stable_success_baseline",
    },
    {
        "case_id": "harden_real_yolo_mock_depth_degraded_success",
        "source_case_id": "real_image_yolo_depth_mock_alignment",
        "case_category": "pass",
        "expected_success_path_status": "pass_real_yolo_mock_depth_alignment",
        "expect_mock_depth": True,
        "expect_entity_count": 1,
    },
    {
        "case_id": "harden_missing_depth_fallback",
        "source_case_id": "real_image_yolo_no_depth_fallback",
        "case_category": "degraded",
        "expected_success_path_status": "degraded_missing_depth",
        "expect_entity_count": 1,
        "expect_geometry_unknown": True,
    },
    {
        "case_id": "harden_multiple_objects_zone_summary",
        "source_case_id": "real_image_multiple_objects_field_assembly",
        "case_category": "pass",
        "allow_status_family": "pass_real_yolo",
        "expected_success_path_status": "pass_real_yolo_mock_depth_alignment",
        "expect_entity_count": 3,
        "expect_zone_summary": True,
    },
    {
        "case_id": "harden_invalid_bbox_failure_localization",
        "source_case_id": "real_image_invalid_bbox_handling",
        "case_category": "failure",
        "expect_localization_area": "yolo_output_bridge",
        "expect_invalid_bbox_localized": True,
    },
    {
        "case_id": "harden_no_detection_graceful_fail",
        "source_case_id": "real_image_no_detection_graceful_fail",
        "case_category": "failure",
        "expected_success_path_status": "failed_no_yolo_detection",
        "expect_localization_area": "yolo_output_bridge",
    },
    {
        "case_id": "harden_timestamp_mismatch_degraded",
        "source_case_id": "timestamp_mismatch_degraded",
        "case_category": "degraded",
        "allow_status_family": "pass_real_yolo",
        "expect_localization_area": "multi_model_alignment",
    },
    {
        "case_id": "harden_traceability_full_chain",
        "source_case_id": "traceability_preserved_full_chain",
        "case_category": "pass",
        "expected_success_path_status": "pass_real_yolo_real_depth",
        "expect_traceability_min": 6,
    },
    {
        "case_id": "harden_depth_confidence_degradation",
        "source_case_id": "real_image_yolo_depth_mock_alignment",
        "case_category": "degraded",
        "expected_success_path_status": "pass_real_yolo_mock_depth_alignment",
        "expect_mock_depth": True,
        "optional_meta": True,
    },
    {
        "case_id": "harden_quality_summary_completeness",
        "source_case_id": "real_image_yolo_with_depth_available",
        "case_category": "quality_meta",
        "expect_quality_summaries": True,
        "optional_meta": True,
    },
)

FIXTURE_REUSE_POLICY: Dict[str, Any] = {
    "policy_id": "fixture_reuse_policy_v1",
    "reuse_upstream_dryrun_artifacts": True,
    "no_real_model_rerun": True,
    "no_camera_dependency": True,
    "baseline_case_refs_from": "reusable_field_construction_case_registry_v1",
}
