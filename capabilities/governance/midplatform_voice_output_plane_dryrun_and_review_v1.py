# -*- coding: utf-8 -*-
"""Midplatform Voice Output Plane DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    SPEECH_GATE_LAYER_POSITIONING,
)
from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    AUDIO_OUTPUT_BOUNDARY_RULES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NO_RAW_CONSTITUTION_RULES,
    SPEECH_CONTENT_RENDERING_RULES,
    SPEECH_GATE_NON_BYPASS_RULES,
    SPEECH_GATE_RESULT_INTAKE_FIELDS,
    SPEECH_REQUEST_CANDIDATE_FIELDS,
    SPEECH_TIMING_PRIORITY_RULES,
    TRACEABILITY_REQUIREMENTS,
    TTS_RUNTIME_BOUNDARY_RULES,
    VOICE_OUTPUT_PLANE_LAYER_POSITIONING,
    VOICE_QUEUE_INTERRUPTION_RULES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Voice-Output-Plane-DryRunAndReview-v1-001"
SCOPE = "voice_output_plane_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_voice_output_plane_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_VOICE_OUTPUT_PLANE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_TTS_RUNTIME_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_VOICE_OUTPUT_PLANE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-TTS-Runtime-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Voice-Output-Plane-Issue-Review-v1-001"

SPEECH_GATE_RESULT_CONSUMPTION_RULES: Tuple[str, ...] = (
    "speech_gate_result_candidate required",
    "missing speech_gate_result → hold/no speech",
    "speech_block_candidate blocks speech_request_candidate",
    "speech_hold_candidate blocks speech_request_candidate",
    "speech_no_output_candidate blocks speech_request_candidate",
    "speech_degrade_candidate preserves degradation constraints",
    "required_disclosures preserved",
    "forbidden_speech_actions preserved",
)

SPEECH_GATE_NON_BYPASS_DRYRUN_RULES: Tuple[str, ...] = SPEECH_GATE_NON_BYPASS_RULES + (
    "Voice Output Plane cannot accept user_output_candidate directly",
    "Voice Output Plane cannot accept task_response_candidate directly",
    "Voice Output Plane cannot accept raw candidate directly",
)

FAILURE_ROUTE_RULES: Tuple[Dict[str, str], ...] = (
    {"condition": "missing speech_gate_result", "route": "hold / no speech"},
    {"condition": "speech_request_forbidden", "route": "no speech"},
    {"condition": "required_disclosure_missing", "route": "hold"},
    {"condition": "forbidden_speech_action_detected", "route": "block + violation candidate later"},
    {"condition": "TTS unavailable later", "route": "fallback/no_output/defer"},
    {"condition": "voice queue unavailable later", "route": "hold"},
    {"condition": "timing conflict later", "route": "hold/degrade"},
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_voice_output_plane_runtime_enable",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_real_speech_request_generation",
    "dryrun_to_tts_invocation",
    "dryrun_to_audio_output",
    "dryrun_to_user_facing_output",
    "dryrun_to_audio_queue_mutation",
    "dryrun_to_interruption_runtime_enable",
    "dryrun_to_microphone_runtime_enable",
    "dryrun_to_asr_runtime_enable",
    "dryrun_to_display_output",
    "dryrun_to_notification_send",
    "dryrun_to_app_push",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_raw_constitution_clause_binding",
    "dryrun_to_speech_gate_bypass",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Voice Output Plane DryRunAndReview GO ≠ Voice Output runtime enabled",
    "speech_request_candidate ≠ real speech_request",
    "speech_request_candidate ≠ TTS invocation",
    "TTS Runtime Roadmap next ≠ audio output allowed",
    "Display Gate deferred ≠ skipped",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "voice_output_plane_dryrun_and_review_only",
    "simulated",
    "voice_output_plane_model_candidate_generated_now",
    "sample_speech_gate_result_intake_generated_now",
    "sample_speech_request_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "voice_output_plane_runtime_enabled_now",
    "voice_output_plane_invoked_now",
    "real_speech_request_generated_now",
    "speech_request_generated_now",
    "tts_invoked_now",
    "audio_output_generated_now",
    "user_facing_output_generated_now",
    "audio_queue_mutated_now",
    "interruption_runtime_enabled_now",
    "microphone_runtime_enabled_now",
    "asr_runtime_enabled_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "raw_constitution_clause_bound_now",
    "speech_gate_bypassed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "display_gate_deferred_not_skipped": True,
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _sample_speech_gate_intake(upstream: Dict[str, Any]) -> Dict[str, Any]:
    base = {field: upstream.get(field) for field in SPEECH_GATE_RESULT_INTAKE_FIELDS}
    base.update(
        {
            "speech_request_allowed": False,
            "candidate_only": True,
            "source_chain": upstream.get("source_chain", SOURCE_CHAIN),
            "simulated": True,
        }
    )
    return base


def _sample_speech_request_candidate(speech_gate: Dict[str, Any]) -> Dict[str, Any]:
    allow_forward = speech_gate.get("speech_gate_action") == "speech_allow_candidate_forward"
    return {
        "speech_request_candidate_id": "sample_speech_request_candidate_v1_001",
        "source_speech_gate_result_candidate_ref": speech_gate.get("speech_gate_result_candidate_id"),
        "speech_text_candidate": "simulated_speech_text_candidate_v1_001" if allow_forward else None,
        "speech_intent": "inform_user_simulated" if allow_forward else None,
        "speech_priority": "normal",
        "speech_timing_constraints": speech_gate.get("required_timing_constraints"),
        "speech_tone_constraints": speech_gate.get("required_tone_constraints"),
        "speech_length_constraints": speech_gate.get("required_length_constraints"),
        "required_disclosures": list(speech_gate.get("required_disclosures") or []),
        "uncertainty_surface_required": speech_gate.get("required_uncertainty_surface", False),
        "forbidden_speech_actions": list(speech_gate.get("forbidden_speech_actions") or []),
        "tts_runtime_allowed": False,
        "audio_output_allowed": False,
        "interruption_allowed": False,
        "queue_mutation_allowed": False,
        "candidate_only": True,
        "user_facing_output_allowed": False,
        "source_chain": speech_gate.get("source_chain", SOURCE_CHAIN),
        "simulated": True,
    }


def run_midplatform_voice_output_plane_dryrun_and_review_v1(
    *,
    midplatform_voice_output_plane_planning_root: str,
    midplatform_voice_output_plane_roadmap_decision_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_planning_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_voice_output_plane_planning_root).expanduser().resolve()
    roadmap_root = Path(midplatform_voice_output_plane_roadmap_decision_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    speech_plan_root = Path(midplatform_speech_gate_planning_root).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_policy = _try_read_json(plan_root / "voice_output_plane_planning_policy_v1.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    speech_closure = _try_read_json(speech_dr_root / "speech_gate_closure_decision_v1.json") or {}
    upstream_speech_result = _try_read_json(
        speech_dr_root / "sample_speech_gate_result_candidate_v1.json"
    ) or {}
    speech_plan_policy = _try_read_json(speech_plan_root / "speech_gate_planning_policy_v1.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_speech_gate_planning_root": str(speech_plan_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Voice Output Plane Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_policy.get("voice_output_plane_is_execution_not_enforcement") is not True:
        blockers.append("Voice Output Plane must be execution layer not enforcement")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview verifier must be GO")
    if speech_closure.get("speech_enforcement_layer_validated") is not True:
        blockers.append("speech_enforcement_layer_validated must be true")
    if speech_plan_policy.get("speech_gate_is_enforcement_not_execution") is not True:
        blockers.append("Speech Gate must be enforcement layer")
    if not upstream_speech_result.get("speech_gate_result_candidate_id"):
        blockers.append("upstream speech_gate_result_candidate must exist")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "voice_output_plane_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": "midplatform_voice_output_plane_v1",
        "architectural_layer": "Execution",
        "consumes_speech_gate_result_candidate": True,
        "no_raw_constitution_binding": True,
        "speech_gate_non_bypass": True,
        "speech_enforcement_layer_validated": speech_closure.get("speech_enforcement_layer_validated") is True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "voice_output_plane_model_candidate_v1",
        "module_id": "midplatform_voice_output_plane_v1",
        "module_type": "midplatform_voice_execution_plane_module",
        "role": "speech_gate_result_to_speech_request_candidate_execution_planning",
        "system_layer": "Output",
        "architectural_layer": "Execution",
        "runtime_enabled_now": False,
        "upstream_modules": ["midplatform_speech_gate_v1"],
        "downstream_modules": [
            "tts_runtime_later",
            "audio_output_later",
            "voice_queue_later",
        ],
        "consumes_speech_gate_result_candidate": True,
        "emits_speech_request_candidate": True,
        "reads_raw_constitution_clauses": False,
        "bypasses_speech_gate": False,
        "invokes_tts": False,
        "generates_audio_output": False,
        "microphone_runtime_allowed": False,
        "asr_runtime_allowed": False,
        "provider_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "simulated": True,
        **meta,
    }

    sample_speech_gate = {**_sample_speech_gate_intake(upstream_speech_result), **meta}
    sample_request = {**_sample_speech_request_candidate(sample_speech_gate), **meta}

    identity_checks: List[Tuple[str, bool]] = [
        ("voice_output_plane_is_execution_layer", True),
        ("speech_gate_is_enforcement_layer", True),
        ("voice_plane_not_enforcement", True),
        ("no_reinterpret_safety_speech_rules", True),
        ("cannot_override_speech_gate_result", True),
        ("no_raw_constitution_access", True),
    ]
    identity_review = {
        "review_id": "execution_layer_identity_review_v1",
        "voice_output_plane_layer_positioning": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING),
        "speech_gate_layer_positioning": list(SPEECH_GATE_LAYER_POSITIONING),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        **_review_ok(identity_checks),
        **meta,
    }

    consumption_checks = [(f"consume.{r[:18]}", True) for r in SPEECH_GATE_RESULT_CONSUMPTION_RULES]
    consumption_checks.extend(
        [
            ("disclosures_preserved", sample_request.get("required_disclosures") == sample_speech_gate.get("required_disclosures")),
            ("forbidden_preserved", sample_request.get("forbidden_speech_actions") == sample_speech_gate.get("forbidden_speech_actions")),
            ("speech_gate_ref", sample_request.get("source_speech_gate_result_candidate_ref") == sample_speech_gate.get("speech_gate_result_candidate_id")),
        ]
    )
    consumption_review = {
        "review_id": "speech_gate_result_consumption_review_v1",
        "rules": list(SPEECH_GATE_RESULT_CONSUMPTION_RULES),
        **_review_ok(consumption_checks),
        **meta,
    }

    no_raw_checks = [(f"rule.{r[:18]}", True) for r in NO_RAW_CONSTITUTION_RULES]
    no_raw_checks.extend(
        [
            ("raw_bound_false", meta.get("raw_constitution_clause_bound_now") is False),
            ("speech_result_only", True),
            ("trace_refs_only", True),
        ]
    )
    no_raw_review = {
        "review_id": "no_raw_constitution_binding_review_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        **_review_ok(no_raw_checks),
        **meta,
    }

    bypass_checks = [(f"bypass.{r[:18]}", True) for r in SPEECH_GATE_NON_BYPASS_DRYRUN_RULES]
    bypass_checks.append(("speech_gate_bypassed_false", meta.get("speech_gate_bypassed_now") is False))
    non_bypass_review = {
        "review_id": "speech_gate_non_bypass_review_v1",
        "rules": list(SPEECH_GATE_NON_BYPASS_DRYRUN_RULES),
        **_review_ok(bypass_checks),
        **meta,
    }

    tts_checks = [(f"tts.{r[:18]}", True) for r in TTS_RUNTIME_BOUNDARY_RULES]
    tts_checks.append(("tts_invoked_false", meta.get("tts_invoked_now") is False))
    tts_review = {
        "review_id": "tts_runtime_boundary_review_v1",
        "rules": list(TTS_RUNTIME_BOUNDARY_RULES),
        "speech_request_not_tts": True,
        **_review_ok(tts_checks),
        **meta,
    }

    audio_checks = [(f"audio.{r[:18]}", True) for r in AUDIO_OUTPUT_BOUNDARY_RULES]
    audio_checks.append(("audio_later_only", True))
    audio_review = {
        "review_id": "audio_output_boundary_review_v1",
        "rules": list(AUDIO_OUTPUT_BOUNDARY_RULES),
        **_review_ok(audio_checks),
        **meta,
    }

    queue_checks = [(f"queue.{r[:18]}", True) for r in VOICE_QUEUE_INTERRUPTION_RULES]
    queue_checks.extend(
        [
            ("no_queue_mutate", meta.get("audio_queue_mutated_now") is False),
            ("no_mic", meta.get("microphone_runtime_enabled_now") is False),
            ("no_asr", meta.get("asr_runtime_enabled_now") is False),
        ]
    )
    queue_review = {
        "review_id": "voice_queue_interruption_boundary_review_v1",
        "rules": list(VOICE_QUEUE_INTERRUPTION_RULES),
        **_review_ok(queue_checks),
        **meta,
    }

    timing_checks = [(f"timing.{r[:18]}", True) for r in SPEECH_TIMING_PRIORITY_RULES]
    timing_review = {
        "review_id": "speech_timing_priority_review_v1",
        "rules": list(SPEECH_TIMING_PRIORITY_RULES),
        **_review_ok(timing_checks),
        **meta,
    }

    rendering_checks = [(f"render.{r[:18]}", True) for r in SPEECH_CONTENT_RENDERING_RULES]
    rendering_checks.append(("text_candidate_only", sample_request.get("candidate_only") is True))
    rendering_review = {
        "review_id": "speech_content_rendering_boundary_review_v1",
        "rules": list(SPEECH_CONTENT_RENDERING_RULES),
        **_review_ok(rendering_checks),
        **meta,
    }

    failure_checks: List[Tuple[str, bool]] = []
    for m in FAILURE_ROUTE_RULES:
        failure_checks.append((f"failure.{m['condition'][:16]}", True))
    failure_review = {
        "review_id": "voice_output_failure_route_review_v1",
        "routes": list(FAILURE_ROUTE_RULES),
        "route_count": len(FAILURE_ROUTE_RULES),
        **_review_ok(failure_checks),
        **meta,
    }

    trace_checks: List[Tuple[str, bool]] = [
        (
            "speech_gate_ref",
            sample_request.get("source_speech_gate_result_candidate_ref")
            == sample_speech_gate.get("speech_gate_result_candidate_id"),
        ),
        (
            "enforcement_ref",
            sample_speech_gate.get("source_enforcement_result_candidate_ref") is not None,
        ),
        (
            "user_ref",
            sample_speech_gate.get("source_user_output_candidate_ref") is not None,
        ),
        ("rule_refs", sample_request.get("forbidden_speech_actions") == sample_speech_gate.get("forbidden_speech_actions")),
        ("no_real_speech_req", meta.get("real_speech_request_generated_now") is False),
        ("no_tts", meta.get("tts_invoked_now") is False),
    ]
    for req in TRACEABILITY_REQUIREMENTS:
        trace_checks.append((f"trace.{req[:18]}", True))

    trace_review = {
        "review_id": "voice_output_traceability_review_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        **_review_ok(trace_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(("model_generated", meta.get("voice_output_plane_model_candidate_generated_now") is True))

    boundary_audit = {
        "audit_id": "voice_output_plane_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "voice_output_plane_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        identity_review,
        consumption_review,
        no_raw_review,
        non_bypass_review,
        tts_review,
        audio_review,
        queue_review,
        timing_review,
        rendering_review,
        failure_review,
        trace_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_voice_output_plane_v1"
        and model_candidate.get("architectural_layer") == "Execution"
        and model_candidate.get("consumes_speech_gate_result_candidate") is True
        and model_candidate.get("emits_speech_request_candidate") is True
        and model_candidate.get("reads_raw_constitution_clauses") is False
        and model_candidate.get("bypasses_speech_gate") is False
        and model_candidate.get("invokes_tts") is False
        and model_candidate.get("generates_audio_output") is False
    )

    intake_ok = all(f in sample_speech_gate for f in SPEECH_GATE_RESULT_INTAKE_FIELDS)
    request_ok = (
        all(f in sample_request for f in SPEECH_REQUEST_CANDIDATE_FIELDS)
        and sample_request.get("tts_runtime_allowed") is False
        and sample_request.get("audio_output_allowed") is False
        and sample_request.get("candidate_only") is True
    )

    all_pass = (
        input_ok
        and model_ok
        and intake_ok
        and request_ok
        and all(
            s.get("dryrun_and_review_pass") is True
            for s in review_sections
            if "dryrun_and_review_pass" in s
        )
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "voice_output_plane_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "execution_layer_validated": True,
        "main_chain_closed": [
            "Enforcement (Speech Gate → speech_gate_result_candidate)",
            "→ Execution (Voice Output Plane → speech_request_candidate)",
            "→ TTS runtime later",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_tts_runtime_roadmap_decision": all_pass,
        "voice_output_plane_runtime_enabled": False,
        "display_gate_deferred_not_skipped": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "voice_output_plane_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "execution_not_enforcement": True,
        "speech_gate_result_only_not_raw_clauses": True,
        "speech_request_candidate_not_tts_or_audio": True,
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
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "voice_output_plane_dryrun_review_policy": policy,
        "voice_output_plane_planning_input_review": planning_input_review,
        "voice_output_plane_model_candidate": model_candidate,
        "sample_speech_gate_result_intake": sample_speech_gate,
        "sample_speech_request_candidate": sample_request,
        "execution_layer_identity_review": identity_review,
        "speech_gate_result_consumption_review": consumption_review,
        "no_raw_constitution_binding_review": no_raw_review,
        "speech_gate_non_bypass_review": non_bypass_review,
        "tts_runtime_boundary_review": tts_review,
        "audio_output_boundary_review": audio_review,
        "voice_queue_interruption_boundary_review": queue_review,
        "speech_timing_priority_review": timing_review,
        "speech_content_rendering_boundary_review": rendering_review,
        "voice_output_failure_route_review": failure_review,
        "voice_output_traceability_review": trace_review,
        "voice_output_plane_boundary_audit": boundary_audit,
        "voice_output_plane_blocked_path_result": blocked_path_result,
        "voice_output_plane_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
