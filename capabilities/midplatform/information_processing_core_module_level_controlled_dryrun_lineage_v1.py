# -*- coding: utf-8 -*-
"""Information Processing Core Module-Level Controlled DryRun template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

IPC_MODULE_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_controlled_implementation_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_controlled_implementation_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_controlled_implementation_v1.py",
)

IPC_MODULE_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "information_processing_core_controlled_implementation", "stage_term": "information_processing_core_module_level_controlled_dryrun"},
    {"base_term": "information_processing_core_controlled_implementation_only", "stage_term": "information_processing_core_module_level_controlled_dryrun_only"},
    {"base_term": "information_processing_core_controlled_implementation_pass", "stage_term": "information_processing_core_module_level_controlled_dryrun_pass"},
)

IPC_MODULE_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_ipc_controlled_implementation_go",
    "ipc_module_level_scenario_set_complete",
    "ipc_module_level_scenario_results_complete",
    "work_manual_flow_validation_complete",
    "information_type_coverage_validation_complete",
    "candidate_output_validation_complete",
    "judge_referee_validation_complete",
    "workload_control_dryrun_complete",
    "peripheral_constraint_dryrun_complete",
    "non_execution_guard_dryrun_complete",
    "ipc_qualification_result_complete",
    "ipc_module_level_controlled_dryrun_ok",
    "information_processing_core_module_level_controlled_dryrun_only",
    "file_size_governance_review_ok",
)

CORE_IMPLEMENTATION_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_types_v1.py",
    "capabilities/midplatform/information_processing_core_contracts_v1.py",
    "capabilities/midplatform/information_processing_core_classifiers_v1.py",
    "capabilities/midplatform/information_processing_core_builders_v1.py",
    "capabilities/midplatform/information_processing_core_static_validators_v1.py",
    "capabilities/midplatform/information_processing_core_v1.py",
)
