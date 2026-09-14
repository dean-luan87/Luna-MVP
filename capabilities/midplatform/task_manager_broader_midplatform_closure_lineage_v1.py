# -*- coding: utf-8 -*-
"""Broader Midplatform Closure template lineage — separate from governance gate lineage."""

from __future__ import annotations

from typing import Dict, Tuple

BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_handoff_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_handoff_v1.py",
)

BROADER_MIDPLATFORM_CLOSURE_ROADMAP_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_module_handoff",
        "stage_term": "task_manager_broader_midplatform_closure_roadmap",
    },
    {
        "base_term": "module_handoff_only",
        "stage_term": "broader_midplatform_closure_roadmap_only",
    },
    {
        "base_term": "module_handoff_pass",
        "stage_term": "broader_midplatform_closure_roadmap_pass",
    },
    {
        "base_term": "module-handoff-scope",
        "stage_term": "broader-midplatform-closure-roadmap-scope",
    },
)

BROADER_MIDPLATFORM_CLOSURE_ROADMAP_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_request_module_handoff_go",
    "broader_midplatform_status_inventory_complete",
    "midplatform_closure_gap_matrix_complete",
    "mainline_closure_route_decision_complete",
    "future_runtime_debt_not_current_blocker",
    "broader_midplatform_closure_roadmap_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
