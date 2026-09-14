# -*- coding: utf-8 -*-
"""Midplatform Candidate Evidence Flow Integration Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HEALTH_POST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    FINAL_DECISION_GO as CORE_RESUME_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
    NEXT_PHASE_GO as DC_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_module_definition_template_planning_v1 import (
    FINAL_DECISION_GO as TEMPLATE_PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Candidate-Evidence-Flow-Integration-Planning-v1-001"
SCOPE = "candidate_evidence_flow_integration_planning_only"
SOURCE_CHAIN = "midplatform_candidate_evidence_flow_integration_planning_v1"

UPSTREAM_DC_DR_FINAL = DC_DR_FINAL_GO
UPSTREAM_DC_DR_NEXT = DC_DR_NEXT_PHASE
UPSTREAM_TEMPLATE_FINAL = TEMPLATE_PLANNING_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_CANDIDATE_EVIDENCE_FLOW_INTEGRATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_CANDIDATE_EVIDENCE_FLOW_INTEGRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Candidate-Evidence-Flow-Integration-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Candidate-Evidence-Flow-Integration-Issue-Review-v1-001"

CANDIDATE_TYPES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "transcript_candidate",
    "speech_response_candidate",
    "emotion_state_candidate",
    "face_identity_candidate",
    "scan_result_candidate",
    "navigation_guidance_candidate",
    "generic_domain_candidate",
)

CANDIDATE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "candidate_id",
    "candidate_type",
    "source_domain",
    "source_chain",
    "ttl",
    "confidence_candidate",
    "uncertainty_ref",
    "evidence_refs",
    "candidate_only",
    "fact_status",
    "write_allowed",
    "user_output_allowed",
)

DOMAIN_CONFIG_DOMAINS: Tuple[str, ...] = (
    "OCR",
    "Vision",
    "Voice",
    "Map",
    "Memory",
    "Library",
    "Hive",
)

VALIDATION_RESULT_STATES: Tuple[Dict[str, str], ...] = (
    {"state": "validation_pass", "mapping": "decision_request may proceed"},
    {"state": "validation_fail", "mapping": "decision_request includes fail ref"},
    {"state": "boundary_violation", "mapping": "decision_request includes violation ref"},
    {"state": "evidence_chain_invalid", "mapping": "decision_request includes evidence invalid hint"},
    {"state": "no_validation_result", "mapping": "decision_request includes request_validation hint"},
    {"state": "validation_pending", "mapping": "decision_request includes pending hint"},
)

DECISION_REQUEST_FIELDS: Tuple[str, ...] = (
    "decision_request_id",
    "source_candidate_refs",
    "domain_config_refs",
    "evidence_pack_refs",
    "validation_result_refs",
    "health_signal_refs",
    "constitution_constraint_refs",
    "domain_standard_refs",
    "whitebox_visibility_refs",
    "task_context_ref",
    "uncertainty_ref",
    "issue_trace_refs",
    "violation_report_refs",
    "source_chain",
    "ttl",
    "candidate_only",
)

FLOW_INTEGRITY_RULES: Tuple[str, ...] = (
    "candidate without source_chain → invalid",
    "candidate without ttl → hold/request_validation",
    "stale evidence → request_more_evidence",
    "conflicting evidence → hold/decision_center_conflict",
    "missing validation → request_validation",
    "boundary violation → block path candidate",
    "low confidence → reobserve/hold hint",
    "no fact write from flow integration",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "provider_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Flow Integration Planning GO ≠ runtime enabled",
    "decision_request contract ≠ decision executed",
    "candidate intake ≠ fact write",
    "evidence binding ≠ validation pass",
    "next DryRunAndReview ≠ user output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("candidate_evidence_flow_integration_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "candidate_flow_runtime_enabled_now",
    "evidence_flow_runtime_enabled_now",
    "decision_request_generated_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_candidate_evidence_flow_integration_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "template_id": TEMPLATE_ID,
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


def _flow_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "candidate_evidence_flow_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_candidate_evidence_flow_integration_v1",
            "module_type": "midplatform_flow_integration_module",
            "role": "candidate_evidence_binding_and_decision_request_assembly",
            "system_layer": "Assembly",
        },
        "upstream_sources": {
            "upstream_modules": [
                "Domain / Factory",
                "Validation Engineering",
                "Health Management",
                "Whitebox Engineering",
                "Task Context",
            ],
            "upstream_object_types": [
                "source_candidate_refs",
                "domain_config_refs",
                "evidence_pack_refs",
                "validation_result_refs",
                "health_signal_refs",
                "whitebox_visibility_refs",
                "issue_trace_refs",
                "violation_report_refs",
            ],
            "required_inputs": list(CANDIDATE_REQUIRED_FIELDS),
            "optional_inputs": ["task_context_ref", "risk_flag"],
            "forbidden_inputs": [
                "decision_candidate",
                "task_response_candidate",
                "user_output_directive",
                "memory_write_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": ["midplatform_decision_center_v1"],
            "downstream_object_types": ["decision_request_candidate"],
            "allowed_outputs": ["decision_request_candidate"],
            "forbidden_outputs": [
                "decision_candidate",
                "task_response_candidate",
                "user_output_candidate",
                "memory_fact",
                "world_model_fact",
            ],
        },
        "input_contract": {
            "input_contract": "upstream_candidate_intake_contract_v1",
            "source_chain": "required",
            "evidence_ref": "required_for_binding",
            "ttl": "required",
            "confidence": "required",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": "bind candidates, evidence, validation, health, whitebox into decision_request",
            "allowed_transformation": [
                "bind evidence_pack to source_candidate",
                "attach validation_result refs",
                "attach health_signal context",
                "attach whitebox_visibility refs",
                "assemble decision_request_candidate later",
            ],
            "forbidden_transformation": [
                "arbitrate or decide",
                "execute validation gates",
                "invoke provider",
                "write memory or world model",
                "generate task_response or user output",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "decision_request_assembly_contract_v1",
            "output_object_type": "decision_request_candidate",
            "decision_refs": "none — assembly only",
            "evidence_refs": "preserved",
            "validation_refs": "preserved",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": [
                "原材料流打通：候选进来、证据绑定、校验关联、白盒可见、健康上下文",
                "组装 decision_request_candidate 供 Decision Center 消费",
                "不裁决、不写事实、不输出用户",
            ],
            "priority_policy": "integrity before assembly",
            "conflict_policy": "conflicting evidence → hold hint for decision center",
            "fallback_policy": "missing validation → request_validation hint",
            "rollback_policy": "assembly does not commit state",
        },
        "external_constraints": {
            "constitution_constraints": "constitution_constraint_refs attached at assembly",
            "domain_standard_constraints": "domain_standard_refs from domain_config",
            "validation_gate_constraints": "consume validation results only",
            "health_signal_constraints": "pressure context only; reserved_not_defined",
            "whitebox_visibility_constraints": "rationale refs; whitebox does not decide",
            "decision_center_constraints": "downstream consumer only; no decision here",
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
            "failure_route": "invalid intake → reject assembly; stale → request_more_evidence hint",
            "issue_trace": "issue_trace_refs preserved unchanged",
            "violation_report": "violation_report_refs preserved unchanged",
            "escalation_path": "severe violation marks escalation hint",
            "audit_required": True,
        },
    }


def run_midplatform_candidate_evidence_flow_integration_planning_v1(
    *,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    midplatform_core_architecture_resume_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    dc_dr_root = Path(
        midplatform_decision_center_module_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()
    core_root = Path(midplatform_core_architecture_resume_root).expanduser().resolve()
    val_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    whitebox_root = Path(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root
    ).expanduser().resolve()
    health_root = Path(
        health_management_layer_integration_post_dryrun_review_root
    ).expanduser().resolve()

    dc_dr_sm = _try_read_json(dc_dr_root / "summary.json") or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    template_sm = _try_read_json(template_root / "summary.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}
    core_vr = _try_read_json(core_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    whitebox_vr = _try_read_json(whitebox_root / "verifier_report.json") or {}
    health_sm = _try_read_json(health_root / "summary.json") or {}
    health_vr = _try_read_json(health_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_template_planning_root": str(template_root),
        "upstream_core_resume_root": str(core_root),
        "upstream_validation_dryrun_root": str(val_root),
        "upstream_whitebox_dryrun_root": str(whitebox_root),
        "upstream_health_post_dryrun_root": str(health_root),
        "output_root": str(out_root),
    }

    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module DryRunAndReview verifier must be GO")
    if dc_dr_sm.get("final_decision") != UPSTREAM_DC_DR_FINAL:
        blockers.append("decision center dryrun final_decision mismatch")
    if dc_dr_sm.get("recommended_next_phase") != UPSTREAM_DC_DR_NEXT:
        blockers.append("decision center dryrun recommended_next_phase mismatch")
    if template_vr.get("verifier") != "GO":
        blockers.append("module definition template planning verifier must be GO")
    if template_sm.get("final_decision") != UPSTREAM_TEMPLATE_FINAL:
        blockers.append("template planning final_decision mismatch")
    if template_sm.get("template_established_as_default") is not True:
        blockers.append("template must be established as default")
    if core_vr.get("verifier") != "GO":
        blockers.append("Core Architecture Resume must be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation separation dryrun must be GO")
    if whitebox_vr.get("verifier") != "GO":
        blockers.append("Whitebox dryrun must be GO")
    if health_vr.get("verifier") != "GO":
        blockers.append("Health post dryrun must be GO")

    flow_module = _flow_module_definition()
    module_valid, module_issues = validate_module_definition(flow_module)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    dc_input_review = {
        "review_id": "upstream_decision_center_input_review_v1",
        "decision_center_dryrun_verifier": dc_dr_vr.get("verifier"),
        "decision_center_dryrun_final": dc_dr_sm.get("final_decision"),
        "decision_candidate_not_task_response": True,
        "decision_candidate_not_user_output": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    template_compliance = {
        "review_id": "module_template_compliance_review_v1",
        "template_id": TEMPLATE_ID,
        "template_verifier": template_vr.get("verifier"),
        "ten_section_structure_required": True,
        "flow_module_valid": module_valid,
        "flow_module_issues": module_issues,
        "compliance_pass": module_valid and template_vr.get("verifier") == "GO",
        **meta,
    }

    candidate_intake = {
        "contract_id": "upstream_candidate_intake_contract_v1",
        "supported_candidate_types": list(CANDIDATE_TYPES),
        "required_fields_per_candidate": list(CANDIDATE_REQUIRED_FIELDS),
        "fact_status": "not_fact",
        "candidate_only": True,
        "write_allowed": False,
        "user_output_allowed": False,
        **meta,
    }

    domain_config_intake = {
        "contract_id": "domain_config_intake_contract_v1",
        "domains": list(DOMAIN_CONFIG_DOMAINS),
        "domain_config_provides_domain_constraints_only": True,
        "common_standards_referenced_not_redefined": True,
        "invalid_domain_config_action": "hold/request_validation later",
        **meta,
    }

    evidence_binding = {
        "contract_id": "evidence_pack_binding_contract_v1",
        "required_fields": [
            "evidence_pack_id",
            "source_candidate_refs",
            "source_chain",
            "provenance",
            "confidence_candidate",
            "ttl",
            "validation_required",
            "whitebox_visibility_required",
            "candidate_only",
            "fact_status",
        ],
        "validation_required": True,
        "whitebox_visibility_required": True,
        "fact_status": "not_fact",
        "candidate_only": True,
        **meta,
    }

    validation_binding = {
        "contract_id": "validation_result_binding_contract_v1",
        "supported_states": list(VALIDATION_RESULT_STATES),
        "does_not_execute_validation": True,
        **meta,
    }

    health_binding = {
        "contract_id": "health_signal_binding_contract_v1",
        "health_signal_is_pressure_context": True,
        "no_numeric_health_score_invented": True,
        "health_metric_definition_status": health_sm.get("health_metric_definition_status", "reserved_not_defined"),
        "health_cannot_authorize_by_itself": True,
        "health_marks_risk_pressure_degrade_context": True,
        **meta,
    }

    whitebox_binding = {
        "contract_id": "whitebox_visibility_binding_contract_v1",
        "whitebox_refs_provide_rationale_explainability": True,
        "visibility_layers": ["system", "chain", "factory", "domain", "node"],
        "node_level_cannot_define_global_status": True,
        "whitebox_does_not_decide": True,
        **meta,
    }

    trace_violation_binding = {
        "contract_id": "issue_trace_violation_binding_contract_v1",
        "issue_trace_refs_preserve_upstream_failure": True,
        "violation_report_refs_preserve_enforcement": True,
        "severe_violation_marks_escalation_hint": True,
        "trace_report_do_not_mutate_candidate": True,
        **meta,
    }

    decision_request_assembly = {
        "contract_id": "decision_request_assembly_contract_v1",
        "output_type": "decision_request_candidate",
        "assembled_later_not_now": True,
        "required_fields": list(DECISION_REQUEST_FIELDS),
        "candidate_only": True,
        "downstream_consumer": "midplatform_decision_center_v1",
        **meta,
    }

    integrity_policy = {
        "policy_id": "candidate_evidence_flow_integrity_policy_v1",
        "rules": list(FLOW_INTEGRITY_RULES),
        "no_fact_write": True,
        **meta,
    }

    stale_missing_policy = {
        "policy_id": "stale_missing_conflicting_evidence_policy_v1",
        "stale_evidence_action": "request_more_evidence",
        "missing_validation_action": "request_validation",
        "conflicting_evidence_action": "hold/decision_center_conflict",
        "missing_source_chain_action": "invalid",
        "missing_ttl_action": "hold/request_validation",
        "low_confidence_action": "reobserve/hold hint",
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "candidate_evidence_flow_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "candidate_evidence_flow_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate candidate_evidence_flow_model_candidate",
            "generate sample candidate intake",
            "generate sample evidence binding",
            "generate sample decision_request_candidate",
            "verify refs assembly logic",
            "verify flow integration does not arbitrate/output/write facts",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid and template_compliance.get("compliance_pass") is True

    planning_decision = {
        "decision_id": "candidate_evidence_flow_integration_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "candidate_evidence_flow_integration_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "flow_integration_not_decision": True,
        "assembles_decision_request_not_decision_candidate": True,
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
        "candidate_evidence_flow_integration_planning_policy": policy,
        "upstream_decision_center_input_review": dc_input_review,
        "module_template_compliance_review": template_compliance,
        "candidate_evidence_flow_module_definition": flow_module,
        "upstream_candidate_intake_contract": candidate_intake,
        "domain_config_intake_contract": domain_config_intake,
        "evidence_pack_binding_contract": evidence_binding,
        "validation_result_binding_contract": validation_binding,
        "health_signal_binding_contract": health_binding,
        "whitebox_visibility_binding_contract": whitebox_binding,
        "issue_trace_violation_binding_contract": trace_violation_binding,
        "decision_request_assembly_contract": decision_request_assembly,
        "candidate_evidence_flow_integrity_policy": integrity_policy,
        "stale_missing_conflicting_evidence_policy": stale_missing_policy,
        "candidate_evidence_flow_boundary_matrix": boundary_matrix,
        "candidate_evidence_flow_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "candidate_evidence_flow_integration_planning_decision": planning_decision,
        "summary": summary,
    }
