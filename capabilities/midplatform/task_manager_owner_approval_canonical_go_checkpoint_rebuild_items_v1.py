# -*- coding: utf-8 -*-
"""Task Manager / Owner Approval canonical GO checkpoint rebuild — items v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Canonical-GO-Checkpoint-Rebuild-v1-001"
SCOPE = "task_manager_owner_approval_canonical_go_checkpoint_rebuild_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_CANONICAL_GO_CHECKPOINT_REBUILD_COMPLETE_READY_FOR_REPAIR_PLAN_DECISION"
)

PASS_FLAG = "checkpoint_rebuild_complete"

REPO_ROOT_STR = "/Users/luanlei/Desktop/Luna-Core"
TMP_EVAL_PREFIX = f"{REPO_ROOT_STR}/_tmp_eval_out/"

# stage_key, runner_script, stage_family, stage_role, readiness_only
# Order is top-down scan order; runner names must exist under tools/evaluation/midplatform.
STAGE_CHAIN: Tuple[Tuple[str, str, str, str, bool], ...] = (
    ("input_output_registry_patch", "run_midplatform_protocol_input_output_symmetry_registry_patch_v1", "A_registry_protocol", "registry_patch", False),
    ("protocol_shared_code_smoke", "run_midplatform_protocol_canonical_standard_shared_code_smoke_v1", "A_registry_protocol", "protocol_smoke", False),
    ("task_manager_foundation_handoff_planning", "run_midplatform_task_manager_foundation_handoff_planning_v1", "A_registry_protocol", "foundation_planning", False),
    ("task_manager_freeze_authorization_planning", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1", "A_registry_protocol", "freeze_authorization_planning", False),
    ("grant_owner_approval_request_planning", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1", "B_owner_approval_request", "planning", False),
    ("grant_owner_approval_request_dryrun", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1", "B_owner_approval_request", "dryrun", False),
    ("grant_owner_approval_request_post_dryrun_review", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1", "B_owner_approval_request", "post_dryrun_review", False),
    ("grant_owner_approval_request_issuance_planning", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1", "C_issuance", "planning", False),
    ("grant_owner_approval_request_issuance_dryrun", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1", "C_issuance", "dryrun", False),
    ("grant_owner_approval_request_issuance_post_dryrun_review", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1", "C_issuance", "post_dryrun_review", False),
    ("record_approval_closure_planning", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1", "D_record_approval_closure", "planning", False),
    ("record_approval_closure_dryrun", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1", "D_record_approval_closure", "dryrun", False),
    ("record_approval_closure_post_dryrun_review", "run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1", "D_record_approval_closure", "post_dryrun_review", False),
    ("governance_gate_integrated_implementation", "run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1", "E_integrated_governance", "integrated_implementation", False),
    ("authorization_preparation_dryrun", "run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1", "E_integrated_governance", "authorization_preparation_dryrun", False),
    ("module_level_functional_slice_planning", "run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1", "E_integrated_governance", "functional_slice_planning", False),
    ("functional_slice_dryrun", "run_task_manager_owner_approval_request_functional_slice_dryrun_v1", "E_integrated_governance", "functional_slice_dryrun", False),
    ("module_governance_closure", "run_task_manager_owner_approval_request_module_governance_closure_v1", "E_integrated_governance", "module_governance_closure", False),
    ("module_handoff", "run_task_manager_owner_approval_request_module_handoff_v1", "E_integrated_governance", "module_handoff", False),
    ("broader_midplatform_closure_roadmap", "run_task_manager_broader_midplatform_closure_roadmap_v1", "E_integrated_governance", "broader_roadmap", False),
    ("model_workflow_protocol_reuse_review", "run_model_workflow_protocol_reuse_and_cleanup_review_v1", "F_slam_readiness", "model_workflow_review", True),
    ("model_adapter_priority_sequence_planning", "run_model_adapter_priority_sequence_planning_v1", "F_slam_readiness", "adapter_priority_planning", True),
    ("slam_spatial_mapping_model_smoke_io_inspection", "run_slam_spatial_mapping_model_smoke_io_inspection_v1", "F_slam_readiness", "slam_smoke_io", True),
    ("slam_spatial_mapping_adapter_skeleton", "run_slam_spatial_mapping_adapter_skeleton_v1", "F_slam_readiness", "slam_adapter_skeleton", True),
    ("slam_spatial_mapping_task_collaboration_planning", "run_slam_spatial_mapping_task_collaboration_planning_v1", "F_slam_readiness", "slam_task_collaboration", True),
    ("slam_spatial_mapping_task_collaboration_revalidation", "run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1", "F_slam_readiness", "slam_revalidation", True),
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "checkpoint_rebuild_only": True,
    "candidate_only": True,
    "review_only": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_action_output": True,
    "no_fake_go_artifacts": True,
    "no_original_stage_pollution": True,
    "no_model_download": True,
    "no_real_inference_execution": True,
    "owner_approval_required": False,
}

CHECKPOINT_STATUS_GO = "go_readable"
CHECKPOINT_STATUS_HOLD = "hold_readable"
CHECKPOINT_STATUS_BLOCKED = "blocked_readable"

GAP_TYPES: Tuple[str, ...] = (
    "artifact_missing",
    "verifier_report_missing",
    "summary_missing",
    "final_decision_drift",
    "upstream_ref_drift",
    "downstream_expectation_drift",
    "genuine_logic_hold",
    "registry_patch_not_go",
    "prior_stage_not_go",
    "runner_missing",
    "verifier_missing",
)

FIX_TYPES: Tuple[str, ...] = (
    "no_fix_needed",
    "regenerate_missing_verifier_report",
    "regenerate_summary",
    "fix_runner_output_schema",
    "fix_verifier_output_schema",
    "align_final_decision_mapping",
    "align_upstream_refs",
    "rerun_original_stage",
    "upstream_stage_not_go",
    "owner_decision_required",
)


def build_stage_specs() -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    keys = [row[0] for row in STAGE_CHAIN]
    for idx, (stage_key, runner_script, family, role, readiness_only) in enumerate(STAGE_CHAIN):
        stage_id = runner_script[4:] if runner_script.startswith("run_") else runner_script
        upstream = [keys[idx - 1]] if idx > 0 else []
        downstream = keys[idx + 1 : idx + 4]
        specs.append({
            "stage_key": stage_key,
            "stage_id": stage_id,
            "stage_name": stage_id,
            "stage_family": family,
            "stage_role": role,
            "runner_script": runner_script,
            "readiness_only": readiness_only,
            "upstream_refs": upstream,
            "downstream_refs": downstream,
            "downstream_consumers": downstream,
        })
    return specs
