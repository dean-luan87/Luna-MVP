# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Skeleton Consolidation template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/evidence_record_approval_permission_alignment_planning_v1.py",
    "tools/evaluation/midplatform/run_evidence_record_approval_permission_alignment_planning_v1.py",
    "tools/evaluation/midplatform/verify_evidence_record_approval_permission_alignment_planning_v1.py",
)

ORCHESTRATION_SKELETON_CONSOLIDATION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "evidence_record_approval_permission_alignment_planning", "stage_term": "task_manager_core_orchestration_skeleton_consolidation"},
    {"base_term": "alignment_planning_only", "stage_term": "orchestration_consolidation_only"},
    {"base_term": "alignment_planning_pass", "stage_term": "orchestration_skeleton_consolidation_pass"},
    {"base_term": "alignment-planning-scope", "stage_term": "orchestration-consolidation-scope"},
)

ORCHESTRATION_SKELETON_CONSOLIDATION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_boundary_registry_go",
    "prior_candidate_lifecycle_go",
    "prior_alignment_planning_go",
    "orchestration_input_output_contract_complete",
    "orchestration_flow_skeleton_complete",
    "orchestration_non_execution_boundary_complete",
    "future_brain_interface_placeholder_complete",
    "orchestration_skeleton_not_runtime",
    "orchestration_plan_candidate_not_executed_plan",
    "route_candidate_not_route_execution",
    "drive_brain_placeholder_not_implementation",
    "reflection_brain_placeholder_not_implementation",
    "future_design_not_current_blocker",
    "orchestration_consolidation_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
