"""Authoritative controlled allocation and execution-instance records.

This is the Runtime Executor mechanical boundary.  It consumes a valid
Provider Binding Decision, Runtime Execution Grant, and the existing
preparation candidates.  Resource and runtime identities are synthetic and
controlled; no machine resource, process, session, provider, or Gateway is
started by these functions.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, replace
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantDecisionV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_decision_v1 import (
    ProviderBindingDecisionV1,
)
from .runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationCandidateV1,
    RuntimeAllocationPreparationCandidateV1,
)


OWNER = "Runtime Executor"
RESOURCE_OWNER = "Resource Governance"
ALLOCATION_STATUSES = ("ALLOCATED", "DENIED", "RELEASED", "FAILED")
INSTANCE_STATES = ("CREATED", "READY", "STOPPED", "FAILED", "REVOKED")


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def _valid_grant(grant: object, binding_ref: str) -> bool:
    return (
        isinstance(grant, RuntimeExecutionGrantDecisionV1)
        and grant.source_provider_binding_candidate_ref == binding_ref
        and grant.decision == "GRANTED"
        and grant.validity_status == "FRESH"
        and grant.authoritative
        and not grant.candidate_only
        and not grant.revocation_ref
    )


@dataclass(frozen=True)
class RuntimeAllocationRecordV1:
    allocation_ref: str
    source_runtime_allocation_preparation_ref: str
    source_provider_binding_decision_ref: str
    source_provider_binding_candidate_ref: str
    source_runtime_grant_ref: str
    runtime_owner_ref: str
    resource_owner_ref: str
    execution_class_ref: str
    resource_class_refs: Tuple[str, ...]
    resource_identity_refs: Tuple[str, ...]
    runtime_ref: str
    allocation_status: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    context_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    denial_reason: Optional[str] = None
    failure_owner_ref: Optional[str] = None
    authoritative: bool = True
    read_only: bool = True
    synthetic: bool = True
    controlled: bool = True
    no_real_resource_effect: bool = True
    provider_bound: bool = True
    runtime_allocated: bool = False
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


@dataclass(frozen=True)
class RuntimeAllocationInputV1:
    allocation_request_ref: str
    binding_decisions: Tuple[ProviderBindingDecisionV1, ...] = field(default_factory=tuple)
    allocation_preparations: Tuple[RuntimeAllocationPreparationCandidateV1, ...] = field(default_factory=tuple)
    runtime_grants: Tuple[RuntimeExecutionGrantDecisionV1, ...] = field(default_factory=tuple)
    resource_feasibility_status: str = "SATISFIABLE"
    allocation_outcome: str = "AUTO"
    resource_identity_refs: Tuple[str, ...] = field(default_factory=tuple)
    runtime_ref: str = ""
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class RuntimeAllocationResultV1:
    allocation_request_ref: str
    formation_status: str
    allocation_refs: Tuple[str, ...]
    records: Tuple[RuntimeAllocationRecordV1, ...]
    excluded_binding_decision_refs: Tuple[str, ...]
    grant_recheck_passed: bool
    owner_ref: str = OWNER
    authoritative: bool = True
    read_only: bool = True
    trace_ref: str = ""
    validation_errors: Tuple[str, ...] = ()


def _allocation_ref(request_ref: str, binding_ref: str) -> str:
    digest = hashlib.sha256(f"{request_ref}|{binding_ref}".encode("utf-8")).hexdigest()[:24]
    return f"runtime-allocation:{digest}"


def _validate_allocation(request: object) -> Tuple[str, ...]:
    if not isinstance(request, RuntimeAllocationInputV1):
        return ("request_type_invalid",)
    errors = []
    for name, value in (
        ("binding_decisions", request.binding_decisions),
        ("allocation_preparations", request.allocation_preparations),
        ("runtime_grants", request.runtime_grants),
        ("resource_identity_refs", request.resource_identity_refs),
        ("provenance_refs", request.provenance_refs),
    ):
        if not isinstance(value, tuple):
            errors.append(f"{name}_must_be_tuple")
    if not request.allocation_request_ref or not request.runtime_ref or not request.trace_ref:
        errors.append("allocation_request_incomplete")
    if not request.candidate_only:
        errors.append("input_candidate_only_required")
    if request.resource_feasibility_status not in {"SATISFIABLE", "UNAVAILABLE"}:
        errors.append("resource_feasibility_status_invalid")
    if request.allocation_outcome not in {"AUTO", "ALLOCATED", "DENIED", "FAILED"}:
        errors.append("allocation_outcome_invalid")
    if not isinstance(request.binding_decisions, tuple) or not isinstance(request.allocation_preparations, tuple) or not isinstance(request.runtime_grants, tuple):
        return tuple(dict.fromkeys(errors))
    decision_refs = [item.binding_ref for item in request.binding_decisions if isinstance(item, ProviderBindingDecisionV1)]
    if len(decision_refs) != len(request.binding_decisions):
        errors.append("binding_decision_type_invalid")
    if len(decision_refs) != len(set(decision_refs)):
        errors.append("duplicate_binding_decision_ref")
    prep_by_binding = {
        item.source_provider_binding_candidate_ref: item
        for item in request.allocation_preparations
        if isinstance(item, RuntimeAllocationPreparationCandidateV1)
    }
    grants_by_binding = {
        item.source_provider_binding_candidate_ref: item
        for item in request.runtime_grants
        if isinstance(item, RuntimeExecutionGrantDecisionV1)
    }
    if len(prep_by_binding) != len(request.allocation_preparations):
        errors.append("allocation_preparation_type_invalid_or_duplicate")
    if len(grants_by_binding) != len(request.runtime_grants):
        errors.append("runtime_grant_type_invalid_or_duplicate")
    if not request.resource_identity_refs:
        errors.append("resource_identity_refs_missing")
    for decision in request.binding_decisions:
        if not isinstance(decision, ProviderBindingDecisionV1):
            continue
        prep = prep_by_binding.get(decision.source_binding_candidate_ref)
        grant = grants_by_binding.get(decision.source_binding_candidate_ref)
        if prep is None:
            errors.append(f"allocation_preparation_missing:{decision.binding_ref}")
        if grant is None:
            errors.append(f"runtime_grant_missing:{decision.binding_ref}")
        if decision.decision != "BOUND":
            errors.append(f"binding_not_bound:{decision.binding_ref}")
        if prep is not None and (
            prep.provider_binding_candidate_ref != decision.source_binding_candidate_ref
            or prep.parent_cognitive_problem_ref != decision.parent_cognitive_problem_ref
            or prep.source_state_ref != decision.source_state_ref
        ):
            errors.append(f"binding_preparation_lineage_mismatch:{decision.binding_ref}")
        if grant is not None and not _valid_grant(grant, decision.source_binding_candidate_ref):
            errors.append(f"runtime_grant_not_valid:{decision.binding_ref}")
    return tuple(dict.fromkeys(errors))


def form_runtime_allocation_records(request: object) -> RuntimeAllocationResultV1:
    errors = _validate_allocation(request)
    if not isinstance(request, RuntimeAllocationInputV1):
        return RuntimeAllocationResultV1("", "INVALID_INPUT", (), (), (), False, validation_errors=errors)
    decision_refs = tuple(item.binding_ref for item in request.binding_decisions if isinstance(item, ProviderBindingDecisionV1))
    if errors:
        return RuntimeAllocationResultV1(request.allocation_request_ref, "INVALID_INPUT", (), (), decision_refs, False, trace_ref=request.trace_ref, validation_errors=errors)
    if not request.binding_decisions:
        return RuntimeAllocationResultV1(request.allocation_request_ref, "NO_RUNTIME_ALLOCATION_RECORD", (), (), (), True, trace_ref=request.trace_ref)
    prep_by_binding = {item.source_provider_binding_candidate_ref: item for item in request.allocation_preparations}
    grant_by_binding = {item.source_provider_binding_candidate_ref: item for item in request.runtime_grants}
    records = []
    for decision in request.binding_decisions:
        prep = prep_by_binding[decision.source_binding_candidate_ref]
        grant = grant_by_binding[decision.source_binding_candidate_ref]
        status = request.allocation_outcome
        if status == "AUTO":
            status = "ALLOCATED" if request.resource_feasibility_status == "SATISFIABLE" else "DENIED"
        reason = None if status == "ALLOCATED" else (
            "resource_unavailable" if request.resource_feasibility_status == "UNAVAILABLE"
            else "allocation_denied" if status == "DENIED" else "allocation_failed"
        )
        records.append(
            RuntimeAllocationRecordV1(
                allocation_ref=_allocation_ref(request.allocation_request_ref, decision.binding_ref),
                source_runtime_allocation_preparation_ref=prep.runtime_allocation_preparation_candidate_ref,
                source_provider_binding_decision_ref=decision.binding_ref,
                source_provider_binding_candidate_ref=decision.source_binding_candidate_ref,
                source_runtime_grant_ref=grant.grant_ref,
                runtime_owner_ref=OWNER,
                resource_owner_ref=RESOURCE_OWNER,
                execution_class_ref=prep.execution_class_refs[0],
                resource_class_refs=prep.resource_class_refs,
                resource_identity_refs=request.resource_identity_refs,
                runtime_ref=request.runtime_ref,
                allocation_status=status,
                parent_cognitive_problem_ref=decision.parent_cognitive_problem_ref,
                source_state_ref=decision.source_state_ref,
                context_refs=decision.context_refs,
                lineage_refs=_unique((*decision.lineage_refs, prep.runtime_allocation_preparation_candidate_ref)),
                provenance_refs=_unique((*decision.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref,
                denial_reason=reason,
                failure_owner_ref=RESOURCE_OWNER if reason else None,
                runtime_allocated=status == "ALLOCATED",
            )
        )
    return RuntimeAllocationResultV1(
        request.allocation_request_ref,
        "RUNTIME_ALLOCATION_RECORDS_FORMED",
        tuple(item.allocation_ref for item in records),
        tuple(records),
        (),
        True,
        trace_ref=request.trace_ref,
    )


def release_runtime_allocation(record: RuntimeAllocationRecordV1, reason: str = "controlled_release") -> RuntimeAllocationRecordV1:
    """Record an authoritative controlled release; no real resource is touched."""
    if not isinstance(record, RuntimeAllocationRecordV1) or record.allocation_status != "ALLOCATED":
        return record
    return replace(record, allocation_status="RELEASED", runtime_allocated=False, denial_reason=reason)


@dataclass(frozen=True)
class ExecutionInstanceV1:
    execution_instance_ref: str
    source_allocation_ref: str
    source_runtime_grant_ref: str
    source_provider_binding_ref: str
    provider_ref: str
    capability_ref: str
    source_model_ref: Optional[str]
    execution_class_ref: str
    runtime_ref: str
    state: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    authoritative: bool = True
    read_only: bool = True
    synthetic: bool = True
    controlled: bool = True
    execution_started: bool = False
    provider_session_started: bool = False
    provider_invoked: bool = False
    model_invoked: bool = False
    gateway_submission: bool = False
    observation_produced: bool = False
    evidence_produced: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ExecutionInstanceInputV1:
    instance_request_ref: str
    allocation_records: Tuple[RuntimeAllocationRecordV1, ...] = field(default_factory=tuple)
    execution_preparations: Tuple[ExecutionInstancePreparationCandidateV1, ...] = field(default_factory=tuple)
    binding_decisions: Tuple[ProviderBindingDecisionV1, ...] = field(default_factory=tuple)
    runtime_grants: Tuple[RuntimeExecutionGrantDecisionV1, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ExecutionInstanceResultV1:
    instance_request_ref: str
    formation_status: str
    execution_instance_refs: Tuple[str, ...]
    instances: Tuple[ExecutionInstanceV1, ...]
    excluded_allocation_refs: Tuple[str, ...]
    grant_recheck_passed: bool
    owner_ref: str = OWNER
    authoritative: bool = True
    read_only: bool = True
    trace_ref: str = ""
    validation_errors: Tuple[str, ...] = ()


def _instance_ref(request_ref: str, allocation_ref: str, binding_ref: str) -> str:
    digest = hashlib.sha256(f"{request_ref}|{allocation_ref}|{binding_ref}".encode("utf-8")).hexdigest()[:24]
    return f"execution-instance:{digest}"


def _validate_instance(request: object) -> Tuple[str, ...]:
    if not isinstance(request, ExecutionInstanceInputV1):
        return ("request_type_invalid",)
    errors = []
    for name, value in (
        ("allocation_records", request.allocation_records),
        ("execution_preparations", request.execution_preparations),
        ("binding_decisions", request.binding_decisions),
        ("runtime_grants", request.runtime_grants),
        ("provenance_refs", request.provenance_refs),
    ):
        if not isinstance(value, tuple):
            errors.append(f"{name}_must_be_tuple")
    if not request.instance_request_ref or not request.trace_ref:
        errors.append("instance_request_incomplete")
    if not request.candidate_only:
        errors.append("input_candidate_only_required")
    if not all(isinstance(value, tuple) for value in (request.allocation_records, request.execution_preparations, request.binding_decisions, request.runtime_grants)):
        return tuple(dict.fromkeys(errors))
    allocation_refs = [item.allocation_ref for item in request.allocation_records if isinstance(item, RuntimeAllocationRecordV1)]
    if len(allocation_refs) != len(request.allocation_records):
        errors.append("allocation_record_type_invalid")
    if len(allocation_refs) != len(set(allocation_refs)):
        errors.append("duplicate_allocation_ref")
    allocations = {item.allocation_ref: item for item in request.allocation_records}
    preps = {item.source_runtime_allocation_preparation_candidate_ref: item for item in request.execution_preparations}
    bindings = {item.binding_ref: item for item in request.binding_decisions}
    grants = {item.source_provider_binding_candidate_ref: item for item in request.runtime_grants}
    for prep in request.execution_preparations:
        if not isinstance(prep, ExecutionInstancePreparationCandidateV1):
            errors.append("execution_preparation_type_invalid")
            continue
        allocation = next((item for item in request.allocation_records if item.source_runtime_allocation_preparation_ref == prep.source_runtime_allocation_preparation_candidate_ref), None)
        binding = next((item for item in request.binding_decisions if item.source_binding_candidate_ref == prep.source_provider_binding_candidate_ref), None)
        grant = next((item for item in request.runtime_grants if item.source_provider_binding_candidate_ref == prep.source_provider_binding_candidate_ref), None)
        if allocation is None:
            errors.append(f"allocation_missing:{prep.execution_instance_preparation_candidate_ref}")
        if binding is None:
            errors.append(f"binding_missing:{prep.execution_instance_preparation_candidate_ref}")
        if grant is None or not _valid_grant(grant, prep.source_provider_binding_candidate_ref):
            errors.append(f"runtime_grant_not_valid:{prep.execution_instance_preparation_candidate_ref}")
        if allocation is not None and allocation.allocation_status != "ALLOCATED":
            errors.append(f"allocation_not_active:{prep.execution_instance_preparation_candidate_ref}")
        if binding is not None and binding.decision != "BOUND":
            errors.append(f"binding_not_bound:{prep.execution_instance_preparation_candidate_ref}")
        if binding is not None and allocation is not None and allocation.source_provider_binding_decision_ref != binding.binding_ref:
            errors.append(f"allocation_binding_mismatch:{prep.execution_instance_preparation_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def create_execution_instances(request: object) -> ExecutionInstanceResultV1:
    errors = _validate_instance(request)
    if not isinstance(request, ExecutionInstanceInputV1):
        return ExecutionInstanceResultV1("", "INVALID_INPUT", (), (), (), False, validation_errors=errors)
    allocation_refs = tuple(item.allocation_ref for item in request.allocation_records if isinstance(item, RuntimeAllocationRecordV1))
    if errors:
        return ExecutionInstanceResultV1(request.instance_request_ref, "INVALID_INPUT", (), (), allocation_refs, False, trace_ref=request.trace_ref, validation_errors=errors)
    if not request.execution_preparations:
        return ExecutionInstanceResultV1(request.instance_request_ref, "NO_EXECUTION_INSTANCE", (), (), (), True, trace_ref=request.trace_ref)
    instances = []
    for prep in request.execution_preparations:
        allocation = next(item for item in request.allocation_records if item.source_runtime_allocation_preparation_ref == prep.source_runtime_allocation_preparation_candidate_ref)
        binding = next(item for item in request.binding_decisions if item.source_binding_candidate_ref == prep.source_provider_binding_candidate_ref)
        grant = next(item for item in request.runtime_grants if item.source_provider_binding_candidate_ref == prep.source_provider_binding_candidate_ref)
        instances.append(
            ExecutionInstanceV1(
                execution_instance_ref=_instance_ref(request.instance_request_ref, allocation.allocation_ref, binding.binding_ref),
                source_allocation_ref=allocation.allocation_ref,
                source_runtime_grant_ref=grant.grant_ref,
                source_provider_binding_ref=binding.binding_ref,
                provider_ref=binding.provider_ref,
                capability_ref=binding.capability_ref,
                source_model_ref=binding.source_model_ref,
                execution_class_ref=allocation.execution_class_ref,
                runtime_ref=allocation.runtime_ref,
                state="CREATED",
                parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
                source_state_ref=binding.source_state_ref,
                lineage_refs=_unique((*binding.lineage_refs, allocation.allocation_ref, prep.execution_instance_preparation_candidate_ref)),
                provenance_refs=_unique((*binding.provenance_refs, *allocation.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref,
            )
        )
    return ExecutionInstanceResultV1(
        request.instance_request_ref,
        "EXECUTION_INSTANCES_CREATED",
        tuple(item.execution_instance_ref for item in instances),
        tuple(instances),
        (),
        True,
        trace_ref=request.trace_ref,
    )


__all__ = [
    "OWNER", "RESOURCE_OWNER", "ALLOCATION_STATUSES", "INSTANCE_STATES",
    "RuntimeAllocationRecordV1", "RuntimeAllocationInputV1", "RuntimeAllocationResultV1",
    "form_runtime_allocation_records", "release_runtime_allocation",
    "ExecutionInstanceV1", "ExecutionInstanceInputV1", "ExecutionInstanceResultV1",
    "create_execution_instances",
]
