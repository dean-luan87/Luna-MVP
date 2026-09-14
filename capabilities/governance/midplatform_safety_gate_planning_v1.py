# -*- coding: utf-8 -*-
"""Midplatform Safety Gate Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    USER_OUTPUT_CANDIDATE_FIELDS,
)
from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    CONSTRAINT_BUNDLE_FIELDS,
    FINAL_DECISION_GO as UO_CONST_DR_FINAL_GO,
    NEXT_PHASE_GO as UO_CONST_DR_NEXT_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Safety-Gate-Planning-v1-001"
SCOPE = "safety_gate_planning_only"
SOURCE_CHAIN = "midplatform_safety_gate_planning_v1"

UPSTREAM_UO_CONST_DR_FINAL = UO_CONST_DR_FINAL_GO
UPSTREAM_UO_CONST_DR_NEXT = UO_CONST_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_SAFETY_GATE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_SAFETY_GATE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Safety-Gate-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Safety-Gate-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "enforcement_result_candidate ≠ execution_output ≠ speech_request ≠ TTS ≠ display rendered"
)

FOUR_LAYER_ARCHITECTURE: Dict[str, Any] = {
    "rule_source_layer": [
        "Luna General Constitution",
        "User Output Constitution",
        "Domain Constitution",
        "Safety / Privacy / Speech rules",
    ],
    "rule_resolution_layer": [
        "Constitution Resolver",
        "constraint_bundle",
    ],
    "enforcement_layer": [
        "Safety Gate",
        "User Output Gate",
        "Speech Gate",
        "Display Gate",
        "Authorization Gate",
        "Validation Factory",
    ],
    "execution_layer": [
        "Voice Output Plane",
        "Display Output",
        "Notification Output",
        "TTS runtime",
        "device action runtime",
    ],
}

ENFORCEMENT_LAYER_POSITIONING: Tuple[str, ...] = (
    "Safety Gate is an enforcement layer module, not an execution layer module",
    "Safety Gate consumes constraint_bundle and emits enforcement_result_candidate",
    "Execution layer consumes enforcement_result_candidate, not raw constitution",
    "constitution does not directly command execution layer",
    "constitution flows through resolver → bundle → enforcer → execution",
)

SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT: Tuple[Dict[str, str], ...] = (
    {"enforcement": "Speech Gate", "execution": "Voice Output Plane"},
    {"enforcement": "Display Gate", "execution": "Display Output"},
)

CONSTRAINT_BUNDLE_INTAKE_FIELDS: Tuple[str, ...] = CONSTRAINT_BUNDLE_FIELDS

USER_OUTPUT_INTAKE_FIELDS: Tuple[str, ...] = USER_OUTPUT_CANDIDATE_FIELDS

SAFETY_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "safety_gate_result_candidate_id",
    "source_user_output_candidate_ref",
    "source_constraint_bundle_ref",
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
    "user_facing_output_allowed",
    "speech_request_allowed",
    "display_output_allowed",
)

SAFETY_ACTION_TAXONOMY: Tuple[str, ...] = (
    "safety_allow_candidate_forward",
    "safety_block_candidate",
    "safety_hold_candidate",
    "safety_degrade_candidate",
    "safety_require_disclosure",
    "safety_require_uncertainty_surface",
    "safety_request_more_evidence",
    "safety_request_reobserve",
    "safety_no_output_candidate",
    "safety_escalate_to_owner_later",
    "safety_escalate_to_hive_later",
    "safety_emit_violation_report_candidate",
)

RULE_APPLICATION_RULES: Tuple[str, ...] = (
    "selected_constraint_action from bundle drives safety evaluation",
    "forbidden_actions from bundle must be enforced",
    "required_gates from bundle must be preserved",
    "required_disclosures must be preserved",
    "privacy_policy must be enforced",
    "uncertainty_policy must be enforced",
    "personalization_limits must be enforced",
    "escalation_required must be preserved",
)

UNCERTAINTY_RISK_RULES: Tuple[str, ...] = (
    "fact_status=not_fact cannot become assertive user-facing output",
    "uncertainty must be surfaced or held according to bundle",
    "missing evidence triggers hold/request_more_evidence",
    "conflicting evidence triggers hold",
    "high safety risk triggers block/no_output/escalation",
    "personalization cannot reduce safety strictness",
)

CHANNEL_BOUNDARY_RULES: Tuple[str, ...] = (
    "Safety Gate enforcement pass ≠ speech_request",
    "Safety Gate enforcement pass ≠ display render",
    "Safety Gate emits enforcement_result only; does not execute output",
    "Speech Gate is speech enforcement; Voice Output Plane is execution",
    "Display Gate is display enforcement; Display Output is execution",
    "notification still requires Notification Gate enforcement later",
    "no_output remains valid",
)

REFUSAL_HOLD_DEGRADE_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"safety_action": "safety_block_candidate", "path": "no_output_candidate or refusal_candidate later"},
    {"safety_action": "safety_hold_candidate", "path": "hold_candidate / no_output later"},
    {"safety_action": "safety_degrade_candidate", "path": "degraded_output_candidate later"},
    {"safety_action": "safety_require_disclosure", "path": "attach disclosure requirement later"},
    {"safety_action": "safety_request_more_evidence", "path": "evidence_request_candidate later"},
    {"safety_action": "safety_emit_violation_report_candidate", "path": "violation_report + escalation later"},
)

TRACEABILITY_REQUIREMENTS: Tuple[str, ...] = (
    "source_chain preserved",
    "source_constraint_bundle_ref preserved",
    "applicable_rule_refs preserved",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "whitebox_trace_refs preserved",
    "safety_action reason preserved",
    "output blocking/hold/degrade reason auditable",
)

DOWNSTREAM_HANDOFF_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {
        "safety_action": "safety_allow_candidate_forward",
        "handoff": "enforcement gates (Speech/Display/Notification) later based on channel",
    },
    {"safety_action": "safety_block_candidate", "handoff": "no_output/refusal path later"},
    {"safety_action": "safety_hold_candidate", "handoff": "hold path later"},
    {"safety_action": "safety_degrade_candidate", "handoff": "degraded output path later"},
    {"safety_action": "safety_request_more_evidence", "handoff": "clarification/evidence path later"},
    {"safety_action": "safety_escalate_to_hive_later", "handoff": "Hive path later"},
    {"safety_action": "safety_escalate_to_owner_later", "handoff": "owner path later"},
)

NO_RAW_CONSTITUTION_RULES: Tuple[str, ...] = (
    "safety gate does not bind raw constitution clauses",
    "safety gate consumes constraint_bundle only",
    "new constitution changes should update resolver/bundle, not safety gate",
    "breaking bundle schema change requires compatibility phase",
    "ordinary constitution change should not rewrite Safety Gate",
    "all rule refs retained for Whitebox audit",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "safety_gate_runtime_enabled_now",
    "safety_gate_invoked_now",
    "safety_gate_result_generated_now",
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
    "constitution_raw_clause_bound_now",
    "hive_constitution_registry_updated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Safety Gate Planning GO ≠ Safety Gate runtime enabled",
    "Safety Gate is enforcement layer ≠ execution layer",
    "enforcement_result_candidate planned ≠ user-facing output allowed",
    "bundle intake planned ≠ gate invoked",
    "enforcement allow planned ≠ Voice/Display execution",
    "next DryRunAndReview ≠ final user output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("safety_gate_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_planning"
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


def _safety_gate_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "safety_gate_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_safety_gate_v1",
            "module_type": "midplatform_enforcement_gate_module",
            "role": "user_output_safety_enforcement",
            "system_layer": "Validation",
            "architectural_layer": "Enforcement",
            "layer_positioning": (
                "Safety Gate is an enforcement layer module, not an execution layer module"
            ),
        },
        "upstream_sources": {
            "upstream_modules": [
                "midplatform_output_plane_integration_v1",
                "constitution_resolver",
                "midplatform_user_output_constitution_v1",
            ],
            "upstream_object_types": [
                "constitution_constraint_bundle",
                "user_output_candidate",
                "safety_refs",
                "evidence_refs",
                "validation_refs",
                "uncertainty_level",
            ],
            "required_inputs": list(CONSTRAINT_BUNDLE_INTAKE_FIELDS) + list(USER_OUTPUT_INTAKE_FIELDS),
            "optional_inputs": ["risk_flags"],
            "forbidden_inputs": [
                "raw_constitution_clauses",
                "constitution_publish_directive",
                "speech_request_directive",
                "display_render_directive",
                "memory_write_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "speech_gate_later",
                "display_gate_later",
                "user_output_gate_later",
                "no_output_handler_later",
            ],
            "downstream_enforcement_only": True,
            "execution_layer_not_direct_downstream": [
                "voice_output_plane_later",
                "display_output_later",
                "tts_runtime_later",
            ],
            "downstream_object_types": ["safety_gate_result_candidate", "enforcement_result_candidate"],
            "allowed_outputs": ["safety_gate_result_candidate", "enforcement_result_candidate"],
            "forbidden_outputs": [
                "user_facing_output",
                "speech_output",
                "display_output",
                "tts_audio",
                "constitution_publication",
                "memory_fact",
            ],
        },
        "input_contract": {
            "input_contract": "safety_gate_constraint_bundle_intake_contract_v1",
            "source_chain": "preserved_from_bundle_and_user_output",
            "evidence_ref": "preserved",
            "ttl": "required_from_bundle",
            "confidence": "preserved_as_uncertainty_level",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": (
                "enforce safety constraints from constraint_bundle + user_output_candidate; "
                "emit enforcement_result_candidate for execution layer"
            ),
            "allowed_transformation": [
                "apply bundle selected_constraint_action",
                "enforce forbidden_actions and policies",
                "select safety_action from taxonomy",
                "emit allow/block/hold/degrade/require_disclosure/no_output enforcement result",
                "preserve refs and traceability",
            ],
            "forbidden_transformation": [
                "bind raw constitution clauses",
                "publish or modify constitution",
                "replace Constitution Resolver",
                "execute user-facing output",
                "invoke Voice Output Plane / Display Output / TTS runtime",
                "write memory or world model",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "safety_gate_result_candidate_contract_v1",
            "output_object_type": "safety_gate_result_candidate",
            "enforcement_result_alias": "enforcement_result_candidate",
            "execution_layer_consumes_enforcement_result": True,
            "decision_refs": "source_user_output_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_intake",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": list(ENFORCEMENT_LAYER_POSITIONING) + [
                "enforcement_result_candidate ≠ execution output",
            ],
            "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
            "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
            "priority_policy": "bundle policies override personalization",
            "conflict_policy": "forbidden_actions from bundle enforced",
            "fallback_policy": "high risk → block/no_output/escalation",
            "rollback_policy": "enforcer does not commit state or execute output",
        },
        "external_constraints": {
            "constitution_constraints": "via constraint_bundle only; no raw clause binding",
            "domain_standard_constraints": "preserved from bundle",
            "validation_gate_constraints": "validation_refs consumed not re-executed",
            "health_signal_constraints": "risk context optional",
            "whitebox_visibility_constraints": "applicable_rule_refs and trace refs preserved",
            "decision_center_constraints": "does not re-decide upstream decisions",
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
            "failure_route": "block/hold/degrade/no_output/escalation per safety_action",
            "issue_trace": "whitebox_trace_refs preserved",
            "violation_report": "safety_emit_violation_report_candidate path",
            "escalation_path": "owner/Hive later; no invoke now",
            "audit_required": True,
        },
    }


def run_midplatform_safety_gate_planning_v1(
    *,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_output_plane_integration_planning_root: str,
    midplatform_module_definition_template_planning_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    uo_dr_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    output_plan_root = Path(
        midplatform_output_plane_integration_planning_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()
    constitution_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()

    uo_dr_sm = _try_read_json(uo_dr_root / "summary.json") or {}
    uo_dr_vr = _try_read_json(uo_dr_root / "verifier_report.json") or {}
    constraint_bundle = _try_read_json(uo_dr_root / "constitution_constraint_bundle_candidate_v1.json") or {}
    resolver_review = _try_read_json(uo_dr_root / "constitution_resolver_binding_review_v1.json") or {}
    impact_review = _try_read_json(uo_dr_root / "downstream_impact_boundary_review_v1.json") or {}
    sample_user_output = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    output_dr_vr = _try_read_json(output_dr_root / "verifier_report.json") or {}
    output_plan_vr = _try_read_json(output_plan_root / "verifier_report.json") or {}
    constitution_dr_vr = _try_read_json(constitution_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_user_output_constitution_dryrun_root": str(uo_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_output_plane_planning_root": str(output_plan_root),
        "upstream_constitution_dryrun_root": str(constitution_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if uo_dr_vr.get("verifier") != "GO":
        blockers.append("User Output Constitution DryRunAndReview verifier must be GO")
    if uo_dr_sm.get("final_decision") != UPSTREAM_UO_CONST_DR_FINAL:
        blockers.append("user output constitution dryrun final_decision mismatch")
    if uo_dr_sm.get("recommended_next_phase") != UPSTREAM_UO_CONST_DR_NEXT:
        blockers.append("user output constitution dryrun recommended_next_phase mismatch")
    if not constraint_bundle.get("bundle_id"):
        blockers.append("constitution_constraint_bundle_candidate must exist")
    if resolver_review.get("dryrun_and_review_pass") is not True:
        blockers.append("Constitution Resolver binding must pass")
    if impact_review.get("dryrun_and_review_pass") is not True:
        blockers.append("downstream impact boundary must pass")
    if resolver_review.get("downstream_gates_consume_constraint_bundle") is not True:
        blockers.append("Safety Gate must consume constraint_bundle not raw clauses")
    if not sample_user_output.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if sample_user_output.get("user_facing_output_allowed") is not False:
        blockers.append("user_facing_output_allowed must be false")
    if output_dr_vr.get("verifier") != "GO":
        blockers.append("Output Plane DryRunAndReview must be GO")
    if output_plan_vr.get("verifier") != "GO":
        blockers.append("Output Plane Planning must be GO")
    if constitution_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    module_def = _safety_gate_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    constitution_input_review = {
        "review_id": "user_output_constitution_input_review_v1",
        "user_output_constitution_dryrun_verifier": uo_dr_vr.get("verifier"),
        "user_output_constitution_dryrun_final": uo_dr_sm.get("final_decision"),
        "constraint_bundle_present": bool(constraint_bundle.get("bundle_id")),
        "resolver_binding_pass": resolver_review.get("dryrun_and_review_pass") is True,
        "downstream_impact_pass": impact_review.get("dryrun_and_review_pass") is True,
        "consumes_bundle_not_raw_clauses": True,
        "user_output_not_user_facing": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    bundle_intake = {
        "contract_id": "safety_gate_constraint_bundle_intake_contract_v1",
        "required_fields": list(CONSTRAINT_BUNDLE_INTAKE_FIELDS),
        "consumes_bundle_only": True,
        "raw_constitution_clause_binding_forbidden": True,
        "bundle_version_required": True,
        "bundle_ttl_required": True,
        "bundle_source_refs_preserved": True,
        "candidate_only": True,
        **meta,
    }

    user_output_intake = {
        "contract_id": "safety_gate_user_output_candidate_intake_contract_v1",
        "required_fields": list(USER_OUTPUT_INTAKE_FIELDS),
        "defaults": {
            "user_facing_output_allowed": False,
            "speech_request_allowed": False,
            "display_output_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
        },
        **meta,
    }

    result_contract = {
        "contract_id": "safety_gate_result_candidate_contract_v1",
        "output_type": "safety_gate_result_candidate",
        "enforcement_result_alias": "enforcement_result_candidate",
        "required_fields": list(SAFETY_GATE_RESULT_FIELDS),
        "enforcement_result_semantics": {
            "allow": "safety_allow_candidate_forward",
            "block": "safety_block_candidate",
            "hold": "safety_hold_candidate",
            "degrade": "safety_degrade_candidate",
            "require_disclosure": "safety_require_disclosure",
            "no_output": "safety_no_output_candidate",
        },
        "execution_layer_reads": [
            "allowed_downstream_gates",
            "blocked_downstream_gates",
            "required_disclosures",
            "forbidden_actions",
            "applicable_rule_refs",
        ],
        "defaults": {
            "candidate_only": True,
            "user_facing_output_allowed": False,
            "speech_request_allowed": False,
            "display_output_allowed": False,
        },
        "not_execution_output": True,
        **meta,
    }

    action_taxonomy = {
        "taxonomy_id": "safety_gate_action_taxonomy_v1",
        "actions": list(SAFETY_ACTION_TAXONOMY),
        "action_count": len(SAFETY_ACTION_TAXONOMY),
        **meta,
    }

    rule_application = {
        "plan_id": "safety_gate_rule_application_plan_v1",
        "rules": list(RULE_APPLICATION_RULES),
        "rule_count": len(RULE_APPLICATION_RULES),
        "bundle_drives_evaluation": True,
        **meta,
    }

    uncertainty_risk = {
        "policy_id": "safety_gate_uncertainty_risk_policy_v1",
        "rules": list(UNCERTAINTY_RISK_RULES),
        "rule_count": len(UNCERTAINTY_RISK_RULES),
        **meta,
    }

    channel_boundary = {
        "plan_id": "safety_gate_channel_boundary_plan_v1",
        "rules": list(CHANNEL_BOUNDARY_RULES),
        "rule_count": len(CHANNEL_BOUNDARY_RULES),
        "safety_pass_not_speech_or_display": True,
        **meta,
    }

    refusal_hold_degrade = {
        "plan_id": "safety_gate_refusal_hold_degrade_plan_v1",
        "mappings": list(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        "mapping_count": len(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        **meta,
    }

    traceability = {
        "plan_id": "safety_gate_traceability_plan_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        "requirement_count": len(TRACEABILITY_REQUIREMENTS),
        **meta,
    }

    downstream_handoff = {
        "plan_id": "safety_gate_downstream_handoff_plan_v1",
        "handoffs": list(DOWNSTREAM_HANDOFF_MAPPINGS),
        "handoff_count": len(DOWNSTREAM_HANDOFF_MAPPINGS),
        "enforcement_to_enforcement_handoff": True,
        "execution_layer_consumes_enforcement_result": True,
        "speech_gate_enforcement_voice_plane_execution": True,
        "display_gate_enforcement_display_output_execution": True,
        "no_downstream_runtime_invoked_now": True,
        **meta,
    }

    no_raw_binding = {
        "policy_id": "safety_gate_no_raw_constitution_binding_policy_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "rule_count": len(NO_RAW_CONSTITUTION_RULES),
        "consumes_constraint_bundle_only": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "safety_gate_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "safety_gate_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate safety_gate_model_candidate",
            "generate sample constraint_bundle intake",
            "generate sample user_output_candidate intake",
            "generate sample safety_gate_result_candidate",
            "verify safety action taxonomy",
            "verify bundle-only consumption",
            "verify no raw constitution binding",
            "verify safety pass ≠ speech/display/user output",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "safety_gate_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "enforcement_layer_exemplar": list(ENFORCEMENT_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "main_chain_defined": [
            "Rule Source (constitutions / standards / rules)",
            "→ Rule Resolution (Constitution Resolver → constraint_bundle)",
            "→ Enforcement (Safety Gate / Speech Gate / Display Gate …)",
            "→ Execution (Voice Output Plane / Display Output / TTS …)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "safety_gate_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "bundle_only_not_raw_clauses": True,
        "safety_gate_is_enforcement_not_execution": True,
        "enforcement_layer_positioning": list(ENFORCEMENT_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "execution_consumes_enforcement_result_not_constitution": True,
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
        "safety_gate_planning_policy": policy,
        "user_output_constitution_input_review": constitution_input_review,
        "safety_gate_module_definition": module_def,
        "safety_gate_constraint_bundle_intake_contract": bundle_intake,
        "safety_gate_user_output_candidate_intake_contract": user_output_intake,
        "safety_gate_result_candidate_contract": result_contract,
        "safety_gate_action_taxonomy": action_taxonomy,
        "safety_gate_rule_application_plan": rule_application,
        "safety_gate_uncertainty_risk_policy": uncertainty_risk,
        "safety_gate_channel_boundary_plan": channel_boundary,
        "safety_gate_refusal_hold_degrade_plan": refusal_hold_degrade,
        "safety_gate_traceability_plan": traceability,
        "safety_gate_downstream_handoff_plan": downstream_handoff,
        "safety_gate_no_raw_constitution_binding_policy": no_raw_binding,
        "safety_gate_boundary_matrix": boundary_matrix,
        "safety_gate_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "safety_gate_planning_decision": planning_decision,
        "summary": summary,
    }
