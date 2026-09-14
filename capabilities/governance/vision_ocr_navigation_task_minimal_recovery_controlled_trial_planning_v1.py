# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Minimal Recovery Controlled Trial Planning v1.

Finite controlled trial design after post-dryrun review GO. Planning-only; trial not started.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Controlled-Trial-Planning-v1-001"
PLANNING_SCOPE = "controlled_trial_planning_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CONTROLLED_TRIAL_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Controlled-Trial-Planning-v1-001"

FINAL_DECISION = "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_CONTROLLED_TRIAL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Controlled-Trial-DryRun-v1-001"

TRIAL_GATES: Tuple[str, ...] = (
    "safety_gate",
    "source_chain_gate",
    "task_scope_gate",
    "runtime_disabled_gate",
    "no_camera_gate",
    "no_ocr_provider_gate",
    "no_navigation_action_gate",
    "no_task_commit_gate",
    "no_worldmodel_write_gate",
    "no_memory_write_gate",
    "no_tts_gate",
    "fallback_gate",
)

CANDIDATE_INVARIANTS: Dict[str, Any] = {
    "candidate_only": True,
    "fact_status": "not_fact",
    "write_allowed": False,
    "runtime_action_allowed": False,
}

ALLOWED_INPUT_SOURCES: Tuple[str, ...] = (
    "controlled_frame_reference",
    "visual_focus_reference",
    "track_reference_artifacts",
    "dryrun_candidate_objects",
    "synthetic_fixture_candidate_input",
)

FORBIDDEN_INPUT_SOURCES: Tuple[str, ...] = (
    "real_camera_capture",
    "new_image_read",
    "live_ocr_provider",
    "live_navigation_action",
    "live_task_commit",
    "user_facing_speech_output",
)

FLOW_STEPS: Tuple[Dict[str, str], ...] = (
    {"step": 1, "output": "visual_observation_candidate"},
    {"step": 2, "output": "task_observation_requirement"},
    {"step": 3, "output": "ocr_request_candidate", "condition": "if_task_requires_text"},
    {"step": 4, "output": "navigation_guidance_candidate", "condition": "if_task_requires_movement"},
    {"step": 5, "output": "task_response_candidate"},
)

STOP_CONDITIONS: Tuple[Dict[str, str], ...] = (
    {"trigger": "real_camera_required", "action": "stop"},
    {"trigger": "ocr_provider_required", "action": "stop"},
    {"trigger": "real_navigation_action_required", "action": "stop"},
    {"trigger": "task_commit_required", "action": "stop"},
    {"trigger": "tts_or_llm_required", "action": "stop"},
    {"trigger": "memory_or_worldmodel_write_required", "action": "stop"},
    {"trigger": "source_chain_missing", "action": "hold"},
    {"trigger": "candidate_upgrade_to_fact", "action": "stop"},
    {"trigger": "midplatform_dual_directory_routing_ambiguity", "action": "hold"},
    {"trigger": "safety_gate_fail", "action": "stop"},
    {"trigger": "fallback_gate_unhandled", "action": "hold"},
)

NON_CLAIMS: Tuple[str, ...] = (
    "Controlled Trial Planning GO ≠ controlled trial started",
    "Controlled Trial Planning GO ≠ runtime enabled",
    "Controlled input source planned ≠ camera invoked",
    "OCR request candidate ≠ OCR provider invoked",
    "Navigation guidance candidate ≠ navigation action",
    "Task response candidate ≠ TTS invoked",
    "candidate flow ≠ fact write",
    "logging plan ≠ Memory / WorldModel write allowed",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "ocr_provider_invoked_now",
    "ocr_evidence_generated_now",
    "navigation_action_triggered_now",
    "map_write_executed_now",
    "gps_strong_anchor_committed_now",
    "task_state_committed_now",
    "task_manager_committed_now",
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
        "controlled_trial_planning_only": True,
        "controlled_trial_started_now": False,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_provider_invoked_now": False,
        "ocr_evidence_generated_now": False,
        "navigation_action_triggered_now": False,
        "map_write_executed_now": False,
        "gps_strong_anchor_committed_now": False,
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
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning_v1(
    *,
    vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_root: str,
    trial_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(
        vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_root
    ).expanduser().resolve()
    dryrun_root = review_root.parent / "vision_ocr_navigation_task_minimal_recovery_execution_dryrun"

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    trial_out = (
        Path(trial_output_root).expanduser().resolve()
        if trial_output_root
        else review_root.parent / "vision_ocr_navigation_task_minimal_recovery_controlled_trial_planning"
    )

    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_post_dryrun_review_root": str(review_root),
        "planned_trial_output_root": str(trial_out),
        "workspace_fallback_trial_logging_only": True,
    }

    review_sm = _try_read_json(review_root / "summary.json") or {}
    review_vr = _try_read_json(review_root / "verifier_report.json") or {}
    scenario_rev = _try_read_json(review_root / "scenario_pass_review_v1.json") or {}
    gate_rev = _try_read_json(review_root / "execution_gate_review_v1.json") or {}
    trial_ready = _try_read_json(review_root / "controlled_trial_planning_readiness_v1.json") or {}

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
    if scenario_rev.get("all_scenarios_pass") is not True:
        blockers.append("all scenarios must pass")
    if scenario_rev.get("all_candidates_candidate_only") is not True:
        blockers.append("all candidates must be candidate_only")
    if scenario_rev.get("all_candidates_not_fact") is not True:
        blockers.append("all candidates must be not_fact")
    if gate_rev.get("gates_passed", 0) < 11:
        blockers.append("gates_pass_count must be >= 11")
    if trial_ready.get("ready_for_controlled_trial_planning") is not True:
        blockers.append("controlled_trial_planning readiness must be true")

    for field in RUNTIME_BOUNDARY_FIELDS:
        if review_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    boundary_ok = not blockers

    policy = {
        "policy_id": "controlled_trial_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "finite_controlled_trial_design_only",
        "p0_chains": ["vision", "ocr", "navigation", "task_midplatform"],
        **meta,
    }

    input_review = {
        "review_id": "post_dryrun_review_input_review_v1",
        "upstream_root": str(review_root),
        "upstream_verifier": review_vr.get("verifier"),
        "upstream_final_decision": review_sm.get("final_decision"),
        "scenario_pass_count": review_sm.get("scenario_pass_count"),
        "gates_passed_upstream": gate_rev.get("gates_passed"),
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    scope_matrix = {
        "matrix_id": "controlled_trial_scope_matrix_v1",
        "trial_label": "minimal_recovery_controlled_trial_v1",
        "chains": ["vision", "ocr", "navigation", "task_midplatform"],
        "candidate_only": True,
        "max_simulation_depth": "candidate_envelope_and_gate_trace",
        "no_runtime_execution": True,
        **meta,
    }

    input_source_policy = {
        "policy_id": "controlled_trial_input_source_policy_v1",
        "allowed_sources": list(ALLOWED_INPUT_SOURCES),
        "forbidden_sources": list(FORBIDDEN_INPUT_SOURCES),
        "primary_upstream_artifacts": [
            str(dryrun_root / "cross_chain_candidate_flow_trace_v1.json"),
            str(dryrun_root / "dryrun_scenario_matrix_v1.json"),
        ],
        "synthetic_fixture_note": "fixture inputs must be labeled synthetic and not_fact",
        **meta,
    }

    candidate_flow = {
        "plan_id": "controlled_trial_allowed_candidate_flow_v1",
        "flow_label": "controlled_trial_candidate_only_loop",
        "steps": list(FLOW_STEPS),
        "candidate_invariants": dict(CANDIDATE_INVARIANTS),
        "diagram": " → ".join(s["output"] for s in FLOW_STEPS),
        **meta,
    }

    gate_matrix = {
        "matrix_id": "controlled_trial_gate_matrix_v1",
        "gates": [
            {
                "gate_id": g,
                "status": "required_closed_in_planning",
                "enforcement": "block_runtime_and_fact_write",
            }
            for g in TRIAL_GATES
        ],
        "gates_total": len(TRIAL_GATES),
        **meta,
    }

    stop_matrix = {
        "matrix_id": "controlled_trial_stop_condition_matrix_v1",
        "conditions": list(STOP_CONDITIONS),
        "immediate_stop_triggers": [
            c["trigger"]
            for c in STOP_CONDITIONS
            if c.get("action") == "stop"
        ],
        "hold_triggers": [
            c["trigger"] for c in STOP_CONDITIONS if c.get("action") == "hold"
        ],
        **meta,
    }

    logging_plan = {
        "plan_id": "controlled_trial_observation_logging_plan_v1",
        "allowed_write_root": str(trial_out),
        "allowed_artifact_types": [
            "trial_trace",
            "gate_consumption_log",
            "candidate_envelope_snapshot",
            "stop_event_log",
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
        "logging_in_planning_phase": "plan_definition_only_no_trial_logs_yet",
        **meta,
    }

    no_fact_policy = {
        "policy_id": "controlled_trial_no_fact_write_policy_v1",
        "fact_write_allowed": False,
        "candidate_upgrade_to_fact_blocked": True,
        "world_model_write_blocked": True,
        "memory_write_blocked": True,
        "scene_delta_write_blocked": True,
        **meta,
    }

    fallback_plan = {
        "plan_id": "controlled_trial_fallback_plan_v1",
        "inherits_from": "minimal_recovery_execution_dryrun",
        "rules": [
            {"condition": "stop_condition_triggered", "action": "halt_trial", "log": True},
            {"condition": "gate_breach", "action": "halt_trial", "log": True},
            {"condition": "midplatform_routing_ambiguity", "action": "hold", "defer_phase": "Midplatform-Structure-Cleanup"},
        ],
        **meta,
    }

    dryrun_plan = {
        "plan_id": "controlled_trial_dryrun_plan_v1",
        "next_phase": NEXT_PHASE,
        "dryrun_goals": [
            "simulate controlled trial input",
            "verify candidate flow under gates",
            "verify stop conditions",
            "verify gate enforcement trace",
            "no runtime enabled",
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
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_CONTROLLED_TRIAL_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
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
        "trial_gates_count": len(TRIAL_GATES),
        "controlled_trial_started_now": False,
        **meta,
    }

    return {
        "controlled_trial_planning_policy": policy,
        "post_dryrun_review_input_review": input_review,
        "controlled_trial_scope_matrix": scope_matrix,
        "controlled_trial_input_source_policy": input_source_policy,
        "controlled_trial_allowed_candidate_flow": candidate_flow,
        "controlled_trial_gate_matrix": gate_matrix,
        "controlled_trial_stop_condition_matrix": stop_matrix,
        "controlled_trial_observation_logging_plan": logging_plan,
        "controlled_trial_no_fact_write_policy": no_fact_policy,
        "controlled_trial_fallback_plan": fallback_plan,
        "controlled_trial_dryrun_plan": dryrun_plan,
        "controlled_trial_non_claims_register": non_claims,
        "controlled_trial_planning_readiness_decision": readiness,
        "summary": summary,
    }
