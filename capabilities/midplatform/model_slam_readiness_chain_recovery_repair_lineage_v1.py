# -*- coding: utf-8 -*-
"""Model-SLAM readiness chain recovery repair — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.model_slam_readiness_chain_recovery_repair_items_v1 import (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_PARTIAL,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_recovery_repair_items_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_recovery_repair_lineage_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_recovery_repair_v1.py",
    "tools/evaluation/midplatform/run_model_slam_readiness_chain_recovery_repair_v1.py",
    "tools/evaluation/midplatform/verify_model_slam_readiness_chain_recovery_repair_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES
DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "model_slam_readiness_chain_recovery_repair_report_v1.json",
    "batch_detection_input_review_v1.json",
    "group_m_safe_candidate_execution_matrix_v1.json",
    "model_workflow_protocol_reuse_review_repair_review_v1.json",
    "model_adapter_priority_sequence_planning_repair_review_v1.json",
    "slam_spatial_mapping_model_smoke_io_repair_review_v1.json",
    "slam_spatial_mapping_adapter_skeleton_repair_review_v1.json",
    "slam_spatial_mapping_task_collaboration_planning_repair_review_v1.json",
    "slam_spatial_mapping_task_collaboration_revalidation_repair_review_v1.json",
    "per_stage_original_rerun_results_v1.json",
    "per_stage_final_decision_alignment_review_v1.json",
    "per_stage_no_model_execution_review_v1.json",
    "per_stage_no_sensor_execution_review_v1.json",
    "per_stage_no_world_model_assembly_review_v1.json",
    "per_stage_no_task_reasoning_review_v1.json",
    "verifier_locator_repair_review_v1.json",
    "schema_output_repair_review_v1.json",
    "downstream_expectation_repair_review_v1.json",
    "canonical_checkpoint_scan_only_after_recovery_repair_v1.json",
    "canonical_checkpoint_topdown_after_recovery_repair_v1.json",
    "no_issue_review_created_review_v1.json",
    "no_gap_review_created_review_v1.json",
    "no_rerun_review_created_review_v1.json",
    "no_protocol_change_review_v1.json",
    "no_model_execution_review_v1.json",
    "no_sensor_execution_review_v1.json",
    "no_world_model_assembly_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "batch_detection_go_confirmed",
    "plan_c_ready_for_slam_readiness_repair",
    "group_m_safe_candidate_count_ok",
    "processed_group_m_candidate_count_ok",
    "all_group_m_original_rerun_attempted",
    "model_workflow_repaired",
    "model_adapter_priority_repaired",
    "slam_smoke_io_repaired",
    "slam_adapter_skeleton_repaired",
    "slam_task_collaboration_planning_repaired",
    "slam_revalidation_verifier_report_repaired",
    "no_model_execution",
    "no_sensor_execution",
    "no_camera_execution",
    "no_world_model_assembly",
    "no_task_reasoning",
    "no_field_simulation",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_rerun_review_stage_created",
    "no_fake_go_artifacts",
    "no_protocol_change",
    "common_validation_reuse_ok",
    "canonical_scan_only_after_repair_recorded",
    "group_m_recovery_repair_complete",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE, FINAL_DECISION_PARTIAL)
