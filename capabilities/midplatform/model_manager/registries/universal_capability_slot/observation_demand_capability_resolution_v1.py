"""Controlled resolution from Cognitive Observation Demand to capabilities.

The Capability Registry / Capability Governance boundary owns the controlled
inventory and resolution projection here.  The bridge accepts only explicit
Demand-to-capability-class mappings and never binds a provider, model, slot, or
runtime execution handle.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import (
    ObservationDemandCandidateV1,
)


CAPABILITY_RESOLUTION_OWNER = "Capability Registry / Capability Governance"
CAPABILITY_ADMISSION_OWNER = "Capability Admission Governance"
CAPABILITY_AVAILABILITY_VALUES = ("AVAILABLE", "UNAVAILABLE")
CAPABILITY_ADMISSION_VALUES = ("ADMITTED", "NOT_ADMITTED")
RESOLUTION_STATUSES = (
    "CAPABILITY_CANDIDATES_RESOLVED",
    "NO_CAPABILITY_REQUIREMENT",
    "NO_MATCHING_CAPABILITY",
    "CAPABILITY_UNAVAILABLE",
    "INVALID_INPUT",
    "UNSUPPORTED_REQUIREMENT_SHAPE",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class GovernedObservationCapabilityRequirementMappingV1:
    """Explicit Demand-to-capability-class mapping; not an inventory record."""

    mapping_ref: str
    observation_demand_ref: str
    required_capability_class_refs: Tuple[str, ...]
    mapping_basis_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ObservationDemandCapabilityRequirementAdapterV1:
    """Minimal bridge projection owned by the capability boundary."""

    requirement_ref: str
    source_observation_demand_ref: str
    source_strategy_ref: str
    source_branch_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    required_capability_class_ref: str
    source_mapping_ref: str
    mapping_basis_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class GovernedCapabilityInventoryEntryV1:
    """Read-only controlled inventory snapshot, without implementation identity."""

    capability_candidate_ref: str
    capability_class_ref: str
    availability_status: str
    admission_status: str
    eligible: bool
    slot_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ObservationDemandCapabilityResolutionCandidateV1:
    """One matched capability candidate for one Demand-derived requirement."""

    capability_resolution_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    source_requirement_ref: str
    source_observation_demand_ref: str
    source_strategy_ref: str
    source_branch_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    match_basis_refs: Tuple[str, ...]
    availability_status: str
    admission_status: str
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    provider_binding: bool = False
    model_binding: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    capability_execution: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ObservationDemandCapabilityResolutionInputV1:
    """Controlled Demand, explicit mappings, and read-only inventory snapshot."""

    resolution_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    observation_demands: Tuple[ObservationDemandCandidateV1, ...] = field(
        default_factory=tuple
    )
    governed_requirement_mappings: Tuple[
        GovernedObservationCapabilityRequirementMappingV1, ...
    ] = field(default_factory=tuple)
    capability_inventory: Tuple[GovernedCapabilityInventoryEntryV1, ...] = field(
        default_factory=tuple
    )
    current_cognitive_state_ref: str = ""
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationDemandCapabilityResolutionResultV1:
    """Resolution result with candidate-only, no-binding boundary markers."""

    resolution_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    resolution_status: str
    input_observation_demand_refs: Tuple[str, ...]
    requirement_refs: Tuple[str, ...]
    resolved_candidate_refs: Tuple[str, ...]
    resolved_candidates: Tuple[ObservationDemandCapabilityResolutionCandidateV1, ...]
    excluded_observation_demand_refs: Tuple[str, ...]
    excluded_inventory_refs: Tuple[str, ...]
    exclusion_reasons: Tuple[Tuple[str, str], ...]
    requirements: Tuple[ObservationDemandCapabilityRequirementAdapterV1, ...]
    current_cognitive_state_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    provider_binding: bool = False
    model_binding: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    capability_scheduling: bool = False
    capability_execution: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    perception_routing: bool = False
    observation_gateway_request: bool = False
    fpo_runtime_request: bool = False
    resource_acquisition: bool = False
    ranking_executed: bool = False
    winner_selected: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    memory_pcn_mutation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _requirement_ref(resolution_ref: str, demand_ref: str, mapping_ref: str) -> str:
    digest = hashlib.sha256(
        f"{resolution_ref}|{demand_ref}|{mapping_ref}".encode("utf-8")
    ).hexdigest()[:24]
    return f"capability-requirement:observation-demand:{digest}"


def _candidate_ref(resolution_ref: str, requirement_ref: str, capability_ref: str) -> str:
    digest = hashlib.sha256(
        f"{resolution_ref}|{requirement_ref}|{capability_ref}".encode("utf-8")
    ).hexdigest()[:24]
    return f"capability-resolution:candidate:{digest}"


def _invalid_result(
    request: ObservationDemandCapabilityResolutionInputV1,
    errors: Tuple[str, ...],
    *,
    status: str = "INVALID_INPUT",
) -> ObservationDemandCapabilityResolutionResultV1:
    demand_refs = tuple(demand.observation_demand_ref for demand in request.observation_demands)
    return ObservationDemandCapabilityResolutionResultV1(
        resolution_ref=request.resolution_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        resolution_status=status,
        input_observation_demand_refs=demand_refs,
        requirement_refs=(),
        resolved_candidate_refs=(),
        resolved_candidates=(),
        excluded_observation_demand_refs=demand_refs,
        excluded_inventory_refs=(),
        exclusion_reasons=(),
        requirements=(),
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        context_refs=request.context_refs,
        provenance_refs=_unique(("provenance:capability-governance:observation-demand:v1", *request.provenance_refs)),
        trace_ref=request.trace_ref or f"trace:{request.resolution_ref}",
        validation_errors=errors,
    )


def _validate(
    request: ObservationDemandCapabilityResolutionInputV1,
) -> Tuple[str, ...]:
    errors = []
    if not request.resolution_ref:
        errors.append("resolution_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("resolution_not_candidate_only")

    demand_refs = tuple(demand.observation_demand_ref for demand in request.observation_demands)
    if len(set(demand_refs)) != len(demand_refs):
        errors.append("duplicate_observation_demand_ref")
    demand_ref_set = set(demand_refs)
    for demand in request.observation_demands:
        if (
            not demand.observation_demand_ref
            or not demand.candidate_only
            or not demand.read_only
            or demand.truth_declared
            or demand.world_truth_declared
            or demand.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or demand.source_state_ref != request.source_state_ref
        ):
            errors.append(f"invalid_observation_demand:{demand.observation_demand_ref}")

    mapping_by_demand = {}
    for mapping in request.governed_requirement_mappings:
        if mapping.observation_demand_ref in mapping_by_demand:
            errors.append(f"duplicate_capability_mapping:{mapping.observation_demand_ref}")
        mapping_by_demand[mapping.observation_demand_ref] = mapping
        if (
            not mapping.mapping_ref
            or mapping.observation_demand_ref not in demand_ref_set
            or not mapping.required_capability_class_refs
            or not mapping.candidate_only
            or not mapping.read_only
            or mapping.truth_declared
            or mapping.world_truth_declared
        ):
            errors.append(f"invalid_capability_mapping:{mapping.observation_demand_ref}")

    if not isinstance(request.capability_inventory, tuple):
        errors.append("capability_inventory_must_be_tuple")
    else:
        inventory_refs = tuple(
            item.capability_candidate_ref
            for item in request.capability_inventory
            if isinstance(item, GovernedCapabilityInventoryEntryV1)
        )
        if len(set(inventory_refs)) != len(inventory_refs):
            errors.append("duplicate_capability_candidate_ref")
        for item in request.capability_inventory:
            if not isinstance(item, GovernedCapabilityInventoryEntryV1):
                errors.append("invalid_capability_inventory_entry_type")
                continue
            if (
                not item.capability_candidate_ref
                or not item.capability_class_ref
                or item.availability_status not in CAPABILITY_AVAILABILITY_VALUES
                or item.admission_status not in CAPABILITY_ADMISSION_VALUES
                or not item.candidate_only
                or not item.read_only
                or item.truth_declared
                or item.world_truth_declared
            ):
                errors.append(f"invalid_capability_inventory_entry:{item.capability_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def _build_requirement(
    demand: ObservationDemandCandidateV1,
    mapping: GovernedObservationCapabilityRequirementMappingV1,
    request: ObservationDemandCapabilityResolutionInputV1,
) -> ObservationDemandCapabilityRequirementAdapterV1:
    class_ref = mapping.required_capability_class_refs[0]
    requirement_ref = _requirement_ref(
        request.resolution_ref, demand.observation_demand_ref, mapping.mapping_ref
    )
    return ObservationDemandCapabilityRequirementAdapterV1(
        requirement_ref=requirement_ref,
        source_observation_demand_ref=demand.observation_demand_ref,
        source_strategy_ref=demand.source_strategy_ref,
        source_branch_ref=demand.source_branch_ref,
        parent_cognitive_problem_ref=demand.parent_cognitive_problem_ref,
        source_state_ref=demand.source_state_ref,
        information_need_refs=demand.information_need_refs,
        information_gap_refs=demand.information_gap_refs,
        required_capability_class_ref=class_ref,
        source_mapping_ref=mapping.mapping_ref,
        mapping_basis_refs=mapping.mapping_basis_refs,
        lineage_refs=_unique((*demand.lineage_refs, mapping.mapping_ref, requirement_ref)),
        provenance_refs=_unique((*demand.provenance_refs, *mapping.provenance_refs)),
        trace_ref=mapping.trace_ref or demand.trace_ref,
    )


def resolve_observation_demand_capabilities(
    request: ObservationDemandCapabilityResolutionInputV1,
) -> ObservationDemandCapabilityResolutionResultV1:
    """Resolve exact class matches from a controlled read-only inventory."""

    errors = _validate(request)
    if errors:
        return _invalid_result(request, errors)
    demands = request.observation_demands
    demand_refs = tuple(demand.observation_demand_ref for demand in demands)
    if not demands:
        return _invalid_result(
            request,
            (),
            status="NO_CAPABILITY_REQUIREMENT",
        )
    mappings = {
        mapping.observation_demand_ref: mapping
        for mapping in request.governed_requirement_mappings
    }
    if any(demand.observation_demand_ref not in mappings for demand in demands):
        return _invalid_result(
            request,
            ("governed_capability_mapping_missing",),
            status="NO_CAPABILITY_REQUIREMENT",
        )
    if any(
        len(mappings[demand.observation_demand_ref].required_capability_class_refs) != 1
        for demand in demands
    ):
        return _invalid_result(
            request,
            ("multi_class_requirement_not_supported",),
            status="UNSUPPORTED_REQUIREMENT_SHAPE",
        )

    requirements = tuple(
        _build_requirement(demand, mappings[demand.observation_demand_ref], request)
        for demand in demands
    )
    candidates = []
    excluded_inventory_refs = []
    exclusion_reasons = []
    unavailable_seen = False
    matching_seen = False
    for requirement in requirements:
        matching = tuple(
            item
            for item in request.capability_inventory
            if item.capability_class_ref == requirement.required_capability_class_ref
        )
        matching_seen = matching_seen or bool(matching)
        for item in matching:
            if item.availability_status != "AVAILABLE":
                unavailable_seen = True
                excluded_inventory_refs.append(item.capability_candidate_ref)
                exclusion_reasons.append((item.capability_candidate_ref, "CAPABILITY_UNAVAILABLE"))
                continue
            if item.admission_status != "ADMITTED" or not item.eligible:
                unavailable_seen = True
                excluded_inventory_refs.append(item.capability_candidate_ref)
                exclusion_reasons.append((item.capability_candidate_ref, "CAPABILITY_NOT_ADMITTED"))
                continue
            candidate_ref = _candidate_ref(
                request.resolution_ref,
                requirement.requirement_ref,
                item.capability_candidate_ref,
            )
            candidates.append(
                ObservationDemandCapabilityResolutionCandidateV1(
                    capability_resolution_candidate_ref=candidate_ref,
                    capability_candidate_ref=item.capability_candidate_ref,
                    capability_class_ref=item.capability_class_ref,
                    source_requirement_ref=requirement.requirement_ref,
                    source_observation_demand_ref=requirement.source_observation_demand_ref,
                    source_strategy_ref=requirement.source_strategy_ref,
                    source_branch_ref=requirement.source_branch_ref,
                    parent_cognitive_problem_ref=requirement.parent_cognitive_problem_ref,
                    source_state_ref=requirement.source_state_ref,
                    information_need_refs=requirement.information_need_refs,
                    information_gap_refs=requirement.information_gap_refs,
                    match_basis_refs=_unique(
                        ("governed:exact-capability-class", requirement.required_capability_class_ref)
                    ),
                    availability_status=item.availability_status,
                    admission_status=item.admission_status,
                    lineage_refs=_unique(
                        (*requirement.lineage_refs, item.capability_candidate_ref, candidate_ref)
                    ),
                    provenance_refs=_unique(
                        (*requirement.provenance_refs, *item.provenance_refs, item.trace_ref)
                    ),
                    trace_ref=request.trace_ref or requirement.trace_ref,
                )
            )

    if candidates:
        status = "CAPABILITY_CANDIDATES_RESOLVED"
    elif matching_seen and unavailable_seen:
        status = "CAPABILITY_UNAVAILABLE"
    else:
        status = "NO_MATCHING_CAPABILITY"
    return ObservationDemandCapabilityResolutionResultV1(
        resolution_ref=request.resolution_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        resolution_status=status,
        input_observation_demand_refs=demand_refs,
        requirement_refs=tuple(requirement.requirement_ref for requirement in requirements),
        resolved_candidate_refs=tuple(candidate.capability_resolution_candidate_ref for candidate in candidates),
        resolved_candidates=tuple(candidates),
        excluded_observation_demand_refs=tuple(
            demand.observation_demand_ref
            for demand in demands
            if not any(candidate.source_observation_demand_ref == demand.observation_demand_ref for candidate in candidates)
        ),
        excluded_inventory_refs=_unique(excluded_inventory_refs),
        exclusion_reasons=tuple(exclusion_reasons),
        requirements=requirements,
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        context_refs=request.context_refs,
        provenance_refs=_unique(("provenance:capability-governance:observation-demand:v1", *request.provenance_refs)),
        trace_ref=request.trace_ref or f"trace:{request.resolution_ref}",
    )


__all__ = [
    "CAPABILITY_RESOLUTION_OWNER",
    "CAPABILITY_ADMISSION_OWNER",
    "CAPABILITY_AVAILABILITY_VALUES",
    "CAPABILITY_ADMISSION_VALUES",
    "RESOLUTION_STATUSES",
    "GovernedObservationCapabilityRequirementMappingV1",
    "ObservationDemandCapabilityRequirementAdapterV1",
    "GovernedCapabilityInventoryEntryV1",
    "ObservationDemandCapabilityResolutionCandidateV1",
    "ObservationDemandCapabilityResolutionInputV1",
    "ObservationDemandCapabilityResolutionResultV1",
    "resolve_observation_demand_capabilities",
]
