# -*- coding: utf-8 -*-
"""Model workflow protocol reuse and cleanup review — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Model-Adapter-Priority-Sequence-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Model Adapter Priority Sequence Planning"
DEFERRED_PHASES = (
    "Phase-Midplatform-Field-Simulation-Planning-v1-001",
    "Phase-Midplatform-Field-Simulation-Skeleton-v1-001",
    "Phase-Midplatform-Task-Reasoning-Planning-v1-001",
    "Phase-Midplatform-Model-Role-Registry-And-Collaboration-Workflow-Planning-v1-001",
)

OWNER_CONSTRAINTS: Dict[str, Any] = {
    "constraints_id": "owner_model_workflow_constraints_v1",
    "no_simulation_test": True,
    "no_field_simulation_mainline": True,
    "no_new_protocol_without_reason": True,
    "must_reuse_existing_protocols": True,
    "no_self_expansion_without_owner_approval": True,
    "dual_track_active": ("world_model_construction", "task_collaboration_under_midplatform"),
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_task_action_output": True,
}

ACTIVE_MAINLINE_PATTERNS: Tuple[str, ...] = (
    "multi_model_alignment",
    "depth_object_fusion",
    "field_geometry",
    "field_assembly",
    "enhanced_field_scene",
    "yolo_depth",
    "yolo_real_output",
    "depth_real_output",
    "real_frame_input",
    "real_model_field_construction",
    "real_model_execution_path",
    "yolo_execution_path",
    "depth_execution_path",
    "real_image_set",
    "real_model_execution_authorization",
    "real_field_construction_quality",
    "real_field_construction_baseline",
    "field_construction_quality",
    "field_construction_failure",
    "field_construction_reusable",
    "field_first_common_validation",
)

REJECT_FROM_MAINLINE_PATTERNS: Tuple[str, ...] = (
    "field_simulation",
    "simulation_eligibility",
)

DEFERRED_PATTERNS: Tuple[str, ...] = (
    "task_reasoning",
)

KEEP_AS_REFERENCE_PATTERNS: Tuple[str, ...] = (
    "field_simulation_planning",
    "field_simulation_skeleton",
)

PROTOCOL_OVERREACH_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "artifact_id": "field_simulation_input_output_contract",
        "path_hint": "field_simulation_planning",
        "verdict": "protocol_overreach",
        "reason": "simulation_contract_duplicates_candidate_layer_without_owner_approval",
        "reuse_existing": "enhanced_field_scene_candidate + field_quality_summary",
    },
    {
        "artifact_id": "field_simulation_plan_candidate_contract",
        "path_hint": "field_simulation_planning",
        "verdict": "protocol_overreach",
        "reason": "simulation_plan_contract_not_on_active_mainline",
        "reuse_existing": "field_assembly_result_candidate",
    },
    {
        "artifact_id": "model_role_registry_before_cleanup",
        "path_hint": "model_role_registry",
        "verdict": "deferred_pending_cleanup",
        "reason": "must_not_proceed_before_protocol_reuse_review",
        "reuse_existing": "multi_model_role_registry from planning artifacts",
    },
)

REVIEW_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "owner_constraints_loaded", "check": "owner_constraints"},
    {"case_id": "field_simulation_deactivated", "check": "field_simulation_reject"},
    {"case_id": "task_reasoning_deferred", "check": "task_reasoning_deferred"},
    {"case_id": "active_mainline_preserved", "check": "active_mainline"},
    {"case_id": "real_model_path_active", "check": "real_model_active"},
    {"case_id": "yolo_depth_chain_active", "check": "yolo_depth_active"},
    {"case_id": "protocol_reuse_review", "check": "protocol_reuse"},
    {"case_id": "protocol_overreach_flagged", "check": "protocol_overreach"},
    {"case_id": "no_simulation_next_phase", "check": "no_sim_next"},
    {"case_id": "no_task_reasoning_next_phase", "check": "no_task_next"},
    {"case_id": "world_model_candidate_scope", "check": "wm_candidate_scope"},
    {"case_id": "task_collaboration_scope", "check": "task_collab_scope"},
    {"case_id": "next_phase_recommendation", "check": "next_phase"},
    {"case_id": "deprecated_registry_nonempty", "check": "deprecated_registry"},
    {"case_id": "cleanup_required_registry", "check": "cleanup_registry"},
)

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_simulation_execution", "simulation_test_route", "task_reasoning_execution",
        "new_protocol_without_reason", "world_model_entry_write", "fact_admission",
        "task_action_output", "model_runtime", "unauthorized_model_download",
        "camera_runtime", "video_stream_runtime", "production_runtime",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "cleanup_review_not_new_model_capability",
    "deprecated_simulation_not_deleted_without_owner_approval",
    "active_mainline_includes_real_field_construction_not_simulation",
    "world_model_candidate_not_world_model_entry",
)

MODEL_ADAPTER_PRIORITY_RECOMMENDATION: Tuple[str, ...] = (
    "SLAM_Spatial_Mapping",
    "Tracking",
    "OCR",
    "Segmentation",
    "Scene_Graph",
)
