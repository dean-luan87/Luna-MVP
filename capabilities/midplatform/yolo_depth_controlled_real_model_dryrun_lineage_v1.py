# -*- coding: utf-8 -*-
"""YOLO + Depth Controlled Real Model DryRun — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
)

DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "yolo_depth_real_field_assembly_dryrun_planning", "stage_term": "yolo_depth_controlled_real_model_dryrun"},
    {"base_term": "yolo_depth_real_field_assembly_dryrun_planning_only", "stage_term": "yolo_depth_controlled_real_model_dryrun_only"},
    {"base_term": "yolo_depth_real_field_assembly_dryrun_planning_pass", "stage_term": "yolo_depth_controlled_real_model_dryrun_pass"},
)

DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_yolo_depth_real_dryrun_planning_go",
    "controlled_real_model_dryrun_complete",
    "real_yolo_output_ingested",
    "depth_path_authorization_respected",
    "alignment_pipeline_reused",
    "depth_object_fusion_pipeline_reused",
    "field_geometry_pipeline_reused",
    "field_assembly_pipeline_reused",
    "enhanced_field_scene_candidate_generated",
    "traceability_preserved",
    "warning_missing_failure_points_propagated",
    "readiness_for_success_path_hardening_ok",
    "no_unauthorized_download",
    "no_runtime_execution",
    "no_field_simulation",
    "common_validation_reuse_ok",
    "yolo_depth_controlled_real_model_dryrun_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = DRYRUN_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_types_v1.py",
    "capabilities/midplatform/real_frame_input_loader_v1.py",
    "capabilities/midplatform/yolo_real_output_bridge_v1.py",
    "capabilities/midplatform/depth_real_output_bridge_v1.py",
    "capabilities/midplatform/real_model_candidate_conversion_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_pipeline_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_result_assembler_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_static_validators_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_core_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_items_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_lineage_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_controlled_real_model_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_controlled_real_model_dryrun_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_types_v1.py",
    "capabilities/midplatform/real_frame_input_loader_v1.py",
    "capabilities/midplatform/yolo_real_output_bridge_v1.py",
    "capabilities/midplatform/depth_real_output_bridge_v1.py",
    "capabilities/midplatform/real_model_candidate_conversion_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_pipeline_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_result_assembler_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_static_validators_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_core_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_items_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_lineage_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_controlled_real_model_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_controlled_real_model_dryrun_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "yolo_depth_controlled_real_model_dryrun_report_v1.json",
    "real_frame_input_package_registry_v1.json",
    "yolo_real_output_package_registry_v1.json",
    "depth_real_output_package_registry_v1.json",
    "object_observation_candidate_from_real_yolo_registry_v1.json",
    "depth_observation_candidate_from_real_depth_registry_v1.json",
    "real_field_assembly_dryrun_result_candidate_registry_v1.json",
    "real_dryrun_case_results_v1.json",
    "real_dryrun_failure_points_v1.json",
    "real_dryrun_traceability_review_v1.json",
    "execution_authorization_review_v1.json",
    "readiness_for_success_path_hardening_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_READY_FOR_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_yolo_depth_real_dryrun_planning_go",
    "controlled_real_model_dryrun_complete",
    "real_yolo_output_ingested",
    "depth_path_authorization_respected",
    "alignment_pipeline_reused",
    "depth_object_fusion_pipeline_reused",
    "field_geometry_pipeline_reused",
    "field_assembly_pipeline_reused",
    "enhanced_field_scene_candidate_generated",
    "warning_missing_failure_points_propagated",
    "traceability_preserved",
    "readiness_for_success_path_hardening_ok",
    "no_unauthorized_download",
    "no_camera_runtime",
    "no_video_stream_runtime",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)
