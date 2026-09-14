# -*- coding: utf-8 -*-
"""Field Simulation Planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_success_path_hardening_v1.py",
)

PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "real_model_field_construction_success_path_hardening", "stage_term": "field_simulation_planning"},
    {"base_term": "real_model_field_construction_success_path_hardening_only", "stage_term": "field_simulation_planning_only"},
    {"base_term": "real_model_field_construction_success_path_hardening_pass", "stage_term": "field_simulation_planning_pass"},
)

PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_real_model_field_construction_success_path_hardening_go",
    "field_simulation_planning_complete",
    "simulation_mode_registry_complete",
    "simulation_eligibility_policy_complete",
    "simulation_plan_candidate_contract_complete",
    "reusable_case_to_simulation_mapping_complete",
    "no_field_simulation_execution",
    "common_validation_reuse_ok",
    "field_simulation_planning_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_simulation_planning_v1.py",
    "capabilities/midplatform/field_simulation_planning_items_v1.py",
    "capabilities/midplatform/field_simulation_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_simulation_planning_v1.py",
    "capabilities/midplatform/field_simulation_planning_items_v1.py",
    "capabilities/midplatform/field_simulation_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_SIMULATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SIMULATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SIMULATION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "field_simulation_planning_report_v1.json",
    "field_simulation_mode_registry_v1.json",
    "field_simulation_input_view_contract_v1.json",
    "simulation_eligibility_policy_v1.json",
    "field_simulation_plan_candidate_contract_v1.json",
    "field_simulation_candidate_contract_v1.json",
    "field_simulation_readiness_policy_v1.json",
    "failure_and_degradation_simulation_policy_v1.json",
    "reusable_case_to_simulation_mapping_v1.json",
    "field_simulation_planning_case_registry_v1.json",
    "readiness_for_field_simulation_skeleton_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = "MIDPLATFORM_FIELD_SIMULATION_PLANNING_READY_FOR_FIELD_SIMULATION_SKELETON"

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_real_model_field_construction_success_path_hardening_go",
    "field_simulation_planning_complete",
    "simulation_mode_registry_complete",
    "simulation_eligibility_policy_complete",
    "simulation_plan_candidate_contract_complete",
    "reusable_case_to_simulation_mapping_complete",
    "all_planning_cases_passed",
    "real_model_hardened_baselines_used",
    "no_field_simulation_execution",
    "no_task_execution",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)
