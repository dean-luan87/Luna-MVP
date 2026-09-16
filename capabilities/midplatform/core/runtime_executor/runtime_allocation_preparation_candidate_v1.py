"""Candidate-only Runtime Allocation and Execution Instance preparation.

Runtime Executor owns execution identity and allocation semantics.  This
module only projects an explicit Provider Binding Candidate into two immutable
preparation candidates.  It never allocates resources, creates an execution
instance, starts a session, or invokes a provider.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateV1,
)


OWNER = "Runtime Executor"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def _valid_ref_collection(value: object, *, allow_empty: bool = True) -> bool:
    return isinstance(value, (list, tuple)) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


@dataclass(frozen=True)
class RuntimeAllocationPreparationCandidateV1:
    runtime_allocation_preparation_candidate_ref: str
    source_provider_binding_candidate_ref: str
    source_provider_binding_preparation_candidate_ref: str
    source_provider_target_candidate_ref: str
    source_admission_compatibility_candidate_ref: str
    source_perception_routing_candidate_ref: str
    source_observation_demand_ref: str
    source_capability_requirement_ref: str
    source_capability_resolution_candidate_ref: str
    provider_binding_candidate_ref: str
    provider_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    source_model_ref: Optional[str]
    runtime_requirement_refs: Tuple[str, ...]
    resource_class_refs: Tuple[str, ...]
    execution_class_refs: Tuple[str, ...]
    observation_class: str
    observation_target_refs: Tuple[str, ...]
    observation_constraint_refs: Tuple[str, ...]
    expected_information_contribution_refs: Tuple[str, ...]
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
    runtime_allocated: bool = False
    resource_allocation: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False


@dataclass(frozen=True)
class RuntimeAllocationPreparationInputV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    provider_binding_candidates: Tuple[ProviderBindingCandidateV1, ...] = field(
        default_factory=tuple
    )
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class RuntimeAllocationPreparationResultV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_provider_binding_candidate_refs: Tuple[str, ...]
    runtime_allocation_preparation_candidate_refs: Tuple[str, ...]
    candidates: Tuple[RuntimeAllocationPreparationCandidateV1, ...]
    excluded_provider_binding_candidate_refs: Tuple[str, ...]
    owner_ref: str = OWNER
    candidate_only: bool = True
    read_only: bool = True
    runtime_allocated: bool = False
    resource_allocation: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    capability_activation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ExecutionInstancePreparationCandidateV1:
    execution_instance_preparation_candidate_ref: str
    source_runtime_allocation_preparation_candidate_ref: str
    source_provider_binding_candidate_ref: str
    provider_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    source_model_ref: Optional[str]
    runtime_requirement_refs: Tuple[str, ...]
    resource_class_refs: Tuple[str, ...]
    execution_class_refs: Tuple[str, ...]
    runtime_envelope_shape_refs: Tuple[str, ...]
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
    execution_instance_created: bool = False
    runtime_allocated: bool = False
    resource_allocation: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False


@dataclass(frozen=True)
class ExecutionInstancePreparationInputV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    runtime_allocation_candidates: Tuple[
        RuntimeAllocationPreparationCandidateV1, ...
    ] = field(default_factory=tuple)
    runtime_envelope_shape_refs: Tuple[str, ...] = field(default_factory=tuple)
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ExecutionInstancePreparationResultV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_runtime_allocation_candidate_refs: Tuple[str, ...]
    execution_instance_preparation_candidate_refs: Tuple[str, ...]
    candidates: Tuple[ExecutionInstancePreparationCandidateV1, ...]
    excluded_runtime_allocation_candidate_refs: Tuple[str, ...]
    owner_ref: str = OWNER
    candidate_only: bool = True
    read_only: bool = True
    execution_instance_created: bool = False
    runtime_allocated: bool = False
    resource_allocation: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)


def _refs(value: object, expected_type: type) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        getattr(item, "provider_binding_candidate_ref", "")
        if expected_type is ProviderBindingCandidateV1
        else getattr(item, "runtime_allocation_preparation_candidate_ref", "")
        for item in value
        if isinstance(item, expected_type)
    )


def _runtime_ref(preparation_ref: str, binding_ref: str) -> str:
    digest = hashlib.sha256(f"{preparation_ref}|{binding_ref}".encode("utf-8")).hexdigest()[:24]
    return f"runtime-allocation-preparation:candidate:{digest}"


def _instance_ref(preparation_ref: str, allocation_ref: str) -> str:
    digest = hashlib.sha256(f"{preparation_ref}|{allocation_ref}".encode("utf-8")).hexdigest()[:24]
    return f"execution-instance-preparation:candidate:{digest}"


def _binding_errors(request: object) -> Tuple[str, ...]:
    if not isinstance(request, RuntimeAllocationPreparationInputV1):
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
    for name in ("context_refs", "provenance_refs"):
        if not _valid_ref_collection(getattr(request, name), allow_empty=True):
            errors.append(f"{name}_must_contain_strings")
    if not isinstance(request.provider_binding_candidates, tuple):
        return tuple((*errors, "provider_binding_candidates_must_be_tuple"))
    refs = _refs(request.provider_binding_candidates, ProviderBindingCandidateV1)
    if len(refs) != len(request.provider_binding_candidates):
        errors.append("provider_binding_candidate_type_invalid")
    if len(refs) != len(set(refs)):
        errors.append("duplicate_provider_binding_candidate_ref")
    for item in request.provider_binding_candidates:
        if not isinstance(item, ProviderBindingCandidateV1):
            continue
        required = (
            item.provider_binding_candidate_ref,
            item.source_provider_binding_preparation_candidate_ref,
            item.source_provider_target_candidate_ref,
            item.source_admission_compatibility_candidate_ref,
            item.source_observation_demand_ref,
            item.source_capability_requirement_ref,
            item.source_capability_resolution_candidate_ref,
            item.provider_candidate_ref,
            item.capability_candidate_ref,
            item.capability_class_ref,
            item.parent_cognitive_problem_ref,
            item.source_state_ref,
            item.trace_ref,
        )
        if not all(required):
            errors.append(f"binding_candidate_incomplete:{item.provider_binding_candidate_ref}")
        if (
            not item.candidate_only
            or not item.read_only
            or item.truth_declared
            or item.world_truth_declared
            or item.provider_bound
            or item.binding_decision_formed
            or item.runtime_allocated
            or item.execution_instance_created
            or item.provider_session_started
            or item.gateway_submission
            or item.provider_invocation
            or item.model_invocation
            or item.capability_activation
            or item.slot_reservation
            or item.resource_allocation
        ):
            errors.append(f"binding_candidate_boundary_invalid:{item.provider_binding_candidate_ref}")
        if item.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"parent_problem_mismatch:{item.provider_binding_candidate_ref}")
        if item.source_state_ref != request.source_state_ref:
            errors.append(f"source_state_mismatch:{item.provider_binding_candidate_ref}")
        for ref in (
            item.provider_binding_candidate_ref,
            item.source_provider_binding_preparation_candidate_ref,
            item.source_provider_target_candidate_ref,
            item.source_admission_compatibility_candidate_ref,
            item.source_observation_demand_ref,
            item.source_capability_resolution_candidate_ref,
        ):
            if ref not in item.lineage_refs:
                errors.append(f"lineage_ref_missing:{item.provider_binding_candidate_ref}:{ref}")
        if not item.runtime_requirement_refs and not item.resource_class_refs and not item.execution_class_refs:
            errors.append(f"runtime_requirement_missing:{item.provider_binding_candidate_ref}")
        for name in (
            "runtime_requirement_refs", "resource_class_refs", "execution_class_refs",
            "observation_target_refs", "observation_constraint_refs",
            "expected_information_contribution_refs", "context_refs", "lineage_refs",
            "provenance_refs",
        ):
            if not _valid_ref_collection(getattr(item, name), allow_empty=True):
                errors.append(f"{name}_invalid:{item.provider_binding_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def _allocation_result(
    request: RuntimeAllocationPreparationInputV1,
    status: str,
    source_refs: Tuple[str, ...],
    candidates: Tuple[RuntimeAllocationPreparationCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> RuntimeAllocationPreparationResultV1:
    formed = {item.source_provider_binding_candidate_ref for item in candidates}
    return RuntimeAllocationPreparationResultV1(
        preparation_ref=getattr(request, "preparation_ref", ""),
        parent_cognitive_problem_ref=getattr(request, "parent_cognitive_problem_ref", ""),
        source_state_ref=getattr(request, "source_state_ref", ""),
        formation_status=status,
        input_provider_binding_candidate_refs=source_refs,
        runtime_allocation_preparation_candidate_refs=tuple(
            item.runtime_allocation_preparation_candidate_ref for item in candidates
        ),
        candidates=candidates,
        excluded_provider_binding_candidate_refs=tuple(
            ref for ref in source_refs if ref not in formed
        ),
        trace_ref=getattr(request, "trace_ref", ""),
        provenance_refs=_unique(
            ("provenance:runtime-allocation-preparation:v1", *getattr(request, "provenance_refs", ()))
        ),
        validation_errors=errors,
    )


def form_runtime_allocation_preparation_candidates(
    request: RuntimeAllocationPreparationInputV1,
) -> RuntimeAllocationPreparationResultV1:
    source_refs = _refs(getattr(request, "provider_binding_candidates", ()), ProviderBindingCandidateV1)
    errors = _binding_errors(request)
    if errors:
        return _allocation_result(request, "INVALID_INPUT", source_refs, (), errors)
    if not source_refs:
        return _allocation_result(request, "NO_RUNTIME_ALLOCATION_PREPARATION_CANDIDATE", (), ())
    candidates = []
    for source in request.provider_binding_candidates:
        candidate_ref = _runtime_ref(request.preparation_ref, source.provider_binding_candidate_ref)
        candidates.append(
            RuntimeAllocationPreparationCandidateV1(
                runtime_allocation_preparation_candidate_ref=candidate_ref,
                source_provider_binding_candidate_ref=source.provider_binding_candidate_ref,
                source_provider_binding_preparation_candidate_ref=source.source_provider_binding_preparation_candidate_ref,
                source_provider_target_candidate_ref=source.source_provider_target_candidate_ref,
                source_admission_compatibility_candidate_ref=source.source_admission_compatibility_candidate_ref,
                source_perception_routing_candidate_ref=source.source_perception_routing_candidate_ref,
                source_observation_demand_ref=source.source_observation_demand_ref,
                source_capability_requirement_ref=source.source_capability_requirement_ref,
                source_capability_resolution_candidate_ref=source.source_capability_resolution_candidate_ref,
                provider_binding_candidate_ref=source.provider_binding_candidate_ref,
                provider_candidate_ref=source.provider_candidate_ref,
                capability_candidate_ref=source.capability_candidate_ref,
                capability_class_ref=source.capability_class_ref,
                source_model_ref=source.source_model_ref,
                runtime_requirement_refs=source.runtime_requirement_refs,
                resource_class_refs=source.resource_class_refs,
                execution_class_refs=source.execution_class_refs,
                observation_class=source.observation_class,
                observation_target_refs=source.observation_target_refs,
                observation_constraint_refs=source.observation_constraint_refs,
                expected_information_contribution_refs=source.expected_information_contribution_refs,
                source_strategy_ref=source.source_strategy_ref,
                source_branch_ref=source.source_branch_ref,
                parent_cognitive_problem_ref=source.parent_cognitive_problem_ref,
                source_state_ref=source.source_state_ref,
                context_refs=_unique((*request.context_refs, *source.context_refs)),
                lineage_refs=_unique((*source.lineage_refs, candidate_ref)),
                provenance_refs=_unique((*source.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref or source.trace_ref,
            )
        )
    return _allocation_result(
        request,
        "RUNTIME_ALLOCATION_PREPARATION_CANDIDATES_FORMED",
        source_refs,
        tuple(candidates),
    )


def _instance_errors(request: object) -> Tuple[str, ...]:
    if not isinstance(request, ExecutionInstancePreparationInputV1):
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
    if not isinstance(request.runtime_allocation_candidates, tuple):
        return tuple((*errors, "runtime_allocation_candidates_must_be_tuple"))
    refs = _refs(request.runtime_allocation_candidates, RuntimeAllocationPreparationCandidateV1)
    if len(refs) != len(request.runtime_allocation_candidates):
        errors.append("runtime_allocation_candidate_type_invalid")
    if len(refs) != len(set(refs)):
        errors.append("duplicate_runtime_allocation_candidate_ref")
    for item in request.runtime_allocation_candidates:
        if not isinstance(item, RuntimeAllocationPreparationCandidateV1):
            continue
        required = (
            item.runtime_allocation_preparation_candidate_ref,
            item.source_provider_binding_candidate_ref,
            item.provider_candidate_ref,
            item.capability_candidate_ref,
            item.capability_class_ref,
            item.parent_cognitive_problem_ref,
            item.source_state_ref,
            item.trace_ref,
        )
        if not all(required) or not item.execution_class_refs:
            errors.append(f"allocation_candidate_incomplete:{item.runtime_allocation_preparation_candidate_ref}")
        if (
            not item.candidate_only
            or not item.read_only
            or item.truth_declared
            or item.world_truth_declared
            or item.runtime_allocated
            or item.resource_allocation
            or item.execution_instance_created
            or item.provider_session_started
            or item.gateway_submission
            or item.provider_invocation
            or item.model_invocation
        ):
            errors.append(f"allocation_candidate_boundary_invalid:{item.runtime_allocation_preparation_candidate_ref}")
        if item.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"parent_problem_mismatch:{item.runtime_allocation_preparation_candidate_ref}")
        if item.source_state_ref != request.source_state_ref:
            errors.append(f"source_state_mismatch:{item.runtime_allocation_preparation_candidate_ref}")
        if item.runtime_allocation_preparation_candidate_ref not in item.lineage_refs:
            errors.append(f"lineage_ref_missing:{item.runtime_allocation_preparation_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def _instance_result(
    request: ExecutionInstancePreparationInputV1,
    status: str,
    source_refs: Tuple[str, ...],
    candidates: Tuple[ExecutionInstancePreparationCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> ExecutionInstancePreparationResultV1:
    formed = {item.source_runtime_allocation_preparation_candidate_ref for item in candidates}
    return ExecutionInstancePreparationResultV1(
        preparation_ref=getattr(request, "preparation_ref", ""),
        parent_cognitive_problem_ref=getattr(request, "parent_cognitive_problem_ref", ""),
        source_state_ref=getattr(request, "source_state_ref", ""),
        formation_status=status,
        input_runtime_allocation_candidate_refs=source_refs,
        execution_instance_preparation_candidate_refs=tuple(
            item.execution_instance_preparation_candidate_ref for item in candidates
        ),
        candidates=candidates,
        excluded_runtime_allocation_candidate_refs=tuple(
            ref for ref in source_refs if ref not in formed
        ),
        trace_ref=getattr(request, "trace_ref", ""),
        provenance_refs=_unique(
            ("provenance:execution-instance-preparation:v1", *getattr(request, "provenance_refs", ()))
        ),
        validation_errors=errors,
    )


def form_execution_instance_preparation_candidates(
    request: ExecutionInstancePreparationInputV1,
) -> ExecutionInstancePreparationResultV1:
    source_refs = _refs(
        getattr(request, "runtime_allocation_candidates", ()),
        RuntimeAllocationPreparationCandidateV1,
    )
    errors = _instance_errors(request)
    if errors:
        return _instance_result(request, "INVALID_INPUT", source_refs, (), errors)
    if not source_refs:
        return _instance_result(request, "NO_EXECUTION_INSTANCE_PREPARATION_CANDIDATE", (), ())
    candidates = []
    for source in request.runtime_allocation_candidates:
        candidate_ref = _instance_ref(
            request.preparation_ref,
            source.runtime_allocation_preparation_candidate_ref,
        )
        candidates.append(
            ExecutionInstancePreparationCandidateV1(
                execution_instance_preparation_candidate_ref=candidate_ref,
                source_runtime_allocation_preparation_candidate_ref=source.runtime_allocation_preparation_candidate_ref,
                source_provider_binding_candidate_ref=source.source_provider_binding_candidate_ref,
                provider_candidate_ref=source.provider_candidate_ref,
                capability_candidate_ref=source.capability_candidate_ref,
                capability_class_ref=source.capability_class_ref,
                source_model_ref=source.source_model_ref,
                runtime_requirement_refs=source.runtime_requirement_refs,
                resource_class_refs=source.resource_class_refs,
                execution_class_refs=source.execution_class_refs,
                runtime_envelope_shape_refs=request.runtime_envelope_shape_refs,
                parent_cognitive_problem_ref=source.parent_cognitive_problem_ref,
                source_state_ref=source.source_state_ref,
                context_refs=_unique((*request.context_refs, *source.context_refs)),
                lineage_refs=_unique((*source.lineage_refs, candidate_ref)),
                provenance_refs=_unique((*source.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref or source.trace_ref,
            )
        )
    return _instance_result(
        request,
        "EXECUTION_INSTANCE_PREPARATION_CANDIDATES_FORMED",
        source_refs,
        tuple(candidates),
    )


__all__ = [
    "OWNER",
    "RuntimeAllocationPreparationCandidateV1",
    "RuntimeAllocationPreparationInputV1",
    "RuntimeAllocationPreparationResultV1",
    "ExecutionInstancePreparationCandidateV1",
    "ExecutionInstancePreparationInputV1",
    "ExecutionInstancePreparationResultV1",
    "form_runtime_allocation_preparation_candidates",
    "form_execution_instance_preparation_candidates",
]
