# -*- coding: utf-8 -*-
"""Governance gate integrated implementation gap review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Implementation-Gap-Review-v1-001"
)
SCOPE = "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1_smoke_v0"
)

PLANNING_GAP_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_functional_slice_planning_gap_review_v1_smoke_v0"
)

INTEGRATED_IMPLEMENTATION_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1_smoke_v0"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_GAP_REVIEW_READY_FOR_FUNCTIONAL_SLICE_PLANNING_GAP_REVIEW_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_GAP_REVIEW_STILL_BLOCKED_BY_DIRECT_UPSTREAM_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Functional-Slice-Planning-Gap-Review-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = (
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_pass"
)

INTEGRATED_RUN_SCRIPT = (
    "run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1"
)

REQUIRED_INTEGRATED_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
)

# Declared direct upstream order from integrated implementation _meta / run() parameter order.
DIRECT_UPSTREAM_SPECS: Tuple[Tuple[str, str, str], ...] = (
    (
        "post_review_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1",
    ),
    (
        "final_gate_planning_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1",
    ),
)

INTEGRATED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.json",
    "integrated_roadmap_decision_v1.json",
    "issuance_authorization_preparation_package_v1.json",
    "missing_conditions_routing_v1.json",
    "real_issuance_precondition_checklist_v1.json",
    "record_approval_ack_evidence_closure_boundary_v1.json",
    "module_level_functional_slice_test_plan_v1.json",
    "governance_rule_reference_v1.json",
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
