# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Controlled Skeleton Implementation template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_implementation_planning_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_implementation_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_implementation_planning_v1.py",
)

ORCHESTRATION_CONTROLLED_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "task_manager_core_orchestration_implementation_planning", "stage_term": "task_manager_core_orchestration_controlled_skeleton_implementation"},
    {"base_term": "orchestration_implementation_planning_only", "stage_term": "orchestration_controlled_skeleton_implementation_only"},
    {"base_term": "orchestration_implementation_planning_pass", "stage_term": "orchestration_controlled_skeleton_implementation_pass"},
    {"base_term": "orchestration-implementation-planning-scope", "stage_term": "orchestration-controlled-skeleton-implementation-scope"},
)

ORCHESTRATION_CONTROLLED_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_implementation_planning_go",
    "types_implemented",
    "contracts_implemented",
    "builders_implemented",
    "validators_implemented",
    "skeleton_implemented",
    "strong_coupled_single_package_ok",
    "controlled_skeleton_smoke_ok",
    "all_outputs_candidate_only",
    "non_execution_guard_ok",
    "implementation_not_split_into_subphases",
    "orchestration_controlled_skeleton_implementation_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

CORE_IMPLEMENTATION_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_types_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_contracts_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_builders_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_static_validators_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_skeleton_v1.py",
)
