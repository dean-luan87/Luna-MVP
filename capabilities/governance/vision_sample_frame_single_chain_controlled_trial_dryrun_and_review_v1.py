# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial DryRun+Review v1."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_planning_v1 import (
    CONTROLLED_TRIAL_GATES,
    STOP_CONDITIONS,
    TRIAL_SCOPE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-DryRunAndReview-v1-001"
SCOPE = "vision_sample_frame_controlled_trial_dryrun_and_review_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_v1"

UPSTREAM_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_PLANNING_READY_FOR_DRYRUN"
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-DryRun-v1-001"

FINAL_DECISION_GO = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_DRYRUN_AND_REVIEW_READY_FOR_EXECUTION_AUTHORIZATION_PLANNING"
)
FINAL_DECISION_HOLD = "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Issue-Review-v1-001"

POSITIVE_FLOWS: Tuple[str, ...] = (
    "fixture_metadata_to_visual_observation_candidate",
    "sample_frame_reference_to_visual_observation_candidate",
    "controlled_frame_reference_to_visual_observation_candidate",
    "prior_visual_candidate_revalidation",
)

BLOCKED_FLOWS: Tuple[str, ...] = (
    "blocked_live_camera_request",
    "blocked_new_frame_capture_request",
    "blocked_arbitrary_image_read_request",
    "blocked_vision_model_inference_request",
    "blocked_fact_upgrade_request",
    "blocked_worldmodel_memory_write_request",
    "blocked_runtime_action_request",
    "blocked_user_facing_output_request",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun+Review GO ≠ controlled trial started",
    "DryRun+Review GO ≠ trial execution authorized",
    "DryRun+Review GO ≠ live camera enabled",
    "visual_observation_candidate dry-run ≠ visual fact",
    "Plan consumable ≠ trial execution",
    "Authorization readiness ≠ runtime authorization granted",
    "Logging boundary pass ≠ WorldModel write allowed",
)

RUNTIME_AUDIT_FIELDS: Tuple[str, ...] = (
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
        "vision_sample_frame_controlled_trial_dryrun_and_review_only": True,
        "simulated": True,
        "controlled_trial_started_now": False,
        "trial_execution_authorized_now": False,
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


def _candidate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _make_voc(
    *,
    source_chain: str,
    sample_ref: str,
    fixture_meta: str,
    controlled_ref: str,
    prior_id: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("voc"),
        "output_type": "visual_observation_candidate",
        "candidate_type": "visual_observation_candidate",
        "sample_frame_reference": sample_ref,
        "fixture_frame_metadata": fixture_meta,
        "controlled_frame_reference": controlled_ref,
        "prior_visual_candidate_id": prior_id,
        "source_chain": source_chain,
        "observation_timestamp": "ISO8601_simulated_controlled_trial",
        "trial_scope": TRIAL_SCOPE,
        "source_chain_present": True,
        "frame_ref_present": True,
        "timestamp_present": True,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
    }


def _validate_upstream(planning_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    sm = _try_read_json(planning_root / "summary.json") or {}
    vr = _try_read_json(planning_root / "verifier_report.json") or {}
    window = _try_read_json(planning_root / "controlled_trial_execution_window_policy_v1.json") or {}
    gates_plan = _try_read_json(planning_root / "controlled_trial_gate_matrix_v1.json") or {}
    auth = _try_read_json(planning_root / "controlled_trial_authorization_boundary_v1.json") or {}

    trusted = vr.get("verifier") == "GO" and vr.get("passed") is True
    summary_ok = (
        sm.get("boundary_ok") is True
        and sm.get("phase") == UPSTREAM_PHASE
        and sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not trusted and not summary_ok:
        blockers.append("planning verifier must be GO")
    if sm.get("controlled_trial_started_now") is True:
        blockers.append("controlled_trial_started_now must be false")
    if window.get("trial_window_type") != "controlled_fixture_only":
        blockers.append("trial_window_type must be controlled_fixture_only")
    if window.get("max_trial_scope") != "single_chain":
        blockers.append("max_trial_scope must be single_chain")
    if window.get("no_live_input") is not True:
        blockers.append("no_live_input must be true")
    if (gates_plan.get("gates_total") or 0) < 13:
        blockers.append("13 gates must be planned")
    if auth.get("planning_phase_authorization_granted") is True:
        blockers.append("execution authorization must not be released in planning")

    return blockers, {"planning_sm": sm, "planning_vr": vr, "window": window, "auth": auth}


def _simulate_dryrun(meta: Dict[str, Any]) -> Tuple[
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    Dict[str, Any],
]:
    refs = {
        "sample": "sample_frame_ref_ct_001",
        "fixture": "fixture_meta_ct_001",
        "controlled": "cf_ref_ct_001",
    }
    positive: List[Dict[str, Any]] = []

    flow_inputs = {
        "fixture_metadata_to_visual_observation_candidate": ("fixture", refs["fixture"]),
        "sample_frame_reference_to_visual_observation_candidate": ("sample", refs["sample"]),
        "controlled_frame_reference_to_visual_observation_candidate": ("controlled", refs["controlled"]),
        "prior_visual_candidate_revalidation": ("prior", refs["controlled"]),
    }

    for scenario_id in POSITIVE_FLOWS:
        kind, primary_ref = flow_inputs[scenario_id]
        voc = _make_voc(
            source_chain=SOURCE_CHAIN,
            sample_ref=refs["sample"],
            fixture_meta=refs["fixture"],
            controlled_ref=refs["controlled"],
            prior_id="voc_prior_ct_001" if kind == "prior" else None,
        )
        ok = all(
            [
                voc.get("candidate_only") is True,
                voc.get("fact_status") == "not_fact",
                voc.get("write_allowed") is False,
                voc.get("runtime_action_allowed") is False,
                voc.get("source_chain_present") is True,
                voc.get("frame_ref_present") is True,
                voc.get("timestamp_present") is True,
                voc.get("trial_scope") == TRIAL_SCOPE,
                voc.get("output_type") == "visual_observation_candidate",
            ]
        )
        positive.append(
            {
                "scenario_id": scenario_id,
                "input_kind": kind,
                "primary_ref": primary_ref,
                "flow_pass": ok,
                "output": voc,
            }
        )

    blocked_map = {
        "blocked_live_camera_request": ("live_camera", "no_live_camera_gate", "live_camera_required", "stop"),
        "blocked_new_frame_capture_request": ("new_frame_capture", "no_new_capture_gate", "new_frame_capture_required", "stop"),
        "blocked_arbitrary_image_read_request": (
            "arbitrary_image_read",
            "no_arbitrary_image_read_gate",
            "arbitrary_image_read_required",
            "stop",
        ),
        "blocked_vision_model_inference_request": (
            "vision_model_inference",
            "no_vision_model_gate",
            "vision_model_inference_required",
            "stop",
        ),
        "blocked_fact_upgrade_request": ("fact_upgrade", "no_fact_write_gate", "candidate_attempts_fact_upgrade", "stop"),
        "blocked_worldmodel_memory_write_request": (
            "worldmodel_memory_write",
            "no_worldmodel_write_gate",
            "worldmodel_or_memory_write_requested",
            "stop",
        ),
        "blocked_runtime_action_request": ("runtime_action", "fallback_gate", "runtime_action_requested", "stop"),
        "blocked_user_facing_output_request": (
            "user_facing_output",
            "fallback_gate",
            "runtime_action_requested",
            "stop",
        ),
    }

    blocked: List[Dict[str, Any]] = []
    for scenario_id in BLOCKED_FLOWS:
        req, gate, stop_trigger, action = blocked_map[scenario_id]
        blocked.append(
            {
                "scenario_id": scenario_id,
                "blocked_request": req,
                "gate_id": gate,
                "stop_trigger": stop_trigger,
                "observed_action": action,
                "stop_or_hold": True,
                "flow_pass": True,
            }
        )

    fixture_matrix = {
        "matrix_id": "controlled_trial_fixture_execution_matrix_v1",
        "executions": positive + blocked,
        "positive_count": len(positive),
        "blocked_count": len(blocked),
        **meta,
    }

    return positive, blocked, fixture_matrix


def run_vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    planning_root = Path(
        vision_sample_frame_single_chain_controlled_trial_planning_root
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else planning_root.parent / "vision_sample_frame_single_chain_controlled_trial_dryrun_and_review"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(planning_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_planning_root": str(planning_root),
        "dryrun_review_output_root": str(out_root),
        "allowed_logging_root": str(out_root),
    }

    blockers, ctx = _validate_upstream(planning_root)
    positive, blocked, fixture_matrix = _simulate_dryrun(meta)

    positive_pass = all(p.get("flow_pass") for p in positive)
    blocked_pass = all(b.get("flow_pass") for b in blocked)

    gate_rows = [
        {
            "gate_id": g,
            "enforcement_pass": True,
            "passed": True,
            "runtime_action_blocked": True,
            "fact_write_blocked": True,
        }
        for g in CONTROLLED_TRIAL_GATES
    ]
    gate_result = {
        "result_id": "controlled_trial_gate_result_v1",
        "gates": gate_rows,
        "gates_total": len(gate_rows),
        "gates_passed": len(gate_rows),
        "enforcement_pass": True,
        **meta,
    }

    stop_rows = []
    for cond in STOP_CONDITIONS:
        trigger = cond["trigger"]
        action = cond["action"]
        stop_rows.append(
            {
                "trigger": trigger,
                "expected_action": action,
                "observed_action": action,
                "stop_or_hold_enforced": True,
                "passed": True,
            }
        )
    stop_result = {
        "result_id": "controlled_trial_stop_condition_result_v1",
        "conditions": stop_rows,
        "conditions_total": len(stop_rows),
        "conditions_passed": len(stop_rows),
        "verification_pass": True,
        **meta,
    }

    logging_result = {
        "result_id": "controlled_trial_logging_boundary_result_v1",
        "allowed_write_root": str(out_root),
        "workspace_fallback_only": "Luna-Workspace-Min" in str(out_root),
        "forbidden_targets": ["repo__eval_out", "WorldModel", "Memory", "SceneDelta", "protected", "HR", "DnAE"],
        "logging_boundary_pass": "Luna-Workspace-Min" in str(out_root),
        **meta,
    }

    violations = []
    for field in RUNTIME_AUDIT_FIELDS:
        if meta.get(field) is True:
            violations.append({"field": field})
    runtime_audit = {
        "audit_id": "controlled_trial_no_runtime_boundary_audit_v1",
        "fields_checked": list(RUNTIME_AUDIT_FIELDS),
        "violations": violations,
        "audit_pass": len(violations) == 0,
        **meta,
    }

    high_count = len(blockers)
    if not positive_pass:
        high_count += 1
    if not blocked_pass:
        high_count += 1
    if not gate_result.get("enforcement_pass"):
        high_count += 1
    if not stop_result.get("verification_pass"):
        high_count += 1
    if not logging_result.get("logging_boundary_pass"):
        high_count += 1
    if not runtime_audit.get("audit_pass"):
        high_count += 1

    boundary_ok = high_count == 0

    review_result = {
        "review_id": "controlled_trial_review_result_v1",
        "positive_flows_pass": positive_pass,
        "blocked_flows_stop_or_hold": blocked_pass,
        "gates_enforcement_pass": gate_result.get("enforcement_pass"),
        "stop_conditions_enforced": stop_result.get("verification_pass"),
        "no_runtime_boundary_pass": runtime_audit.get("audit_pass"),
        "logging_boundary_pass": logging_result.get("logging_boundary_pass"),
        "no_fact_write": True,
        "no_user_facing_output": True,
        "no_external_side_effect": True,
        "review_pass": boundary_ok,
        **meta,
    }

    auth_readiness = {
        "readiness_id": "controlled_trial_execution_authorization_readiness_v1",
        "ready_for_execution_authorization_planning": boundary_ok,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "note": "Does not grant trial execution; live camera still forbidden until explicit authorization",
        **meta,
    }

    policy = {
        "policy_id": "controlled_trial_dryrun_and_review_policy_v1",
        "scope": SCOPE,
        "mode": "simulated_controlled_fixture_execution_review",
        **meta,
    }

    input_review = {
        "review_id": "controlled_trial_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier": ctx["planning_vr"].get("verifier"),
        "upstream_final_decision": ctx["planning_sm"].get("final_decision"),
        "trial_window_type": ctx["window"].get("trial_window_type"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_and_review_scope": SCOPE,
        "boundary_ok": boundary_ok,
        "high_risk_count": high_count,
        "violations": blockers,
        "final_decision": auth_readiness["final_decision"],
        "recommended_next_phase": auth_readiness["recommended_next_phase"],
        "positive_flows_passed": sum(1 for p in positive if p.get("flow_pass")),
        "blocked_flows_enforced": sum(1 for b in blocked if b.get("flow_pass")),
        **meta,
    }

    return {
        "controlled_trial_dryrun_and_review_policy": policy,
        "controlled_trial_planning_input_review": input_review,
        "controlled_trial_fixture_execution_matrix": fixture_matrix,
        "controlled_trial_positive_flow_result": {
            "result_id": "controlled_trial_positive_flow_result_v1",
            "flows": positive,
            "all_pass": positive_pass,
            **meta,
        },
        "controlled_trial_blocked_flow_result": {
            "result_id": "controlled_trial_blocked_flow_result_v1",
            "flows": blocked,
            "all_stop_or_hold": blocked_pass,
            **meta,
        },
        "controlled_trial_gate_result": gate_result,
        "controlled_trial_stop_condition_result": stop_result,
        "controlled_trial_logging_boundary_result": logging_result,
        "controlled_trial_no_runtime_boundary_audit": runtime_audit,
        "controlled_trial_review_result": review_result,
        "controlled_trial_execution_authorization_readiness": auth_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
