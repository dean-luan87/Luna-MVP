# -*- coding: utf-8 -*-
"""Real Model Field Construction Execution Path Hardening — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.real_model_execution_path_hardening_types_v1 import FINAL_DECISION_GO

EXECUTION_PATH_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_success_path_hardening_v1.py",
)

EXECUTION_PATH_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "real_model_field_construction_success_path_hardening", "stage_term": "real_model_field_construction_execution_path_hardening"},
    {"base_term": "real_model_field_construction_success_path_hardening_only", "stage_term": "real_model_field_construction_execution_path_hardening_only"},
    {"base_term": "real_model_field_construction_success_path_hardening_pass", "stage_term": "real_model_execution_path_hardening_pass"},
)

EXECUTION_PATH_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_real_model_field_construction_success_path_hardening_go",
    "prior_yolo_depth_controlled_real_model_dryrun_go",
    "real_model_execution_path_hardening_complete",
    "authorization_boundary_ok",
    "real_frame_input_set_loaded",
    "yolo_execution_path_ok",
    "depth_execution_path_classified",
    "enhanced_field_scene_candidate_generated",
    "real_field_construction_quality_report_generated",
    "real_field_construction_baseline_registry_generated",
    "no_simulation_boundary_ok",
    "traceability_review_ok",
    "failure_localization_ok",
    "route_switched_from_simulation_to_real_content",
    "field_simulation_deferred",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = EXECUTION_PATH_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_types_v1.py",
    "capabilities/midplatform/real_model_execution_authorization_resolver_v1.py",
    "capabilities/midplatform/real_image_set_loader_v1.py",
    "capabilities/midplatform/yolo_execution_path_bridge_v1.py",
    "capabilities/midplatform/depth_execution_path_bridge_v1.py",
    "capabilities/midplatform/real_model_field_construction_pipeline_v1.py",
    "capabilities/midplatform/real_field_construction_quality_report_builder_v1.py",
    "capabilities/midplatform/real_field_construction_baseline_builder_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_static_validators_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_core_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_items_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_execution_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_execution_path_hardening_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_execution_path_hardening_types_v1.py",
    "capabilities/midplatform/real_model_execution_authorization_resolver_v1.py",
    "capabilities/midplatform/real_image_set_loader_v1.py",
    "capabilities/midplatform/yolo_execution_path_bridge_v1.py",
    "capabilities/midplatform/depth_execution_path_bridge_v1.py",
    "capabilities/midplatform/real_model_field_construction_pipeline_v1.py",
    "capabilities/midplatform/real_field_construction_quality_report_builder_v1.py",
    "capabilities/midplatform/real_field_construction_baseline_builder_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_static_validators_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_core_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_items_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_execution_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_execution_path_hardening_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "real_model_field_construction_execution_path_hardening_report_v1.json",
    "real_model_execution_authorization_resolved_v1.json",
    "real_frame_input_set_registry_v1.json",
    "yolo_execution_path_result_registry_v1.json",
    "depth_execution_path_result_registry_v1.json",
    "real_model_execution_path_result_registry_v1.json",
    "real_field_construction_quality_report_v1.json",
    "real_field_construction_baseline_registry_v1.json",
    "real_model_execution_case_results_v1.json",
    "real_field_failure_localization_review_v1.json",
    "real_field_traceability_review_v1.json",
    "no_simulation_boundary_review_v1.json",
    "readiness_for_real_field_quality_evaluation_review_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_yolo_depth_controlled_real_model_dryrun_go",
    "prior_real_model_field_construction_success_path_hardening_go",
    "real_model_execution_path_hardening_complete",
    "authorization_boundary_ok",
    "real_frame_input_set_loaded",
    "yolo_execution_path_ok",
    "depth_execution_path_classified",
    "enhanced_field_scene_candidate_generated",
    "real_field_construction_quality_report_generated",
    "real_field_construction_baseline_registry_generated",
    "mock_depth_not_marked_as_real",
    "stub_depth_not_marked_as_full_real_model",
    "failure_localization_ok",
    "traceability_review_ok",
    "no_simulation_boundary_ok",
    "route_switched_from_simulation_to_real_content",
    "field_simulation_deferred",
    "no_field_simulation",
    "no_task_execution",
    "no_world_model_fact_creation",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
