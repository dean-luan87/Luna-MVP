# -*- coding: utf-8 -*-
"""Module Boundary Registry Planning template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_module_integration_planning_v1.py",
    "tools/evaluation/midplatform/run_task_manager_module_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_module_integration_planning_v1.py",
)

MODULE_BOUNDARY_REGISTRY_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "task_manager_module_integration_planning", "stage_term": "module_boundary_registry_planning"},
    {"base_term": "module_integration_planning_only", "stage_term": "boundary_registry_planning_only"},
    {"base_term": "module_integration_planning_pass", "stage_term": "boundary_registry_planning_pass"},
    {"base_term": "module-integration-planning-scope", "stage_term": "boundary-registry-planning-scope"},
)

MODULE_BOUNDARY_REGISTRY_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_module_integration_planning_go",
    "module_boundary_registry_draft_complete",
    "ownership_matrix_complete",
    "not_owned_forbidden_transition_statement_complete",
    "boundary_conflict_detection_plan_complete",
    "all_required_modules_have_registry_entries",
    "no_forbidden_ownership_detected",
    "boundary_registry_planning_only",
    "module_boundary_registry_planning_not_runtime_registry",
    "boundary_conflict_detection_plan_not_full_repo_scan",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
