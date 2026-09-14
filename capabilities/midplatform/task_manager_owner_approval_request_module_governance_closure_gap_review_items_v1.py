# -*- coding: utf-8 -*-
"""Module governance closure gap review — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Governance-Closure-Gap-Review-v1-001"
)
SCOPE = "task_manager_owner_approval_request_module_governance_closure_gap_review_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_governance_closure_gap_review_v1_smoke_v0"
)

HANDOFF_GAP_CLOSURE_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_handoff_gap_closure_v1_smoke_v0"
)

GOVERNANCE_CLOSURE_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_governance_closure_v1_smoke_v0"
)

FUNCTIONAL_SLICE_DRYRUN_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_functional_slice_dryrun_v1_smoke_v0"
)

FUNCTIONAL_SLICE_PLANNING_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_level_functional_slice_planning_v1_smoke_v0"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_GAP_REVIEW_READY_FOR_HANDOFF_GAP_CLOSURE_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_GAP_REVIEW_STILL_BLOCKED_BY_FUNCTIONAL_SLICE_DRYRUN_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-Gap-Closure-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "task_manager_owner_approval_request_module_governance_closure_gap_review_pass"

GOVERNANCE_CLOSURE_RUN_SCRIPT = (
    "run_task_manager_owner_approval_request_module_governance_closure_v1"
)
FUNCTIONAL_SLICE_DRYRUN_RUN_SCRIPT = (
    "run_task_manager_owner_approval_request_functional_slice_dryrun_v1"
)

REQUIRED_GOVERNANCE_CLOSURE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_governance_closure_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_governance_closure_v1.py",
)

REQUIRED_DRYRUN_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
)

OPTIONAL_GOVERNANCE_DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_V1_GO_NO_GO_PACK_V0.md",
)

DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "functional_slice_dryrun_report_v1.json",
    "functional_slice_dryrun_registry_v1.json",
    "owner_approval_request_candidate_lifecycle_dryrun_v1.json",
    "authorization_preparation_lifecycle_dryrun_v1.json",
    "record_approval_ack_evidence_closure_lifecycle_dryrun_v1.json",
    "absence_and_rollback_safety_lifecycle_dryrun_v1.json",
    "functional_slice_result_summary_v1.json",
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
