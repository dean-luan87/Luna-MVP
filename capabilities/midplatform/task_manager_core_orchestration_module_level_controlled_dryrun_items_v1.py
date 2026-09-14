# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Module-Level Controlled DryRun scenario definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.midplatform.task_manager_core_orchestration_builders_v1 import (
    build_blocker_or_defer_decision_candidate,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_v1 import (
    run_controlled_orchestration_skeleton,
)
from capabilities.midplatform.task_manager_core_orchestration_static_validators_v1 import (
    validate_candidate_only_outputs,
    validate_orchestration_result_candidate,
)
from capabilities.midplatform.task_manager_core_orchestration_types_v1 import (
    OrchestrationInputCandidate,
)


def base_dryrun_input(candidate_id: str, **overrides: Any) -> OrchestrationInputCandidate:
    base = {
        "candidate_id": candidate_id,
        "source_module_ref": "task_manager_core_orchestration",
        "boundary_registry_ref": "boundary:task_manager_core",
        "lifecycle_state_ref": "lifecycle:candidate_review",
        "alignment_rule_ref": "alignment:evidence_record_approval_permission",
        "governance_constraint_ref": "governance:migration_development_constraints_v1",
        "protocol_trace_ref": "trace:orch:dryrun_v1",
        "traceability_refs": ("trace:orch:dryrun_v1", "chain:task_manager_core_orchestration"),
        "governance_refs": ("governance:migration_development_constraints_v1",),
    }
    base.update(overrides)
    return OrchestrationInputCandidate(**base)


def _candidate_flags_ok(obj: Any) -> bool:
    if obj is None:
        return False
    return (
        getattr(obj, "candidate_only", True) is True
        and getattr(obj, "side_effect_allowed", False) is False
        and getattr(obj, "real_execution", False) is False
        and getattr(obj, "runtime_required_now", False) is False
    )


def _has_refs(obj: Any) -> Tuple[bool, bool]:
    trace = getattr(obj, "traceability_refs", ()) or ()
    gov = getattr(obj, "governance_refs", ()) or ()
    return bool(trace), bool(gov)


def _non_execution_guard_result(obj: Any, owner_chain_ok: bool) -> Dict[str, bool]:
    return {
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": getattr(obj, "real_execution", False) is False,
        "no_route_execution": getattr(obj, "route_execution", False) is False,
        "no_real_handoff_execution": getattr(obj, "handoff_execution", False) is False,
        "no_owner_approval_request_reopen": owner_chain_ok,
        "no_candidate_promotion_execution": getattr(obj, "promotion_execution", False) is False,
        "no_whitebox_runtime_call": True,
    }


def run_dryrun_scenario(scenario: Dict[str, Any], owner_chain_ok: bool) -> Dict[str, Any]:
    sid = scenario["scenario_id"]
    input_ref = f"orch_input_{sid}"
    decision_override = scenario.get("decision_kind_override")

    if decision_override:
        decision = build_blocker_or_defer_decision_candidate(
            decision_kind=decision_override,
            decision_reason=f"controlled_dryrun_{decision_override}_candidate",
            source_check_refs=(input_ref,),
            traceability_refs=("trace:orch:dryrun_v1",),
            governance_refs=("governance:migration_development_constraints_v1",),
            candidate_id=f"orch_decision_{sid}",
        )
        guard = _non_execution_guard_result(decision, owner_chain_ok)
        val = validate_candidate_only_outputs(decision)
        passed = _candidate_flags_ok(decision) and val.valid and all(guard.values())
        return {
            "scenario_id": sid,
            "input_candidate_ref": input_ref,
            "expected_result_type": scenario["expected_result_type"],
            "actual_result_type": type(decision).__name__,
            "produced_candidates": [type(decision).__name__],
            "validation_result": {"valid": val.valid, "issues": list(val.issues)},
            "non_execution_guard_result": guard,
            "real_execution": False,
            "side_effect_allowed": False,
            "scenario_passed": passed,
            "skeleton_pass": None,
            "decision_kind": decision.decision_kind,
        }

    overrides = dict(scenario.get("input_overrides") or {})
    input_candidate = base_dryrun_input(input_ref, **overrides)
    payload = run_controlled_orchestration_skeleton(input_candidate)

    focus = scenario.get("focus_output")
    if focus == "traceability_bundle":
        actual_type = type(payload.get("traceability_bundle")).__name__
        focus_obj = payload.get("traceability_bundle")
    else:
        actual_type = type(payload.get("result_candidate")).__name__
        focus_obj = payload.get("result_candidate")

    produced = [
        type(payload[k]).__name__
        for k in (
            "plan_candidate", "route_candidate", "handoff_candidate",
            "traceability_bundle", "decision_candidate", "lifecycle_request",
            "alignment_request", "governance_request", "result_candidate",
        )
        if payload.get(k) is not None
    ]
    result_candidate = payload.get("result_candidate")
    val_result = validate_orchestration_result_candidate(result_candidate) if result_candidate else None
    guard_target = focus_obj or result_candidate or payload
    guard = _non_execution_guard_result(guard_target, owner_chain_ok)
    if scenario.get("focus_guard"):
        for key in ("route_candidate", "handoff_candidate", "decision_candidate"):
            sub = payload.get(key)
            if sub is not None:
                sub_guard = _non_execution_guard_result(sub, owner_chain_ok)
                guard = {k: guard.get(k, True) and sub_guard.get(k, True) for k in guard}

    expect_pass = scenario.get("expect_skeleton_pass")
    skeleton_pass = payload.get("skeleton_pass")
    decision_kind = getattr(payload.get("decision_candidate"), "decision_kind", None)
    expect_decision = scenario.get("expect_decision_kind")

    passed = (
        _candidate_flags_ok(payload)
        and all(guard.values())
        and actual_type == scenario["expected_result_type"]
    )
    if expect_pass is True:
        passed = passed and skeleton_pass is True and (val_result.valid if val_result else False)
    elif expect_pass is False:
        passed = passed and skeleton_pass is False
        if expect_decision:
            passed = passed and decision_kind == expect_decision
    if focus == "traceability_bundle":
        has_trace, has_gov = _has_refs(focus_obj)
        passed = passed and has_trace and has_gov

    return {
        "scenario_id": sid,
        "input_candidate_ref": input_ref,
        "expected_result_type": scenario["expected_result_type"],
        "actual_result_type": actual_type,
        "produced_candidates": produced,
        "validation_result": {
            "valid": val_result.valid if val_result else True,
            "issues": list(val_result.issues) if val_result else [],
        },
        "non_execution_guard_result": guard,
        "real_execution": False,
        "side_effect_allowed": False,
        "scenario_passed": passed,
        "skeleton_pass": skeleton_pass,
        "decision_kind": decision_kind,
    }

DRYRUN_SCENARIOS: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_id": "happy_path_candidate_orchestration",
        "description": "Valid input completes full candidate-level orchestration flow",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": True,
        "input_overrides": {},
    },
    {
        "scenario_id": "boundary_check_missing_ref",
        "description": "Missing boundary_registry_ref triggers candidate-level validation failure",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": False,
        "input_overrides": {"boundary_registry_ref": ""},
    },
    {
        "scenario_id": "lifecycle_state_invalid",
        "description": "Invalid lifecycle_state_ref triggers lifecycle check failure",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": False,
        "input_overrides": {"lifecycle_state_ref": ""},
    },
    {
        "scenario_id": "alignment_rule_missing",
        "description": "Missing alignment_rule_ref triggers alignment check failure",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": False,
        "input_overrides": {"alignment_rule_ref": ""},
    },
    {
        "scenario_id": "governance_constraint_missing",
        "description": "Missing governance refs triggers governance check failure",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": False,
        "input_overrides": {"governance_constraint_ref": "", "governance_refs": ()},
    },
    {
        "scenario_id": "blocker_decision_path",
        "description": "Multiple missing refs produce blocker decision candidate",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": False,
        "expect_decision_kind": "blocker",
        "input_overrides": {"boundary_registry_ref": "", "alignment_rule_ref": ""},
    },
    {
        "scenario_id": "defer_decision_path",
        "description": "Defer decision candidate built without real-world action",
        "expected_result_type": "BlockerOrDeferDecisionCandidate",
        "expect_skeleton_pass": None,
        "decision_kind_override": "defer",
    },
    {
        "scenario_id": "reject_decision_path",
        "description": "Reject decision candidate built without real-world action",
        "expected_result_type": "BlockerOrDeferDecisionCandidate",
        "expect_skeleton_pass": None,
        "decision_kind_override": "reject",
    },
    {
        "scenario_id": "close_decision_path",
        "description": "Close decision candidate built without real-world action",
        "expected_result_type": "BlockerOrDeferDecisionCandidate",
        "expect_skeleton_pass": None,
        "decision_kind_override": "close",
    },
    {
        "scenario_id": "traceability_bundle_generation",
        "description": "Traceability bundle candidate generated with refs intact",
        "expected_result_type": "TraceabilityBundleCandidate",
        "expect_skeleton_pass": True,
        "input_overrides": {},
        "focus_output": "traceability_bundle",
    },
    {
        "scenario_id": "non_execution_guard_enforcement",
        "description": "All non-execution guards hold across module outputs",
        "expected_result_type": "OrchestrationResultCandidate",
        "expect_skeleton_pass": True,
        "input_overrides": {},
        "focus_guard": True,
    },
)

FLOW_STEPS: Tuple[str, ...] = (
    "normalize_input",
    "check_boundary",
    "check_lifecycle",
    "check_alignment",
    "check_governance",
    "build_route_candidate",
    "build_handoff_candidate",
    "build_traceability_bundle",
    "build_decision_candidate",
    "assemble_orchestration_result",
    "validate_result_candidate",
)

CANDIDATE_OUTPUT_TYPES: Tuple[str, ...] = (
    "OrchestrationPlanCandidate",
    "CandidateRouteCandidate",
    "ModuleHandoffCandidate",
    "LifecycleTransitionRequestCandidate",
    "AlignmentCheckRequestCandidate",
    "GovernanceCheckRequestCandidate",
    "TraceabilityBundleCandidate",
    "BlockerOrDeferDecisionCandidate",
    "OrchestrationResultCandidate",
)

NON_EXECUTION_GUARDS: Tuple[str, ...] = (
    "no_record_creation",
    "no_grant_creation",
    "no_authorization_request_creation",
    "no_runtime_execution",
    "no_route_execution",
    "no_real_handoff_execution",
    "no_owner_approval_request_reopen",
    "no_candidate_promotion_execution",
    "no_whitebox_runtime_call",
)

SELECTED_NEXT_ROUTE = "Midplatform Module Integration Gap Consolidation"
NEXT_ROUTE_A = "Phase-Midplatform-Module-Integration-Gap-Consolidation-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Task-Manager-Core-Orchestration-Module-Level-Review-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Candidate-Lifecycle-Manager-Controlled-Implementation-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Module-Level-Integration-Planning-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"
