# -*- coding: utf-8 -*-
"""SLAM spatial mapping task collaboration planning revalidation — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_items_v1 import (
    FINAL_DECISION_GO as P0_TCP_FINAL_DECISION_GO,
    TASK_MODEL_GROUPS,
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_REVALIDATED_READY_FOR_TRACKING_OPTICALFLOW_TASK_COLLABORATION_REVALIDATION"
)
SELECTED_NEXT_PHASE = "Phase-Midplatform-Tracking-OpticalFlow-Task-Collaboration-Planning-Revalidation-v1-001"
SELECTED_NEXT_ROUTE = "Tracking Optical Flow Task Collaboration Planning Revalidation"

P0_TCP_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/slam_spatial_mapping_task_collaboration_planning_v1_smoke_v0"
P0_TCP_PASS_FLAG = "slam_task_collaboration_planning_pass"

REQUIRED_TCP_ARTIFACTS: Tuple[str, ...] = (
    "slam_spatial_mapping_task_collaboration_planning_report_v1.json",
    "slam_task_collaboration_model_group_registry_v1.json",
    "slam_task_input_mapping_review_v1.json",
    "slam_task_output_evidence_mapping_review_v1.json",
    "slam_task_invocation_control_review_v1.json",
    "slam_task_failure_degradation_policy_v1.json",
    "slam_task_collaboration_case_registry_v1.json",
    "slam_task_collaboration_protocol_reuse_decision_v1.json",
    "new_protocol_reason_required_report_v1.json",
    "no_action_boundary_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

P0_SOURCE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_items_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_lineage_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/run_slam_spatial_mapping_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/verify_slam_spatial_mapping_task_collaboration_planning_v1.py",
)

# Ordered upstream bootstrap: TM/org → field-first → field model → exec path → SLAM tail
BOOTSTRAP_RUN_SCRIPTS: Tuple[str, ...] = (
    "run_task_manager_broader_midplatform_closure_roadmap_v1",
    "run_task_manager_foundation_closure_consolidation_v1",
    "run_task_manager_broader_midplatform_remaining_work_roadmap_v1",
    "run_task_manager_module_integration_planning_v1",
    "run_module_boundary_registry_planning_v1",
    "run_candidate_lifecycle_unification_planning_v1",
    "run_evidence_record_approval_permission_alignment_planning_v1",
    "run_task_manager_core_orchestration_skeleton_consolidation_v1",
    "run_task_manager_core_orchestration_implementation_planning_v1",
    "run_task_manager_core_orchestration_controlled_skeleton_implementation_v1",
    "run_task_manager_core_orchestration_module_level_controlled_dryrun_v1",
    "run_module_integration_gap_consolidation_v1",
    "run_core_capability_peripheral_service_recalibration_v1",
    "run_luna_project_organization_work_manual_and_existing_work_mapping_v1",
    "run_information_processing_core_work_manual_definition_v1",
    "run_information_processing_core_controlled_implementation_v1",
    "run_information_processing_core_self_work_core_design_v1",
    "run_field_first_core_recalibration_and_next_work_definition_v1",
    "run_field_first_core_role_function_redefinition_v1",
    "run_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1",
    "run_field_first_core_model_preinstall_plan_v1",
    "run_field_first_core_model_document_capability_review_v1",
    "run_field_first_core_model_io_compatibility_precheck_v1",
    "run_field_scene_small_range_construction_core_definition_v1",
    "run_field_continuity_detection_planning_v1",
    "run_field_continuity_detection_controlled_skeleton_implementation_v1",
    "run_static_dynamic_target_locking_tracking_planning_v1",
    "run_static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1",
    "run_trajectory_analysis_task_impact_planning_v1",
    "run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1",
    "run_field_first_core_logic_formal_implementation_v1",
    "run_field_first_minimal_real_model_adapter_integration_planning_v1",
    "run_real_observation_candidate_ingestion_skeleton_v1",
    "run_field_construction_depth_geometry_model_integration_planning_v1",
    "run_depth_observation_candidate_ingestion_skeleton_v1",
    "run_multi_model_field_assembly_core_planning_v1",
    "run_multi_model_alignment_skeleton_v1",
    "run_depth_object_fusion_skeleton_v1",
    "run_field_geometry_candidate_skeleton_v1",
    "run_field_assembly_skeleton_v1",
    "run_yolo_depth_real_field_assembly_dryrun_planning_v1",
    "run_yolo_depth_controlled_real_model_dryrun_v1",
    "run_real_model_field_construction_success_path_hardening_v1",
    "run_real_model_field_construction_execution_path_hardening_v1",
    "run_model_workflow_protocol_reuse_and_cleanup_review_v1",
    "run_model_adapter_priority_sequence_planning_v1",
    "run_slam_spatial_mapping_model_smoke_io_inspection_v1",
    "run_slam_spatial_mapping_adapter_skeleton_v1",
    "run_slam_spatial_mapping_task_collaboration_planning_v1",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "revalidation_only": True,
    "no_scene_graph_smoke_io": True,
    "no_world_model_assembly": True,
    "no_task_reasoning_execution": True,
    "no_action_output": True,
    "no_new_protocol_added": True,
    "no_field_simulation": True,
}

EXPECTED_TASK_GROUPS: Tuple[str, ...] = tuple(g["group_id"] for g in TASK_MODEL_GROUPS)

SCENE_GRAPH_P0_EXPECTED: Dict[str, Any] = {
    "final_decision": P0_TCP_FINAL_DECISION_GO,
    "pass_flag": P0_TCP_PASS_FLAG,
    "verifier": "GO",
}
