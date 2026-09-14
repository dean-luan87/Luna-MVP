"""Candidate-only handoff from capability resolution to perception control.

This module is deliberately positioned before the existing Observation Gateway
runtime ingress.  It projects already-resolved capability candidates into
perception routing candidates; it does not route, admit, bind, schedule, or
execute anything.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import (
    ObservationDemandCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.observation_demand_capability_resolution_v1 import (
    ObservationDemandCapabilityRequirementAdapterV1,
    ObservationDemandCapabilityResolutionCandidateV1,
    ObservationDemandCapabilityResolutionResultV1,
)


PERCEPTION_ROUTING_OWNER = "Observation Control / Perception Routing Candidate Formation"
FORMATION_STATUSES = (
    "ROUTING_CANDIDATES_FORMED",
    "NO_ROUTING_CANDIDATE",
    "INVALID_INPUT",
    "UNSUPPORTED_ROUTING_SHAPE",
)
ZERO_RESOLUTION_STATUSES = {
    "NO_CAPABILITY_REQUIREMENT",
    "NO_MATCHING_CAPABILITY",
    "CAPABILITY_UNAVAILABLE",
    "UNSUPPORTED_REQUIREMENT_SHAPE",
}


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def _safe_refs(value: object, attribute: str) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        getattr(item, attribute)
        for item in value
        if hasattr(item, attribute)
    )


@dataclass(frozen=True)
class PerceptionRoutingCandidateV1:
    """One Demand x resolved-capability handoff candidate.

    The candidate says that a compatible capability may be handed to a future
    perception-control boundary.  It is not a submitted runtime request.
    """

    perception_routing_candidate_ref: str
    source_observation_demand_ref: str
    source_capability_requirement_ref: str
    source_capability_resolution_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    slot_ref: str
    observation_class: str
    observation_target_refs: Tuple[str, ...]
    observation_constraint_refs: Tuple[str, ...]
    expected_information_contribution_refs: Tuple[str, ...]
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    source_strategy_ref: str
    source_branch_ref: str
    parent_cognitive_problem_ref: str
    routing_basis_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    routing_executed: bool = False
    gateway_submission: bool = False
    fpo_runtime_request: bool = False
    provider_binding: bool = False
    provider_invocation: bool = False
    model_binding: bool = False
    model_invocation: bool = False
    observation_execution: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    routing_admitted: bool = False
    route_priority_assigned: bool = False


@dataclass(frozen=True)
class PerceptionRoutingFormationInputV1:
    """Resolution output plus the immutable upstream projections it references."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    observation_demands: Tuple[ObservationDemandCandidateV1, ...] = field(
        default_factory=tuple
    )
    capability_requirements: Tuple[
        ObservationDemandCapabilityRequirementAdapterV1, ...
    ] = field(default_factory=tuple)
    resolution_result: ObservationDemandCapabilityResolutionResultV1 | None = None
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class PerceptionRoutingFormationResultV1:
    """Immutable routing candidates and explicit non-runtime boundary markers."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_resolution_candidate_refs: Tuple[str, ...]
    routing_candidate_refs: Tuple[str, ...]
    routes: Tuple[PerceptionRoutingCandidateV1, ...]
    excluded_resolution_candidate_refs: Tuple[str, ...]
    current_cognitive_state_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    routing_executed: bool = False
    routing_admitted: bool = False
    route_priority_assigned: bool = False
    route_ranking_executed: bool = False
    route_winner_selected: bool = False
    gateway_submission: bool = False
    fpo_runtime_request: bool = False
    provider_binding: bool = False
    provider_invocation: bool = False
    model_binding: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    capability_scheduling: bool = False
    observation_execution: bool = False
    resource_scheduling: bool = False
    resource_acquisition: bool = False
    attention_formed: bool = False
    evidence_ingress: bool = False
    evidence_fusion_executed: bool = False
    conflict_resolution_executed: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    memory_pcn_mutation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _route_ref(formation_ref: str, demand_ref: str, resolution_ref: str) -> str:
    digest = hashlib.sha256(
        f"{formation_ref}|{demand_ref}|{resolution_ref}".encode("utf-8")
    ).hexdigest()[:24]
    return f"perception-routing:candidate:{digest}"


def _result(
    request: PerceptionRoutingFormationInputV1,
    status: str,
    candidate_refs: Tuple[str, ...],
    routes: Tuple[PerceptionRoutingCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> PerceptionRoutingFormationResultV1:
    resolution = request.resolution_result
    return PerceptionRoutingFormationResultV1(
        formation_ref=request.formation_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status=status,
        input_resolution_candidate_refs=candidate_refs,
        routing_candidate_refs=tuple(route.perception_routing_candidate_ref for route in routes),
        routes=routes,
        excluded_resolution_candidate_refs=tuple(
            ref for ref in candidate_refs
            if ref not in {route.source_capability_resolution_candidate_ref for route in routes}
        ),
        current_cognitive_state_ref=(
            resolution.current_cognitive_state_ref if resolution else ""
        ),
        context_refs=request.context_refs,
        provenance_refs=_unique(
            ("provenance:observation-control:perception-routing:v1", *request.provenance_refs)
        ),
        trace_ref=request.trace_ref or f"trace:{request.formation_ref}",
        validation_errors=errors,
    )


def _validate(request: PerceptionRoutingFormationInputV1) -> Tuple[str, ...]:
    errors = []
    resolution = request.resolution_result
    if not request.formation_ref:
        errors.append("formation_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("formation_not_candidate_only")
    if not isinstance(request.observation_demands, tuple):
        errors.append("observation_demands_must_be_tuple")
    if not isinstance(request.capability_requirements, tuple):
        errors.append("capability_requirements_must_be_tuple")
    if resolution is None:
        errors.append("resolution_result_missing")
        return tuple(errors)
    if not resolution.candidate_only or not resolution.read_only:
        errors.append("resolution_not_read_only_candidate")
    if resolution.truth_declared or resolution.world_truth_declared:
        errors.append("resolution_truth_declared")
    if (
        resolution.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
        or resolution.source_state_ref != request.source_state_ref
    ):
        errors.append("resolution_context_mismatch")
    if resolution.resolution_status == "INVALID_INPUT":
        errors.append("upstream_resolution_invalid")

    demands = request.observation_demands if isinstance(request.observation_demands, tuple) else ()
    requirements = (
        request.capability_requirements
        if isinstance(request.capability_requirements, tuple)
        else ()
    )
    candidates = (
        resolution.resolved_candidates
        if isinstance(resolution.resolved_candidates, tuple)
        else ()
    )
    if candidates and resolution.resolution_status != "CAPABILITY_CANDIDATES_RESOLVED":
        errors.append("resolution_status_candidate_mismatch")
    resolution_demand_refs = set(resolution.input_observation_demand_refs)
    resolution_requirement_refs = set(resolution.requirement_refs)
    requirement_refs = tuple(
        requirement.requirement_ref
        for requirement in requirements
        if isinstance(requirement, ObservationDemandCapabilityRequirementAdapterV1)
    )
    if requirement_refs != tuple(resolution.requirement_refs):
        errors.append("resolution_requirement_universe_mismatch")
    demand_by_ref = {}
    for demand in demands:
        if not isinstance(demand, ObservationDemandCandidateV1):
            errors.append("invalid_observation_demand_type")
            continue
        if demand.observation_demand_ref in demand_by_ref:
            errors.append(f"duplicate_observation_demand:{demand.observation_demand_ref}")
        demand_by_ref[demand.observation_demand_ref] = demand
        if (
            not demand.candidate_only
            or not demand.read_only
            or demand.truth_declared
            or demand.world_truth_declared
            or demand.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or demand.source_state_ref != request.source_state_ref
        ):
            errors.append(f"invalid_observation_demand:{demand.observation_demand_ref}")

    requirement_by_ref = {}
    for requirement in requirements:
        if not isinstance(requirement, ObservationDemandCapabilityRequirementAdapterV1):
            errors.append("invalid_capability_requirement_type")
            continue
        if requirement.requirement_ref in requirement_by_ref:
            errors.append(f"duplicate_capability_requirement:{requirement.requirement_ref}")
        requirement_by_ref[requirement.requirement_ref] = requirement
        if (
            not requirement.candidate_only
            or not requirement.read_only
            or requirement.truth_declared
            or requirement.world_truth_declared
            or requirement.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or requirement.source_state_ref != request.source_state_ref
        ):
            errors.append(f"invalid_capability_requirement:{requirement.requirement_ref}")

    candidate_refs = tuple(
        candidate.capability_resolution_candidate_ref
        for candidate in candidates
        if isinstance(candidate, ObservationDemandCapabilityResolutionCandidateV1)
    )
    if len(set(candidate_refs)) != len(candidate_refs):
        errors.append("duplicate_resolution_candidate_ref")
    if tuple(resolution.resolved_candidate_refs) != candidate_refs:
        errors.append("resolution_candidate_universe_mismatch")

    for candidate in candidates:
        if not isinstance(candidate, ObservationDemandCapabilityResolutionCandidateV1):
            errors.append("invalid_resolution_candidate_type")
            continue
        demand = demand_by_ref.get(candidate.source_observation_demand_ref)
        requirement = requirement_by_ref.get(candidate.source_requirement_ref)
        if (
            not candidate.capability_resolution_candidate_ref
            or not candidate.capability_candidate_ref
            or not candidate.candidate_only
            or not candidate.read_only
            or candidate.truth_declared
            or candidate.world_truth_declared
            or candidate.availability_status != "AVAILABLE"
            or candidate.admission_status != "ADMITTED"
            or demand is None
            or requirement is None
            or candidate.source_observation_demand_ref not in resolution_demand_refs
            or candidate.source_requirement_ref not in resolution_requirement_refs
        ):
            errors.append(f"invalid_active_resolution_candidate:{candidate.capability_resolution_candidate_ref}")
            continue
        if (
            requirement.source_observation_demand_ref != demand.observation_demand_ref
            or requirement.required_capability_class_ref != candidate.capability_class_ref
            or candidate.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or candidate.source_state_ref != request.source_state_ref
        ):
            errors.append(f"resolution_lineage_mismatch:{candidate.capability_resolution_candidate_ref}")
        if candidate.source_observation_demand_ref not in candidate.lineage_refs:
            errors.append(f"resolution_demand_lineage_missing:{candidate.capability_resolution_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def form_perception_routing_candidates(
    request: PerceptionRoutingFormationInputV1,
) -> PerceptionRoutingFormationResultV1:
    """Project each valid active resolution candidate into one route candidate."""

    errors = _validate(request)
    resolution = request.resolution_result
    if errors:
        candidate_refs = _safe_refs(
            resolution.resolved_candidates if resolution else (),
            "capability_resolution_candidate_ref",
        )
        return _result(request, "INVALID_INPUT", candidate_refs, (), errors)
    assert resolution is not None
    candidate_refs = tuple(
        candidate.capability_resolution_candidate_ref
        for candidate in resolution.resolved_candidates
    )
    if not candidate_refs:
        if resolution.resolution_status not in ZERO_RESOLUTION_STATUSES:
            return _result(
                request,
                "INVALID_INPUT",
                (),
                (),
                (f"unsupported_zero_resolution_status:{resolution.resolution_status}",),
            )
        return _result(request, "NO_ROUTING_CANDIDATE", (), ())

    demands = {item.observation_demand_ref: item for item in request.observation_demands}
    requirements = {item.requirement_ref: item for item in request.capability_requirements}
    routes = []
    for candidate in resolution.resolved_candidates:
        demand = demands[candidate.source_observation_demand_ref]
        requirement = requirements[candidate.source_requirement_ref]
        route_ref = _route_ref(
            request.formation_ref,
            demand.observation_demand_ref,
            candidate.capability_resolution_candidate_ref,
        )
        routes.append(
            PerceptionRoutingCandidateV1(
                perception_routing_candidate_ref=route_ref,
                source_observation_demand_ref=demand.observation_demand_ref,
                source_capability_requirement_ref=requirement.requirement_ref,
                source_capability_resolution_candidate_ref=candidate.capability_resolution_candidate_ref,
                capability_candidate_ref=candidate.capability_candidate_ref,
                capability_class_ref=candidate.capability_class_ref,
                slot_ref="",
                observation_class=demand.observation_class,
                observation_target_refs=demand.observation_target_refs,
                observation_constraint_refs=demand.observation_constraint_refs,
                expected_information_contribution_refs=demand.expected_information_contribution_refs,
                information_need_refs=demand.information_need_refs,
                information_gap_refs=demand.information_gap_refs,
                source_strategy_ref=demand.source_strategy_ref,
                source_branch_ref=demand.source_branch_ref,
                parent_cognitive_problem_ref=demand.parent_cognitive_problem_ref,
                routing_basis_refs=_unique(
                    (
                        "governed:resolution-to-perception-routing",
                        *candidate.match_basis_refs,
                    )
                ),
                context_refs=_unique((*request.context_refs, *demand.context_refs)),
                lineage_refs=_unique(
                    (
                        *demand.lineage_refs,
                        *requirement.lineage_refs,
                        *candidate.lineage_refs,
                        route_ref,
                    )
                ),
                provenance_refs=_unique(
                    (
                        *demand.provenance_refs,
                        *requirement.provenance_refs,
                        *candidate.provenance_refs,
                        *request.provenance_refs,
                    )
                ),
                trace_ref=request.trace_ref or f"trace:{route_ref}",
            )
        )
    route_tuple = tuple(routes)
    return _result(request, "ROUTING_CANDIDATES_FORMED", candidate_refs, route_tuple)


__all__ = [
    "PERCEPTION_ROUTING_OWNER",
    "FORMATION_STATUSES",
    "PerceptionRoutingCandidateV1",
    "PerceptionRoutingFormationInputV1",
    "PerceptionRoutingFormationResultV1",
    "form_perception_routing_candidates",
]
