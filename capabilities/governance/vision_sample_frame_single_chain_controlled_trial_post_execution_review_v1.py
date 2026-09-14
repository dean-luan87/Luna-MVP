# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Post-Execution Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_trial_post_execution_review_harness_v1 import (
    HARNESS_ID,
    review_controlled_trial_execution,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_v1 import (
    FINAL_DECISION_GO as EXECUTION_FINAL_GO,
    NEXT_PHASE_GO as EXECUTION_NEXT_PHASE,
    TRIAL_SCOPE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Post-Execution-Review-v1-001"
REVIEW_SCOPE = "controlled_trial_post_execution_review_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1"

UPSTREAM_EXECUTION_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-v1-001"

FINAL_DECISION_GO = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_POST_EXECUTION_REVIEW_CLOSED_READY_FOR_OCR_MOCK_SINGLE_CHAIN_TRIAL"
)
FINAL_DECISION_HOLD = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_POST_EXECUTION_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Mock-Result-Single-Chain-Trial-Via-Validation-Factory-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Post-Execution-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Post-Execution Review GO ≠ visual fact generated",
    "Vision sample frame trial closure ≠ live camera enabled",
    "visual_observation_candidate closure ≠ WorldModel / Memory write allowed",
    "single-chain Vision closure ≠ OCR / Navigation / Task runtime enabled",
    "next-chain readiness ≠ next-chain execution started",
    "Post-execution review pass ≠ grant issued",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta(review_pass: bool) -> Dict[str, Any]:
    return {
        "controlled_trial_post_execution_review_only": True,
        "review_only": True,
        "controlled_trial_execution_completed_observed": True,
        "post_execution_review_passed_now": review_pass,
        "harness_id": HARNESS_ID,
        "harness_runtime_consumption_tested_now": True,
        "controlled_trial_closed_now": review_pass,
        "visual_fact_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "user_facing_output_generated_now": False,
        "live_camera_enabled_now": False,
        "vision_model_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "grant_issued_now": False,
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


def _validate_upstream(execution_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    sm = _try_read_json(execution_root / "summary.json") or {}
    vr = _try_read_json(execution_root / "verifier_report.json") or {}

    if not (vr.get("verifier") == "GO" and vr.get("passed") is True):
        if sm.get("boundary_ok") is not True:
            blockers.append("execution verifier must be GO")
    if sm.get("phase") != UPSTREAM_EXECUTION_PHASE:
        blockers.append("upstream must be execution phase")
    if sm.get("final_decision") != EXECUTION_FINAL_GO:
        blockers.append("execution final_decision mismatch")
    if sm.get("recommended_next_phase") != EXECUTION_NEXT_PHASE:
        blockers.append("execution recommended_next_phase mismatch")
    if sm.get("controlled_trial_started_now") is not True:
        blockers.append("controlled_trial_started_now must be true")
    if sm.get("execution_window_opened_now") is not True:
        blockers.append("execution_window_opened_now must be true")
    if sm.get("execution_window_type") != "controlled_fixture_only":
        blockers.append("execution_window_type must be controlled_fixture_only")
    if sm.get("max_trial_scope") != "single_chain":
        blockers.append("max_trial_scope must be single_chain")
    if (sm.get("candidates_generated") or 0) != 3:
        blockers.append("output_count must be 3")
    if sm.get("execution_aborted") is True:
        blockers.append("execution must not be aborted")

    for i in range(1, 4):
        if not (execution_root / f"visual_observation_candidate_{i}_v1.json").is_file():
            blockers.append(f"visual_observation_candidate_{i}_v1.json missing")

    return blockers, {"execution_sm": sm, "execution_vr": vr}


def run_vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_execution_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    execution_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_root
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else execution_root.parent / "vision_sample_frame_single_chain_controlled_trial_post_execution_review"
    )

    upstream_blockers, ctx = _validate_upstream(execution_root)
    review_bundle = review_controlled_trial_execution(execution_root, trial_scope=TRIAL_SCOPE)

    review_pass = (
        review_bundle["harness_result"].get("review_pass") is True and len(upstream_blockers) == 0
    )
    blockers = upstream_blockers + review_bundle["harness_result"].get("blockers", [])

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(execution_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(review_pass),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_execution_root": str(execution_root),
        "post_execution_review_output_root": str(out_root),
        "controlled_trial_started_now": ctx["execution_sm"].get("controlled_trial_started_now"),
        "execution_window_opened_now": ctx["execution_sm"].get("execution_window_opened_now"),
        "execution_window_type": ctx["execution_sm"].get("execution_window_type"),
        "max_trial_scope": ctx["execution_sm"].get("max_trial_scope"),
        "output_count": ctx["execution_sm"].get("candidates_generated"),
    }

    policy = {
        "policy_id": "post_execution_review_policy_v1",
        "scope": REVIEW_SCOPE,
        "harness_entrypoint": "review_controlled_trial_execution",
        **meta,
    }

    execution_input_review = {
        "review_id": "controlled_trial_execution_input_review_v1",
        "execution_root": str(execution_root),
        "execution_verifier": ctx["execution_vr"].get("verifier"),
        "execution_final_decision": ctx["execution_sm"].get("final_decision"),
        "review_pass": len(upstream_blockers) == 0,
        "blockers": upstream_blockers,
        **meta,
    }

    closure = {
        "decision_id": "controlled_trial_closure_decision_v1",
        "trial_id": "vision_sample_frame_controlled",
        "chain_id": "vision_sample_frame",
        "vision_sample_frame_controlled_trial_closed": review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "boundary_ok": review_pass,
        "blockers": blockers,
        **meta,
    }

    next_chain = {
        "readiness_id": "next_chain_adoption_readiness_v1",
        "ready_for_ocr_mock_single_chain_via_validation_factory": review_pass,
        "recommended_next_chain": "ocr_mock_result",
        "validation_factory_required": True,
        "do_not_enable_real_ocr_provider_yet": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": review_pass,
        "violations": blockers,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "harness_review_pass": review_bundle["harness_result"].get("review_pass"),
        **meta,
    }

    return {
        "post_execution_review_policy": policy,
        "controlled_trial_execution_input_review": execution_input_review,
        "execution_result_completeness_review": {**review_bundle["completeness"], **meta},
        "visual_observation_candidate_contract_review": {**review_bundle["candidate_contract"], **meta},
        "no_runtime_boundary_post_execution_review": {**review_bundle["no_runtime"], **meta},
        "abort_monitor_post_execution_review": {**review_bundle["abort"], **meta},
        "logging_path_compliance_review": {**review_bundle["logging"], **meta},
        "side_effect_absence_review": {**review_bundle["side_effect"], **meta},
        "controlled_trial_closure_decision": closure,
        "next_chain_adoption_readiness": next_chain,
        "non_claims_register": non_claims,
        "summary": summary,
    }
