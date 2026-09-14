# -*- coding: utf-8 -*-
"""YOLO + Depth Real Field Assembly DryRun Planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_assembly_skeleton_v1.py",
    "tools/evaluation/midplatform/run_field_assembly_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_assembly_skeleton_v1.py",
)

PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_assembly_skeleton", "stage_term": "yolo_depth_real_field_assembly_dryrun_planning"},
    {"base_term": "field_assembly_skeleton_only", "stage_term": "yolo_depth_real_field_assembly_dryrun_planning_only"},
    {"base_term": "field_assembly_skeleton_pass", "stage_term": "yolo_depth_real_field_assembly_dryrun_planning_pass"},
)

PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_assembly_skeleton_go",
    "yolo_depth_real_field_assembly_dryrun_planning_complete",
    "success_criteria_complete",
    "real_input_output_contracts_complete",
    "dryrun_case_registry_complete",
    "authorization_matrix_complete",
    "traceability_policy_complete",
    "controlled_dryrun_plan_complete",
    "controlled_dryrun_deferred_to_next_phase",
    "no_real_model_execution",
    "common_validation_reuse_ok",
    "yolo_depth_real_field_assembly_dryrun_planning_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_items_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_items_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "yolo_depth_real_field_assembly_dryrun_planning_report_v1.json",
    "real_frame_input_package_contract_v1.json",
    "yolo_real_output_package_contract_v1.json",
    "depth_real_output_package_contract_v1.json",
    "real_field_assembly_dryrun_result_candidate_contract_v1.json",
    "real_field_assembly_success_criteria_v1.json",
    "yolo_depth_real_dryrun_case_registry_v1.json",
    "real_model_execution_authorization_matrix_v1.json",
    "dryrun_failure_point_policy_v1.json",
    "dryrun_traceability_policy_v1.json",
    "next_controlled_dryrun_plan_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_READY_FOR_CONTROLLED_REAL_MODEL_DRYRUN"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_assembly_skeleton_go",
    "yolo_depth_real_field_assembly_dryrun_planning_complete",
    "success_criteria_complete",
    "real_input_output_contracts_complete",
    "dryrun_case_registry_complete",
    "authorization_matrix_complete",
    "traceability_policy_complete",
    "controlled_dryrun_plan_complete",
    "yolo_already_integrated_acknowledged",
    "depth_model_or_adapter_required",
    "controlled_dryrun_deferred_to_next_phase",
    "no_real_model_execution",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
