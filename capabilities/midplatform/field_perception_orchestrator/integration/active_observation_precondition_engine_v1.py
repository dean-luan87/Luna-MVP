"""Controlled active-observation precondition evaluation.

The engine is deliberately upstream of provider execution.  It evaluates
whether an observation is necessary and currently eligible; it never invokes
OCR, camera, SLAM, or any other provider.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Mapping, Tuple

from .active_observation_precondition_types_v1 import (
    ActiveObservationPreconditionResultV1,
    MinimumObservationConditionsV1,
    ObservationCapabilityEligibilityCandidateV1,
    ObservationConditionGapV1,
    ObservationFeasibilityCandidateV1,
    ObservationNecessityCandidateV1,
    ObservationPreconditionRequestV1,
    ObservationRequirementV1,
    ObservationWindowCandidateV1,
    RelativeObservationAdjustmentNeedV1,
    RelativeObservationStateV1,
    SelfPerceptualViewpointStateV1,
)
from .field_perception_active_observation_control_types_v1 import (
    CapabilityRequirementCandidateV1,
    ObservationDemandCandidateV1,
    ObservationRequestCandidateV1,
)


PHASE = "Phase-P1-Luna-Active-Observation-Precondition-And-Dynamic-Viewpoint-Foundation-v1-001"
EXECUTION_MODE = "CONTROLLED_DYNAMIC_STATE"
OWNER = "Field Perception Orchestrator / Active Observation Preconditions"


def _tuple(value: Any) -> Tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _ref(prefix: str, case_id: str, state_id: str) -> str:
    return f"{prefix}:{case_id}:{state_id}"


def _canonical_chain(request: ObservationPreconditionRequestV1) -> Dict[str, Any]:
    """Materialize the existing FPO demand/request/requirement contracts."""

    requirement = request.observation_requirement
    demand = ObservationDemandCandidateV1(
        demand_id=request.observation_demand_ref,
        root_cycle_trace_id=_ref("root-cycle", request.case_id, request.state_id),
        source_owner="Field Perception Orchestrator",
        source_context_refs=(request.goal_ref, request.concern_ref),
        source_intent_refs=(request.goal_ref,),
        source_task_refs=tuple(),
        source_safety_refs=tuple(),
        source_field_refs=(requirement.field_ref,),
        information_need=request.information_need_ref,
        expected_evidence_kinds=("OCR_TEXT_EVIDENCE",),
        target_semantics=requirement.target_ref,
        spatial_scope_candidate=requirement.target_ref,
        temporal_scope_candidate=request.temporal_ref,
        urgency_candidate="normal",
        priority_candidate="normal",
        resource_budget_candidate={},
        stop_conditions=("observation_window_closed", "capability_eligible"),
        uncertainty_refs=request.information_gap_refs,
        provenance_refs=request.provenance_refs,
        trace_ref=_ref("trace:demand", request.case_id, request.state_id),
    )
    observation_request = ObservationRequestCandidateV1(
        request_id=request.observation_request_ref,
        demand_ref=demand.demand_id,
        observation_goal=request.information_need_ref,
        target_region_candidate=requirement.target_ref,
        target_semantic_candidate=requirement.target_ref,
        required_capability_kinds=("OCR_TEXT_EVIDENCE",),
        optional_capability_kinds=tuple(),
        forbidden_capability_kinds=tuple(),
        evidence_expectation=("OCR_TEXT_EVIDENCE",),
        budget={},
        temporal_validity={"temporal_ref": request.temporal_ref},
        trace_ref=_ref("trace:request", request.case_id, request.state_id),
        provenance_refs=request.provenance_refs,
    )
    capability_requirement = CapabilityRequirementCandidateV1(
        requirement_id=requirement.capability_requirement_ref,
        observation_request_ref=observation_request.request_id,
        required_capability_kinds=observation_request.required_capability_kinds,
        optional_capability_kinds=tuple(),
        forbidden_capability_kinds=tuple(),
        requirement_reason=request.information_need_ref,
        target_region_candidate=requirement.target_ref,
        semantic_scope_candidate=requirement.target_ref,
        evidence_goal=observation_request.evidence_expectation,
        budget_candidate={},
        trace_ref=_ref("trace:capability", request.case_id, request.state_id),
        provenance_refs=request.provenance_refs,
    )
    return {
        "observation_demand": demand,
        "observation_request": observation_request,
        "capability_requirement": capability_requirement,
    }


def _condition_rows(
    minimum: MinimumObservationConditionsV1,
    self_state: SelfPerceptualViewpointStateV1,
    relative: RelativeObservationStateV1,
) -> Tuple[Tuple[str, str, str], ...]:
    """Return (condition, required, observed) categorical comparisons."""

    return (
        ("target_visibility", minimum.target_visibility_requirement, relative.target_visibility_candidate),
        ("target_completeness", minimum.target_completeness_requirement, relative.target_completeness_candidate),
        ("relative_scale", minimum.relative_scale_requirement, relative.target_scale_candidate),
        ("view_orientation", minimum.view_orientation_requirement, relative.relative_orientation_candidate),
        ("stability", minimum.stability_requirement, relative.stability_candidate),
        ("occlusion", minimum.occlusion_requirement, relative.occlusion_candidate),
        ("sensor", minimum.sensor_requirement, self_state.sensor_availability_candidate),
    )


def _condition_satisfied(required: str, observed: str) -> bool:
    if required in {"NOT_REQUIRED", "UNAVAILABLE"}:
        return required == "NOT_REQUIRED"
    return observed == required


def _necessity(request: ObservationPreconditionRequestV1) -> ObservationNecessityCandidateV1:
    required = set(request.required_information_refs)
    available = set(request.available_information_refs)
    missing = tuple(sorted(required - available))
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:necessity", request.case_id, request.state_id))))
    if request.continuation_possible_candidate is None:
        status = "DEFERRED"
        reason = "continuation feasibility is not available as a candidate"
    elif request.continuation_possible_candidate is True:
        status = "NOT_REQUIRED"
        reason = "current continuation is possible; unknown information does not imply observation"
    elif not request.information_need_ref or not request.observation_requirement.observation_requirement_ref:
        status = "DEFERRED"
        reason = "observation need is not bound to a canonical requirement"
    elif missing:
        status = "REQUIRED"
        reason = "current information need is missing required information and continuation is not possible"
    else:
        status = "NOT_REQUIRED"
        reason = "required information is already available"
    return ObservationNecessityCandidateV1(
        necessity_ref=_ref("observation-necessity", request.case_id, request.state_id),
        observation_requirement_ref=request.observation_requirement.observation_requirement_ref,
        information_need_ref=request.information_need_ref,
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        required_information_refs=request.required_information_refs,
        available_information_refs=request.available_information_refs,
        information_gap_refs=request.information_gap_refs,
        continuation_possible_candidate=request.continuation_possible_candidate,
        status=status,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


def _feasibility(
    request: ObservationPreconditionRequestV1,
    necessity: ObservationNecessityCandidateV1,
) -> ObservationFeasibilityCandidateV1:
    satisfied = []
    unsatisfied = []
    for condition, required, observed in _condition_rows(request.minimum_conditions, request.self_state, request.relative_state):
        ref = _ref(f"condition:{condition}", request.case_id, request.state_id)
        if _condition_satisfied(required, observed):
            satisfied.append(ref)
        elif necessity.status == "REQUIRED":
            unsatisfied.append(ref)

    if necessity.status != "REQUIRED":
        status = "NOT_OBSERVABLE"
        unsatisfied = [_ref("condition:observation_not_required", request.case_id, request.state_id)]
    elif not unsatisfied:
        status = "OBSERVABLE"
    elif request.previous_window_state == "OPEN" and any(
        item.startswith(("condition:occlusion", "condition:target_visibility", "condition:stability"))
        for item in unsatisfied
    ):
        status = "LOSING_OBSERVABILITY"
    elif any(item.startswith("condition:stability") for item in unsatisfied):
        status = "OBSERVABLE_UNSTABLE"
    elif any(item.startswith("condition:target_visibility") for item in unsatisfied):
        status = "NOT_OBSERVABLE"
    else:
        status = "APPROACHING_OBSERVABLE"

    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:feasibility", request.case_id, request.state_id))))
    return ObservationFeasibilityCandidateV1(
        feasibility_ref=_ref("observation-feasibility", request.case_id, request.state_id),
        observation_requirement_ref=request.observation_requirement.observation_requirement_ref,
        necessity_ref=necessity.necessity_ref,
        minimum_conditions_ref=_ref("minimum-conditions", request.case_id, request.state_id),
        self_state_ref=request.self_state.state_ref,
        relative_state_ref=request.relative_state.relative_state_ref,
        field_ref=request.observation_requirement.field_ref,
        target_ref=request.observation_requirement.target_ref,
        status=status,
        satisfied_condition_refs=tuple(satisfied),
        unsatisfied_condition_refs=tuple(unsatisfied),
        trace_refs=trace,
        provenance_refs=trace,
    )


def _window(
    request: ObservationPreconditionRequestV1,
    necessity: ObservationNecessityCandidateV1,
    feasibility: ObservationFeasibilityCandidateV1,
) -> ObservationWindowCandidateV1:
    if necessity.status == "REQUIRED" and feasibility.status == "OBSERVABLE" and not feasibility.unsatisfied_condition_refs:
        status = "OPEN"
        reason = "observation is required and all requirement-relative conditions are satisfied"
    elif feasibility.status == "OBSERVABLE_UNSTABLE":
        status = "UNSTABLE"
        reason = "observation conditions are present but stability is insufficient"
    else:
        status = "CLOSED"
        reason = "observation necessity or requirement-relative conditions do not permit observation now"
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:window", request.case_id, request.state_id))))
    return ObservationWindowCandidateV1(
        window_ref=_ref("observation-window", request.case_id, request.state_id),
        observation_requirement_ref=request.observation_requirement.observation_requirement_ref,
        necessity_ref=necessity.necessity_ref,
        feasibility_ref=feasibility.feasibility_ref,
        status=status,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


def _eligibility(
    request: ObservationPreconditionRequestV1,
    necessity: ObservationNecessityCandidateV1,
    window: ObservationWindowCandidateV1,
) -> ObservationCapabilityEligibilityCandidateV1:
    available = request.observation_requirement.capability_ref in request.available_capabilities
    eligible = necessity.status == "REQUIRED" and window.status == "OPEN" and available
    if eligible:
        reason = "required observation window is open and capability is available; invocation remains a separate step"
    elif not available:
        reason = "canonical capability is unavailable"
    elif window.status != "OPEN":
        reason = "observation window is not open"
    else:
        reason = "observation is not necessary"
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:eligibility", request.case_id, request.state_id))))
    return ObservationCapabilityEligibilityCandidateV1(
        eligibility_ref=_ref("observation-eligibility", request.case_id, request.state_id),
        observation_requirement_ref=request.observation_requirement.observation_requirement_ref,
        capability_ref=request.observation_requirement.capability_ref,
        necessity_ref=necessity.necessity_ref,
        window_ref=window.window_ref,
        eligible_now=eligible,
        capability_available_candidate=available,
        reason=reason,
        trace_refs=trace,
        provenance_refs=trace,
    )


_GAP_MAP = {
    "target_visibility": "TARGET_NOT_VISIBLE",
    "target_completeness": "TARGET_INCOMPLETE",
    "relative_scale": "TARGET_TOO_SMALL",
    "view_orientation": "VIEW_ORIENTATION_UNSUITABLE",
    "stability": "MOTION_UNSTABLE",
    "occlusion": "OCCLUDED",
    "sensor": "SENSOR_UNAVAILABLE",
}
_ADJUSTMENT_MAP = {
    "target_visibility": "NEED_TARGET_VISIBLE",
    "target_completeness": "NEED_TARGET_MORE_COMPLETE",
    "relative_scale": "NEED_LARGER_TARGET_SCALE",
    "view_orientation": "NEED_MORE_FRONTAL_VIEW",
    "stability": "NEED_STABLE_VIEW",
    "occlusion": "NEED_CLEAR_LINE_OF_SIGHT",
    "sensor": "NEED_SENSOR_AVAILABLE",
}


def _gaps_and_adjustments(
    request: ObservationPreconditionRequestV1,
    necessity: ObservationNecessityCandidateV1,
    feasibility: ObservationFeasibilityCandidateV1,
) -> Tuple[Tuple[ObservationConditionGapV1, ...], Tuple[RelativeObservationAdjustmentNeedV1, ...]]:
    if necessity.status != "REQUIRED":
        return tuple(), tuple()
    gaps = []
    adjustments = []
    unsatisfied_by_ref = {ref.split(":", 2)[1]: ref for ref in feasibility.unsatisfied_condition_refs if ref.startswith("condition:")}
    for condition, _, _ in _condition_rows(request.minimum_conditions, request.self_state, request.relative_state):
        condition_ref = unsatisfied_by_ref.get(condition)
        if not condition_ref or condition not in _GAP_MAP:
            continue
        gap_ref = _ref("observation-condition-gap", request.case_id, request.state_id) + f":{condition}"
        gap = ObservationConditionGapV1(
            gap_ref=gap_ref,
            observation_requirement_ref=request.observation_requirement.observation_requirement_ref,
            information_need_ref=request.information_need_ref,
            kind=_GAP_MAP[condition],
            unsatisfied_condition_ref=condition_ref,
            reason=f"{condition} does not satisfy the current observation requirement",
            trace_refs=tuple(dict.fromkeys((*request.provenance_refs, gap_ref))),
            provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, gap_ref))),
        )
        adjustment_ref = _ref("relative-adjustment", request.case_id, request.state_id) + f":{condition}"
        adjustment = RelativeObservationAdjustmentNeedV1(
            adjustment_ref=adjustment_ref,
            observation_requirement_ref=request.observation_requirement.observation_requirement_ref,
            condition_gap_ref=gap_ref,
            kind=_ADJUSTMENT_MAP[condition],
            reason=f"improve {condition} before capability eligibility",
            trace_refs=tuple(dict.fromkeys((*request.provenance_refs, gap_ref, adjustment_ref))),
            provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, gap_ref, adjustment_ref))),
        )
        gaps.append(gap)
        adjustments.append(adjustment)
    return tuple(gaps), tuple(adjustments)


def evaluate(request: ObservationPreconditionRequestV1) -> Tuple[ActiveObservationPreconditionResultV1, Dict[str, Any]]:
    necessity = _necessity(request)
    feasibility = _feasibility(request, necessity)
    window = _window(request, necessity, feasibility)
    eligibility = _eligibility(request, necessity, window)
    gaps, adjustments = _gaps_and_adjustments(request, necessity, feasibility)
    trace = tuple(dict.fromkeys((*request.provenance_refs, _ref("trace:precondition", request.case_id, request.state_id))))
    result = ActiveObservationPreconditionResultV1(
        case_id=request.case_id,
        state_id=request.state_id,
        cycle_index=request.cycle_index,
        request=request,
        necessity=necessity,
        feasibility=feasibility,
        window=window,
        capability_eligibility=eligibility,
        condition_gaps=gaps,
        adjustment_needs=adjustments,
        trace_refs=trace,
        provenance_refs=trace,
        behavior={
            "runtime_execution": False,
            "provider_invocation": False,
            "model_invocation": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "device_control": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "self_owns_observation_decision": False,
            "capability_eligible_means_provider_invoked": False,
            "scenario_id_semantic_driver": False,
        },
    )
    return result, _canonical_chain(request)


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


__all__ = ["EXECUTION_MODE", "OWNER", "PHASE", "evaluate", "jsonable"]
