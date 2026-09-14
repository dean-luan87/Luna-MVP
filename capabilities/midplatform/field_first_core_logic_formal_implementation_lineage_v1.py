# -*- coding: utf-8 -*-
"""Field-First Core Logic Formal Implementation — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

CORE_LOGIC_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
)

CORE_LOGIC_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "trajectory_analysis_task_impact_controlled_skeleton_implementation", "stage_term": "field_first_core_logic_formal_implementation"},
    {"base_term": "trajectory_analysis_task_impact_controlled_skeleton_only", "stage_term": "field_first_core_logic_formal_implementation_only"},
    {"base_term": "trajectory_analysis_task_impact_controlled_skeleton_pass", "stage_term": "field_first_core_logic_formal_implementation_pass"},
)

CORE_LOGIC_STAGE_ADDITIONS: Tuple[str, ...] = (
    "all_four_upstream_skeletons_go",
    "field_first_core_pipeline_complete",
    "core_result_candidate_generated",
    "cross_stage_consistency_validated",
    "all_core_pipeline_mock_cases_passed",
    "field_first_core_logic_formal_implementation_only",
    "common_validation_reuse_ok",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = CORE_LOGIC_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_first_core_logic_types_v1.py",
    "capabilities/midplatform/field_first_core_pipeline_v1.py",
    "capabilities/midplatform/field_first_core_result_assembler_v1.py",
    "capabilities/midplatform/field_first_core_consistency_validators_v1.py",
    "capabilities/midplatform/field_first_core_logic_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_items_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_logic_formal_implementation_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_logic_formal_implementation_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_logic_types_v1.py",
    "capabilities/midplatform/field_first_core_pipeline_v1.py",
    "capabilities/midplatform/field_first_core_result_assembler_v1.py",
    "capabilities/midplatform/field_first_core_consistency_validators_v1.py",
    "capabilities/midplatform/field_first_core_logic_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_items_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_logic_formal_implementation_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_logic_formal_implementation_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "field_first_core_logic_formal_implementation_report_v1.json",
    "field_first_core_input_package_contract_v1.json",
    "field_first_core_pipeline_registry_v1.json",
    "field_first_core_result_candidate_registry_v1.json",
    "field_first_core_consistency_validation_results_v1.json",
    "field_first_core_mock_case_results_v1.json",
    "decision_readiness_summary_registry_v1.json",
    "warning_missing_information_propagation_review_v1.json",
    "non_execution_boundary_review_v1.json",
    "next_stage_split_plan_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION_READY_FOR_FIELD_SIMULATION_PLANNING"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "all_four_upstream_skeletons_go",
    "field_first_core_pipeline_complete",
    "core_result_candidate_generated",
    "cross_stage_consistency_validated",
    "all_core_pipeline_mock_cases_passed",
    "missing_information_propagation_ok",
    "warning_summary_ok",
    "decision_readiness_summary_ok",
    "common_validation_reuse_ok",
    "non_execution_boundary_ok",
    "no_model_execution",
    "no_runtime_execution",
    "no_final_action_output",
    "no_world_model_fact_creation",
    "no_memory_write",
    "next_phase_readiness_ok",
)

UPSTREAM_SKELETONS: Tuple[Dict[str, str], ...] = (
    {
        "phase": "field_scene",
        "summary_path": "_tmp_eval_out/field_scene_small_range_construction_core_definition_v1_smoke_v0/summary.json",
        "verifier_path": "_tmp_eval_out/field_scene_small_range_construction_core_definition_v1_smoke_v0/verifier_report.json",
        "final_go": "MIDPLATFORM_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_CORE_DEFINITION_READY_FOR_FIELD_CONTINUITY_DETECTION_PLANNING",
        "pass_flag": "field_scene_small_range_construction_pass",
        "min_checks": 460,
    },
    {
        "phase": "continuity",
        "summary_path": "_tmp_eval_out/field_continuity_detection_controlled_skeleton_implementation_v1_smoke_v0/summary.json",
        "verifier_path": "_tmp_eval_out/field_continuity_detection_controlled_skeleton_implementation_v1_smoke_v0/verifier_report.json",
        "final_go": "MIDPLATFORM_FIELD_CONTINUITY_DETECTION_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_STATIC_AND_DYNAMIC_TARGET_LOCKING_TRACKING_PLANNING",
        "pass_flag": "field_continuity_detection_controlled_skeleton_pass",
        "min_checks": 480,
    },
    {
        "phase": "target_locking",
        "summary_path": "_tmp_eval_out/static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1_smoke_v0/summary.json",
        "verifier_path": "_tmp_eval_out/static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1_smoke_v0/verifier_report.json",
        "final_go": "MIDPLATFORM_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING",
        "pass_flag": "static_dynamic_target_locking_tracking_controlled_skeleton_pass",
        "min_checks": 500,
    },
    {
        "phase": "trajectory",
        "summary_path": "_tmp_eval_out/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1_smoke_v0/summary.json",
        "verifier_path": "_tmp_eval_out/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1_smoke_v0/verifier_report.json",
        "final_go": "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION",
        "pass_flag": "trajectory_analysis_task_impact_controlled_skeleton_pass",
        "min_checks": 400,
    },
)
