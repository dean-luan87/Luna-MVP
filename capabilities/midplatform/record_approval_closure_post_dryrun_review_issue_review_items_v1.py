# -*- coding: utf-8 -*-
"""Record approval closure post-dryrun review issue review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-Issue-Review-v1-001"
)
SCOPE = "record_approval_closure_post_dryrun_review_issue_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "record_approval_closure_post_dryrun_review_issue_review_v1_smoke_v0"
)

INTEGRATED_IMPL_GAP_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1_smoke_v0"
)

POST_DRYRUN_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1_smoke_v0"
)

POST_DRYRUN_STAGE_ID = (
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_ISSUE_REVIEW_READY_FOR_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_GAP_REVIEW_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_ISSUE_REVIEW_STILL_BLOCKED_BY_DIRECT_DRYRUN_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Implementation-Gap-Review-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "record_approval_closure_post_dryrun_review_issue_review_pass"

POST_DRYRUN_RUN_SCRIPT = (
    "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1"
)

REQUIRED_POST_DRYRUN_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
)

# Direct dryrun upstream from post-dryrun review summary field record_approval_closure_dryrun_root.
DIRECT_DRYRUN_SPEC: Tuple[str, str, str] = (
    "record_approval_closure_dryrun_root",
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1",
    "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1",
)

POST_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_result_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_next_phase_readiness_v1.json",
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
    "skipped_integrated_implementation_rerun": True,
}
