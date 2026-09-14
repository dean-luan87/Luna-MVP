# -*- coding: utf-8 -*-
"""Real Model Field Construction Success Path Hardening — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

HARDENING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_controlled_real_model_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_controlled_real_model_dryrun_v1.py",
)

HARDENING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "yolo_depth_controlled_real_model_dryrun", "stage_term": "real_model_field_construction_success_path_hardening"},
    {"base_term": "yolo_depth_controlled_real_model_dryrun_only", "stage_term": "real_model_field_construction_success_path_hardening_only"},
    {"base_term": "yolo_depth_controlled_real_model_dryrun_pass", "stage_term": "real_model_field_construction_success_path_hardening_pass"},
)

HARDENING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_yolo_depth_controlled_real_model_dryrun_go",
    "real_model_field_construction_success_path_hardening_complete",
    "stability_review_ok",
    "explainability_review_ok",
    "reusability_review_ok",
    "failure_localization_ok",
    "quality_hardening_ok",
    "readiness_for_core_success_path_ok",
    "readiness_for_field_simulation_planning_ok",
    "no_real_model_rerun",
    "common_validation_reuse_ok",
    "real_model_field_construction_success_path_hardening_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = HARDENING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_types_v1.py",
    "capabilities/midplatform/field_construction_success_path_quality_assessor_v1.py",
    "capabilities/midplatform/field_construction_reusable_case_builder_v1.py",
    "capabilities/midplatform/field_construction_failure_localizer_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_result_assembler_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_static_validators_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_core_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_items_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_success_path_hardening_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_field_construction_hardening_types_v1.py",
    "capabilities/midplatform/field_construction_success_path_quality_assessor_v1.py",
    "capabilities/midplatform/field_construction_reusable_case_builder_v1.py",
    "capabilities/midplatform/field_construction_failure_localizer_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_result_assembler_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_static_validators_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_core_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_items_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_success_path_hardening_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "real_model_field_construction_success_path_hardening_report_v1.json",
    "hardened_field_construction_result_candidate_registry_v1.json",
    "success_path_quality_assessment_candidate_registry_v1.json",
    "reusable_field_construction_case_registry_v1.json",
    "success_path_stability_review_v1.json",
    "success_path_explainability_review_v1.json",
    "success_path_reusability_review_v1.json",
    "field_construction_failure_localization_review_v1.json",
    "field_construction_quality_hardening_review_v1.json",
    "readiness_for_core_success_path_review_v1.json",
    "readiness_for_field_simulation_planning_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_READY_FOR_FIELD_SIMULATION_PLANNING"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_yolo_depth_controlled_real_model_dryrun_go",
    "real_model_field_construction_success_path_hardening_complete",
    "stability_review_ok",
    "explainability_review_ok",
    "reusability_review_ok",
    "failure_localization_ok",
    "quality_hardening_ok",
    "readiness_for_core_success_path_ok",
    "readiness_for_field_simulation_planning_ok",
    "pass_cases_reusable",
    "degraded_cases_limitations_recorded",
    "failed_cases_localized",
    "traceability_completeness_checked",
    "mock_depth_not_marked_as_real",
    "quality_summary_completeness_checked",
    "no_real_model_rerun",
    "no_field_simulation",
    "no_task_execution",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)
