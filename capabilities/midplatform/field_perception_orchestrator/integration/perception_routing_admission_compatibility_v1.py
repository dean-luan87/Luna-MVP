"""Candidate-only compatibility projection for Perception Routing.

The existing Field Perception Orchestrator owns active-observation control,
while Observation Gateway owns runtime ingress admission.  This module only
projects a valid Perception Routing Candidate into an FPO-facing compatibility
candidate.  It does not make an admission decision and does not submit or
execute an observation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from capabilities.midplatform.core.observation_gateway.perception_routing_candidate_v1 import (
    PerceptionRoutingCandidateV1,
)


OWNER = "Field Perception Orchestrator / Active Observation Control"
SUPPORTED_OBSERVATION_CLASSES = ("PERCEPTION",)
FORMATION_STATUSES = (
    "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED",
    "NO_ADMISSION_COMPATIBILITY_CANDIDATE",
    "ADMISSION_COMPATIBILITY_GAP",
    "INVALID_INPUT",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def _route_refs(value: object) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        route.perception_routing_candidate_ref
        for route in value
        if isinstance(route, PerceptionRoutingCandidateV1)
    )


@dataclass(frozen=True)
class PerceptionRoutingAdmissionCompatibilityCandidateV1:
    """One candidate-only projection toward the existing FPO boundary."""

    admission_compatibility_candidate_ref: str
    source_perception_routing_candidate_ref: str
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
    source_state_ref: str
    context_refs: Tuple[str, ...]
    admission_compatibility_basis_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    owner_ref: str = OWNER
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    fpo_runtime_request: bool = False
    gateway_submission: bool = False
    provider_binding: bool = False
    model_binding: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    observation_execution: bool = False
    attention_formed: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    memory_pcn_mutation: bool = False


@dataclass(frozen=True)
class PerceptionRoutingAdmissionCompatibilityInputV1:
    """Immutable routing-candidate collection supplied by Perception Routing."""

    compatibility_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    routing_candidates: Tuple[PerceptionRoutingCandidateV1, ...] = field(
        default_factory=tuple
    )
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class PerceptionRoutingAdmissionCompatibilityResultV1:
    """Compatibility candidates and explicit no-runtime boundary markers."""

    compatibility_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_perception_routing_candidate_refs: Tuple[str, ...]
    admission_compatibility_candidate_refs: Tuple[str, ...]
    candidates: Tuple[PerceptionRoutingAdmissionCompatibilityCandidateV1, ...]
    excluded_perception_routing_candidate_refs: Tuple[str, ...]
    owner_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    fpo_runtime_request: bool = False
    gateway_submission: bool = False
    provider_binding: bool = False
    model_binding: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    observation_execution: bool = False
    attention_formed: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    memory_pcn_mutation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _candidate_ref(compatibility_ref: str, route_ref: str) -> str:
    digest = hashlib.sha256(
        f"{compatibility_ref}|{route_ref}".encode("utf-8")
    ).hexdigest()[:24]
    return f"fpo-admission-compatibility:candidate:{digest}"


def _result(
    request: PerceptionRoutingAdmissionCompatibilityInputV1,
    status: str,
    route_refs: Tuple[str, ...],
    candidates: Tuple[PerceptionRoutingAdmissionCompatibilityCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> PerceptionRoutingAdmissionCompatibilityResultV1:
    return PerceptionRoutingAdmissionCompatibilityResultV1(
        compatibility_ref=request.compatibility_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status=status,
        input_perception_routing_candidate_refs=route_refs,
        admission_compatibility_candidate_refs=tuple(
            candidate.admission_compatibility_candidate_ref for candidate in candidates
        ),
        candidates=candidates,
        excluded_perception_routing_candidate_refs=tuple(
            ref for ref in route_refs
            if ref not in {
                candidate.source_perception_routing_candidate_ref
                for candidate in candidates
            }
        ),
        owner_ref=OWNER,
        context_refs=request.context_refs,
        provenance_refs=_unique(
            ("provenance:fpo-admission-compatibility:v1", *request.provenance_refs)
        ),
        trace_ref=request.trace_ref or f"trace:{request.compatibility_ref}",
        validation_errors=errors,
    )


def _validate(
    request: PerceptionRoutingAdmissionCompatibilityInputV1,
) -> Tuple[str, ...]:
    errors = []
    if not request.compatibility_ref:
        errors.append("compatibility_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("compatibility_not_candidate_only")
    if not isinstance(request.routing_candidates, tuple):
        return tuple((*errors, "routing_candidates_must_be_tuple"))

    route_refs = _route_refs(request.routing_candidates)
    if len(set(route_refs)) != len(route_refs):
        errors.append("duplicate_perception_routing_candidate_ref")
    for route in request.routing_candidates:
        if not isinstance(route, PerceptionRoutingCandidateV1):
            errors.append("invalid_perception_routing_candidate_type")
            continue
        required_refs = (
            route.perception_routing_candidate_ref,
            route.source_observation_demand_ref,
            route.source_capability_requirement_ref,
            route.source_capability_resolution_candidate_ref,
            route.capability_candidate_ref,
            route.capability_class_ref,
            route.observation_class,
            route.parent_cognitive_problem_ref,
            route.trace_ref,
        )
        if (
            not all(required_refs)
            or not route.observation_target_refs
            or route.observation_class not in SUPPORTED_OBSERVATION_CLASSES
            or not route.candidate_only
            or not route.read_only
            or route.truth_declared
            or route.world_truth_declared
            or route.routing_executed
            or route.routing_admitted
            or route.gateway_submission
            or route.provider_binding
            or route.model_binding
            or route.observation_execution
            or route.capability_activation
            or route.capability_reservation
            or route.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
        ):
            if not route.observation_target_refs:
                errors.append(
                    f"observation_target_missing:{route.perception_routing_candidate_ref}"
                )
            elif route.observation_class not in SUPPORTED_OBSERVATION_CLASSES:
                errors.append(
                    f"unsupported_observation_class:{route.observation_class}"
                )
            else:
                errors.append(
                    f"invalid_perception_routing_candidate:{route.perception_routing_candidate_ref}"
                )
        if route.source_observation_demand_ref not in route.lineage_refs:
            errors.append(
                f"routing_demand_lineage_missing:{route.perception_routing_candidate_ref}"
            )
        if route.source_capability_resolution_candidate_ref not in route.lineage_refs:
            errors.append(
                f"routing_resolution_lineage_missing:{route.perception_routing_candidate_ref}"
            )
    return tuple(dict.fromkeys(errors))


def form_fpo_admission_compatibility_candidates(
    request: PerceptionRoutingAdmissionCompatibilityInputV1,
) -> PerceptionRoutingAdmissionCompatibilityResultV1:
    """Project valid routes without granting runtime admission."""

    errors = _validate(request)
    route_refs = _route_refs(request.routing_candidates)
    if errors:
        status = (
            "ADMISSION_COMPATIBILITY_GAP"
            if any(
                error.startswith(("observation_target_missing:", "unsupported_observation_class:"))
                for error in errors
            )
            else "INVALID_INPUT"
        )
        return _result(request, status, route_refs, (), errors)
    if not route_refs:
        return _result(request, "NO_ADMISSION_COMPATIBILITY_CANDIDATE", (), ())

    candidates = []
    for route in request.routing_candidates:
        candidates.append(
            PerceptionRoutingAdmissionCompatibilityCandidateV1(
                admission_compatibility_candidate_ref=_candidate_ref(
                    request.compatibility_ref,
                    route.perception_routing_candidate_ref,
                ),
                source_perception_routing_candidate_ref=route.perception_routing_candidate_ref,
                source_observation_demand_ref=route.source_observation_demand_ref,
                source_capability_requirement_ref=route.source_capability_requirement_ref,
                source_capability_resolution_candidate_ref=route.source_capability_resolution_candidate_ref,
                capability_candidate_ref=route.capability_candidate_ref,
                capability_class_ref=route.capability_class_ref,
                slot_ref=route.slot_ref,
                observation_class=route.observation_class,
                observation_target_refs=route.observation_target_refs,
                observation_constraint_refs=route.observation_constraint_refs,
                expected_information_contribution_refs=route.expected_information_contribution_refs,
                information_need_refs=route.information_need_refs,
                information_gap_refs=route.information_gap_refs,
                source_strategy_ref=route.source_strategy_ref,
                source_branch_ref=route.source_branch_ref,
                parent_cognitive_problem_ref=route.parent_cognitive_problem_ref,
                source_state_ref=request.source_state_ref,
                context_refs=_unique((*request.context_refs, *route.context_refs)),
                admission_compatibility_basis_refs=_unique(
                    ("governed:fpo-admission-compatibility", *route.routing_basis_refs)
                ),
                lineage_refs=_unique(
                    (*route.lineage_refs, _candidate_ref(
                        request.compatibility_ref,
                        route.perception_routing_candidate_ref,
                    ))
                ),
                provenance_refs=_unique(
                    (*route.provenance_refs, *request.provenance_refs)
                ),
                trace_ref=request.trace_ref or route.trace_ref,
            )
        )
    return _result(
        request,
        "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED",
        route_refs,
        tuple(candidates),
    )


__all__ = [
    "OWNER",
    "SUPPORTED_OBSERVATION_CLASSES",
    "FORMATION_STATUSES",
    "PerceptionRoutingAdmissionCompatibilityCandidateV1",
    "PerceptionRoutingAdmissionCompatibilityInputV1",
    "PerceptionRoutingAdmissionCompatibilityResultV1",
    "form_fpo_admission_compatibility_candidates",
]
