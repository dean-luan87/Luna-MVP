# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration skeleton v1 — controlled candidate-level coordination only."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.task_manager_core_orchestration_builders_v1 import (
    build_alignment_check_request_candidate,
    build_blocker_or_defer_decision_candidate,
    build_candidate_route_candidate,
    build_governance_check_request_candidate,
    build_lifecycle_transition_request_candidate,
    build_module_handoff_candidate,
    build_orchestration_plan_candidate,
    build_orchestration_result_candidate,
    build_traceability_bundle_candidate,
)
from capabilities.midplatform.task_manager_core_orchestration_contracts_v1 import (
    check_governance_contract,
    check_io_input_contract,
    check_traceability_contract,
)
from capabilities.midplatform.task_manager_core_orchestration_static_validators_v1 import (
    run_all_static_validators,
    validate_alignment_rule_refs,
    validate_boundary_refs,
    validate_governance_constraint_refs,
    validate_lifecycle_state_refs,
    validate_orchestration_result_candidate,
)
from capabilities.midplatform.task_manager_core_orchestration_types_v1 import (
    AlignmentCheckRequestCandidate,
    BlockerOrDeferDecisionCandidate,
    CandidateRouteCandidate,
    GovernanceCheckRequestCandidate,
    LifecycleTransitionRequestCandidate,
    ModuleHandoffCandidate,
    OrchestrationDecisionKind,
    OrchestrationInputCandidate,
    OrchestrationPlanCandidate,
    OrchestrationResultCandidate,
    TraceabilityBundleCandidate,
)

SKELETON_FUNCTIONS: Tuple[str, ...] = (
    "normalize_orchestration_input",
    "check_boundary_for_candidate",
    "check_lifecycle_for_candidate",
    "check_alignment_for_candidate",
    "check_governance_for_candidate",
    "produce_candidate_route",
    "produce_module_handoff_candidate",
    "produce_traceability_bundle",
    "produce_blocker_defer_reject_close_decision",
    "assemble_orchestration_result",
    "run_controlled_orchestration_skeleton",
)


def normalize_orchestration_input(
    input_candidate: OrchestrationInputCandidate,
) -> OrchestrationInputCandidate:
    ok, issues = check_io_input_contract(input_candidate)
    if not ok:
        return input_candidate
    trace_ok, _ = check_traceability_contract(input_candidate)
    gov_ok, _ = check_governance_contract(input_candidate)
    if trace_ok and gov_ok:
        return input_candidate
    return OrchestrationInputCandidate(
        candidate_id=input_candidate.candidate_id,
        source_module_ref=input_candidate.source_module_ref,
        boundary_registry_ref=input_candidate.boundary_registry_ref,
        lifecycle_state_ref=input_candidate.lifecycle_state_ref,
        alignment_rule_ref=input_candidate.alignment_rule_ref,
        governance_constraint_ref=input_candidate.governance_constraint_ref,
        protocol_trace_ref=input_candidate.protocol_trace_ref or "trace:orch:default",
        traceability_refs=input_candidate.traceability_refs or (input_candidate.protocol_trace_ref,),
        governance_refs=input_candidate.governance_refs or (input_candidate.governance_constraint_ref,),
    )


def check_boundary_for_candidate(
    input_candidate: OrchestrationInputCandidate,
) -> ValidationResult:
    return validate_boundary_refs(input_candidate)


def check_lifecycle_for_candidate(
    input_candidate: OrchestrationInputCandidate,
) -> Tuple[ValidationResult, LifecycleTransitionRequestCandidate]:
    result = validate_lifecycle_state_refs(input_candidate)
    request = build_lifecycle_transition_request_candidate(
        lifecycle_state_ref=input_candidate.lifecycle_state_ref,
        transition_intent="review",
        reason="controlled_skeleton_lifecycle_check",
        traceability_refs=input_candidate.traceability_refs,
        governance_refs=input_candidate.governance_refs,
        candidate_id=f"orch_lifecycle_{input_candidate.candidate_id}",
    )
    return result, request


def check_alignment_for_candidate(
    input_candidate: OrchestrationInputCandidate,
) -> Tuple[ValidationResult, AlignmentCheckRequestCandidate]:
    result = validate_alignment_rule_refs(input_candidate)
    request = build_alignment_check_request_candidate(
        alignment_rule_ref=input_candidate.alignment_rule_ref,
        check_scope="boundary_alignment",
        boundary_registry_ref=input_candidate.boundary_registry_ref,
        traceability_refs=input_candidate.traceability_refs,
        governance_refs=input_candidate.governance_refs,
        candidate_id=f"orch_align_{input_candidate.candidate_id}",
    )
    return result, request


def check_governance_for_candidate(
    input_candidate: OrchestrationInputCandidate,
) -> Tuple[ValidationResult, GovernanceCheckRequestCandidate]:
    result = validate_governance_constraint_refs(input_candidate)
    request = build_governance_check_request_candidate(
        governance_constraint_ref=input_candidate.governance_constraint_ref,
        check_scope="orchestration_governance",
        traceability_refs=input_candidate.traceability_refs,
        governance_refs=input_candidate.governance_refs,
        candidate_id=f"orch_gov_{input_candidate.candidate_id}",
    )
    return result, request


def produce_candidate_route(
    plan_candidate: OrchestrationPlanCandidate,
    *,
    route_target_module_ref: Optional[str] = None,
) -> CandidateRouteCandidate:
    target = route_target_module_ref or plan_candidate.boundary_registry_ref
    return build_candidate_route_candidate(
        plan_candidate,
        route_target_module_ref=target,
        route_reason="controlled_skeleton_route_candidate_only",
    )


def produce_module_handoff_candidate(
    route_candidate: CandidateRouteCandidate,
) -> ModuleHandoffCandidate:
    return build_module_handoff_candidate(
        route_candidate,
        handoff_reason="controlled_skeleton_handoff_candidate_only",
    )


def produce_traceability_bundle(
    input_candidate: OrchestrationInputCandidate,
    *,
    source_refs: Tuple[str, ...] = (),
) -> TraceabilityBundleCandidate:
    refs = source_refs or (input_candidate.candidate_id,)
    return build_traceability_bundle_candidate(
        protocol_trace_ref=input_candidate.protocol_trace_ref,
        alignment_rule_ref=input_candidate.alignment_rule_ref,
        source_refs=refs,
        traceability_refs=input_candidate.traceability_refs,
        governance_refs=input_candidate.governance_refs,
        candidate_id=f"orch_trace_{input_candidate.candidate_id}",
    )


def produce_blocker_defer_reject_close_decision(
    *,
    checks: Tuple[ValidationResult, ...],
    traceability_refs: Tuple[str, ...],
    governance_refs: Tuple[str, ...],
    source_check_refs: Tuple[str, ...],
) -> BlockerOrDeferDecisionCandidate:
    blocked = any(c.blocked for c in checks)
    kind = OrchestrationDecisionKind.BLOCKER.value if blocked else OrchestrationDecisionKind.PROCEED.value
    reason = "controlled_skeleton_blocker_detected" if blocked else "controlled_skeleton_proceed_candidate"
    return build_blocker_or_defer_decision_candidate(
        decision_kind=kind,
        decision_reason=reason,
        source_check_refs=source_check_refs,
        traceability_refs=traceability_refs,
        governance_refs=governance_refs,
        candidate_id=f"orch_decision_{kind}",
    )


def assemble_orchestration_result(
    *,
    plan_candidate: OrchestrationPlanCandidate,
    route_candidate: CandidateRouteCandidate,
    handoff_candidate: ModuleHandoffCandidate,
    traceability_bundle: TraceabilityBundleCandidate,
    decision_candidate: BlockerOrDeferDecisionCandidate,
    lifecycle_request: LifecycleTransitionRequestCandidate,
    alignment_request: AlignmentCheckRequestCandidate,
    governance_request: GovernanceCheckRequestCandidate,
    skeleton_pass: bool,
) -> OrchestrationResultCandidate:
    return build_orchestration_result_candidate(
        plan_candidate=plan_candidate,
        route_candidate=route_candidate,
        handoff_candidate=handoff_candidate,
        traceability_bundle=traceability_bundle,
        decision_candidate=decision_candidate,
        lifecycle_request=lifecycle_request,
        alignment_request=alignment_request,
        governance_request=governance_request,
        skeleton_pass=skeleton_pass,
    )


def run_controlled_orchestration_skeleton(
    input_candidate: OrchestrationInputCandidate,
) -> Dict[str, Any]:
    normalized = normalize_orchestration_input(input_candidate)
    boundary_check = check_boundary_for_candidate(normalized)
    lifecycle_check, lifecycle_request = check_lifecycle_for_candidate(normalized)
    alignment_check, alignment_request = check_alignment_for_candidate(normalized)
    governance_check, governance_request = check_governance_for_candidate(normalized)
    checks = (boundary_check, lifecycle_check, alignment_check, governance_check)
    static_check = run_all_static_validators(normalized)
    plan_candidate = build_orchestration_plan_candidate(normalized)
    route_candidate = produce_candidate_route(plan_candidate)
    handoff_candidate = produce_module_handoff_candidate(route_candidate)
    traceability_bundle = produce_traceability_bundle(normalized, source_refs=(plan_candidate.candidate_id,))
    decision_candidate = produce_blocker_defer_reject_close_decision(
        checks=checks + (static_check,),
        traceability_refs=normalized.traceability_refs,
        governance_refs=normalized.governance_refs,
        source_check_refs=(
            lifecycle_request.candidate_id,
            alignment_request.candidate_id,
            governance_request.candidate_id,
        ),
    )
    skeleton_pass = all(c.valid for c in checks) and static_check.valid
    result = assemble_orchestration_result(
        plan_candidate=plan_candidate,
        route_candidate=route_candidate,
        handoff_candidate=handoff_candidate,
        traceability_bundle=traceability_bundle,
        decision_candidate=decision_candidate,
        lifecycle_request=lifecycle_request,
        alignment_request=alignment_request,
        governance_request=governance_request,
        skeleton_pass=skeleton_pass,
    )
    result_validation = validate_orchestration_result_candidate(result)
    return {
        "normalized_input": normalized,
        "plan_candidate": plan_candidate,
        "route_candidate": route_candidate,
        "handoff_candidate": handoff_candidate,
        "traceability_bundle": traceability_bundle,
        "decision_candidate": decision_candidate,
        "lifecycle_request": lifecycle_request,
        "alignment_request": alignment_request,
        "governance_request": governance_request,
        "result_candidate": result,
        "skeleton_pass": skeleton_pass and result_validation.valid,
        "validation": result_validation,
        "candidate_only": True,
        "side_effect_allowed": False,
        "real_execution": False,
        "runtime_required_now": False,
    }
