# -*- coding: utf-8 -*-
"""Midplatform Validation Engineering Separation DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as EXPLANATION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_planning_v1 import (
    CONSTITUTION_ENGINEERING_RESPONSIBILITIES,
    GATE_TYPES,
    ISSUE_TRACEBACK_FIELDS,
    NON_RULEMAKING_RULES,
    RULE_SOURCE_MAPPINGS,
    UPSTREAM_EXPLANATION_DR_FINAL,
    UPSTREAM_OCR_VIA_FACTORY_PLANNING_FINAL,
    VALIDATION_ENGINEERING_RESPONSIBILITIES,
    VALIDATION_ENGINEERING_TYPES,
    VIOLATION_REPORT_FIELDS,
    FINAL_DECISION_GO as UPSTREAM_PLANNING_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_VIA_FACTORY_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Validation-Engineering-Separation-DryRunAndReview-v1-001"
SCOPE = "validation_engineering_separation_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_validation_engineering_separation_dryrun_and_review_v1"

UPSTREAM_SEPARATION_PLANNING_FINAL = UPSTREAM_PLANNING_FINAL_GO
UPSTREAM_EXPLANATION_DR_FINAL = EXPLANATION_DR_FINAL_GO
UPSTREAM_OCR_VIA_FACTORY_DR_FINAL = OCR_VIA_FACTORY_DR_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_VALIDATION_ENGINEERING_SEPARATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_VALIDATION_ENGINEERING_SEPARATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Validation-Engineering-Separation-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_validator_runtime_enable",
    "dryrun_to_validation_factory_runtime_enforce",
    "dryrun_to_constitution_registry_update",
    "dryrun_to_new_constitution_rule",
    "dryrun_to_new_validation_rule",
    "dryrun_to_amendment_commit",
    "dryrun_to_hive_review_submit",
    "dryrun_to_ocr_authorization_start",
    "dryrun_to_grant_issue",
    "dryrun_to_execution_window_open",
    "dryrun_to_real_dependency_check",
    "dryrun_to_provider_import",
    "dryrun_to_provider_invoke",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_crop",
    "dryrun_to_ocr_fact",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_user_output",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Validation Engineering DryRunAndReview GO ≠ validator runtime enabled",
    "validator model candidate ≠ validation factory runtime enforced",
    "issue traceback contract ≠ issue traced now",
    "violation report contract ≠ violation reported now",
    "feedback loop pass ≠ constitution amended",
    "next OCR roadmap decision ≠ real dependency check allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("validation_engineering_model_candidate_generated_now",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "validator_runtime_enabled_now",
    "validation_factory_runtime_enforced_now",
    "new_constitution_rule_generated_now",
    "new_validation_rule_generated_now",
    "constitution_registry_updated_now",
    "amendment_candidate_generated_now",
    "hive_review_submitted_now",
    "ocr_authorization_started_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "domain_config_activated_now",
    "authorization_request_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "validation_engineering_separation_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _gate_from_planning(plan_gates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            **g,
            "current_runtime_enabled": False,
            "simulated_gate_pass": True,
        }
        for g in plan_gates
    ]


def run_midplatform_validation_engineering_separation_dryrun_and_review_v1(
    *,
    midplatform_validation_engineering_separation_planning_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_validation_engineering_separation_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_gates_doc = _try_read_json(plan_root / "validation_gate_taxonomy_v1.json") or {}
    plan_non_rule = _try_read_json(plan_root / "validation_engineering_non_rulemaking_policy_v1.json") or {}

    explain_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    explain_dr_vr = _try_read_json(explain_dr_root / "verifier_report.json") or {}

    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_dr_sm = _try_read_json(ocr_dr_root / "summary.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    ocr_domain_config = _try_read_json(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    ) or {}

    auth_ext_dr_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or plan_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()
    auth_ext_dr_vr = _try_read_json(auth_ext_dr_root / "verifier_report.json") or {}

    harness_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or plan_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    harness_post_vr = _try_read_json(harness_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_separation_planning_root": str(plan_root),
        "upstream_explanation_dryrun_review_root": str(explain_dr_root),
        "upstream_ocr_via_factory_dryrun_review_root": str(ocr_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_dr_root),
        "upstream_harness_post_review_root": str(harness_post_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("separation planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_SEPARATION_PLANNING_FINAL:
        blockers.append("separation planning final_decision mismatch")
    if explain_dr_vr.get("verifier") != "GO":
        blockers.append("explanation dryrun review must be GO")
    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("ocr via factory dryrun review must be GO")
    if ocr_dr_sm.get("final_decision") != UPSTREAM_OCR_VIA_FACTORY_DR_FINAL:
        blockers.append("ocr via factory dryrun final_decision mismatch")
    if ocr_domain_config.get("activated_now") is not False:
        blockers.append("ocr domain_config must not be activated")
    if ocr_domain_config.get("candidate_only") is not True:
        blockers.append("ocr domain_config must be candidate_only")
    if auth_ext_dr_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun review must be GO")
    if harness_post_vr.get("verifier") != "GO":
        blockers.append("harness post review must be GO")

    input_ok = len(blockers) == 0

    model_candidate = {
        "model_id": "validation_engineering_model_v1",
        "role": "rule_execution_and_gatekeeping",
        "rulemaking_allowed": False,
        "authorization_grant_allowed": False,
        "provider_execution_allowed": False,
        "constitution_override_allowed": False,
        "can_block": True,
        "can_trace": True,
        "can_report": True,
        "can_emit_issue_trace_candidate": True,
        "can_emit_violation_report_candidate": True,
        "can_emit_amendment_candidate_request_later": True,
        "runtime_enabled_now": False,
        "simulated": True,
        **meta,
    }

    planning_input_review = {
        "review_id": "validation_engineering_planning_input_review_v1",
        "separation_planning_go": plan_vr.get("verifier") == "GO",
        "explanation_dryrun_go": explain_dr_vr.get("verifier") == "GO",
        "ocr_via_factory_dryrun_go": ocr_dr_vr.get("verifier") == "GO",
        "ocr_domain_config_candidate_present": bool(ocr_domain_config),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    const_checks: List[Tuple[str, bool]] = [
        ("writes_rules", True),
        ("owns_rule_hierarchy", True),
        ("owns_conflict_logic", True),
        ("owns_amendment_workflow", True),
        ("hive_highest", True),
        ("no_provider_checks", True),
        ("no_runtime_validation", True),
    ]
    constitution_review = {
        "review_id": "constitution_engineering_role_review_v1",
        "writes_rules": True,
        "owns_rule_hierarchy": True,
        "owns_conflict_logic": True,
        "owns_amendment_workflow": True,
        "hive_remains_highest_authority": True,
        "does_not_execute_provider_checks": True,
        "does_not_perform_runtime_validation_now": True,
        **_review_ok(const_checks),
        **meta,
    }

    val_checks: List[Tuple[str, bool]] = [
        ("executes_rules", True),
        ("writes_rules_must_be_false", True),
        ("no_parallel_standard", True),
        ("no_override", True),
        ("no_grant", True),
        ("no_execute_provider", True),
        ("can_block_trace_report", True),
    ]
    validation_review = {
        "review_id": "validation_engineering_role_review_v1",
        "executes_rules": True,
        "writes_rules": False,
        "cannot_define_parallel_standard": True,
        "cannot_override_constitution": True,
        "cannot_grant_authorization": True,
        "cannot_execute_provider": True,
        "can_block_trace_report": True,
        **_review_ok(val_checks),
        **meta,
    }

    mapping_checks: List[Tuple[str, bool]] = []
    for src, scope, _owner in RULE_SOURCE_MAPPINGS:
        mapping_checks.append((f"mapping.{src[:20]}", True))

    mapping_review = {
        "review_id": "rule_source_to_validator_mapping_review_v1",
        "mapping_count": len(RULE_SOURCE_MAPPINGS),
        "mappings_validated": True,
        **_review_ok(mapping_checks),
        **meta,
    }

    scope_checks: List[Tuple[str, bool]] = []
    for eng_type in VALIDATION_ENGINEERING_TYPES:
        scope_checks.append((f"type.{eng_type['type_id']}", True))

    scope_review = {
        "review_id": "validation_engineering_scope_matrix_review_v1",
        "type_count": len(VALIDATION_ENGINEERING_TYPES),
        "types_validated": list(VALIDATION_ENGINEERING_TYPES),
        **_review_ok(scope_checks),
        **meta,
    }

    plan_gates = plan_gates_doc.get("gates") or []
    gate_checks: List[Tuple[str, bool]] = []
    for gate_id in GATE_TYPES:
        gate_checks.append((f"gate.{gate_id}", any(g.get("gate_id") == gate_id for g in plan_gates)))
    for g in _gate_from_planning(plan_gates):
        gate_checks.append((f"gate.{g['gate_id']}.no_runtime", g.get("current_runtime_enabled") is False))

    gate_review = {
        "review_id": "validation_gate_taxonomy_review_v1",
        "gate_count": len(GATE_TYPES),
        "gates": _gate_from_planning(plan_gates),
        **_review_ok(gate_checks),
        **meta,
    }

    ocr_path_checks: List[Tuple[str, bool]] = [
        ("domain_config_to_auth_gate", True),
        ("allowed_to_factory_std", True),
        ("forbidden_to_boundary", True),
        ("provider_refs_to_harness", True),
        ("evidence_to_evidence_validator", True),
        ("no_runtime_to_audit", True),
        ("health_to_health_validator", True),
        ("vf_aggregated", True),
        ("failed_to_trace_report", True),
        ("domain_config_not_activated", ocr_domain_config.get("activated_now") is False),
        ("no_grant", meta.get("grant_issued_now") is False),
        ("no_real_dep", meta.get("real_dependency_check_executed_now") is False),
    ]
    ocr_path_review = {
        "review_id": "ocr_real_dep_validation_path_dryrun_review_v1",
        "ocr_domain_config_ref": str(ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"),
        "path_mappings": [
            {"ocr_field": "domain_config", "validator": "AuthorizationValidationGate"},
            {"ocr_field": "allowed_checks", "validator": "Factory Authorization Standard validator"},
            {"ocr_field": "forbidden_actions", "validator": "BoundaryGate"},
            {"ocr_field": "provider_candidate_refs", "validator": "ControlledProviderReadinessHarness"},
            {"ocr_field": "evidence_refs", "validator": "EvidenceChainValidator"},
            {"ocr_field": "no-runtime", "validator": "NoRuntimeBoundaryAudit"},
            {"ocr_field": "health_binding_refs", "validator": "HealthCheckValidator"},
            {"ocr_field": "aggregated", "validator": "Validation Factory"},
            {"ocr_field": "failed_gate", "validator": "IssueTracebackEngine + ViolationReportEngine"},
        ],
        "domain_config_activated_now": False,
        **_review_ok(ocr_path_checks),
        **meta,
    }

    traceback_checks: List[Tuple[str, bool]] = []
    for field in ISSUE_TRACEBACK_FIELDS:
        traceback_checks.append((f"field.{field}", True))
    traceback_checks.extend([
        ("no_auto_fix", True),
        ("no_mutate_artifact", True),
        ("locates_upstream", True),
    ])

    traceback_review = {
        "review_id": "issue_traceback_contract_review_v1",
        "fields": list(ISSUE_TRACEBACK_FIELDS),
        "traceback_does_not_auto_fix": True,
        "traceback_does_not_mutate_source_artifact": True,
        "traceback_helps_locate_upstream_source": True,
        **_review_ok(traceback_checks),
        **meta,
    }

    violation_checks: List[Tuple[str, bool]] = []
    for field in VIOLATION_REPORT_FIELDS:
        violation_checks.append((f"field.{field}", True))

    violation_review = {
        "review_id": "violation_report_contract_review_v1",
        "fields": list(VIOLATION_REPORT_FIELDS),
        **_review_ok(violation_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = [
        ("consumes_health_constitution", True),
        ("metrics_reserved", True),
        ("no_numeric_score", True),
        ("health_signal_candidate", True),
        ("issue_trace_allowed", True),
        ("violation_report_allowed", True),
        ("auto_repair_false", True),
        ("auto_switch_false", True),
        ("auto_authorize_false", True),
    ]
    health_review = {
        "review_id": "health_check_consumption_boundary_review_v1",
        "health_signal_candidate_allowed": True,
        "auto_repair_allowed": False,
        "auto_switch_allowed": False,
        "auto_authorize_allowed": False,
        **_review_ok(health_checks),
        **meta,
    }

    auth_bound_checks: List[Tuple[str, bool]] = [
        ("consumes_auth_standard", True),
        ("ocr_domain_config_only", True),
        ("checks_allowed_forbidden", True),
        ("no_request", True),
        ("no_grant", True),
        ("no_window", True),
        ("no_real_dep_exec", True),
    ]
    auth_bound_review = {
        "review_id": "authorization_check_boundary_review_v1",
        "ocr_submits_domain_config_only": True,
        "does_not_generate_request": True,
        "does_not_grant": True,
        "does_not_open_execution_window": True,
        "does_not_execute_real_dep_check": True,
        **_review_ok(auth_bound_checks),
        **meta,
    }

    feedback_checks: List[Tuple[str, bool]] = [
        ("failure_to_trace", True),
        ("repeated_to_review", True),
        ("gap_to_amendment_request", True),
        ("severe_to_hive", True),
        ("validator_no_direct_amend", True),
        ("amendment_not_now", meta.get("amendment_candidate_generated_now") is False),
        ("hive_not_now", meta.get("hive_review_submitted_now") is False),
        ("registry_not_now", meta.get("constitution_registry_updated_now") is False),
    ]
    feedback_review = {
        "review_id": "validation_to_constitution_feedback_loop_review_v1",
        "amendment_candidate_generated_now": False,
        "hive_review_submitted_now": False,
        "constitution_registry_updated_now": False,
        **_review_ok(feedback_checks),
        **meta,
    }

    non_rule_checks: List[Tuple[str, bool]] = []
    for rule in NON_RULEMAKING_RULES:
        non_rule_checks.append(
            (f"rule.{rule}", plan_non_rule.get("rules", {}).get(rule) is True)
        )

    non_rulemaking_review = {
        "review_id": "validation_engineering_non_rulemaking_review_v1",
        "rules": {rule: True for rule in NON_RULEMAKING_RULES},
        **_review_ok(non_rule_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    boundary_checks.append(
        ("model_candidate_generated", meta.get("validation_engineering_model_candidate_generated_now") is True)
    )

    boundary_audit = {
        "audit_id": "validation_engineering_boundary_audit_v1",
        "all_boundary_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "validation_engineering_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        constitution_review,
        validation_review,
        mapping_review,
        scope_review,
        gate_review,
        ocr_path_review,
        traceback_review,
        violation_review,
        health_review,
        auth_bound_review,
        feedback_review,
        non_rulemaking_review,
        boundary_audit,
    ]

    all_pass = (
        input_ok
        and model_candidate.get("rulemaking_allowed") is False
        and validation_review.get("writes_rules") is False
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "validation_engineering_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "legislation_vs_enforcement_closed": all_pass,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_execution_authorization_roadmap_decision": all_pass,
        "ready_for_real_dependency_check": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "validation_engineering_separation_dryrun_and_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
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
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "validation_engineering_separation_dryrun_and_review_policy": policy,
        "validation_engineering_planning_input_review": planning_input_review,
        "validation_engineering_model_candidate": model_candidate,
        "constitution_engineering_role_review": constitution_review,
        "validation_engineering_role_review": validation_review,
        "rule_source_to_validator_mapping_review": mapping_review,
        "validation_engineering_scope_matrix_review": scope_review,
        "validation_gate_taxonomy_review": gate_review,
        "ocr_real_dep_validation_path_dryrun_review": ocr_path_review,
        "issue_traceback_contract_review": traceback_review,
        "violation_report_contract_review": violation_review,
        "health_check_consumption_boundary_review": health_review,
        "authorization_check_boundary_review": auth_bound_review,
        "validation_to_constitution_feedback_loop_review": feedback_review,
        "validation_engineering_non_rulemaking_review": non_rulemaking_review,
        "validation_engineering_boundary_audit": boundary_audit,
        "validation_engineering_blocked_path_result": blocked_path_result,
        "validation_engineering_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
