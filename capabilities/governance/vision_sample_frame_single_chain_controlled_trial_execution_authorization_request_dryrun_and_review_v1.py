# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Execution Authorization Request DryRun+Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1 import (
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
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_v1 import (
    CHAIN_ID,
    FINAL_DECISION as UPSTREAM_REQUIRED_FINAL,
    LIFECYCLE_STATES,
    NON_GRANT_STATEMENTS,
    REQUEST_SOURCE_PHASE,
    REQUEST_TYPE,
    TARGET_EXECUTION_PHASE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-DryRunAndReview-v1-001"
SCOPE = "execution_authorization_request_dryrun_and_review_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review_v1"

UPSTREAM_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-Planning-v1-001"
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-DryRun-v1-001"

FINAL_DECISION_GO = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_REQUEST_DRYRUN_AND_REVIEW_READY_FOR_REQUEST_ARTIFACT_GENERATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_REQUEST_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-Artifact-Generation-Planning-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-Issue-Review-v1-001"
)

NON_CLAIMS: Tuple[str, ...] = (
    "Request DryRun+Review GO ≠ request artifact generated",
    "Request DryRun+Review GO ≠ request sent",
    "Request DryRun+Review GO ≠ grant issued",
    "Request DryRun+Review GO ≠ trial execution authorized",
    "Lifecycle consumable ≠ lifecycle advanced",
    "Non-grant review pass ≠ execution window opened",
    "Binding consumption pass ≠ controlled trial started",
    "Ready for Artifact Generation Planning ≠ Trial Execution",
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
        "execution_authorization_request_dryrun_and_review_only": True,
        "simulated": True,
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
        "lifecycle_current_state": "planning_defined",
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _validate_upstream(planning_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    sm = _try_read_json(planning_root / "summary.json") or {}
    vr = _try_read_json(planning_root / "verifier_report.json") or {}
    identity = _try_read_json(planning_root / "authorization_request_identity_schema_v1.json") or {}
    scope = _try_read_json(planning_root / "authorization_request_scope_binding_v1.json") or {}
    lifecycle = _try_read_json(planning_root / "authorization_request_lifecycle_plan_v1.json") or {}
    readiness = _try_read_json(planning_root / "authorization_request_planning_readiness_decision_v1.json") or {}

    trusted = vr.get("verifier") == "GO" and vr.get("passed") is True
    summary_ok = (
        sm.get("boundary_ok") is True
        and sm.get("phase") == UPSTREAM_PHASE
        and sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not trusted and not summary_ok:
        blockers.append("request planning verifier must be GO")
    if sm.get("execution_authorization_request_planning_only") is not True:
        blockers.append("execution_authorization_request_planning_only must be true")
    if sm.get("authorization_request_artifact_generated_now") is True:
        blockers.append("authorization_request_artifact_generated_now must be false")
    if sm.get("authorization_request_sent_now") is True:
        blockers.append("authorization_request_sent_now must be false")
    if sm.get("execution_authorization_granted_now") is True:
        blockers.append("execution_authorization_granted_now must be false")
    if sm.get("lifecycle_current_state") != "planning_defined":
        blockers.append("lifecycle_current_state must be planning_defined")
    if lifecycle.get("current_state") != "planning_defined":
        blockers.append("lifecycle plan current_state must be planning_defined")
    if readiness.get("ready_for_authorization_request_dryrun") is not True:
        blockers.append("ready_for_authorization_request_dryrun must be true")
    if identity.get("request_type") != REQUEST_TYPE:
        blockers.append("request_type mismatch in planning")
    if identity.get("trial_scope") != "controlled_fixture_only":
        blockers.append("identity trial_scope must be controlled_fixture_only")

    allowed = set(scope.get("allowed_bindings") or [])
    for item in AUTHORIZATION_ALLOWED:
        if item not in allowed:
            blockers.append(f"scope binding missing: {item}")

    return blockers, {
        "planning_sm": sm,
        "planning_vr": vr,
        "identity": identity,
        "scope": scope,
        "input_binding": _try_read_json(planning_root / "authorization_request_input_binding_v1.json") or {},
        "window_binding": _try_read_json(planning_root / "authorization_request_execution_window_binding_v1.json") or {},
        "gate_binding": _try_read_json(planning_root / "authorization_request_gate_binding_v1.json") or {},
        "abort_binding": _try_read_json(planning_root / "authorization_request_abort_binding_v1.json") or {},
        "output_binding": _try_read_json(planning_root / "authorization_request_output_contract_binding_v1.json") or {},
        "post_binding": _try_read_json(planning_root / "authorization_request_post_execution_review_binding_v1.json") or {},
        "non_grant": _try_read_json(planning_root / "authorization_request_non_grant_statement_v1.json") or {},
        "lifecycle": lifecycle,
        "readiness": readiness,
    }


def _consume_identity(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    ident = ctx["identity"]
    checks = {
        "request_type": ident.get("request_type") == REQUEST_TYPE,
        "target_phase": ident.get("target_phase") == TARGET_EXECUTION_PHASE,
        "source_phase": ident.get("source_phase") == REQUEST_SOURCE_PHASE,
        "chain_id": ident.get("chain_id") == CHAIN_ID,
        "trial_scope": ident.get("trial_scope") == "controlled_fixture_only",
        "requested_execution_window": ident.get("requested_execution_window") == "single_chain",
        "max_output_count": ident.get("max_output_count") == 3,
        "post_execution_review_required": ident.get("post_execution_review_required") is True,
    }
    return {
        "result_id": "request_identity_consumption_result_v1",
        "consumption_pass": all(checks.values()),
        "checks": checks,
        **meta,
    }


def _consume_scope(meta: Dict[str, Any]) -> Dict[str, Any]:
    forbidden_checks = {item: True for item in AUTHORIZATION_FORBIDDEN}
    return {
        "result_id": "request_scope_binding_consumption_result_v1",
        "consumption_pass": True,
        "allowed_confirmed": list(AUTHORIZATION_ALLOWED),
        "forbidden_confirmed": list(AUTHORIZATION_FORBIDDEN),
        "forbidden_enforcement_simulated": forbidden_checks,
        "live_camera_excluded": True,
        "model_inference_excluded": True,
        "fact_write_excluded": True,
        **meta,
    }


def _consume_input_binding(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    inp = ctx["input_binding"]
    checks = [
        inp.get("requires_source_chain") is True,
        inp.get("requires_frame_ref") is True,
        inp.get("requires_timestamp") is True,
        inp.get("no_live_input") is True,
        inp.get("no_arbitrary_image_read") is True,
    ]
    return {
        "result_id": "request_input_binding_consumption_result_v1",
        "consumption_pass": all(checks),
        **meta,
    }


def _window_binding_result(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    win = ctx["window_binding"]
    out_dir = str(win.get("output_directory") or PLANNED_EXECUTION_OUTPUT_DIR)
    checks = {
        "execution_window_type": win.get("execution_window_type") == "controlled_fixture_only",
        "max_trial_scope": win.get("max_trial_scope") == "single_chain",
        "max_output_count": win.get("max_output_count") == 3,
        "output_directory_workspace": "Luna-Workspace-Min" in out_dir,
        "no_live_input": win.get("no_live_input") is True,
        "no_external_provider": win.get("no_external_provider") is True,
        "no_user_facing_output": win.get("no_user_facing_output") is True,
    }
    window_not_opened = meta.get("execution_window_opened_now") is False
    return {
        "result_id": "request_execution_window_binding_result_v1",
        "binding_pass": all(checks.values()) and window_not_opened,
        "checks": checks,
        "output_directory": out_dir,
        "execution_window_opened_now": False,
        **meta,
    }


def _gate_abort_binding_result(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    gates = ctx["gate_binding"]
    abort = ctx["abort_binding"]
    gate_ids = {g for g in (gates.get("pre_execution_gates") or [])}
    gates_ok = all(g in gate_ids for g in PRE_EXECUTION_GATES) and gates.get("gates_total") == len(PRE_EXECUTION_GATES)
    abort_triggers = {c.get("trigger") for c in (abort.get("abort_conditions") or [])}
    abort_ok = all(c["trigger"] in abort_triggers for c in ABORT_CONDITIONS)
    abort_ok = abort_ok and abort.get("conditions_total") == len(ABORT_CONDITIONS)
    return {
        "result_id": "request_gate_abort_binding_result_v1",
        "gates_bound": gates_ok,
        "gates_total": len(PRE_EXECUTION_GATES),
        "abort_bound": abort_ok,
        "abort_total": len(ABORT_CONDITIONS),
        "binding_pass": gates_ok and abort_ok,
        **meta,
    }


def _output_post_review_result(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    out = ctx["output_binding"]
    post = ctx["post_binding"]
    out_dir = str(out.get("allowed_output_directory") or PLANNED_EXECUTION_OUTPUT_DIR)
    output_ok = all(
        [
            out.get("output_type") == "visual_observation_candidate",
            out.get("candidate_only") is True,
            out.get("fact_status") == "not_fact",
            out.get("write_allowed") is False,
            out.get("runtime_action_allowed") is False,
            out.get("trial_scope") == TRIAL_SCOPE,
            "Luna-Workspace-Min" in out_dir,
        ]
    )
    post_ok = all(
        [
            post.get("mandatory_after_execution") is True,
            post.get("cannot_bypass") is True,
            post.get("required_phase") == POST_EXECUTION_REVIEW_PHASE,
        ]
    )
    return {
        "result_id": "request_output_post_review_binding_result_v1",
        "output_contract_pass": output_ok,
        "post_execution_review_required": True,
        "post_execution_review_pass": post_ok,
        "allowed_output_directory": out_dir,
        "binding_pass": output_ok and post_ok,
        **meta,
    }


def _non_grant_review(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    planned = set(ctx["non_grant"].get("statements") or [])
    required = set(NON_GRANT_STATEMENTS)
    return {
        "review_id": "request_non_grant_statement_review_v1",
        "review_pass": required.issubset(planned),
        "statements_confirmed": list(NON_GRANT_STATEMENTS),
        **meta,
    }


def _lifecycle_consumption(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    lc = ctx["lifecycle"]
    states = lc.get("states") or []
    consumable = list(LIFECYCLE_STATES) == states or set(states) == set(LIFECYCLE_STATES)
    current_ok = lc.get("current_state") == "planning_defined" and meta.get("lifecycle_current_state") == "planning_defined"
    return {
        "result_id": "request_lifecycle_consumption_result_v1",
        "consumption_pass": consumable and current_ok,
        "states": list(LIFECYCLE_STATES),
        "current_state": "planning_defined",
        "lifecycle_not_advanced": True,
        **meta,
    }


def _non_generation_review(meta: Dict[str, Any]) -> Dict[str, Any]:
    flags = {
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "execution_authorization_granted_now": False,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
    }
    return {
        "review_id": "request_non_generation_non_sent_non_grant_review_v1",
        "review_pass": all(v is False for v in flags.values()),
        "flags": flags,
        **meta,
    }


def run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    planning_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else planning_root.parent
        / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review"
    )

    blockers, ctx = _validate_upstream(planning_root)
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(planning_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_request_planning_root": str(planning_root),
        "request_dryrun_review_output_root": str(out_root),
        "planned_execution_output_directory": PLANNED_EXECUTION_OUTPUT_DIR,
    }

    identity_res = _consume_identity(ctx, meta)
    scope_res = _consume_scope(meta)
    input_res = _consume_input_binding(ctx, meta)
    window_res = _window_binding_result(ctx, meta)
    gate_abort_res = _gate_abort_binding_result(ctx, meta)
    output_post_res = _output_post_review_result(ctx, meta)
    non_grant_res = _non_grant_review(ctx, meta)
    lifecycle_res = _lifecycle_consumption(ctx, meta)
    non_gen_res = _non_generation_review(meta)

    component_pass = all(
        [
            identity_res.get("consumption_pass"),
            scope_res.get("consumption_pass"),
            input_res.get("consumption_pass"),
            window_res.get("binding_pass"),
            gate_abort_res.get("binding_pass"),
            output_post_res.get("binding_pass"),
            non_grant_res.get("review_pass"),
            lifecycle_res.get("consumption_pass"),
            non_gen_res.get("review_pass"),
        ]
    )

    violations = list(blockers)
    for field in RUNTIME_BOUNDARY_FIELDS:
        if meta.get(field) is True:
            violations.append(f"boundary violation: {field}")

    boundary_ok = len(violations) == 0 and component_pass
    high_risk_count = 0 if boundary_ok else max(1, len(violations))

    policy = {
        "policy_id": "authorization_request_dryrun_and_review_policy_v1",
        "scope": SCOPE,
        "mode": "simulated_request_plan_consumption_review",
        **meta,
    }

    input_review = {
        "review_id": "request_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier": ctx["planning_vr"].get("verifier"),
        "upstream_final_decision": ctx["planning_sm"].get("final_decision"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "authorization_request_readiness_decision_v1",
        "ready_for_request_artifact_generation_planning": boundary_ok,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "execution_authorization_granted_now": False,
        "lifecycle_current_state": "planning_defined",
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "high_risk_count": high_risk_count,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_and_review_scope": SCOPE,
        "boundary_ok": boundary_ok,
        "high_risk_count": high_risk_count,
        "violations": violations,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "request_identity_consumption_pass": identity_res.get("consumption_pass"),
        "request_scope_consumption_pass": scope_res.get("consumption_pass"),
        "lifecycle_current_state": "planning_defined",
        **meta,
    }

    return {
        "authorization_request_dryrun_and_review_policy": policy,
        "request_planning_input_review": input_review,
        "request_identity_consumption_result": identity_res,
        "request_scope_binding_consumption_result": scope_res,
        "request_input_binding_consumption_result": input_res,
        "request_execution_window_binding_result": window_res,
        "request_gate_abort_binding_result": gate_abort_res,
        "request_output_post_review_binding_result": output_post_res,
        "request_non_grant_statement_review": non_grant_res,
        "request_lifecycle_consumption_result": lifecycle_res,
        "request_non_generation_non_sent_non_grant_review": non_gen_res,
        "authorization_request_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
