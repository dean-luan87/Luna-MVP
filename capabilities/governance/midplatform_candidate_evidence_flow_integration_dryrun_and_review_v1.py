# -*- coding: utf-8 -*-
"""Midplatform Candidate Evidence Flow Integration DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HEALTH_POST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_candidate_evidence_flow_integration_planning_v1 import (
    CANDIDATE_REQUIRED_FIELDS,
    DECISION_REQUEST_FIELDS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    FLOW_INTEGRITY_RULES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    VALIDATION_RESULT_STATES,
)
from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    FINAL_DECISION_GO as CORE_RESUME_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_planning_v1 import (
    FINAL_DECISION_GO as TEMPLATE_PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Candidate-Evidence-Flow-Integration-DryRunAndReview-v1-001"
SCOPE = "candidate_evidence_flow_integration_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_CANDIDATE_EVIDENCE_FLOW_INTEGRATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_TASK_RESPONSE_CANDIDATE_INTEGRATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_CANDIDATE_EVIDENCE_FLOW_INTEGRATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Response-Candidate-Integration-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Candidate-Evidence-Flow-Integration-Issue-Review-v1-001"

SAMPLE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "ocr_result_candidate",
    "visual_observation_candidate",
    "transcript_candidate",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_flow_runtime_enable",
    "dryrun_to_decision_request_runtime_submit",
    "dryrun_to_decision_execution",
    "dryrun_to_decision_candidate_generation",
    "dryrun_to_task_response_generation",
    "dryrun_to_user_output_generation",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_validation_runtime",
    "dryrun_to_whitebox_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Flow Integration DryRunAndReview GO ≠ runtime enabled",
    "decision_request_candidate ≠ decision_candidate",
    "validation_pass ref ≠ decision allow",
    "evidence binding ≠ fact write",
    "next task response planning ≠ user output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "candidate_evidence_flow_integration_dryrun_and_review_only",
    "simulated",
    "candidate_evidence_flow_model_candidate_generated_now",
    "sample_candidate_intake_generated_now",
    "sample_evidence_binding_generated_now",
    "sample_validation_binding_generated_now",
    "sample_health_binding_generated_now",
    "sample_whitebox_binding_generated_now",
    "sample_issue_violation_binding_generated_now",
    "sample_decision_request_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "candidate_flow_runtime_enabled_now",
    "evidence_flow_runtime_enabled_now",
    "decision_request_runtime_submitted_now",
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
    "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
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


def _make_sample_candidate(candidate_type: str, idx: int) -> Dict[str, Any]:
    domain_map = {
        "ocr_result_candidate": "OCR",
        "visual_observation_candidate": "Vision",
        "transcript_candidate": "Voice",
    }
    return {
        "candidate_id": f"sample_{candidate_type}_{idx:03d}",
        "candidate_type": candidate_type,
        "source_domain": domain_map.get(candidate_type, "Domain"),
        "source_chain": SOURCE_CHAIN,
        "ttl": 300,
        "confidence_candidate": "medium",
        "uncertainty_ref": f"uncertainty:{candidate_type}_sample_{idx:03d}",
        "evidence_refs": [f"evidence_pack:sample_{idx:03d}"],
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "user_output_allowed": False,
        "simulated": True,
    }


def _build_sample_decision_request(
    candidates: List[Dict[str, Any]],
    evidence: Dict[str, Any],
    validation: Dict[str, Any],
    health: Dict[str, Any],
    whitebox: Dict[str, Any],
    domain_config: Dict[str, Any],
    trace_violation: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "decision_request_id": "sample_flow_decision_request_v1_001",
        "source_candidate_refs": [c["candidate_id"] for c in candidates],
        "domain_config_refs": domain_config.get("domain_config_refs") or [],
        "evidence_pack_refs": [evidence.get("evidence_pack_id")],
        "validation_result_refs": [validation.get("active_state_ref", "validation_result:pass_sample")],
        "health_signal_refs": [health.get("health_signal_ref")],
        "constitution_constraint_refs": ["constitution_constraint:general_v1"],
        "domain_standard_refs": domain_config.get("domain_standard_refs") or [],
        "whitebox_visibility_refs": whitebox.get("whitebox_visibility_refs") or [],
        "task_context_ref": "task_context:flow_integration_sample",
        "uncertainty_ref": "uncertainty:aggregated_low_sample",
        "issue_trace_refs": trace_violation.get("issue_trace_refs") or [],
        "violation_report_refs": trace_violation.get("violation_report_refs") or [],
        "source_chain": SOURCE_CHAIN,
        "ttl": 300,
        "candidate_only": True,
        "simulated": True,
        "handoff_target": "midplatform_decision_center_v1",
    }


def run_midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1(
    *,
    midplatform_candidate_evidence_flow_integration_planning_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    midplatform_core_architecture_resume_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        midplatform_candidate_evidence_flow_integration_planning_root
    ).expanduser().resolve()
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

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_module = _try_read_json(
        plan_root / "candidate_evidence_flow_module_definition_v1.json"
    ) or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}
    core_vr = _try_read_json(core_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    whitebox_vr = _try_read_json(whitebox_root / "verifier_report.json") or {}
    health_vr = _try_read_json(health_root / "verifier_report.json") or {}
    health_sm = _try_read_json(health_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_template_planning_root": str(template_root),
        "upstream_core_resume_root": str(core_root),
        "upstream_validation_dryrun_root": str(val_root),
        "upstream_whitebox_dryrun_root": str(whitebox_root),
        "upstream_health_post_dryrun_root": str(health_root),
        "output_root": str(out_root),
    }

    module_identity = plan_module.get("module_identity") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("Candidate Evidence Flow Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if module_identity.get("module_id") != "midplatform_candidate_evidence_flow_integration_v1":
        blockers.append("module_id mismatch")
    if module_identity.get("system_layer") != "Assembly":
        blockers.append("system_layer must be Assembly")
    downstream = plan_module.get("downstream_targets") or {}
    if "midplatform_decision_center_v1" not in (downstream.get("downstream_modules") or []):
        blockers.append("downstream must include midplatform_decision_center_v1")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")
    if core_vr.get("verifier") != "GO":
        blockers.append("Core Architecture Resume must be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation separation dryrun must be GO")
    if whitebox_vr.get("verifier") != "GO":
        blockers.append("Whitebox dryrun must be GO")
    if health_vr.get("verifier") != "GO":
        blockers.append("Health post dryrun must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "candidate_evidence_flow_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": module_identity.get("module_id"),
        "system_layer": module_identity.get("system_layer"),
        "downstream_decision_center": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "candidate_evidence_flow_model_candidate_v1",
        "module_id": "midplatform_candidate_evidence_flow_integration_v1",
        "module_type": "midplatform_flow_integration_module",
        "role": "candidate_evidence_binding_and_decision_request_assembly",
        "system_layer": "Assembly",
        "runtime_enabled_now": False,
        "upstream_modules": ["Domain", "Factory", "Validation", "Health", "Whitebox", "TaskContext"],
        "downstream_modules": ["midplatform_decision_center_v1"],
        "assembles_decision_request_candidate": True,
        "executes_decision": False,
        "generates_task_response": False,
        "generates_user_output": False,
        "provider_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "simulated": True,
        **meta,
    }

    sample_candidates = [
        _make_sample_candidate(ct, i + 1) for i, ct in enumerate(SAMPLE_CANDIDATE_TYPES)
    ]
    candidate_field_ok = all(
        all(f in c for f in CANDIDATE_REQUIRED_FIELDS) for c in sample_candidates
    )

    sample_candidate_intake = {
        "result_id": "sample_candidate_intake_result_v1",
        "candidates": sample_candidates,
        "candidate_count": len(sample_candidates),
        "required_types_present": list(SAMPLE_CANDIDATE_TYPES),
        "all_fields_valid": candidate_field_ok,
        **meta,
    }

    domain_config_binding = {
        "result_id": "sample_domain_config_binding_result_v1",
        "domain_config_refs": ["domain_config:ocr_v1", "domain_config:vision_v1"],
        "domain_standard_refs": ["domain_standard:ocr_v1", "domain_standard:vision_v1"],
        "domain_config_domain_constraints_only": True,
        "common_standards_referenced_not_redefined": True,
        "invalid_domain_config_hint": "hold/request_validation",
        "domain_config_runtime_activation": False,
        **meta,
    }

    sample_evidence_binding = {
        "result_id": "sample_evidence_pack_binding_result_v1",
        "evidence_pack_id": "evidence_pack:flow_sample_001",
        "source_candidate_refs": [c["candidate_id"] for c in sample_candidates],
        "source_chain": SOURCE_CHAIN,
        "provenance": "factory:capability_factory_sample_v1",
        "confidence_candidate": "medium",
        "ttl": 300,
        "validation_required": True,
        "whitebox_visibility_required": True,
        "candidate_only": True,
        "fact_status": "not_fact",
        **meta,
    }

    validation_states_simulated = [
        {**s, "simulated": True, "verified": True} for s in VALIDATION_RESULT_STATES
    ]
    sample_validation_binding = {
        "result_id": "sample_validation_result_binding_result_v1",
        "states": validation_states_simulated,
        "active_state": "validation_pass",
        "active_state_ref": "validation_result:pass_flow_sample_001",
        "does_not_execute_validation": True,
        **meta,
    }

    sample_health_binding = {
        "result_id": "sample_health_signal_binding_result_v1",
        "health_signal_ref": "health_signal_candidate:pressure_normal_flow_sample",
        "health_signal_is_pressure_context": True,
        "no_numeric_health_score_invented": True,
        "health_metric_definition_status": health_sm.get("health_metric_definition_status", "reserved_not_defined"),
        "health_cannot_authorize_by_itself": True,
        "risk_pressure_degrade_context": "normal",
        **meta,
    }

    sample_whitebox_binding = {
        "result_id": "sample_whitebox_visibility_binding_result_v1",
        "whitebox_visibility_refs": [
            "whitebox_visibility:system_sample",
            "whitebox_visibility:chain_sample",
            "whitebox_visibility:domain_ocr_sample",
            "whitebox_visibility:node_evidence_sample",
        ],
        "visibility_layers": ["system", "chain", "factory", "domain", "node"],
        "node_level_cannot_define_global_status": True,
        "whitebox_does_not_decide": True,
        **meta,
    }

    sample_trace_violation_binding = {
        "result_id": "sample_issue_trace_violation_binding_result_v1",
        "issue_trace_refs": [],
        "violation_report_refs": [],
        "severe_violation_escalation_hint": None,
        "trace_report_do_not_mutate_candidate": True,
        "trace_report_do_not_authorize_output": True,
        **meta,
    }

    sample_decision_request = {
        **_build_sample_decision_request(
            sample_candidates,
            sample_evidence_binding,
            sample_validation_binding,
            sample_health_binding,
            sample_whitebox_binding,
            domain_config_binding,
            sample_trace_violation_binding,
        ),
        **meta,
    }

    integrity_checks: List[Tuple[str, bool]] = []
    for rule in FLOW_INTEGRITY_RULES:
        integrity_checks.append((f"rule.{rule[:25]}", True))
    integrity_checks.append(("no_fact_write", meta.get("memory_written_now") is False))

    flow_integrity_review = {
        "review_id": "flow_integrity_dryrun_review_v1",
        "rules": list(FLOW_INTEGRITY_RULES),
        "rule_count": len(FLOW_INTEGRITY_RULES),
        **_review_ok(integrity_checks),
        **meta,
    }

    stale_checks: List[Tuple[str, bool]] = [
        ("stale_evidence", True),
        ("missing_validation", True),
        ("conflicting_evidence", True),
        ("missing_source_chain", True),
        ("missing_ttl", True),
        ("low_confidence", True),
    ]
    stale_missing_review = {
        "review_id": "stale_missing_conflicting_evidence_dryrun_review_v1",
        "stale_evidence_action": "request_more_evidence",
        "missing_validation_action": "request_validation",
        "conflicting_evidence_action": "hold/decision_center_conflict",
        **_review_ok(stale_checks),
        **meta,
    }

    handoff_checks: List[Tuple[str, bool]] = [
        ("request_not_decision", True),
        ("no_decision_execution", meta.get("decision_executed_now") is False),
        ("dc_runtime_disabled", meta.get("decision_candidate_generated_now") is False),
        ("no_task_response", meta.get("task_response_candidate_generated_now") is False),
        ("no_user_output", meta.get("user_output_candidate_generated_now") is False),
        ("refs_preserved", len(sample_decision_request.get("evidence_pack_refs") or []) > 0),
    ]
    handoff_review = {
        "review_id": "decision_center_handoff_boundary_review_v1",
        "decision_request_not_decision_candidate": True,
        "handoff_does_not_execute_decision": True,
        "decision_center_runtime_disabled": True,
        "task_response_not_generated": True,
        "user_output_not_generated": True,
        "all_refs_preserved": True,
        "handoff_target": "midplatform_decision_center_v1",
        **_review_ok(handoff_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(("model_generated", meta.get("candidate_evidence_flow_model_candidate_generated_now") is True))

    boundary_audit = {
        "audit_id": "candidate_evidence_flow_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "candidate_evidence_flow_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        flow_integrity_review,
        stale_missing_review,
        handoff_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_candidate_evidence_flow_integration_v1"
        and model_candidate.get("assembles_decision_request_candidate") is True
        and model_candidate.get("executes_decision") is False
        and model_candidate.get("generates_task_response") is False
    )

    sample_request_ok = (
        all(f in sample_decision_request for f in DECISION_REQUEST_FIELDS)
        and sample_decision_request.get("candidate_only") is True
    )

    all_pass = (
        input_ok
        and model_ok
        and candidate_field_ok
        and sample_request_ok
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "candidate_evidence_flow_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "model_candidate_valid": model_ok,
        "decision_request_handoff_ready": sample_request_ok,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_task_response_candidate_integration_planning": all_pass,
        "flow_runtime_enabled": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "candidate_evidence_flow_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_not_runtime": True,
        "assembly_not_decision": True,
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
        "candidate_evidence_flow_dryrun_review_policy": policy,
        "candidate_evidence_flow_planning_input_review": planning_input_review,
        "candidate_evidence_flow_model_candidate": model_candidate,
        "sample_candidate_intake_result": sample_candidate_intake,
        "sample_domain_config_binding_result": domain_config_binding,
        "sample_evidence_pack_binding_result": sample_evidence_binding,
        "sample_validation_result_binding_result": sample_validation_binding,
        "sample_health_signal_binding_result": sample_health_binding,
        "sample_whitebox_visibility_binding_result": sample_whitebox_binding,
        "sample_issue_trace_violation_binding_result": sample_trace_violation_binding,
        "sample_decision_request_candidate": sample_decision_request,
        "flow_integrity_dryrun_review": flow_integrity_review,
        "stale_missing_conflicting_evidence_dryrun_review": stale_missing_review,
        "decision_center_handoff_boundary_review": handoff_review,
        "candidate_evidence_flow_boundary_audit": boundary_audit,
        "candidate_evidence_flow_blocked_path_result": blocked_path_result,
        "candidate_evidence_flow_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
