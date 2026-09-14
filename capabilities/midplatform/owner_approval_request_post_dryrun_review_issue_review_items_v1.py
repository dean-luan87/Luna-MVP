# -*- coding: utf-8 -*-
"""Owner approval request post-dryrun review issue review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-Issue-Review-v1-001"
)
SCOPE = "owner_approval_request_post_dryrun_review_issue_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "owner_approval_request_post_dryrun_review_issue_review_v1_smoke_v0"
)

ISSUANCE_PLANNING_ISSUE_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "issuance_planning_issue_review_v1_smoke_v0"
)

POST_DRYRUN_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1_smoke_v0"
)

POST_DRYRUN_REVIEW_STAGE_ID = (
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_ISSUE_REVIEW_READY_FOR_ISSUANCE_PLANNING_ISSUE_REVIEW_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_ISSUE_REVIEW_STILL_BLOCKED_BY_DIRECT_REQUEST_UPSTREAM_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Planning-Issue-Review-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "owner_approval_request_post_dryrun_review_issue_review_pass"

POST_DRYRUN_RUN_SCRIPT = (
    "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1"
)

REQUIRED_POST_DRYRUN_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
)

# Declared direct upstream order from post-dryrun review upstream GO checks (issues append order).
DIRECT_UPSTREAM_SPECS: Tuple[Tuple[str, str, str], ...] = (
    (
        "grant_owner_approval_request_planning_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1",
    ),
    (
        "input_output_registry_patch_root",
        "midplatform_protocol_input_output_symmetry_registry_patch_v1",
        "run_midplatform_protocol_input_output_symmetry_registry_patch_v1",
    ),
    (
        "protocol_shared_code_smoke_root",
        "midplatform_protocol_canonical_standard_shared_code_smoke_v1",
        "run_midplatform_protocol_canonical_standard_shared_code_smoke_v1",
    ),
    (
        "grant_owner_approval_request_dryrun_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1",
    ),
)

POST_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_report_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_dryrun_result_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_evidence_chain_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness_v1.json",
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
    "skipped_issuance_planning_rerun": True,
    "skipped_issuance_post_dryrun_review_rerun": True,
    "skipped_record_approval_closure_rerun": True,
    "skipped_integrated_implementation_rerun": True,
}
