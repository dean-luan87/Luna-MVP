# -*- coding: utf-8 -*-
"""Midplatform Validation Engineering Separation Planning v1 — 立法 vs 执法."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL_GO,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as EXPLANATION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    DOMAIN_STANDARD_CATEGORIES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    ALLOWED_CHECKS,
    FINAL_DECISION_GO as OCR_VIA_FACTORY_PLANNING_FINAL_GO,
    FORBIDDEN_ACTIONS,
)

PHASE_ID = "Phase-Midplatform-Validation-Engineering-Separation-Planning-v1-001"
SCOPE = "validation_engineering_separation_planning_only"
SOURCE_CHAIN = "midplatform_validation_engineering_separation_planning_v1"

UPSTREAM_EXPLANATION_DR_FINAL = EXPLANATION_DR_FINAL_GO
UPSTREAM_AUTH_EXT_DR_FINAL = AUTH_EXT_DR_FINAL_GO
UPSTREAM_OCR_VIA_FACTORY_PLANNING_FINAL = OCR_VIA_FACTORY_PLANNING_FINAL_GO

FINAL_DECISION_GO = "MIDPLATFORM_VALIDATION_ENGINEERING_SEPARATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_VALIDATION_ENGINEERING_SEPARATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Validation-Engineering-Separation-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Validation-Engineering-Separation-Issue-Review-v1-001"

CONSTITUTION_ENGINEERING_RESPONSIBILITIES: Tuple[str, ...] = (
    "define General Constitution",
    "define Domain Constitution",
    "define Domain Standard",
    "define Factory Standard",
    "define Authorization Standard",
    "define conflict rules",
    "define amendment workflow",
    "define Hive authority",
    "define personalization boundary",
    "define violation penalty policy",
)

VALIDATION_ENGINEERING_RESPONSIBILITIES: Tuple[str, ...] = (
    "execute gates",
    "inspect candidate / artifact / provider / authorization / boundary",
    "perform health check based on defined health rules",
    "perform no-runtime boundary audit",
    "perform compliance check before Midplatform consumption",
    "trace issue source upstream",
    "generate violation report",
    "generate issue_trace",
    "submit constitution_amendment_candidate_request if rule gap found",
)

RULE_SOURCE_MAPPINGS: Tuple[Tuple[str, str, str], ...] = (
    ("Luna General Constitution", "global_validation_gates", "Constitution Engineering"),
    ("Domain Constitution", "domain_specific_validation_gates", "Constitution Engineering"),
    ("Domain Standard", "input_output_evidence_provider_authorization_checks", "Constitution Engineering"),
    ("Factory Standard", "capability_factory_validation_gates", "Constitution Engineering"),
    ("Factory Authorization Standard", "authorization_validation_gates", "Constitution Engineering"),
    ("Provider Readiness Harness", "provider_model_readiness_checks", "Validation Engineering executor"),
    ("Health Management rules", "health_check_validators", "Constitution defines; Validation executes"),
    ("Validation Factory", "aggregation_inspection_gate_execution", "Validation Engineering"),
)

VALIDATION_ENGINEERING_TYPES: Tuple[Dict[str, str], ...] = (
    {
        "type_id": "validation_factory",
        "label": "Validation Factory",
        "role": "市场检测中心 — 候选、产物、授权、边界、工厂标准合规验收",
    },
    {
        "type_id": "controlled_provider_readiness_harness",
        "label": "ControlledProviderReadinessHarness",
        "role": "机器准入质检员 — provider/model readiness",
    },
    {
        "type_id": "no_runtime_boundary_audit",
        "label": "NoRuntimeBoundaryAudit",
        "role": "安检门 — no runtime / no provider / no write",
    },
    {
        "type_id": "candidate_output_contract_validator",
        "label": "CandidateOutputContractValidator",
        "role": "候选输出质检",
    },
    {
        "type_id": "authorization_validation_gate",
        "label": "AuthorizationValidationGate",
        "role": "授权守门",
    },
    {
        "type_id": "evidence_chain_validator",
        "label": "EvidenceChainValidator",
        "role": "证据链审计",
    },
    {
        "type_id": "health_check_validator",
        "label": "HealthCheckValidator",
        "role": "健康度检查守门",
    },
    {
        "type_id": "issue_traceback_engine",
        "label": "IssueTracebackEngine",
        "role": "问题追溯",
    },
    {
        "type_id": "violation_report_engine",
        "label": "ViolationReportEngine",
        "role": "违规提报",
    },
)

GATE_TYPES: Tuple[str, ...] = (
    "input_gate",
    "output_gate",
    "candidate_gate",
    "evidence_gate",
    "authorization_gate",
    "provider_readiness_gate",
    "health_gate",
    "boundary_gate",
    "runtime_gate",
    "memory_write_gate",
    "worldmodel_write_gate",
    "user_output_gate",
    "midplatform_consumption_gate",
)

ISSUE_TRACEBACK_FIELDS: Tuple[str, ...] = (
    "issue_id",
    "detected_by_validator",
    "failed_gate_id",
    "rule_source_ref",
    "input_object_ref",
    "upstream_source_chain",
    "suspected_source_module",
    "suspected_source_provider",
    "suspected_source_phase",
    "suspected_source_artifact",
    "failure_type",
    "failure_severity",
    "root_cause_candidate",
    "recommended_fix_route",
    "constitution_gap_candidate",
    "evidence_refs",
)

VIOLATION_REPORT_FIELDS: Tuple[str, ...] = (
    "violation_id",
    "violated_constitution_ref",
    "violated_standard_ref",
    "validator_id",
    "source_module",
    "source_provider",
    "triggering_event",
    "failed_gate",
    "severity",
    "action_taken",
    "blocked_action",
    "evidence_ref",
    "traceback_ref",
    "hive_report_required",
    "owner_review_required",
    "rollback_required",
    "quarantine_required",
)

NON_RULEMAKING_RULES: Tuple[str, ...] = (
    "validation_engineering_must_not_create_parallel_standard",
    "validation_engineering_must_reference_rule_source",
    "validation_engineering_cannot_override_constitution",
    "validation_engineering_cannot_grant_authorization",
    "validation_engineering_cannot_execute_provider",
    "validation_engineering_can_only_block_trace_report",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Validation Engineering Planning GO ≠ validator runtime enabled",
    "validator defined ≠ provider check executed",
    "issue traceback contract ≠ issue traced now",
    "violation report contract ≠ violation reported now",
    "feedback loop planning ≠ constitution amended",
    "OCR mapping ≠ OCR authorization granted",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "validation_engineering_runtime_enabled_now",
    "constitution_registry_updated_now",
    "validation_factory_runtime_enforced_now",
    "new_constitution_rule_generated_now",
    "new_validation_rule_generated_now",
    "ocr_authorization_started_now",
    "real_dependency_check_executed_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "amendment_candidate_generated_now",
    "hive_review_submitted_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "validation_engineering_separation_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "constitution_engineering_analogy": "立法系统 / 法律体系 / 宪法工程",
        "validation_engineering_analogy": "质检员 / 警察 / 审计员 / 海关 / 安检",
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["provider_selection_finalized_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _gate_template(gate_id: str, rule_source: str, jurisdiction: str) -> Dict[str, Any]:
    return {
        "gate_id": gate_id,
        "rule_source_ref": rule_source,
        "jurisdiction_scope": jurisdiction,
        "input_object_type": "candidate_or_artifact",
        "pass_condition": "compliant_with_rule_source",
        "fail_condition": "violates_rule_source_or_boundary",
        "blocked_action": "downstream_consumption",
        "evidence_required": True,
        "traceback_required": True,
        "report_required": True,
        "current_runtime_enabled": False,
    }


def run_midplatform_validation_engineering_separation_planning_v1(
    *,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    midplatform_constitution_governance_hierarchy_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_planning_root: str,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    explain_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    explain_dr_sm = _try_read_json(explain_dr_root / "summary.json") or {}
    explain_dr_vr = _try_read_json(explain_dr_root / "verifier_report.json") or {}

    hierarchy_dr_root = Path(
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root
    ).expanduser().resolve()
    hierarchy_dr_vr = _try_read_json(hierarchy_dr_root / "verifier_report.json") or {}

    auth_ext_dr_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
    ).expanduser().resolve()
    auth_ext_dr_sm = _try_read_json(auth_ext_dr_root / "summary.json") or {}
    auth_ext_dr_vr = _try_read_json(auth_ext_dr_root / "verifier_report.json") or {}

    ocr_plan_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_planning_root
    ).expanduser().resolve()
    ocr_plan_sm = _try_read_json(ocr_plan_root / "summary.json") or {}
    ocr_plan_vr = _try_read_json(ocr_plan_root / "verifier_report.json") or {}

    harness_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or explain_dr_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    harness_post_vr = _try_read_json(harness_post_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or explain_dr_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_explanation_dryrun_review_root": str(explain_dr_root),
        "upstream_hierarchy_dryrun_review_root": str(hierarchy_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_dr_root),
        "upstream_ocr_via_factory_planning_root": str(ocr_plan_root),
        "upstream_harness_post_review_root": str(harness_post_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "output_root": str(out_root),
    }

    if explain_dr_vr.get("verifier") != "GO":
        blockers.append("explanation dryrun review must be GO")
    if explain_dr_sm.get("final_decision") != UPSTREAM_EXPLANATION_DR_FINAL:
        blockers.append("explanation dryrun final_decision mismatch")

    if auth_ext_dr_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun review must be GO")
    if auth_ext_dr_sm.get("final_decision") != UPSTREAM_AUTH_EXT_DR_FINAL:
        blockers.append("auth extension dryrun final_decision mismatch")

    if ocr_plan_vr.get("verifier") != "GO":
        blockers.append("ocr via factory standard planning must be GO")
    if ocr_plan_sm.get("final_decision") != UPSTREAM_OCR_VIA_FACTORY_PLANNING_FINAL:
        blockers.append("ocr via factory planning final_decision mismatch")

    if hierarchy_dr_vr.get("verifier") != "GO":
        blockers.append("hierarchy dryrun review must be GO")
    if harness_post_vr.get("verifier") != "GO":
        blockers.append("harness post review must be GO")
    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    upstream_review = {
        "review_id": "upstream_constitution_and_factory_input_review_v1",
        "explanation_dryrun_go": explain_dr_vr.get("verifier") == "GO",
        "auth_extension_dryrun_go": auth_ext_dr_vr.get("verifier") == "GO",
        "ocr_via_factory_planning_go": ocr_plan_vr.get("verifier") == "GO",
        "validation_factory_compliance_layer": True,
        "constitution_and_standard_are_rule_sources": True,
        "validation_and_harness_are_execution_layers": True,
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    constitution_engineering = {
        "definition_id": "constitution_engineering_role_definition_v1",
        "engineering_type": "Constitution Engineering / 宪法工程",
        "analogy": "立法系统、法律体系、最高法理",
        "responsibilities": list(CONSTITUTION_ENGINEERING_RESPONSIBILITIES),
        "writes_rules": True,
        "owns_rule_hierarchy": True,
        "executes_provider_runtime_checks": False,
        "hive_highest_authority_for_general_constitution": True,
        "does_not_execute_validation_gates": True,
        **meta,
    }

    validation_engineering = {
        "definition_id": "validation_engineering_role_definition_v1",
        "engineering_type": "Validation Engineering / 校验工程",
        "analogy": "质检员、警察、审计员、海关、安检",
        "responsibilities": list(VALIDATION_ENGINEERING_RESPONSIBILITIES),
        "executes_rules": True,
        "writes_general_constitution": False,
        "defines_parallel_domain_standard": False,
        "cannot_override_constitution": True,
        "cannot_grant_authorization_by_itself": True,
        "can_generate_violation_report": True,
        "can_generate_issue_trace": True,
        "can_submit_amendment_candidate_request": True,
        "cannot_amend_constitution_directly": True,
        **meta,
    }

    rule_mapping = {
        "mapping_id": "rule_source_to_validator_mapping_v1",
        "mappings": [
            {
                "rule_source": src,
                "validator_scope": scope,
                "owned_by": owner,
            }
            for src, scope, owner in RULE_SOURCE_MAPPINGS
        ],
        "validation_engineering_rule_sources_only_from_constitution_layer": True,
        **meta,
    }

    scope_matrix = {
        "matrix_id": "validation_engineering_scope_matrix_v1",
        "engineering_types": list(VALIDATION_ENGINEERING_TYPES),
        "type_count": len(VALIDATION_ENGINEERING_TYPES),
        **meta,
    }

    gate_taxonomy = {
        "taxonomy_id": "validation_gate_taxonomy_v1",
        "gate_types": list(GATE_TYPES),
        "gates": [
            _gate_template(
                gate_id,
                "Factory Authorization Standard" if gate_id == "authorization_gate" else "Domain Standard",
                "domain" if gate_id in ("input_gate", "output_gate", "evidence_gate") else "platform",
            )
            for gate_id in GATE_TYPES
        ],
        "gate_count": len(GATE_TYPES),
        **meta,
    }

    issue_traceback = {
        "contract_id": "validation_issue_traceback_contract_v1",
        "fields": list(ISSUE_TRACEBACK_FIELDS),
        "traceback_locates_upstream_problem": True,
        "traceback_does_not_auto_fix": True,
        "traceback_does_not_mutate_source_artifact": True,
        **meta,
    }

    violation_report = {
        "contract_id": "validation_violation_report_contract_v1",
        "fields": list(VIOLATION_REPORT_FIELDS),
        **meta,
    }

    health_boundary = {
        "plan_id": "validation_health_check_boundary_plan_v1",
        "consumes": ["Health Management rules", "Constitution rules"],
        "health_metrics_reserved_if_undefined": True,
        "no_numeric_health_score_invented": True,
        "can_emit_health_signal_candidate": True,
        "can_trigger_issue_trace_or_violation_report": True,
        "cannot_auto_repair": True,
        "cannot_auto_switch": True,
        "cannot_auto_authorize": True,
        **meta,
    }

    auth_check_boundary = {
        "plan_id": "validation_authorization_check_boundary_plan_v1",
        "consumes": AUTHORIZATION_STANDARD_ID,
        "ocr_submits_domain_config_only": True,
        "validator_checks": [
            "allowed_checks",
            "forbidden_actions",
            "evidence_refs",
            "rollback_refs",
        ],
        "does_not_generate_request": True,
        "does_not_grant": True,
        "does_not_open_execution_window": True,
        "does_not_execute_check": True,
        **meta,
    }

    feedback_loop = {
        "plan_id": "validation_to_constitution_feedback_loop_plan_v1",
        "flow": [
            "validation failure → issue_trace",
            "repeated validation failure → constitution_review_candidate",
            "rule gap detected → amendment_candidate_request",
            "severe violation → Hive escalation",
            "validator cannot amend constitution directly",
        ],
        "amendment_candidate_generated_now": False,
        "hive_review_submitted_now": False,
        "constitution_registry_updated_now": False,
        **meta,
    }

    non_rulemaking = {
        "policy_id": "validation_engineering_non_rulemaking_policy_v1",
        "core_principle": "校验工程不写法律，只执行法律",
        "rules": {rule: True for rule in NON_RULEMAKING_RULES},
        **meta,
    }

    ocr_mapping = {
        "mapping_id": "ocr_real_dep_validation_engineering_mapping_v1",
        "ocr_domain_config_only": True,
        "mappings": [
            {"ocr_field": "domain_config", "validator": "AuthorizationValidationGate"},
            {"ocr_field": "allowed_checks", "validator": "Factory Authorization Standard validator"},
            {"ocr_field": "forbidden_actions", "validator": "BoundaryGate"},
            {"ocr_field": "provider_candidate_refs", "validator": "ProviderReadinessHarness"},
            {"ocr_field": "evidence_refs", "validator": "EvidenceChainValidator"},
            {"ocr_field": "no-runtime", "validator": "NoRuntimeBoundaryAudit"},
            {"ocr_field": "aggregated", "validator": "Validation Factory"},
            {"ocr_field": "failed_gate", "validator": "IssueTracebackEngine + ViolationReportEngine"},
        ],
        "allowed_checks_from_planning": list(ALLOWED_CHECKS),
        "forbidden_actions_from_planning": list(FORBIDDEN_ACTIONS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "validation_engineering_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "objectives": [
            "generate validation_engineering_model_candidate",
            "verify Constitution / Validation Engineering separation",
            "verify rule_source_to_validator mapping",
            "verify OCR real-dep via validation gates",
            "verify issue traceback / violation report contracts",
            "verify validators do not write rules / grant / execute provider",
        ],
        "dryrun_forbids_runtime": True,
        **meta,
    }

    planning_decision = {
        "decision_id": "validation_engineering_separation_planning_decision_v1",
        "planning_pass": boundary_ok,
        "legislation_vs_enforcement_separated": boundary_ok,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "validation_engineering_separation_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims_reg = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "gate_type_count": len(GATE_TYPES),
        "validation_engineering_type_count": len(VALIDATION_ENGINEERING_TYPES),
        "domain_standard_categories": len(DOMAIN_STANDARD_CATEGORIES),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "validation_engineering_separation_planning_policy": policy,
        "upstream_constitution_and_factory_input_review": upstream_review,
        "constitution_engineering_role_definition": constitution_engineering,
        "validation_engineering_role_definition": validation_engineering,
        "rule_source_to_validator_mapping": rule_mapping,
        "validation_engineering_scope_matrix": scope_matrix,
        "validation_gate_taxonomy": gate_taxonomy,
        "validation_issue_traceback_contract": issue_traceback,
        "validation_violation_report_contract": violation_report,
        "validation_health_check_boundary_plan": health_boundary,
        "validation_authorization_check_boundary_plan": auth_check_boundary,
        "validation_to_constitution_feedback_loop_plan": feedback_loop,
        "validation_engineering_non_rulemaking_policy": non_rulemaking,
        "ocr_real_dep_validation_engineering_mapping": ocr_mapping,
        "validation_engineering_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims_reg,
        "validation_engineering_separation_planning_decision": planning_decision,
        "summary": summary,
    }
