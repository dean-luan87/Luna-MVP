# -*- coding: utf-8 -*-
"""Midplatform Display Gate Planning v1."""

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
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
    NEXT_PHASE_GO as PROVIDER_ABS_DR_NEXT_PHASE,
)

PHASE_ID = "Phase-Midplatform-Display-Gate-Planning-v1-001"
SCOPE = "display_gate_planning_only"
SOURCE_CHAIN = "midplatform_display_gate_planning_v1"

UPSTREAM_PROVIDER_ABS_DR_FINAL = PROVIDER_ABS_DR_FINAL_GO
UPSTREAM_PROVIDER_ABS_DR_NEXT = PROVIDER_ABS_DR_NEXT_PHASE
UPSTREAM_SAFETY_DR_FINAL = SAFETY_DR_FINAL_GO

FINAL_DECISION_GO = "MIDPLATFORM_DISPLAY_GATE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_DISPLAY_GATE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Display-Gate-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Display-Gate-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "display_gate_result_candidate ≠ Display Output ≠ UI render ≠ notification ≠ app push"
)

DISPLAY_GATE_LAYER_POSITIONING: Tuple[str, ...] = (
    "Display Gate is an enforcement layer module, not an execution layer module",
    "Display Gate consumes enforcement_result_candidate and emits display_gate_result_candidate",
    "Display Output / Notification Output are execution layer; they consume display_gate_result_candidate later",
    "Display Gate does not read raw constitution clauses",
    "enforcement_result_candidate flows Safety Gate → Display Gate → Display Output later",
    "Safety Gate / Speech Gate / Display Gate = Enforcement Layer",
    "Voice Output Plane / Display Output / TTS / Notification Output = Execution Layer",
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

DISPLAY_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "display_gate_result_candidate_id",
    "source_enforcement_result_candidate_ref",
    "source_user_output_candidate_ref",
    "display_gate_action",
    "display_gate_status",
    "display_channel_allowed",
    "display_output_allowed",
    "required_disclosures",
    "required_uncertainty_surface",
    "required_privacy_masking",
    "required_layout_constraints",
    "required_notification_constraints",
    "forbidden_display_actions",
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

DISPLAY_ACTION_TAXONOMY: Tuple[str, ...] = (
    "display_allow_candidate_forward",
    "display_block_candidate",
    "display_hold_candidate",
    "display_degrade_candidate",
    "display_require_disclosure",
    "display_require_uncertainty_surface",
    "display_require_privacy_masking",
    "display_require_compact_layout_later",
    "display_no_output_candidate",
    "display_request_more_evidence",
    "display_request_reobserve",
    "display_escalate_to_owner_later",
    "display_emit_violation_report_candidate",
)

CHANNEL_ADMISSION_RULES: Tuple[str, ...] = (
    "display channel must be allowed by enforcement_result_candidate",
    "blocked_downstream_gates containing display_gate blocks display path",
    "forbidden_actions containing display_output blocks display path",
    "no_output_candidate can override display preference",
    "display channel preference cannot override safety result",
    "display channel candidate does not execute display",
)

CONTENT_CONSTRAINT_RULES: Tuple[str, ...] = (
    "display payload candidate preserves required disclosures",
    "display preserves uncertainty if required",
    "display does not present not_fact as fact",
    "display does not remove safety warning",
    "display does not expose privacy-sensitive content",
    "display does not expand beyond validated content",
    "display does not add unsupported facts",
)

UNCERTAINTY_DISCLOSURE_RULES: Tuple[str, ...] = (
    "uncertainty_level preserved",
    "required_disclosures preserved",
    "low confidence requires uncertainty surface or hold",
    "missing evidence requires hold / evidence request",
    "conflicting evidence requires hold / explanation later",
    "urgent safety warning can be prioritized later but not rendered now",
)

PRIVACY_MASKING_RULES: Tuple[str, ...] = (
    "privacy_sensitive_fields require masking later",
    "bystander information requires masking / hold",
    "personal data minimization required",
    "memory-derived content requires memory policy later",
    "personalization cannot override privacy masking",
)

LAYOUT_BOUNDARY_RULES: Tuple[str, ...] = (
    "layout constraints may be attached later",
    "compact layout candidate may be required",
    "long content may require truncation / summary later",
    "no UI rendering now",
    "no device display access now",
    "no visual overlay now",
)

NOTIFICATION_BOUNDARY_RULES: Tuple[str, ...] = (
    "notification requires Notification Gate later",
    "app push requires Notification Output later",
    "display gate pass ≠ notification sent",
    "no notification / app push now",
    "silent/no_output remains valid",
)

REFUSAL_HOLD_DEGRADE_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"safety_signal": "safety_block", "display_path": "display_no_output_candidate or refusal_candidate later"},
    {"safety_signal": "safety_hold", "display_path": "display_hold_candidate later"},
    {"safety_signal": "safety_degrade", "display_path": "display_degrade_candidate later"},
    {"safety_signal": "require_disclosure", "display_path": "attach disclosure requirement"},
    {"safety_signal": "request_more_evidence", "display_path": "display evidence request candidate later"},
    {"safety_signal": "severe_violation", "display_path": "no display + escalation later"},
)

DOWNSTREAM_HANDOFF_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"display_action": "display_allow_candidate_forward", "handoff": "Display Output planning later"},
    {"display_action": "display_block_candidate", "handoff": "no_output/refusal path later"},
    {"display_action": "display_hold_candidate", "handoff": "hold/no_output path later"},
    {"display_action": "display_degrade_candidate", "handoff": "degraded display candidate later"},
    {"display_action": "display_request_more_evidence", "handoff": "clarification/evidence path later"},
    {"display_action": "display_escalate_to_owner_later", "handoff": "owner escalation path later"},
)

NO_RAW_CONSTITUTION_RULES: Tuple[str, ...] = (
    "display gate does not bind raw constitution clauses",
    "display gate consumes enforcement_result_candidate / constraint-derived result",
    "constitution changes update Resolver / constraint_bundle / Safety Gate result, not Display Gate",
    "breaking result schema change requires compatibility phase",
    "ordinary constitution amendment should not rewrite Display Gate",
    "all rule refs retained for Whitebox audit",
)

EXECUTION_LAYER_BOUNDARY_RULES: Tuple[str, ...] = (
    "Display Gate pass ≠ Display Output",
    "Display Gate pass ≠ UI render",
    "Display Gate pass ≠ notification / app push",
    "Display Output required separately",
    "Notification Gate / Notification Output required separately",
    "execution layer cannot override display_gate_result_candidate",
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
    "display action reason preserved",
    "display block/hold/degrade reason auditable",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "display_gate_runtime_enabled_now",
    "display_gate_invoked_now",
    "display_gate_result_generated_now",
    "display_output_invoked_now",
    "ui_rendered_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "raw_constitution_clause_bound_now",
    "safety_gate_bypassed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Display Gate Planning GO ≠ Display Gate runtime enabled",
    "Display Gate planned ≠ Display Output invoked",
    "display_allow candidate planned ≠ UI rendered",
    "notification boundary planned ≠ notification sent",
    "next DryRunAndReview ≠ final display output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("display_gate_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_planning"
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


def _display_gate_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "display_gate_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_display_gate_v1",
            "module_type": "midplatform_user_output_gate_module",
            "role": "display_output_enforcement_gate",
            "system_layer": "Validation",
            "architectural_layer": "Enforcement",
            "runtime_enabled_now": False,
            "layer_positioning": (
                "Display Gate is an enforcement layer module, not an execution layer module"
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
                "display_channel_candidate",
                "required_disclosures",
                "uncertainty_policy",
                "privacy_policy",
                "forbidden_actions",
                "layout_display_constraints",
            ],
            "required_inputs": list(ENFORCEMENT_RESULT_INTAKE_FIELDS) + list(USER_OUTPUT_INTAKE_FIELDS),
            "optional_inputs": ["risk_flags", "channel_preferences"],
            "forbidden_inputs": [
                "raw_constitution_clauses",
                "constitution_publish_directive",
                "display_output_directive",
                "ui_render_directive",
                "notification_directive",
                "app_push_directive",
                "memory_write_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "display_output_later",
                "notification_gate_later",
                "no_output_handler_later",
            ],
            "downstream_object_types": ["display_gate_result_candidate"],
            "allowed_outputs": ["display_gate_result_candidate"],
            "forbidden_outputs": [
                "display_output",
                "ui_render",
                "notification",
                "app_push",
                "user_facing_display",
                "memory_fact",
            ],
        },
        "input_contract": {
            "input_contract": "display_gate_enforcement_result_intake_contract_v1",
            "source_chain": "preserved_from_enforcement_result_and_user_output",
            "evidence_ref": "preserved",
            "ttl": "required_from_enforcement_result",
            "confidence": "preserved_as_uncertainty_level",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": (
                "enforce display output constraints from enforcement_result_candidate + "
                "user_output_candidate; emit display_gate_result_candidate for Display Output later"
            ),
            "allowed_transformation": [
                "check display channel admission from enforcement result",
                "apply content/privacy/layout/notification/uncertainty constraints",
                "select display_gate_action from taxonomy",
                "emit allow/block/hold/degrade/require_disclosure/no_output display gate result",
                "preserve refs and traceability",
            ],
            "forbidden_transformation": [
                "bind raw constitution clauses",
                "invoke Display Output",
                "render UI",
                "send notification or app push",
                "write memory or world model",
                "commit task_state",
                "invoke provider or model runtime",
                "bypass Safety Gate",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "display_gate_result_candidate_contract_v1",
            "output_object_type": "display_gate_result_candidate",
            "execution_layer_consumes_display_gate_result": True,
            "decision_refs": "source_enforcement_result_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_intake",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
            "display_output_allowed": False,
        },
        "module_principles": {
            "module_principles": list(DISPLAY_GATE_LAYER_POSITIONING) + [
                "display_gate_result_candidate ≠ Display Output ≠ UI render",
            ],
            "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
            "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
            "priority_policy": "safety enforcement result overrides display channel preference",
            "conflict_policy": "forbidden_actions from enforcement result enforced",
            "fallback_policy": "safety block/hold → display_no_output or hold",
            "rollback_policy": "enforcer does not commit state or execute display output",
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
            "display_output_allowed_now": False,
            "memory_allowed_now": False,
            "world_model_allowed_now": False,
        },
        "failure_and_traceability": {
            "failure_route": "block/hold/degrade/no_output/escalation per display_gate_action",
            "issue_trace": "whitebox_trace_refs preserved",
            "violation_report": "display_emit_violation_report_candidate path",
            "escalation_path": "owner later; no invoke now",
            "audit_required": True,
        },
    }


def run_midplatform_display_gate_planning_v1(
    *,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_speech_display_gate_roadmap_decision_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    roadmap_root = Path(midplatform_speech_display_gate_roadmap_decision_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    uo_dr_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    deferred_routes = _try_read_json(roadmap_root / "deferred_routes_register_v1.json") or {}
    next_route = _try_read_json(roadmap_root / "next_phase_readiness_decision_v1.json") or {}
    safety_dr_sm = _try_read_json(safety_dr_root / "summary.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    safety_model = _try_read_json(safety_dr_root / "safety_gate_model_candidate_v1.json") or {}
    sample_user_output = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    output_dr_vr = _try_read_json(output_dr_root / "verifier_report.json") or {}
    uo_dr_vr = _try_read_json(uo_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_user_output_constitution_dryrun_root": str(uo_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview verifier must be GO")
    if provider_dr_sm.get("final_decision") != UPSTREAM_PROVIDER_ABS_DR_FINAL:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if provider_dr_sm.get("recommended_next_phase") != UPSTREAM_PROVIDER_ABS_DR_NEXT:
        blockers.append("provider abstraction dryrun recommended_next_phase mismatch")
    if roadmap_vr.get("verifier") != "GO":
        blockers.append("Speech Display Gate Roadmap Decision verifier must be GO")
    display_deferred = (
        next_route.get("display_gate_deferred_not_skipped") is True
        or deferred_routes.get("display_gate_deferred_not_skipped") is True
        or "Route B — Display Gate First" in (roadmap_sm.get("deferred_routes") or [])
    )
    if not display_deferred:
        blockers.append("Display Gate must be deferred not skipped in roadmap")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview verifier must be GO")
    if safety_dr_sm.get("final_decision") != UPSTREAM_SAFETY_DR_FINAL:
        blockers.append("safety gate dryrun final_decision mismatch")
    if safety_model.get("emits_enforcement_result_candidate") is not True:
        blockers.append("Safety Gate must emit enforcement_result_candidate")
    if not sample_user_output.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if output_dr_vr.get("verifier") != "GO":
        blockers.append("Output Plane DryRunAndReview must be GO")
    if uo_dr_vr.get("verifier") != "GO":
        blockers.append("User Output Constitution DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    module_def = _display_gate_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    provider_input_review = {
        "review_id": "provider_abstraction_alignment_input_review_v1",
        "provider_abstraction_dryrun_verifier": provider_dr_vr.get("verifier"),
        "provider_abstraction_final_decision": provider_dr_sm.get("final_decision"),
        "roadmap_decision_verifier": roadmap_vr.get("verifier"),
        "display_gate_deferred_not_skipped": display_deferred,
        "safety_gate_dryrun_verifier": safety_dr_vr.get("verifier"),
        "safety_gate_emits_enforcement_result": safety_model.get("emits_enforcement_result_candidate") is True,
        "display_gate_is_enforcement_layer": True,
        "display_output_is_execution_layer": True,
        "display_gate_consumes_enforcement_result": True,
        "display_gate_no_raw_constitution": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    enforcement_intake = {
        "contract_id": "display_gate_enforcement_result_intake_contract_v1",
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
        "contract_id": "display_gate_user_output_candidate_intake_contract_v1",
        "required_fields": list(USER_OUTPUT_INTAKE_FIELDS),
        "defaults": {
            "user_facing_output_allowed": False,
            "display_output_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
        },
        **meta,
    }

    result_contract = {
        "contract_id": "display_gate_result_candidate_contract_v1",
        "output_type": "display_gate_result_candidate",
        "required_fields": list(DISPLAY_GATE_RESULT_FIELDS),
        "display_gate_semantics": {
            "allow": "display_allow_candidate_forward",
            "block": "display_block_candidate",
            "hold": "display_hold_candidate",
            "degrade": "display_degrade_candidate",
            "require_disclosure": "display_require_disclosure",
            "no_output": "display_no_output_candidate",
        },
        "execution_layer_reads": [
            "display_channel_allowed",
            "required_disclosures",
            "required_uncertainty_surface",
            "required_privacy_masking",
            "required_layout_constraints",
            "required_notification_constraints",
            "forbidden_display_actions",
            "applicable_rule_refs",
        ],
        "defaults": {
            "candidate_only": True,
            "display_output_allowed": False,
        },
        "not_execution_output": True,
        **meta,
    }

    action_taxonomy = {
        "taxonomy_id": "display_gate_action_taxonomy_v1",
        "actions": list(DISPLAY_ACTION_TAXONOMY),
        "action_count": len(DISPLAY_ACTION_TAXONOMY),
        **meta,
    }

    channel_admission = {
        "plan_id": "display_channel_admission_rule_plan_v1",
        "rules": list(CHANNEL_ADMISSION_RULES),
        "rule_count": len(CHANNEL_ADMISSION_RULES),
        **meta,
    }

    content_constraint = {
        "plan_id": "display_content_constraint_rule_plan_v1",
        "rules": list(CONTENT_CONSTRAINT_RULES),
        "rule_count": len(CONTENT_CONSTRAINT_RULES),
        **meta,
    }

    uncertainty_disclosure = {
        "plan_id": "display_uncertainty_disclosure_rule_plan_v1",
        "rules": list(UNCERTAINTY_DISCLOSURE_RULES),
        "rule_count": len(UNCERTAINTY_DISCLOSURE_RULES),
        **meta,
    }

    privacy_masking = {
        "plan_id": "display_privacy_masking_rule_plan_v1",
        "rules": list(PRIVACY_MASKING_RULES),
        "rule_count": len(PRIVACY_MASKING_RULES),
        **meta,
    }

    layout_boundary = {
        "plan_id": "display_layout_boundary_plan_v1",
        "rules": list(LAYOUT_BOUNDARY_RULES),
        "rule_count": len(LAYOUT_BOUNDARY_RULES),
        **meta,
    }

    notification_boundary = {
        "plan_id": "display_notification_boundary_plan_v1",
        "rules": list(NOTIFICATION_BOUNDARY_RULES),
        "rule_count": len(NOTIFICATION_BOUNDARY_RULES),
        **meta,
    }

    refusal_hold_degrade = {
        "plan_id": "display_refusal_hold_degrade_plan_v1",
        "mappings": list(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        "mapping_count": len(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        **meta,
    }

    downstream_handoff = {
        "plan_id": "display_gate_downstream_handoff_plan_v1",
        "handoffs": list(DOWNSTREAM_HANDOFF_MAPPINGS),
        "handoff_count": len(DOWNSTREAM_HANDOFF_MAPPINGS),
        "display_gate_enforcement_display_output_execution": True,
        "no_downstream_runtime_invoked_now": True,
        **meta,
    }

    no_raw_binding = {
        "policy_id": "display_gate_no_raw_constitution_binding_policy_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "rule_count": len(NO_RAW_CONSTITUTION_RULES),
        "consumes_enforcement_result_only": True,
        **meta,
    }

    execution_boundary = {
        "plan_id": "display_gate_execution_layer_boundary_plan_v1",
        "rules": list(EXECUTION_LAYER_BOUNDARY_RULES),
        "rule_count": len(EXECUTION_LAYER_BOUNDARY_RULES),
        "display_pass_not_display_output_or_ui": True,
        **meta,
    }

    traceability = {
        "plan_id": "display_gate_traceability_plan_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        "requirement_count": len(TRACEABILITY_REQUIREMENTS),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "display_gate_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "display_gate_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate display_gate_model_candidate",
            "generate sample enforcement_result intake",
            "generate sample user_output_candidate intake",
            "generate sample display_gate_result_candidate",
            "verify Display Gate as Enforcement Layer",
            "verify no raw constitution binding",
            "verify display pass ≠ Display Output / UI render / notification",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "display_gate_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "display_gate_layer_positioning": list(DISPLAY_GATE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "main_chain_defined": [
            "Rule Source (constitutions / standards / rules)",
            "→ Rule Resolution (Constitution Resolver → constraint_bundle)",
            "→ Enforcement (Safety Gate → Speech Gate → Display Gate …)",
            "→ Execution (Voice Output Plane / Display Output / TTS / Notification Output …)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "display_gate_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "enforcement_result_only_not_raw_clauses": True,
        "display_gate_is_enforcement_not_execution": True,
        "display_gate_layer_positioning": list(DISPLAY_GATE_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "execution_consumes_display_gate_result_later": True,
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
        "display_gate_planning_policy": policy,
        "provider_abstraction_alignment_input_review": provider_input_review,
        "display_gate_module_definition": module_def,
        "display_gate_enforcement_result_intake_contract": enforcement_intake,
        "display_gate_user_output_candidate_intake_contract": user_output_intake,
        "display_gate_result_candidate_contract": result_contract,
        "display_gate_action_taxonomy": action_taxonomy,
        "display_channel_admission_rule_plan": channel_admission,
        "display_content_constraint_rule_plan": content_constraint,
        "display_uncertainty_disclosure_rule_plan": uncertainty_disclosure,
        "display_privacy_masking_rule_plan": privacy_masking,
        "display_layout_boundary_plan": layout_boundary,
        "display_notification_boundary_plan": notification_boundary,
        "display_refusal_hold_degrade_plan": refusal_hold_degrade,
        "display_gate_downstream_handoff_plan": downstream_handoff,
        "display_gate_no_raw_constitution_binding_policy": no_raw_binding,
        "display_gate_execution_layer_boundary_plan": execution_boundary,
        "display_gate_traceability_plan": traceability,
        "display_gate_boundary_matrix": boundary_matrix,
        "display_gate_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "display_gate_planning_decision": planning_decision,
        "summary": summary,
    }
