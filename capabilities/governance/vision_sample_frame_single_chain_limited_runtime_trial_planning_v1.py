# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Limited Runtime Trial Planning v1.

First single-chain trial: sample/fixture frame → visual_observation_candidate only. Planning-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-Planning-v1-001"
PLANNING_SCOPE = "vision_sample_frame_single_chain_trial_planning_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_limited_runtime_trial_planning_v1"
TRIAL_SCOPE = "vision_sample_frame_single_chain"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_POST_DRYRUN_REVIEW_READY_FOR_SINGLE_CHAIN_VISION_SAMPLE_FRAME_TRIAL_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-Planning-v1-001"

FINAL_DECISION = "VISION_SAMPLE_FRAME_SINGLE_CHAIN_LIMITED_RUNTIME_TRIAL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-DryRun-v1-001"

VISION_SINGLE_CHAIN_GATES: Tuple[str, ...] = (
    "safety_gate",
    "source_chain_gate",
    "fixture_or_controlled_input_gate",
    "no_live_camera_gate",
    "no_new_capture_gate",
    "no_arbitrary_image_read_gate",
    "no_vision_model_gate",
    "no_fact_write_gate",
    "no_worldmodel_write_gate",
    "no_memory_write_gate",
    "fallback_gate",
)

STOP_CONDITIONS: Tuple[Dict[str, str], ...] = (
    {"trigger": "live_camera_required", "action": "stop"},
    {"trigger": "new_frame_capture_required", "action": "stop"},
    {"trigger": "arbitrary_image_read_required", "action": "stop"},
    {"trigger": "visual_model_inference_required", "action": "stop"},
    {"trigger": "missing_frame_ref", "action": "hold"},
    {"trigger": "missing_source_chain", "action": "hold"},
    {"trigger": "candidate_attempts_fact_upgrade", "action": "stop"},
    {"trigger": "worldmodel_or_memory_write_requested", "action": "stop"},
    {"trigger": "safety_gate_failed", "action": "stop"},
    {"trigger": "fixture_control_input_unverifiable", "action": "hold"},
)

ALLOWED_INPUT_SOURCES: Tuple[str, ...] = (
    "existing_sample_frame_reference",
    "fixture_frame_metadata",
    "controlled_frame_reference",
    "previous_dryrun_visual_candidate_object",
)

FORBIDDEN_INPUT_SOURCES: Tuple[str, ...] = (
    "live_camera",
    "new_camera_capture",
    "arbitrary_image_read",
    "visual_model_inference",
    "ocr",
    "navigation",
    "task_commit",
    "tts",
    "llm",
    "worldmodel_write",
    "memory_write",
)

CANDIDATE_INVARIANTS: Dict[str, Any] = {
    "candidate_only": True,
    "fact_status": "not_fact",
    "write_allowed": False,
    "runtime_action_allowed": False,
    "source_chain_required": True,
    "frame_ref_required": True,
    "timestamp_required": True,
    "trial_scope": TRIAL_SCOPE,
}

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ single-chain trial started",
    "sample frame reference ≠ live camera",
    "visual_observation_candidate ≠ visual fact",
    "source_chain pass ≠ WorldModel write allowed",
    "fixture frame consumed ≠ arbitrary image read allowed",
    "single-chain planning ≠ OCR / Navigation / Task runtime allowed",
    "DryRun plan ≠ vision model invoked",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "live_runtime_enabled_now",
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "vision_sample_frame_single_chain_trial_planning_only": True,
        "single_chain_trial_started_now": False,
        "limited_runtime_trial_started_now": False,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_provider_invoked_now": False,
        "real_ocr_provider_enabled_now": False,
        "navigation_action_triggered_now": False,
        "real_navigation_runtime_enabled_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
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


def _validate_upstream(review_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    review_sm = _try_read_json(review_root / "summary.json") or {}
    review_vr = _try_read_json(review_root / "verifier_report.json") or {}
    positive = _try_read_json(review_root / "limited_runtime_positive_flow_review_v1.json") or {}
    blocked = _try_read_json(review_root / "limited_runtime_blocked_flow_review_v1.json") or {}
    gate_review = _try_read_json(review_root / "limited_runtime_gate_review_v1.json") or {}
    stop_review = _try_read_json(review_root / "limited_runtime_stop_condition_review_v1.json") or {}
    single_chain = _try_read_json(review_root / "single_chain_trial_planning_readiness_v1.json") or {}

    review_verifier_trusted = review_vr.get("verifier") == "GO" and review_vr.get("passed") is True
    review_summary_trusted = (
        review_sm.get("boundary_ok") is True
        and review_sm.get("phase") == UPSTREAM_PHASE
        and review_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and review_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and review_sm.get("review_only") is True
    )
    if not review_verifier_trusted and not review_summary_trusted:
        blockers.append("post-dryrun review verifier must be GO")
    if review_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if (review_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")
    if positive.get("all_positive_flows_pass") is not True:
        blockers.append("4 positive flows must pass")
    if (positive.get("positive_flows_passed") or 0) < 4:
        blockers.append("positive_flow_pass_count must be >= 4")
    if blocked.get("all_blocked_flows_stop_or_hold") is not True:
        blockers.append("4 blocked flows must stop/hold")
    if gate_review.get("enforcement_pass") is not True:
        blockers.append("12 gates enforcement_pass required")
    if (gate_review.get("gates_passed") or 0) < 12:
        blockers.append("gates_pass_count must be >= 12")
    if stop_review.get("review_pass") is not True:
        blockers.append("12 stop conditions must be verified")
    if review_sm.get("limited_runtime_trial_started_now") is True:
        blockers.append("limited_runtime_trial_started_now must be false")
    if review_sm.get("live_runtime_enabled_now") is True:
        blockers.append("live_runtime_enabled_now must be false")
    if single_chain.get("ready_for_single_chain_trial_planning") is not True:
        blockers.append("single_chain_trial_planning readiness must be true")

    cross_chain_off = [
        "ocr_provider_invoked_now",
        "real_ocr_provider_enabled_now",
        "paddleocr_invoked_now",
        "rapidocr_invoked_now",
        "navigation_action_triggered_now",
        "real_navigation_runtime_enabled_now",
        "task_state_committed_now",
        "task_manager_committed_now",
        "tts_invoked_now",
        "llm_invoked_now",
    ]
    for field in cross_chain_off:
        if review_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    for field in RUNTIME_BOUNDARY_FIELDS:
        if review_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    ctx = {
        "review_sm": review_sm,
        "review_vr": review_vr,
        "positive": positive,
        "blocked": blocked,
        "gate_review": gate_review,
        "stop_review": stop_review,
        "single_chain": single_chain,
    }
    return blockers, ctx


def run_vision_sample_frame_single_chain_limited_runtime_trial_planning_v1(
    *,
    vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root: str,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    review_root = Path(
        vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root
    ).expanduser().resolve()

    plan_out = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else review_root.parent / "vision_sample_frame_single_chain_limited_runtime_trial_planning"
    )

    dryrun_root = review_root.parent / "vision_ocr_navigation_task_limited_runtime_trial_dryrun"
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_post_dryrun_review_root": str(review_root),
        "upstream_dryrun_root": str(dryrun_root),
        "planned_single_chain_output_root": str(plan_out),
    }

    blockers, ctx = _validate_upstream(review_root)
    review_sm = ctx["review_sm"]
    review_vr = ctx["review_vr"]
    boundary_ok = len(blockers) == 0

    policy = {
        "policy_id": "vision_sample_frame_single_chain_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "vision_sample_frame_single_chain_design_only",
        "chain": "vision_only",
        "output_candidate_type": "visual_observation_candidate",
        "deferred_chains": ["ocr", "navigation", "task"],
        **meta,
    }

    input_review = {
        "review_id": "limited_runtime_post_dryrun_review_input_review_v1",
        "upstream_root": str(review_root),
        "upstream_verifier": review_vr.get("verifier"),
        "upstream_final_decision": review_sm.get("final_decision"),
        "positive_flows_passed": ctx["positive"].get("positive_flows_passed"),
        "blocked_flows_enforced": ctx["blocked"].get("blocked_flows_enforced"),
        "upstream_gates_passed": ctx["gate_review"].get("gates_passed"),
        "recommended_first_chain": ctx["single_chain"].get("recommended_first_chain"),
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    trial_scope = {
        "scope_id": "vision_sample_frame_trial_scope_v1",
        "trial_label": TRIAL_SCOPE,
        "single_chain": "vision_sample_frame",
        "input_to_output": "sample_or_fixture_frame_reference → visual_observation_candidate",
        "chains_excluded": ["ocr", "navigation", "task_midplatform"],
        "candidate_only": True,
        "no_live_runtime": True,
        **meta,
    }

    input_source_policy = {
        "policy_id": "vision_sample_frame_input_source_policy_v1",
        "allowed_sources": list(ALLOWED_INPUT_SOURCES),
        "forbidden_sources": list(FORBIDDEN_INPUT_SOURCES),
        "primary_upstream_artifacts": [
            str(dryrun_root / "vision_sample_frame_candidate_dryrun_v1.json"),
            str(dryrun_root / "limited_runtime_fixture_input_matrix_v1.json"),
        ],
        **meta,
    }

    candidate_schema = {
        "schema_id": "vision_sample_frame_candidate_schema_v1",
        "candidate_type": "visual_observation_candidate",
        "required_fields": [
            "candidate_id",
            "candidate_type",
            "sample_frame_reference",
            "fixture_frame_metadata",
            "controlled_frame_reference",
            "source_chain",
            "observation_timestamp",
            "trial_scope",
        ],
        "invariants": dict(CANDIDATE_INVARIANTS),
        "example_envelope": {
            "candidate_id": "voc_<uuid>",
            "candidate_type": "visual_observation_candidate",
            "sample_frame_reference": "sample_frame_ref_sc_001",
            "fixture_frame_metadata": "fixture_meta_sc_001",
            "controlled_frame_reference": "cf_ref_sc_001",
            "source_chain": SOURCE_CHAIN,
            "observation_timestamp": "ISO8601_planned_not_runtime",
            "trial_scope": TRIAL_SCOPE,
            **CANDIDATE_INVARIANTS,
        },
        **meta,
    }

    gate_matrix = {
        "matrix_id": "vision_sample_frame_gate_matrix_v1",
        "gates": [
            {
                "gate_id": g,
                "status": "required_closed_in_planning",
                "enforcement": "block_live_camera_model_fact_wm_memory",
            }
            for g in VISION_SINGLE_CHAIN_GATES
        ],
        "gates_total": len(VISION_SINGLE_CHAIN_GATES),
        **meta,
    }

    stop_matrix = {
        "matrix_id": "vision_sample_frame_stop_condition_matrix_v1",
        "conditions": list(STOP_CONDITIONS),
        "immediate_stop_triggers": [c["trigger"] for c in STOP_CONDITIONS if c.get("action") == "stop"],
        "hold_triggers": [c["trigger"] for c in STOP_CONDITIONS if c.get("action") == "hold"],
        **meta,
    }

    logging_plan = {
        "plan_id": "vision_sample_frame_logging_plan_v1",
        "allowed_write_root": str(plan_out),
        "allowed_artifact_types": [
            "single_chain_trial_trace",
            "frame_ref_verification_log",
            "gate_consumption_log",
            "candidate_envelope_snapshot",
        ],
        "forbidden_write_targets": ["Memory", "WorldModel", "SceneDelta", "protected", "HR", "DnAE", "repo__eval_out"],
        "logging_in_planning_phase": "plan_definition_only",
        **meta,
    }

    dryrun_plan = {
        "plan_id": "vision_sample_frame_dryrun_plan_v1",
        "next_phase": NEXT_PHASE,
        "dryrun_goals": [
            "consume fixture/sample frame metadata only",
            "emit visual_observation_candidate envelope",
            "verify vision single-chain gates and stop conditions",
            "no live camera",
            "no vision model",
            "no fact write",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "vision_sample_frame_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "vision_sample_frame_trial_planning_readiness_decision_v1",
        "final_decision": (
            FINAL_DECISION
            if boundary_ok
            else "VISION_SAMPLE_FRAME_SINGLE_CHAIN_LIMITED_RUNTIME_TRIAL_PLANNING_REQUIRES_FIXES"
        ),
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "single_chain_trial_started_now": False,
        "ready_for_vision_sample_frame_dryrun": boundary_ok,
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
        "vision_single_chain_gates_count": len(VISION_SINGLE_CHAIN_GATES),
        "single_chain_trial_started_now": False,
        **meta,
    }

    return {
        "vision_sample_frame_single_chain_planning_policy": policy,
        "limited_runtime_post_dryrun_review_input_review": input_review,
        "vision_sample_frame_trial_scope": trial_scope,
        "vision_sample_frame_input_source_policy": input_source_policy,
        "vision_sample_frame_candidate_schema": candidate_schema,
        "vision_sample_frame_gate_matrix": gate_matrix,
        "vision_sample_frame_stop_condition_matrix": stop_matrix,
        "vision_sample_frame_logging_plan": logging_plan,
        "vision_sample_frame_dryrun_plan": dryrun_plan,
        "vision_sample_frame_non_claims_register": non_claims,
        "vision_sample_frame_trial_planning_readiness_decision": readiness,
        "summary": summary,
    }
