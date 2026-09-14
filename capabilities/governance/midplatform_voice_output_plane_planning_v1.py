# -*- coding: utf-8 -*-
"""Midplatform Voice Output Plane Planning v1."""

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
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_DR_FINAL_GO,
)
from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    SPEECH_GATE_RESULT_FIELDS,
)
from capabilities.governance.midplatform_voice_output_plane_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    ROUTE_D,
    SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Voice-Output-Plane-Planning-v1-001"
SCOPE = "voice_output_plane_planning_only"
SOURCE_CHAIN = "midplatform_voice_output_plane_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_VOICE_OUTPUT_PLANE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_VOICE_OUTPUT_PLANE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Voice-Output-Plane-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Voice-Output-Plane-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "speech_gate_result_candidate → speech_request_candidate later → TTS later → audio output later"
)

VOICE_OUTPUT_PLANE_LAYER_POSITIONING: Tuple[str, ...] = (
    "Voice Output Plane is an execution layer module, not an enforcement layer module",
    "Voice Output Plane consumes speech_gate_result_candidate and emits speech_request_candidate later",
    "Speech Gate is enforcement; Voice Output Plane is execution",
    "Voice Output Plane does not read raw constitution clauses",
    "Voice Output Plane cannot override Speech Gate result",
    "TTS runtime is downstream execution, not Voice Output Plane planning now",
)

SPEECH_GATE_RESULT_INTAKE_FIELDS: Tuple[str, ...] = SPEECH_GATE_RESULT_FIELDS

SPEECH_REQUEST_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "speech_request_candidate_id",
    "source_speech_gate_result_candidate_ref",
    "speech_text_candidate",
    "speech_intent",
    "speech_priority",
    "speech_timing_constraints",
    "speech_tone_constraints",
    "speech_length_constraints",
    "required_disclosures",
    "uncertainty_surface_required",
    "forbidden_speech_actions",
    "tts_runtime_allowed",
    "audio_output_allowed",
    "interruption_allowed",
    "queue_mutation_allowed",
    "candidate_only",
    "user_facing_output_allowed",
)

EXECUTION_SCOPE_RULES: Tuple[str, ...] = (
    "Voice Output Plane is execution layer",
    "execution is later only",
    "planning may define speech_request_candidate contract",
    "current phase cannot generate speech_request",
    "current phase cannot invoke TTS",
    "current phase cannot output audio",
    "current phase cannot mutate audio queue",
)

TTS_RUNTIME_BOUNDARY_RULES: Tuple[str, ...] = (
    "TTS runtime requires separate authorization / runtime phase later",
    "speech_request_candidate ≠ TTS invocation",
    "TTS provider/model not invoked now",
    "no voice model selected now",
    "no audio synthesis now",
    "no streaming audio now",
)

AUDIO_OUTPUT_BOUNDARY_RULES: Tuple[str, ...] = (
    "audio_output_generated_now=false",
    "no speaker device access",
    "no audio playback",
    "no haptic/audio fallback",
    "no user-facing voice output",
)

VOICE_QUEUE_INTERRUPTION_RULES: Tuple[str, ...] = (
    "no audio queue mutation",
    "no interruption runtime",
    "no microphone runtime",
    "no ASR runtime",
    "no live user interruption handling",
    "interruption policy remains later-only",
    "future queue behavior must preserve Speech Gate constraints",
)

SPEECH_TIMING_PRIORITY_RULES: Tuple[str, ...] = (
    "urgent safety speech may receive priority later only",
    "hold/no_output must remain valid",
    "calm/slow tone constraint preserved",
    "short-form constraint preserved",
    "required_disclosures preserved",
    "no scheduling now",
)

SPEECH_CONTENT_RENDERING_RULES: Tuple[str, ...] = (
    "rendering cannot add unsupported facts",
    "rendering cannot remove uncertainty",
    "rendering cannot remove required disclosures",
    "rendering cannot weaken refusal/block/hold",
    "rendering cannot convert not_fact into fact",
    "rendering cannot expose privacy-sensitive content",
)

FAILURE_ROUTE_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"condition": "missing speech_gate_result", "route": "hold / no speech"},
    {"condition": "speech_request_forbidden", "route": "no speech"},
    {"condition": "TTS unavailable later", "route": "fallback/no_output/defer"},
    {"condition": "voice queue unavailable later", "route": "hold"},
    {"condition": "timing conflict later", "route": "hold/degrade"},
    {"condition": "forbidden action detected", "route": "block + violation candidate later"},
)

TRACEABILITY_REQUIREMENTS: Tuple[str, ...] = (
    "source_speech_gate_result_candidate_ref preserved",
    "source_enforcement_result_candidate_ref preserved",
    "source_user_output_candidate_ref preserved",
    "applicable_rule_refs preserved",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "whitebox_trace_refs preserved",
    "speech_request rationale auditable later",
)

NO_RAW_CONSTITUTION_RULES: Tuple[str, ...] = (
    "Voice Output Plane does not read raw constitution",
    "Voice Output Plane does not consume constraint_bundle directly unless through enforcement result refs",
    "Voice Output Plane consumes speech_gate_result_candidate",
    "applicable_rule_refs are trace refs only",
    "constitution changes should propagate via Resolver → bundle → gates → result, not direct execution rewrite",
)

SPEECH_GATE_NON_BYPASS_RULES: Tuple[str, ...] = (
    "Voice Output Plane cannot generate speech_request without speech_gate_result_candidate",
    "Voice Output Plane cannot override speech_gate_action",
    "blocked/hold/no_output speech result blocks speech_request",
    "degraded constraints must be preserved",
    "required disclosures must be preserved",
    "forbidden speech actions must be preserved",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "voice_output_plane_runtime_enabled_now",
    "voice_output_plane_invoked_now",
    "speech_request_generated_now",
    "speech_request_candidate_generated_now",
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

NON_CLAIMS: Tuple[str, ...] = (
    "Voice Output Plane Planning GO ≠ Voice Output runtime enabled",
    "speech_request_candidate contract ≠ speech_request generated",
    "speech_request_candidate ≠ TTS invocation",
    "TTS boundary planned ≠ audio output allowed",
    "Display Gate deferred ≠ skipped",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("voice_output_plane_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_voice_output_plane_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "template_id": TEMPLATE_ID,
        "core_chain_boundary": CORE_CHAIN_BOUNDARY,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "display_gate_deferred_not_skipped": True,
        "direct_tts_runtime_route_blocked": True,
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


def _voice_output_plane_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "voice_output_plane_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_voice_output_plane_v1",
            "module_type": "midplatform_voice_execution_plane_module",
            "role": "speech_gate_result_to_speech_request_candidate_execution_planning",
            "system_layer": "Output",
            "architectural_layer": "Execution",
            "layer_positioning": (
                "Voice Output Plane is an execution layer module, not an enforcement layer module"
            ),
        },
        "upstream_sources": {
            "upstream_modules": ["midplatform_speech_gate_v1"],
            "upstream_object_types": [
                "speech_gate_result_candidate",
                "required_disclosures",
                "required_uncertainty_surface",
                "required_tone_constraints",
                "required_timing_constraints",
                "forbidden_speech_actions",
            ],
            "required_inputs": list(SPEECH_GATE_RESULT_INTAKE_FIELDS),
            "optional_inputs": ["channel_preferences", "risk_flags"],
            "forbidden_inputs": [
                "raw_constitution_clauses",
                "constraint_bundle_direct",
                "constitution_publish_directive",
                "tts_directive",
                "audio_output_directive",
                "memory_write_directive",
                "speech_gate_bypass_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "tts_runtime_later",
                "audio_output_later",
                "voice_queue_later",
            ],
            "downstream_object_types": ["speech_request_candidate"],
            "allowed_outputs": ["speech_request_candidate"],
            "forbidden_outputs": [
                "tts_audio",
                "audio_output",
                "user_facing_speech",
                "speech_request",
                "memory_fact",
            ],
        },
        "input_contract": {
            "input_contract": "speech_gate_result_intake_contract_v1",
            "source_chain": "preserved_from_speech_gate_result",
            "evidence_ref": "preserved",
            "ttl": "required_from_speech_gate_result",
            "confidence": "preserved_as_uncertainty_surface",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": (
                "consume speech_gate_result_candidate later; plan speech_request_candidate "
                "generation with TTS/audio/queue boundaries"
            ),
            "allowed_transformation": [
                "plan speech_request_candidate contract from speech_gate_result",
                "preserve tone/timing/length/disclosure constraints",
                "plan TTS runtime preconditions",
                "plan audio output preconditions",
                "preserve refs and traceability",
            ],
            "forbidden_transformation": [
                "read raw constitution clauses",
                "re-interpret safety rules",
                "override Speech Gate result",
                "bypass Speech Gate",
                "invoke TTS runtime",
                "generate audio output",
                "enable microphone/ASR",
                "write memory or world model",
                "commit task_state",
                "invoke provider or model runtime",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "speech_request_candidate_contract_v1",
            "output_object_type": "speech_request_candidate",
            "decision_refs": "source_speech_gate_result_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_intake",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING) + [
                "speech_request_candidate ≠ TTS ≠ audio output",
            ],
            "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
            "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
            "priority_policy": "Speech Gate constraints override execution preferences",
            "conflict_policy": "forbidden_speech_actions from speech_gate_result enforced",
            "fallback_policy": "hold/no_output when speech_request not allowed",
            "rollback_policy": "execution planner does not commit state or emit audio",
        },
        "external_constraints": {
            "constitution_constraints": "via speech_gate_result refs only; no raw clause binding",
            "domain_standard_constraints": "preserved from speech_gate_result refs",
            "validation_gate_constraints": "validation_refs consumed not re-executed",
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
            "escalation_path": "escalation_required from speech_gate_result preserved",
            "audit_required": True,
        },
    }


def run_midplatform_voice_output_plane_planning_v1(
    *,
    midplatform_voice_output_plane_roadmap_decision_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_planning_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(midplatform_voice_output_plane_roadmap_decision_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    speech_plan_root = Path(midplatform_speech_gate_planning_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    blocked_register = _try_read_json(roadmap_root / "deferred_routes_register_v1.json") or {}
    speech_dr_sm = _try_read_json(speech_dr_root / "summary.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    closure = _try_read_json(speech_dr_root / "speech_gate_closure_decision_v1.json") or {}
    sample_speech_result = _try_read_json(
        speech_dr_root / "sample_speech_gate_result_candidate_v1.json"
    ) or {}
    speech_plan_policy = _try_read_json(speech_plan_root / "speech_gate_planning_policy_v1.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_speech_gate_planning_root": str(speech_plan_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("Voice Output Plane Roadmap Decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A — Voice Output Plane Planning")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview verifier must be GO")
    if closure.get("speech_enforcement_layer_validated") is not True:
        blockers.append("speech_enforcement_layer_validated must be true")
    if speech_plan_policy.get("speech_gate_is_enforcement_not_execution") is not True:
        blockers.append("Speech Gate must be enforcement layer")
    if not sample_speech_result.get("speech_gate_result_candidate_id"):
        blockers.append("sample speech_gate_result_candidate must exist")
    if speech_dr_sm.get("final_decision") != SPEECH_DR_FINAL_GO:
        blockers.append("speech gate dryrun must be closed for voice output plane roadmap")
    blocked_paths = [
        x.get("route")
        for x in (blocked_register.get("blocked_routes") or [])
        if x.get("status") == "blocked"
    ]
    if ROUTE_D not in blocked_paths:
        blockers.append("Direct TTS Runtime route must be blocked")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    module_def = _voice_output_plane_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    roadmap_input_review = {
        "review_id": "voice_output_plane_roadmap_input_review_v1",
        "roadmap_verifier": roadmap_vr.get("verifier"),
        "roadmap_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "speech_gate_dryrun_verifier": speech_dr_vr.get("verifier"),
        "speech_enforcement_layer_validated": closure.get("speech_enforcement_layer_validated") is True,
        "speech_gate_result_exists": bool(sample_speech_result.get("speech_gate_result_candidate_id")),
        "voice_output_plane_is_execution_layer": True,
        "speech_gate_is_enforcement_layer": True,
        "direct_tts_route_blocked": ROUTE_D in blocked_paths,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    speech_gate_intake = {
        "contract_id": "speech_gate_result_intake_contract_v1",
        "required_fields": list(SPEECH_GATE_RESULT_INTAKE_FIELDS),
        "consumes_speech_gate_result_only": True,
        "raw_constitution_clause_binding_forbidden": True,
        "speech_gate_bypass_forbidden": True,
        "candidate_only": True,
        **meta,
    }

    speech_request_contract = {
        "contract_id": "speech_request_candidate_contract_v1",
        "output_type": "speech_request_candidate",
        "required_fields": list(SPEECH_REQUEST_CANDIDATE_FIELDS),
        "defaults": {
            "tts_runtime_allowed": False,
            "audio_output_allowed": False,
            "interruption_allowed": False,
            "queue_mutation_allowed": False,
            "candidate_only": True,
            "user_facing_output_allowed": False,
        },
        "not_tts_or_audio_output": True,
        **meta,
    }

    execution_scope = {
        "plan_id": "voice_output_execution_scope_plan_v1",
        "rules": list(EXECUTION_SCOPE_RULES),
        "rule_count": len(EXECUTION_SCOPE_RULES),
        "execution_layer_not_enforcement": True,
        **meta,
    }

    tts_boundary = {
        "plan_id": "tts_runtime_boundary_plan_v1",
        "rules": list(TTS_RUNTIME_BOUNDARY_RULES),
        "rule_count": len(TTS_RUNTIME_BOUNDARY_RULES),
        **meta,
    }

    audio_boundary = {
        "plan_id": "audio_output_boundary_plan_v1",
        "rules": list(AUDIO_OUTPUT_BOUNDARY_RULES),
        "rule_count": len(AUDIO_OUTPUT_BOUNDARY_RULES),
        **meta,
    }

    queue_interruption = {
        "plan_id": "voice_queue_and_interruption_boundary_plan_v1",
        "rules": list(VOICE_QUEUE_INTERRUPTION_RULES),
        "rule_count": len(VOICE_QUEUE_INTERRUPTION_RULES),
        **meta,
    }

    timing_priority = {
        "plan_id": "speech_timing_and_priority_plan_v1",
        "rules": list(SPEECH_TIMING_PRIORITY_RULES),
        "rule_count": len(SPEECH_TIMING_PRIORITY_RULES),
        **meta,
    }

    content_rendering = {
        "plan_id": "speech_content_rendering_boundary_plan_v1",
        "rules": list(SPEECH_CONTENT_RENDERING_RULES),
        "rule_count": len(SPEECH_CONTENT_RENDERING_RULES),
        **meta,
    }

    failure_routes = {
        "plan_id": "voice_output_failure_route_plan_v1",
        "routes": list(FAILURE_ROUTE_MAPPINGS),
        "route_count": len(FAILURE_ROUTE_MAPPINGS),
        **meta,
    }

    traceability = {
        "plan_id": "voice_output_traceability_plan_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        "requirement_count": len(TRACEABILITY_REQUIREMENTS),
        **meta,
    }

    no_raw = {
        "policy_id": "voice_output_no_raw_constitution_policy_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "rule_count": len(NO_RAW_CONSTITUTION_RULES),
        "consumes_speech_gate_result_only": True,
        **meta,
    }

    non_bypass = {
        "policy_id": "voice_output_speech_gate_non_bypass_policy_v1",
        "rules": list(SPEECH_GATE_NON_BYPASS_RULES),
        "rule_count": len(SPEECH_GATE_NON_BYPASS_RULES),
        "speech_gate_bypass_forbidden": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "voice_output_plane_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "voice_output_plane_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate voice_output_plane_model_candidate",
            "generate sample speech_gate_result intake",
            "generate sample speech_request_candidate",
            "verify execution layer identity",
            "verify no raw constitution binding",
            "verify no Speech Gate bypass",
            "verify speech_request_candidate ≠ TTS / audio output",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "voice_output_plane_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "voice_output_plane_layer_positioning": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "main_chain_defined": [
            "Rule Source → Rule Resolution (constraint_bundle)",
            "→ Enforcement (Safety Gate → Speech Gate → speech_gate_result_candidate)",
            "→ Execution (Voice Output Plane → speech_request_candidate later → TTS later)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "voice_output_plane_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "speech_gate_result_only_not_raw_clauses": True,
        "voice_output_plane_is_execution_not_enforcement": True,
        "voice_output_plane_layer_positioning": list(VOICE_OUTPUT_PLANE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
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
        "voice_output_plane_planning_policy": policy,
        "voice_output_plane_roadmap_input_review": roadmap_input_review,
        "voice_output_plane_module_definition": module_def,
        "speech_gate_result_intake_contract": speech_gate_intake,
        "speech_request_candidate_contract": speech_request_contract,
        "voice_output_execution_scope_plan": execution_scope,
        "tts_runtime_boundary_plan": tts_boundary,
        "audio_output_boundary_plan": audio_boundary,
        "voice_queue_and_interruption_boundary_plan": queue_interruption,
        "speech_timing_and_priority_plan": timing_priority,
        "speech_content_rendering_boundary_plan": content_rendering,
        "voice_output_failure_route_plan": failure_routes,
        "voice_output_traceability_plan": traceability,
        "voice_output_no_raw_constitution_policy": no_raw,
        "voice_output_speech_gate_non_bypass_policy": non_bypass,
        "voice_output_plane_boundary_matrix": boundary_matrix,
        "voice_output_plane_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "voice_output_plane_planning_decision": planning_decision,
        "summary": summary,
    }
