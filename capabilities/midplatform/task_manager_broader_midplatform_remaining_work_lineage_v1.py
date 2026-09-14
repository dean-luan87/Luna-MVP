# -*- coding: utf-8 -*-
"""Broader Midplatform Remaining Work Roadmap template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_closure_consolidation_v1.py",
    "tools/evaluation/midplatform/run_task_manager_foundation_closure_consolidation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_foundation_closure_consolidation_v1.py",
)

BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "task_manager_foundation_closure_consolidation",
        "stage_term": "task_manager_broader_midplatform_remaining_work_roadmap",
    },
    {
        "base_term": "foundation_closure_consolidation_only",
        "stage_term": "remaining_work_roadmap_only",
    },
    {
        "base_term": "foundation_consolidation_pass",
        "stage_term": "remaining_work_roadmap_pass",
    },
    {
        "base_term": "foundation-closure-consolidation-scope",
        "stage_term": "remaining-work-roadmap-scope",
    },
)

BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_foundation_consolidation_go",
    "remaining_work_inventory_complete",
    "work_classification_matrix_complete",
    "future_runtime_debt_not_current_blocker",
    "future_design_not_current_blocker",
    "remaining_work_roadmap_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
