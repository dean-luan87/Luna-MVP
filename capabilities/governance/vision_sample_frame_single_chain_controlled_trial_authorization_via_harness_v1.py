# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Authorization Via Harness v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    HARNESS_ID,
    build_vision_sample_frame_authorization_config,
    run_authorization_validate,
)
from capabilities.governance.controlled_trial_authorization_harness_validation_closure_v1 import (
    FINAL_DECISION as HARNESS_CLOSURE_FINAL,
    UPSTREAM_EXTRACTION_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Authorization-Via-Harness-v1-001"
SCOPE = "vision_sample_frame_controlled_trial_authorization_via_harness_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1"

UPSTREAM_HARNESS_CLOSURE_PHASE = "Phase-Controlled-Trial-Authorization-Harness-Validation-Closure-v1-001"
UPSTREAM_PLAN_AND_DRYRUN_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-PlanAndDryRun-v1-001"
UPSTREAM_PLAN_AND_DRYRUN_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_PLAN_AND_DRYRUN_READY_FOR_CONTROLLED_TRIAL_PLANNING"
)
UPSTREAM_CONTROLLED_DRYRUN_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-DryRunAndReview-v1-001"
UPSTREAM_CONTROLLED_DRYRUN_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_DRYRUN_AND_REVIEW_READY_FOR_EXECUTION_AUTHORIZATION_PLANNING"
)

FINAL_DECISION = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_AUTHORIZATION_VIA_HARNESS_READY_FOR_CONTROLLED_TRIAL_EXECUTION"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-v1-001"
TARGET_EXECUTION_PHASE = NEXT_PHASE

NON_CLAIMS: Tuple[str, ...] = (
    "Authorization Via Harness GO ≠ controlled trial started",
    "Authorization Via Harness GO ≠ grant issued",
    "Authorization Via Harness GO ≠ request sent",
    "Harness validation pass ≠ live camera allowed",
    "Execution readiness ≠ visual fact",
    "Absorbed legacy auth phases ≠ bypass Execution phase",
    "Harness path ≠ skip Post-Execution Review",
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
    "user_facing_output_generated_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "vision_sample_frame_controlled_trial_authorization_via_harness_only": True,
        "controlled_trial_authorization_via_harness_only": True,
        "harness_id": HARNESS_ID,
        "harness_validated_now": True,
        "authorization_harness_enforced_via_config": True,
        "legacy_authorization_phase_chain_bypassed": True,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "execution_authorization_granted_now": False,
        "grant_issued_now": False,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
        "runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "scene_delta_generated_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "user_facing_output_generated_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _validate_upstream(
    closure_root: Path,
    plan_dryrun_root: Optional[Path],
    controlled_dryrun_root: Optional[Path],
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {}

    closure_sm = _try_read_json(closure_root / "summary.json") or {}
    closure_vr = _try_read_json(closure_root / "verifier_report.json") or {}
    ctx["closure_sm"] = closure_sm
    ctx["closure_vr"] = closure_vr

    if not (closure_vr.get("verifier") == "GO" and closure_vr.get("passed") is True):
        if closure_sm.get("boundary_ok") is not True:
            blockers.append("harness validation closure must be GO")
    if closure_sm.get("final_decision") != HARNESS_CLOSURE_FINAL:
        blockers.append("harness closure final_decision mismatch")
    if closure_sm.get("harness_contract_validated_now") is not True:
        blockers.append("harness_contract_validated_now required")

    if plan_dryrun_root and plan_dryrun_root.is_dir():
        pd_sm = _try_read_json(plan_dryrun_root / "summary.json") or {}
        pd_vr = _try_read_json(plan_dryrun_root / "verifier_report.json") or {}
        ctx["plan_dryrun_sm"] = pd_sm
        if not (pd_vr.get("verifier") == "GO" and pd_vr.get("passed") is True):
            if pd_sm.get("boundary_ok") is not True:
                blockers.append("vision plan_and_dryrun must be GO")
        if pd_sm.get("final_decision") != UPSTREAM_PLAN_AND_DRYRUN_FINAL:
            blockers.append("vision plan_and_dryrun final_decision mismatch")

    if controlled_dryrun_root and controlled_dryrun_root.is_dir():
        ct_sm = _try_read_json(controlled_dryrun_root / "summary.json") or {}
        ct_vr = _try_read_json(controlled_dryrun_root / "verifier_report.json") or {}
        ctx["controlled_dryrun_sm"] = ct_sm
        if not (ct_vr.get("verifier") == "GO" and ct_vr.get("passed") is True):
            if ct_sm.get("boundary_ok") is not True:
                blockers.append("controlled trial dryrun+review must be GO")
        if ct_sm.get("trial_execution_authorized_now") is True:
            blockers.append("trial must not be pre-authorized before harness path")

    return blockers, ctx


def run_vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1(
    *,
    controlled_trial_authorization_harness_validation_closure_root: str,
    vision_sample_frame_single_chain_plan_and_dryrun_root: Optional[str] = None,
    vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    closure_root = Path(
        controlled_trial_authorization_harness_validation_closure_root
    ).expanduser().resolve()
    plan_root = (
        Path(vision_sample_frame_single_chain_plan_and_dryrun_root).expanduser().resolve()
        if vision_sample_frame_single_chain_plan_and_dryrun_root
        else closure_root.parent / "vision_sample_frame_single_chain_plan_and_dryrun"
    )
    controlled_root = (
        Path(vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root).expanduser().resolve()
        if vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root
        else closure_root.parent / "vision_sample_frame_single_chain_controlled_trial_dryrun_and_review"
    )

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else closure_root.parent / "vision_sample_frame_single_chain_controlled_trial_authorization_via_harness"
    )

    upstream_blockers, ctx = _validate_upstream(closure_root, plan_root, controlled_root)

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(closure_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_harness_closure_root": str(closure_root),
        "upstream_plan_and_dryrun_root": str(plan_root),
        "upstream_controlled_trial_dryrun_root": str(controlled_root),
        "authorization_via_harness_output_root": str(out_root),
    }

    auth_config = build_vision_sample_frame_authorization_config(
        source_validation_phase=PHASE_ID,
    )
    auth_config["source_validation_phase"] = PHASE_ID
    auth_config["target_execution_phase"] = TARGET_EXECUTION_PHASE

    harness_result = run_authorization_validate(
        auth_config,
        boundary_meta=meta,
        upstream_blockers=upstream_blockers,
    )

    validation_pass = harness_result.get("validation_pass") is True
    boundary_ok = validation_pass

    policy = {
        "policy_id": "vision_sample_frame_authorization_via_harness_policy_v1",
        "scope": SCOPE,
        "mode": "authorization_config_driven_via_controlled_trial_authorization_harness",
        "harness_entrypoint": "run_authorization_validate",
        "absorbed_legacy_phases": [
            "Execution-Authorization-Planning",
            "Execution-Authorization-DryRunAndReview",
            "Execution-Authorization-Request-Planning",
            "Execution-Authorization-Request-DryRunAndReview",
        ],
        **meta,
    }

    input_review = {
        "review_id": "harness_validation_closure_input_review_v1",
        "closure_root": str(closure_root),
        "closure_verifier": ctx.get("closure_vr", {}).get("verifier"),
        "closure_final_decision": ctx.get("closure_sm", {}).get("final_decision"),
        "extraction_phase_ref": UPSTREAM_EXTRACTION_PHASE,
        "review_pass": len(upstream_blockers) == 0,
        "blockers": upstream_blockers,
        **meta,
    }

    config_snapshot = {
        "snapshot_id": "authorization_config_snapshot_v1",
        "harness_id": HARNESS_ID,
        "chain_id": auth_config.get("chain_id"),
        "trial_id": auth_config.get("trial_id"),
        "authorization_config": auth_config,
        **meta,
    }

    readiness = {
        **harness_result["execution_readiness"],
        "decision_id": "controlled_trial_execution_readiness_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_AUTHORIZATION_VIA_HARNESS_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "violations": harness_result.get("blockers") or [],
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "authorization_via_harness_scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": readiness.get("violations") or [],
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "authorization_validation_pass": validation_pass,
        "request_lifecycle_state": harness_result["request_lifecycle_result"].get("current_state"),
        "grant_lifecycle_state": harness_result["grant_lifecycle_result"].get("current_state"),
        "ready_for_controlled_trial_execution": readiness.get("ready_for_controlled_trial_execution"),
        **meta,
    }

    return {
        "vision_sample_frame_authorization_via_harness_policy": policy,
        "harness_validation_closure_input_review": input_review,
        "authorization_config_snapshot": config_snapshot,
        "authorization_validation_result": {
            **harness_result["authorization_validation_result"],
            "result_id": "authorization_validation_result_v1",
        },
        "request_lifecycle_result": {
            **harness_result["request_lifecycle_result"],
            "result_id": "request_lifecycle_result_v1",
        },
        "grant_lifecycle_result": {
            **harness_result["grant_lifecycle_result"],
            "result_id": "grant_lifecycle_result_v1",
        },
        "controlled_trial_execution_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
