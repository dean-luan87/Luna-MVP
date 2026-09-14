# -*- coding: utf-8 -*-
"""Task Manager Foundation Closure Consolidation template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_broader_midplatform_closure_roadmap_v1.py",
    "tools/evaluation/midplatform/run_task_manager_broader_midplatform_closure_roadmap_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_broader_midplatform_closure_roadmap_v1.py",
)

FOUNDATION_CLOSURE_CONSOLIDATION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "task_manager_broader_midplatform_closure_roadmap",
        "stage_term": "task_manager_foundation_closure_consolidation",
    },
    {
        "base_term": "broader_midplatform_closure_roadmap_only",
        "stage_term": "foundation_closure_consolidation_only",
    },
    {
        "base_term": "broader_midplatform_closure_roadmap_pass",
        "stage_term": "foundation_consolidation_pass",
    },
    {
        "base_term": "broader-midplatform-closure-roadmap-scope",
        "stage_term": "foundation-closure-consolidation-scope",
    },
)

FOUNDATION_CLOSURE_CONSOLIDATION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_broader_midplatform_roadmap_go",
    "foundation_consolidation_not_final_midplatform_completion",
    "midplatform_still_has_remaining_work",
    "future_runtime_debt_not_current_blocker",
    "foundation_closure_consolidation_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
