# -*- coding: utf-8 -*-
"""Field Simulation Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_simulation_planning_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_planning_v1.py",
)

SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_simulation_planning", "stage_term": "field_simulation_skeleton"},
    {"base_term": "field_simulation_planning_only", "stage_term": "field_simulation_skeleton_only"},
    {"base_term": "field_simulation_planning_pass", "stage_term": "field_simulation_skeleton_pass"},
)

SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_simulation_planning_go",
    "field_simulation_skeleton_complete",
    "simulation_input_view_builder_complete",
    "eligibility_evaluator_complete",
    "simulation_plan_builder_complete",
    "simulation_candidate_generator_complete",
    "readiness_assembler_complete",
    "all_skeleton_cases_passed",
    "no_action_no_fact_boundary_ok",
    "common_validation_reuse_ok",
    "field_simulation_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_simulation_types_v1.py",
    "capabilities/midplatform/field_simulation_input_view_builder_v1.py",
    "capabilities/midplatform/simulation_eligibility_evaluator_v1.py",
    "capabilities/midplatform/field_simulation_plan_builder_v1.py",
    "capabilities/midplatform/field_simulation_candidate_generator_v1.py",
    "capabilities/midplatform/field_simulation_readiness_assembler_v1.py",
    "capabilities/midplatform/field_simulation_static_validators_v1.py",
    "capabilities/midplatform/field_simulation_core_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_items_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_simulation_types_v1.py",
    "capabilities/midplatform/field_simulation_input_view_builder_v1.py",
    "capabilities/midplatform/simulation_eligibility_evaluator_v1.py",
    "capabilities/midplatform/field_simulation_plan_builder_v1.py",
    "capabilities/midplatform/field_simulation_candidate_generator_v1.py",
    "capabilities/midplatform/field_simulation_readiness_assembler_v1.py",
    "capabilities/midplatform/field_simulation_static_validators_v1.py",
    "capabilities/midplatform/field_simulation_core_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_items_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_SIMULATION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SIMULATION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SIMULATION_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "field_simulation_skeleton_report_v1.json",
    "field_simulation_input_view_registry_v1.json",
    "simulation_eligibility_candidate_registry_v1.json",
    "field_simulation_plan_candidate_registry_v1.json",
    "field_simulation_candidate_registry_v1.json",
    "field_simulation_readiness_candidate_registry_v1.json",
    "field_simulation_skeleton_case_results_v1.json",
    "field_simulation_traceability_review_v1.json",
    "no_action_no_fact_boundary_review_v1.json",
    "readiness_for_task_reasoning_planning_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = "MIDPLATFORM_FIELD_SIMULATION_SKELETON_READY_FOR_TASK_REASONING_PLANNING"

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_simulation_planning_go",
    "field_simulation_skeleton_complete",
    "simulation_input_view_builder_complete",
    "eligibility_evaluator_complete",
    "simulation_plan_builder_complete",
    "simulation_candidate_generator_complete",
    "readiness_assembler_complete",
    "all_skeleton_cases_passed",
    "no_action_no_fact_boundary_ok",
    "readiness_for_task_reasoning_planning_ok",
    "no_task_reasoning",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)
