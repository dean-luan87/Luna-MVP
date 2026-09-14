# -*- coding: utf-8 -*-
"""Midplatform Speech / Display Gate Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_DR_FINAL_GO,
    NEXT_PHASE_GO as SAFETY_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    ENFORCEMENT_LAYER_POSITIONING,
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Speech-Display-Gate-Roadmap-Decision-v1-001"
SCOPE = "speech_display_gate_roadmap_decision_only"
SOURCE_CHAIN = "midplatform_speech_display_gate_roadmap_decision_v1"

UPSTREAM_SAFETY_DR_FINAL = SAFETY_DR_FINAL_GO
UPSTREAM_SAFETY_DR_NEXT = SAFETY_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_SPEECH_DISPLAY_GATE_ROADMAP_DECISION_READY_FOR_SPEECH_GATE_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_SPEECH_DISPLAY_GATE_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Speech-Gate-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Speech-Display-Gate-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Speech Gate First"
ROUTE_B = "Route B — Display Gate First"
ROUTE_C = "Route C — Parallel Speech + Display Gate"
ROUTE_D = "Route D — Direct Voice Output Plane"
ROUTE_E = "Route E — Direct Display Output"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTES: Tuple[str, ...] = (ROUTE_B, ROUTE_C)
BLOCKED_ROUTES: Tuple[str, ...] = (ROUTE_D, ROUTE_E)

LAYER_POSITION_CONFIRMATIONS: Tuple[str, ...] = (
    "Speech Gate = Enforcement Layer",
    "Display Gate = Enforcement Layer",
    "Notification Gate = Enforcement Layer later",
    "Voice Output Plane = Execution Layer",
    "Display Output = Execution Layer",
    "TTS runtime = Execution Layer",
    "Enforcement Layer consumes enforcement_result_candidate",
    "Execution Layer consumes enforcement_result_candidate + execution command later",
    "Execution Layer does not read raw constitution",
)

ENFORCEMENT_EXECUTION_BOUNDARY_RULES: Tuple[str, ...] = (
    "Safety Gate result ≠ speech_request",
    "Speech Gate pass ≠ TTS",
    "Display Gate pass ≠ UI render",
    "Enforcement result only grants path eligibility, not execution",
    "Voice Output Plane requires Speech Gate result later",
    "Display Output requires Display Gate result later",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "speech_gate_planning_started_now",
    "display_gate_planning_started_now",
    "voice_output_plane_planning_started_now",
    "display_output_planning_started_now",
    "speech_gate_runtime_enabled_now",
    "display_gate_runtime_enabled_now",
    "speech_request_generated_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "display_output_invoked_now",
    "user_facing_output_generated_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ Speech Gate planned",
    "Speech Gate selected ≠ speech_request generated",
    "Speech Gate selected ≠ TTS allowed",
    "Display Gate deferred ≠ Display Gate skipped",
    "Voice Output Plane blocked direct path ≠ voice output permanently blocked",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_speech_display_gate_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "speech_display_gate_roadmap_decision_only": True,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "selected_route": SELECTED_ROUTE,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_speech_display_gate_roadmap_decision_v1(
    *,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_planning_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    safety_plan_root = Path(midplatform_safety_gate_planning_root).expanduser().resolve()
    uo_dr_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()

    safety_dr_sm = _try_read_json(safety_dr_root / "summary.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    safety_plan_policy = _try_read_json(safety_plan_root / "safety_gate_planning_policy_v1.json") or {}
    closure = _try_read_json(safety_dr_root / "safety_gate_closure_decision_v1.json") or {}
    model = _try_read_json(safety_dr_root / "safety_gate_model_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_safety_gate_planning_root": str(safety_plan_root),
        "upstream_user_output_constitution_dryrun_root": str(uo_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "output_root": str(out_root),
    }

    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview verifier must be GO")
    if safety_dr_sm.get("final_decision") != UPSTREAM_SAFETY_DR_FINAL:
        blockers.append("safety gate dryrun final_decision mismatch")
    if safety_dr_sm.get("recommended_next_phase") != UPSTREAM_SAFETY_DR_NEXT:
        blockers.append("safety gate dryrun recommended_next_phase mismatch")
    if safety_plan_policy.get("safety_gate_is_enforcement_not_execution") is not True:
        blockers.append("Safety Gate must be Enforcement Layer not Execution Layer")
    if model.get("emits_enforcement_result_candidate") is not True:
        blockers.append("Safety Gate must emit enforcement_result_candidate")
    if closure.get("enforcement_layer_validated") is not True:
        blockers.append("enforcement layer must be validated in safety dryrun")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "safety_gate_dryrun_input_review_v1",
        "safety_gate_dryrun_verifier": safety_dr_vr.get("verifier"),
        "safety_gate_dryrun_final": safety_dr_sm.get("final_decision"),
        "enforcement_layer_validated": closure.get("enforcement_layer_validated") is True,
        "emits_enforcement_result_candidate": model.get("emits_enforcement_result_candidate") is True,
        "execution_consumes_enforcement_not_constitution": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    layer_review = {
        "review_id": "speech_display_gate_layer_position_review_v1",
        "confirmations": list(LAYER_POSITION_CONFIRMATIONS),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        "enforcement_layer_positioning": list(ENFORCEMENT_LAYER_POSITIONING),
        "review_pass": True,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_speech_gate_first_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "Luna Badge / first-person interaction output priority favors speech",
            "speech output risk higher: ambiguity, urgency, interruption, tone, timing",
            "Speech Gate must constrain speech_request / TTS / Voice Output Plane first",
            "establishing speech enforcement gate helps Voice Output Plane integration later",
            "Display Gate can defer",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_display_gate_first_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred",
        "defer_reasons": [
            "Display output important but Luna Badge main chain favors speech now",
            "Display Output still required but not current priority",
            "Display Gate can reuse enforcement pattern after Speech Gate validation",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_parallel_speech_display_gate_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "parallel approach expands engineering surface",
            "maintain convergence now",
            "use Speech Gate as enforcement gate exemplar first, then reuse for Display Gate",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_voice_output_plane_direct_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "blocked",
        "block_reasons": [
            "Voice Output Plane is execution layer; cannot bypass Speech Gate",
            "cannot go from Safety Gate directly to TTS/Voice runtime",
            "speech enforcement gate must be established first",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_display_output_direct_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "blocked",
        "block_reasons": [
            "Display Output is execution layer; cannot bypass Display Gate",
            "cannot directly UI render / notification / app push",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "speech_display_gate_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "blocked"},
            {"route": ROUTE_E, "status": "blocked"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_routes": list(DEFERRED_ROUTES),
        "blocked_routes": list(BLOCKED_ROUTES),
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "Safety Gate DryRunAndReview GO",
            "enforcement_result_candidate validated",
            "Speech Gate planning only next — no runtime",
            "Speech Gate is Enforcement Layer not Execution Layer",
            "Voice Output Plane remains blocked until Speech Gate established",
            "Display Gate deferred not skipped",
        ],
        "forbidden_now": [
            "speech_request generation",
            "TTS invocation",
            "Voice Output Plane planning/invocation",
            "Display Output execution",
            "Display Gate planning start (deferred)",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_routes": [
            {"route": ROUTE_B, "status": "deferred", "note": "Display Gate after Speech Gate exemplar"},
            {"route": ROUTE_C, "status": "deferred", "note": "parallel deferred for convergence"},
        ],
        "blocked_routes": [
            {"route": ROUTE_D, "status": "blocked", "note": "execution layer bypass forbidden"},
            {"route": ROUTE_E, "status": "blocked", "note": "execution layer bypass forbidden"},
        ],
        **meta,
    }

    boundary_review = {
        "review_id": "enforcement_execution_layer_boundary_review_v1",
        "rules": list(ENFORCEMENT_EXECUTION_BOUNDARY_RULES),
        "enforcement_result_grants_eligibility_not_execution": True,
        "review_pass": True,
        **meta,
    }

    decision_ok = input_ok
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_speech_gate_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_skip_to_voice_output_plane": True,
        "display_gate_deferred_not_skipped": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "speech_display_gate_roadmap_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_decision_not_planning": True,
        "speech_gate_first_selected": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": next_readiness["final_decision"],
        "recommended_next_phase": next_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "deferred_routes": list(DEFERRED_ROUTES),
        "blocked_routes": list(BLOCKED_ROUTES),
        **meta,
    }

    return {
        "speech_display_gate_roadmap_policy": policy,
        "safety_gate_dryrun_input_review": input_review,
        "speech_display_gate_layer_position_review": layer_review,
        "route_a_speech_gate_first_assessment": route_a,
        "route_b_display_gate_first_assessment": route_b,
        "route_c_parallel_speech_display_gate_assessment": route_c,
        "route_d_voice_output_plane_direct_assessment": route_d,
        "route_e_display_output_direct_assessment": route_e,
        "speech_display_gate_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "enforcement_execution_layer_boundary_review": boundary_review,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
