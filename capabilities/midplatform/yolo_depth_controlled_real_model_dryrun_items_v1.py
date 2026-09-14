# -*- coding: utf-8 -*-
"""YOLO + Depth Controlled Real Model DryRun — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Real-Model-Field-Construction-Success-Path-Hardening-v1-001"
SELECTED_NEXT_ROUTE = "Real Model Field Construction Success Path Hardening"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "unauthorized_model_download", "unauthorized_weight_download", "large_dependency_install",
        "real_camera_read", "real_video_stream", "production_runtime", "field_simulation",
        "task_reasoning", "world_model_entry", "memory_candidate", "integration_test",
        "candidate_lifecycle_manager", "module_handoff_contract",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "controlled_dryrun_not_production_runtime",
    "mock_depth_not_real_depth_model",
    "dryrun_result_not_world_model_fact",
    "cached_yolo_not_live_video_stream",
)

DEFAULT_AUTHORIZATION: Dict[str, Any] = {
    "matrix_id": "real_model_execution_authorization_matrix_v1",
    "yolo_path": "cached_output",
    "yolo_local_runner_available": False,
    "yolo_model_ref": "yolo_integrated_cached",
    "depth_path": "mock_adapter_with_real_frame_alignment",
    "local_depth_adapter_available": False,
    "depth_model_download_authorized": False,
    "depth_anything_v2_authorized": False,
    "unidepth_v2_authorized": False,
    "no_unauthorized_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
}

FRAME_DEFAULTS: Dict[str, Any] = {
    "frame_width": 640,
    "frame_height": 480,
    "timestamp": "2026-06-11T10:00:00Z",
    "source_ref": "controlled_dryrun_fixture_v1",
}

CONTROLLED_DRYRUN_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "real_image_yolo_with_depth_available",
        "description": "Real image + YOLO + local depth adapter stub",
        "frame_ref": "frame_depth_avail_001",
        "detections": [
            {"bbox_xyxy": {"x1": 100, "y1": 50, "x2": 200, "y2": 300}, "label": "person", "confidence": 0.92},
        ],
        "depth_mode": "local_adapter",
        "depth_samples": {"150_175": 2.0},
        "expect_scene": True,
        "expect_status_prefix": "pass_real_yolo",
        "expect_objects_min": 1,
        "expect_aligned_min": 1,
    },
    {
        "case_id": "real_image_yolo_depth_mock_alignment",
        "description": "Real image + YOLO + mock depth with frame alignment",
        "frame_ref": "frame_mock_depth_002",
        "detections": [
            {"bbox_xyxy": {"x1": 120, "y1": 60, "x2": 220, "y2": 280}, "label": "chair", "confidence": 0.85},
        ],
        "depth_mode": "mock",
        "depth_samples": {"170_170": 3.5},
        "expect_scene": True,
        "expect_status": "pass_real_yolo_mock_depth_alignment",
        "expect_objects_min": 1,
    },
    {
        "case_id": "real_image_yolo_no_depth_fallback",
        "description": "YOLO output with depth missing — object retained, geometry unknown",
        "frame_ref": "frame_no_depth_003",
        "detections": [
            {"bbox_xyxy": {"x1": 80, "y1": 40, "x2": 180, "y2": 260}, "label": "table", "confidence": 0.78},
        ],
        "depth_mode": "missing",
        "expect_scene": True,
        "expect_status": "degraded_missing_depth",
        "expect_objects_min": 1,
        "expect_geometry_unknown": True,
    },
    {
        "case_id": "real_image_multiple_objects_field_assembly",
        "description": "Multiple YOLO detections → multiple entities + zone summary",
        "frame_ref": "frame_multi_004",
        "detections": [
            {"bbox_xyxy": {"x1": 50, "y1": 30, "x2": 150, "y2": 200}, "label": "person", "confidence": 0.9},
            {"bbox_xyxy": {"x1": 250, "y1": 80, "x2": 350, "y2": 280}, "label": "chair", "confidence": 0.82},
            {"bbox_xyxy": {"x1": 400, "y1": 100, "x2": 500, "y2": 350}, "label": "door", "confidence": 0.75},
        ],
        "depth_mode": "mock",
        "depth_samples": {"100_115": 1.8, "300_180": 5.0, "450_225": 8.0},
        "expect_scene": True,
        "expect_entities_min": 3,
        "expect_zone_summary": True,
    },
    {
        "case_id": "real_image_invalid_bbox_handling",
        "description": "Invalid bbox rejected, dryrun continues with valid detection",
        "frame_ref": "frame_invalid_bbox_005",
        "detections": [
            {"bbox_xyxy": {"x1": 100, "y1": 50, "x2": 200, "y2": 300}, "label": "cup", "confidence": 0.88},
            {"bbox_xyxy": {"x1": 500, "y1": 400, "x2": 100, "y2": 100}, "label": "bad", "confidence": 0.5},
        ],
        "depth_mode": "mock",
        "depth_samples": {"150_175": 2.5},
        "expect_scene": True,
        "expect_invalid_bbox_warning": True,
        "expect_objects_min": 1,
        "expect_objects_max": 1,
    },
    {
        "case_id": "real_image_no_detection_graceful_fail",
        "description": "No YOLO detections — graceful failure_points, no crash",
        "frame_ref": "frame_no_det_006",
        "detections": [],
        "depth_mode": "mock",
        "expect_scene": False,
        "expect_status": "failed_no_yolo_detection",
        "expect_failure_points": True,
    },
    {
        "case_id": "timestamp_mismatch_degraded",
        "description": "YOLO / depth timestamp mismatch → alignment degraded",
        "frame_ref": "frame_ts_mismatch_007",
        "detections": [
            {"bbox_xyxy": {"x1": 110, "y1": 55, "x2": 210, "y2": 290}, "label": "box", "confidence": 0.8},
        ],
        "depth_mode": "mock",
        "depth_timestamp": "2026-06-11T10:00:01Z",
        "depth_samples": {"160_172": 2.2},
        "expect_scene": True,
        "expect_ts_degraded": True,
    },
    {
        "case_id": "traceability_preserved_full_chain",
        "description": "frame_ref / model_ref / raw_output_ref / candidate refs preserved",
        "frame_ref": "frame_trace_008",
        "detections": [
            {"bbox_xyxy": {"x1": 130, "y1": 70, "x2": 230, "y2": 310}, "label": "sign", "confidence": 0.91},
        ],
        "depth_mode": "local_adapter",
        "depth_samples": {"180_190": 2.0},
        "expect_scene": True,
        "expect_traceability_min": 4,
    },
)

PIPELINE_MODULES_REUSED: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_alignment_core_v1.py",
    "capabilities/midplatform/depth_object_fusion_core_v1.py",
    "capabilities/midplatform/field_geometry_candidate_core_v1.py",
    "capabilities/midplatform/field_assembly_core_v1.py",
)
