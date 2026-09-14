# -*- coding: utf-8 -*-
"""Candidate Lifecycle Unification Planning template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/module_boundary_registry_planning_v1.py",
    "tools/evaluation/midplatform/run_module_boundary_registry_planning_v1.py",
    "tools/evaluation/midplatform/verify_module_boundary_registry_planning_v1.py",
)

CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "module_boundary_registry_planning", "stage_term": "candidate_lifecycle_unification_planning"},
    {"base_term": "boundary_registry_planning_only", "stage_term": "candidate_lifecycle_planning_only"},
    {"base_term": "boundary_registry_planning_pass", "stage_term": "candidate_lifecycle_unification_planning_pass"},
    {"base_term": "boundary-registry-planning-scope", "stage_term": "candidate-lifecycle-planning-scope"},
)

CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_module_boundary_registry_planning_go",
    "candidate_type_registry_complete",
    "unified_lifecycle_state_machine_complete",
    "state_transition_rules_complete",
    "forbidden_candidate_promotion_rules_complete",
    "all_candidate_types_covered",
    "promotion_ready_not_promotion_executed",
    "upgraded_not_real_record_or_grant",
    "candidate_closed_not_runtime_closure",
    "candidate_lifecycle_runtime_absent",
    "candidate_lifecycle_planning_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
