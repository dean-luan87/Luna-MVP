# -*- coding: utf-8 -*-
"""Issuance planning issue review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Planning-Issue-Review-v1-001"
)
SCOPE = "issuance_planning_issue_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "issuance_planning_issue_review_v1_smoke_v0"
)

ISSUANCE_POST_DRYRUN_ISSUE_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "issuance_post_dryrun_review_issue_review_v1_smoke_v0"
)

ISSUANCE_PLANNING_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1_smoke_v0"
)

ISSUANCE_PLANNING_STAGE_ID = (
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_ISSUANCE_PLANNING_ISSUE_REVIEW_READY_FOR_ISSUANCE_POST_DRYRUN_REVIEW_ISSUE_REVIEW_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_ISSUANCE_PLANNING_ISSUE_REVIEW_STILL_BLOCKED_BY_DIRECT_PRIOR_UPSTREAM_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Post-DryRun-Review-Issue-Review-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "issuance_planning_issue_review_pass"

ISSUANCE_PLANNING_RUN_SCRIPT = (
    "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1"
)

REQUIRED_ISSUANCE_PLANNING_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py",
)

# Declared prior upstream order from issuance planning upstream GO checks (issues append order).
DIRECT_PRIOR_UPSTREAM_SPECS: Tuple[Tuple[str, str, str], ...] = (
    (
        "grant_owner_approval_request_post_dryrun_review_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1",
    ),
    (
        "grant_owner_approval_request_planning_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1",
    ),
    (
        "grant_owner_approval_request_dryrun_root",
        "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1",
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1",
    ),
    (
        "input_output_registry_patch_root",
        "midplatform_protocol_input_output_symmetry_registry_patch_v1",
        "run_midplatform_protocol_input_output_symmetry_registry_patch_v1",
    ),
)

ISSUANCE_PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_prerequisite_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness_v1.json",
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
    "skipped_issuance_post_dryrun_review_rerun": True,
    "skipped_record_approval_closure_planning_rerun": True,
    "skipped_integrated_implementation_rerun": True,
}
