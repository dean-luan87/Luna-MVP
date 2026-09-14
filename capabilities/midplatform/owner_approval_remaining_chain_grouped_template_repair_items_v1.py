# -*- coding: utf-8 -*-
"""Owner approval remaining chain grouped template repair — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Owner-Approval-Remaining-Chain-Grouped-Template-Repair-v1-001"
SCOPE = "owner_approval_remaining_chain_grouped_template_repair_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "owner_approval_remaining_chain_grouped_template_repair_v1_smoke_v0"
)

BATCH_DETECTION_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

GROUP_G_STAGES: Tuple[str, ...] = (
    "governance_gate_integrated_implementation",
    "module_governance_closure",
    "module_handoff",
    "broader_midplatform_closure_roadmap",
)

GROUP_M_STAGES: Tuple[str, ...] = (
    "model_workflow_protocol_reuse_review",
    "model_adapter_priority_sequence_planning",
)

SAFE_TEMPLATE_CANDIDATES: Tuple[str, ...] = (
    "grant_owner_approval_request_issuance_planning",
    "record_approval_closure_planning",
    "grant_owner_approval_request_issuance_dryrun",
    "record_approval_closure_dryrun",
    "authorization_preparation_dryrun",
    "functional_slice_dryrun",
    "grant_owner_approval_request_issuance_post_dryrun_review",
    "record_approval_closure_post_dryrun_review",
)

GROUP_P_CANDIDATES: Tuple[str, ...] = (
    "grant_owner_approval_request_issuance_planning",
    "record_approval_closure_planning",
)

GROUP_D_CANDIDATES: Tuple[str, ...] = (
    "grant_owner_approval_request_issuance_dryrun",
    "record_approval_closure_dryrun",
    "authorization_preparation_dryrun",
    "functional_slice_dryrun",
)

GROUP_R_CANDIDATES: Tuple[str, ...] = (
    "grant_owner_approval_request_issuance_post_dryrun_review",
    "record_approval_closure_post_dryrun_review",
)

ISSUANCE_CLOSURE_TEMPLATE_CHAIN: Tuple[str, ...] = (
    "grant_owner_approval_request_issuance_planning",
    "grant_owner_approval_request_issuance_dryrun",
    "grant_owner_approval_request_issuance_post_dryrun_review",
    "record_approval_closure_planning",
    "record_approval_closure_dryrun",
    "record_approval_closure_post_dryrun_review",
)

STAGE_RUNNERS: Dict[str, str] = {
    "grant_owner_approval_request_issuance_planning": (
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1"
    ),
    "record_approval_closure_planning": (
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1"
    ),
    "grant_owner_approval_request_issuance_dryrun": (
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1"
    ),
    "record_approval_closure_dryrun": (
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1"
    ),
    "authorization_preparation_dryrun": (
        "run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1"
    ),
    "functional_slice_dryrun": "run_task_manager_owner_approval_request_functional_slice_dryrun_v1",
    "grant_owner_approval_request_issuance_post_dryrun_review": (
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1"
    ),
    "record_approval_closure_post_dryrun_review": (
        "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1"
    ),
}

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_OWNER_APPROVAL_REMAINING_CHAIN_GROUPED_TEMPLATE_REPAIR_READY_FOR_GOVERNANCE_INDIVIDUAL_REPAIR_DECISION"
)
FINAL_DECISION_PARTIAL = (
    "MIDPLATFORM_OWNER_APPROVAL_REMAINING_CHAIN_GROUPED_TEMPLATE_REPAIR_PARTIAL_BLOCKED_BY_TEMPLATE_CANDIDATE_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Implementation-Repair-v1-001"
)
NEXT_PHASE_PARTIAL = PHASE_ID

PASS_FLAG = "grouped_template_repair_complete"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "owner_approval_remaining_chain_grouped_template_repair_only": True,
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
