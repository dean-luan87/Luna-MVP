# -*- coding: utf-8 -*-
"""Midplatform Speech Gate Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    USER_OUTPUT_CANDIDATE_FIELDS,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_DR_FINAL_GO,
    NEXT_PHASE_GO as SAFETY_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_speech_display_gate_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Speech-Gate-Planning-v1-001"
SCOPE = "speech_gate_planning_only"
SOURCE_CHAIN = "midplatform_speech_gate_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE
UPSTREAM_SAFETY_DR_FINAL = SAFETY_DR_FINAL_GO
UPSTREAM_SAFETY_DR_NEXT = SAFETY_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_SPEECH_GATE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_SPEECH_GATE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Speech-Gate-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Speech-Gate-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "speech_gate_result_candidate ≠ speech_request ≠ TTS ≠ audio output ≠ user-facing speech"
)

SPEECH_GATE_LAYER_POSITIONING: Tuple[str, ...] = (
    "Speech Gate is an enforcement layer module, not an execution layer module",
    "Speech Gate consumes enforcement_result_candidate and emits speech_gate_result_candidate",
    "Voice Output Plane / TTS are execution layer; they consume speech_gate_result_candidate later",
    "Speech Gate does not read raw constitution clauses",
    "enforcement_result_candidate flows Safety Gate → Speech Gate → Voice Output Plane later",
)

ENFORCEMENT_RESULT_INTAKE_FIELDS: Tuple[str, ...] = (
    "enforcement_result_candidate_id",
    "source_safety_gate_result_ref",
    "source_user_output_candidate_ref",
    "safety_action",
    "safety_status",
    "allowed_downstream_gates",
    "blocked_downstream_gates",
    "required_disclosures",
    "forbidden_actions",
    "required_degradation",
    "required_hold_reason",
    "refusal_reason",
    "escalation_required",
    "rationale_refs",
    "evidence_refs",
    "applicable_rule_refs",
    "whitebox_trace_refs",
    "candidate_only",
)

USER_OUTPUT_INTAKE_FIELDS: Tuple[str, ...] = USER_OUTPUT_CANDIDATE_FIELDS

SPEECH_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "speech_gate_result_candidate_id",
    "source_enforcement_result_candidate_ref",
    "source_user_output_candidate_ref",
    "speech_gate_action",
    "speech_gate_status",
    "speech_channel_allowed",
    "speech_request_allowed",
    "required_disclosures",
    "required_uncertainty_surface",
    "required_tone_constraints",
    "required_timing_constraints",
    "required_length_constraints",
    "forbidden_speech_actions",
    "refusal_reason",
    "hold_reason",
    "degradation_reason",
    "escalation_required",
    "rationale_refs",
    "evidence_refs",
    "applicable_rule_refs",
    "whitebox_trace_refs",
    "candidate_only",
)

SPEECH_ACTION_TAXONOMY: Tuple[str, ...] = (
    "speech_allow_candidate_forward",
    "speech_block_candidate",
    "speech_hold_candidate",
    "speech_degrade_candidate",
    "speech_require_disclosure",
    "speech_require_uncertainty_surface",
    "speech_require_short_form",
    "speech_require_slow_or_calm_tone_later",
    "speech_no_output_candidate",
    "speech_request_more_evidence",
    "speech_request_reobserve",
    "speech_escalate_to_owner_later",
    "speech_emit_violation_report_candidate",
)

CHANNEL_ADMISSION_RULES: Tuple[str, ...] = (
    "speech channel must be allowed by enforcement_result_candidate",
    "blocked_downstream_gates containing speech_gate blocks speech path",
    "forbidden_actions containing speech_output blocks speech path",
    "no_output_candidate can override speech preference",
    "speech channel preference cannot override safety result",
    "speech channel candidate does not execute speech",
)

CONTENT_CONSTRAINT_RULES: Tuple[str, ...] = (
    "speech payload candidate must preserve required disclosures",
    "speech must preserve uncertainty if required",
    "speech must not present not_fact as fact",
    "speech must not remove safety warning",
    "speech must not expose privacy-sensitive content",
    "speech must not expand beyond validated content",
    "speech must not add unsupported facts",
)

UNCERTAINTY_DISCLOSURE_RULES: Tuple[str, ...] = (
    "uncertainty_level preserved",
    "required_disclosures preserved",
    "low confidence requires uncertainty surface or hold",
    "missing evidence requires hold / evidence request",
    "conflicting evidence requires hold / explanation later",
    "urgent safety warning can be prioritized later but not spoken now",
)

TONE_PERSONALIZATION_RULES: Tuple[str, ...] = (
    "personalization may shape tone later",
    "personalization cannot override safety / disclosure / uncertainty / privacy",
    "emotional tone must not distort facts",
    "calm/slow tone requirement may be attached later",
    "no user profile update",
    "no personal memory write",
)

INTERRUPTION_TIMING_RULES: Tuple[str, ...] = (
    "speech timing constraints may be attached later",
    "interruption policy later only",
    "no runtime interruption behavior now",
    "no audio queue mutation now",
    "no live microphone / ASR behavior now",
    "no TTS scheduling now",
)

REFUSAL_HOLD_DEGRADE_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"safety_signal": "safety_block", "speech_path": "speech_no_output_candidate or refusal_candidate later"},
    {"safety_signal": "safety_hold", "speech_path": "speech_hold_candidate later"},
    {"safety_signal": "safety_degrade", "speech_path": "speech_degrade_candidate later"},
    {"safety_signal": "require_disclosure", "speech_path": "attach disclosure requirement"},
    {"safety_signal": "request_more_evidence", "speech_path": "speech evidence request candidate later"},
    {"safety_signal": "severe_violation", "speech_path": "no speech + escalation later"},
)

DOWNSTREAM_HANDOFF_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"speech_action": "speech_allow_candidate_forward", "handoff": "Voice Output Plane planning later"},
    {"speech_action": "speech_block_candidate", "handoff": "no_output/refusal path later"},
    {"speech_action": "speech_hold_candidate", "handoff": "hold/no_output path later"},
    {"speech_action": "speech_degrade_candidate", "handoff": "degraded voice output candidate later"},
    {"speech_action": "speech_request_more_evidence", "handoff": "clarification/evidence path later"},
    {"speech_action": "speech_escalate_to_owner_later", "handoff": "owner escalation path later"},
)

NO_RAW_CONSTITUTION_RULES: Tuple[str, ...] = (
    "speech gate does not bind raw constitution clauses",
    "speech gate consumes enforcement_result_candidate / constraint-derived result",
    "constitution changes update Resolver / constraint_bundle / Safety Gate result, not Speech Gate",
    "breaking result schema change requires compatibility phase",
    "ordinary constitution amendment should not rewrite Speech Gate",
    "all rule refs retained for Whitebox audit",
)

EXECUTION_LAYER_BOUNDARY_RULES: Tuple[str, ...] = (
    "Speech Gate pass ≠ speech_request",
    "Speech Gate pass ≠ TTS",
    "Speech Gate pass ≠ audio output",
    "Voice Output Plane required separately",
    "TTS runtime required separately",
    "execution layer cannot override speech_gate_result_candidate",
    "execution layer cannot read raw constitution",
)

TRACEABILITY_REQUIREMENTS: Tuple[str, ...] = (
    "source_chain preserved",
    "source_enforcement_result_candidate_ref preserved",
    "source_user_output_candidate_ref preserved",
    "applicable_rule_refs preserved",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "whitebox_trace_refs preserved",
    "speech action reason preserved",
    "speech block/hold/degrade reason auditable",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "speech_gate_runtime_enabled_now",
    "speech_gate_invoked_now",
    "speech_gate_result_generated_now",
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
    "raw_constitution_clause_bound_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Speech Gate Planning GO ≠ Speech Gate runtime enabled",
    "Speech Gate planned ≠ speech_request generated",
    "Speech allow candidate planned ≠ TTS allowed",
    "Voice Output Plane later ≠ voice output now",
    "Display Gate deferred ≠ skipped",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("speech_gate_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_planning"
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


def _speech_gate_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "speech_gate_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_speech_gate_v1",
            "module_type": "midplatform_user_output_gate_module",
            "role": "speech_output_enforcement_gate",
            "system_layer": "Validation",
            "architectural_layer": "Enforcement",
            "layer_positioning": (
                "Speech Gate is an enforcement layer module, not an execution layer module"
            ),
        },
        "upstream_sources": {
            "upstream_modules": [
                "safety_gate",
                "output_plane_integration",
                "constitution_resolver",
            ],
            "upstream_object_types": [
                "enforcement_result_candidate",
                "user_output_candidate",
                "channel_constraints",
                "required_disclosures",
                "uncertainty_policy",
                "forbidden_actions",
                "tone_personalization_limits",
            ],
            "required_inputs": list(ENFORCEMENT_RESULT_INTAKE_FIELDS) + list(USER_OUTPUT_INTAKE_FIELDS),
            "optional_inputs": ["risk_flags", "channel_preferences"],
            "forbidden_inputs": [
                "raw_constitution_clauses",
                "constitution_publish_directive",
                "speech_request_directive",
                "tts_directive",
                "voice_output_plane_directive",
                "memory_write_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "voice_output_plane_later",
                "no_output_handler_later",
                "display_gate_later",
            ],
            "downstream_enforcement_only": False,
            "execution_layer_handoff_later": [
                "voice_output_plane_later",
            ],
            "enforcement_layer_deferred": [
                "display_gate_later",
            ],
            "downstream_object_types": ["speech_gate_result_candidate"],
            "allowed_outputs": ["speech_gate_result_candidate"],
            "forbidden_outputs": [
                "speech_request",
                "tts_audio",
                "user_facing_speech",
                "audio_output",
                "display_output",
                "memory_fact",
            ],
        },
        "input_contract": {
            "input_contract": "speech_gate_enforcement_result_intake_contract_v1",
            "source_chain": "preserved_from_enforcement_result_and_user_output",
            "evidence_ref": "preserved",
            "ttl": "required_from_enforcement_result",
            "confidence": "preserved_as_uncertainty_level",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": (
                "enforce speech output constraints from enforcement_result_candidate + "
                "user_output_candidate; emit speech_gate_result_candidate for Voice Output Plane later"
            ),
            "allowed_transformation": [
                "check speech channel admission from enforcement result",
                "apply content/tone/timing/uncertainty constraints",
                "select speech_gate_action from taxonomy",
                "emit allow/block/hold/degrade/require_disclosure/no_output speech gate result",
                "preserve refs and traceability",
            ],
            "forbidden_transformation": [
                "bind raw constitution clauses",
                "generate speech_request",
                "invoke TTS or Voice Output Plane",
                "generate audio output",
                "execute interruption runtime",
                "write memory or world model",
                "commit task_state",
                "invoke provider or model runtime",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "speech_gate_result_candidate_contract_v1",
            "output_object_type": "speech_gate_result_candidate",
            "execution_layer_consumes_speech_gate_result": True,
            "decision_refs": "source_enforcement_result_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_intake",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": list(SPEECH_GATE_LAYER_POSITIONING) + [
                "speech_gate_result_candidate ≠ speech_request ≠ TTS",
            ],
            "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
            "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
            "priority_policy": "safety enforcement result overrides speech channel preference",
            "conflict_policy": "forbidden_actions from enforcement result enforced",
            "fallback_policy": "safety block/hold → speech_no_output or hold",
            "rollback_policy": "enforcer does not commit state or execute speech output",
        },
        "external_constraints": {
            "constitution_constraints": "via enforcement_result_candidate only; no raw clause binding",
            "domain_standard_constraints": "preserved from enforcement result refs",
            "validation_gate_constraints": "validation_refs consumed not re-executed",
            "health_signal_constraints": "risk context optional",
            "whitebox_visibility_constraints": "applicable_rule_refs and trace refs preserved",
            "decision_center_constraints": "does not re-decide upstream safety decisions",
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
            "failure_route": "block/hold/degrade/no_output/escalation per speech_gate_action",
            "issue_trace": "whitebox_trace_refs preserved",
            "violation_report": "speech_emit_violation_report_candidate path",
            "escalation_path": "owner later; no invoke now",
            "audit_required": True,
        },
    }


def run_midplatform_speech_gate_planning_v1(
    *,
    midplatform_speech_display_gate_roadmap_decision_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_planning_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(midplatform_speech_display_gate_roadmap_decision_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    safety_plan_root = Path(midplatform_safety_gate_planning_root).expanduser().resolve()
    uo_dr_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    safety_dr_sm = _try_read_json(safety_dr_root / "summary.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    safety_model = _try_read_json(safety_dr_root / "safety_gate_model_candidate_v1.json") or {}
    safety_plan_policy = _try_read_json(safety_plan_root / "safety_gate_planning_policy_v1.json") or {}
    sample_user_output = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    output_dr_vr = _try_read_json(output_dr_root / "verifier_report.json") or {}
    uo_dr_vr = _try_read_json(uo_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_safety_gate_planning_root": str(safety_plan_root),
        "upstream_user_output_constitution_dryrun_root": str(uo_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("Speech Display Gate Roadmap Decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap decision final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap decision recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A — Speech Gate First")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview verifier must be GO")
    if safety_dr_sm.get("final_decision") != UPSTREAM_SAFETY_DR_FINAL:
        blockers.append("safety gate dryrun final_decision mismatch")
    if safety_model.get("emits_enforcement_result_candidate") is not True:
        blockers.append("Safety Gate must emit enforcement_result_candidate")
    if safety_plan_policy.get("safety_gate_is_enforcement_not_execution") is not True:
        blockers.append("Safety Gate must be enforcement layer not execution")
    if not sample_user_output.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if output_dr_vr.get("verifier") != "GO":
        blockers.append("Output Plane DryRunAndReview must be GO")
    if uo_dr_vr.get("verifier") != "GO":
        blockers.append("User Output Constitution DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    module_def = _speech_gate_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    roadmap_input_review = {
        "review_id": "speech_display_roadmap_input_review_v1",
        "roadmap_decision_verifier": roadmap_vr.get("verifier"),
        "roadmap_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "safety_gate_dryrun_verifier": safety_dr_vr.get("verifier"),
        "safety_gate_emits_enforcement_result": safety_model.get("emits_enforcement_result_candidate") is True,
        "speech_gate_is_enforcement_layer": True,
        "voice_output_plane_is_execution_layer": True,
        "execution_consumes_enforcement_result_later": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    enforcement_intake = {
        "contract_id": "speech_gate_enforcement_result_intake_contract_v1",
        "required_fields": list(ENFORCEMENT_RESULT_INTAKE_FIELDS),
        "consumes_enforcement_result_only": True,
        "raw_constitution_clause_binding_forbidden": True,
        "applicable_rule_refs_are_trace_refs": True,
        "enforcement_result_version_required": True,
        "enforcement_result_ttl_required": True,
        "enforcement_result_source_refs_preserved": True,
        "candidate_only": True,
        **meta,
    }

    user_output_intake = {
        "contract_id": "speech_gate_user_output_candidate_intake_contract_v1",
        "required_fields": list(USER_OUTPUT_INTAKE_FIELDS),
        "defaults": {
            "user_facing_output_allowed": False,
            "speech_request_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
        },
        **meta,
    }

    result_contract = {
        "contract_id": "speech_gate_result_candidate_contract_v1",
        "output_type": "speech_gate_result_candidate",
        "required_fields": list(SPEECH_GATE_RESULT_FIELDS),
        "speech_gate_semantics": {
            "allow": "speech_allow_candidate_forward",
            "block": "speech_block_candidate",
            "hold": "speech_hold_candidate",
            "degrade": "speech_degrade_candidate",
            "require_disclosure": "speech_require_disclosure",
            "no_output": "speech_no_output_candidate",
        },
        "execution_layer_reads": [
            "speech_channel_allowed",
            "required_disclosures",
            "required_uncertainty_surface",
            "required_tone_constraints",
            "required_timing_constraints",
            "forbidden_speech_actions",
            "applicable_rule_refs",
        ],
        "defaults": {
            "candidate_only": True,
            "speech_request_allowed": False,
        },
        "not_execution_output": True,
        **meta,
    }

    action_taxonomy = {
        "taxonomy_id": "speech_gate_action_taxonomy_v1",
        "actions": list(SPEECH_ACTION_TAXONOMY),
        "action_count": len(SPEECH_ACTION_TAXONOMY),
        **meta,
    }

    channel_admission = {
        "plan_id": "speech_channel_admission_rule_plan_v1",
        "rules": list(CHANNEL_ADMISSION_RULES),
        "rule_count": len(CHANNEL_ADMISSION_RULES),
        **meta,
    }

    content_constraint = {
        "plan_id": "speech_content_constraint_rule_plan_v1",
        "rules": list(CONTENT_CONSTRAINT_RULES),
        "rule_count": len(CONTENT_CONSTRAINT_RULES),
        **meta,
    }

    uncertainty_disclosure = {
        "plan_id": "speech_uncertainty_disclosure_rule_plan_v1",
        "rules": list(UNCERTAINTY_DISCLOSURE_RULES),
        "rule_count": len(UNCERTAINTY_DISCLOSURE_RULES),
        **meta,
    }

    tone_personalization = {
        "plan_id": "speech_tone_personalization_boundary_plan_v1",
        "rules": list(TONE_PERSONALIZATION_RULES),
        "rule_count": len(TONE_PERSONALIZATION_RULES),
        **meta,
    }

    interruption_timing = {
        "plan_id": "speech_interruption_and_timing_boundary_plan_v1",
        "rules": list(INTERRUPTION_TIMING_RULES),
        "rule_count": len(INTERRUPTION_TIMING_RULES),
        **meta,
    }

    refusal_hold_degrade = {
        "plan_id": "speech_safety_refusal_hold_degrade_plan_v1",
        "mappings": list(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        "mapping_count": len(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        **meta,
    }

    downstream_handoff = {
        "plan_id": "speech_gate_downstream_handoff_plan_v1",
        "handoffs": list(DOWNSTREAM_HANDOFF_MAPPINGS),
        "handoff_count": len(DOWNSTREAM_HANDOFF_MAPPINGS),
        "speech_gate_enforcement_voice_plane_execution": True,
        "display_gate_deferred_not_skipped": True,
        "no_downstream_runtime_invoked_now": True,
        **meta,
    }

    no_raw_binding = {
        "policy_id": "speech_gate_no_raw_constitution_binding_policy_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "rule_count": len(NO_RAW_CONSTITUTION_RULES),
        "consumes_enforcement_result_only": True,
        **meta,
    }

    execution_boundary = {
        "plan_id": "speech_gate_execution_layer_boundary_plan_v1",
        "rules": list(EXECUTION_LAYER_BOUNDARY_RULES),
        "rule_count": len(EXECUTION_LAYER_BOUNDARY_RULES),
        "speech_pass_not_speech_request_or_tts": True,
        **meta,
    }

    traceability = {
        "plan_id": "speech_gate_traceability_plan_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        "requirement_count": len(TRACEABILITY_REQUIREMENTS),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "speech_gate_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "speech_gate_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate speech_gate_model_candidate",
            "generate sample enforcement_result intake",
            "generate sample user_output_candidate intake",
            "generate sample speech_gate_result_candidate",
            "verify speech gate as Enforcement Layer",
            "verify no raw constitution binding",
            "verify speech pass ≠ speech_request/TTS/audio",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "speech_gate_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "speech_gate_layer_positioning": list(SPEECH_GATE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "main_chain_defined": [
            "Rule Source (constitutions / standards / rules)",
            "→ Rule Resolution (Constitution Resolver → constraint_bundle)",
            "→ Enforcement (Safety Gate → Speech Gate → Display Gate …)",
            "→ Execution (Voice Output Plane / Display Output / TTS …)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "speech_gate_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "enforcement_result_only_not_raw_clauses": True,
        "speech_gate_is_enforcement_not_execution": True,
        "speech_gate_layer_positioning": list(SPEECH_GATE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "execution_consumes_speech_gate_result_later": True,
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
        "speech_gate_planning_policy": policy,
        "speech_display_roadmap_input_review": roadmap_input_review,
        "speech_gate_module_definition": module_def,
        "speech_gate_enforcement_result_intake_contract": enforcement_intake,
        "speech_gate_user_output_candidate_intake_contract": user_output_intake,
        "speech_gate_result_candidate_contract": result_contract,
        "speech_gate_action_taxonomy": action_taxonomy,
        "speech_channel_admission_rule_plan": channel_admission,
        "speech_content_constraint_rule_plan": content_constraint,
        "speech_uncertainty_disclosure_rule_plan": uncertainty_disclosure,
        "speech_tone_personalization_boundary_plan": tone_personalization,
        "speech_interruption_and_timing_boundary_plan": interruption_timing,
        "speech_safety_refusal_hold_degrade_plan": refusal_hold_degrade,
        "speech_gate_downstream_handoff_plan": downstream_handoff,
        "speech_gate_no_raw_constitution_binding_policy": no_raw_binding,
        "speech_gate_execution_layer_boundary_plan": execution_boundary,
        "speech_gate_traceability_plan": traceability,
        "speech_gate_boundary_matrix": boundary_matrix,
        "speech_gate_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "speech_gate_planning_decision": planning_decision,
        "summary": summary,
    }
