# -*- coding: utf-8 -*-
"""Evidence Record Approval Permission Alignment Planning template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

ALIGNMENT_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/candidate_lifecycle_unification_planning_v1.py",
    "tools/evaluation/midplatform/run_candidate_lifecycle_unification_planning_v1.py",
    "tools/evaluation/midplatform/verify_candidate_lifecycle_unification_planning_v1.py",
)

ALIGNMENT_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "candidate_lifecycle_unification_planning", "stage_term": "evidence_record_approval_permission_alignment_planning"},
    {"base_term": "candidate_lifecycle_planning_only", "stage_term": "alignment_planning_only"},
    {"base_term": "candidate_lifecycle_unification_planning_pass", "stage_term": "alignment_planning_pass"},
    {"base_term": "candidate-lifecycle-planning-scope", "stage_term": "alignment-planning-scope"},
)

ALIGNMENT_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_candidate_lifecycle_unification_go",
    "alignment_object_registry_complete",
    "candidate_real_object_boundary_matrix_complete",
    "promotion_creation_preconditions_complete",
    "forbidden_alignment_transitions_complete",
    "alignment_traceability_contract_complete",
    "real_objects_absent",
    "alignment_runtime_absent",
    "candidate_promotion_executed",
    "promotion_preconditions_not_promotion_execution",
    "alignment_planning_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
