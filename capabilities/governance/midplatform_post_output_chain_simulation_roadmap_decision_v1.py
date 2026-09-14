# -*- coding: utf-8 -*-
"""Midplatform Post-Output-Chain-Simulation Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
    NEXT_PHASE_GO as E2E_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Post-Output-Chain-Simulation-Roadmap-Decision-v1-001"
SCOPE = "post_output_chain_simulation_roadmap_decision_only"
SOURCE_CHAIN = "midplatform_post_output_chain_simulation_roadmap_decision_v1"

UPSTREAM_E2E_DR_FINAL = E2E_DR_FINAL_GO
UPSTREAM_E2E_DR_NEXT = E2E_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_POST_OUTPUT_CHAIN_SIMULATION_ROADMAP_DECISION_READY_FOR_"
    "PROVIDER_ABSTRACTION_STANDARD_ALIGNMENT_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_POST_OUTPUT_CHAIN_SIMULATION_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Provider-Abstraction-Standard-Alignment-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Post-Output-Chain-Simulation-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Provider Abstraction Standard Alignment"
ROUTE_B = "Route B — Display Gate Planning"
ROUTE_C = "Route C — Controlled Runtime Planning"
ROUTE_D = "Route D — Direct Real TTS / Audio Runtime"
ROUTE_E = "Route E — Health Enforcement Supervisor Planning"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTES: Tuple[str, ...] = (ROUTE_B, ROUTE_C, ROUTE_E)
BLOCKED_ROUTES: Tuple[str, ...] = (ROUTE_D,)

SYSTEM_LEVEL_GO_NONCLAIMS: Tuple[str, ...] = (
    "system-level simulated GO ≠ production ready",
    "system-level simulated GO ≠ runtime enabled",
    "audio_artifact_candidate ≠ audio generated",
    "qianwen_tts_candidate ≠ provider selected",
    "Display Gate deferred ≠ skipped",
    "Provider Abstraction Alignment selected ≠ historical verdict rewritten",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ provider abstraction applied",
    "selected alignment route ≠ runtime enabled",
    "Display Gate deferred ≠ skipped",
    "controlled runtime deferred ≠ cancelled",
    "direct real TTS blocked ≠ TTS permanently blocked",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("post_output_chain_simulation_roadmap_decision_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "provider_abstraction_alignment_started_now",
    "display_gate_planning_started_now",
    "controlled_runtime_planning_started_now",
    "real_runtime_enabled_now",
    "tts_runtime_invoked_now",
    "qianwen_tts_invoked_now",
    "provider_invoked_now",
    "audio_synthesis_invoked_now",
    "audio_output_generated_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_post_output_chain_simulation_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "selected_route": SELECTED_ROUTE,
        "display_gate_deferred_not_skipped": True,
        "system_level_simulated_go": True,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_post_output_chain_simulation_roadmap_decision_v1(
    *,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    e2e_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    tts_dr_root = Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve()
    voice_dr_root = Path(midplatform_voice_output_plane_dryrun_and_review_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    uo_const_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()

    e2e_sm = _try_read_json(e2e_root / "summary.json") or {}
    e2e_vr = _try_read_json(e2e_root / "verifier_report.json") or {}
    exp_actual = _try_read_json(e2e_root / "expected_vs_actual_decision_matrix_v1.json") or {}
    boundary_v = _try_read_json(e2e_root / "boundary_violation_matrix_v1.json") or {}
    trace = _try_read_json(e2e_root / "traceability_matrix_v1.json") or {}
    closure_review = _try_read_json(e2e_root / "system_level_chain_closure_review_v1.json") or {}
    tts_model = _try_read_json(tts_dr_root / "tts_runtime_model_candidate_v1.json") or {}
    tts_dr_sm = _try_read_json(tts_dr_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_e2e_simulation_dryrun_root": str(e2e_root),
        "upstream_tts_runtime_dryrun_root": str(tts_dr_root),
        "upstream_voice_output_plane_dryrun_root": str(voice_dr_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_user_output_constitution_dryrun_root": str(uo_const_root),
        "output_root": str(out_root),
    }

    if e2e_vr.get("verifier") != "GO":
        blockers.append("End-to-End Simulation DryRunAndReview verifier must be GO")
    if e2e_sm.get("final_decision") != UPSTREAM_E2E_DR_FINAL:
        blockers.append("e2e dryrun final_decision mismatch")
    if e2e_sm.get("recommended_next_phase") != UPSTREAM_E2E_DR_NEXT:
        blockers.append("e2e dryrun recommended_next_phase mismatch")
    if e2e_sm.get("cases_passed") != 8:
        blockers.append("cases_passed must be 8/8")
    if e2e_sm.get("case_count") != 8:
        blockers.append("case_count must be 8")
    if exp_actual.get("all_match") is not True:
        blockers.append("expected_vs_actual_decision_matrix must pass")
    if boundary_v.get("all_boundaries_clear") is not True:
        blockers.append("boundary_violation_matrix must pass")
    if trace.get("all_preserved") is not True:
        blockers.append("traceability_matrix must pass")
    if closure_review.get("no_runtime_leakage") is not True:
        blockers.append("no runtime leakage must be confirmed")
    if tts_model.get("runtime_abstraction") is not True:
        blockers.append("TTS Runtime must remain abstract runtime")
    if tts_model.get("current_preferred_provider_candidate") != CURRENT_PREFERRED_PROVIDER_CANDIDATE:
        blockers.append("qianwen_tts_candidate must be registered")
    if tts_model.get("provider_selected_for_execution_now") is not False:
        blockers.append("provider must not be selected for execution")
    if e2e_sm.get("qianwen_tts_invoked_now") is not False:
        blockers.append("qianwen must not be invoked")
    if meta.get("display_gate_deferred_not_skipped") is not True:
        blockers.append("Display Gate must remain deferred not skipped")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "system_level_simulation_input_review_v1",
        "e2e_dryrun_verifier": e2e_vr.get("verifier"),
        "e2e_dryrun_final_decision": e2e_sm.get("final_decision"),
        "cases_passed": e2e_sm.get("cases_passed"),
        "case_count": e2e_sm.get("case_count"),
        "expected_vs_actual_pass": exp_actual.get("all_match") is True,
        "boundary_violation_pass": boundary_v.get("all_boundaries_clear") is True,
        "traceability_pass": trace.get("all_preserved") is True,
        "no_runtime_leakage": closure_review.get("no_runtime_leakage") is True,
        "tts_runtime_abstraction": tts_model.get("runtime_abstraction") is True,
        "qianwen_registered_not_invoked": (
            tts_model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
            and e2e_sm.get("qianwen_tts_invoked_now") is False
            and tts_dr_sm.get("qianwen_tts_invoked_now") is False
        ),
        "display_gate_deferred_not_skipped": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_provider_abstraction_alignment_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "TTS Runtime corrected to abstract runtime + qianwen_tts_candidate",
            "OCR / Vision / Voice / Map / Library / Hive / Memory provider modules need unified abstraction",
            "PaddleOCR / Qianwen / SenseVoice / Map SDK must not be mistaken as runtime core",
            "horizontal alignment avoids provider switch rewriting midplatform core",
            "no historical verdict rewrite — standard absorption and future enforcement only",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_display_gate_planning_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_next",
        "defer_reasons": [
            "Display Gate still needs to be added",
            "Display Gate is Enforcement Layer, not Display Output execution",
            "voice main chain simulation GO but display cannot remain permanently absent",
            "recommended after Provider Abstraction Standard Alignment",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_controlled_runtime_planning_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred_after_alignment_and_display_gate",
        "defer_reasons": [
            "system-level simulated GO does not equal real runtime allowed",
            "real TTS / audio / display require provider abstraction, Display Gate, runtime authorization",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_direct_real_tts_audio_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "blocked",
        "block_reasons": [
            "system-level simulated GO ≠ real TTS allowed",
            "qianwen_tts_candidate registered ≠ selected/invoked",
            "audio_artifact_candidate ≠ audio output",
            "cannot bypass runtime authorization / provider readiness / post-execution review",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_health_enforcement_supervisor_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "deferred_but_registered",
        "defer_reasons": [
            "Health Management Layer needs Enforcement Layer Health Supervisor",
            "supervisor monitors Safety / Speech / Display / Authorization / Validation Factory compliance",
            "current mainline priority is provider abstraction and Display Gate",
            "must be planned separately later — not lost",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "post_simulation_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_next"},
            {"route": ROUTE_C, "status": "deferred_after_alignment_and_display_gate"},
            {"route": ROUTE_D, "status": "blocked"},
            {"route": ROUTE_E, "status": "deferred_but_registered"},
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
            "End-to-End Output Chain Simulation DryRunAndReview GO",
            "system-level simulated GO confirmed (8/8 cases)",
            "Provider Abstraction Standard Alignment planning only next",
            "no historical verdict rewrite",
            "no real runtime / TTS / audio / display",
            "Display Gate deferred not skipped",
            "Controlled Runtime deferred after alignment and Display Gate",
        ],
        "forbidden_now": [
            "real TTS / audio runtime",
            "provider import / invocation",
            "Display Gate planning start (deferred_next after alignment)",
            "controlled runtime planning start",
            "Memory / WorldModel write",
            "task_state commit",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_routes": [
            {"route": ROUTE_B, "status": "deferred_next", "note": "Display Gate Planning after alignment"},
            {
                "route": ROUTE_C,
                "status": "deferred_after_alignment_and_display_gate",
                "note": "Controlled Runtime Planning after alignment + Display Gate",
            },
            {
                "route": ROUTE_E,
                "status": "deferred_but_registered",
                "note": "Health Enforcement Supervisor Planning registered for later",
            },
        ],
        **meta,
    }

    blocked_register = {
        "register_id": "blocked_routes_register_v1",
        "blocked_routes": [
            {
                "route": ROUTE_D,
                "status": "blocked",
                "note": "Direct Real TTS / Audio Runtime forbidden — requires authorization chain",
            },
        ],
        **meta,
    }

    nonclaims_review = {
        "review_id": "system_level_go_nonclaims_review_v1",
        "non_claims": list(SYSTEM_LEVEL_GO_NONCLAIMS),
        "review_pass": True,
        **meta,
    }

    decision_ok = input_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_provider_abstraction_standard_alignment_planning": decision_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_open_real_runtime_now": True,
        "display_gate_deferred_not_skipped": True,
        "controlled_runtime_deferred_not_cancelled": True,
        "direct_real_tts_blocked": True,
        "recommended_next_phase": NEXT_PHASE_GO if decision_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if decision_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "post_output_chain_simulation_roadmap_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_decision_not_runtime": True,
        "provider_abstraction_alignment_selected": True,
        "system_level_simulated_go_acknowledged": True,
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
        "boundary_ok": decision_ok,
        "violations": blockers,
        "final_decision": next_readiness["final_decision"],
        "recommended_next_phase": next_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "deferred_routes": list(DEFERRED_ROUTES),
        "blocked_routes": list(BLOCKED_ROUTES),
        **meta,
    }

    return {
        "post_output_chain_simulation_roadmap_policy": policy,
        "system_level_simulation_input_review": input_review,
        "route_a_provider_abstraction_alignment_assessment": route_a,
        "route_b_display_gate_planning_assessment": route_b,
        "route_c_controlled_runtime_planning_assessment": route_c,
        "route_d_direct_real_tts_audio_assessment": route_d,
        "route_e_health_enforcement_supervisor_assessment": route_e,
        "post_simulation_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "blocked_routes_register": blocked_register,
        "system_level_go_nonclaims_review": nonclaims_review,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
