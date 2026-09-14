# -*- coding: utf-8 -*-
"""Trajectory Analysis Task Impact Controlled Skeleton lineage v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

TRAJECTORY_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_planning_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_planning_v1.py",
)

TRAJECTORY_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "trajectory_analysis_task_impact_planning", "stage_term": "trajectory_analysis_task_impact_controlled_skeleton_implementation"},
    {"base_term": "trajectory_analysis_task_impact_planning_only", "stage_term": "trajectory_analysis_task_impact_controlled_skeleton_only"},
    {"base_term": "trajectory_analysis_task_impact_planning_pass", "stage_term": "trajectory_analysis_task_impact_controlled_skeleton_pass"},
)

TRAJECTORY_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_trajectory_analysis_task_impact_planning_go",
    "controlled_skeleton_implementation_complete",
    "trajectory_builder_complete",
    "task_impact_analyzer_complete",
    "risk_projection_builder_complete",
    "all_mock_cases_passed",
    "trajectory_analysis_result_generated",
    "trajectory_analysis_task_impact_controlled_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = TRAJECTORY_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_types_v1.py",
    "capabilities/midplatform/trajectory_builder_v1.py",
    "capabilities/midplatform/task_impact_analyzer_v1.py",
    "capabilities/midplatform/risk_projection_builder_v1.py",
    "capabilities/midplatform/trajectory_analysis_static_validators_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_core_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_items_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_types_v1.py",
    "capabilities/midplatform/trajectory_builder_v1.py",
    "capabilities/midplatform/task_impact_analyzer_v1.py",
    "capabilities/midplatform/risk_projection_builder_v1.py",
    "capabilities/midplatform/trajectory_analysis_static_validators_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_core_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_items_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "trajectory_analysis_task_impact_controlled_skeleton_report_v1.json",
    "trajectory_candidate_registry_v1.json",
    "task_impact_analysis_candidate_registry_v1.json",
    "risk_projection_candidate_registry_v1.json",
    "missing_information_candidate_registry_v1.json",
    "trajectory_analysis_mock_case_results_v1.json",
    "trajectory_status_validation_results_v1.json",
    "non_execution_boundary_review_v1.json",
    "next_stage_split_plan_v1.json",
    "prohibited_scope_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_trajectory_analysis_task_impact_planning_go",
    "controlled_skeleton_implementation_complete",
    "trajectory_builder_complete",
    "task_impact_analyzer_complete",
    "risk_projection_builder_complete",
    "all_mock_cases_passed",
    "trajectory_analysis_result_generated",
    "trajectory_analysis_depends_on_dynamic_tracks",
    "no_trajectory_when_tracking_frozen",
    "new_field_resets_trajectory",
    "no_real_tracking_execution",
    "no_trajectory_prediction",
    "no_final_action_output",
    "non_execution_boundary_ok",
    "common_validation_reuse_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)
