# -*- coding: utf-8 -*-
"""Module Integration Planning template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

MODULE_INTEGRATION_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_broader_midplatform_remaining_work_roadmap_v1.py",
    "tools/evaluation/midplatform/run_task_manager_broader_midplatform_remaining_work_roadmap_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_broader_midplatform_remaining_work_roadmap_v1.py",
)

MODULE_INTEGRATION_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "task_manager_broader_midplatform_remaining_work_roadmap",
        "stage_term": "task_manager_module_integration_planning",
    },
    {
        "base_term": "remaining_work_roadmap_only",
        "stage_term": "module_integration_planning_only",
    },
    {
        "base_term": "remaining_work_roadmap_pass",
        "stage_term": "module_integration_planning_pass",
    },
    {
        "base_term": "remaining-work-roadmap-scope",
        "stage_term": "module-integration-planning-scope",
    },
)

MODULE_INTEGRATION_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_remaining_work_roadmap_go",
    "module_boundary_integration_map_complete",
    "candidate_lifecycle_integration_plan_complete",
    "evidence_record_approval_permission_alignment_plan_complete",
    "task_manager_core_orchestration_skeleton_positioning_complete",
    "module_integration_planning_only",
    "candidate_not_promoted_to_record",
    "permission_candidate_not_promoted_to_grant",
    "authorization_request_candidate_not_promoted_to_authorization_request",
    "module_integration_planning_not_integration_test",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
