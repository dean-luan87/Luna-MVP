# -*- coding: utf-8 -*-
"""Midplatform TTS Runtime Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL_GO,
    NEXT_PHASE_GO as VOICE_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    VOICE_OUTPUT_PLANE_LAYER_POSITIONING,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-TTS-Runtime-Roadmap-Decision-v1-001"
SCOPE = "tts_runtime_roadmap_decision_only"
SOURCE_CHAIN = "midplatform_tts_runtime_roadmap_decision_v1"

UPSTREAM_VOICE_DR_FINAL = VOICE_DR_FINAL_GO
UPSTREAM_VOICE_DR_NEXT = VOICE_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_TTS_RUNTIME_ROADMAP_DECISION_READY_FOR_TTS_RUNTIME_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_TTS_RUNTIME_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-TTS-Runtime-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-TTS-Runtime-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — TTS Runtime Planning"
ROUTE_B = "Route B — Hold at Speech Request Candidate"
ROUTE_C = "Route C — Return to Display Gate"
ROUTE_D = "Route D — Direct TTS Execution"
ROUTE_E = "Route E — End-to-End Simulation Before TTS"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTES: Tuple[str, ...] = (ROUTE_B, ROUTE_C, ROUTE_E)
BLOCKED_ROUTES: Tuple[str, ...] = (ROUTE_D,)

LAYER_POSITION_CONFIRMATIONS: Tuple[str, ...] = (
    "Voice Output Plane = Execution Layer",
    "TTS Runtime = lower execution runtime",
    "speech_request_candidate is not real speech_request",
    "TTS Runtime requires planning / authorization / provider readiness",
    "Speech Gate enforcement chain not bypassed",
    "Display Gate deferred, not skipped",
    "End-to-End Simulation remains future route",
)

EXECUTION_RUNTIME_BOUNDARY_RULES: Tuple[str, ...] = (
    "speech_request_candidate is not real speech_request",
    "TTS Runtime is lower execution runtime",
    "TTS Runtime cannot start without planning / authorization / provider readiness",
    "TTS provider/model cannot be imported now",
    "audio synthesis cannot be invoked now",
    "audio playback cannot start now",
    "Display Gate deferred is not skipped",
    "End-to-End Simulation remains future route",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "tts_runtime_planning_started_now",
    "tts_runtime_enabled_now",
    "tts_provider_selected_now",
    "tts_provider_imported_now",
    "voice_model_selected_now",
    "speech_request_submitted_now",
    "audio_synthesis_invoked_now",
    "audio_output_generated_now",
    "audio_playback_started_now",
    "voice_output_plane_invoked_now",
    "display_gate_planning_started_now",
    "display_output_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ TTS runtime enabled",
    "TTS Runtime Planning selected ≠ provider selected",
    "TTS Runtime Planning selected ≠ audio synthesis allowed",
    "speech_request_candidate ≠ real speech_request",
    "Display Gate deferred ≠ skipped",
    "End-to-End Simulation deferred ≠ cancelled",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "tts_runtime_roadmap_decision_only": True,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "selected_route": SELECTED_ROUTE,
        "display_gate_deferred_not_skipped": True,
        "end_to_end_simulation_deferred_not_cancelled": True,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_tts_runtime_roadmap_decision_v1(
    *,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_voice_output_plane_planning_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    voice_dr_root = Path(midplatform_voice_output_plane_dryrun_and_review_root).expanduser().resolve()
    voice_plan_root = Path(midplatform_voice_output_plane_planning_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()

    voice_dr_sm = _try_read_json(voice_dr_root / "summary.json") or {}
    voice_dr_vr = _try_read_json(voice_dr_root / "verifier_report.json") or {}
    closure = _try_read_json(voice_dr_root / "voice_output_plane_closure_decision_v1.json") or {}
    model = _try_read_json(voice_dr_root / "voice_output_plane_model_candidate_v1.json") or {}
    sample_request = _try_read_json(voice_dr_root / "sample_speech_request_candidate_v1.json") or {}
    blocked_result = _try_read_json(voice_dr_root / "voice_output_plane_blocked_path_result_v1.json") or {}
    voice_plan_policy = _try_read_json(voice_plan_root / "voice_output_plane_planning_policy_v1.json") or {}
    speech_closure = _try_read_json(speech_dr_root / "speech_gate_closure_decision_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_voice_output_plane_dryrun_root": str(voice_dr_root),
        "upstream_voice_output_plane_planning_root": str(voice_plan_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "output_root": str(out_root),
    }

    if voice_dr_vr.get("verifier") != "GO":
        blockers.append("Voice Output Plane DryRunAndReview verifier must be GO")
    if voice_dr_sm.get("final_decision") != UPSTREAM_VOICE_DR_FINAL:
        blockers.append("voice output plane dryrun final_decision mismatch")
    if voice_dr_sm.get("recommended_next_phase") != UPSTREAM_VOICE_DR_NEXT:
        blockers.append("voice output plane dryrun recommended_next_phase mismatch")
    if closure.get("execution_layer_validated") is not True:
        blockers.append("execution_layer_validated must be true")
    if voice_plan_policy.get("voice_output_plane_is_execution_not_enforcement") is not True:
        blockers.append("Voice Output Plane must be execution layer")
    if model.get("bypasses_speech_gate") is not False:
        blockers.append("Voice Output Plane must not bypass Speech Gate")
    if not sample_request.get("speech_request_candidate_id"):
        blockers.append("sample speech_request_candidate must exist")
    if sample_request.get("candidate_only") is not True:
        blockers.append("speech_request_candidate must be candidate_only")
    if sample_request.get("tts_runtime_allowed") is not False:
        blockers.append("speech_request_candidate tts_runtime_allowed must be false")
    if speech_closure.get("speech_enforcement_layer_validated") is not True:
        blockers.append("speech enforcement layer must be validated")

    tts_blocked = any(
        x.get("blocked_path") == "dryrun_to_tts_invocation" and x.get("blocked") is True
        for x in (blocked_result.get("blocked_paths") or [])
    )
    if not tts_blocked:
        blockers.append("direct TTS runtime must remain blocked in upstream dryrun")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "voice_output_plane_dryrun_input_review_v1",
        "voice_output_plane_dryrun_verifier": voice_dr_vr.get("verifier"),
        "voice_output_plane_dryrun_final": voice_dr_sm.get("final_decision"),
        "execution_layer_validated": closure.get("execution_layer_validated") is True,
        "speech_request_candidate_exists": bool(sample_request.get("speech_request_candidate_id")),
        "speech_request_not_real": meta.get("speech_request_submitted_now") is False,
        "speech_request_not_tts": sample_request.get("tts_runtime_allowed") is False,
        "speech_gate_not_bypassed": model.get("bypasses_speech_gate") is False,
        "direct_tts_not_opened": tts_blocked,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    layer_review = {
        "review_id": "tts_runtime_layer_position_review_v1",
        "confirmations": list(LAYER_POSITION_CONFIRMATIONS),
        "voice_output_plane_layer_positioning": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        "review_pass": True,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_tts_runtime_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "Voice Output Plane completed Planning + DryRunAndReview",
            "speech_request_candidate layer closed",
            "next step defines TTS runtime boundaries, provider admission, model selection, audio generation/playback, failure routes",
            "planning only — no TTS runtime, no audio synthesis",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_hold_at_speech_request_candidate_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred",
        "defer_reasons": [
            "can serve as end-to-end simulation seal point",
            "TTS Runtime Planning helps clarify real voice execution boundaries",
            "not selected as primary route now",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_return_to_display_gate_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "Display Gate still needs to be added",
            "speech main chain advanced to Voice Output Plane",
            "Display Gate not skipped — to be added separately later",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_direct_tts_execution_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "blocked",
        "block_reasons": [
            "TTS is real runtime",
            "cannot bypass TTS Runtime Planning / authorization / provider readiness",
            "cannot directly import provider, synthesize audio, or play back",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_end_to_end_simulation_before_tts_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "deferred_after_tts_runtime_planning",
        "defer_reasons": [
            "end-to-end simulation requested for later",
            "complete TTS Runtime Planning first for fuller chain boundaries",
            "simulation must not open real TTS/audio",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "tts_runtime_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "blocked"},
            {"route": ROUTE_E, "status": "deferred_after_tts_runtime_planning"},
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
            "Voice Output Plane DryRunAndReview GO",
            "speech_request_candidate validated",
            "TTS Runtime planning only next — no runtime",
            "no provider import / voice model selection / audio synthesis",
            "Display Gate deferred not skipped",
            "End-to-End Simulation deferred after TTS Runtime Planning",
        ],
        "forbidden_now": [
            "TTS provider import",
            "voice model selection",
            "audio synthesis",
            "audio playback",
            "real speech_request submission",
            "Display Gate planning start (deferred)",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_routes": [
            {"route": ROUTE_B, "status": "deferred", "note": "hold at speech_request_candidate for simulation seal"},
            {"route": ROUTE_C, "status": "deferred", "note": "Display Gate to be added later"},
            {
                "route": ROUTE_E,
                "status": "deferred_after_tts_runtime_planning",
                "note": "end-to-end simulation after TTS Runtime Planning",
            },
        ],
        "blocked_routes": [
            {"route": ROUTE_D, "status": "blocked", "note": "direct TTS execution forbidden"},
        ],
        **meta,
    }

    boundary_review = {
        "review_id": "execution_runtime_boundary_review_v1",
        "rules": list(EXECUTION_RUNTIME_BOUNDARY_RULES),
        "tts_runtime_requires_planning_first": True,
        "review_pass": True,
        **meta,
    }

    decision_ok = input_ok
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_tts_runtime_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_open_tts_runtime_now": True,
        "display_gate_deferred_not_skipped": True,
        "end_to_end_simulation_deferred_not_cancelled": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "tts_runtime_roadmap_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_decision_not_planning": True,
        "tts_runtime_planning_selected": True,
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
        "tts_runtime_roadmap_policy": policy,
        "voice_output_plane_dryrun_input_review": input_review,
        "tts_runtime_layer_position_review": layer_review,
        "route_a_tts_runtime_planning_assessment": route_a,
        "route_b_hold_at_speech_request_candidate_assessment": route_b,
        "route_c_return_to_display_gate_assessment": route_c,
        "route_d_direct_tts_execution_assessment": route_d,
        "route_e_end_to_end_simulation_before_tts_assessment": route_e,
        "tts_runtime_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "execution_runtime_boundary_review": boundary_review,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
