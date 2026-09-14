# -*- coding: utf-8 -*-
"""Midplatform Module Definition Template v1 — default 10-section module design schema."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

TEMPLATE_ID = "midplatform_module_definition_template_v1"
TEMPLATE_VERSION = "v1"

TEMPLATE_PRINCIPLE = (
    "每个模块都要定义：关系、输入、加工、输出、准则、约束、边界、追溯"
)

TEMPLATE_SECTIONS: Tuple[str, ...] = (
    "module_identity",
    "upstream_sources",
    "downstream_targets",
    "input_contract",
    "processing_scope",
    "output_contract",
    "module_principles",
    "external_constraints",
    "runtime_boundaries",
    "failure_and_traceability",
)

SYSTEM_LAYERS: Tuple[str, ...] = (
    "Constitution",
    "Health",
    "Validation",
    "Whitebox",
    "Decision",
    "Assembly",
    "Output",
    "Domain",
)

INPUT_CONTRACT_BASE_FIELDS: Tuple[str, ...] = (
    "input_contract",
    "source_chain",
    "evidence_ref",
    "ttl",
    "confidence",
    "risk_flag",
    "candidate_only",
)

OUTPUT_CONTRACT_BASE_FIELDS: Tuple[str, ...] = (
    "output_contract",
    "output_object_type",
    "decision_refs",
    "evidence_refs",
    "validation_refs",
    "fact_status",
    "write_allowed",
    "user_output_allowed",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "write_allowed_now",
    "provider_invocation_allowed_now",
    "user_output_allowed_now",
    "memory_allowed_now",
    "world_model_allowed_now",
)

FAILURE_TRACE_FIELDS: Tuple[str, ...] = (
    "failure_route",
    "issue_trace",
    "violation_report",
    "escalation_path",
    "audit_required",
)


def template_schema() -> Dict[str, Any]:
    return {
        "template_id": TEMPLATE_ID,
        "template_version": TEMPLATE_VERSION,
        "template_principle": TEMPLATE_PRINCIPLE,
        "required_sections": list(TEMPLATE_SECTIONS),
        "section_definitions": {
            "module_identity": {
                "required_fields": ["module_id", "module_type", "role", "system_layer"],
                "system_layer_options": list(SYSTEM_LAYERS),
            },
            "upstream_sources": {
                "required_fields": [
                    "upstream_modules",
                    "upstream_object_types",
                    "required_inputs",
                    "optional_inputs",
                    "forbidden_inputs",
                ],
            },
            "downstream_targets": {
                "required_fields": [
                    "downstream_modules",
                    "downstream_object_types",
                    "allowed_outputs",
                    "forbidden_outputs",
                ],
            },
            "input_contract": {
                "required_fields": list(INPUT_CONTRACT_BASE_FIELDS),
            },
            "processing_scope": {
                "required_fields": [
                    "processing_scope",
                    "allowed_transformation",
                    "forbidden_transformation",
                    "arbitration_allowed",
                    "write_allowed",
                    "provider_invocation_allowed",
                ],
            },
            "output_contract": {
                "required_fields": list(OUTPUT_CONTRACT_BASE_FIELDS),
            },
            "module_principles": {
                "required_fields": [
                    "module_principles",
                    "priority_policy",
                    "conflict_policy",
                    "fallback_policy",
                    "rollback_policy",
                ],
            },
            "external_constraints": {
                "required_fields": [
                    "constitution_constraints",
                    "domain_standard_constraints",
                    "validation_gate_constraints",
                    "health_signal_constraints",
                    "whitebox_visibility_constraints",
                    "decision_center_constraints",
                ],
            },
            "runtime_boundaries": {
                "required_fields": list(RUNTIME_BOUNDARY_FIELDS),
            },
            "failure_and_traceability": {
                "required_fields": list(FAILURE_TRACE_FIELDS),
            },
        },
        "adoption_rule": (
            "后续所有中台模块不得只写'这个模块做什么'，"
            "必须按本模板写清模块在系统中的位置"
        ),
    }


def decision_center_exemplar() -> Dict[str, Any]:
    """Full 10-section exemplar for midplatform_decision_center_v1."""
    return {
        "exemplar_id": "decision_center_module_full_definition_exemplar_v1",
        "template_id": TEMPLATE_ID,
        "module_identity": {
            "module_id": "midplatform_decision_center_v1",
            "module_type": "core_midplatform_governance_module",
            "role": "decision_arbitration_and_candidate_routing",
            "system_layer": "Decision",
            "one_liner": "消费宪法、检测、健康度，作综合裁决；不是独立王国",
        },
        "upstream_sources": {
            "upstream_modules": [
                "Constitution Engineering",
                "Validation Engineering",
                "Health Management",
                "Whitebox Engineering",
                "Factory / Domain",
                "Evidence Chain",
                "Task Context",
            ],
            "upstream_object_types": [
                "constitution_constraint_refs",
                "domain_standard_refs",
                "validation_result",
                "health_signal_candidate",
                "whitebox_visibility_refs",
                "domain_config",
                "evidence_pack",
                "source_candidate_refs",
                "task_context_ref",
                "issue_trace",
                "violation_report",
            ],
            "required_inputs": [
                "decision_request_id",
                "source_candidate_refs",
                "source_chain",
                "constitution_constraint_refs",
                "validation_result_refs",
            ],
            "optional_inputs": [
                "health_signal_refs",
                "whitebox_visibility_refs",
                "evidence_pack_refs",
                "task_context_ref",
                "uncertainty_ref",
                "issue_trace_refs",
                "violation_report_refs",
            ],
            "forbidden_inputs": [
                "raw_provider_runtime_output_without_evidence",
                "user_output_directive",
                "memory_write_directive",
                "world_model_write_directive",
                "constitution_rule_draft",
                "validation_gate_execution_request",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "task_response_candidate_integration",
                "issue_traceback_engine",
                "violation_report_engine",
            ],
            "downstream_object_types": [
                "decision_candidate",
                "issue_trace_candidate",
                "violation_report_candidate",
            ],
            "allowed_outputs": [
                "decision_candidate",
                "issue_trace_candidate",
                "violation_report_candidate",
            ],
            "forbidden_outputs": [
                "task_response_candidate",
                "user_output_candidate",
                "memory_fact",
                "world_model_fact",
                "constitution_rule",
                "validation_result",
                "health_metric_definition",
            ],
        },
        "input_contract": {
            "input_contract": "decision_center_input_contract_v1",
            "source_chain": "required",
            "evidence_ref": "required_when_candidate_forward_considered",
            "ttl": "required",
            "confidence": "required",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": "consume governance bindings and emit decision_candidate",
            "allowed_transformation": [
                "aggregate constitution/validation/health/whitebox/evidence signals",
                "select decision action from taxonomy",
                "attach rationale_refs and traceability refs",
            ],
            "forbidden_transformation": [
                "author constitution rules",
                "execute validation gates",
                "invent health score",
                "replace whitebox visibility",
                "invoke provider",
                "assemble task_response",
                "generate user output",
                "write memory or world model",
            ],
            "arbitration_allowed": True,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "decision_center_output_contract_v1",
            "output_object_type": "decision_candidate",
            "decision_refs": "self_ref_as_decision_candidate",
            "evidence_refs": "preserved_from_input",
            "validation_refs": "preserved_from_input",
            "fact_status": "candidate_not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": [
                "宪法定法，检测执法，健康度给压力数据，裁决中心作综合裁决",
                "消费上游，不替代上游",
                "裁决可解释，必须保留 rationale_refs",
            ],
            "priority_policy": "decision_priority_and_conflict_policy_v1",
            "conflict_policy": "constitution > validation > health > evidence > task context > user preference",
            "fallback_policy": "hold_candidate or degrade_mode_candidate on uncertainty",
            "rollback_policy": "decision_candidate does not commit state; downstream integration decides",
        },
        "external_constraints": {
            "constitution_constraints": "consume rule refs; cannot override; block on constitution_block",
            "domain_standard_constraints": "consume domain_standard_refs; domain_config after validation",
            "validation_gate_constraints": "consume pass/fail; does not execute gates",
            "health_signal_constraints": "pressure context only; reserved_not_defined; no score invention",
            "whitebox_visibility_constraints": "rationale and traceability; whitebox does not decide",
            "decision_center_constraints": "n/a — this module is the decision center",
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
            "failure_route": "validation fail → hold/block; boundary violation → violation_report",
            "issue_trace": "emit_issue_trace_candidate on validation/evidence failures",
            "violation_report": "emit_violation_report_candidate on boundary violations",
            "escalation_path": "escalate_to_hive_later / escalate_to_owner_later on severe cases",
            "audit_required": True,
        },
    }


def validate_module_definition(defn: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for section in TEMPLATE_SECTIONS:
        if section not in defn:
            issues.append(f"missing section: {section}")
            continue
        section_def = template_schema()["section_definitions"].get(section, {})
        for field in section_def.get("required_fields", []):
            if field not in defn[section]:
                issues.append(f"missing field {field} in {section}")
    return len(issues) == 0, issues
