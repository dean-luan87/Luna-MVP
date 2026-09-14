"""Candidate-only evaluator for situated capability preconditions."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Mapping, Tuple

from .situated_capability_precondition_types_v1 import (
    CapabilityConditionAdjustmentNeedV1,
    CapabilityConditionGapV1,
    CapabilityFeasibilityCandidateV1,
    CapabilityNecessityCandidateV1,
    CapabilityOpportunityCandidateV1,
    SituatedCapabilityEligibilityCandidateV1,
    SituatedCapabilityPreconditionRequestV1,
    SituatedCapabilityPreconditionResultV1,
)


OWNER = "Capability Admission / Capability Governance"
EXECUTION_MODE = "CONTROLLED_SITUATED_STATE"


def _ref(prefix: str, request: SituatedCapabilityPreconditionRequestV1) -> str:
    return f"{prefix}:{request.case_id}:{request.state_id}"


def _necessity(request: SituatedCapabilityPreconditionRequestV1) -> CapabilityNecessityCandidateV1:
    need = request.capability_need
    missing = tuple(sorted(set(need.required_information_refs) - set(need.available_information_refs)))
    if need.capability_need_active_candidate is None or need.continuation_possible_candidate is None:
        status = "DEFERRED"
        reason = "capability need or continuation status is not available as a candidate"
    elif not need.capability_need_active_candidate or need.continuation_possible_candidate:
        status = "NOT_REQUIRED"
        reason = "capability is available as a candidate, but the current need does not require execution"
    elif missing or need.capability_need_active_candidate:
        status = "REQUIRED"
        reason = "current capability need is active and continuation is not currently sufficient"
    else:
        status = "NOT_REQUIRED"
        reason = "current capability need is already covered"
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:capability-necessity", request))))
    return CapabilityNecessityCandidateV1(
        necessity_ref=_ref("capability-necessity", request),
        capability_need_ref=need.capability_need_ref,
        capability_requirement_ref=need.capability_requirement_ref,
        required_information_refs=need.required_information_refs,
        available_information_refs=need.available_information_refs,
        missing_information_refs=missing,
        continuation_possible_candidate=need.continuation_possible_candidate,
        capability_need_active_candidate=need.capability_need_active_candidate,
        status=status,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


def _feasibility(
    request: SituatedCapabilityPreconditionRequestV1,
    necessity: CapabilityNecessityCandidateV1,
) -> CapabilityFeasibilityCandidateV1:
    definition = request.precondition_definition
    minimum = request.minimum_condition_requirement
    state = request.situated_state
    if state.condition_state_candidates:
        condition_status = {
            candidate.condition_ref: candidate.status
            for candidate in state.condition_state_candidates
        }
        satisfied = tuple(
            ref for ref in minimum.required_condition_refs
            if condition_status.get(ref) == "SATISFIED"
        )
        unsatisfied = tuple(
            ref for ref in minimum.required_condition_refs
            if condition_status.get(ref) == "UNSATISFIED"
        )
        unknown = tuple(
            ref for ref in minimum.required_condition_refs
            if condition_status.get(ref, "UNKNOWN") == "UNKNOWN"
        )
    else:
        # Legacy callers remain readable, while the new perception path always
        # supplies condition_state_candidates before feasibility is evaluated.
        satisfied = tuple(ref for ref in minimum.required_condition_refs if ref in state.satisfied_condition_refs)
        unsatisfied = tuple(ref for ref in minimum.required_condition_refs if ref not in state.satisfied_condition_refs)
        unknown = tuple()
    if necessity.status != "REQUIRED":
        status = "NOT_FEASIBLE"
        reason = "capability necessity is not required now"
    elif unsatisfied or unknown:
        status = "NOT_FEASIBLE"
        reason = "one or more capability preconditions are unsatisfied or unknown in the situated state"
    elif state.relation_stability_candidate == "UNSTABLE":
        status = "FEASIBLE_UNSTABLE"
        reason = "preconditions are present but the situated relation is unstable"
    else:
        status = "FEASIBLE"
        reason = "all declared capability preconditions are satisfied"
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:capability-feasibility", request))))
    return CapabilityFeasibilityCandidateV1(
        feasibility_ref=_ref("capability-feasibility", request),
        capability_requirement_ref=definition.capability_requirement_ref,
        capability_need_ref=necessity.capability_need_ref,
        precondition_definition_ref=f"capability-preconditions:{definition.capability_requirement_ref}",
        minimum_condition_requirement_ref=minimum.requirement_ref,
        situated_state_ref=state.situated_state_ref,
        satisfied_condition_refs=satisfied,
        unsatisfied_condition_refs=unsatisfied,
        unknown_condition_refs=unknown,
        status=status,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


def _gaps_and_adjustments(
    request: SituatedCapabilityPreconditionRequestV1,
    necessity: CapabilityNecessityCandidateV1,
    feasibility: CapabilityFeasibilityCandidateV1,
) -> Tuple[Tuple[CapabilityConditionGapV1, ...], Tuple[CapabilityConditionAdjustmentNeedV1, ...]]:
    if necessity.status != "REQUIRED":
        return tuple(), tuple()
    gaps = []
    adjustments = []
    definition = request.precondition_definition
    for condition_ref in (*feasibility.unsatisfied_condition_refs, *feasibility.unknown_condition_refs):
        gap_ref = f"capability-condition-gap:{request.case_id}:{request.state_id}:{condition_ref}"
        gap = CapabilityConditionGapV1(
            condition_gap_ref=gap_ref,
            capability_requirement_ref=definition.capability_requirement_ref,
            capability_need_ref=necessity.capability_need_ref,
            missing_condition_ref=condition_ref,
            reason=(
                "declared capability precondition is unknown in the current situated state"
                if condition_ref in feasibility.unknown_condition_refs
                else "declared capability precondition is not satisfied by the current situated state"
            ),
            trace_refs=tuple(dict.fromkeys((*request.provenance_refs, feasibility.situated_state_ref, gap_ref))),
            provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, feasibility.situated_state_ref, gap_ref))),
        )
        adjustment_kind = definition.adjustment_by_condition_ref.get(condition_ref)
        if adjustment_kind:
            adjustment_ref = f"capability-adjustment-need:{request.case_id}:{request.state_id}:{condition_ref}"
            adjustments.append(CapabilityConditionAdjustmentNeedV1(
                adjustment_need_ref=adjustment_ref,
                capability_requirement_ref=definition.capability_requirement_ref,
                condition_gap_ref=gap_ref,
                adjustment_kind=adjustment_kind,
                reason="candidate condition improvement only; no movement or action is prescribed",
                trace_refs=tuple(dict.fromkeys((*request.provenance_refs, gap_ref, adjustment_ref))),
                provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, gap_ref, adjustment_ref))),
            ))
        gaps.append(gap)
    return tuple(gaps), tuple(adjustments)


def _opportunity(
    request: SituatedCapabilityPreconditionRequestV1,
    necessity: CapabilityNecessityCandidateV1,
    feasibility: CapabilityFeasibilityCandidateV1,
) -> CapabilityOpportunityCandidateV1:
    if necessity.status == "REQUIRED" and feasibility.status == "FEASIBLE":
        status = "OPEN"
        reason = "required capability is feasible in the current situated state"
    elif necessity.status == "REQUIRED" and feasibility.status == "FEASIBLE_UNSTABLE":
        status = "UNSTABLE"
        reason = "required capability is feasible but the situated opportunity is unstable"
    else:
        status = "CLOSED"
        reason = "need or situated feasibility does not establish an execution opportunity"
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:capability-opportunity", request))))
    return CapabilityOpportunityCandidateV1(
        opportunity_ref=_ref("capability-opportunity", request),
        capability_requirement_ref=request.precondition_definition.capability_requirement_ref,
        capability_need_ref=necessity.capability_need_ref,
        feasibility_ref=feasibility.feasibility_ref,
        status=status,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


def _eligibility(
    request: SituatedCapabilityPreconditionRequestV1,
    necessity: CapabilityNecessityCandidateV1,
    feasibility: CapabilityFeasibilityCandidateV1,
    opportunity: CapabilityOpportunityCandidateV1,
) -> SituatedCapabilityEligibilityCandidateV1:
    eligible = (
        necessity.status == "REQUIRED"
        and feasibility.status == "FEASIBLE"
        and opportunity.status == "OPEN"
        and request.capability_available_candidate
    )
    if eligible:
        reason = "necessity, situated feasibility, opportunity, and capability availability are all candidates in agreement"
    elif not request.capability_available_candidate:
        reason = "capability availability is false even though situated feasibility may be true"
    elif feasibility.status != "FEASIBLE":
        reason = "situated capability preconditions are not feasible now"
    elif opportunity.status != "OPEN":
        reason = "capability opportunity is not open"
    else:
        reason = "capability necessity is not required now"
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:capability-eligibility", request))))
    return SituatedCapabilityEligibilityCandidateV1(
        eligibility_ref=_ref("situated-capability-eligibility", request),
        capability_requirement_ref=request.precondition_definition.capability_requirement_ref,
        capability_ref=request.precondition_definition.capability_ref,
        capability_need_ref=necessity.capability_need_ref,
        necessity_ref=necessity.necessity_ref,
        feasibility_ref=feasibility.feasibility_ref,
        opportunity_ref=opportunity.opportunity_ref,
        capability_available_candidate=request.capability_available_candidate,
        eligible_now=eligible,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


def evaluate(request: SituatedCapabilityPreconditionRequestV1) -> SituatedCapabilityPreconditionResultV1:
    necessity = _necessity(request)
    feasibility = _feasibility(request, necessity)
    gaps, adjustments = _gaps_and_adjustments(request, necessity, feasibility)
    opportunity = _opportunity(request, necessity, feasibility)
    eligibility = _eligibility(request, necessity, feasibility, opportunity)
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:situated-capability", request))))
    return SituatedCapabilityPreconditionResultV1(
        case_id=request.case_id,
        state_id=request.state_id,
        cycle_index=request.cycle_index,
        request=request,
        minimum_condition_requirement=request.minimum_condition_requirement,
        necessity=necessity,
        feasibility=feasibility,
        condition_gaps=gaps,
        adjustment_needs=adjustments,
        opportunity=opportunity,
        eligibility=eligibility,
        trace_refs=trace,
        provenance_refs=trace,
        behavior={
            "provider_invocation": False,
            "model_invocation": False,
            "runtime_execution": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "device_control": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "self_owns_capability_decision": False,
            "scenario_id_semantic_driver": False,
            "cycle_index_semantic_driver": False,
        },
    )


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


__all__ = ["EXECUTION_MODE", "OWNER", "evaluate", "jsonable"]
