# -*- coding: utf-8 -*-
"""Midplatform Voice Output Plane Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_DR_FINAL_GO,
    NEXT_PHASE_GO as SPEECH_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    SPEECH_GATE_LAYER_POSITIONING,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Voice-Output-Plane-Roadmap-Decision-v1-001"
SCOPE = "voice_output_plane_roadmap_decision_only"
SOURCE_CHAIN = "midplatform_voice_output_plane_roadmap_decision_v1"

UPSTREAM_SPEECH_DR_FINAL = SPEECH_DR_FINAL_GO
UPSTREAM_SPEECH_DR_NEXT = SPEECH_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_VOICE_OUTPUT_PLANE_ROADMAP_DECISION_READY_FOR_VOICE_OUTPUT_PLANE_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_VOICE_OUTPUT_PLANE_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Voice-Output-Plane-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Voice-Output-Plane-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Voice Output Plane Planning"
ROUTE_B = "Route B — Display Gate First"
ROUTE_C = "Route C — Voice + Display Parallel"
ROUTE_D = "Route D — Direct TTS Runtime"
ROUTE_E = "Route E — Return to Output Constitution"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTES: Tuple[str, ...] = (ROUTE_B, ROUTE_C, ROUTE_E)
BLOCKED_ROUTES: Tuple[str, ...] = (ROUTE_D,)

LAYER_READINESS_CONFIRMATIONS: Tuple[str, ...] = (
    "Speech Gate = Enforcement Layer",
    "Voice Output Plane = Execution Layer",
    "TTS runtime = Execution Layer",
    "speech_gate_result_candidate is enforcement result",
    "Voice Output Plane consumes speech_gate_result_candidate later",
    "Execution Layer does not read raw constitution",
    "Speech Gate pass ≠ speech_request / TTS / audio output",
    "Display Gate deferred, not skipped",
)

ENFORCEMENT_TO_EXECUTION_BOUNDARY_RULES: Tuple[str, ...] = (
    "speech_gate_result_candidate is enforcement result",
    "Voice Output Plane is execution layer",
    "Voice Output Plane consumes speech_gate_result_candidate later",
    "Voice Output Plane does not read raw constitution",
    "Voice Output Plane cannot override Speech Gate result",
    "TTS runtime cannot be invoked before Voice Output Plane authorization",
    "speech_request is not generated in roadmap phase",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "voice_output_plane_planning_started_now",
    "display_gate_planning_started_now",
    "speech_request_generated_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "audio_output_generated_now",
    "user_facing_output_generated_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ Voice Output Plane planned",
    "Voice Output Plane selected ≠ TTS allowed",
    "Voice Output Plane selected ≠ audio output generated",
    "Speech Gate result ≠ speech_request",
    "Display Gate deferred ≠ skipped",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "voice_output_plane_roadmap_decision_only": True,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "selected_route": SELECTED_ROUTE,
        "display_gate_deferred_not_skipped": True,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_voice_output_plane_roadmap_decision_v1(
    *,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_planning_root: str,
    midplatform_speech_display_gate_roadmap_decision_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    speech_plan_root = Path(midplatform_speech_gate_planning_root).expanduser().resolve()
    roadmap_root = Path(midplatform_speech_display_gate_roadmap_decision_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()

    speech_dr_sm = _try_read_json(speech_dr_root / "summary.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    speech_plan_policy = _try_read_json(speech_plan_root / "speech_gate_planning_policy_v1.json") or {}
    closure = _try_read_json(speech_dr_root / "speech_gate_closure_decision_v1.json") or {}
    model = _try_read_json(speech_dr_root / "speech_gate_model_candidate_v1.json") or {}
    sample_result = _try_read_json(speech_dr_root / "sample_speech_gate_result_candidate_v1.json") or {}
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_next = _try_read_json(roadmap_root / "next_phase_readiness_decision_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_speech_gate_planning_root": str(speech_plan_root),
        "upstream_speech_display_roadmap_root": str(roadmap_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "output_root": str(out_root),
    }

    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview verifier must be GO")
    if speech_dr_sm.get("final_decision") != UPSTREAM_SPEECH_DR_FINAL:
        blockers.append("speech gate dryrun final_decision mismatch")
    if speech_dr_sm.get("recommended_next_phase") != UPSTREAM_SPEECH_DR_NEXT:
        blockers.append("speech gate dryrun recommended_next_phase mismatch")
    if closure.get("speech_enforcement_layer_validated") is not True:
        blockers.append("speech_enforcement_layer_validated must be true")
    if speech_plan_policy.get("speech_gate_is_enforcement_not_execution") is not True:
        blockers.append("Speech Gate must be Enforcement Layer not Execution Layer")
    if model.get("emits_speech_gate_result_candidate") is not True:
        blockers.append("Speech Gate must emit speech_gate_result_candidate")
    if model.get("generates_speech_request") is not False:
        blockers.append("Speech Gate must not generate speech_request")
    if model.get("invokes_tts") is not False:
        blockers.append("Speech Gate must not invoke TTS")
    if not sample_result.get("speech_gate_result_candidate_id"):
        blockers.append("sample speech_gate_result_candidate must exist")
    if sample_result.get("speech_request_allowed") is not False:
        blockers.append("speech_gate_result speech_request_allowed must be false")
    display_deferred = (
        roadmap_next.get("display_gate_deferred_not_skipped") is True
        or "Route B — Display Gate First" in (roadmap_sm.get("deferred_routes") or [])
    )
    if not display_deferred:
        blockers.append("Display Gate must be deferred not skipped")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "speech_gate_dryrun_input_review_v1",
        "speech_gate_dryrun_verifier": speech_dr_vr.get("verifier"),
        "speech_gate_dryrun_final": speech_dr_sm.get("final_decision"),
        "speech_enforcement_layer_validated": closure.get("speech_enforcement_layer_validated") is True,
        "emits_speech_gate_result_candidate": model.get("emits_speech_gate_result_candidate") is True,
        "speech_pass_not_speech_request_or_tts": True,
        "display_gate_deferred_not_skipped": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    readiness_review = {
        "review_id": "enforcement_execution_layer_readiness_review_v1",
        "confirmations": list(LAYER_READINESS_CONFIRMATIONS),
        "speech_gate_layer_positioning": list(SPEECH_GATE_LAYER_POSITIONING),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        "review_pass": True,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_voice_output_plane_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "Speech Gate completed Planning + DryRunAndReview",
            "speech enforcement layer outputs speech_gate_result_candidate",
            "Luna Badge / first-person interaction favors speech output priority",
            "next step defines how execution layer consumes speech_gate_result_candidate",
            "planning only — no TTS / audio runtime",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_display_gate_first_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred",
        "defer_reasons": [
            "Display Gate still required",
            "main chain prioritizes speech now",
            "Display Gate can follow Voice Output Plane planning",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_voice_and_display_parallel_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "parallel approach expands engineering surface",
            "maintain single-line convergence now",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_direct_tts_runtime_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "blocked",
        "block_reasons": [
            "TTS is execution runtime",
            "cannot bypass Voice Output Plane Planning",
            "cannot trigger TTS directly from Speech Gate",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_return_to_output_constitution_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "deferred",
        "defer_reasons": [
            "User Output Constitution DryRunAndReview already completed",
            "no need to roll back at this stage",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "voice_output_plane_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "blocked"},
            {"route": ROUTE_E, "status": "deferred"},
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
            "Speech Gate DryRunAndReview GO",
            "speech_gate_result_candidate validated",
            "Voice Output Plane planning only next — no runtime",
            "Voice Output Plane is Execution Layer not Enforcement",
            "consumes speech_gate_result_candidate only",
            "Display Gate deferred not skipped",
        ],
        "forbidden_now": [
            "speech_request generation",
            "TTS invocation",
            "Voice Output Plane runtime invocation",
            "audio output generation",
            "Display Gate planning start (deferred)",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_routes": [
            {"route": ROUTE_B, "status": "deferred", "note": "Display Gate after Voice Output Plane planning"},
            {"route": ROUTE_C, "status": "deferred", "note": "parallel deferred for convergence"},
            {"route": ROUTE_E, "status": "deferred", "note": "constitution rollback not needed"},
        ],
        "blocked_routes": [
            {"route": ROUTE_D, "status": "blocked", "note": "direct TTS runtime bypass forbidden"},
        ],
        **meta,
    }

    boundary_review = {
        "review_id": "enforcement_to_execution_boundary_review_v1",
        "rules": list(ENFORCEMENT_TO_EXECUTION_BOUNDARY_RULES),
        "speech_gate_result_is_enforcement_not_execution": True,
        "review_pass": True,
        **meta,
    }

    decision_ok = input_ok
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_voice_output_plane_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_skip_to_tts_runtime": True,
        "display_gate_deferred_not_skipped": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "voice_output_plane_roadmap_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_decision_not_planning": True,
        "voice_output_plane_planning_selected": True,
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
        "voice_output_plane_roadmap_policy": policy,
        "speech_gate_dryrun_input_review": input_review,
        "enforcement_execution_layer_readiness_review": readiness_review,
        "route_a_voice_output_plane_planning_assessment": route_a,
        "route_b_display_gate_first_assessment": route_b,
        "route_c_voice_and_display_parallel_assessment": route_c,
        "route_d_direct_tts_runtime_assessment": route_d,
        "route_e_return_to_output_constitution_assessment": route_e,
        "voice_output_plane_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "enforcement_to_execution_boundary_review": boundary_review,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
