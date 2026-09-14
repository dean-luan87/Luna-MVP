# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration builders v1 — candidate builders only."""

from __future__ import annotations

from typing import Optional, Tuple

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


def _refs(*items: str) -> Tuple[str, ...]:
    return tuple(x for x in items if x)


def build_orchestration_plan_candidate(
    input_candidate: OrchestrationInputCandidate,
    *,
    plan_stage: str = "controlled_skeleton_plan",
) -> OrchestrationPlanCandidate:
    return OrchestrationPlanCandidate(
        candidate_id=f"orch_plan_{input_candidate.candidate_id}",
        input_candidate_ref=input_candidate.candidate_id,
        plan_stage=plan_stage,
        boundary_registry_ref=input_candidate.boundary_registry_ref,
        lifecycle_state_ref=input_candidate.lifecycle_state_ref,
        alignment_rule_ref=input_candidate.alignment_rule_ref,
        governance_constraint_ref=input_candidate.governance_constraint_ref,
        traceability_refs=_refs(input_candidate.protocol_trace_ref, *input_candidate.traceability_refs),
        governance_refs=input_candidate.governance_refs,
    )


def build_candidate_route_candidate(
    plan_candidate: OrchestrationPlanCandidate,
    *,
    route_target_module_ref: str,
    route_reason: str = "controlled_skeleton_route_candidate",
) -> CandidateRouteCandidate:
    return CandidateRouteCandidate(
        candidate_id=f"orch_route_{plan_candidate.candidate_id}",
        plan_candidate_ref=plan_candidate.candidate_id,
        route_target_module_ref=route_target_module_ref,
        route_reason=route_reason,
        boundary_registry_ref=plan_candidate.boundary_registry_ref,
        traceability_refs=plan_candidate.traceability_refs,
        governance_refs=plan_candidate.governance_refs,
    )


def build_module_handoff_candidate(
    route_candidate: CandidateRouteCandidate,
    *,
    handoff_reason: str = "controlled_skeleton_handoff_candidate",
) -> ModuleHandoffCandidate:
    return ModuleHandoffCandidate(
        candidate_id=f"orch_handoff_{route_candidate.candidate_id}",
        route_candidate_ref=route_candidate.candidate_id,
        target_module_ref=route_candidate.route_target_module_ref,
        handoff_reason=handoff_reason,
        traceability_refs=route_candidate.traceability_refs,
        governance_refs=route_candidate.governance_refs,
    )


def build_lifecycle_transition_request_candidate(
    *,
    lifecycle_state_ref: str,
    transition_intent: str,
    reason: str,
    traceability_refs: Tuple[str, ...],
    governance_refs: Tuple[str, ...],
    candidate_id: Optional[str] = None,
) -> LifecycleTransitionRequestCandidate:
    cid = candidate_id or f"orch_lifecycle_{lifecycle_state_ref}"
    return LifecycleTransitionRequestCandidate(
        candidate_id=cid,
        lifecycle_state_ref=lifecycle_state_ref,
        transition_intent=transition_intent,
        reason=reason,
        traceability_refs=traceability_refs,
        governance_refs=governance_refs,
    )


def build_alignment_check_request_candidate(
    *,
    alignment_rule_ref: str,
    check_scope: str,
    boundary_registry_ref: str,
    traceability_refs: Tuple[str, ...],
    governance_refs: Tuple[str, ...],
    candidate_id: Optional[str] = None,
) -> AlignmentCheckRequestCandidate:
    cid = candidate_id or f"orch_align_{alignment_rule_ref}"
    return AlignmentCheckRequestCandidate(
        candidate_id=cid,
        alignment_rule_ref=alignment_rule_ref,
        check_scope=check_scope,
        boundary_registry_ref=boundary_registry_ref,
        traceability_refs=traceability_refs,
        governance_refs=governance_refs,
    )


def build_governance_check_request_candidate(
    *,
    governance_constraint_ref: str,
    check_scope: str,
    traceability_refs: Tuple[str, ...],
    governance_refs: Tuple[str, ...],
    candidate_id: Optional[str] = None,
) -> GovernanceCheckRequestCandidate:
    cid = candidate_id or f"orch_gov_{governance_constraint_ref}"
    return GovernanceCheckRequestCandidate(
        candidate_id=cid,
        governance_constraint_ref=governance_constraint_ref,
        check_scope=check_scope,
        traceability_refs=traceability_refs,
        governance_refs=governance_refs,
    )


def build_traceability_bundle_candidate(
    *,
    protocol_trace_ref: str,
    alignment_rule_ref: str,
    source_refs: Tuple[str, ...],
    traceability_refs: Tuple[str, ...],
    governance_refs: Tuple[str, ...],
    candidate_id: Optional[str] = None,
) -> TraceabilityBundleCandidate:
    cid = candidate_id or f"orch_trace_{protocol_trace_ref}"
    return TraceabilityBundleCandidate(
        candidate_id=cid,
        protocol_trace_ref=protocol_trace_ref,
        alignment_rule_ref=alignment_rule_ref,
        source_refs=source_refs,
        traceability_refs=traceability_refs,
        governance_refs=governance_refs,
    )


def build_blocker_or_defer_decision_candidate(
    *,
    decision_kind: str,
    decision_reason: str,
    source_check_refs: Tuple[str, ...],
    traceability_refs: Tuple[str, ...],
    governance_refs: Tuple[str, ...],
    candidate_id: Optional[str] = None,
) -> BlockerOrDeferDecisionCandidate:
    cid = candidate_id or f"orch_decision_{decision_kind}"
    return BlockerOrDeferDecisionCandidate(
        candidate_id=cid,
        decision_kind=decision_kind,
        decision_reason=decision_reason,
        source_check_refs=source_check_refs,
        traceability_refs=traceability_refs,
        governance_refs=governance_refs,
    )


def build_orchestration_result_candidate(
    *,
    plan_candidate: OrchestrationPlanCandidate,
    route_candidate: CandidateRouteCandidate,
    handoff_candidate: ModuleHandoffCandidate,
    traceability_bundle: TraceabilityBundleCandidate,
    decision_candidate: BlockerOrDeferDecisionCandidate,
    lifecycle_request: Optional[LifecycleTransitionRequestCandidate],
    alignment_request: Optional[AlignmentCheckRequestCandidate],
    governance_request: Optional[GovernanceCheckRequestCandidate],
    skeleton_pass: bool,
) -> OrchestrationResultCandidate:
    return OrchestrationResultCandidate(
        candidate_id=f"orch_result_{plan_candidate.candidate_id}",
        plan_candidate_ref=plan_candidate.candidate_id,
        route_candidate_ref=route_candidate.candidate_id,
        handoff_candidate_ref=handoff_candidate.candidate_id,
        traceability_bundle_ref=traceability_bundle.candidate_id,
        decision_candidate_ref=decision_candidate.candidate_id,
        lifecycle_request_ref=lifecycle_request.candidate_id if lifecycle_request else None,
        alignment_request_ref=alignment_request.candidate_id if alignment_request else None,
        governance_request_ref=governance_request.candidate_id if governance_request else None,
        traceability_refs=traceability_bundle.traceability_refs,
        governance_refs=plan_candidate.governance_refs,
        skeleton_pass=skeleton_pass,
    )


BUILDER_FUNCTIONS: Tuple[str, ...] = (
    "build_orchestration_plan_candidate",
    "build_candidate_route_candidate",
    "build_module_handoff_candidate",
    "build_lifecycle_transition_request_candidate",
    "build_alignment_check_request_candidate",
    "build_governance_check_request_candidate",
    "build_traceability_bundle_candidate",
    "build_blocker_or_defer_decision_candidate",
    "build_orchestration_result_candidate",
)
