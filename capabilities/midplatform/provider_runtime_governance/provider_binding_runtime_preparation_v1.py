"""Candidate-only Provider Binding / Runtime Preparation seam.

The existing Model↔Provider binding contract is downstream and requires
model-side declarations.  This module deliberately stops one step earlier:
it carries a governed Provider Runtime Target into a preparation candidate
without binding, allocating, starting, or executing anything.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    ProviderRuntimeTargetPreparationCandidateV1,
)


OWNER = "Provider Governance"
FORMATION_STATUSES = (
    "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED",
    "NO_PROVIDER_BINDING_PREPARATION_CANDIDATE",
    "BINDING_CONTRACT_GAP",
    "INVALID_INPUT",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def _valid_ref_collection(value: object, *, allow_empty: bool = True) -> bool:
    return isinstance(value, (list, tuple)) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


@dataclass(frozen=True)
class ProviderBindingRuntimePreparationCandidateV1:
    """A preparation projection, not a Provider Binding record."""

    provider_binding_preparation_candidate_ref: str
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
    source_model_ref: Optional[str]
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
    binding_preparation_basis_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    owner_ref: str = OWNER
    preparation_status: str = "PREPARATION_CANDIDATE"
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    provider_bound: bool = False
    provider_binding: bool = False
    model_binding: bool = False
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    runtime_observation_created: bool = False
    observation_execution: bool = False


@dataclass(frozen=True)
class ProviderBindingRuntimePreparationInputV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    provider_target_candidates: Tuple[
        ProviderRuntimeTargetPreparationCandidateV1, ...
    ] = field(default_factory=tuple)
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderBindingRuntimePreparationResultV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_provider_target_candidate_refs: Tuple[str, ...]
    provider_binding_preparation_candidate_refs: Tuple[str, ...]
    candidates: Tuple[ProviderBindingRuntimePreparationCandidateV1, ...]
    excluded_provider_target_candidate_refs: Tuple[str, ...]
    owner_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    provider_bound: bool = False
    provider_binding: bool = False
    model_binding: bool = False
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    runtime_observation_created: bool = False
    observation_execution: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _candidate_ref(preparation_ref: str, target_ref: str) -> str:
    digest = hashlib.sha256(f"{preparation_ref}|{target_ref}".encode("utf-8")).hexdigest()[:24]
    return f"provider-binding-preparation:candidate:{digest}"


def _target_refs(value: object) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        item.provider_target_candidate_ref
        for item in value
        if isinstance(item, ProviderRuntimeTargetPreparationCandidateV1)
    )


def _result(
    request: ProviderBindingRuntimePreparationInputV1,
    status: str,
    target_refs: Tuple[str, ...],
    candidates: Tuple[ProviderBindingRuntimePreparationCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> ProviderBindingRuntimePreparationResultV1:
    candidate_sources = {item.source_provider_target_candidate_ref for item in candidates}
    return ProviderBindingRuntimePreparationResultV1(
        preparation_ref=getattr(request, "preparation_ref", ""),
        parent_cognitive_problem_ref=getattr(request, "parent_cognitive_problem_ref", ""),
        source_state_ref=getattr(request, "source_state_ref", ""),
        formation_status=status,
        input_provider_target_candidate_refs=target_refs,
        provider_binding_preparation_candidate_refs=tuple(
            item.provider_binding_preparation_candidate_ref for item in candidates
        ),
        candidates=candidates,
        excluded_provider_target_candidate_refs=tuple(
            ref for ref in target_refs if ref not in candidate_sources
        ),
        owner_ref=OWNER,
        context_refs=getattr(request, "context_refs", ()),
        provenance_refs=_unique(
            (
                "provenance:provider-binding-runtime-preparation:v1",
                *getattr(request, "provenance_refs", ()),
            )
        ),
        trace_ref=getattr(request, "trace_ref", "") or f"trace:{getattr(request, 'preparation_ref', '')}",
        validation_errors=errors,
    )


def _validate(request: ProviderBindingRuntimePreparationInputV1) -> Tuple[str, ...]:
    errors = []
    if not isinstance(request, ProviderBindingRuntimePreparationInputV1):
        return ("request_type_invalid",)
    if not request.preparation_ref:
        errors.append("preparation_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("preparation_not_candidate_only")
    for name in ("context_refs", "provenance_refs"):
        if not _valid_ref_collection(getattr(request, name), allow_empty=True):
            errors.append(f"{name}_must_contain_strings")
    if not isinstance(request.provider_target_candidates, tuple):
        errors.append("provider_target_candidates_must_be_tuple")
        return tuple(dict.fromkeys(errors))

    target_refs = _target_refs(request.provider_target_candidates)
    if len(set(target_refs)) != len(target_refs):
        errors.append("duplicate_provider_target_candidate_ref")
    for target in request.provider_target_candidates:
        if not isinstance(target, ProviderRuntimeTargetPreparationCandidateV1):
            errors.append("invalid_provider_target_candidate_type")
            continue
        required = (
            target.provider_target_candidate_ref,
            target.source_admission_compatibility_candidate_ref,
            target.source_perception_routing_candidate_ref,
            target.source_observation_demand_ref,
            target.source_capability_requirement_ref,
            target.source_capability_resolution_candidate_ref,
            target.capability_candidate_ref,
            target.capability_class_ref,
            target.provider_candidate_ref,
            target.provider_class_ref,
            target.observation_class,
            target.parent_cognitive_problem_ref,
            target.source_state_ref,
            target.trace_ref,
        )
        if not all(required) or not target.observation_target_refs or not target.expected_information_contribution_refs:
            errors.append(f"provider_target_requirement_incomplete:{target.provider_target_candidate_ref}")
        if (
            not target.candidate_only
            or not target.read_only
            or target.truth_declared
            or target.world_truth_declared
            or target.provider_binding
            or target.model_binding
            or target.provider_invocation
            or target.model_invocation
            or target.execution_instance_created
            or target.provider_session_started
            or target.runtime_admission_requested
            or target.runtime_admission_executed
            or target.gateway_submission
            or target.capability_activation
            or target.capability_reservation
            or target.slot_reservation
            or target.resource_scheduling
            or target.observation_execution
        ):
            errors.append(f"invalid_provider_target_flags:{target.provider_target_candidate_ref}")
        if target.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"parent_problem_mismatch:{target.provider_target_candidate_ref}")
        if target.source_state_ref != request.source_state_ref:
            errors.append(f"source_state_mismatch:{target.provider_target_candidate_ref}")
        for ref in (
            target.source_admission_compatibility_candidate_ref,
            target.source_observation_demand_ref,
            target.source_capability_resolution_candidate_ref,
            target.provider_target_candidate_ref,
        ):
            if ref not in target.lineage_refs:
                errors.append(f"lineage_ref_missing:{target.provider_target_candidate_ref}:{ref}")
        for name in (
            "observation_target_refs", "observation_constraint_refs",
            "expected_information_contribution_refs", "information_need_refs",
            "information_gap_refs",
            "context_refs", "lineage_refs", "provenance_refs",
        ):
            if not _valid_ref_collection(getattr(target, name), allow_empty=True):
                errors.append(f"{name}_invalid:{target.provider_target_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def form_provider_binding_runtime_preparation_candidates(
    request: ProviderBindingRuntimePreparationInputV1,
) -> ProviderBindingRuntimePreparationResultV1:
    """Project valid Provider Targets without producing an actual binding."""

    target_refs = _target_refs(getattr(request, "provider_target_candidates", ()))
    errors = _validate(request)
    if errors:
        return _result(request, "INVALID_INPUT", target_refs, (), errors)
    if not target_refs:
        return _result(request, "NO_PROVIDER_BINDING_PREPARATION_CANDIDATE", (), ())

    candidates = []
    for target in request.provider_target_candidates:
        candidate_ref = _candidate_ref(request.preparation_ref, target.provider_target_candidate_ref)
        candidates.append(
            ProviderBindingRuntimePreparationCandidateV1(
                provider_binding_preparation_candidate_ref=candidate_ref,
                source_provider_target_candidate_ref=target.provider_target_candidate_ref,
                source_admission_compatibility_candidate_ref=target.source_admission_compatibility_candidate_ref,
                source_perception_routing_candidate_ref=target.source_perception_routing_candidate_ref,
                source_observation_demand_ref=target.source_observation_demand_ref,
                source_capability_requirement_ref=target.source_capability_requirement_ref,
                source_capability_resolution_candidate_ref=target.source_capability_resolution_candidate_ref,
                capability_candidate_ref=target.capability_candidate_ref,
                capability_class_ref=target.capability_class_ref,
                provider_candidate_ref=target.provider_candidate_ref,
                provider_class_ref=target.provider_class_ref,
                source_model_ref=target.source_model_ref,
                observation_class=target.observation_class,
                observation_target_refs=target.observation_target_refs,
                observation_constraint_refs=target.observation_constraint_refs,
                expected_information_contribution_refs=target.expected_information_contribution_refs,
                information_need_refs=target.information_need_refs,
                information_gap_refs=target.information_gap_refs,
                source_strategy_ref=target.source_strategy_ref,
                source_branch_ref=target.source_branch_ref,
                parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
                source_state_ref=target.source_state_ref,
                binding_preparation_basis_refs=("governed:provider-target-to-binding-preparation",),
                context_refs=_unique((*request.context_refs, *target.context_refs)),
                lineage_refs=_unique((*target.lineage_refs, target.provider_target_candidate_ref, candidate_ref)),
                provenance_refs=_unique((*target.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref or target.trace_ref,
            )
        )
    return _result(
        request,
        "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED",
        target_refs,
        tuple(candidates),
    )


__all__ = [
    "OWNER",
    "FORMATION_STATUSES",
    "ProviderBindingRuntimePreparationCandidateV1",
    "ProviderBindingRuntimePreparationInputV1",
    "ProviderBindingRuntimePreparationResultV1",
    "form_provider_binding_runtime_preparation_candidates",
]
