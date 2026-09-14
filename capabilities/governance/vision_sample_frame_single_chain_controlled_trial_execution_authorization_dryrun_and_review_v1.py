# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Execution Authorization DryRun+Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    ABORT_CONDITIONS,
    AUTHORIZATION_ALLOWED,
    AUTHORIZATION_FORBIDDEN,
    EXECUTION_ALLOWLIST,
    EXECUTION_BLOCKLIST,
    POST_EXECUTION_REVIEW_PHASE,
    PRE_EXECUTION_GATES,
    TRIAL_SCOPE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-DryRunAndReview-v1-001"
SCOPE = "execution_authorization_dryrun_and_review_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1"

UPSTREAM_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_PLANNING_READY_FOR_AUTHORIZATION_DRYRUN"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-DryRun-v1-001"

FINAL_DECISION_GO = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_DRYRUN_AND_REVIEW_READY_FOR_AUTHORIZATION_REQUEST_PLANNING"
)
FINAL_DECISION_HOLD = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Issue-Review-v1-001"

PLANNED_EXECUTION_OUTPUT_DIR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_sample_frame_single_chain_controlled_trial_execution"
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun+Review GO ≠ trial execution authorized",
    "DryRun+Review GO ≠ controlled trial started",
    "DryRun+Review GO ≠ execution window opened",
    "Authorization scope consumable ≠ live camera allowed",
    "Gate dryrun pass ≠ runtime authorization grant",
    "Output contract review pass ≠ visual fact",
    "Logging policy review pass ≠ WorldModel / Memory write",
    "Ready for Authorization Request Planning ≠ Trial Execution",
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
        "execution_authorization_dryrun_and_review_only": True,
        "simulated": True,
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


def _validate_upstream(planning_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    sm = _try_read_json(planning_root / "summary.json") or {}
    vr = _try_read_json(planning_root / "verifier_report.json") or {}
    scope = _try_read_json(planning_root / "controlled_trial_execution_authorization_scope_v1.json") or {}
    allow = _try_read_json(planning_root / "controlled_trial_execution_allowlist_v1.json") or {}
    block = _try_read_json(planning_root / "controlled_trial_execution_blocklist_v1.json") or {}
    gates = _try_read_json(planning_root / "controlled_trial_pre_execution_gate_matrix_v1.json") or {}
    window = _try_read_json(planning_root / "controlled_trial_execution_window_authorization_plan_v1.json") or {}
    abort = _try_read_json(planning_root / "controlled_trial_abort_condition_matrix_v1.json") or {}
    output = _try_read_json(planning_root / "controlled_trial_output_contract_v1.json") or {}
    logging = _try_read_json(planning_root / "controlled_trial_execution_logging_policy_v1.json") or {}
    post = _try_read_json(planning_root / "controlled_trial_post_execution_review_requirement_v1.json") or {}
    readiness = _try_read_json(planning_root / "execution_authorization_planning_readiness_decision_v1.json") or {}

    trusted = vr.get("verifier") == "GO" and vr.get("passed") is True
    summary_ok = (
        sm.get("boundary_ok") is True
        and sm.get("phase") == UPSTREAM_PHASE
        and sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not trusted and not summary_ok:
        blockers.append("authorization planning verifier must be GO")
    if sm.get("controlled_trial_execution_authorization_planning_only") is not True:
        blockers.append("controlled_trial_execution_authorization_planning_only must be true")
    if sm.get("trial_execution_authorized_now") is True:
        blockers.append("trial_execution_authorized_now must be false in planning")
    if sm.get("controlled_trial_started_now") is True:
        blockers.append("controlled_trial_started_now must be false in planning")
    if readiness.get("ready_for_authorization_dryrun") is not True:
        blockers.append("ready_for_authorization_dryrun must be true")
    if window.get("execution_window_type") != "controlled_fixture_only":
        blockers.append("execution_window_type must be controlled_fixture_only")
    if window.get("max_trial_scope") != "single_chain":
        blockers.append("max_trial_scope must be single_chain")
    if window.get("max_output_count") != 3:
        blockers.append("max_output_count must be 3")
    if window.get("post_execution_review_required") is not True:
        blockers.append("post_execution_review_required must be true")

    allowed = set(scope.get("allowed_future_inputs") or [])
    for item in AUTHORIZATION_ALLOWED:
        if item not in allowed:
            blockers.append(f"scope missing allowed input: {item}")

    forbidden = set(scope.get("explicitly_forbidden") or [])
    for item in ("live_camera", "new_camera_capture", "arbitrary_image_read", "vision_model_inference", "fact_write"):
        if item not in forbidden:
            blockers.append(f"scope missing forbidden: {item}")

    allow_ops = set(allow.get("allowed_operations") or [])
    for op in EXECUTION_ALLOWLIST:
        if op not in allow_ops:
            blockers.append(f"allowlist missing: {op}")

    block_ops = set(block.get("blocked_operations") or [])
    for op in ("live_camera", "model_inference", "fact_upgrade", "runtime_action"):
        if op not in block_ops:
            blockers.append(f"blocklist missing: {op}")

    planned_gates = {g.get("gate_id") for g in gates.get("gates") or []}
    for g in PRE_EXECUTION_GATES:
        if g not in planned_gates:
            blockers.append(f"pre_execution gate missing in planning: {g}")

    abort_triggers = {c.get("trigger") for c in abort.get("conditions") or []}
    for cond in ABORT_CONDITIONS:
        if cond["trigger"] not in abort_triggers:
            blockers.append(f"abort condition missing: {cond['trigger']}")

    if output.get("output_type") != "visual_observation_candidate":
        blockers.append("output contract output_type invalid")
    if output.get("candidate_only") is not True:
        blockers.append("output contract candidate_only must be true")
    if logging.get("allowed_write_root") is None:
        blockers.append("logging policy allowed_write_root required")
    if post.get("required_phase") != POST_EXECUTION_REVIEW_PHASE:
        blockers.append("post_execution_review phase mismatch")

    return blockers, {
        "planning_sm": sm,
        "planning_vr": vr,
        "scope": scope,
        "allow": allow,
        "block": block,
        "gates": gates,
        "window": window,
        "abort": abort,
        "output": output,
        "logging": logging,
        "post": post,
        "readiness": readiness,
    }


def _consume_scope(meta: Dict[str, Any]) -> Dict[str, Any]:
    allowed_ok = list(AUTHORIZATION_ALLOWED)
    forbidden_ok = list(AUTHORIZATION_FORBIDDEN)
    forbidden_checks = {
        "live_camera": True,
        "new_camera_capture": True,
        "arbitrary_image_read": True,
        "vision_model_inference": True,
        "fact_write": True,
        "worldmodel_write": True,
        "memory_write": True,
        "scene_delta_write": True,
        "user_facing_output": True,
        "external_provider": True,
        "runtime_action": True,
    }
    return {
        "result_id": "authorization_scope_consumption_result_v1",
        "consumption_pass": True,
        "allowed_confirmed": allowed_ok,
        "forbidden_confirmed": forbidden_ok,
        "forbidden_enforcement_simulated": forbidden_checks,
        "live_camera_blocked": True,
        "model_inference_blocked": True,
        "fact_write_blocked": True,
        **meta,
    }


def _review_allowlist_blocklist(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "review_id": "execution_allowlist_blocklist_review_v1",
        "allowlist_pass": True,
        "blocklist_pass": True,
        "allowlist_operations": list(EXECUTION_ALLOWLIST),
        "blocklist_operations": list(EXECUTION_BLOCKLIST),
        "allowlist_only_narrow_ops": True,
        "blocklist_covers_runtime_and_model": True,
        **meta,
    }


def _consume_gates(meta: Dict[str, Any]) -> Dict[str, Any]:
    rows = [
        {
            "gate_id": g,
            "dryrun_pass": True,
            "enforcement_pass": True,
            "simulated": True,
        }
        for g in PRE_EXECUTION_GATES
    ]
    return {
        "result_id": "pre_execution_gate_consumption_result_v1",
        "gates": rows,
        "gates_total": len(rows),
        "gates_passed": len(rows),
        "all_dryrun_pass": True,
        **meta,
    }


def _dryrun_window(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    window = ctx["window"]
    out_dir = str(window.get("output_directory") or PLANNED_EXECUTION_OUTPUT_DIR)
    checks = {
        "execution_window_type": window.get("execution_window_type") == "controlled_fixture_only",
        "max_trial_scope": window.get("max_trial_scope") == "single_chain",
        "max_output_count": window.get("max_output_count") == 3,
        "output_directory_workspace": "Luna-Workspace-Min" in out_dir,
        "no_live_input": window.get("no_live_input") is True,
        "no_external_provider": window.get("no_external_provider") is True,
        "no_user_facing_output": window.get("no_user_facing_output") is True,
        "post_execution_review_required": window.get("post_execution_review_required") is True,
    }
    window_not_opened = meta.get("execution_window_opened_now") is False
    return {
        "result_id": "execution_window_dryrun_result_v1",
        "dryrun_pass": all(checks.values()) and window_not_opened,
        "checks": checks,
        "execution_window_not_opened": window_not_opened,
        "output_directory": out_dir,
        "execution_window_opened_now": False,
        **meta,
    }


def _consume_abort(meta: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for cond in ABORT_CONDITIONS:
        rows.append(
            {
                "trigger": cond["trigger"],
                "expected_action": cond["action"],
                "consumable": True,
                "simulated_abort": True,
            }
        )
    return {
        "result_id": "abort_condition_consumption_result_v1",
        "conditions": rows,
        "conditions_total": len(rows),
        "all_consumable": True,
        **meta,
    }


def _review_output_contract(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    out = ctx["output"]
    checks = [
        out.get("output_type") == "visual_observation_candidate",
        out.get("candidate_only") is True,
        out.get("fact_status") == "not_fact",
        out.get("write_allowed") is False,
        out.get("runtime_action_allowed") is False,
        out.get("trial_scope") == TRIAL_SCOPE,
        out.get("source_chain_present") is True,
        out.get("frame_ref_present") is True,
        out.get("timestamp_present") is True,
    ]
    return {
        "review_id": "output_contract_review_v1",
        "review_pass": all(checks),
        "contract": out,
        **meta,
    }


def _review_logging(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    logging = ctx["logging"]
    root = str(logging.get("allowed_write_root") or "")
    return {
        "review_id": "logging_policy_review_v1",
        "review_pass": "Luna-Workspace-Min" in root,
        "allowed_write_root": root,
        "workspace_fallback_only": logging.get("workspace_fallback_only") is True,
        "forbidden_targets": logging.get("forbidden_targets") or [],
        "no_worldmodel_memory_write": True,
        **meta,
    }


def _post_exec_requirement(ctx: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    post = ctx["post"]
    return {
        "result_id": "post_execution_review_requirement_result_v1",
        "requirement_pass": post.get("mandatory_after_execution") is True,
        "required_phase": post.get("required_phase"),
        "cannot_bypass": post.get("cannot_bypass") is True,
        "post_execution_review_required": True,
        **meta,
    }


def _non_release_review(meta: Dict[str, Any]) -> Dict[str, Any]:
    release_blocked = {
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "vision_model_invoked_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "user_facing_output_generated_now": False,
    }
    return {
        "review_id": "authorization_non_release_review_v1",
        "review_pass": all(v is False for v in release_blocked.values()),
        "release_blocked": release_blocked,
        "note": "DryRun+Review does not grant execution authorization or open execution window",
        **meta,
    }


def run_vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    planning_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else planning_root.parent
        / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(planning_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_authorization_planning_root": str(planning_root),
        "dryrun_review_output_root": str(out_root),
        "planned_execution_output_directory": PLANNED_EXECUTION_OUTPUT_DIR,
    }

    blockers, ctx = _validate_upstream(planning_root)

    scope_result = _consume_scope(meta)
    allow_block_review = _review_allowlist_blocklist(meta)
    gate_result = _consume_gates(meta)
    window_result = _dryrun_window(ctx, meta)
    abort_result = _consume_abort(meta)
    output_review = _review_output_contract(ctx, meta)
    logging_review = _review_logging(ctx, meta)
    post_result = _post_exec_requirement(ctx, meta)
    non_release = _non_release_review(meta)

    component_pass = all(
        [
            scope_result.get("consumption_pass"),
            allow_block_review.get("allowlist_pass"),
            allow_block_review.get("blocklist_pass"),
            gate_result.get("all_dryrun_pass"),
            window_result.get("dryrun_pass"),
            abort_result.get("all_consumable"),
            output_review.get("review_pass"),
            logging_review.get("review_pass"),
            post_result.get("requirement_pass"),
            non_release.get("review_pass"),
        ]
    )

    violations = list(blockers)
    for field in RUNTIME_BOUNDARY_FIELDS:
        if meta.get(field) is True:
            violations.append(f"boundary violation: {field}")

    boundary_ok = len(violations) == 0 and component_pass

    policy = {
        "policy_id": "execution_authorization_dryrun_and_review_policy_v1",
        "scope": SCOPE,
        "mode": "simulated_authorization_plan_consumption_review",
        **meta,
    }

    input_review = {
        "review_id": "authorization_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier": ctx["planning_vr"].get("verifier"),
        "upstream_final_decision": ctx["planning_sm"].get("final_decision"),
        "upstream_recommended_next_phase": ctx["planning_sm"].get("recommended_next_phase"),
        "planning_only_confirmed": ctx["planning_sm"].get("controlled_trial_execution_authorization_planning_only"),
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
        "decision_id": "trial_execution_readiness_decision_v1",
        "ready_for_authorization_request_planning": boundary_ok,
        "ready_for_trial_execution": False,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "note": "Does not authorize trial execution; request/grant/execution/post-review chain still required",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_and_review_scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": violations,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "pre_execution_gates_passed": gate_result.get("gates_passed"),
        "authorization_scope_consumption_pass": scope_result.get("consumption_pass"),
        "execution_window_dryrun_pass": window_result.get("dryrun_pass"),
        **meta,
    }

    return {
        "execution_authorization_dryrun_and_review_policy": policy,
        "authorization_planning_input_review": input_review,
        "authorization_scope_consumption_result": scope_result,
        "execution_allowlist_blocklist_review": allow_block_review,
        "pre_execution_gate_consumption_result": gate_result,
        "execution_window_dryrun_result": window_result,
        "abort_condition_consumption_result": abort_result,
        "output_contract_review": output_review,
        "logging_policy_review": logging_review,
        "post_execution_review_requirement_result": post_result,
        "authorization_non_release_review": non_release,
        "trial_execution_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
