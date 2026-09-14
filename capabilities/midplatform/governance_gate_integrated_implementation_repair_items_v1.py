# -*- coding: utf-8 -*-
"""Governance gate integrated implementation repair — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Governance-Gate-Integrated-Implementation-Repair-v1-001"
SCOPE = "governance_gate_integrated_implementation_repair_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "governance_gate_integrated_implementation_repair_v1_smoke_v0"
)

GROUPED_REPAIR_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "owner_approval_remaining_chain_grouped_template_repair_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

GOVERNANCE_GATE_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1_smoke_v0"
)

POST_REVIEW_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1_smoke_v0"
)

STAGE_KEY = "governance_gate_integrated_implementation"
GOVERNANCE_RUNNER = "run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1"
GOVERNANCE_FINAL_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_READY_FOR_AUTHORIZATION_PREPARATION_DRYRUN_OR_FUNCTIONAL_SLICE_PLANNING"
)

GROUP_M_STAGES: Tuple[str, ...] = (
    "model_workflow_protocol_reuse_review",
    "model_adapter_priority_sequence_planning",
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_REPAIR_READY_FOR_NEXT_GOVERNANCE_STAGE_REPAIR_DECISION"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_REPAIR_STILL_BLOCKED_BY_GOVERNANCE_LOGIC_OR_TRACEABILITY_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Authorization-Preparation-DryRun-Repair-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "governance_gate_integrated_implementation_repair_complete"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "governance_gate_integrated_implementation_repair_only": True,
    "candidate_only": True,
    "no_execution_leakage": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_fake_go_artifacts": True,
    "no_issue_review_stage_created": True,
    "no_gap_review_stage_created": True,
    "no_rerun_review_stage_created": True,
    "no_original_stage_pollution": True,
    "no_model_download": True,
    "no_real_inference_execution": True,
}
