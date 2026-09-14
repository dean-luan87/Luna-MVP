# -*- coding: utf-8 -*-
"""Module Integration Gap Consolidation template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_module_level_controlled_dryrun_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_module_level_controlled_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_module_level_controlled_dryrun_v1.py",
)

MODULE_INTEGRATION_GAP_CONSOLIDATION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "task_manager_core_orchestration_module_level_controlled_dryrun", "stage_term": "module_integration_gap_consolidation"},
    {"base_term": "orchestration_module_level_controlled_dryrun_only", "stage_term": "module_integration_gap_consolidation_only"},
    {"base_term": "orchestration_module_level_controlled_dryrun_pass", "stage_term": "module_integration_gap_consolidation_pass"},
    {"base_term": "orchestration-module-level-controlled-dryrun-scope", "stage_term": "module-integration-gap-consolidation-scope"},
)

MODULE_INTEGRATION_GAP_CONSOLIDATION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_core_orchestration_module_dryrun_go",
    "completed_module_inventory_complete",
    "remaining_gap_inventory_complete",
    "gap_classification_matrix_complete",
    "module_chain_readiness_map_complete",
    "next_module_candidate_selection_complete",
    "do_not_reopen_do_not_overbuild_rules_complete",
    "core_orchestration_not_extended",
    "module_handoff_contract_gap_identified",
    "module_integration_gap_consolidation_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
