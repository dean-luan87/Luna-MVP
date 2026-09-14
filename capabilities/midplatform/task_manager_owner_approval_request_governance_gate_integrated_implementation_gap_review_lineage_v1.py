# -*- coding: utf-8 -*-
"""Governance gate integrated implementation gap review — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

FINAL_DECISION_GO = FINAL_DECISION_COMPLETE

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_items_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_lineage_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_GAP_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_GAP_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_GAP_REVIEW_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_report_v1.json",
    "integrated_implementation_gap_review_v1.json",
    "integrated_implementation_direct_upstream_registry_v1.json",
    "integrated_implementation_first_non_go_upstream_review_v1.json",
    "integrated_implementation_upstream_artifact_visibility_review_v1.json",
    "integrated_implementation_upstream_boundary_gap_review_v1.json",
    "integrated_implementation_routing_gap_review_v1.json",
    "integrated_implementation_roadmap_gap_review_v1.json",
    "integrated_implementation_auth_prep_gap_review_v1.json",
    "integrated_implementation_closure_boundary_gap_review_v1.json",
    "integrated_implementation_slice_plan_gap_review_v1.json",
    "integrated_implementation_checklist_gap_review_v1.json",
    "integrated_implementation_rerun_review_v1.json",
    "authorization_preparation_dryrun_rerun_readiness_review_v1.json",
    "first_unresolved_gap_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "functional_slice_planning_gap_review_result_b_confirmed",
    "next_required_fix_confirmed",
    "integrated_implementation_files_exist",
    "integrated_implementation_rerun_attempted",
    "integrated_implementation_result_recorded",
    "integrated_implementation_direct_upstream_registry_exists",
    "first_non_go_direct_upstream_identified",
    "direct_upstream_visibility_review_exists",
    "routing_gap_review_exists",
    "roadmap_gap_review_exists",
    "auth_prep_gap_review_exists",
    "closure_boundary_gap_review_exists",
    "slice_plan_gap_review_exists",
    "checklist_gap_review_exists",
    "first_unresolved_gap_review_exists",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "no_fake_go_artifacts",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_BLOCKED,
)
