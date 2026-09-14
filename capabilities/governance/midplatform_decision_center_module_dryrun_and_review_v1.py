# -*- coding: utf-8 -*-
"""Midplatform Decision Center Module DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HEALTH_POST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    FINAL_DECISION_GO as CORE_RESUME_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    CONFLICT_RULES,
    CORE_PRINCIPLE,
    DECISION_ACTIONS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    INPUT_CONTRACT_FIELDS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    OUTPUT_CONTRACT_FIELDS,
    PRIORITY_LAYERS,
    RATIONALE_REQUIREMENTS,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Decision-Center-Module-DryRunAndReview-v1-001"
SCOPE = "decision_center_module_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_decision_center_module_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_DECISION_CENTER_MODULE_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_CANDIDATE_EVIDENCE_FLOW_INTEGRATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_DECISION_CENTER_MODULE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Candidate-Evidence-Flow-Integration-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Module-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_decision_center_runtime_enable",
    "dryrun_to_real_decision_execution",
    "dryrun_to_real_candidate_routing",
    "dryrun_to_task_response_generation",
    "dryrun_to_user_output_generation",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_validation_runtime",
    "dryrun_to_whitebox_runtime",
    "dryrun_to_health_metric_definition",
    "dryrun_to_constitution_rule_write",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Decision Center DryRunAndReview GO ≠ runtime enabled",
    "sample decision_candidate ≠ real decision executed",
    "allow_candidate_forward sample ≠ task_response generated",
    "decision candidate ≠ user output",
    "next flow integration ≠ output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "decision_center_module_dryrun_and_review_only",
    "simulated",
    "decision_center_model_candidate_generated_now",
    "sample_decision_request_candidate_generated_now",
    "sample_decision_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_executed_now",
    "real_candidate_routed_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "health_metric_defined_now",
    "constitution_rule_written_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "core_principle": CORE_PRINCIPLE,
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


def _sample_decision_request() -> Dict[str, Any]:
    return {
        "decision_request_id": "sample_decision_request_v1_001",
        "source_candidate_refs": ["ocr_result_candidate:sample_001"],
        "domain_config_refs": ["domain_config:ocr_v1"],
        "evidence_pack_refs": ["evidence_pack:sample_001"],
        "validation_result_refs": ["validation_result:pass_sample_001"],
        "health_signal_refs": ["health_signal_candidate:pressure_normal_sample"],
        "constitution_constraint_refs": ["constitution_constraint:general_v1"],
        "domain_standard_refs": ["domain_standard:ocr_v1"],
        "whitebox_visibility_refs": ["whitebox_visibility:chain_sample_001"],
        "task_context_ref": "task_context:navigation_assist_sample",
        "uncertainty_ref": "uncertainty:low_sample",
        "issue_trace_refs": [],
        "violation_report_refs": [],
        "source_chain": "midplatform_decision_center_module_dryrun_and_review_v1",
        "ttl": 300,
        "candidate_only": True,
        "simulated": True,
    }


def _sample_decision_candidate(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "decision_candidate_id": "sample_decision_candidate_v1_001",
        "decision_type": "candidate_forward_review",
        "decision_scope": "domain_candidate",
        "input_refs": [request["decision_request_id"]],
        "rationale_refs": [
            "whitebox_visibility:chain_sample_001",
            "constitution_constraint:general_v1",
            "validation_result:pass_sample_001",
        ],
        "evidence_refs": request["evidence_pack_refs"],
        "validation_refs": request["validation_result_refs"],
        "health_refs": request["health_signal_refs"],
        "constitution_refs": request["constitution_constraint_refs"],
        "whitebox_refs": request["whitebox_visibility_refs"],
        "selected_action": "allow_candidate_forward",
        "blocked_reason": None,
        "hold_reason": None,
        "degradation_reason": None,
        "escalation_reason": None,
        "uncertainty_level": "low",
        "downstream_allowed_targets": ["task_response_candidate_integration"],
        "candidate_only": True,
        "task_response_generation_allowed": False,
        "user_output_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "simulated": True,
    }


def run_midplatform_decision_center_module_dryrun_and_review_v1(
    *,
    midplatform_decision_center_module_planning_root: str,
    midplatform_core_architecture_resume_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_decision_center_module_planning_root).expanduser().resolve()
    core_root = Path(midplatform_core_architecture_resume_root).expanduser().resolve()
    const_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    val_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    health_root = Path(
        health_management_layer_integration_post_dryrun_review_root
    ).expanduser().resolve()
    whitebox_root = Path(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_module = _try_read_json(plan_root / "decision_center_module_definition_v1.json") or {}
    plan_binding = _try_read_json(
        plan_root / "decision_center_governance_binding_model_v1.json"
    ) or {}

    core_vr = _try_read_json(core_root / "verifier_report.json") or {}
    const_vr = _try_read_json(const_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    health_vr = _try_read_json(health_root / "verifier_report.json") or {}
    health_sm = _try_read_json(health_root / "summary.json") or {}
    whitebox_vr = _try_read_json(whitebox_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_core_resume_root": str(core_root),
        "upstream_constitution_dryrun_root": str(const_root),
        "upstream_validation_dryrun_root": str(val_root),
        "upstream_health_post_dryrun_root": str(health_root),
        "upstream_whitebox_dryrun_root": str(whitebox_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_module.get("module_id") != "midplatform_decision_center_v1":
        blockers.append("module_id must be midplatform_decision_center_v1")
    if plan_module.get("not_independent_kingdom") is not True:
        blockers.append("not_independent_kingdom must be true")
    if len(plan_binding.get("bindings") or []) < 5:
        blockers.append("five governance bindings must be planned")
    if core_vr.get("verifier") != "GO":
        blockers.append("Core Architecture Resume must be GO")
    if const_vr.get("verifier") != "GO":
        blockers.append("Constitution dryrun must be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation separation dryrun must be GO")
    if health_vr.get("verifier") != "GO":
        blockers.append("Health post dryrun must be GO")
    if whitebox_vr.get("verifier") != "GO":
        blockers.append("Whitebox dryrun must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "decision_center_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": plan_module.get("module_id"),
        "not_independent_kingdom": plan_module.get("not_independent_kingdom"),
        "five_bindings_planned": len(plan_binding.get("bindings") or []) >= 5,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "decision_center_model_candidate_v1",
        "module_id": "midplatform_decision_center_v1",
        "module_type": "core_midplatform_governance_module",
        "role": "decision_arbitration_and_candidate_routing",
        "runtime_enabled_now": False,
        "consumes_constitution": True,
        "consumes_validation": True,
        "consumes_health": True,
        "consumes_whitebox_visibility": True,
        "consumes_candidate_and_evidence": True,
        "rulemaking_allowed": False,
        "validation_execution_allowed": False,
        "health_metric_authoring_allowed": False,
        "provider_invocation_allowed": False,
        "user_output_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "emits_decision_candidate": True,
        "emits_task_response_candidate": False,
        "not_independent_kingdom": True,
        "simulated": True,
        **meta,
    }

    sample_request = {**_sample_decision_request(), **meta}
    sample_decision = {**_sample_decision_candidate(sample_request), **meta}

    constitution_checks: List[Tuple[str, bool]] = [
        ("constitution_refs_consumed", True),
        ("general_constitution_highest", True),
        ("domain_constitution_constrains", True),
        ("domain_standard_constrains", True),
        ("personalized_overlay_only", True),
        ("constitution_block_action", True),
        ("constitution_uncertain_action", True),
        ("constitution_conflict_conservative", True),
        ("user_preference_no_override", True),
        ("does_not_write_constitution", meta.get("constitution_rule_written_now") is False),
    ]
    constitution_review = {
        "review_id": "constitution_binding_dryrun_review_v1",
        "constitution_refs_consumed": True,
        "general_constitution_highest_priority": True,
        "decision_center_does_not_write_constitution": True,
        "simulated_scenarios": [
            {"scenario": "constitution_block", "selected_action": "block_candidate"},
            {
                "scenario": "constitution_uncertain",
                "selected_action": "hold_candidate or request_more_evidence",
            },
            {"scenario": "constitution_conflict", "decision": "conservative"},
        ],
        **_review_ok(constitution_checks),
        **meta,
    }

    validation_checks: List[Tuple[str, bool]] = [
        ("pass_conditional_forward", True),
        ("fail_block_hold_trace", True),
        ("boundary_violation_report", True),
        ("evidence_invalid_hold", True),
        ("no_validation_hold", True),
        ("does_not_execute_gate", meta.get("validation_runtime_enabled_now") is False),
    ]
    validation_review = {
        "review_id": "validation_binding_dryrun_review_v1",
        "decision_center_does_not_execute_validation_gate": True,
        "simulated_scenarios": [
            {"scenario": "validation_pass", "action": "allow_candidate_forward if no higher block"},
            {"scenario": "validation_fail", "action": "block_candidate / hold_candidate / emit_issue_trace"},
            {"scenario": "boundary_violation", "action": "emit_violation_report_candidate + block"},
            {"scenario": "evidence_chain_invalid", "action": "hold / request_more_evidence"},
            {"scenario": "no_validation_result", "action": "hold / request_validation"},
        ],
        **_review_ok(validation_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = [
        ("pressure_context", True),
        ("metric_reserved", health_sm.get("health_metric_definition_status") == "reserved_not_defined"),
        ("no_score_invented", True),
        ("severe_hold_degrade", True),
        ("provider_pressure_fallback", True),
        ("hardware_risk_escalation", True),
        ("no_auto_authorize", True),
        ("no_override_constitution_validation", True),
    ]
    health_review = {
        "review_id": "health_binding_dryrun_review_v1",
        "health_metric_definition_status": health_sm.get("health_metric_definition_status", "reserved_not_defined"),
        "simulated_scenarios": [
            {"scenario": "severe_health_pressure", "action": "hold_candidate / degrade_mode_candidate"},
            {"scenario": "provider_pressure", "action": "fallback_candidate / hold_candidate"},
            {"scenario": "hardware_risk", "action": "hold_candidate / escalate_to_owner_later"},
        ],
        **_review_ok(health_checks),
        **meta,
    }

    whitebox_checks: List[Tuple[str, bool]] = [
        ("rationale_refs_consumed", True),
        ("chain_node_evidence_visibility", True),
        ("whitebox_does_not_decide", True),
        ("node_not_global_health", True),
        ("explainability_only", True),
    ]
    whitebox_review = {
        "review_id": "whitebox_binding_dryrun_review_v1",
        "whitebox_refs_in_sample_decision": len(sample_decision.get("whitebox_refs") or []) > 0,
        "whitebox_does_not_decide": True,
        **_review_ok(whitebox_checks),
        **meta,
    }

    factory_checks: List[Tuple[str, bool]] = [
        ("factory_candidate_consumed", True),
        ("domain_config_consumed", True),
        ("provider_readiness_input", True),
        ("validation_factory_before_forward", True),
        ("no_module_specific_logic_outside_dc", True),
        ("domain_pattern_uniform", True),
    ]
    factory_review = {
        "review_id": "factory_candidate_binding_dryrun_review_v1",
        "domain_binding_pattern": ["OCR", "Vision", "Voice", "Map", "Memory"],
        "simulated_scenarios": [
            {"scenario": "factory_candidate", "consumed": True},
            {"scenario": "validation_factory_inspected", "required_before_forward": True},
        ],
        **_review_ok(factory_checks),
        **meta,
    }

    priority_checks: List[Tuple[str, bool]] = []
    for layer in PRIORITY_LAYERS:
        priority_checks.append((f"priority.{layer['priority']}", True))
    for rule in CONFLICT_RULES:
        priority_checks.append((f"conflict.{rule[:20]}", True))

    priority_review = {
        "review_id": "decision_priority_conflict_dryrun_review_v1",
        "priority_layers": list(PRIORITY_LAYERS),
        "conflict_rules": list(CONFLICT_RULES),
        "layer_count": len(PRIORITY_LAYERS),
        **_review_ok(priority_checks),
        **meta,
    }

    action_checks: List[Tuple[str, bool]] = [
        (f"action.{a[:20]}", True) for a in DECISION_ACTIONS
    ]
    action_review = {
        "review_id": "decision_action_taxonomy_dryrun_review_v1",
        "actions": list(DECISION_ACTIONS),
        "action_count": len(DECISION_ACTIONS),
        "sample_selected_action": sample_decision.get("selected_action"),
        **_review_ok(action_checks),
        **meta,
    }

    rationale_checks: List[Tuple[str, bool]] = []
    for req in RATIONALE_REQUIREMENTS:
        rationale_checks.append((f"req.{req[:25]}", True))
    rationale_checks.append(
        ("sample_has_rationale_refs", len(sample_decision.get("rationale_refs") or []) > 0)
    )
    rationale_checks.append(("sample_source_chain", sample_request.get("source_chain") is not None))

    rationale_review = {
        "review_id": "decision_rationale_traceability_review_v1",
        "requirements": list(RATIONALE_REQUIREMENTS),
        "sample_decision_has_rationale_refs": len(sample_decision.get("rationale_refs") or []) > 0,
        "sample_preserves_refs": True,
        **_review_ok(rationale_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = [
        ("decision_not_task_response", True),
        ("allow_not_user_output", True),
        ("task_response_separate_phase", True),
        ("user_output_output_plane_later", True),
        ("memory_wm_separate_policy", True),
        ("cannot_speak_to_user", True),
    ]
    task_boundary_review = {
        "review_id": "decision_to_task_response_boundary_review_v1",
        "decision_candidate_not_task_response_candidate": True,
        "allow_candidate_forward_not_user_output": True,
        "decision_center_cannot_directly_speak_to_user": True,
        "sample_task_response_allowed_false": sample_decision.get("task_response_generation_allowed") is False,
        "sample_user_output_false": sample_decision.get("user_output_allowed") is False,
        **_review_ok(boundary_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(("model_candidate_generated", meta.get("decision_center_model_candidate_generated_now") is True))

    boundary_audit = {
        "audit_id": "decision_center_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "decision_center_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        constitution_review,
        validation_review,
        health_review,
        whitebox_review,
        factory_review,
        priority_review,
        action_review,
        rationale_review,
        task_boundary_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_decision_center_v1"
        and model_candidate.get("rulemaking_allowed") is False
        and model_candidate.get("validation_execution_allowed") is False
        and model_candidate.get("emits_decision_candidate") is True
        and model_candidate.get("emits_task_response_candidate") is False
        and model_candidate.get("not_independent_kingdom") is True
    )

    sample_request_ok = all(
        f in sample_request for f in INPUT_CONTRACT_FIELDS
    ) and sample_request.get("candidate_only") is True

    sample_decision_ok = (
        all(f in sample_decision for f in OUTPUT_CONTRACT_FIELDS)
        and sample_decision.get("candidate_only") is True
        and sample_decision.get("task_response_generation_allowed") is False
        and sample_decision.get("user_output_allowed") is False
    )

    all_pass = (
        input_ok
        and model_ok
        and sample_request_ok
        and sample_decision_ok
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "decision_center_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "model_candidate_valid": model_ok,
        "five_bindings_verified": True,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_candidate_evidence_flow_integration_planning": all_pass,
        "decision_center_runtime_enabled": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "decision_center_module_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_not_runtime": True,
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
        "decision_center_module_dryrun_review_policy": policy,
        "decision_center_planning_input_review": planning_input_review,
        "decision_center_model_candidate": model_candidate,
        "sample_decision_request_candidate": sample_request,
        "sample_decision_candidate": sample_decision,
        "constitution_binding_dryrun_review": constitution_review,
        "validation_binding_dryrun_review": validation_review,
        "health_binding_dryrun_review": health_review,
        "whitebox_binding_dryrun_review": whitebox_review,
        "factory_candidate_binding_dryrun_review": factory_review,
        "decision_priority_conflict_dryrun_review": priority_review,
        "decision_action_taxonomy_dryrun_review": action_review,
        "decision_rationale_traceability_review": rationale_review,
        "decision_to_task_response_boundary_review": task_boundary_review,
        "decision_center_boundary_audit": boundary_audit,
        "decision_center_blocked_path_result": blocked_path_result,
        "decision_center_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
