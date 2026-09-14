# -*- coding: utf-8 -*-
"""Functional slice planning gap review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Functional-Slice-Planning-Gap-Review-v1-001"
)
SCOPE = "task_manager_owner_approval_request_functional_slice_planning_gap_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_functional_slice_planning_gap_review_v1_smoke_v0"
)

GOVERNANCE_GAP_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_governance_closure_gap_review_v1_smoke_v0"
)

FUNCTIONAL_SLICE_PLANNING_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_level_functional_slice_planning_v1_smoke_v0"
)

AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_authorization_preparation_dryrun_v1_smoke_v0"
)

INTEGRATED_IMPLEMENTATION_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1_smoke_v0"
)

AUTHORIZATION_PREPARATION_PLANNING_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_authorization_preparation_planning_v1_smoke_v0"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_PLANNING_GAP_REVIEW_READY_FOR_GOVERNANCE_CLOSURE_GAP_REVIEW_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_PLANNING_GAP_REVIEW_STILL_BLOCKED_BY_AUTHORIZATION_PREPARATION_DRYRUN_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Governance-Closure-Gap-Review-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "task_manager_owner_approval_request_functional_slice_planning_gap_review_pass"

FUNCTIONAL_SLICE_PLANNING_RUN_SCRIPT = (
    "run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1"
)
AUTHORIZATION_PREPARATION_DRYRUN_RUN_SCRIPT = (
    "run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1"
)

REQUIRED_PLANNING_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
)

REQUIRED_AUTH_DRYRUN_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
)

AUTH_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "authorization_preparation_dryrun_report_v1.json",
    "authorization_preparation_package_validation_v1.json",
    "authorization_precondition_validation_v1.json",
    "missing_conditions_routing_validation_v1.json",
    "real_issuance_safety_boundary_validation_v1.json",
    "functional_slice_followup_reference_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "gap_review_only": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_action_output": True,
    "no_fake_go_artifacts": True,
}
