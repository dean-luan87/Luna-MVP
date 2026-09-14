"""Candidate-only Provider Binding boundary owned by Provider Governance.

This contract deliberately supports a Provider-only binding candidate because
the existing Model↔Provider binding contract requires model declarations while
the upstream Provider Runtime Target may have no model.  No binding decision,
reservation, runtime allocation, or invocation is performed here.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from .provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationCandidateV1,
)


OWNER = "Provider Governance"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class ProviderBindingCandidateV1:
    provider_binding_candidate_ref: str
    source_provider_binding_preparation_candidate_ref: str
    source_provider_target_candidate_ref: str
    source_admission_compatibility_candidate_ref: str
    source_perception_routing_candidate_ref: str
    source_observation_demand_ref: str
    source_capability_requirement_ref: str
    source_capability_resolution_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    provider_candidate_ref: str
    provider_class_ref: str
    source_model_ref: str | None
    binding_scope_refs: Tuple[str, ...]
    runtime_requirement_refs: Tuple[str, ...]
    resource_class_refs: Tuple[str, ...]
    execution_class_refs: Tuple[str, ...]
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
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    owner_ref: str = OWNER
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    provider_bound: bool = False
    binding_decision_formed: bool = False
    model_binding: bool = False
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    slot_reservation: bool = False
    resource_allocation: bool = False


@dataclass(frozen=True)
class ProviderBindingCandidateInputV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    preparation_candidates: Tuple[
        ProviderBindingRuntimePreparationCandidateV1, ...
    ] = field(default_factory=tuple)
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    # These are explicit downstream preparation requirements.  They are
    # carried into a candidate but are never interpreted as an allocation.
    runtime_requirement_refs: Tuple[str, ...] = field(default_factory=tuple)
    resource_class_refs: Tuple[str, ...] = field(default_factory=tuple)
    execution_class_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderBindingCandidateResultV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_preparation_candidate_refs: Tuple[str, ...]
    provider_binding_candidate_refs: Tuple[str, ...]
    candidates: Tuple[ProviderBindingCandidateV1, ...]
    excluded_preparation_candidate_refs: Tuple[str, ...]
    owner_ref: str = OWNER
    candidate_only: bool = True
    read_only: bool = True
    provider_bound: bool = False
    binding_decision_formed: bool = False
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    slot_reservation: bool = False
    resource_allocation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)


def _candidate_ref(preparation_ref: str, source_ref: str) -> str:
    digest = hashlib.sha256(f"{preparation_ref}|{source_ref}".encode("utf-8")).hexdigest()[:24]
    return f"provider-binding:candidate:{digest}"


def _source_refs(value: object) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        item.provider_binding_preparation_candidate_ref
        for item in value
        if isinstance(item, ProviderBindingRuntimePreparationCandidateV1)
    )


def _result(
    request: ProviderBindingCandidateInputV1,
    status: str,
    source_refs: Tuple[str, ...],
    candidates: Tuple[ProviderBindingCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> ProviderBindingCandidateResultV1:
    formed = {item.source_provider_binding_preparation_candidate_ref for item in candidates}
    preparation_ref = getattr(request, "preparation_ref", "")
    return ProviderBindingCandidateResultV1(
        preparation_ref=preparation_ref,
        parent_cognitive_problem_ref=getattr(request, "parent_cognitive_problem_ref", ""),
        source_state_ref=getattr(request, "source_state_ref", ""),
        formation_status=status,
        input_preparation_candidate_refs=source_refs,
        provider_binding_candidate_refs=tuple(item.provider_binding_candidate_ref for item in candidates),
        candidates=candidates,
        excluded_preparation_candidate_refs=tuple(ref for ref in source_refs if ref not in formed),
        trace_ref=getattr(request, "trace_ref", "") or f"trace:{preparation_ref}",
        provenance_refs=_unique(("provenance:provider-binding-candidate:v1", *getattr(request, "provenance_refs", ()))),
        validation_errors=errors,
    )


def _validate(request: object) -> Tuple[str, ...]:
    if not isinstance(request, ProviderBindingCandidateInputV1):
        return ("request_type_invalid",)
    errors = []
    if not request.preparation_ref:
        errors.append("preparation_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("candidate_only_required")
    if not isinstance(request.preparation_candidates, tuple):
        return tuple((*errors, "preparation_candidates_must_be_tuple"))
    refs = _source_refs(request.preparation_candidates)
    if len(refs) != len(set(refs)):
        errors.append("duplicate_preparation_candidate_ref")
    for candidate in request.preparation_candidates:
        if not isinstance(candidate, ProviderBindingRuntimePreparationCandidateV1):
            errors.append("preparation_candidate_type_invalid")
            continue
        required = (
            candidate.provider_binding_preparation_candidate_ref,
            candidate.source_provider_target_candidate_ref,
            candidate.source_admission_compatibility_candidate_ref,
            candidate.source_observation_demand_ref,
            candidate.source_capability_requirement_ref,
            candidate.source_capability_resolution_candidate_ref,
            candidate.capability_candidate_ref,
            candidate.capability_class_ref,
            candidate.provider_candidate_ref,
            candidate.parent_cognitive_problem_ref,
            candidate.source_state_ref,
            candidate.trace_ref,
        )
        if (
            not all(required)
            or not candidate.observation_target_refs
            or not candidate.expected_information_contribution_refs
        ):
            errors.append(f"preparation_candidate_incomplete:{candidate.provider_binding_preparation_candidate_ref}")
        if (
            not candidate.candidate_only
            or not candidate.read_only
            or candidate.truth_declared
            or candidate.world_truth_declared
            or candidate.provider_binding
            or candidate.model_binding
            or candidate.runtime_allocated
            or candidate.execution_instance_created
            or candidate.provider_session_started
            or candidate.gateway_submission
            or candidate.provider_invocation
            or candidate.model_invocation
            or candidate.capability_activation
            or candidate.slot_reservation
            or candidate.resource_scheduling
            or candidate.observation_execution
        ):
            errors.append(f"preparation_candidate_boundary_invalid:{candidate.provider_binding_preparation_candidate_ref}")
        if candidate.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"parent_problem_mismatch:{candidate.provider_binding_preparation_candidate_ref}")
        if candidate.source_state_ref != request.source_state_ref:
            errors.append(f"source_state_mismatch:{candidate.provider_binding_preparation_candidate_ref}")
        for ref in (
            candidate.provider_binding_preparation_candidate_ref,
            candidate.source_provider_target_candidate_ref,
            candidate.source_admission_compatibility_candidate_ref,
            candidate.source_perception_routing_candidate_ref,
            candidate.source_observation_demand_ref,
            candidate.source_capability_resolution_candidate_ref,
        ):
            if ref not in candidate.lineage_refs:
                errors.append(f"lineage_ref_missing:{candidate.provider_binding_preparation_candidate_ref}:{ref}")
    return tuple(dict.fromkeys(errors))


def form_provider_binding_candidates(
    request: ProviderBindingCandidateInputV1,
) -> ProviderBindingCandidateResultV1:
    source_refs = _source_refs(getattr(request, "preparation_candidates", ()))
    errors = _validate(request)
    if errors:
        return _result(request, "INVALID_INPUT", source_refs, (), errors)
    if not source_refs:
        return _result(request, "NO_PROVIDER_BINDING_CANDIDATE", (), ())
    candidates = []
    for source in request.preparation_candidates:
        candidate_ref = _candidate_ref(request.preparation_ref, source.provider_binding_preparation_candidate_ref)
        candidates.append(
            ProviderBindingCandidateV1(
                provider_binding_candidate_ref=candidate_ref,
                source_provider_binding_preparation_candidate_ref=source.provider_binding_preparation_candidate_ref,
                source_provider_target_candidate_ref=source.source_provider_target_candidate_ref,
                source_admission_compatibility_candidate_ref=source.source_admission_compatibility_candidate_ref,
                source_perception_routing_candidate_ref=source.source_perception_routing_candidate_ref,
                source_observation_demand_ref=source.source_observation_demand_ref,
                source_capability_requirement_ref=source.source_capability_requirement_ref,
                source_capability_resolution_candidate_ref=source.source_capability_resolution_candidate_ref,
                capability_candidate_ref=source.capability_candidate_ref,
                capability_class_ref=source.capability_class_ref,
                provider_candidate_ref=source.provider_candidate_ref,
                provider_class_ref=source.provider_class_ref,
                source_model_ref=source.source_model_ref,
                binding_scope_refs=("governed:provider-binding-candidate",),
                runtime_requirement_refs=request.runtime_requirement_refs,
                resource_class_refs=request.resource_class_refs,
                execution_class_refs=request.execution_class_refs,
                observation_class=source.observation_class,
                observation_target_refs=source.observation_target_refs,
                observation_constraint_refs=source.observation_constraint_refs,
                expected_information_contribution_refs=source.expected_information_contribution_refs,
                information_need_refs=source.information_need_refs,
                information_gap_refs=source.information_gap_refs,
                source_strategy_ref=source.source_strategy_ref,
                source_branch_ref=source.source_branch_ref,
                parent_cognitive_problem_ref=source.parent_cognitive_problem_ref,
                source_state_ref=source.source_state_ref,
                context_refs=_unique((*request.context_refs, *source.context_refs)),
                lineage_refs=_unique((*source.lineage_refs, source.provider_binding_preparation_candidate_ref, candidate_ref)),
                provenance_refs=_unique((*source.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref or source.trace_ref,
            )
        )
    return _result(request, "PROVIDER_BINDING_CANDIDATES_FORMED", source_refs, tuple(candidates))


__all__ = [
    "OWNER",
    "ProviderBindingCandidateV1",
    "ProviderBindingCandidateInputV1",
    "ProviderBindingCandidateResultV1",
    "form_provider_binding_candidates",
]
