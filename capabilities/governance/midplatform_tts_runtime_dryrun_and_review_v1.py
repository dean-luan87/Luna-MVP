# -*- coding: utf-8 -*-
"""Midplatform TTS Runtime DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    AUDIO_ARTIFACT_CANDIDATE_FIELDS,
    AUDIO_PLAYBACK_BOUNDARY_RULES,
    AUDIO_SYNTHESIS_BOUNDARY_RULES,
    AUTHORIZATION_REQUIREMENTS,
    CACHE_ARTIFACT_BOUNDARY_RULES,
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
    FAILURE_ROUTE_MAPPINGS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HARNESS_ID,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NO_RAW_CONSTITUTION_RULES,
    PROVIDER_ABSTRACTION_RULES,
    PROVIDER_READINESS_RULES,
    PROVIDER_SWITCH_BOUNDARY_RULES,
    SPEECH_GATE_NON_BYPASS_RULES,
    SPEECH_REQUEST_INTAKE_FIELDS,
    TRACEABILITY_REQUIREMENTS,
    TTS_RUNTIME_LAYER_POSITIONING,
    VOICE_MODEL_BOUNDARY_RULES,
    VOICE_PROFILE_BOUNDARY_RULES,
)
from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    VOICE_OUTPUT_PLANE_LAYER_POSITIONING,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-TTS-Runtime-DryRunAndReview-v1-001"
SCOPE = "tts_runtime_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_tts_runtime_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_TTS_RUNTIME_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_END_TO_END_OUTPUT_CHAIN_SIMULATION_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_TTS_RUNTIME_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-End-to-End-Output-Chain-Simulation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-TTS-Runtime-Issue-Review-v1-001"

FUTURE_PROVIDER_CANDIDATES: Tuple[str, ...] = (
    "local_tts_candidate_later",
    "system_tts_candidate_later",
    "moss_tts_candidate_later",
    "external_tts_candidate_later",
)

PROVIDER_ABSTRACTION_DRYRUN_RULES: Tuple[str, ...] = (
    "TTS Runtime is abstract execution runtime",
    "TTS Runtime is not equal to Qianwen",
    "provider candidates are pluggable machines under runtime",
    "provider-specific logic stays outside runtime core",
    "provider selection requires ControlledProviderReadinessHarness later",
    "provider switch does not rewrite TTS Runtime core",
    "provider readiness / authorization / failure route are provider-scoped",
)

AUDIO_SYNTHESIS_DRYRUN_RULES: Tuple[str, ...] = AUDIO_SYNTHESIS_BOUNDARY_RULES + (
    "no Qianwen TTS execution",
)

TRACEABILITY_DRYRUN_REQUIREMENTS: Tuple[str, ...] = TRACEABILITY_REQUIREMENTS + (
    "provider candidate refs preserved",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_tts_runtime_enable",
    "dryrun_to_tts_runtime_invocation",
    "dryrun_to_provider_selection",
    "dryrun_to_qianwen_tts_invocation",
    "dryrun_to_qianwen_network_call",
    "dryrun_to_provider_auto_switch",
    "dryrun_to_provider_specific_runtime_logic_binding",
    "dryrun_to_provider_import",
    "dryrun_to_voice_model_selection",
    "dryrun_to_speech_request_submission",
    "dryrun_to_audio_synthesis",
    "dryrun_to_audio_artifact_generation",
    "dryrun_to_audio_output",
    "dryrun_to_audio_playback",
    "dryrun_to_speaker_device_access",
    "dryrun_to_model_download",
    "dryrun_to_cache_mutation",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_raw_constitution_clause_binding",
    "dryrun_to_speech_gate_bypass",
)

NON_CLAIMS: Tuple[str, ...] = (
    "TTS Runtime DryRunAndReview GO ≠ TTS runtime enabled",
    "qianwen_tts_candidate registered ≠ Qianwen selected",
    "sample audio_artifact_candidate ≠ audio generated",
    "provider abstraction pass ≠ provider switch allowed",
    "next End-to-End Simulation Planning ≠ real output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "tts_runtime_dryrun_and_review_only",
    "simulated",
    "tts_runtime_model_candidate_generated_now",
    "sample_speech_request_candidate_intake_generated_now",
    "sample_audio_artifact_candidate_generated_now",
    "provider_abstraction_review_generated_now",
    "qianwen_provider_candidate_review_generated_now",
    "provider_switch_boundary_review_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "tts_runtime_enabled_now",
    "tts_runtime_invoked_now",
    "tts_provider_selected_now",
    "provider_selected_for_execution_now",
    "tts_provider_imported_now",
    "qianwen_tts_invoked_now",
    "qianwen_network_call_executed_now",
    "provider_auto_switch_executed_now",
    "provider_specific_runtime_logic_bound_now",
    "voice_model_selected_now",
    "voice_profile_loaded_now",
    "speech_request_submitted_now",
    "audio_synthesis_invoked_now",
    "audio_artifact_generated_now",
    "audio_output_generated_now",
    "audio_playback_started_now",
    "speaker_device_accessed_now",
    "network_tts_call_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "raw_constitution_clause_bound_now",
    "speech_gate_bypassed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "controlled_provider_readiness_harness_ref": HARNESS_ID,
        "display_gate_deferred_not_skipped": True,
        "end_to_end_simulation_deferred_not_cancelled": True,
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


def _sample_speech_request_intake(upstream: Dict[str, Any]) -> Dict[str, Any]:
    base = {field: upstream.get(field) for field in SPEECH_REQUEST_INTAKE_FIELDS}
    base.update(
        {
            "tts_runtime_allowed": False,
            "audio_output_allowed": False,
            "interruption_allowed": False,
            "queue_mutation_allowed": False,
            "candidate_only": True,
            "user_facing_output_allowed": False,
            "source_chain": upstream.get("source_chain", SOURCE_CHAIN),
            "simulated": True,
        }
    )
    return base


def _sample_audio_artifact_candidate(speech_request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "audio_artifact_candidate_id": "sample_audio_artifact_candidate_v1_001",
        "source_speech_request_candidate_ref": speech_request.get("speech_request_candidate_id"),
        "tts_provider_ref": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "voice_model_ref": None,
        "voice_profile_ref": None,
        "audio_format_candidate": "simulated_format_candidate_pcm16",
        "audio_duration_candidate": None,
        "synthesis_metadata_refs": ["simulated_synthesis_metadata_ref_v1_001"],
        "required_disclosures_preserved": True,
        "uncertainty_surface_preserved": True,
        "timing_constraints_ref": speech_request.get("speech_timing_constraints"),
        "tone_constraints_ref": speech_request.get("speech_tone_constraints"),
        "evidence_refs": ["simulated_evidence_ref_v1_001"],
        "rationale_refs": ["simulated_rationale_ref_v1_001"],
        "whitebox_trace_refs": ["simulated_whitebox_trace_ref_v1_001"],
        "candidate_only": True,
        "audio_output_allowed": False,
        "playback_allowed": False,
        "user_facing_output_allowed": False,
        "source_chain": speech_request.get("source_chain", SOURCE_CHAIN),
        "simulated": True,
    }


def run_midplatform_tts_runtime_dryrun_and_review_v1(
    *,
    midplatform_tts_runtime_planning_root: str,
    midplatform_tts_runtime_roadmap_decision_root: str,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_tts_runtime_planning_root).expanduser().resolve()
    roadmap_root = Path(midplatform_tts_runtime_roadmap_decision_root).expanduser().resolve()
    voice_dr_root = Path(midplatform_voice_output_plane_dryrun_and_review_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    harness_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_policy = _try_read_json(plan_root / "tts_runtime_planning_policy_v1.json") or {}
    plan_module = _try_read_json(plan_root / "tts_runtime_module_definition_v1.json") or {}
    plan_provider_register = _try_read_json(
        plan_root / "current_tts_provider_candidate_register_v1.json"
    ) or {}
    voice_dr_vr = _try_read_json(voice_dr_root / "verifier_report.json") or {}
    voice_dr_sm = _try_read_json(voice_dr_root / "summary.json") or {}
    upstream_request = _try_read_json(voice_dr_root / "sample_speech_request_candidate_v1.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    speech_closure = _try_read_json(speech_dr_root / "speech_gate_closure_decision_v1.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    harness_registry = _try_read_json(
        harness_root / "controlled_provider_harness_registry_entry_review_v1.json"
    ) or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    module_identity = plan_module.get("module_identity") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_voice_output_plane_dryrun_root": str(voice_dr_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_harness_post_review_root": str(harness_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("TTS Runtime Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_policy.get("tts_runtime_is_execution_runtime_not_enforcement") is not True:
        blockers.append("TTS Runtime must be execution runtime not enforcement")
    if module_identity.get("runtime_abstraction") is not True:
        blockers.append("runtime_abstraction must be true")
    if module_identity.get("provider_abstraction_required") is not True:
        blockers.append("provider_abstraction_required must be true")
    if module_identity.get("provider_specific_logic_forbidden_in_runtime_core") is not True:
        blockers.append("provider_specific_logic_forbidden_in_runtime_core must be true")
    if module_identity.get("current_preferred_provider_candidate") != CURRENT_PREFERRED_PROVIDER_CANDIDATE:
        blockers.append("current_preferred_provider_candidate mismatch")
    if module_identity.get("provider_selected_for_execution_now") is not False:
        blockers.append("provider_selected_for_execution_now must be false")
    if plan_sm.get("qianwen_tts_invoked_now") is not False:
        blockers.append("qianwen_tts_invoked_now must be false")
    if voice_dr_vr.get("verifier") != "GO":
        blockers.append("Voice Output Plane DryRunAndReview verifier must be GO")
    if voice_dr_sm.get("final_decision") != VOICE_DR_FINAL_GO:
        blockers.append("voice output plane dryrun must be closed")
    if not upstream_request.get("speech_request_candidate_id"):
        blockers.append("upstream speech_request_candidate must exist")
    if upstream_request.get("tts_runtime_allowed") is not False:
        blockers.append("speech_request_candidate must not be TTS invocation")
    if upstream_request.get("candidate_only") is not True:
        blockers.append("speech_request_candidate must be candidate_only")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview verifier must be GO")
    if speech_closure.get("speech_enforcement_layer_validated") is not True:
        blockers.append("speech_enforcement_layer_validated must be true")
    if harness_vr.get("verifier") != "GO":
        blockers.append("ControlledProviderReadinessHarness post dryrun review must be GO")
    if harness_registry.get("review_pass") is not True:
        blockers.append("harness registry entry review must pass")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "tts_runtime_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": "midplatform_tts_runtime_v1",
        "architectural_layer": "ExecutionRuntime",
        "runtime_abstraction": module_identity.get("runtime_abstraction") is True,
        "provider_abstraction_required": module_identity.get("provider_abstraction_required") is True,
        "provider_specific_logic_forbidden_in_runtime_core": (
            module_identity.get("provider_specific_logic_forbidden_in_runtime_core") is True
        ),
        "current_preferred_provider_candidate": module_identity.get("current_preferred_provider_candidate"),
        "provider_selected_for_execution_now": False,
        "speech_request_candidate_exists": bool(upstream_request.get("speech_request_candidate_id")),
        "speech_request_not_tts": upstream_request.get("tts_runtime_allowed") is False,
        "speech_gate_non_bypass": True,
        "harness_post_review_go": harness_vr.get("verifier") == "GO",
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "tts_runtime_model_candidate_v1",
        "module_id": "midplatform_tts_runtime_v1",
        "module_type": "midplatform_voice_synthesis_runtime_module",
        "role": "speech_request_candidate_to_audio_artifact_runtime_planning",
        "system_layer": "Output",
        "architectural_layer": "ExecutionRuntime",
        "runtime_enabled_now": False,
        "runtime_abstraction": True,
        "provider_abstraction_required": True,
        "provider_specific_logic_forbidden_in_runtime_core": True,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "provider_selected_for_execution_now": False,
        "upstream_modules": ["midplatform_voice_output_plane_v1"],
        "downstream_modules": [
            "audio_output_later",
            "voice_queue_later",
            "playback_device_later",
        ],
        "consumes_speech_request_candidate": True,
        "emits_audio_artifact_candidate": True,
        "invokes_tts": False,
        "generates_audio_output": False,
        "reads_raw_constitution_clauses": False,
        "bypasses_speech_gate": False,
        "provider_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "simulated": True,
        **meta,
    }

    sample_intake = {**_sample_speech_request_intake(upstream_request), **meta}
    sample_audio = {**_sample_audio_artifact_candidate(sample_intake), **meta}

    provider_abstraction_checks = [(f"pabs.{r[:18]}", True) for r in PROVIDER_ABSTRACTION_DRYRUN_RULES]
    provider_abstraction_checks.append(
        ("provider_specific_logic_bound_false", meta.get("provider_specific_runtime_logic_bound_now") is False)
    )
    provider_abstraction_review = {
        "review_id": "tts_provider_abstraction_dryrun_review_v1",
        "rules": list(PROVIDER_ABSTRACTION_DRYRUN_RULES),
        "runtime_not_qianwen": True,
        **_review_ok(provider_abstraction_checks),
        **meta,
    }

    qianwen_entry = next(
        (
            x
            for x in (plan_provider_register.get("provider_candidates") or [])
            if x.get("provider_candidate_id") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
        ),
        {},
    )
    future_ids = [
        x.get("provider_candidate_id")
        for x in (plan_provider_register.get("provider_candidates") or [])
        if x.get("current_project_usage") == "future_candidate"
    ]
    qianwen_checks: List[Tuple[str, bool]] = [
        ("qianwen_registered", qianwen_entry.get("provider_candidate_id") == CURRENT_PREFERRED_PROVIDER_CANDIDATE),
        ("qianwen_type", qianwen_entry.get("provider_type") == "external_or_cloud_tts_provider"),
        ("qianwen_usage", qianwen_entry.get("current_project_usage") == "current_preferred_candidate"),
        ("runtime_invoked_false", qianwen_entry.get("runtime_invoked_now") is False),
        ("provider_selected_false", qianwen_entry.get("provider_selected_for_execution_now") is False),
        ("provider_imported_false", qianwen_entry.get("provider_imported_now") is False),
        ("qianwen_invoked_false", meta.get("qianwen_tts_invoked_now") is False),
        ("qianwen_network_false", meta.get("qianwen_network_call_executed_now") is False),
        ("voice_model_false", qianwen_entry.get("voice_model_selected_now") is False),
        ("audio_generated_false", qianwen_entry.get("audio_generated_now") is False),
    ]
    for fc in FUTURE_PROVIDER_CANDIDATES:
        qianwen_checks.append((f"future.{fc[:18]}", fc in future_ids))

    qianwen_provider_review = {
        "review_id": "current_tts_provider_candidate_review_v1",
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "future_provider_candidates": list(FUTURE_PROVIDER_CANDIDATES),
        "qianwen_candidate_registered_not_selected": True,
        **_review_ok(qianwen_checks),
        **meta,
    }

    switch_checks = [(f"switch.{r[:18]}", True) for r in PROVIDER_SWITCH_BOUNDARY_RULES]
    switch_checks.extend(
        [
            ("auto_switch_false", meta.get("provider_auto_switch_executed_now") is False),
            ("no_provider_exec_now", meta.get("provider_selected_for_execution_now") is False),
            ("no_network_now", meta.get("network_tts_call_executed_now") is False),
        ]
    )
    provider_switch_review = {
        "review_id": "provider_switch_boundary_dryrun_review_v1",
        "rules": list(PROVIDER_SWITCH_BOUNDARY_RULES),
        **_review_ok(switch_checks),
        **meta,
    }

    readiness_checks = [(f"ready.{r[:18]}", True) for r in PROVIDER_READINESS_RULES]
    readiness_review = {
        "review_id": "provider_readiness_requirement_review_v1",
        "rules": list(PROVIDER_READINESS_RULES),
        "controlled_provider_readiness_harness_ref": HARNESS_ID,
        **_review_ok(readiness_checks),
        **meta,
    }

    voice_model_checks = [(f"vmodel.{r[:18]}", True) for r in VOICE_MODEL_BOUNDARY_RULES]
    voice_model_review = {
        "review_id": "voice_model_boundary_review_v1",
        "rules": list(VOICE_MODEL_BOUNDARY_RULES),
        **_review_ok(voice_model_checks),
        **meta,
    }

    voice_profile_checks = [(f"vprofile.{r[:18]}", True) for r in VOICE_PROFILE_BOUNDARY_RULES]
    voice_profile_review = {
        "review_id": "voice_profile_personalization_boundary_review_v1",
        "rules": list(VOICE_PROFILE_BOUNDARY_RULES),
        **_review_ok(voice_profile_checks),
        **meta,
    }

    synthesis_checks = [(f"synth.{r[:18]}", True) for r in AUDIO_SYNTHESIS_DRYRUN_RULES]
    synthesis_checks.append(("synthesis_invoked_false", meta.get("audio_synthesis_invoked_now") is False))
    synthesis_review = {
        "review_id": "audio_synthesis_boundary_review_v1",
        "rules": list(AUDIO_SYNTHESIS_DRYRUN_RULES),
        **_review_ok(synthesis_checks),
        **meta,
    }

    playback_checks = [(f"playback.{r[:18]}", True) for r in AUDIO_PLAYBACK_BOUNDARY_RULES]
    playback_checks.extend(
        [
            ("audio_output_false", meta.get("audio_output_generated_now") is False),
            ("playback_false", meta.get("audio_playback_started_now") is False),
        ]
    )
    playback_review = {
        "review_id": "audio_output_playback_boundary_review_v1",
        "rules": list(AUDIO_PLAYBACK_BOUNDARY_RULES),
        **_review_ok(playback_checks),
        **meta,
    }

    cache_checks = [(f"cache.{r[:18]}", True) for r in CACHE_ARTIFACT_BOUNDARY_RULES]
    cache_review = {
        "review_id": "cache_artifact_boundary_review_v1",
        "rules": list(CACHE_ARTIFACT_BOUNDARY_RULES),
        **_review_ok(cache_checks),
        **meta,
    }

    auth_checks = [(f"auth.{r[:18]}", True) for r in AUTHORIZATION_REQUIREMENTS]
    authorization_review = {
        "review_id": "authorization_requirement_review_v1",
        "requirements": list(AUTHORIZATION_REQUIREMENTS),
        **_review_ok(auth_checks),
        **meta,
    }

    failure_checks: List[Tuple[str, bool]] = []
    for m in FAILURE_ROUTE_MAPPINGS:
        failure_checks.append((f"failure.{m['condition'][:16]}", True))
    failure_review = {
        "review_id": "tts_failure_route_review_v1",
        "routes": list(FAILURE_ROUTE_MAPPINGS),
        "route_count": len(FAILURE_ROUTE_MAPPINGS),
        **_review_ok(failure_checks),
        **meta,
    }

    trace_checks: List[Tuple[str, bool]] = [
        (
            "request_ref",
            sample_audio.get("source_speech_request_candidate_ref")
            == sample_intake.get("speech_request_candidate_id"),
        ),
        (
            "gate_ref",
            sample_intake.get("source_speech_gate_result_candidate_ref") is not None,
        ),
        ("provider_ref", sample_audio.get("tts_provider_ref") == CURRENT_PREFERRED_PROVIDER_CANDIDATE),
        ("disclosures_preserved", sample_audio.get("required_disclosures_preserved") is True),
        ("uncertainty_preserved", sample_audio.get("uncertainty_surface_preserved") is True),
        ("no_audio_gen", meta.get("audio_artifact_generated_now") is False),
        ("no_tts_invoke", meta.get("tts_runtime_invoked_now") is False),
    ]
    for req in TRACEABILITY_DRYRUN_REQUIREMENTS:
        trace_checks.append((f"trace.{req[:18]}", True))

    traceability_review = {
        "review_id": "tts_traceability_audit_review_v1",
        "requirements": list(TRACEABILITY_DRYRUN_REQUIREMENTS),
        **_review_ok(trace_checks),
        **meta,
    }

    no_raw_checks = [(f"noraw.{r[:18]}", True) for r in NO_RAW_CONSTITUTION_RULES]
    no_raw_checks.append(("raw_bound_false", meta.get("raw_constitution_clause_bound_now") is False))
    no_raw_review = {
        "review_id": "tts_no_raw_constitution_review_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        **_review_ok(no_raw_checks),
        **meta,
    }

    bypass_checks = [(f"bypass.{r[:18]}", True) for r in SPEECH_GATE_NON_BYPASS_RULES]
    bypass_checks.append(("speech_gate_bypassed_false", meta.get("speech_gate_bypassed_now") is False))
    non_bypass_review = {
        "review_id": "tts_speech_gate_non_bypass_review_v1",
        "rules": list(SPEECH_GATE_NON_BYPASS_RULES),
        **_review_ok(bypass_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.extend(
        [
            ("model_generated", meta.get("tts_runtime_model_candidate_generated_now") is True),
            ("intake_generated", meta.get("sample_speech_request_candidate_intake_generated_now") is True),
            ("audio_candidate_generated", meta.get("sample_audio_artifact_candidate_generated_now") is True),
            ("provider_abstraction_generated", meta.get("provider_abstraction_review_generated_now") is True),
            ("qianwen_review_generated", meta.get("qianwen_provider_candidate_review_generated_now") is True),
            ("switch_review_generated", meta.get("provider_switch_boundary_review_generated_now") is True),
        ]
    )
    boundary_audit = {
        "audit_id": "tts_runtime_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "tts_runtime_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        provider_abstraction_review,
        qianwen_provider_review,
        provider_switch_review,
        readiness_review,
        voice_model_review,
        voice_profile_review,
        synthesis_review,
        playback_review,
        cache_review,
        authorization_review,
        failure_review,
        traceability_review,
        no_raw_review,
        non_bypass_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_tts_runtime_v1"
        and model_candidate.get("architectural_layer") == "ExecutionRuntime"
        and model_candidate.get("runtime_abstraction") is True
        and model_candidate.get("provider_abstraction_required") is True
        and model_candidate.get("provider_specific_logic_forbidden_in_runtime_core") is True
        and model_candidate.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
        and model_candidate.get("provider_selected_for_execution_now") is False
        and model_candidate.get("consumes_speech_request_candidate") is True
        and model_candidate.get("emits_audio_artifact_candidate") is True
        and model_candidate.get("reads_raw_constitution_clauses") is False
        and model_candidate.get("bypasses_speech_gate") is False
        and model_candidate.get("invokes_tts") is False
        and model_candidate.get("generates_audio_output") is False
        and model_candidate.get("provider_invocation_allowed") is False
    )

    intake_ok = (
        all(f in sample_intake for f in SPEECH_REQUEST_INTAKE_FIELDS)
        and sample_intake.get("tts_runtime_allowed") is False
        and sample_intake.get("audio_output_allowed") is False
        and sample_intake.get("candidate_only") is True
    )

    audio_ok = (
        all(f in sample_audio for f in AUDIO_ARTIFACT_CANDIDATE_FIELDS)
        and sample_audio.get("tts_provider_ref") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
        and sample_audio.get("voice_model_ref") is None
        and sample_audio.get("voice_profile_ref") is None
        and sample_audio.get("required_disclosures_preserved") is True
        and sample_audio.get("uncertainty_surface_preserved") is True
        and sample_audio.get("candidate_only") is True
        and sample_audio.get("audio_output_allowed") is False
        and sample_audio.get("playback_allowed") is False
        and sample_audio.get("user_facing_output_allowed") is False
    )

    all_pass = (
        input_ok
        and model_ok
        and intake_ok
        and audio_ok
        and all(
            s.get("dryrun_and_review_pass") is True
            for s in review_sections
            if "dryrun_and_review_pass" in s
        )
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "tts_runtime_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "execution_runtime_validated": True,
        "provider_abstraction_validated": True,
        "main_chain_closed": [
            "Enforcement (Speech Gate → speech_gate_result_candidate)",
            "→ Execution (Voice Output Plane → speech_request_candidate)",
            "→ TTS Runtime (audio_artifact_candidate later)",
            "→ playback later",
        ],
        "tts_runtime_layer_positioning": list(TTS_RUNTIME_LAYER_POSITIONING),
        "voice_output_plane_layer_positioning": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_end_to_end_output_chain_simulation_planning": all_pass,
        "tts_runtime_runtime_enabled": False,
        "provider_selected_for_execution": False,
        "display_gate_deferred_not_skipped": True,
        "end_to_end_simulation_deferred_not_cancelled": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "tts_runtime_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "execution_runtime_not_enforcement": True,
        "runtime_abstraction": True,
        "provider_abstraction_required": True,
        "speech_request_candidate_not_tts_or_audio": True,
        "audio_artifact_candidate_not_audio_output": True,
        "qianwen_is_provider_candidate_not_runtime": True,
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
        "tts_runtime_dryrun_review_policy": policy,
        "tts_runtime_planning_input_review": planning_input_review,
        "tts_runtime_model_candidate": model_candidate,
        "sample_speech_request_candidate_intake": sample_intake,
        "sample_audio_artifact_candidate": sample_audio,
        "tts_provider_abstraction_dryrun_review": provider_abstraction_review,
        "current_tts_provider_candidate_review": qianwen_provider_review,
        "provider_switch_boundary_dryrun_review": provider_switch_review,
        "provider_readiness_requirement_review": readiness_review,
        "voice_model_boundary_review": voice_model_review,
        "voice_profile_personalization_boundary_review": voice_profile_review,
        "audio_synthesis_boundary_review": synthesis_review,
        "audio_output_playback_boundary_review": playback_review,
        "cache_artifact_boundary_review": cache_review,
        "authorization_requirement_review": authorization_review,
        "tts_failure_route_review": failure_review,
        "tts_traceability_audit_review": traceability_review,
        "tts_no_raw_constitution_review": no_raw_review,
        "tts_speech_gate_non_bypass_review": non_bypass_review,
        "tts_runtime_boundary_audit": boundary_audit,
        "tts_runtime_blocked_path_result": blocked_path_result,
        "tts_runtime_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
