# -*- coding: utf-8 -*-
"""Health Enforcement Supervisor Planning v1 — planning only, no supervisor runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_SIGNAL_CONTRACT_FIELDS,
    HEALTH_STATUS_TAXONOMY,
    SEVERITY_TAXONOMY,
)
from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HEALTH_POST_FINAL_GO,
)
from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DISPLAY_DR_FINAL_GO,
    NEXT_PHASE_GO as DISPLAY_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Health-Enforcement-Supervisor-Planning-v1-001"
SCOPE = "health_enforcement_supervisor_planning_only"
SOURCE_CHAIN = "health_enforcement_supervisor_planning_v1"

UPSTREAM_DISPLAY_DR_FINAL = DISPLAY_DR_FINAL_GO
UPSTREAM_DISPLAY_DR_NEXT = DISPLAY_DR_NEXT_PHASE
UPSTREAM_HEALTH_POST_FINAL = HEALTH_POST_FINAL_GO

FINAL_DECISION_GO = "HEALTH_ENFORCEMENT_SUPERVISOR_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "HEALTH_ENFORCEMENT_SUPERVISOR_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Health-Enforcement-Supervisor-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Health-Enforcement-Supervisor-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "health_enforcement_supervision_result_candidate ≠ enforcement override ≠ gate invocation ≠ runtime enable"
)

SUPERVISOR_LAYER_POSITIONING: Tuple[str, ...] = (
    "Health Enforcement Supervisor is a Health Management Layer supervisory module",
    "Supervisor monitors Enforcement Layer gate compliance; it is not an enforcement gate",
    "Supervisor consumes health_signal_candidate and gate result candidates",
    "Supervisor emits health_enforcement_supervision_result_candidate later",
    "Supervisor does not read raw constitution clauses",
    "Supervisor does not invoke Safety / Speech / Display / Authorization / Validation Factory",
    "Supervisor does not override enforcement results or enable runtime",
    "Safety / Speech / Display Gate = Enforcement Layer; Voice / Display Output / TTS = Execution Layer",
)

SUPERVISED_GATES: Tuple[str, ...] = (
    "safety_gate",
    "speech_gate",
    "display_gate",
    "authorization_gate",
    "validation_factory",
)

HEALTH_SIGNAL_INTAKE_FIELDS: Tuple[str, ...] = HEALTH_SIGNAL_CONTRACT_FIELDS

GATE_RESULT_INTAKE_FIELDS: Tuple[str, ...] = (
    "gate_result_candidate_id",
    "gate_module_id",
    "gate_action",
    "gate_status",
    "compliance_status",
    "boundary_violation_flags",
    "bypass_attempt_flags",
    "required_hold_reason",
    "required_degradation",
    "refusal_reason",
    "rationale_refs",
    "evidence_refs",
    "applicable_rule_refs",
    "whitebox_trace_refs",
    "candidate_only",
)

SUPERVISION_RESULT_FIELDS: Tuple[str, ...] = (
    "health_enforcement_supervision_result_candidate_id",
    "source_health_signal_refs",
    "source_gate_result_refs",
    "supervision_action",
    "supervision_status",
    "enforcement_compliance_ok",
    "boundary_violation_detected",
    "bypass_attempt_detected",
    "recommended_hold",
    "recommended_degrade",
    "recommended_no_runtime",
    "recommended_escalation",
    "forbidden_supervisor_actions",
    "rationale_refs",
    "evidence_refs",
    "applicable_rule_refs",
    "whitebox_trace_refs",
    "candidate_only",
)

SUPERVISION_ACTION_TAXONOMY: Tuple[str, ...] = (
    "supervise_compliance_ok_candidate",
    "supervise_gate_degraded_candidate",
    "supervise_gate_failure_candidate",
    "supervise_boundary_violation_candidate",
    "supervise_bypass_attempt_blocked_candidate",
    "supervise_enforcement_hold_recommended_candidate",
    "supervise_enforcement_degrade_recommended_candidate",
    "supervise_runtime_not_recommended_candidate",
    "supervise_escalation_recommended_candidate",
    "supervise_health_signal_attached_candidate",
    "supervise_request_more_evidence_candidate",
    "supervise_emit_violation_report_candidate",
)

GATE_COMPLIANCE_MONITORING_RULES: Tuple[str, ...] = (
    "supervisor observes gate result candidates without re-executing gates",
    "safety_gate compliance required before speech/display path recommendation",
    "speech_gate compliance required before voice output path recommendation",
    "display_gate compliance required before display output path recommendation",
    "authorization_gate compliance required before privileged runtime recommendation",
    "validation_factory compliance required before candidate promotion recommendation",
    "gate failure surfaces as supervision failure candidate not runtime enable",
)

HEALTH_SIGNAL_BINDING_RULES: Tuple[str, ...] = (
    "health_signal_candidate may recommend hold/degrade/no_runtime",
    "health severity may elevate supervision action but not override enforcement",
    "provider_not_ready health signal recommends runtime_not_recommended",
    "resource_pressure health signal recommends degrade candidate",
    "gate_failure health signal recommends hold candidate",
    "health signal binding is candidate-only not automatic execution",
)

BOUNDARY_VIOLATION_DETECTION_RULES: Tuple[str, ...] = (
    "detect execution layer reading raw constitution",
    "detect execution layer bypassing enforcement gate results",
    "detect gate result schema mismatch or missing refs",
    "detect enforcement_result used without source refs",
    "detect display/speech path opened without prior gate pass candidate",
    "detect provider invoked without readiness/authorization candidate",
)

BYPASS_PREVENTION_RULES: Tuple[str, ...] = (
    "supervisor must flag bypass attempts as blocked candidate",
    "supervisor cannot authorize bypass of Safety Gate",
    "supervisor cannot authorize bypass of Speech Gate",
    "supervisor cannot authorize bypass of Display Gate",
    "supervisor cannot authorize direct TTS/runtime from enforcement skip",
    "bypass detection is observational not punitive execution",
)

ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES: Tuple[str, ...] = (
    "supervisor cannot override safety_gate_result_candidate",
    "supervisor cannot override speech_gate_result_candidate",
    "supervisor cannot override display_gate_result_candidate",
    "supervisor cannot rewrite enforcement_result_candidate",
    "supervisor recommendations are candidate-only",
    "enforcement layer remains authoritative for allow/block/hold/degrade",
)

RUNTIME_RECOMMENDATION_RULES: Tuple[str, ...] = (
    "supervision pass ≠ runtime enabled",
    "supervision degrade recommendation ≠ degradation executed",
    "supervision hold recommendation ≠ hold executed",
    "runtime_not_recommended is valid supervision outcome",
    "controlled runtime planning consumes supervision result later",
    "no provider/model invocation from supervisor planning",
)

DEGRADATION_HOLD_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"health_signal": "degraded", "supervision_path": "supervise_enforcement_degrade_recommended_candidate"},
    {"health_signal": "critical", "supervision_path": "supervise_enforcement_hold_recommended_candidate"},
    {"health_signal": "blocked", "supervision_path": "supervise_runtime_not_recommended_candidate"},
    {"gate_signal": "gate_failure", "supervision_path": "supervise_gate_failure_candidate"},
    {"gate_signal": "boundary_violation", "supervision_path": "supervise_boundary_violation_candidate"},
    {"gate_signal": "bypass_attempt", "supervision_path": "supervise_bypass_attempt_blocked_candidate"},
)

DOWNSTREAM_HANDOFF_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"supervision_action": "supervise_compliance_ok_candidate", "handoff": "Controlled Runtime Planning later"},
    {"supervision_action": "supervise_runtime_not_recommended_candidate", "handoff": "hold/no_runtime path later"},
    {"supervision_action": "supervise_enforcement_hold_recommended_candidate", "handoff": "hold path later"},
    {"supervision_action": "supervise_enforcement_degrade_recommended_candidate", "handoff": "degrade path later"},
    {"supervision_action": "supervise_emit_violation_report_candidate", "handoff": "violation report path later"},
)

NO_RAW_CONSTITUTION_RULES: Tuple[str, ...] = (
    "supervisor does not bind raw constitution clauses",
    "supervisor consumes gate results and health signals only",
    "constitution changes flow through Resolver / constraint_bundle / gates",
    "supervisor retains rule refs for Whitebox audit only",
    "breaking gate result schema requires compatibility phase",
)

TRACEABILITY_REQUIREMENTS: Tuple[str, ...] = (
    "source_health_signal_refs preserved",
    "source_gate_result_refs preserved",
    "applicable_rule_refs preserved",
    "evidence_refs preserved",
    "rationale_refs preserved",
    "whitebox_trace_refs preserved",
    "supervision action reason auditable",
    "compliance/bypass/violation reason auditable",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "health_enforcement_supervisor_runtime_enabled_now",
    "health_enforcement_supervisor_invoked_now",
    "supervision_result_generated_now",
    "enforcement_result_overridden_now",
    "gate_invoked_by_supervisor_now",
    "safety_gate_bypassed_now",
    "speech_gate_bypassed_now",
    "display_gate_bypassed_now",
    "enforcement_layer_bypassed_now",
    "runtime_enabled_now",
    "controlled_runtime_planning_started_now",
    "automatic_degradation_executed_now",
    "fallback_executed_now",
    "health_signal_generated_now",
    "model_runtime_invoked_now",
    "provider_invoked_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "raw_constitution_clause_bound_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Health Enforcement Supervisor Planning GO ≠ supervisor runtime enabled",
    "supervision result planned ≠ enforcement override",
    "compliance monitoring planned ≠ gate re-execution",
    "degrade/hold recommendation planned ≠ degradation/hold executed",
    "next DryRunAndReview ≠ controlled runtime enabled",
    "health signal contract consumed ≠ health monitor running",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("health_enforcement_supervisor_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_enforcement_supervisor_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "template_id": TEMPLATE_ID,
        "core_chain_boundary": CORE_CHAIN_BOUNDARY,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "health_metric_definition_status": "reserved_not_defined",
        "controlled_runtime_deferred_not_cancelled": True,
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


def _supervisor_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "health_enforcement_supervisor_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "health_enforcement_supervisor_v1",
            "module_type": "health_management_supervisory_module",
            "role": "enforcement_layer_health_supervisor",
            "system_layer": "Health Management",
            "architectural_layer": "Supervision",
            "runtime_enabled_now": False,
            "layer_positioning": (
                "Health Enforcement Supervisor is a supervisory module in Health Management Layer"
            ),
        },
        "upstream_sources": {
            "upstream_modules": [
                "health_management_layer",
                "safety_gate",
                "speech_gate",
                "display_gate",
                "authorization_gate",
                "validation_factory",
            ],
            "upstream_object_types": [
                "health_signal_candidate",
                "safety_gate_result_candidate",
                "speech_gate_result_candidate",
                "display_gate_result_candidate",
                "authorization_gate_result_candidate",
                "validation_factory_result_candidate",
            ],
            "required_inputs": list(HEALTH_SIGNAL_INTAKE_FIELDS) + list(GATE_RESULT_INTAKE_FIELDS),
            "optional_inputs": ["provider_abstraction_status", "whitebox_trace_bundle"],
            "forbidden_inputs": [
                "raw_constitution_clauses",
                "constitution_publish_directive",
                "gate_invocation_directive",
                "enforcement_override_directive",
                "runtime_enable_directive",
                "provider_invocation_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "controlled_runtime_planning_later",
                "decision_center_later",
                "whitebox_audit_later",
            ],
            "downstream_object_types": ["health_enforcement_supervision_result_candidate"],
            "allowed_outputs": ["health_enforcement_supervision_result_candidate"],
            "forbidden_outputs": [
                "enforcement_result_candidate",
                "gate_invocation",
                "runtime_enable",
                "provider_invocation",
                "user_facing_output",
            ],
        },
        "input_contract": {
            "input_contract": "health_enforcement_supervisor_intake_contract_v1",
            "source_chain": "preserved_from_health_and_gate_results",
            "evidence_ref": "preserved",
            "ttl": "required_from_health_signal",
            "confidence": "preserved_from_gate_results",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": (
                "observe enforcement gate compliance and health context; "
                "emit health_enforcement_supervision_result_candidate for downstream planning"
            ),
            "allowed_transformation": [
                "assess gate compliance from gate result candidates",
                "bind health_signal_candidate context to supervision outcome",
                "detect boundary violations and bypass attempts as candidates",
                "recommend hold/degrade/no_runtime/escalation as candidates",
                "preserve refs and traceability",
            ],
            "forbidden_transformation": [
                "bind raw constitution clauses",
                "invoke enforcement gates",
                "override gate results",
                "enable runtime or provider",
                "execute degradation/hold/fallback",
                "write memory or world model",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "health_enforcement_supervision_result_candidate_contract_v1",
            "output_object_type": "health_enforcement_supervision_result_candidate",
            "controlled_runtime_planning_consumes_later": True,
            "decision_refs": "source_gate_result_refs",
            "evidence_refs": "preserved",
            "validation_refs": "preserved_from_intake",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
            "runtime_enable_allowed": False,
        },
        "module_principles": {
            "module_principles": list(SUPERVISOR_LAYER_POSITIONING),
            "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
            "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
            "supervised_gates": list(SUPERVISED_GATES),
            "priority_policy": "enforcement gate results remain authoritative",
            "conflict_policy": "supervisor recommends only; cannot override enforcement",
            "fallback_policy": "gate failure or health critical → hold/no_runtime recommendation",
            "rollback_policy": "supervisor does not commit state or enable runtime",
        },
        "external_constraints": {
            "constitution_constraints": "via gate results only; no raw clause binding",
            "domain_standard_constraints": "preserved from gate result refs",
            "validation_gate_constraints": "validation_refs consumed not re-executed",
            "health_signal_constraints": "severity/status taxonomy consumed not executed",
            "whitebox_visibility_constraints": "trace refs preserved for audit",
            "decision_center_constraints": "does not re-decide upstream enforcement",
        },
        "runtime_boundaries": {
            "runtime_enabled_now": False,
            "write_allowed_now": False,
            "provider_invocation_allowed_now": False,
            "gate_invocation_allowed_now": False,
            "enforcement_override_allowed_now": False,
            "user_output_allowed_now": False,
            "memory_allowed_now": False,
            "world_model_allowed_now": False,
        },
        "failure_and_traceability": {
            "failure_route": "violation/bypass/gate_failure/no_runtime recommendation paths",
            "issue_trace": "whitebox_trace_refs preserved",
            "violation_report": "supervise_emit_violation_report_candidate path",
            "escalation_path": "owner later; no invoke now",
            "audit_required": True,
        },
    }


def run_health_enforcement_supervisor_planning_v1(
    *,
    midplatform_display_gate_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    health_management_layer_integration_dryrun_root: Optional[str] = None,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    display_dr_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
    ).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    template_root = Path(midplatform_module_definition_template_planning_root).expanduser().resolve()

    display_dr_sm = _try_read_json(display_dr_root / "summary.json") or {}
    display_dr_vr = _try_read_json(display_dr_root / "verifier_report.json") or {}
    display_model = _try_read_json(display_dr_root / "display_gate_model_candidate_v1.json") or {}
    next_route = _try_read_json(display_dr_root / "next_route_readiness_decision_v1.json") or {}

    health_post_sm = _try_read_json(health_post_root / "summary.json") or {}
    health_post_vr = _try_read_json(health_post_root / "verifier_report.json") or {}

    health_dryrun_root = Path(
        health_management_layer_integration_dryrun_root
        or health_post_sm.get("upstream_dryrun_root")
        or health_post_root.parent / "health_management_layer_integration_dryrun"
    ).expanduser().resolve()
    health_dryrun_vr = _try_read_json(health_dryrun_root / "verifier_report.json") or {}

    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    fmis_vr: Dict[str, Any] = {}
    if midplatform_frontend_model_influence_simulation_dryrun_and_review_root:
        fmis_root = Path(
            midplatform_frontend_model_influence_simulation_dryrun_and_review_root
        ).expanduser().resolve()
        fmis_vr = _try_read_json(fmis_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_display_gate_dryrun_root": str(display_dr_root),
        "upstream_health_post_dryrun_review_root": str(health_post_root),
        "upstream_health_dryrun_root": str(health_dryrun_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if display_dr_vr.get("verifier") != "GO":
        blockers.append("Display Gate DryRunAndReview verifier must be GO")
    if display_dr_sm.get("final_decision") != UPSTREAM_DISPLAY_DR_FINAL:
        blockers.append("display gate dryrun final_decision mismatch")
    if display_dr_sm.get("recommended_next_phase") != UPSTREAM_DISPLAY_DR_NEXT:
        blockers.append("display gate dryrun recommended_next_phase mismatch")
    if next_route.get("ready_for_health_enforcement_supervisor_planning") is not True:
        blockers.append("display gate dryrun must be ready for health enforcement supervisor planning")
    if health_post_vr.get("verifier") != "GO":
        blockers.append("Health Management Post-DryRun Review verifier must be GO")
    if health_post_sm.get("final_decision") != UPSTREAM_HEALTH_POST_FINAL:
        blockers.append("health management post dryrun final_decision mismatch")
    if health_dryrun_vr.get("verifier") != "GO":
        blockers.append("Health Management Integration DryRun must be GO")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview must be GO")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")
    if display_model.get("architectural_layer") != "Enforcement":
        blockers.append("display gate must remain Enforcement Layer")

    module_def = _supervisor_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    display_input_review = {
        "review_id": "display_gate_dryrun_input_review_v1",
        "display_gate_dryrun_verifier": display_dr_vr.get("verifier"),
        "display_gate_dryrun_final_decision": display_dr_sm.get("final_decision"),
        "ready_for_health_enforcement_supervisor_planning": next_route.get(
            "ready_for_health_enforcement_supervisor_planning"
        ),
        "display_gate_is_enforcement_layer": display_model.get("architectural_layer") == "Enforcement",
        "supervisor_is_not_enforcement_gate": True,
        "supervisor_monitors_enforcement_compliance": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    health_input_review = {
        "review_id": "health_management_input_review_v1",
        "health_post_dryrun_verifier": health_post_vr.get("verifier"),
        "health_post_final_decision": health_post_sm.get("final_decision"),
        "health_dryrun_verifier": health_dryrun_vr.get("verifier"),
        "health_signal_contract_available": True,
        "health_metric_reserved_not_defined": True,
        "fmis_dryrun_verifier": fmis_vr.get("verifier"),
        "health_influence_on_front_model_validated": fmis_vr.get("verifier") == "GO",
        "review_pass": input_ok,
        **meta,
    }

    health_signal_intake = {
        "contract_id": "health_enforcement_supervisor_health_signal_intake_contract_v1",
        "required_fields": list(HEALTH_SIGNAL_INTAKE_FIELDS),
        "severity_taxonomy": list(SEVERITY_TAXONOMY),
        "health_status_taxonomy": list(HEALTH_STATUS_TAXONOMY),
        "candidate_only": True,
        "health_signal_generated_now": False,
        **meta,
    }

    gate_result_intake = {
        "contract_id": "health_enforcement_supervisor_gate_result_intake_contract_v1",
        "required_fields": list(GATE_RESULT_INTAKE_FIELDS),
        "supervised_gates": list(SUPERVISED_GATES),
        "consumes_gate_results_only": True,
        "raw_constitution_clause_binding_forbidden": True,
        "candidate_only": True,
        **meta,
    }

    result_contract = {
        "contract_id": "health_enforcement_supervision_result_candidate_contract_v1",
        "output_type": "health_enforcement_supervision_result_candidate",
        "required_fields": list(SUPERVISION_RESULT_FIELDS),
        "supervision_semantics": {
            "compliance_ok": "supervise_compliance_ok_candidate",
            "gate_failure": "supervise_gate_failure_candidate",
            "boundary_violation": "supervise_boundary_violation_candidate",
            "bypass_blocked": "supervise_bypass_attempt_blocked_candidate",
            "hold_recommended": "supervise_enforcement_hold_recommended_candidate",
            "degrade_recommended": "supervise_enforcement_degrade_recommended_candidate",
            "no_runtime": "supervise_runtime_not_recommended_candidate",
        },
        "defaults": {
            "candidate_only": True,
            "enforcement_compliance_ok": False,
            "runtime_enable_allowed": False,
        },
        "not_runtime_output": True,
        **meta,
    }

    action_taxonomy = {
        "taxonomy_id": "health_enforcement_supervision_action_taxonomy_v1",
        "actions": list(SUPERVISION_ACTION_TAXONOMY),
        "action_count": len(SUPERVISION_ACTION_TAXONOMY),
        **meta,
    }

    compliance_monitoring = {
        "plan_id": "gate_compliance_monitoring_rule_plan_v1",
        "rules": list(GATE_COMPLIANCE_MONITORING_RULES),
        "rule_count": len(GATE_COMPLIANCE_MONITORING_RULES),
        "supervised_gates": list(SUPERVISED_GATES),
        **meta,
    }

    health_signal_binding = {
        "plan_id": "health_signal_binding_rule_plan_v1",
        "rules": list(HEALTH_SIGNAL_BINDING_RULES),
        "rule_count": len(HEALTH_SIGNAL_BINDING_RULES),
        **meta,
    }

    boundary_violation = {
        "plan_id": "boundary_violation_detection_rule_plan_v1",
        "rules": list(BOUNDARY_VIOLATION_DETECTION_RULES),
        "rule_count": len(BOUNDARY_VIOLATION_DETECTION_RULES),
        **meta,
    }

    bypass_prevention = {
        "plan_id": "bypass_prevention_rule_plan_v1",
        "rules": list(BYPASS_PREVENTION_RULES),
        "rule_count": len(BYPASS_PREVENTION_RULES),
        **meta,
    }

    override_forbidden = {
        "plan_id": "enforcement_override_forbidden_rule_plan_v1",
        "rules": list(ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES),
        "rule_count": len(ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES),
        **meta,
    }

    runtime_recommendation = {
        "plan_id": "runtime_recommendation_rule_plan_v1",
        "rules": list(RUNTIME_RECOMMENDATION_RULES),
        "rule_count": len(RUNTIME_RECOMMENDATION_RULES),
        **meta,
    }

    degrade_hold = {
        "plan_id": "health_enforcement_degrade_hold_plan_v1",
        "mappings": list(DEGRADATION_HOLD_MAPPINGS),
        "mapping_count": len(DEGRADATION_HOLD_MAPPINGS),
        **meta,
    }

    downstream_handoff = {
        "plan_id": "health_enforcement_supervisor_downstream_handoff_plan_v1",
        "handoffs": list(DOWNSTREAM_HANDOFF_MAPPINGS),
        "handoff_count": len(DOWNSTREAM_HANDOFF_MAPPINGS),
        "supervision_not_runtime_enable": True,
        "controlled_runtime_planning_consumes_later": True,
        **meta,
    }

    no_raw_binding = {
        "policy_id": "health_enforcement_supervisor_no_raw_constitution_binding_policy_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "rule_count": len(NO_RAW_CONSTITUTION_RULES),
        "consumes_gate_results_and_health_signals_only": True,
        **meta,
    }

    traceability = {
        "plan_id": "health_enforcement_supervisor_traceability_plan_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        "requirement_count": len(TRACEABILITY_REQUIREMENTS),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "health_enforcement_supervisor_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "health_enforcement_supervisor_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate health_enforcement_supervisor_model_candidate",
            "generate sample health_signal intake",
            "generate sample gate_result intake bundle",
            "generate sample health_enforcement_supervision_result_candidate",
            "verify supervisor as Health Management supervisory module",
            "verify no raw constitution binding",
            "verify supervisor ≠ gate invocation ≠ enforcement override",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "health_enforcement_supervisor_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "supervisor_layer_positioning": list(SUPERVISOR_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "supervised_gates": list(SUPERVISED_GATES),
        "main_chain_defined": [
            "Health Management (health_signal_candidate)",
            "→ Enforcement Layer gate results (Safety / Speech / Display / Authorization / Validation)",
            "→ Health Enforcement Supervisor (compliance observation)",
            "→ health_enforcement_supervision_result_candidate",
            "→ Controlled Runtime Planning later (not now)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "health_enforcement_supervisor_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "gate_results_and_health_signals_only_not_raw_clauses": True,
        "supervisor_is_supervisory_not_enforcement": True,
        "supervisor_layer_positioning": list(SUPERVISOR_LAYER_POSITIONING),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "controlled_runtime_consumes_supervision_result_later": True,
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
        "health_enforcement_supervisor_planning_policy": policy,
        "display_gate_dryrun_input_review": display_input_review,
        "health_management_input_review": health_input_review,
        "health_enforcement_supervisor_module_definition": module_def,
        "health_enforcement_supervisor_health_signal_intake_contract": health_signal_intake,
        "health_enforcement_supervisor_gate_result_intake_contract": gate_result_intake,
        "health_enforcement_supervision_result_candidate_contract": result_contract,
        "health_enforcement_supervision_action_taxonomy": action_taxonomy,
        "gate_compliance_monitoring_rule_plan": compliance_monitoring,
        "health_signal_binding_rule_plan": health_signal_binding,
        "boundary_violation_detection_rule_plan": boundary_violation,
        "bypass_prevention_rule_plan": bypass_prevention,
        "enforcement_override_forbidden_rule_plan": override_forbidden,
        "runtime_recommendation_rule_plan": runtime_recommendation,
        "health_enforcement_degrade_hold_plan": degrade_hold,
        "health_enforcement_supervisor_downstream_handoff_plan": downstream_handoff,
        "health_enforcement_supervisor_no_raw_constitution_binding_policy": no_raw_binding,
        "health_enforcement_supervisor_traceability_plan": traceability,
        "health_enforcement_supervisor_boundary_matrix": boundary_matrix,
        "health_enforcement_supervisor_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "health_enforcement_supervisor_planning_decision": planning_decision,
        "summary": summary,
    }
