# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Planning v1.

Plans controlled trial execution window after harness closure + plan+dryrun GO.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Planning-v1-001"
PLANNING_SCOPE = "vision_sample_frame_controlled_trial_planning_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_planning_v1"
TRIAL_SCOPE = "vision_sample_frame_single_chain"

UPSTREAM_CLOSURE_PHASE = "Phase-Single-Chain-Trial-Validation-Harness-Extraction-Validation-Closure-v1-001"
UPSTREAM_CLOSURE_FINAL = (
    "SINGLE_CHAIN_TRIAL_VALIDATION_HARNESS_VALIDATION_CLOSED_READY_FOR_VISION_SAMPLE_FRAME_CONTROLLED_TRIAL_PLANNING"
)
UPSTREAM_CLOSURE_NEXT = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Planning-v1-001"

UPSTREAM_PAD_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-PlanAndDryRun-v1-001"
UPSTREAM_PAD_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_PLAN_AND_DRYRUN_READY_FOR_CONTROLLED_TRIAL_PLANNING"
)

FINAL_DECISION = "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-DryRun-v1-001"

CONTROLLED_TRIAL_GATES: Tuple[str, ...] = (
    "safety_gate",
    "source_chain_gate",
    "fixture_or_controlled_input_gate",
    "frame_ref_gate",
    "timestamp_gate",
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
    {"trigger": "vision_model_inference_required", "action": "stop"},
    {"trigger": "missing_frame_ref", "action": "hold"},
    {"trigger": "missing_source_chain", "action": "hold"},
    {"trigger": "missing_timestamp", "action": "hold"},
    {"trigger": "candidate_attempts_fact_upgrade", "action": "stop"},
    {"trigger": "worldmodel_or_memory_write_requested", "action": "stop"},
    {"trigger": "runtime_action_requested", "action": "stop"},
    {"trigger": "safety_gate_failed", "action": "stop"},
    {"trigger": "fixture_control_input_unverifiable", "action": "hold"},
)

ALLOWED_INPUTS: Tuple[str, ...] = (
    "existing_sample_frame_reference",
    "fixture_frame_metadata",
    "controlled_frame_reference",
    "prior_dryrun_visual_candidate_object",
)

FORBIDDEN_INPUTS: Tuple[str, ...] = (
    "live_camera",
    "new_frame_capture",
    "arbitrary_image_read",
    "visual_model_inference",
    "ocr_provider",
    "navigation_action",
    "task_commit",
    "user_facing_speech",
    "worldmodel_write",
    "memory_write",
    "scene_delta_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Controlled Trial Planning GO ≠ controlled trial started",
    "Controlled trial planned ≠ live camera enabled",
    "sample frame reference planned ≠ new image capture",
    "visual_observation_candidate planned ≠ visual fact",
    "DryRun plan ≠ trial execution",
    "Authorization boundary planned ≠ runtime authorization granted",
    "Harness closure ≠ automatic trial execution",
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
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "vision_sample_frame_controlled_trial_planning_only": True,
        "controlled_trial_started_now": False,
        "single_chain_trial_started_now": False,
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
        "navigation_action_triggered_now": False,
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


def run_vision_sample_frame_single_chain_controlled_trial_planning_v1(
    *,
    single_chain_trial_validation_harness_validation_closure_root: str,
    vision_sample_frame_single_chain_plan_and_dryrun_root: str,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    closure_root = Path(
        single_chain_trial_validation_harness_validation_closure_root
    ).expanduser().resolve()
    pad_root = Path(vision_sample_frame_single_chain_plan_and_dryrun_root).expanduser().resolve()

    plan_out = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else closure_root.parent / "vision_sample_frame_single_chain_controlled_trial_planning"
    )

    blockers: List[str] = []
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(closure_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_closure_root": str(closure_root),
        "upstream_plan_and_dryrun_root": str(pad_root),
        "planned_controlled_trial_output_root": str(plan_out),
    }

    closure_sm = _try_read_json(closure_root / "summary.json") or {}
    closure_vr = _try_read_json(closure_root / "verifier_report.json") or {}
    closure_dec = _try_read_json(closure_root / "single_chain_harness_validation_closure_decision_v1.json") or {}

    pad_sm = _try_read_json(pad_root / "summary.json") or {}
    pad_vr = _try_read_json(pad_root / "verifier_report.json") or {}
    positive = _try_read_json(pad_root / "vision_sample_frame_positive_flow_result_v1.json") or {}
    blocked = _try_read_json(pad_root / "vision_sample_frame_blocked_flow_result_v1.json") or {}
    gates_pad = _try_read_json(pad_root / "vision_sample_frame_gate_result_v1.json") or {}
    stops_pad = _try_read_json(pad_root / "vision_sample_frame_stop_condition_result_v1.json") or {}

    closure_trusted = closure_vr.get("verifier") == "GO" and closure_vr.get("passed") is True
    closure_ok = (
        closure_sm.get("boundary_ok") is True
        and closure_sm.get("phase") == UPSTREAM_CLOSURE_PHASE
        and closure_sm.get("final_decision") == UPSTREAM_CLOSURE_FINAL
        and closure_sm.get("recommended_next_phase") == UPSTREAM_CLOSURE_NEXT
    )
    if not closure_trusted and not closure_ok:
        blockers.append("harness validation closure verifier must be GO")
    if closure_sm.get("harness_contract_validated_now") is not True:
        blockers.append("harness_contract_validated_now must be true")
    if closure_sm.get("harness_module_present_now") is not True:
        blockers.append("harness_module_present_now must be true")
    if closure_sm.get("harness_first_consumer_validated_now") is not True:
        blockers.append("harness_first_consumer_validated_now must be true")
    if closure_dec.get("harness_validation_closed") is not True:
        blockers.append("harness_validation_closed must be true")

    pad_trusted = pad_vr.get("verifier") == "GO" and pad_vr.get("passed") is True
    pad_ok = (
        pad_sm.get("boundary_ok") is True
        and pad_sm.get("phase") == UPSTREAM_PAD_PHASE
        and pad_sm.get("final_decision") == UPSTREAM_PAD_FINAL
    )
    if not pad_trusted and not pad_ok:
        blockers.append("vision plan+dryrun verifier must be GO")
    if positive.get("all_pass") is not True:
        blockers.append("positive flows must pass")
    if blocked.get("all_stop_or_hold") is not True:
        blockers.append("blocked flows must stop/hold")
    if gates_pad.get("enforcement_pass") is not True:
        blockers.append("gates enforcement_pass required")
    if stops_pad.get("verification_pass") is not True:
        blockers.append("stop conditions verification_pass required")

    for field in RUNTIME_BOUNDARY_FIELDS:
        if closure_sm.get(field) is True or pad_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    boundary_ok = len(blockers) == 0

    policy = {
        "policy_id": "vision_sample_frame_controlled_trial_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "controlled_fixture_only_trial_design",
        "chain_id": "vision_sample_frame",
        **meta,
    }

    harness_review = {
        "review_id": "harness_validation_input_review_v1",
        "upstream_root": str(closure_root),
        "upstream_verifier": closure_vr.get("verifier"),
        "upstream_final_decision": closure_sm.get("final_decision"),
        "harness_contract_validated": closure_sm.get("harness_contract_validated"),
        "harness_first_consumer_validated": closure_sm.get("harness_first_consumer_validated"),
        "review_pass": closure_ok,
        "blockers": [b for b in blockers if "harness" in b or "closure" in b],
        **meta,
    }

    pad_review = {
        "review_id": "vision_plan_and_dryrun_input_review_v1",
        "upstream_root": str(pad_root),
        "upstream_verifier": pad_vr.get("verifier"),
        "upstream_final_decision": pad_sm.get("final_decision"),
        "positive_flows_passed": positive.get("flows_passed"),
        "blocked_flows_enforced": blocked.get("flows_enforced"),
        "gates_passed": gates_pad.get("gates_passed"),
        "review_pass": pad_ok,
        **meta,
    }

    trial_scope = {
        "scope_id": "controlled_trial_scope_v1",
        "trial_label": "vision_sample_frame_controlled_trial_v1",
        "trial_scope": TRIAL_SCOPE,
        "single_chain_only": True,
        "output_type": "visual_observation_candidate",
        "input_to_output": "controlled/sample/fixture frame reference → visual_observation_candidate",
        "no_live_runtime": True,
        **meta,
    }

    allowlist = {
        "policy_id": "controlled_trial_input_allowlist_v1",
        "allowed_inputs": list(ALLOWED_INPUTS),
        "forbidden_inputs": list(FORBIDDEN_INPUTS),
        **meta,
    }

    execution_window = {
        "policy_id": "controlled_trial_execution_window_policy_v1",
        "trial_window_type": "controlled_fixture_only",
        "max_trial_scope": "single_chain",
        "max_output_count_default": 3,
        "max_output_count_configurable": True,
        "no_live_input": True,
        "no_external_provider": True,
        "no_user_facing_output": True,
        "controlled_trial_started_in_planning": False,
        **meta,
    }

    gate_matrix = {
        "matrix_id": "controlled_trial_gate_matrix_v1",
        "gates": [
            {
                "gate_id": g,
                "status": "required_closed_until_controlled_dryrun",
                "enforcement": "block_live_input_fact_write_side_effects",
            }
            for g in CONTROLLED_TRIAL_GATES
        ],
        "gates_total": len(CONTROLLED_TRIAL_GATES),
        **meta,
    }

    stop_matrix = {
        "matrix_id": "controlled_trial_stop_condition_matrix_v1",
        "conditions": list(STOP_CONDITIONS),
        **meta,
    }

    success_criteria = {
        "criteria_id": "controlled_trial_success_criteria_v1",
        "criteria": [
            {"criterion": "controlled_input_accepted", "required": True},
            {"criterion": "visual_observation_candidate_generated", "required": True},
            {"criterion": "candidate_only_true", "required": True},
            {"criterion": "fact_status_not_fact", "required": True},
            {"criterion": "all_gates_pass", "required": True},
            {"criterion": "all_stop_conditions_enforceable", "required": True},
            {"criterion": "no_runtime_boundary_violation", "required": True},
            {"criterion": "no_fact_write", "required": True},
            {"criterion": "no_external_side_effect", "required": True},
        ],
        "output_invariants": {
            "output_type": "visual_observation_candidate",
            "candidate_only": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "runtime_action_allowed": False,
            "source_chain_present": True,
            "frame_ref_present": True,
            "timestamp_present": True,
            "trial_scope": TRIAL_SCOPE,
        },
        **meta,
    }

    logging_policy = {
        "policy_id": "controlled_trial_logging_policy_v1",
        "allowed_write_root": str(plan_out),
        "allowed_artifact_types": [
            "controlled_trial_trace",
            "frame_ref_verification_log",
            "gate_enforcement_log",
            "candidate_envelope_snapshot",
        ],
        "forbidden_write_targets": [
            "Memory",
            "WorldModel",
            "SceneDelta",
            "protected",
            "HR",
            "DnAE",
            "repo__eval_out",
        ],
        **meta,
    }

    abort_policy = {
        "policy_id": "controlled_trial_abort_and_rollback_policy_v1",
        "on_stop_condition": {"action": "halt_trial", "log": True, "rollback": "no_state_committed"},
        "on_gate_breach": {"action": "halt_trial", "log": True},
        "on_runtime_boundary_violation": {"action": "immediate_stop", "log": True},
        "on_fact_upgrade_attempt": {"action": "stop_and_hold", "log": True},
        **meta,
    }

    auth_boundary = {
        "policy_id": "controlled_trial_authorization_boundary_v1",
        "planning_phase_authorization_granted": False,
        "trial_execution_authorization_required": True,
        "deferred_until": "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-v1-001",
        "requires_before_execution": [
            "controlled_trial_dryrun_go",
            "explicit_no_live_camera_ack",
            "explicit_no_fact_write_ack",
            "workspace_fallback_logging_only",
        ],
        "forbidden_without_authorization": [
            "live_camera",
            "vision_model_inference",
            "fact_write",
            "worldmodel_write",
            "memory_write",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "controlled_trial_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "controlled_trial_planning_readiness_decision_v1",
        "final_decision": (
            FINAL_DECISION
            if boundary_ok
            else "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_PLANNING_REQUIRES_FIXES"
        ),
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "ready_for_controlled_trial_dryrun": boundary_ok,
        "controlled_trial_started_now": False,
        "upstream_blockers": blockers,
        "note": "Next phase is Controlled Trial DryRun, not Trial Execution",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "controlled_trial_gates_count": len(CONTROLLED_TRIAL_GATES),
        **meta,
    }

    return {
        "vision_sample_frame_controlled_trial_planning_policy": policy,
        "harness_validation_input_review": harness_review,
        "vision_plan_and_dryrun_input_review": pad_review,
        "controlled_trial_scope": trial_scope,
        "controlled_trial_input_allowlist": allowlist,
        "controlled_trial_execution_window_policy": execution_window,
        "controlled_trial_gate_matrix": gate_matrix,
        "controlled_trial_stop_condition_matrix": stop_matrix,
        "controlled_trial_success_criteria": success_criteria,
        "controlled_trial_logging_policy": logging_policy,
        "controlled_trial_abort_and_rollback_policy": abort_policy,
        "controlled_trial_authorization_boundary": auth_boundary,
        "controlled_trial_non_claims_register": non_claims,
        "controlled_trial_planning_readiness_decision": readiness,
        "summary": summary,
    }
