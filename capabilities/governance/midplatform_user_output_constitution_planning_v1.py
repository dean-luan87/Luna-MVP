# -*- coding: utf-8 -*-
"""Midplatform User Output Constitution Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_planning_v1 import (
    FINAL_DECISION_GO as TEMPLATE_PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_ID
from capabilities.governance.midplatform_output_plane_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OUTPUT_DR_FINAL_GO,
    NEXT_PHASE_GO as OUTPUT_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    OUTPUT_CHANNEL_TAXONOMY,
    USER_OUTPUT_CANDIDATE_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-User-Output-Constitution-Planning-v1-001"
SCOPE = "user_output_constitution_planning_only"
SOURCE_CHAIN = "midplatform_user_output_constitution_planning_v1"

UPSTREAM_OUTPUT_DR_FINAL = OUTPUT_DR_FINAL_GO
UPSTREAM_OUTPUT_DR_NEXT = OUTPUT_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_USER_OUTPUT_CONSTITUTION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_USER_OUTPUT_CONSTITUTION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-User-Output-Constitution-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-User-Output-Constitution-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "user_output_candidate ≠ user_facing_output ≠ speech_request ≠ TTS ≠ display rendered ≠ app notification"
)

JURISDICTION_GOVERNED: Tuple[str, ...] = (
    "user_output_candidate",
    "speech_output_candidate",
    "display_output_candidate",
    "haptic_output_candidate_later",
    "app_notification_candidate_later",
    "no_output_candidate",
)

JURISDICTION_NOT_GOVERNED: Tuple[str, ...] = (
    "raw_candidate",
    "decision_candidate",
    "task_response_candidate_before_output_plane",
    "provider_runtime",
    "model_runtime",
    "memory_write",
    "world_model_write",
)

ADMISSION_RULES: Tuple[str, ...] = (
    "source_task_response_candidate_ref exists",
    "decision_ref exists",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "constitution_refs preserved",
    "safety_refs required later",
    "uncertainty_level present",
    "output_channel_candidate valid",
    "user_facing_output_allowed remains false until gate pass",
    "unvalidated content cannot proceed",
)

SAFETY_RULES: Tuple[str, ...] = (
    "safety block → no_output_candidate or safety_hold_candidate",
    "physical safety warning must preserve urgency later",
    "unsafe instruction → reject/block output candidate",
    "severe violation → escalation / violation report later",
    "safety cannot be relaxed by personalization",
    "safety gate required before final output",
)

FACT_UNCERTAINTY_RULES: Tuple[str, ...] = (
    "fact_status=not_fact cannot be presented as fact",
    "uncertain content must preserve uncertainty",
    "low confidence requires hedge / hold / request_more_evidence later",
    "missing evidence blocks assertive output",
    "stale evidence requires caveat or hold",
    "conflicting evidence requires hold or explanation",
    "no fabricated certainty",
)

PRIVACY_RULES: Tuple[str, ...] = (
    "sensitive personal data must be minimized",
    "private context cannot be exposed without authorization",
    "bystander/privacy-sensitive content requires hold or masking later",
    "memory-derived content requires memory policy later",
    "user preference cannot override privacy/safety",
)

CHANNEL_RULES: Tuple[str, ...] = (
    "speech channel requires Speech Gate + Voice Output Plane",
    "display channel requires Display Output Gate",
    "app notification requires Notification Gate later",
    "silent/no_output is valid",
    "channel candidate does not execute channel",
    "urgency may influence channel later, but not now",
)

REFUSAL_HOLD_DEGRADE_RULES: Tuple[Dict[str, str], ...] = (
    {"trigger": "block", "response": "refusal/no_output/block_notice candidate later"},
    {"trigger": "hold", "response": "hold_notice/no_output candidate later"},
    {"trigger": "degrade", "response": "degraded_notice candidate later"},
    {"trigger": "request_more_evidence", "response": "clarification candidate later"},
    {"trigger": "request_reobserve", "response": "reobserve guidance candidate later"},
    {"trigger": "severe violation", "response": "no_output + escalation later"},
    {"trigger": "silent mode", "response": "valid when output may cause harm or confusion"},
)

EXPLAINABILITY_REQUIREMENTS: Tuple[str, ...] = (
    "source_chain preserved",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "validation_refs preserved",
    "health_refs preserved",
    "constitution_refs preserved",
    "whitebox_refs preserved",
    "blocked/hold/degrade reason preserved",
    "output decision must be auditable later",
)

CONFLICT_PRIORITY: Tuple[str, ...] = (
    "Safety / survival / privacy",
    "General Constitution",
    "User Output Constitution",
    "Domain Constitution / Standard",
    "Validation result",
    "Evidence confidence",
    "Health signal",
    "Task context",
    "Personalization / user preference",
)

CONFLICT_RULES: Tuple[str, ...] = (
    "safety/privacy block overrides output preference",
    "fact uncertainty blocks assertive wording",
    "validation fail blocks user-facing output",
    "missing evidence blocks assertive output",
    "personalization cannot override safety/fact/privacy",
    "channel preference cannot override safety or availability",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "user_output_constitution_runtime_enabled_now",
    "user_output_gate_invoked_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
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
    "User Output Constitution Planning GO ≠ user output allowed",
    "constitution defined ≠ output gate invoked",
    "channel rules planned ≠ speech/display execution",
    "uncertainty rule planned ≠ final wording generated",
    "next DryRunAndReview ≠ final output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("user_output_constitution_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_planning"
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


def _user_output_constitution_definition() -> Dict[str, Any]:
    return {
        "constitution_id": "midplatform_user_output_constitution_v1",
        "constitution_type": "user_output_governance_constitution",
        "jurisdiction": "user_output_candidate_to_user_facing_output",
        "system_layer": "Output",
        "runtime_enabled_now": False,
        "governs_user_output_candidate": True,
        "governs_speech_output_candidate": True,
        "governs_display_output_candidate": True,
        "governs_notification_candidate": True,
        "does_not_govern_provider_runtime": True,
        "does_not_write_memory": True,
        "does_not_write_worldmodel": True,
        "core_responsibilities": [
            "judge whether user_output_candidate may enter user-facing output path",
            "constrain output safety",
            "constrain fact and uncertainty expression",
            "constrain privacy exposure",
            "constrain tone/personalization boundaries",
            "constrain output channels",
            "constrain refusal/hold/degrade/silent/no_output rules",
            "preserve evidence/rationale/source_chain",
        ],
        "explicitly_not": [
            "does not directly generate output",
            "does not trigger TTS",
            "does not trigger Display",
            "does not invoke provider/model",
            "does not write Memory/WorldModel",
            "does not commit task_state",
        ],
    }


def run_midplatform_user_output_constitution_planning_v1(
    *,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_output_plane_integration_planning_root: str,
    midplatform_task_response_candidate_integration_dryrun_and_review_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    output_plan_root = Path(
        midplatform_output_plane_integration_planning_root
    ).expanduser().resolve()
    task_dr_root = Path(
        midplatform_task_response_candidate_integration_dryrun_and_review_root
    ).expanduser().resolve()
    constitution_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    output_dr_sm = _try_read_json(output_dr_root / "summary.json") or {}
    output_dr_vr = _try_read_json(output_dr_root / "verifier_report.json") or {}
    sample_user_output = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    output_plan_vr = _try_read_json(output_plan_root / "verifier_report.json") or {}
    task_dr_vr = _try_read_json(task_dr_root / "verifier_report.json") or {}
    constitution_dr_vr = _try_read_json(constitution_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_output_plane_planning_root": str(output_plan_root),
        "upstream_task_response_dryrun_root": str(task_dr_root),
        "upstream_constitution_dryrun_root": str(constitution_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if output_dr_vr.get("verifier") != "GO":
        blockers.append("Output Plane DryRunAndReview verifier must be GO")
    if output_dr_sm.get("final_decision") != UPSTREAM_OUTPUT_DR_FINAL:
        blockers.append("output plane dryrun final_decision mismatch")
    if output_dr_sm.get("recommended_next_phase") != UPSTREAM_OUTPUT_DR_NEXT:
        blockers.append("output plane dryrun recommended_next_phase mismatch")
    if not sample_user_output.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if sample_user_output.get("user_facing_output_allowed") is not False:
        blockers.append("sample user_output must have user_facing_output_allowed=false")
    if sample_user_output.get("speech_request_allowed") is not False:
        blockers.append("sample user_output must have speech_request_allowed=false")
    if sample_user_output.get("display_output_allowed") is not False:
        blockers.append("sample user_output must have display_output_allowed=false")
    if output_dr_sm.get("output_plane_runtime_enabled_now") is not False:
        blockers.append("Output Plane runtime must not be enabled")
    if output_plan_vr.get("verifier") != "GO":
        blockers.append("Output Plane Planning verifier must be GO")
    if task_dr_vr.get("verifier") != "GO":
        blockers.append("Task Response DryRunAndReview must be GO")
    if constitution_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    constitution_def = _user_output_constitution_definition()
    input_ok = len(blockers) == 0

    dryrun_input_review = {
        "review_id": "output_plane_dryrun_input_review_v1",
        "output_plane_dryrun_verifier": output_dr_vr.get("verifier"),
        "output_plane_dryrun_final": output_dr_sm.get("final_decision"),
        "sample_user_output_present": bool(sample_user_output.get("user_output_candidate_id")),
        "user_output_not_user_facing": True,
        "constitution_not_speech_not_display": True,
        "output_plane_runtime_disabled": output_dr_sm.get("output_plane_runtime_enabled_now") is False,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    scope_jurisdiction = {
        "document_id": "user_output_scope_and_jurisdiction_v1",
        "governed_objects": list(JURISDICTION_GOVERNED),
        "not_governed_objects": list(JURISDICTION_NOT_GOVERNED),
        "governed_count": len(JURISDICTION_GOVERNED),
        "not_governed_count": len(JURISDICTION_NOT_GOVERNED),
        **meta,
    }

    admission_plan = {
        "plan_id": "user_output_admission_rule_plan_v1",
        "rules": list(ADMISSION_RULES),
        "rule_count": len(ADMISSION_RULES),
        "admission_does_not_generate_output": True,
        **meta,
    }

    safety_plan = {
        "plan_id": "user_output_safety_rule_plan_v1",
        "rules": list(SAFETY_RULES),
        "rule_count": len(SAFETY_RULES),
        "safety_gate_required_before_final_output": True,
        "safety_not_relaxed_by_personalization": True,
        **meta,
    }

    fact_uncertainty_plan = {
        "plan_id": "user_output_fact_and_uncertainty_rule_plan_v1",
        "rules": list(FACT_UNCERTAINTY_RULES),
        "rule_count": len(FACT_UNCERTAINTY_RULES),
        "no_fabricated_certainty": True,
        **meta,
    }

    privacy_plan = {
        "plan_id": "user_output_privacy_rule_plan_v1",
        "rules": list(PRIVACY_RULES),
        "rule_count": len(PRIVACY_RULES),
        "user_preference_cannot_override_privacy_safety": True,
        **meta,
    }

    channel_plan = {
        "plan_id": "user_output_channel_rule_plan_v1",
        "rules": list(CHANNEL_RULES),
        "rule_count": len(CHANNEL_RULES),
        "channel_taxonomy_ref": [ch["channel_id"] for ch in OUTPUT_CHANNEL_TAXONOMY],
        "channel_candidate_not_execution": True,
        **meta,
    }

    tone_personalization = {
        "plan_id": "user_output_tone_personalization_boundary_plan_v1",
        "personalization_may_shape_tone_later": True,
        "personalization_cannot_override_safety_constitution_validation_privacy": True,
        "emotional_tone_must_not_distort_factual_uncertainty": True,
        "no_personal_memory_write": True,
        "no_user_profile_update": True,
        **meta,
    }

    refusal_hold_degrade = {
        "plan_id": "user_output_refusal_hold_degrade_rule_plan_v1",
        "rules": list(REFUSAL_HOLD_DEGRADE_RULES),
        "rule_count": len(REFUSAL_HOLD_DEGRADE_RULES),
        "silent_mode_valid": True,
        **meta,
    }

    explainability = {
        "plan_id": "user_output_explainability_traceability_plan_v1",
        "requirements": list(EXPLAINABILITY_REQUIREMENTS),
        "requirement_count": len(EXPLAINABILITY_REQUIREMENTS),
        "output_decision_auditable_later": True,
        **meta,
    }

    speech_display_boundary = {
        "plan_id": "user_output_speech_display_boundary_plan_v1",
        "constitution_pass_not_speech_request": True,
        "speech_gate_required_separately": True,
        "tts_required_separately": True,
        "voice_output_plane_required_separately": True,
        "display_output_required_separately": True,
        "speech_request_generated_now": False,
        "speech_gate_invoked_now": False,
        "tts_invoked_now": False,
        "display_output_invoked_now": False,
        **meta,
    }

    memory_task_boundary = {
        "plan_id": "user_output_memory_worldmodel_taskstate_boundary_plan_v1",
        "no_memory_write": True,
        "no_world_model_write": True,
        "no_fact_admission": True,
        "no_task_state_commit": True,
        "write_requires_separate_admission_policy_later": True,
        **meta,
    }

    conflict_policy = {
        "policy_id": "user_output_constitution_conflict_policy_v1",
        "priority_layers": list(CONFLICT_PRIORITY),
        "priority_count": len(CONFLICT_PRIORITY),
        "conflict_rules": list(CONFLICT_RULES),
        "conflict_rule_count": len(CONFLICT_RULES),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "user_output_constitution_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "user_output_constitution_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate user_output_constitution_candidate",
            "generate sample user_output_candidate intake",
            "verify admission/safety/fact uncertainty/privacy/channel/personalization/refusal-hold-degrade rules",
            "verify speech/display/memory/worldmodel/taskstate boundaries",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok

    planning_decision = {
        "decision_id": "user_output_constitution_planning_decision_v1",
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
            "→ User Output Constitution gate (planned)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "user_output_constitution_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "constitution_not_user_facing_output": True,
        "constitution_not_speech_not_display": True,
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
        "user_output_constitution_planning_policy": policy,
        "output_plane_dryrun_input_review": dryrun_input_review,
        "user_output_constitution_definition": constitution_def,
        "user_output_scope_and_jurisdiction": scope_jurisdiction,
        "user_output_admission_rule_plan": admission_plan,
        "user_output_safety_rule_plan": safety_plan,
        "user_output_fact_and_uncertainty_rule_plan": fact_uncertainty_plan,
        "user_output_privacy_rule_plan": privacy_plan,
        "user_output_channel_rule_plan": channel_plan,
        "user_output_tone_personalization_boundary_plan": tone_personalization,
        "user_output_refusal_hold_degrade_rule_plan": refusal_hold_degrade,
        "user_output_explainability_traceability_plan": explainability,
        "user_output_speech_display_boundary_plan": speech_display_boundary,
        "user_output_memory_worldmodel_taskstate_boundary_plan": memory_task_boundary,
        "user_output_constitution_conflict_policy": conflict_policy,
        "user_output_constitution_boundary_matrix": boundary_matrix,
        "user_output_constitution_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "user_output_constitution_planning_decision": planning_decision,
        "summary": summary,
    }
