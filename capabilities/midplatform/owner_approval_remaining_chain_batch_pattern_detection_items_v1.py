# -*- coding: utf-8 -*-
"""Owner approval remaining chain batch pattern detection — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = (
    "Phase-Midplatform-Owner-Approval-Remaining-Chain-Batch-Pattern-Detection-And-Repair-Plan-v1-001"
)
SCOPE = "owner_approval_remaining_chain_batch_pattern_detection_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

GO_STAGE_KEYS: Tuple[str, ...] = (
    "input_output_registry_patch",
    "protocol_shared_code_smoke",
    "task_manager_foundation_handoff_planning",
    "task_manager_freeze_authorization_planning",
    "grant_owner_approval_request_planning",
    "grant_owner_approval_request_dryrun",
    "grant_owner_approval_request_post_dryrun_review",
)

FIRST_FAILED_STAGE_KEY = "grant_owner_approval_request_issuance_planning"
MIN_GO_STAGE_COUNT = 7
MIN_REMAINING_STAGE_COUNT = 19

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_OWNER_APPROVAL_REMAINING_CHAIN_BATCH_PATTERN_DETECTION_READY_FOR_GROUPED_REPAIR_EXECUTION"
)
NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Owner-Approval-Remaining-Chain-Grouped-Template-Repair-v1-001"
)

PASS_FLAG = "batch_pattern_detection_complete"

GAP_CLASSES: Tuple[str, ...] = (
    "downstream_expectation_gap",
    "runner_verifier_decision_drift",
    "evidence_traceability_gap",
    "schema_output_gap",
    "verifier_locator_gap",
    "genuine_logic_hold",
)

STAGE_FAMILIES: Tuple[str, ...] = (
    "planning",
    "dryrun",
    "post_dryrun_review",
    "closure",
    "governance",
    "handoff",
    "model_workflow",
    "model_adapter",
    "slam_readiness",
    "unknown",
)

REPAIR_GROUPS: Tuple[str, ...] = (
    "Group_P_planning_template_repair_candidates",
    "Group_D_dryrun_template_repair_candidates",
    "Group_R_review_template_repair_candidates",
    "Group_G_governance_individual_repair_required",
    "Group_M_model_slam_readiness_individual_repair_required",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "owner_approval_remaining_chain_batch_pattern_detection_only": True,
    "candidate_only": True,
    "review_only": True,
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

ROLE_TO_FAMILY: Dict[str, str] = {
    "planning": "planning",
    "freeze_authorization_planning": "planning",
    "foundation_planning": "planning",
    "functional_slice_planning": "planning",
    "adapter_priority_planning": "model_adapter",
    "dryrun": "dryrun",
    "authorization_preparation_dryrun": "dryrun",
    "functional_slice_dryrun": "dryrun",
    "post_dryrun_review": "post_dryrun_review",
    "integrated_implementation": "governance",
    "module_governance_closure": "governance",
    "module_handoff": "handoff",
    "broader_roadmap": "governance",
    "model_workflow_review": "model_workflow",
    "slam_smoke_io": "slam_readiness",
    "slam_adapter_skeleton": "slam_readiness",
    "slam_task_collaboration": "slam_readiness",
    "slam_revalidation": "slam_readiness",
}
