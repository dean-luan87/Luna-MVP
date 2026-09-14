# -*- coding: utf-8 -*-
"""Model-SLAM readiness chain batch detection — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.model_slam_readiness_chain_batch_detection_items_v1 import (
    FINAL_DECISION_COMPLETE,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_batch_detection_items_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_batch_detection_scan_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_batch_detection_lineage_v1.py",
    "capabilities/midplatform/model_slam_readiness_chain_batch_detection_and_recovery_plan_v1.py",
    "tools/evaluation/midplatform/run_model_slam_readiness_chain_batch_detection_and_recovery_plan_v1.py",
    "tools/evaluation/midplatform/verify_model_slam_readiness_chain_batch_detection_and_recovery_plan_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES
DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "model_slam_readiness_chain_batch_detection_report_v1.json",
    "group_m_stage_inventory_v1.json",
    "group_m_checkpoint_status_matrix_v1.json",
    "group_m_runner_verifier_locator_matrix_v1.json",
    "group_m_gap_classification_v1.json",
    "model_workflow_reuse_review_diagnostic_v1.json",
    "model_adapter_priority_sequence_diagnostic_v1.json",
    "slam_p0_smoke_io_diagnostic_v1.json",
    "slam_p0_adapter_skeleton_diagnostic_v1.json",
    "slam_p0_task_collaboration_planning_diagnostic_v1.json",
    "slam_p0_revalidation_diagnostic_v1.json",
    "verifier_locator_gap_matrix_v1.json",
    "schema_output_gap_matrix_v1.json",
    "downstream_expectation_gap_matrix_v1.json",
    "evidence_traceability_gap_matrix_v1.json",
    "model_execution_leakage_review_v1.json",
    "safe_model_slam_readiness_repair_candidates_v1.json",
    "stages_requiring_individual_repair_v1.json",
    "group_m_recovery_plan_v1.json",
    "no_model_execution_review_v1.json",
    "no_sensor_execution_review_v1.json",
    "no_world_model_assembly_review_v1.json",
    "no_task_reasoning_review_v1.json",
    "no_issue_review_created_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "governance_gate_repair_go_confirmed",
    "go_stage_count_at_least_20",
    "first_failed_stage_group_m_confirmed",
    "group_m_stage_count",
    "group_m_inventory_complete",
    "group_m_gap_classification_complete",
    "group_m_recovery_plan_complete",
    "no_model_execution",
    "no_sensor_execution",
    "no_world_model_assembly",
    "no_task_reasoning",
    "no_field_simulation",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_rerun_review_stage_created",
    "no_fake_go_artifacts",
    "no_protocol_change",
    "common_validation_reuse_ok",
    "group_m_batch_detection_complete",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE,)
