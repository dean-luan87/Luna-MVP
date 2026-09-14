# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Execution Authorization Request Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UPSTREAM_REQUIRED_FINAL,
    PLANNED_EXECUTION_OUTPUT_DIR,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    ABORT_CONDITIONS,
    AUTHORIZATION_ALLOWED,
    AUTHORIZATION_FORBIDDEN,
    POST_EXECUTION_REVIEW_PHASE,
    PRE_EXECUTION_GATES,
    TRIAL_SCOPE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-Planning-v1-001"
PLANNING_SCOPE = "execution_authorization_request_planning_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1"

UPSTREAM_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-DryRunAndReview-v1-001"
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-Planning-v1-001"

FINAL_DECISION = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-DryRun-v1-001"

TARGET_EXECUTION_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-v1-001"
REQUEST_SOURCE_PHASE = UPSTREAM_PHASE
CHAIN_ID = "vision_sample_frame_single_chain"
REQUEST_TYPE = "controlled_trial_execution_authorization_request"

LIFECYCLE_STATES: Tuple[str, ...] = (
    "planning_defined",
    "artifact_generation_planning",
    "artifact_generated",
    "request_send_planning",
    "request_sent",
    "grant_planning",
    "grant_issued",
    "execution_window_opened",
    "controlled_trial_execution",
    "post_execution_review",
)

NON_GRANT_STATEMENTS: Tuple[str, ...] = (
    "request planning ≠ request artifact generated",
    "request artifact generated ≠ request sent",
    "request sent ≠ grant issued",
    "grant issued ≠ trial execution started",
    "trial execution completed ≠ visual fact",
    "trial output logging ≠ WorldModel / Memory write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Request Planning GO ≠ request artifact generated",
    "Request Planning GO ≠ request sent",
    "Request Planning GO ≠ grant issued",
    "Request Planning GO ≠ trial execution authorized",
    "Request schema defined ≠ controlled trial started",
    "Lifecycle planning_defined ≠ execution window opened",
    "Fixture-bound request scope ≠ live camera allowed",
    "Candidate output contract in request ≠ visual fact",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "user_facing_output_generated_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "execution_authorization_request_planning_only": True,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "execution_authorization_granted_now": False,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
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


def _validate_upstream(dryrun_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    sm = _try_read_json(dryrun_root / "summary.json") or {}
    vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    scope_res = _try_read_json(dryrun_root / "authorization_scope_consumption_result_v1.json") or {}
    allow_block = _try_read_json(dryrun_root / "execution_allowlist_blocklist_review_v1.json") or {}
    gates = _try_read_json(dryrun_root / "pre_execution_gate_consumption_result_v1.json") or {}
    abort = _try_read_json(dryrun_root / "abort_condition_consumption_result_v1.json") or {}
    output = _try_read_json(dryrun_root / "output_contract_review_v1.json") or {}
    post = _try_read_json(dryrun_root / "post_execution_review_requirement_result_v1.json") or {}
    non_release = _try_read_json(dryrun_root / "authorization_non_release_review_v1.json") or {}
    readiness = _try_read_json(dryrun_root / "trial_execution_readiness_decision_v1.json") or {}

    trusted = vr.get("verifier") == "GO" and vr.get("passed") is True
    summary_ok = (
        sm.get("boundary_ok") is True
        and sm.get("phase") == UPSTREAM_PHASE
        and sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not trusted and not summary_ok:
        blockers.append("authorization dryrun+review verifier must be GO")
    if scope_res.get("consumption_pass") is not True:
        blockers.append("authorization scope consumption must pass")
    if allow_block.get("allowlist_pass") is not True or allow_block.get("blocklist_pass") is not True:
        blockers.append("allowlist/blocklist review must pass")
    if gates.get("all_dryrun_pass") is not True:
        blockers.append("13 pre-execution gates dryrun must pass")
    if gates.get("gates_passed") != len(PRE_EXECUTION_GATES):
        blockers.append("pre_execution gates count mismatch")
    if abort.get("all_consumable") is not True:
        blockers.append("abort conditions must be consumable")
    if abort.get("conditions_total") != len(ABORT_CONDITIONS):
        blockers.append("abort conditions count mismatch")
    if output.get("review_pass") is not True:
        blockers.append("output contract review must pass")
    if post.get("post_execution_review_required") is not True:
        blockers.append("post_execution_review_required must be true")
    if non_release.get("review_pass") is not True:
        blockers.append("authorization non-release review must pass")
    if readiness.get("ready_for_authorization_request_planning") is not True:
        blockers.append("ready_for_authorization_request_planning must be true")
    if sm.get("trial_execution_authorized_now") is True:
        blockers.append("trial_execution_authorized_now must be false")
    if sm.get("controlled_trial_started_now") is True:
        blockers.append("controlled_trial_started_now must be false")
    if sm.get("execution_window_opened_now") is True:
        blockers.append("execution_window_opened_now must be false")

    return blockers, {
        "dryrun_sm": sm,
        "dryrun_vr": vr,
        "scope_res": scope_res,
        "allow_block": allow_block,
        "gates": gates,
        "abort": abort,
        "output": output,
        "post": post,
        "non_release": non_release,
        "readiness": readiness,
    }


def run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root: str,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    upstream_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root
    ).expanduser().resolve()

    plan_out = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else upstream_root.parent
        / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning"
    )

    blockers, ctx = _validate_upstream(upstream_root)
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(upstream_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_authorization_dryrun_and_review_root": str(upstream_root),
        "authorization_request_planning_output_root": str(plan_out),
        "planned_execution_output_directory": PLANNED_EXECUTION_OUTPUT_DIR,
    }

    boundary_ok = len(blockers) == 0

    policy = {
        "policy_id": "execution_authorization_request_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "controlled_trial_execution_authorization_request_structure_planning_only",
        "note": "Does not generate request artifact, send request, grant authorization, or start trial",
        **meta,
    }

    input_review = {
        "review_id": "authorization_dryrun_and_review_input_review_v1",
        "upstream_root": str(upstream_root),
        "upstream_verifier": ctx["dryrun_vr"].get("verifier"),
        "upstream_final_decision": ctx["dryrun_sm"].get("final_decision"),
        "scope_consumption_pass": ctx["scope_res"].get("consumption_pass"),
        "allowlist_pass": ctx["allow_block"].get("allowlist_pass"),
        "blocklist_pass": ctx["allow_block"].get("blocklist_pass"),
        "gates_dryrun_pass": ctx["gates"].get("all_dryrun_pass"),
        "abort_consumable": ctx["abort"].get("all_consumable"),
        "output_contract_pass": ctx["output"].get("review_pass"),
        "post_execution_review_required": ctx["post"].get("post_execution_review_required"),
        "non_release_pass": ctx["non_release"].get("review_pass"),
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    identity_schema = {
        "schema_id": "authorization_request_identity_schema_v1",
        "request_id": "{chain_id}_{request_type}_{uuid}",
        "request_type": REQUEST_TYPE,
        "target_phase": TARGET_EXECUTION_PHASE,
        "source_phase": REQUEST_SOURCE_PHASE,
        "chain_id": CHAIN_ID,
        "requested_execution_window": "single_chain",
        "max_output_count": 3,
        "post_execution_review_required": True,
        "post_execution_review_phase": POST_EXECUTION_REVIEW_PHASE,
        "artifact_not_generated_in_this_phase": True,
        **meta,
        "trial_scope": "controlled_fixture_only",
        "chain_trial_scope": TRIAL_SCOPE,
    }

    scope_binding = {
        "binding_id": "authorization_request_scope_binding_v1",
        "allowed_bindings": list(AUTHORIZATION_ALLOWED),
        "forbidden_bindings": list(AUTHORIZATION_FORBIDDEN),
        "live_camera_forbidden": True,
        "model_inference_forbidden": True,
        "fact_write_forbidden": True,
        "worldmodel_memory_scene_delta_write_forbidden": True,
        **meta,
    }

    input_binding = {
        "binding_id": "authorization_request_input_binding_v1",
        "input_kinds": list(AUTHORIZATION_ALLOWED),
        "requires_source_chain": True,
        "requires_frame_ref": True,
        "requires_timestamp": True,
        "no_live_input": True,
        "no_arbitrary_image_read": True,
        **meta,
    }

    window_binding = {
        "binding_id": "authorization_request_execution_window_binding_v1",
        "execution_window_type": "controlled_fixture_only",
        "max_trial_scope": "single_chain",
        "max_output_count": 3,
        "output_directory": PLANNED_EXECUTION_OUTPUT_DIR,
        "no_live_input": True,
        "no_external_provider": True,
        "no_user_facing_output": True,
        "execution_window_opened_in_this_phase": False,
        **meta,
    }

    gate_binding = {
        "binding_id": "authorization_request_gate_binding_v1",
        "pre_execution_gates": list(PRE_EXECUTION_GATES),
        "gates_total": len(PRE_EXECUTION_GATES),
        "all_required_before_grant": True,
        **meta,
    }

    abort_binding = {
        "binding_id": "authorization_request_abort_binding_v1",
        "abort_conditions": list(ABORT_CONDITIONS),
        "conditions_total": len(ABORT_CONDITIONS),
        "immediate_abort_on_boundary_violation": True,
        **meta,
    }

    output_binding = {
        "binding_id": "authorization_request_output_contract_binding_v1",
        "output_type": "visual_observation_candidate",
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "trial_scope": TRIAL_SCOPE,
        "source_chain_present": True,
        "frame_ref_present": True,
        "timestamp_present": True,
        "allowed_output_directory": PLANNED_EXECUTION_OUTPUT_DIR,
        **meta,
    }

    post_binding = {
        "binding_id": "authorization_request_post_execution_review_binding_v1",
        "required_phase": POST_EXECUTION_REVIEW_PHASE,
        "mandatory_after_execution": True,
        "cannot_bypass": True,
        **meta,
    }

    non_grant = {
        "statement_id": "authorization_request_non_grant_statement_v1",
        "statements": list(NON_GRANT_STATEMENTS),
        "request_planning_only": True,
        "grant_not_issued_in_this_phase": True,
        **meta,
    }

    lifecycle = {
        "plan_id": "authorization_request_lifecycle_plan_v1",
        "states": list(LIFECYCLE_STATES),
        "current_state": "planning_defined",
        "transitions_planned_only": True,
        "next_allowed_states_from_planning_defined": ["artifact_generation_planning"],
        "terminal_requires_post_execution_review": True,
        **meta,
    }

    non_claims = {
        "register_id": "authorization_request_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "authorization_request_planning_readiness_decision_v1",
        "final_decision": (
            FINAL_DECISION
            if boundary_ok
            else "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_REQUEST_PLANNING_REQUIRES_FIXES"
        ),
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "ready_for_authorization_request_dryrun": boundary_ok,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "execution_authorization_granted_now": False,
        "lifecycle_current_state": "planning_defined",
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
        "lifecycle_current_state": "planning_defined",
        "request_type": REQUEST_TYPE,
        "chain_id": CHAIN_ID,
        **meta,
    }

    return {
        "execution_authorization_request_planning_policy": policy,
        "authorization_dryrun_and_review_input_review": input_review,
        "authorization_request_identity_schema": identity_schema,
        "authorization_request_scope_binding": scope_binding,
        "authorization_request_input_binding": input_binding,
        "authorization_request_execution_window_binding": window_binding,
        "authorization_request_gate_binding": gate_binding,
        "authorization_request_abort_binding": abort_binding,
        "authorization_request_output_contract_binding": output_binding,
        "authorization_request_post_execution_review_binding": post_binding,
        "authorization_request_non_grant_statement": non_grant,
        "authorization_request_lifecycle_plan": lifecycle,
        "authorization_request_non_claims_register": non_claims,
        "authorization_request_planning_readiness_decision": readiness,
        "summary": summary,
    }
