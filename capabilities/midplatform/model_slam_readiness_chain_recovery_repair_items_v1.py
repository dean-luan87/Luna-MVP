# -*- coding: utf-8 -*-
"""Model-SLAM readiness chain recovery repair — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Model-SLAM-Readiness-Chain-Recovery-Repair-v1-001"
SCOPE = "model_slam_readiness_chain_recovery_repair_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "model_slam_readiness_chain_recovery_repair_v1_smoke_v0"
)

BATCH_DETECTION_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "model_slam_readiness_chain_batch_detection_and_recovery_plan_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

GROUP_M_STAGES: Tuple[str, ...] = (
    "model_workflow_protocol_reuse_review",
    "model_adapter_priority_sequence_planning",
    "slam_spatial_mapping_model_smoke_io_inspection",
    "slam_spatial_mapping_adapter_skeleton",
    "slam_spatial_mapping_task_collaboration_planning",
    "slam_spatial_mapping_task_collaboration_revalidation",
)

STAGE_OUTPUT_DIRS: Dict[str, str] = {
    "model_workflow_protocol_reuse_review": (
        "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
        "model_workflow_protocol_reuse_and_cleanup_review_v1_smoke_v0"
    ),
    "model_adapter_priority_sequence_planning": (
        "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
        "model_adapter_priority_sequence_planning_v1_smoke_v0"
    ),
    "slam_spatial_mapping_model_smoke_io_inspection": (
        "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
        "slam_spatial_mapping_model_smoke_io_inspection_v1_smoke_v0"
    ),
    "slam_spatial_mapping_adapter_skeleton": (
        "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
        "slam_spatial_mapping_adapter_skeleton_v1_smoke_v0"
    ),
    "slam_spatial_mapping_task_collaboration_planning": (
        "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
        "slam_spatial_mapping_task_collaboration_planning_v1_smoke_v0"
    ),
    "slam_spatial_mapping_task_collaboration_revalidation": (
        "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
        "slam_spatial_mapping_task_collaboration_planning_revalidation_v1_smoke_v0"
    ),
}

STAGE_RUNNERS: Dict[str, str] = {
    "model_workflow_protocol_reuse_review": "run_model_workflow_protocol_reuse_and_cleanup_review_v1",
    "model_adapter_priority_sequence_planning": "run_model_adapter_priority_sequence_planning_v1",
    "slam_spatial_mapping_model_smoke_io_inspection": "run_slam_spatial_mapping_model_smoke_io_inspection_v1",
    "slam_spatial_mapping_adapter_skeleton": "run_slam_spatial_mapping_adapter_skeleton_v1",
    "slam_spatial_mapping_task_collaboration_planning": "run_slam_spatial_mapping_task_collaboration_planning_v1",
    "slam_spatial_mapping_task_collaboration_revalidation": "run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1",
}

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_MODEL_SLAM_READINESS_CHAIN_RECOVERY_REPAIR_READY_FOR_SLAM_ROUTE_DECISION"
)
FINAL_DECISION_PARTIAL = (
    "MIDPLATFORM_MODEL_SLAM_READINESS_CHAIN_RECOVERY_REPAIR_PARTIAL_BLOCKED_BY_GROUP_M_CANDIDATE_GAP"
)

NEXT_PHASE_COMPLETE = "Phase-Midplatform-SLAM-Route-Decision-v1-001"
NEXT_PHASE_PARTIAL = PHASE_ID

PASS_FLAG = "group_m_recovery_repair_complete"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "model_slam_readiness_chain_recovery_repair_only": True,
    "candidate_only": True,
    "no_model_execution": True,
    "no_sensor_execution": True,
    "no_camera_execution": True,
    "no_world_model_assembly": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_protocol_change": True,
    "no_model_download": True,
    "no_fake_go_artifacts": True,
    "no_issue_review_stage_created": True,
    "no_gap_review_stage_created": True,
    "no_rerun_review_stage_created": True,
    "no_original_stage_pollution": True,
}
