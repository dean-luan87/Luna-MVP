# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Implementation Planning template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_skeleton_consolidation_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_skeleton_consolidation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_skeleton_consolidation_v1.py",
)

ORCHESTRATION_IMPLEMENTATION_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "task_manager_core_orchestration_skeleton_consolidation", "stage_term": "task_manager_core_orchestration_implementation_planning"},
    {"base_term": "orchestration_consolidation_only", "stage_term": "orchestration_implementation_planning_only"},
    {"base_term": "orchestration_skeleton_consolidation_pass", "stage_term": "orchestration_implementation_planning_pass"},
    {"base_term": "orchestration-consolidation-scope", "stage_term": "orchestration-implementation-planning-scope"},
)

ORCHESTRATION_IMPLEMENTATION_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_orchestration_skeleton_consolidation_go",
    "orchestration_functional_units_complete",
    "orchestration_data_structure_plan_complete",
    "static_validator_plan_complete",
    "implementation_file_plan_complete",
    "implementation_files_split_by_responsibility",
    "no_monolithic_skeleton_planned",
    "controlled_implementation_ready",
    "runtime_dependency_absent",
    "drive_brain_implementation_absent",
    "reflection_brain_implementation_absent",
    "orchestration_implementation_planning_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
