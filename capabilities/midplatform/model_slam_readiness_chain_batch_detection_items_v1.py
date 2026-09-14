# -*- coding: utf-8 -*-
"""Model-SLAM readiness chain batch detection — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Model-SLAM-Readiness-Chain-Batch-Detection-And-Recovery-Plan-v1-001"
SCOPE = "model_slam_readiness_chain_batch_detection_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "model_slam_readiness_chain_batch_detection_and_recovery_plan_v1_smoke_v0"
)

GOVERNANCE_REPAIR_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "governance_gate_integrated_implementation_repair_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

FIRST_FAILED_STAGE_KEY = "model_workflow_protocol_reuse_review"
MIN_GO_STAGE_COUNT = 20

GROUP_M_STAGES: Tuple[str, ...] = (
    "model_workflow_protocol_reuse_review",
    "model_adapter_priority_sequence_planning",
    "slam_spatial_mapping_model_smoke_io_inspection",
    "slam_spatial_mapping_adapter_skeleton",
    "slam_spatial_mapping_task_collaboration_planning",
    "slam_spatial_mapping_task_collaboration_revalidation",
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_MODEL_SLAM_READINESS_CHAIN_BATCH_DETECTION_READY_FOR_RECOVERY_REPAIR_EXECUTION"
)
NEXT_PHASE_BATCH_REPAIR = (
    "Phase-Midplatform-Model-SLAM-Readiness-Chain-Recovery-Repair-v1-001"
)
NEXT_PHASE_SINGLE_REPAIR = (
    "Phase-Midplatform-Model-Workflow-Protocol-Reuse-Review-Repair-v1-001"
)

PASS_FLAG = "group_m_batch_detection_complete"

GAP_CLASSES: Tuple[str, ...] = (
    "verifier_locator_gap",
    "schema_output_gap",
    "downstream_expectation_gap",
    "evidence_traceability_gap",
    "model_execution_leakage",
    "genuine_logic_hold",
)

STAGE_FAMILIES: Tuple[str, ...] = (
    "model_workflow",
    "model_adapter_priority",
    "slam_smoke_io",
    "slam_adapter_skeleton",
    "slam_task_collaboration_planning",
    "slam_revalidation",
    "unknown",
)

ROLE_TO_FAMILY: Dict[str, str] = {
    "model_workflow_review": "model_workflow",
    "adapter_priority_planning": "model_adapter_priority",
    "slam_smoke_io": "slam_smoke_io",
    "slam_adapter_skeleton": "slam_adapter_skeleton",
    "slam_task_collaboration": "slam_task_collaboration_planning",
    "slam_revalidation": "slam_revalidation",
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "model_slam_readiness_chain_batch_detection_only": True,
    "candidate_only": True,
    "review_only": True,
    "no_model_execution": True,
    "no_sensor_execution": True,
    "no_world_model_assembly": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_protocol_change": True,
    "no_model_download": True,
    "no_real_inference_execution": True,
    "no_fake_go_artifacts": True,
    "no_issue_review_stage_created": True,
    "no_gap_review_stage_created": True,
    "no_rerun_review_stage_created": True,
    "no_original_stage_pollution": True,
}
