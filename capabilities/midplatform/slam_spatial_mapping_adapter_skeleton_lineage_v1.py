# -*- coding: utf-8 -*-
"""SLAM spatial mapping adapter skeleton — lineage v1 (revision)."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.slam_spatial_mapping_adapter_types_v1 import FINAL_DECISION_GO

SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/slam_spatial_mapping_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/run_slam_spatial_mapping_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/verify_slam_spatial_mapping_model_smoke_io_inspection_v1.py",
)

SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "model_smoke_io_inspection", "stage_term": "slam_spatial_mapping_adapter_skeleton"},
    {"base_term": "model_smoke_io_inspection_pass", "stage_term": "slam_spatial_mapping_adapter_skeleton_pass"},
)

SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_slam_spatial_mapping_smoke_io_inspection_go",
    "smoke_io_inspection_artifacts_read",
    "adapter_based_on_real_inspection_results",
    "slam_spatial_mapping_adapter_skeleton_complete",
    "raw_output_loader_complete",
    "readiness_for_task_collaboration_ok",
    "readiness_for_later_world_model_candidate_assembly_ok",
    "no_world_model_candidate_generated",
    "no_field_simulation",
    "no_task_reasoning",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_types_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_input_builder_v1.py",
    "capabilities/midplatform/spatial_mapping_raw_output_loader_v1.py",
    "capabilities/midplatform/spatial_mapping_output_normalizer_v1.py",
    "capabilities/midplatform/spatial_anchor_candidate_builder_v1.py",
    "capabilities/midplatform/local_map_candidate_builder_v1.py",
    "capabilities/midplatform/spatial_mapping_adapter_result_assembler_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_static_validators_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_core_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_skeleton_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_skeleton_items_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_slam_spatial_mapping_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_slam_spatial_mapping_adapter_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/slam_spatial_mapping_adapter_types_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_input_builder_v1.py",
    "capabilities/midplatform/spatial_mapping_raw_output_loader_v1.py",
    "capabilities/midplatform/spatial_mapping_output_normalizer_v1.py",
    "capabilities/midplatform/spatial_anchor_candidate_builder_v1.py",
    "capabilities/midplatform/local_map_candidate_builder_v1.py",
    "capabilities/midplatform/spatial_mapping_adapter_result_assembler_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_static_validators_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_core_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_skeleton_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_skeleton_items_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_adapter_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_slam_spatial_mapping_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_slam_spatial_mapping_adapter_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_SLAM_SPATIAL_MAPPING_ADAPTER_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_SLAM_SPATIAL_MAPPING_ADAPTER_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_SLAM_SPATIAL_MAPPING_ADAPTER_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "slam_spatial_mapping_adapter_skeleton_report_v1.json",
    "spatial_mapping_adapter_input_registry_v1.json",
    "spatial_mapping_raw_output_candidate_registry_v1.json",
    "camera_pose_candidate_registry_v1.json",
    "camera_trajectory_candidate_registry_v1.json",
    "spatial_anchor_candidate_registry_v1.json",
    "local_map_candidate_registry_v1.json",
    "map_quality_candidate_registry_v1.json",
    "spatial_mapping_adapter_result_candidate_registry_v1.json",
    "spatial_mapping_task_collaboration_mapping_review_v1.json",
    "spatial_mapping_later_world_model_readiness_review_v1.json",
    "protocol_reuse_decision_v1.json",
    "new_protocol_reason_required_report_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "skeleton_case_results_v1.json",
    "prohibited_scope_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_slam_spatial_mapping_smoke_io_inspection_go",
    "smoke_io_inspection_artifacts_read",
    "adapter_based_on_real_inspection_results",
    "slam_spatial_mapping_adapter_skeleton_complete",
    "adapter_input_builder_complete",
    "raw_output_loader_complete",
    "spatial_output_normalizer_complete",
    "spatial_anchor_builder_complete",
    "local_map_builder_complete",
    "adapter_result_assembler_complete",
    "all_skeleton_cases_passed",
    "protocol_reuse_decision_ok",
    "readiness_for_task_collaboration_ok",
    "readiness_for_later_world_model_candidate_assembly_ok",
    "existing_io_reuse_ok",
    "no_new_protocol_without_reason",
    "cached_output_not_marked_as_real_run",
    "adapter_stub_not_marked_as_real_run",
    "blocked_cases_do_not_fabricate_outputs",
    "no_real_slam_execution",
    "no_field_simulation",
    "no_task_reasoning",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "owner_constraints_inherited",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
