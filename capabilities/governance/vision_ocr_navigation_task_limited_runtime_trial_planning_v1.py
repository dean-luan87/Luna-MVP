# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Limited Runtime Trial Planning v1.

Plans extremely limited near-real trial paths after controlled plan+dryrun GO. Planning-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Planning-v1-001"
PLANNING_SCOPE = "limited_runtime_trial_planning_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_limited_runtime_trial_planning_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Controlled-Trial-PlanAndDryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_CONTROLLED_TRIAL_PLAN_AND_DRYRUN_READY_FOR_LIMITED_RUNTIME_TRIAL_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Planning-v1-001"

FINAL_DECISION = "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-DryRun-v1-001"

LIMITED_RUNTIME_GATES: Tuple[str, ...] = (
    "safety_gate",
    "source_chain_gate",
    "task_scope_gate",
    "fixture_or_controlled_input_gate",
    "no_live_camera_gate",
    "no_real_ocr_provider_gate",
    "no_navigation_action_gate",
    "no_task_commit_gate",
    "no_worldmodel_write_gate",
    "no_memory_write_gate",
    "no_tts_gate",
    "fallback_gate",
)

STOP_CONDITIONS: Tuple[Dict[str, str], ...] = (
    {"trigger": "live_camera_required", "action": "stop"},
    {"trigger": "new_image_capture_required", "action": "stop"},
    {"trigger": "real_ocr_provider_required", "action": "stop"},
    {"trigger": "real_navigation_action_required", "action": "stop"},
    {"trigger": "task_commit_required", "action": "stop"},
    {"trigger": "tts_or_llm_required", "action": "stop"},
    {"trigger": "worldmodel_or_memory_write_required", "action": "stop"},
    {"trigger": "source_chain_missing", "action": "hold"},
    {"trigger": "candidate_upgrade_to_fact", "action": "stop"},
    {"trigger": "safety_gate_fail", "action": "stop"},
    {"trigger": "fixture_control_input_unverifiable", "action": "hold"},
    {"trigger": "midplatform_dual_directory_routing_ambiguity", "action": "hold"},
)

ALLOWED_INPUT_SOURCES: Tuple[str, ...] = (
    "existing_sample_frame_reference",
    "controlled_fixture_frame",
    "pre_existing_frame_metadata",
    "mock_ocr_provider_response",
    "fixture_ocr_response",
    "pre_existing_ocr_request_candidate",
    "readonly_map_hint",
    "synthetic_route_context",
    "dryrun_candidate_objects",
    "controlled_trial_fixture_artifacts",
)

FORBIDDEN_INPUT_SOURCES: Tuple[str, ...] = (
    "live_camera",
    "new_camera_capture",
    "arbitrary_image_read",
    "new_visual_model_inference",
    "paddle_ocr",
    "rapidocr",
    "real_ocr_provider",
    "real_navigation_action",
    "map_write",
    "gps_strong_anchor_commit",
    "task_state_commit",
    "task_manager_runtime_action",
    "tts",
    "llm",
    "worldmodel_write",
    "memory_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Limited Runtime Trial Planning GO ≠ limited runtime trial started",
    "Limited runtime scope planned ≠ live runtime enabled",
    "sample frame reference ≠ live camera",
    "mock OCR provider ≠ real OCR provider",
    "guidance candidate ≠ navigation action",
    "task response candidate ≠ task commit / TTS",
    "logging plan ≠ Memory / WorldModel write allowed",
    "ocr_result_candidate planned ≠ OCR fact generated",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "live_runtime_enabled_now",
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "image_read_executed_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "real_ocr_provider_enabled_now",
    "navigation_action_triggered_now",
    "real_navigation_runtime_enabled_now",
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
        "limited_runtime_trial_planning_only": True,
        "limited_runtime_trial_started_now": False,
        "controlled_trial_started_now": False,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_provider_invoked_now": False,
        "real_ocr_provider_enabled_now": False,
        "ocr_evidence_generated_now": False,
        "navigation_action_triggered_now": False,
        "real_navigation_runtime_enabled_now": False,
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


def _validate_upstream(upstream_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    upstream_sm = _try_read_json(upstream_root / "summary.json") or {}
    upstream_vr = _try_read_json(upstream_root / "verifier_report.json") or {}
    gate_result = _try_read_json(upstream_root / "controlled_trial_gate_result_v1.json") or {}
    stop_result = _try_read_json(upstream_root / "controlled_trial_stop_condition_result_v1.json") or {}
    flow_dryrun = _try_read_json(upstream_root / "controlled_trial_candidate_flow_dryrun_v1.json") or {}
    runtime_audit = _try_read_json(upstream_root / "no_runtime_boundary_audit_v1.json") or {}

    upstream_verifier_trusted = upstream_vr.get("verifier") == "GO" and upstream_vr.get("passed") is True
    upstream_summary_trusted = (
        upstream_sm.get("boundary_ok") is True
        and upstream_sm.get("phase") == UPSTREAM_PHASE
        and upstream_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and upstream_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not upstream_verifier_trusted and not upstream_summary_trusted:
        blockers.append("plan+dryrun verifier must be GO")
    if upstream_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if (upstream_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")
    if upstream_sm.get("controlled_trial_started_now") is True:
        blockers.append("controlled_trial_started_now must be false")
    if upstream_sm.get("limited_runtime_trial_started_now") is True:
        blockers.append("limited_runtime_trial_started_now must be false")
    if gate_result.get("enforcement_pass") is not True:
        blockers.append("upstream 12 gates enforcement_pass required")
    if (gate_result.get("gates_passed") or 0) < 12:
        blockers.append("upstream gates_passed must be >= 12")
    if stop_result.get("verification_pass") is not True:
        blockers.append("upstream stop conditions verification_pass required")
    if (stop_result.get("conditions_passed") or 0) < 10:
        blockers.append("upstream stop conditions must be fully verified")
    if flow_dryrun.get("all_scenarios_pass") is not True:
        blockers.append("upstream fixture flows must all pass")
    if runtime_audit.get("audit_pass") is not True:
        blockers.append("upstream no_runtime_boundary_audit must pass")

    for field in RUNTIME_BOUNDARY_FIELDS:
        if upstream_sm.get(field) is True:
            blockers.append(f"upstream {field} must be false")

    ctx = {
        "upstream_sm": upstream_sm,
        "upstream_vr": upstream_vr,
        "gate_result": gate_result,
        "stop_result": stop_result,
        "flow_dryrun": flow_dryrun,
        "runtime_audit": runtime_audit,
        "upstream_verifier_trusted": upstream_verifier_trusted,
        "upstream_summary_trusted": upstream_summary_trusted,
    }
    return blockers, ctx


def run_vision_ocr_navigation_task_limited_runtime_trial_planning_v1(
    *,
    vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root: str,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    upstream_root = Path(
        vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root
    ).expanduser().resolve()

    plan_out = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else upstream_root.parent / "vision_ocr_navigation_task_limited_runtime_trial_planning"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(upstream_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_plan_and_dryrun_root": str(upstream_root),
        "planned_limited_runtime_output_root": str(plan_out),
        "workspace_fallback_trial_logging_only": True,
    }

    blockers, ctx = _validate_upstream(upstream_root)
    upstream_sm = ctx["upstream_sm"]
    upstream_vr = ctx["upstream_vr"]
    boundary_ok = len(blockers) == 0

    policy = {
        "policy_id": "limited_runtime_trial_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "extremely_limited_near_real_trial_design_only",
        "p0_chains": ["vision", "ocr", "navigation", "task_midplatform"],
        "no_live_runtime": True,
        **meta,
    }

    input_review = {
        "review_id": "controlled_trial_plan_and_dryrun_input_review_v1",
        "upstream_root": str(upstream_root),
        "upstream_verifier": upstream_vr.get("verifier"),
        "upstream_final_decision": upstream_sm.get("final_decision"),
        "upstream_high_risk_count": upstream_sm.get("high_risk_count"),
        "upstream_gates_passed": ctx["gate_result"].get("gates_passed"),
        "upstream_stop_conditions_passed": ctx["stop_result"].get("conditions_passed"),
        "upstream_scenarios_passed": ctx["flow_dryrun"].get("scenarios_passed"),
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    scope_matrix = {
        "matrix_id": "limited_runtime_scope_matrix_v1",
        "trial_label": "limited_runtime_trial_v1",
        "chains": ["vision", "ocr", "navigation", "task_midplatform"],
        "candidate_only": True,
        "max_execution_depth": "fixture_sample_mock_candidate_envelope",
        "live_runtime_allowed_in_planning": False,
        "limited_runtime_trial_started": False,
        **meta,
    }

    input_source_policy = {
        "policy_id": "limited_runtime_input_source_policy_v1",
        "allowed_sources": list(ALLOWED_INPUT_SOURCES),
        "forbidden_sources": list(FORBIDDEN_INPUT_SOURCES),
        "primary_upstream_artifacts": [
            str(upstream_root / "controlled_trial_fixture_input_matrix_v1.json"),
            str(upstream_root / "controlled_trial_candidate_flow_dryrun_v1.json"),
        ],
        "fixture_verification_required": True,
        **meta,
    }

    vision_plan = {
        "plan_id": "vision_limited_runtime_trial_plan_v1",
        "chain": "vision",
        "allowed": [
            "existing_sample_frame_reference",
            "controlled_fixture_frame",
            "pre_existing_frame_metadata",
        ],
        "forbidden": [
            "live_camera",
            "new_camera_capture",
            "arbitrary_image_read",
            "new_visual_model_inference",
        ],
        "output_candidate_type": "visual_observation_candidate",
        "fact_write_allowed": False,
        **meta,
    }

    ocr_plan = {
        "plan_id": "ocr_limited_runtime_trial_plan_v1",
        "chain": "ocr",
        "allowed": [
            "mock_ocr_provider",
            "fixture_ocr_response",
            "pre_existing_ocr_request_candidate",
        ],
        "forbidden": ["paddle_ocr", "rapidocr", "real_ocr_provider"],
        "output_candidate_type": "ocr_result_candidate",
        "provider_mode": "mock_or_fixture_only",
        "fact_write_allowed": False,
        "world_model_write_allowed": False,
        **meta,
    }

    navigation_plan = {
        "plan_id": "navigation_limited_runtime_trial_plan_v1",
        "chain": "navigation",
        "allowed": ["readonly_map_hint", "synthetic_route_context", "guidance_candidate"],
        "forbidden": [
            "real_navigation_action",
            "map_write",
            "gps_strong_anchor_commit",
        ],
        "output_candidate_type": "navigation_guidance_candidate",
        **meta,
    }

    task_plan = {
        "plan_id": "task_limited_runtime_trial_plan_v1",
        "chain": "task_midplatform",
        "allowed": [
            "task_state_candidate",
            "lifecycle_candidate",
            "task_response_candidate",
        ],
        "forbidden": [
            "commit_task_state",
            "task_manager_runtime_action",
            "tts",
            "llm",
        ],
        "output_candidate_types": [
            "task_state_candidate",
            "lifecycle_candidate",
            "task_response_candidate",
        ],
        "primary_output": "task_response_candidate",
        **meta,
    }

    gate_matrix = {
        "matrix_id": "limited_runtime_gate_matrix_v1",
        "gates": [
            {
                "gate_id": g,
                "status": "required_closed_in_planning",
                "enforcement": "block_live_runtime_fact_write_and_commit",
            }
            for g in LIMITED_RUNTIME_GATES
        ],
        "gates_total": len(LIMITED_RUNTIME_GATES),
        **meta,
    }

    stop_matrix = {
        "matrix_id": "limited_runtime_stop_condition_matrix_v1",
        "conditions": list(STOP_CONDITIONS),
        "immediate_stop_triggers": [c["trigger"] for c in STOP_CONDITIONS if c.get("action") == "stop"],
        "hold_triggers": [c["trigger"] for c in STOP_CONDITIONS if c.get("action") == "hold"],
        **meta,
    }

    logging_plan = {
        "plan_id": "limited_runtime_observation_logging_plan_v1",
        "allowed_write_root": str(plan_out),
        "allowed_artifact_types": [
            "limited_runtime_trial_trace",
            "gate_consumption_log",
            "mock_provider_envelope_snapshot",
            "fixture_input_verification_log",
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
        "logging_in_planning_phase": "plan_definition_only_no_limited_runtime_logs_yet",
        **meta,
    }

    dryrun_plan = {
        "plan_id": "limited_runtime_dryrun_plan_v1",
        "next_phase": NEXT_PHASE,
        "dryrun_goals": [
            "validate limited runtime trial plan with fixture/sample/mock input",
            "verify gates and stop conditions under mock envelopes",
            "no live runtime",
            "no real OCR provider",
            "no navigation action",
            "no task commit",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "limited_runtime_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "limited_runtime_trial_planning_readiness_decision_v1",
        "final_decision": (
            FINAL_DECISION
            if boundary_ok
            else "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_PLANNING_REQUIRES_FIXES"
        ),
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "limited_runtime_trial_started_now": False,
        "ready_for_limited_runtime_dryrun": boundary_ok,
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
        "limited_runtime_gates_count": len(LIMITED_RUNTIME_GATES),
        "limited_runtime_trial_started_now": False,
        "live_runtime_enabled_now": False,
        **meta,
    }

    return {
        "limited_runtime_trial_planning_policy": policy,
        "controlled_trial_plan_and_dryrun_input_review": input_review,
        "limited_runtime_scope_matrix": scope_matrix,
        "limited_runtime_input_source_policy": input_source_policy,
        "vision_limited_runtime_trial_plan": vision_plan,
        "ocr_limited_runtime_trial_plan": ocr_plan,
        "navigation_limited_runtime_trial_plan": navigation_plan,
        "task_limited_runtime_trial_plan": task_plan,
        "limited_runtime_gate_matrix": gate_matrix,
        "limited_runtime_stop_condition_matrix": stop_matrix,
        "limited_runtime_observation_logging_plan": logging_plan,
        "limited_runtime_dryrun_plan": dryrun_plan,
        "limited_runtime_non_claims_register": non_claims,
        "limited_runtime_trial_planning_readiness_decision": readiness,
        "summary": summary,
    }
