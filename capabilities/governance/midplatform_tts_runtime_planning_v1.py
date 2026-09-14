# -*- coding: utf-8 -*-
"""Midplatform TTS Runtime Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_tts_runtime_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    ROUTE_D,
    SELECTED_ROUTE,
)
from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    SPEECH_REQUEST_CANDIDATE_FIELDS,
    VOICE_OUTPUT_PLANE_LAYER_POSITIONING,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-TTS-Runtime-Planning-v1-001"
SCOPE = "tts_runtime_planning_only"
SOURCE_CHAIN = "midplatform_tts_runtime_planning_v1"
HARNESS_ID = "controlled_provider_readiness_harness_v1"
CURRENT_PREFERRED_PROVIDER_CANDIDATE = "qianwen_tts_candidate"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_TTS_RUNTIME_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_TTS_RUNTIME_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-TTS-Runtime-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-TTS-Runtime-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "speech_request_candidate → audio_artifact_candidate later → playback later; no synthesis now"
)

TTS_RUNTIME_LAYER_POSITIONING: Tuple[str, ...] = (
    "TTS Runtime is execution runtime, not enforcement layer",
    "TTS Runtime consumes speech_request_candidate and emits audio_artifact_candidate later",
    "Voice Output Plane is upstream execution; TTS Runtime is downstream synthesis runtime",
    "TTS Runtime does not read raw constitution clauses",
    "TTS Runtime cannot bypass Speech Gate or Voice Output Plane",
    "TTS Runtime is abstract execution runtime (provider-pluggable)",
    "TTS Runtime is not equal to any specific provider candidate (e.g., Qianwen)",
    "provider readiness via ControlledProviderReadinessHarness required later (provider-scoped)",
)

SPEECH_REQUEST_INTAKE_FIELDS: Tuple[str, ...] = SPEECH_REQUEST_CANDIDATE_FIELDS

AUDIO_ARTIFACT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "audio_artifact_candidate_id",
    "source_speech_request_candidate_ref",
    "tts_provider_ref",
    "voice_model_ref",
    "voice_profile_ref",
    "audio_format_candidate",
    "audio_duration_candidate",
    "synthesis_metadata_refs",
    "required_disclosures_preserved",
    "uncertainty_surface_preserved",
    "timing_constraints_ref",
    "tone_constraints_ref",
    "evidence_refs",
    "rationale_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "audio_output_allowed",
    "playback_allowed",
    "user_facing_output_allowed",
)

PROVIDER_READINESS_RULES: Tuple[str, ...] = (
    "provider readiness applies to provider candidates, not runtime core",
    "qianwen_tts_candidate must pass provider readiness before execution",
    "ControlledProviderReadinessHarness required later",
    "provider selection requires authorization later",
    "provider import / SDK / network access requires separate check later",
    "local / external / cloud TTS providers are candidates only",
    "no provider selected now",
    "no provider imported now",
    "no network TTS call now",
    "no model runtime invocation now",
)

PROVIDER_ABSTRACTION_RULES: Tuple[str, ...] = (
    "TTS Runtime is abstract execution runtime",
    "TTS Runtime is not equal to Qianwen",
    "provider candidates are pluggable machines under runtime",
    "current provider candidate may be qianwen_tts_candidate",
    "provider-specific logic must stay outside runtime core",
    "provider selection requires ControlledProviderReadinessHarness later",
    "provider switch should not rewrite TTS Runtime core",
    "provider readiness / authorization / failure route must be provider-scoped",
)

PROVIDER_SWITCH_BOUNDARY_RULES: Tuple[str, ...] = (
    "switching provider must not rewrite TTS Runtime core",
    "provider-specific adapter may change later",
    "provider selection requires readiness / authorization / evidence",
    "provider failure triggers fallback candidate, not automatic switch",
    "no provider auto-selection now",
    "no provider runtime invocation now",
    "no network TTS call now",
)

VOICE_MODEL_BOUNDARY_RULES: Tuple[str, ...] = (
    "no voice model selected now",
    "no voice model loaded now",
    "no voice cloning now",
    "no restricted / unsafe voice impersonation",
    "model license / consent / privacy checks required later",
    "voice model selection cannot override speech_gate_result",
)

VOICE_PROFILE_BOUNDARY_RULES: Tuple[str, ...] = (
    "personalization may affect tone later",
    "personalization cannot remove safety disclosures",
    "personalization cannot remove uncertainty",
    "personalization cannot imitate protected voice without authorization",
    "no personal memory write",
    "no user profile update",
    "no speaker identity binding now",
)

AUDIO_SYNTHESIS_BOUNDARY_RULES: Tuple[str, ...] = (
    "audio_synthesis_invoked_now=false",
    "no waveform generation",
    "no streaming synthesis",
    "no local TTS execution",
    "no external TTS execution",
    "no audio artifact generated now",
)

AUDIO_PLAYBACK_BOUNDARY_RULES: Tuple[str, ...] = (
    "audio_output_generated_now=false",
    "audio_playback_started_now=false",
    "no speaker device access",
    "no playback queue mutation",
    "no haptic/audio fallback",
    "no user-facing voice output",
)

CACHE_ARTIFACT_BOUNDARY_RULES: Tuple[str, ...] = (
    "no cache mutation",
    "no model download",
    "no audio file write",
    "no artifact persisted",
    "no temp audio artifact generated",
    "later cache use requires controlled path + audit",
)

AUTHORIZATION_REQUIREMENTS: Tuple[str, ...] = (
    "speech_request_candidate exists",
    "Voice Output Plane pass",
    "Speech Gate result pass",
    "provider readiness pass",
    "TTS runtime authorization",
    "audio output authorization",
    "failure/rollback plan",
    "evidence capture plan",
    "post-execution review",
)

FAILURE_ROUTE_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"condition": "missing speech_request_candidate", "route": "hold / no TTS"},
    {"condition": "speech_request_forbidden", "route": "no TTS"},
    {"condition": "provider_not_ready", "route": "hold / provider readiness route"},
    {"condition": "voice_model_missing", "route": "hold / no download"},
    {"condition": "synthesis_failure later", "route": "no_output / fallback / issue_trace"},
    {"condition": "playback_unavailable later", "route": "hold / degraded route"},
    {"condition": "forbidden_speech_action_detected", "route": "block + violation candidate"},
    {"condition": "required_disclosure_missing", "route": "hold"},
)

TRACEABILITY_REQUIREMENTS: Tuple[str, ...] = (
    "source_speech_request_candidate_ref preserved",
    "source_speech_gate_result_candidate_ref preserved",
    "source_enforcement_result_candidate_ref preserved",
    "applicable_rule_refs preserved",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "whitebox_trace_refs preserved",
    "provider readiness refs preserved later",
    "synthesis metadata auditable later",
)

NO_RAW_CONSTITUTION_RULES: Tuple[str, ...] = (
    "TTS Runtime does not read raw constitution",
    "TTS Runtime does not consume constraint_bundle directly",
    "TTS Runtime consumes speech_request_candidate only",
    "applicable_rule_refs are trace refs only",
    "constitution changes propagate through Resolver → bundle → gates → speech_request_candidate",
)

SPEECH_GATE_NON_BYPASS_RULES: Tuple[str, ...] = (
    "TTS cannot run without speech_request_candidate",
    "speech_request_candidate must reference speech_gate_result_candidate",
    "blocked/hold/no_output speech result blocks TTS",
    "TTS cannot override required disclosures",
    "TTS cannot override forbidden_speech_actions",
    "TTS cannot override uncertainty_surface_required",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "tts_runtime_enabled_now",
    "tts_runtime_invoked_now",
    "tts_provider_selected_now",
    "tts_provider_imported_now",
    "provider_selected_for_execution_now",
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
    "microphone_runtime_enabled_now",
    "asr_runtime_enabled_now",
    "audio_queue_mutated_now",
    "interruption_runtime_enabled_now",
    "network_tts_call_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "raw_constitution_clause_bound_now",
    "speech_gate_bypassed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "TTS Runtime Planning GO ≠ TTS runtime enabled",
    "provider readiness planned ≠ provider selected",
    "audio artifact contract ≠ audio generated",
    "voice model boundary planned ≠ voice model loaded",
    "next DryRunAndReview ≠ audio output allowed",
    "TTS Runtime Planning GO ≠ Qianwen selected",
    "current_preferred_provider_candidate ≠ provider selected for execution",
    "provider abstraction planned ≠ provider switch allowed",
    "Qianwen candidate registered ≠ Qianwen invoked",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("tts_runtime_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "template_id": TEMPLATE_ID,
        "core_chain_boundary": CORE_CHAIN_BOUNDARY,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
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


def _tts_runtime_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "tts_runtime_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_tts_runtime_v1",
            "module_type": "midplatform_voice_synthesis_runtime_module",
            "role": "speech_request_candidate_to_audio_artifact_runtime_planning",
            "system_layer": "Output",
            "architectural_layer": "ExecutionRuntime",
            "runtime_abstraction": True,
            "provider_abstraction_required": True,
            "provider_specific_logic_forbidden_in_runtime_core": True,
            "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
            "provider_selected_for_execution_now": False,
            "layer_positioning": "TTS Runtime is execution runtime, not enforcement layer",
        },
        "upstream_sources": {
            "upstream_modules": ["midplatform_voice_output_plane_v1"],
            "upstream_object_types": [
                "speech_request_candidate",
                "required_disclosures",
                "uncertainty_surface_required",
                "speech_tone_constraints",
                "forbidden_speech_actions",
            ],
            "required_inputs": list(SPEECH_REQUEST_INTAKE_FIELDS),
            "optional_inputs": ["channel_preferences"],
            "forbidden_inputs": [
                "raw_constitution_clauses",
                "constraint_bundle_direct",
                "user_output_candidate_direct",
                "task_response_candidate_direct",
                "speech_gate_bypass_directive",
                "tts_provider_directive_without_readiness",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "audio_output_later",
                "voice_queue_later",
                "playback_device_later",
            ],
            "downstream_object_types": ["audio_artifact_candidate"],
            "allowed_outputs": ["audio_artifact_candidate"],
            "forbidden_outputs": [
                "user_facing_audio",
                "persisted_audio_file",
                "memory_fact",
            ],
        },
        "input_contract": {
            "input_contract": "speech_request_candidate_intake_contract_v1",
            "source_chain": "preserved_from_speech_request_candidate",
            "evidence_ref": "preserved",
            "ttl": "required_from_speech_request_candidate",
            "confidence": "preserved_as_uncertainty_surface",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": (
                "consume speech_request_candidate later; plan audio_artifact_candidate "
                "with provider readiness, synthesis, playback, cache boundaries"
            ),
            "allowed_transformation": [
                "plan audio_artifact_candidate contract",
                "preserve disclosures/uncertainty/tone constraints",
                "plan provider readiness requirements",
                "plan authorization and failure routes",
                "preserve refs and traceability",
            ],
            "forbidden_transformation": [
                "read raw constitution clauses",
                "bypass Speech Gate or Voice Output Plane",
                "modify speech_text removing constraints",
                "select or import TTS provider",
                "download voice model",
                "synthesize or play audio",
                "write memory or world model",
                "commit task_state",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "tts_runtime_output_contract_v1",
            "output_object_type": "audio_artifact_candidate",
            "decision_refs": "source_speech_request_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_intake",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": list(TTS_RUNTIME_LAYER_POSITIONING) + [
                "audio_artifact_candidate ≠ audio output ≠ playback",
            ],
            "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
            "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
            "priority_policy": "Speech Gate / Voice Output Plane constraints override TTS preferences",
            "conflict_policy": "forbidden_speech_actions from speech_request enforced",
            "fallback_policy": "hold/no_output when speech_request not allowed for TTS",
            "rollback_policy": "runtime planner does not commit state or emit audio",
        },
        "external_constraints": {
            "constitution_constraints": "via speech_request_candidate refs only; no raw clause binding",
            "domain_standard_constraints": "preserved from upstream refs",
            "validation_gate_constraints": "ControlledProviderReadinessHarness required later",
            "health_signal_constraints": "risk context optional",
            "whitebox_visibility_constraints": "applicable_rule_refs and trace refs preserved",
            "decision_center_constraints": "does not re-decide upstream enforcement decisions",
        },
        "runtime_boundaries": {
            "runtime_enabled_now": False,
            "write_allowed_now": False,
            "provider_invocation_allowed_now": False,
            "user_output_allowed_now": False,
            "memory_allowed_now": False,
            "world_model_allowed_now": False,
        },
        "failure_and_traceability": {
            "failure_route": "hold/no_output/defer per failure_route_plan",
            "issue_trace": "whitebox_trace_refs preserved",
            "violation_report": "forbidden action → violation candidate later",
            "escalation_path": "provider readiness / authorization failure routes",
            "audit_required": True,
        },
    }


def run_midplatform_tts_runtime_planning_v1(
    *,
    midplatform_tts_runtime_roadmap_decision_root: str,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_voice_output_plane_planning_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(midplatform_tts_runtime_roadmap_decision_root).expanduser().resolve()
    voice_dr_root = Path(midplatform_voice_output_plane_dryrun_and_review_root).expanduser().resolve()
    voice_plan_root = Path(midplatform_voice_output_plane_planning_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()
    harness_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    ).expanduser().resolve()

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    blocked_register = _try_read_json(roadmap_root / "deferred_routes_register_v1.json") or {}
    voice_dr_vr = _try_read_json(voice_dr_root / "verifier_report.json") or {}
    voice_dr_sm = _try_read_json(voice_dr_root / "summary.json") or {}
    sample_request = _try_read_json(voice_dr_root / "sample_speech_request_candidate_v1.json") or {}
    voice_plan_policy = _try_read_json(voice_plan_root / "voice_output_plane_planning_policy_v1.json") or {}
    speech_closure = _try_read_json(speech_dr_root / "speech_gate_closure_decision_v1.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    harness_registry = _try_read_json(
        harness_root / "controlled_provider_harness_registry_entry_review_v1.json"
    ) or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_voice_output_plane_dryrun_root": str(voice_dr_root),
        "upstream_voice_output_plane_planning_root": str(voice_plan_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_template_planning_root": str(template_root),
        "upstream_harness_post_review_root": str(harness_root),
        "output_root": str(out_root),
    }

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("TTS Runtime Roadmap Decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A — TTS Runtime Planning")
    if voice_dr_vr.get("verifier") != "GO":
        blockers.append("Voice Output Plane DryRunAndReview verifier must be GO")
    if voice_dr_sm.get("final_decision") != VOICE_DR_FINAL_GO:
        blockers.append("voice output plane dryrun must be closed")
    if voice_plan_policy.get("voice_output_plane_is_execution_not_enforcement") is not True:
        blockers.append("Voice Output Plane must be execution layer")
    if not sample_request.get("speech_request_candidate_id"):
        blockers.append("sample speech_request_candidate must exist")
    if sample_request.get("candidate_only") is not True:
        blockers.append("speech_request_candidate must be candidate_only")
    if sample_request.get("tts_runtime_allowed") is not False:
        blockers.append("speech_request_candidate tts_runtime_allowed must be false")
    if speech_closure.get("speech_enforcement_layer_validated") is not True:
        blockers.append("speech enforcement layer must be validated")
    blocked_paths = [
        x.get("route")
        for x in (blocked_register.get("blocked_routes") or [])
        if x.get("status") == "blocked"
    ]
    if ROUTE_D not in blocked_paths:
        blockers.append("Direct TTS Execution route must be blocked")
    if harness_vr.get("verifier") != "GO":
        blockers.append("ControlledProviderReadinessHarness post dryrun review must be GO")
    if harness_registry.get("review_pass") is not True:
        blockers.append("harness registry entry review must pass")
    if harness_registry.get("module_id") != HARNESS_ID:
        blockers.append("harness module_id mismatch")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    module_def = _tts_runtime_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    roadmap_input_review = {
        "review_id": "tts_runtime_roadmap_input_review_v1",
        "roadmap_verifier": roadmap_vr.get("verifier"),
        "roadmap_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "voice_output_plane_dryrun_verifier": voice_dr_vr.get("verifier"),
        "speech_request_candidate_exists": bool(sample_request.get("speech_request_candidate_id")),
        "speech_request_not_real": sample_request.get("candidate_only") is True,
        "speech_request_not_tts": sample_request.get("tts_runtime_allowed") is False,
        "direct_tts_route_blocked": ROUTE_D in blocked_paths,
        "harness_post_review_go": harness_vr.get("verifier") == "GO",
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    speech_request_intake = {
        "contract_id": "speech_request_candidate_intake_contract_v1",
        "required_fields": list(SPEECH_REQUEST_INTAKE_FIELDS),
        "consumes_speech_request_candidate_only": True,
        "raw_constitution_clause_binding_forbidden": True,
        "speech_gate_bypass_forbidden": True,
        "candidate_only": True,
        **meta,
    }

    output_contract = {
        "contract_id": "tts_runtime_output_contract_v1",
        "output_type": "audio_artifact_candidate",
        "required_fields": list(AUDIO_ARTIFACT_CANDIDATE_FIELDS),
        "defaults": {
            "candidate_only": True,
            "audio_output_allowed": False,
            "playback_allowed": False,
            "user_facing_output_allowed": False,
        },
        "not_synthesis_or_playback": True,
        **meta,
    }

    provider_readiness = {
        "plan_id": "tts_provider_readiness_plan_v1",
        "rules": list(PROVIDER_READINESS_RULES),
        "rule_count": len(PROVIDER_READINESS_RULES),
        "controlled_provider_readiness_harness_ref": HARNESS_ID,
        **meta,
    }

    provider_abstraction = {
        "plan_id": "tts_provider_abstraction_plan_v1",
        "rules": list(PROVIDER_ABSTRACTION_RULES),
        "rule_count": len(PROVIDER_ABSTRACTION_RULES),
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        **meta,
    }

    current_provider_candidate_register = {
        "register_id": "current_tts_provider_candidate_register_v1",
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "provider_candidates": [
            {
                "provider_candidate_id": "qianwen_tts_candidate",
                "provider_type": "external_or_cloud_tts_provider",
                "current_project_usage": "current_preferred_candidate",
                "runtime_invoked_now": False,
                "provider_selected_for_execution_now": False,
                "provider_imported_now": False,
                "network_call_executed_now": False,
                "voice_model_selected_now": False,
                "audio_generated_now": False,
            },
            {
                "provider_candidate_id": "local_tts_candidate_later",
                "provider_type": "local_tts_provider_candidate_later",
                "current_project_usage": "future_candidate",
            },
            {
                "provider_candidate_id": "system_tts_candidate_later",
                "provider_type": "system_tts_provider_candidate_later",
                "current_project_usage": "future_candidate",
            },
            {
                "provider_candidate_id": "moss_tts_candidate_later",
                "provider_type": "external_or_cloud_tts_provider_candidate_later",
                "current_project_usage": "future_candidate",
            },
            {
                "provider_candidate_id": "external_tts_candidate_later",
                "provider_type": "external_or_cloud_tts_provider_candidate_later",
                "current_project_usage": "future_candidate",
            },
        ],
        "runtime_invoked_now": False,
        "provider_selected_for_execution_now": False,
        "provider_imported_now": False,
        "network_call_executed_now": False,
        "voice_model_selected_now": False,
        "audio_generated_now": False,
        **meta,
    }

    provider_switch_boundary = {
        "plan_id": "provider_switch_boundary_plan_v1",
        "rules": list(PROVIDER_SWITCH_BOUNDARY_RULES),
        "rule_count": len(PROVIDER_SWITCH_BOUNDARY_RULES),
        "provider_auto_switch_executed_now": False,
        "provider_selected_for_execution_now": False,
        **meta,
    }

    voice_model = {
        "plan_id": "tts_voice_model_boundary_plan_v1",
        "rules": list(VOICE_MODEL_BOUNDARY_RULES),
        "rule_count": len(VOICE_MODEL_BOUNDARY_RULES),
        **meta,
    }

    voice_profile = {
        "plan_id": "tts_voice_profile_personalization_boundary_plan_v1",
        "rules": list(VOICE_PROFILE_BOUNDARY_RULES),
        "rule_count": len(VOICE_PROFILE_BOUNDARY_RULES),
        **meta,
    }

    synthesis_boundary = {
        "plan_id": "tts_audio_synthesis_boundary_plan_v1",
        "rules": list(AUDIO_SYNTHESIS_BOUNDARY_RULES),
        "rule_count": len(AUDIO_SYNTHESIS_BOUNDARY_RULES),
        **meta,
    }

    playback_boundary = {
        "plan_id": "tts_audio_output_playback_boundary_plan_v1",
        "rules": list(AUDIO_PLAYBACK_BOUNDARY_RULES),
        "rule_count": len(AUDIO_PLAYBACK_BOUNDARY_RULES),
        **meta,
    }

    cache_boundary = {
        "plan_id": "tts_cache_and_artifact_boundary_plan_v1",
        "rules": list(CACHE_ARTIFACT_BOUNDARY_RULES),
        "rule_count": len(CACHE_ARTIFACT_BOUNDARY_RULES),
        **meta,
    }

    authorization = {
        "plan_id": "tts_authorization_requirement_plan_v1",
        "requirements": list(AUTHORIZATION_REQUIREMENTS),
        "requirement_count": len(AUTHORIZATION_REQUIREMENTS),
        **meta,
    }

    failure_routes = {
        "plan_id": "tts_failure_route_plan_v1",
        "routes": list(FAILURE_ROUTE_MAPPINGS),
        "route_count": len(FAILURE_ROUTE_MAPPINGS),
        **meta,
    }

    traceability = {
        "plan_id": "tts_traceability_audit_plan_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        "requirement_count": len(TRACEABILITY_REQUIREMENTS),
        **meta,
    }

    no_raw = {
        "policy_id": "tts_no_raw_constitution_policy_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "rule_count": len(NO_RAW_CONSTITUTION_RULES),
        "consumes_speech_request_candidate_only": True,
        **meta,
    }

    non_bypass = {
        "policy_id": "tts_speech_gate_non_bypass_policy_v1",
        "rules": list(SPEECH_GATE_NON_BYPASS_RULES),
        "rule_count": len(SPEECH_GATE_NON_BYPASS_RULES),
        "speech_gate_bypass_forbidden": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "tts_runtime_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "tts_runtime_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate tts_runtime_model_candidate",
            "generate sample speech_request_candidate intake",
            "generate sample audio_artifact_candidate contract",
            "verify provider readiness requirement",
            "verify voice model / voice profile / synthesis / playback / cache / authorization / failure / traceability boundaries",
            "no runtime enabled",
            "no provider import",
            "no audio generated",
        ],
        "post_dryrun_note": "after DryRun GO, prefer End-to-End Output Chain Simulation before real TTS",
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "tts_runtime_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "tts_runtime_layer_positioning": list(TTS_RUNTIME_LAYER_POSITIONING),
        "voice_output_plane_layer_positioning": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "main_chain_defined": [
            "Enforcement (Speech Gate → speech_gate_result_candidate)",
            "→ Execution (Voice Output Plane → speech_request_candidate)",
            "→ TTS Runtime (audio_artifact_candidate later)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "tts_runtime_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "speech_request_candidate_only_not_raw_clauses": True,
        "tts_runtime_is_execution_runtime_not_enforcement": True,
        "tts_runtime_layer_positioning": list(TTS_RUNTIME_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "controlled_provider_readiness_harness_required_later": True,
        "speech_gate_non_bypass_required": True,
        "planning_not_runtime": True,
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
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "tts_runtime_planning_policy": policy,
        "tts_runtime_roadmap_input_review": roadmap_input_review,
        "tts_runtime_module_definition": module_def,
        "speech_request_candidate_intake_contract": speech_request_intake,
        "tts_runtime_output_contract": output_contract,
        "tts_provider_abstraction_plan": provider_abstraction,
        "current_tts_provider_candidate_register": current_provider_candidate_register,
        "provider_switch_boundary_plan": provider_switch_boundary,
        "tts_provider_readiness_plan": provider_readiness,
        "tts_voice_model_boundary_plan": voice_model,
        "tts_voice_profile_personalization_boundary_plan": voice_profile,
        "tts_audio_synthesis_boundary_plan": synthesis_boundary,
        "tts_audio_output_playback_boundary_plan": playback_boundary,
        "tts_cache_and_artifact_boundary_plan": cache_boundary,
        "tts_authorization_requirement_plan": authorization,
        "tts_failure_route_plan": failure_routes,
        "tts_traceability_audit_plan": traceability,
        "tts_no_raw_constitution_policy": no_raw,
        "tts_speech_gate_non_bypass_policy": non_bypass,
        "tts_runtime_boundary_matrix": boundary_matrix,
        "tts_runtime_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "tts_runtime_planning_decision": planning_decision,
        "summary": summary,
    }
