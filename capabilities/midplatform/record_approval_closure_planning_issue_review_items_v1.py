# -*- coding: utf-8 -*-
"""Record approval closure planning issue review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Planning-Issue-Review-v1-001"
)
SCOPE = "record_approval_closure_planning_issue_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "record_approval_closure_planning_issue_review_v1_smoke_v0"
)

DRYRUN_ISSUE_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "record_approval_closure_dryrun_issue_review_v1_smoke_v0"
)

PLANNING_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1_smoke_v0"
)

PLANNING_STAGE_ID = (
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_RECORD_APPROVAL_CLOSURE_PLANNING_ISSUE_REVIEW_READY_FOR_DRYRUN_ISSUE_REVIEW_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_RECORD_APPROVAL_CLOSURE_PLANNING_ISSUE_REVIEW_STILL_BLOCKED_BY_DIRECT_PRIOR_REVIEW_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-Issue-Review-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "record_approval_closure_planning_issue_review_pass"

PLANNING_RUN_SCRIPT = (
    "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1"
)

REQUIRED_PLANNING_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
)

# Direct prior review upstream from planning summary field owner_approval_request_issuance_post_dryrun_review_root.
DIRECT_PRIOR_REVIEW_SPEC: Tuple[str, str, str] = (
    "owner_approval_request_issuance_post_dryrun_review_root",
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1",
    "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1",
)

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "issue_review_only": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_action_output": True,
    "no_fake_go_artifacts": True,
    "skipped_dryrun_rerun": True,
    "skipped_post_dryrun_review_rerun": True,
    "skipped_integrated_implementation_rerun": True,
}
