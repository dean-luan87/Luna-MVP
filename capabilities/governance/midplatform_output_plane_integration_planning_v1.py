# -*- coding: utf-8 -*-
"""Midplatform Output Plane Integration Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_planning_v1 import (
    FINAL_DECISION_GO as TEMPLATE_PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_task_response_candidate_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TASK_RESP_DR_FINAL_GO,
    NEXT_PHASE_GO as TASK_RESP_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_task_response_candidate_integration_planning_v1 import (
    TASK_RESPONSE_OUTPUT_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Output-Plane-Integration-Planning-v1-001"
SCOPE = "output_plane_integration_planning_only"
SOURCE_CHAIN = "midplatform_output_plane_integration_planning_v1"

UPSTREAM_TASK_RESP_DR_FINAL = TASK_RESP_DR_FINAL_GO
UPSTREAM_TASK_RESP_DR_NEXT = TASK_RESP_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_OUTPUT_PLANE_INTEGRATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_OUTPUT_PLANE_INTEGRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Output-Plane-Integration-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Output-Plane-Integration-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "task_response_candidate ≠ user_output_candidate ≠ speech_request ≠ TTS ≠ final broadcast/display"
)

TASK_RESPONSE_INTAKE_FIELDS: Tuple[str, ...] = TASK_RESPONSE_OUTPUT_FIELDS

USER_OUTPUT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "user_output_candidate_id",
    "source_task_response_candidate_ref",
    "output_type",
    "output_channel_candidate",
    "output_payload_candidate",
    "safety_refs",
    "constitution_refs",
    "evidence_refs",
    "rationale_refs",
    "uncertainty_level",
    "personalization_refs",
    "output_constraints",
    "user_facing_output_allowed",
    "speech_request_allowed",
    "display_output_allowed",
    "candidate_only",
    "fact_status",
)

OUTPUT_CHANNEL_TAXONOMY: Tuple[Dict[str, Any], ...] = (
    {
        "channel_id": "speech_output_candidate",
        "channel_type": "speech",
        "executes_now": False,
        "is_tts": False,
        "requires_speech_gate_later": True,
        "requires_voice_output_plane_later": True,
    },
    {
        "channel_id": "display_output_candidate",
        "channel_type": "display",
        "executes_now": False,
        "is_actual_display": False,
        "requires_display_output_later": True,
    },
    {
        "channel_id": "haptic_output_candidate_later",
        "channel_type": "haptic",
        "executes_now": False,
        "later_only": True,
    },
    {
        "channel_id": "app_notification_candidate_later",
        "channel_type": "notification",
        "executes_now": False,
        "later_only": True,
    },
    {
        "channel_id": "silent_state_update_candidate_later",
        "channel_type": "silent_state",
        "executes_now": False,
        "later_only": True,
    },
    {
        "channel_id": "no_output_candidate",
        "channel_type": "no_output",
        "executes_now": False,
        "valid_for_blocked_hold_safety": True,
    },
)

OUTPUT_ASSEMBLY_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {
        "task_response_type": "normal_task_response_candidate",
        "output_assembly": "user_output_candidate_later",
    },
    {
        "task_response_type": "block_response_candidate",
        "output_assembly": "no_output_or_block_notice_candidate_later",
    },
    {
        "task_response_type": "hold_response_candidate",
        "output_assembly": "hold_notice_candidate_later",
    },
    {
        "task_response_type": "evidence_request_response_candidate",
        "output_assembly": "clarification_or_evidence_request_output_candidate_later",
    },
    {
        "task_response_type": "validation_request_response_candidate",
        "output_assembly": "internal_hold_or_validation_notice_candidate_later",
    },
    {
        "task_response_type": "reobserve_response_candidate",
        "output_assembly": "reobserve_guidance_output_candidate_later",
    },
    {
        "task_response_type": "degraded_response_candidate",
        "output_assembly": "degraded_mode_notice_candidate_later",
    },
    {
        "task_response_type": "fallback_response_candidate",
        "output_assembly": "fallback_output_candidate_later",
    },
    {
        "task_response_type": "escalation_candidate",
        "output_assembly": "escalation_notice_candidate_later",
    },
    {
        "task_response_type": "violation_response_candidate",
        "output_assembly": "safety_or_violation_notice_candidate_later",
    },
    {
        "task_response_type": "reject_response_candidate",
        "output_assembly": "reject_output_candidate_later",
    },
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "output_plane_runtime_enabled_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "display_output_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Output Plane Planning GO ≠ user_output_candidate generated",
    "user_output_candidate contract ≠ user-facing output allowed",
    "speech channel planned ≠ TTS allowed",
    "display channel planned ≠ UI rendered",
    "next DryRunAndReview ≠ final output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("output_plane_integration_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "output_plane_runtime_enabled_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "display_output_invoked_now",
    "task_response_runtime_enabled_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "template_id": TEMPLATE_ID,
        "core_chain_boundary": CORE_CHAIN_BOUNDARY,
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


def _output_plane_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "output_plane_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_output_plane_integration_v1",
            "module_type": "midplatform_output_candidate_assembly_module",
            "role": "task_response_candidate_to_user_output_candidate_assembly",
            "system_layer": "Output",
        },
        "upstream_sources": {
            "upstream_modules": ["midplatform_task_response_candidate_integration_v1"],
            "upstream_object_types": [
                "task_response_candidate",
                "rationale_refs",
                "evidence_refs",
                "validation_refs",
                "health_refs",
                "constitution_refs",
                "whitebox_refs",
            ],
            "required_inputs": list(TASK_RESPONSE_INTAKE_FIELDS),
            "optional_inputs": ["personalization_refs"],
            "forbidden_inputs": [
                "speech_request_directive",
                "tts_directive",
                "display_render_directive",
                "memory_write_directive",
                "task_state_commit_directive",
                "provider_invocation_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "speech_gate_later",
                "voice_output_plane_later",
                "display_output_later",
                "user_output_constitution_later",
            ],
            "downstream_object_types": ["user_output_candidate"],
            "allowed_outputs": ["user_output_candidate"],
            "forbidden_outputs": [
                "user_facing_output",
                "speech_output",
                "display_output",
                "tts_audio",
                "memory_fact",
                "world_model_fact",
                "task_state_commit",
            ],
        },
        "input_contract": {
            "input_contract": "task_response_candidate_intake_contract_v1",
            "source_chain": "preserved_from_task_response_candidate",
            "evidence_ref": "preserved",
            "ttl": "preserved",
            "confidence": "preserved_as_uncertainty_level",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": "assemble user_output_candidate from task_response_candidate",
            "allowed_transformation": [
                "map response_type to output assembly rule",
                "select output_channel_candidate",
                "preserve refs and uncertainty",
                "bind constitution/safety constraints later",
            ],
            "forbidden_transformation": [
                "render display or UI",
                "invoke TTS or speech gate",
                "invoke voice output plane",
                "write memory or world model",
                "commit task state",
                "invoke provider or model runtime",
                "generate user-facing output now",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "user_output_candidate_contract_v1",
            "output_object_type": "user_output_candidate",
            "decision_refs": "source_task_response_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_upstream",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": [
                "task_response_candidate ≠ user_output_candidate",
                "user_output_candidate ≠ user-facing output",
                "output channel candidate ≠ channel execution",
                "assembly candidate-only; output not executed",
            ],
            "priority_policy": "safety/constitution/validation override personalization",
            "conflict_policy": "do not override task_response_candidate refs",
            "fallback_policy": "fallback response → fallback_output_candidate_later",
            "rollback_policy": "assembly does not commit state",
        },
        "external_constraints": {
            "constitution_constraints": "User Output Constitution required before user-facing output",
            "domain_standard_constraints": "preserved from task_response_candidate",
            "validation_gate_constraints": "validation refs preserved; unsafe content blocked later",
            "health_signal_constraints": "health refs preserved as context",
            "whitebox_visibility_constraints": "rationale refs preserved",
            "decision_center_constraints": "consume task_response_candidate only; do not re-decide",
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
            "failure_route": "blocked/hold/safety → no_output_candidate or notice candidate later",
            "issue_trace": "preserve upstream refs",
            "violation_report": "violation response → safety_or_violation_notice_candidate_later",
            "escalation_path": "escalation notice later; no Hive/owner notify now",
            "audit_required": True,
        },
    }


def run_midplatform_output_plane_integration_planning_v1(
    *,
    midplatform_task_response_candidate_integration_dryrun_and_review_root: str,
    midplatform_task_response_candidate_integration_planning_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    task_dr_root = Path(
        midplatform_task_response_candidate_integration_dryrun_and_review_root
    ).expanduser().resolve()
    task_plan_root = Path(
        midplatform_task_response_candidate_integration_planning_root
    ).expanduser().resolve()
    dc_dr_root = Path(
        midplatform_decision_center_module_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()
    constitution_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()

    task_dr_sm = _try_read_json(task_dr_root / "summary.json") or {}
    task_dr_vr = _try_read_json(task_dr_root / "verifier_report.json") or {}
    sample_task_resp = _try_read_json(task_dr_root / "sample_task_response_candidate_v1.json") or {}
    task_plan_vr = _try_read_json(task_plan_root / "verifier_report.json") or {}
    task_output_contract = (
        _try_read_json(task_plan_root / "task_response_candidate_output_contract_v1.json") or {}
    )
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}
    constitution_dr_vr = _try_read_json(constitution_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_task_response_dryrun_root": str(task_dr_root),
        "upstream_task_response_planning_root": str(task_plan_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_template_planning_root": str(template_root),
        "upstream_constitution_dryrun_root": str(constitution_dr_root),
        "output_root": str(out_root),
    }

    output_defaults = task_output_contract.get("defaults") or {}

    if task_dr_vr.get("verifier") != "GO":
        blockers.append("Task Response DryRunAndReview verifier must be GO")
    if task_dr_sm.get("final_decision") != UPSTREAM_TASK_RESP_DR_FINAL:
        blockers.append("task response dryrun final_decision mismatch")
    if task_dr_sm.get("recommended_next_phase") != UPSTREAM_TASK_RESP_DR_NEXT:
        blockers.append("task response dryrun recommended_next_phase mismatch")
    if not sample_task_resp.get("task_response_candidate_id"):
        blockers.append("sample task_response_candidate must exist")
    if sample_task_resp.get("user_output_allowed") is not False:
        blockers.append("sample task_response must have user_output_allowed=false")
    if sample_task_resp.get("speech_output_allowed") is not False:
        blockers.append("sample task_response must have speech_output_allowed=false")
    if sample_task_resp.get("memory_write_allowed") is not False:
        blockers.append("sample task_response must forbid memory write")
    if sample_task_resp.get("world_model_write_allowed") is not False:
        blockers.append("sample task_response must forbid world model write")
    if sample_task_resp.get("task_state_commit_allowed") is not False:
        blockers.append("sample task_response must forbid task state commit")
    if output_defaults.get("user_output_allowed") is not False:
        blockers.append("task_response defaults must forbid user_output")
    if output_defaults.get("speech_output_allowed") is not False:
        blockers.append("task_response defaults must forbid speech_output")
    if task_plan_vr.get("verifier") != "GO":
        blockers.append("Task Response Planning verifier must be GO")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")
    if constitution_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution Governance Explanation DryRunAndReview must be GO")

    module_def = _output_plane_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    upstream_review = {
        "review_id": "upstream_task_response_input_review_v1",
        "task_response_dryrun_verifier": task_dr_vr.get("verifier"),
        "task_response_dryrun_final": task_dr_sm.get("final_decision"),
        "sample_task_response_present": bool(sample_task_resp.get("task_response_candidate_id")),
        "task_response_not_user_output": True,
        "user_output_candidate_not_user_facing": True,
        "output_plane_not_speech_not_tts": True,
        "decision_center_dryrun_go": dc_dr_vr.get("verifier") == "GO",
        "constitution_dryrun_go": constitution_dr_vr.get("verifier") == "GO",
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    task_intake = {
        "contract_id": "task_response_candidate_intake_contract_v1",
        "required_fields": list(TASK_RESPONSE_INTAKE_FIELDS),
        "defaults": {
            "candidate_only": True,
            "fact_status": "not_fact",
            "user_output_allowed": False,
            "speech_output_allowed": False,
            "memory_write_allowed": False,
            "world_model_write_allowed": False,
            "task_state_commit_allowed": False,
        },
        "does_not_modify_task_response_candidate": True,
        **meta,
    }

    user_output_contract = {
        "contract_id": "user_output_candidate_contract_v1",
        "output_type": "user_output_candidate",
        "required_fields": list(USER_OUTPUT_CANDIDATE_FIELDS),
        "defaults": {
            "user_facing_output_allowed": False,
            "speech_request_allowed": False,
            "display_output_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
        },
        "not_user_facing_output": True,
        "not_speech_request": True,
        "not_display_output": True,
        **meta,
    }

    channel_taxonomy = {
        "taxonomy_id": "output_channel_taxonomy_v1",
        "channels": list(OUTPUT_CHANNEL_TAXONOMY),
        "channel_count": len(OUTPUT_CHANNEL_TAXONOMY),
        "channel_candidate_not_execution": True,
        "speech_output_candidate_not_tts": True,
        "display_output_candidate_not_actual_display": True,
        "no_output_candidate_valid_for_blocked_hold_safety": True,
        **meta,
    }

    constitution_binding = {
        "plan_id": "user_output_constitution_binding_plan_v1",
        "user_output_candidate_requires_constitution_later": True,
        "safety_privacy_fact_constraints_must_bind": True,
        "personalized_preference_cannot_override_constitution": True,
        "uncertainty_must_be_surfaced_if_required": True,
        "unsafe_or_unvalidated_cannot_become_user_facing": True,
        **meta,
    }

    safety_binding = {
        "plan_id": "safety_gate_binding_plan_v1",
        "safety_gate_required_before_user_facing_output": True,
        "safety_block_overrides_output_preference": True,
        "safety_hold_can_produce_no_output_candidate": True,
        "safety_warning_may_be_attached_later": True,
        "safety_gate_not_invoked_now": True,
        **meta,
    }

    speech_binding = {
        "plan_id": "speech_gate_binding_plan_v1",
        "speech_output_requires_speech_gate_later": True,
        "speech_output_requires_voice_output_plane_later": True,
        "tts_requires_separate_authorization_runtime": True,
        "speech_request_generated_now": False,
        "speech_gate_invoked_now": False,
        "tts_invoked_now": False,
        **meta,
    }

    voice_boundary = {
        "plan_id": "voice_output_plane_boundary_plan_v1",
        "voice_output_plane_invoked_now": False,
        "no_tts": True,
        "no_audio_output": True,
        "no_interruption_runtime_voice_behavior": True,
        "voice_output_remains_later_only": True,
        **meta,
    }

    display_boundary = {
        "plan_id": "display_output_boundary_plan_v1",
        "display_output_invoked_now": False,
        "no_ui_rendering": True,
        "no_notification": True,
        "no_app_push": True,
        "display_output_remains_later_only": True,
        **meta,
    }

    assembly_rules = {
        "plan_id": "output_assembly_rule_plan_v1",
        "mappings": list(OUTPUT_ASSEMBLY_MAPPINGS),
        "mapping_count": len(OUTPUT_ASSEMBLY_MAPPINGS),
        "assembled_later_not_now": True,
        "assembly_does_not_execute_output": True,
        "notice_candidate_not_user_facing_now": True,
        "clarification_candidate_does_not_ask_user_now": True,
        "reobserve_candidate_does_not_activate_camera": True,
        "escalation_notice_does_not_notify_hive_owner_now": True,
        **meta,
    }

    preservation = {
        "plan_id": "output_uncertainty_and_evidence_preservation_plan_v1",
        "uncertainty_level_preserved": True,
        "evidence_refs_preserved": True,
        "rationale_refs_preserved": True,
        "source_chain_preserved": True,
        "validation_refs_preserved": True,
        "health_refs_preserved": True,
        "constitution_refs_preserved": True,
        "whitebox_refs_preserved": True,
        "no_evidence_mutation": True,
        **meta,
    }

    personalization_boundary = {
        "plan_id": "output_personalization_boundary_plan_v1",
        "personalization_can_shape_tone_channel_later": True,
        "personalization_cannot_override_safety_constitution_validation": True,
        "no_personal_memory_write": True,
        "no_user_profile_update": True,
        "personalization_refs_optional_context_only": True,
        **meta,
    }

    memory_task_boundary = {
        "plan_id": "memory_worldmodel_task_state_boundary_plan_v1",
        "no_memory_write": True,
        "no_world_model_write": True,
        "no_fact_admission": True,
        "no_task_state_commit": True,
        "task_state_requires_separate_integration_later": True,
        "memory_worldmodel_requires_separate_admission_policy_later": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "output_plane_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "output_plane_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate output_plane_model_candidate",
            "generate sample task_response_candidate intake",
            "generate sample user_output_candidate",
            "verify output channel taxonomy",
            "verify User Output Constitution / Safety / Speech / Voice / Display boundaries",
            "verify user_output_candidate ≠ user_facing_output / speech / display",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "output_plane_integration_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "main_chain_defined": [
            "candidate/evidence/validation/health/whitebox",
            "→ decision_request_candidate",
            "→ decision_candidate",
            "→ task_response_candidate",
            "→ user_output_candidate",
        ],
        **meta,
    }

    policy = {
        "policy_id": "output_plane_integration_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "output_plane_not_user_facing_output": True,
        "output_plane_not_speech_not_tts": True,
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
        "output_plane_integration_planning_policy": policy,
        "upstream_task_response_input_review": upstream_review,
        "output_plane_module_definition": module_def,
        "task_response_candidate_intake_contract": task_intake,
        "user_output_candidate_contract": user_output_contract,
        "output_channel_taxonomy": channel_taxonomy,
        "user_output_constitution_binding_plan": constitution_binding,
        "safety_gate_binding_plan": safety_binding,
        "speech_gate_binding_plan": speech_binding,
        "voice_output_plane_boundary_plan": voice_boundary,
        "display_output_boundary_plan": display_boundary,
        "output_assembly_rule_plan": assembly_rules,
        "output_uncertainty_and_evidence_preservation_plan": preservation,
        "output_personalization_boundary_plan": personalization_boundary,
        "memory_worldmodel_task_state_boundary_plan": memory_task_boundary,
        "output_plane_boundary_matrix": boundary_matrix,
        "output_plane_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "output_plane_integration_planning_decision": planning_decision,
        "summary": summary,
    }
