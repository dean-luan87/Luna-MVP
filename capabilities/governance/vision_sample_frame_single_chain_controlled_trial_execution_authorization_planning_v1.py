# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Execution Authorization Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_planning_v1 import (
    TRIAL_SCOPE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Planning-v1-001"
PLANNING_SCOPE = "controlled_trial_execution_authorization_planning_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1"

UPSTREAM_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-DryRunAndReview-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_DRYRUN_AND_REVIEW_READY_FOR_EXECUTION_AUTHORIZATION_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Planning-v1-001"

FINAL_DECISION = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_PLANNING_READY_FOR_AUTHORIZATION_DRYRUN"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-DryRun-v1-001"
POST_EXECUTION_REVIEW_PHASE = (
    "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Post-Execution-Review-v1-001"
)

AUTHORIZATION_ALLOWED: Tuple[str, ...] = (
    "fixture_frame_metadata",
    "sample_frame_reference",
    "controlled_frame_reference",
    "prior_visual_candidate_reference",
)

AUTHORIZATION_FORBIDDEN: Tuple[str, ...] = (
    "live_camera",
    "new_camera_capture",
    "arbitrary_image_read",
    "vision_model_inference",
    "ocr_provider",
    "navigation_action",
    "task_commit",
    "user_facing_output",
    "worldmodel_write",
    "memory_write",
    "scene_delta_write",
    "fact_write",
)

EXECUTION_ALLOWLIST: Tuple[str, ...] = (
    "consume_controlled_input_reference",
    "validate_source_chain",
    "validate_frame_ref",
    "validate_timestamp",
    "generate_visual_observation_candidate",
    "write_trial_output_to_workspace_tmp_eval_out_only",
)

EXECUTION_BLOCKLIST: Tuple[str, ...] = (
    "live_camera",
    "image_capture",
    "arbitrary_filesystem_image_read",
    "model_inference",
    "fact_upgrade",
    "memory_worldmodel_write",
    "external_provider",
    "user_facing_output",
    "runtime_action",
)

PRE_EXECUTION_GATES: Tuple[str, ...] = (
    "authorization_scope_gate",
    "input_allowlist_gate",
    "source_chain_gate",
    "frame_ref_gate",
    "timestamp_gate",
    "no_live_camera_gate",
    "no_new_capture_gate",
    "no_arbitrary_image_read_gate",
    "no_model_inference_gate",
    "no_fact_write_gate",
    "no_worldmodel_memory_write_gate",
    "no_user_output_gate",
    "fallback_gate",
)

ABORT_CONDITIONS: Tuple[Dict[str, str], ...] = (
    {"trigger": "live_camera_requested", "action": "abort"},
    {"trigger": "new_capture_requested", "action": "abort"},
    {"trigger": "arbitrary_image_read_requested", "action": "abort"},
    {"trigger": "model_inference_requested", "action": "abort"},
    {"trigger": "missing_source_chain", "action": "abort"},
    {"trigger": "missing_frame_ref", "action": "abort"},
    {"trigger": "missing_timestamp", "action": "abort"},
    {"trigger": "candidate_attempts_fact_upgrade", "action": "abort"},
    {"trigger": "output_path_outside_allowed_directory", "action": "abort"},
    {"trigger": "worldmodel_or_memory_write_requested", "action": "abort"},
    {"trigger": "user_facing_output_requested", "action": "abort"},
    {"trigger": "safety_gate_failed", "action": "abort"},
)

NON_CLAIMS: Tuple[str, ...] = (
    "Authorization Planning GO ≠ execution authorized",
    "Authorization scope planned ≠ trial started",
    "Controlled fixture input ≠ live camera",
    "Candidate output ≠ visual fact",
    "Trial output logging ≠ WorldModel / Memory write",
    "Execution readiness ≠ bypass post-execution review",
    "Narrow authorization planned ≠ vision model allowed",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_trial_execution_authorization_planning_only": True,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_authorized_now": False,
        "runtime_enabled_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "midplatform_refactor_executed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "trial_scope": TRIAL_SCOPE,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root: str,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    upstream_root = Path(
        vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root
    ).expanduser().resolve()

    plan_out = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else upstream_root.parent / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning"
    )

    execution_output_dir = (
        upstream_root.parent / "vision_sample_frame_single_chain_controlled_trial_execution"
    )

    blockers: List[str] = []
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(upstream_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_dryrun_and_review_root": str(upstream_root),
        "authorization_planning_output_root": str(plan_out),
        "planned_execution_output_directory": str(execution_output_dir),
    }

    up_sm = _try_read_json(upstream_root / "summary.json") or {}
    up_vr = _try_read_json(upstream_root / "verifier_report.json") or {}
    review = _try_read_json(upstream_root / "controlled_trial_review_result_v1.json") or {}
    positive = _try_read_json(upstream_root / "controlled_trial_positive_flow_result_v1.json") or {}
    blocked = _try_read_json(upstream_root / "controlled_trial_blocked_flow_result_v1.json") or {}
    gates = _try_read_json(upstream_root / "controlled_trial_gate_result_v1.json") or {}
    stops = _try_read_json(upstream_root / "controlled_trial_stop_condition_result_v1.json") or {}
    audit = _try_read_json(upstream_root / "controlled_trial_no_runtime_boundary_audit_v1.json") or {}
    auth_ready = _try_read_json(
        upstream_root / "controlled_trial_execution_authorization_readiness_v1.json"
    ) or {}

    trusted = up_vr.get("verifier") == "GO" and up_vr.get("passed") is True
    summary_ok = (
        up_sm.get("boundary_ok") is True
        and up_sm.get("phase") == UPSTREAM_PHASE
        and up_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and up_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not trusted and not summary_ok:
        blockers.append("dryrun+review verifier must be GO")
    if (up_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")
    if review.get("review_pass") is not True:
        blockers.append("controlled_trial_review must pass")
    if positive.get("all_pass") is not True:
        blockers.append("4 positive flows must pass")
    if blocked.get("all_stop_or_hold") is not True:
        blockers.append("8 blocked flows must stop/hold")
    if gates.get("enforcement_pass") is not True:
        blockers.append("13 gates enforcement_pass required")
    if stops.get("verification_pass") is not True:
        blockers.append("12 stop conditions must be enforced")
    if audit.get("audit_pass") is not True:
        blockers.append("no_runtime_boundary_audit must pass")
    if up_sm.get("controlled_trial_started_now") is True:
        blockers.append("controlled_trial_started_now must be false")
    if up_sm.get("trial_execution_authorized_now") is True:
        blockers.append("trial_execution_authorized_now must be false")
    if auth_ready.get("ready_for_execution_authorization_planning") is not True:
        blockers.append("authorization readiness must be true")

    for field in RUNTIME_BOUNDARY_FIELDS:
        if up_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    boundary_ok = len(blockers) == 0

    policy = {
        "policy_id": "execution_authorization_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "narrow_controlled_fixture_execution_authorization_design_only",
        "chain_id": "vision_sample_frame",
        "note": "Planning GO does not grant execution; live camera remains forbidden",
        **meta,
    }

    input_review = {
        "review_id": "dryrun_and_review_input_review_v1",
        "upstream_root": str(upstream_root),
        "upstream_verifier": up_vr.get("verifier"),
        "upstream_final_decision": up_sm.get("final_decision"),
        "positive_flows_passed": up_sm.get("positive_flows_passed"),
        "blocked_flows_enforced": up_sm.get("blocked_flows_enforced"),
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    auth_scope = {
        "scope_id": "controlled_trial_execution_authorization_scope_v1",
        "trial_scope": TRIAL_SCOPE,
        "authorization_narrow": True,
        "allowed_future_inputs": list(AUTHORIZATION_ALLOWED),
        "explicitly_forbidden": list(AUTHORIZATION_FORBIDDEN),
        "live_camera_never_authorized_in_this_planning": True,
        **meta,
    }

    allowlist = {
        "policy_id": "controlled_trial_execution_allowlist_v1",
        "allowed_operations": list(EXECUTION_ALLOWLIST),
        **meta,
    }

    blocklist = {
        "policy_id": "controlled_trial_execution_blocklist_v1",
        "blocked_operations": list(EXECUTION_BLOCKLIST),
        **meta,
    }

    gate_matrix = {
        "matrix_id": "controlled_trial_pre_execution_gate_matrix_v1",
        "gates": [
            {
                "gate_id": g,
                "status": "required_before_any_execution_authorization_grant",
                "enforcement": "narrow_fixture_only",
            }
            for g in PRE_EXECUTION_GATES
        ],
        "gates_total": len(PRE_EXECUTION_GATES),
        **meta,
    }

    window_plan = {
        "policy_id": "controlled_trial_execution_window_authorization_plan_v1",
        "execution_window_type": "controlled_fixture_only",
        "max_trial_scope": "single_chain",
        "max_output_count": 3,
        "output_directory": str(execution_output_dir),
        "no_live_input": True,
        "no_external_provider": True,
        "no_user_facing_output": True,
        "post_execution_review_required": True,
        "post_execution_review_phase": POST_EXECUTION_REVIEW_PHASE,
        **meta,
    }

    abort_matrix = {
        "matrix_id": "controlled_trial_abort_condition_matrix_v1",
        "conditions": list(ABORT_CONDITIONS),
        "immediate_abort_triggers": [c["trigger"] for c in ABORT_CONDITIONS],
        **meta,
    }

    output_contract = {
        "contract_id": "controlled_trial_output_contract_v1",
        "output_type": "visual_observation_candidate",
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "trial_scope": TRIAL_SCOPE,
        "source_chain_present": True,
        "frame_ref_present": True,
        "timestamp_present": True,
        **meta,
    }

    logging_policy = {
        "policy_id": "controlled_trial_execution_logging_policy_v1",
        "allowed_write_root": str(execution_output_dir),
        "workspace_fallback_only": True,
        "forbidden_targets": [
            "repo__eval_out",
            "WorldModel",
            "Memory",
            "SceneDelta",
            "protected",
            "HR",
            "DnAE",
        ],
        **meta,
    }

    post_exec_req = {
        "requirement_id": "controlled_trial_post_execution_review_requirement_v1",
        "required_phase": POST_EXECUTION_REVIEW_PHASE,
        "mandatory_after_execution": True,
        "cannot_bypass": True,
        "review_checks": [
            "no_runtime_boundary_violation",
            "output_contract_honored",
            "no_fact_write",
            "logging_boundary_respected",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "execution_authorization_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "execution_authorization_planning_readiness_decision_v1",
        "final_decision": (
            FINAL_DECISION
            if boundary_ok
            else "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_PLANNING_REQUIRES_FIXES"
        ),
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "ready_for_authorization_dryrun": boundary_ok,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "upstream_blockers": blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "pre_execution_gates_count": len(PRE_EXECUTION_GATES),
        **meta,
    }

    return {
        "execution_authorization_planning_policy": policy,
        "dryrun_and_review_input_review": input_review,
        "controlled_trial_execution_authorization_scope": auth_scope,
        "controlled_trial_execution_allowlist": allowlist,
        "controlled_trial_execution_blocklist": blocklist,
        "controlled_trial_pre_execution_gate_matrix": gate_matrix,
        "controlled_trial_execution_window_authorization_plan": window_plan,
        "controlled_trial_abort_condition_matrix": abort_matrix,
        "controlled_trial_output_contract": output_contract,
        "controlled_trial_execution_logging_policy": logging_policy,
        "controlled_trial_post_execution_review_requirement": post_exec_req,
        "execution_authorization_non_claims_register": non_claims,
        "execution_authorization_planning_readiness_decision": readiness,
        "summary": summary,
    }
