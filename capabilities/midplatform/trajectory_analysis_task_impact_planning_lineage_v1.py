# -*- coding: utf-8 -*-
"""Trajectory Analysis & Task Impact Planning — lineage v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

TRAJECTORY_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/run_static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1.py",
)

TRAJECTORY_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "static_dynamic_target_locking_tracking_controlled_skeleton_implementation", "stage_term": "trajectory_analysis_task_impact_planning"},
    {"base_term": "static_dynamic_target_locking_tracking_controlled_skeleton_only", "stage_term": "trajectory_analysis_task_impact_planning_only"},
    {"base_term": "static_dynamic_target_locking_tracking_controlled_skeleton_implementation_pass", "stage_term": "trajectory_analysis_task_impact_planning_pass"},
)

TRAJECTORY_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_static_dynamic_target_locking_tracking_controlled_skeleton_go",
    "trajectory_analysis_task_impact_planning_complete",
    "trajectory_candidate_model_complete",
    "task_impact_analysis_candidate_model_complete",
    "risk_projection_candidate_model_complete",
    "missing_information_candidate_model_complete",
    "mock_cases_complete",
    "common_validation_reuse_ok",
    "trajectory_analysis_task_impact_planning_only",
    "file_size_governance_review_ok",
)

UPSTREAM_OUTPUT = "_tmp_eval_out/static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1_smoke_v0"
UPSTREAM_FINAL_GO = (
    "MIDPLATFORM_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING"
)
UPSTREAM_PASS_FLAG = "static_dynamic_target_locking_tracking_controlled_skeleton_pass"

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_items_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_lineage_v1.py",
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_planning_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_items_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_planning_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "trajectory_analysis_task_impact_planning_report_v1.json",
    "trajectory_status_registry_v1.json",
    "task_impact_type_registry_v1.json",
    "trajectory_candidate_model_v1.json",
    "task_impact_analysis_candidate_model_v1.json",
    "risk_projection_candidate_model_v1.json",
    "missing_information_candidate_model_v1.json",
    "trajectory_task_impact_rule_registry_v1.json",
    "trajectory_task_impact_mock_case_registry_v1.json",
    "trajectory_task_impact_mock_case_expected_results_v1.json",
    "trajectory_task_impact_input_output_contract_v1.json",
    "trajectory_task_impact_next_implementation_plan_v1.json",
    "prohibited_scope_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "trajectory_analysis_task_impact_planning_complete",
    "trajectory_candidate_model_complete",
    "task_impact_analysis_candidate_model_complete",
    "risk_projection_candidate_model_complete",
    "missing_information_candidate_model_complete",
    "mock_cases_complete",
    "common_validation_reuse_ok",
    "no_final_action_output",
    "no_task_execution",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
    "trajectory_analysis_depends_on_dynamic_tracks",
    "no_trajectory_when_tracking_frozen",
    "new_field_resets_trajectory",
    "depth_uncertainty_limits_confidence",
    "missing_info_explicit",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
)


def build_template_lineage() -> Dict[str, Any]:
    return {
        "upstream_output": UPSTREAM_OUTPUT,
        "upstream_final_go": UPSTREAM_FINAL_GO,
        "whitelist_files": list(WHITELIST_FILES),
        "phase_python_files": list(PHASE_PYTHON_FILES),
        "docs": list(DOCS),
        "artifacts": list(ARTIFACTS),
    }
