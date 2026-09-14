# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Module-Level Controlled DryRun template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_controlled_skeleton_implementation_v1.py",
)

ORCHESTRATION_MODULE_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "task_manager_core_orchestration_controlled_skeleton_implementation", "stage_term": "task_manager_core_orchestration_module_level_controlled_dryrun"},
    {"base_term": "orchestration_controlled_skeleton_implementation_only", "stage_term": "orchestration_module_level_controlled_dryrun_only"},
    {"base_term": "orchestration_controlled_skeleton_implementation_pass", "stage_term": "orchestration_module_level_controlled_dryrun_pass"},
    {"base_term": "orchestration-controlled-skeleton-implementation-scope", "stage_term": "orchestration-module-level-controlled-dryrun-scope"},
)

ORCHESTRATION_MODULE_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_controlled_skeleton_implementation_go",
    "controlled_dryrun_scenario_set_complete",
    "controlled_dryrun_scenario_results_complete",
    "module_level_flow_validation_complete",
    "candidate_output_validation_complete",
    "non_execution_guard_dryrun_complete",
    "error_blocker_defer_handling_validation_complete",
    "module_level_dryrun_result_summary_complete",
    "module_level_controlled_dryrun_ok",
    "all_scenarios_passed",
    "orchestration_module_level_controlled_dryrun_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
