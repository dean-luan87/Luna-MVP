"""Controlled Provider Runtime Session and Invocation lifecycle records.

This module is the Provider Runtime Governance boundary for a synthetic,
controlled lifecycle.  It consumes already-authoritative binding, grant,
allocation, and execution-instance records.  It never calls a provider,
model, network, process, thread, camera, or Gateway.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, replace
from typing import Optional, Tuple

from capabilities.midplatform.core.runtime_executor.runtime_allocation_execution_instance_v1 import (
    ExecutionInstanceV1,
    RuntimeAllocationRecordV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantDecisionV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_decision_v1 import (
    ProviderBindingDecisionV1,
)


OWNER = "Provider Runtime Governance"
SESSION_STATUSES = (
    "CREATED", "READY", "STARTED", "COMPLETED", "STOPPED", "FAILED",
    "REVOKED", "TIMED_OUT",
)
INVOCATION_STATUSES = (
    "STARTED", "COMPLETED", "FAILED", "STOPPED", "REVOKED", "TIMED_OUT",
    "DUPLICATE_START_BLOCKED",
)
INVOCATION_OUTCOMES = ("COMPLETED", "FAILED", "STOPPED", "REVOKED", "TIMED_OUT")


def _unique(values: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class ProviderRuntimeSessionInputV1:
    session_request_ref: str
    execution_instance: ExecutionInstanceV1
    provider_binding: ProviderBindingDecisionV1
    runtime_grant: RuntimeExecutionGrantDecisionV1
    runtime_allocation: RuntimeAllocationRecordV1
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    source_bounded_provider_session_ref: Optional[str] = None
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeSessionV1:
    session_ref: str
    execution_instance_ref: str
    provider_binding_ref: str
    runtime_grant_ref: str
    runtime_allocation_ref: str
    provider_ref: str
    capability_ref: str
    source_model_ref: Optional[str]
    session_owner_ref: str
    status: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    authoritative: bool = True
    read_only: bool = True
    execution_started: bool = False
    provider_invoked: bool = False
    synthetic: bool = True
    controlled: bool = True
    no_real_provider_effect: bool = True
    no_real_model_effect: bool = True


@dataclass(frozen=True)
class ProviderRuntimeSessionResultV1:
    session_request_ref: str
    formation_status: str
    session: Optional[ProviderRuntimeSessionV1]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    source_execution_instance_ref: str = ""
    trace_ref: str = ""


@dataclass(frozen=True)
class ProviderInvocationInputV1:
    invocation_request_ref: str
    session: ProviderRuntimeSessionV1
    execution_instance: ExecutionInstanceV1
    provider_binding: ProviderBindingDecisionV1
    runtime_grant: RuntimeExecutionGrantDecisionV1
    runtime_allocation: RuntimeAllocationRecordV1
    outcome: str = "COMPLETED"
    duplicate_start: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProviderInvocationRecordV1:
    invocation_ref: str
    session_ref: str
    execution_instance_ref: str
    provider_binding_ref: str
    runtime_grant_ref: str
    runtime_allocation_ref: str
    provider_ref: str
    capability_ref: str
    source_model_ref: Optional[str]
    status: str
    result_ref: str
    payload_ref: str
    failure_owner_ref: Optional[str]
    parent_cognitive_problem_ref: str
    source_state_ref: str
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    authoritative: bool = True
    read_only: bool = True
    controlled_invocation_started: bool = True
    controlled_invocation_completed: bool = False
    real_provider_invoked: bool = False
    real_model_invoked: bool = False
    network_called: bool = False
    subprocess_started: bool = False
    thread_started: bool = False
    socket_used: bool = False
    runtime_observation_created: bool = False
    gateway_submission: bool = False
    evidence_created: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ProviderInvocationResultV1:
    invocation_request_ref: str
    formation_status: str
    session: Optional[ProviderRuntimeSessionV1]
    invocation: Optional[ProviderInvocationRecordV1]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""


def _session_ref(request_ref: str, execution_instance_ref: str) -> str:
    digest = hashlib.sha256(f"{request_ref}|{execution_instance_ref}".encode("utf-8")).hexdigest()[:24]
    return f"provider-runtime-session:{digest}"


def _invocation_ref(request_ref: str, session_ref: str) -> str:
    digest = hashlib.sha256(f"{request_ref}|{session_ref}".encode("utf-8")).hexdigest()[:24]
    return f"provider-invocation:{digest}"


def _valid_source_lineage(
    execution: ExecutionInstanceV1,
    binding: ProviderBindingDecisionV1,
    grant: RuntimeExecutionGrantDecisionV1,
    allocation: RuntimeAllocationRecordV1,
) -> Tuple[str, ...]:
    errors = []
    if execution.source_provider_binding_ref != binding.binding_ref:
        errors.append("execution_binding_mismatch")
    if execution.source_runtime_grant_ref != grant.grant_ref:
        errors.append("execution_grant_mismatch")
    if execution.source_allocation_ref != allocation.allocation_ref:
        errors.append("execution_allocation_mismatch")
    if binding.source_runtime_grant_ref != grant.grant_ref:
        errors.append("binding_grant_mismatch")
    if allocation.source_provider_binding_decision_ref != binding.binding_ref:
        errors.append("allocation_binding_mismatch")
    if allocation.source_runtime_grant_ref != grant.grant_ref:
        errors.append("allocation_grant_mismatch")
    if grant.source_provider_binding_candidate_ref != binding.source_binding_candidate_ref:
        errors.append("grant_binding_candidate_mismatch")
    if execution.provider_ref != binding.provider_ref:
        errors.append("execution_provider_mismatch")
    if execution.capability_ref != binding.capability_ref:
        errors.append("execution_capability_mismatch")
    if execution.source_model_ref != binding.source_model_ref:
        errors.append("execution_model_mismatch")
    for left, right, label in (
        (execution.parent_cognitive_problem_ref, binding.parent_cognitive_problem_ref, "execution_binding_problem"),
        (execution.source_state_ref, binding.source_state_ref, "execution_binding_state"),
        (grant.parent_cognitive_problem_ref, binding.parent_cognitive_problem_ref, "grant_binding_problem"),
        (grant.source_state_ref, binding.source_state_ref, "grant_binding_state"),
        (allocation.parent_cognitive_problem_ref, binding.parent_cognitive_problem_ref, "allocation_binding_problem"),
        (allocation.source_state_ref, binding.source_state_ref, "allocation_binding_state"),
    ):
        if left != right:
            errors.append(label)
    return tuple(dict.fromkeys(errors))


def _valid_session_sources(request: ProviderRuntimeSessionInputV1) -> Tuple[str, ...]:
    errors = []
    if not isinstance(request, ProviderRuntimeSessionInputV1):
        return ("request_type_invalid",)
    if not request.session_request_ref or not request.trace_ref:
        errors.append("session_request_ref_or_trace_missing")
    if not isinstance(request.execution_instance, ExecutionInstanceV1):
        errors.append("execution_instance_type_invalid")
    if not isinstance(request.provider_binding, ProviderBindingDecisionV1):
        errors.append("provider_binding_type_invalid")
    if not isinstance(request.runtime_grant, RuntimeExecutionGrantDecisionV1):
        errors.append("runtime_grant_type_invalid")
    if not isinstance(request.runtime_allocation, RuntimeAllocationRecordV1):
        errors.append("runtime_allocation_type_invalid")
    if errors:
        return tuple(errors)
    execution = request.execution_instance
    binding = request.provider_binding
    grant = request.runtime_grant
    allocation = request.runtime_allocation
    errors.extend(_valid_source_lineage(execution, binding, grant, allocation))
    if binding.decision != "BOUND" or not binding.provider_bound or not binding.authoritative or binding.validity_status != "FRESH":
        errors.append("provider_binding_not_valid")
    if (
        grant.decision != "GRANTED"
        or not grant.authoritative
        or grant.candidate_only
        or grant.validity_status != "FRESH"
        or not grant.execution_authorized
        or grant.revocation_ref
        or query_active_authorization_for_grant(grant) is None
    ):
        errors.append("runtime_grant_not_valid")
    if allocation.allocation_status != "ALLOCATED" or not allocation.authoritative or not allocation.runtime_allocated:
        errors.append("runtime_allocation_not_active")
    if (
        execution.state not in {"CREATED", "READY"}
        or not execution.authoritative
        or execution.execution_started
        or execution.provider_session_started
        or execution.provider_invoked
    ):
        errors.append("execution_instance_not_startable")
    return tuple(dict.fromkeys(errors))


def create_provider_runtime_session(
    request: ProviderRuntimeSessionInputV1,
) -> ProviderRuntimeSessionResultV1:
    errors = _valid_session_sources(request)
    if errors:
        return ProviderRuntimeSessionResultV1(
            getattr(request, "session_request_ref", ""), "INVALID_INPUT", None,
            errors, getattr(getattr(request, "execution_instance", None), "execution_instance_ref", ""),
            getattr(request, "trace_ref", ""),
        )
    execution = request.execution_instance
    binding = request.provider_binding
    grant = request.runtime_grant
    allocation = request.runtime_allocation
    session = ProviderRuntimeSessionV1(
        session_ref=_session_ref(request.session_request_ref, execution.execution_instance_ref),
        execution_instance_ref=execution.execution_instance_ref,
        provider_binding_ref=binding.binding_ref,
        runtime_grant_ref=grant.grant_ref,
        runtime_allocation_ref=allocation.allocation_ref,
        provider_ref=binding.provider_ref,
        capability_ref=binding.capability_ref,
        source_model_ref=binding.source_model_ref,
        session_owner_ref=OWNER,
        status="CREATED",
        parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
        source_state_ref=execution.source_state_ref,
        lineage_refs=_unique((*execution.lineage_refs, binding.binding_ref, grant.grant_ref, allocation.allocation_ref)),
        provenance_refs=_unique((*execution.provenance_refs, *binding.provenance_refs, *grant.provenance_refs, *allocation.provenance_refs, *request.provenance_refs)),
        trace_ref=request.trace_ref,
    )
    return ProviderRuntimeSessionResultV1(
        request.session_request_ref, "PROVIDER_RUNTIME_SESSION_CREATED", session,
        (), execution.execution_instance_ref, request.trace_ref,
    )


def _valid_invocation_sources(request: ProviderInvocationInputV1) -> Tuple[str, ...]:
    errors = []
    if not isinstance(request, ProviderInvocationInputV1):
        return ("request_type_invalid",)
    if not request.invocation_request_ref or not request.trace_ref:
        errors.append("invocation_request_ref_or_trace_missing")
    if request.outcome not in INVOCATION_OUTCOMES:
        errors.append("invocation_outcome_invalid")
    if not isinstance(request.session, ProviderRuntimeSessionV1):
        errors.append("session_type_invalid")
    if not isinstance(request.execution_instance, ExecutionInstanceV1):
        errors.append("execution_instance_type_invalid")
    if not isinstance(request.provider_binding, ProviderBindingDecisionV1):
        errors.append("provider_binding_type_invalid")
    if not isinstance(request.runtime_grant, RuntimeExecutionGrantDecisionV1):
        errors.append("runtime_grant_type_invalid")
    if not isinstance(request.runtime_allocation, RuntimeAllocationRecordV1):
        errors.append("runtime_allocation_type_invalid")
    if errors:
        return tuple(errors)
    errors.extend(_valid_source_lineage(request.execution_instance, request.provider_binding, request.runtime_grant, request.runtime_allocation))
    session = request.session
    if session.status not in {"CREATED", "READY"}:
        errors.append("session_not_startable")
    if session.execution_instance_ref != request.execution_instance.execution_instance_ref:
        errors.append("session_execution_mismatch")
    if session.provider_binding_ref != request.provider_binding.binding_ref:
        errors.append("session_binding_mismatch")
    if session.runtime_grant_ref != request.runtime_grant.grant_ref:
        errors.append("session_grant_mismatch")
    if session.runtime_allocation_ref != request.runtime_allocation.allocation_ref:
        errors.append("session_allocation_mismatch")
    errors.extend(_valid_session_sources(ProviderRuntimeSessionInputV1(
        session_request_ref=request.invocation_request_ref,
        execution_instance=request.execution_instance,
        provider_binding=request.provider_binding,
        runtime_grant=request.runtime_grant,
        runtime_allocation=request.runtime_allocation,
        trace_ref=request.trace_ref,
    )))
    return tuple(dict.fromkeys(errors))


def start_controlled_provider_invocation(
    request: ProviderInvocationInputV1,
) -> ProviderInvocationResultV1:
    if isinstance(request, ProviderInvocationInputV1) and request.duplicate_start:
        if isinstance(request.session, ProviderRuntimeSessionV1) and request.session.status == "STARTED":
            return ProviderInvocationResultV1(
                request.invocation_request_ref, "DUPLICATE_START_BLOCKED", request.session, None,
                (), request.trace_ref,
            )
    errors = _valid_invocation_sources(request)
    if errors:
        return ProviderInvocationResultV1(
            getattr(request, "invocation_request_ref", ""), "INVALID_INPUT", None, None,
            errors, getattr(request, "trace_ref", ""),
        )
    session = request.session
    status_map = {
        "COMPLETED": ("COMPLETED", True, None),
        "FAILED": ("FAILED", False, "Provider Runtime Governance"),
        "STOPPED": ("STOPPED", False, "Provider Runtime Governance"),
        "REVOKED": ("REVOKED", False, "Permission / Admission Manager"),
        "TIMED_OUT": ("TIMED_OUT", False, "Provider Runtime Governance"),
    }
    session_status, completed, failure_owner = status_map[request.outcome]
    invocation_ref = _invocation_ref(request.invocation_request_ref, session.session_ref)
    result_ref = f"result:controlled:{invocation_ref}"
    payload_ref = f"payload:synthetic:opaque:{invocation_ref}"
    invocation = ProviderInvocationRecordV1(
        invocation_ref=invocation_ref,
        session_ref=session.session_ref,
        execution_instance_ref=request.execution_instance.execution_instance_ref,
        provider_binding_ref=request.provider_binding.binding_ref,
        runtime_grant_ref=request.runtime_grant.grant_ref,
        runtime_allocation_ref=request.runtime_allocation.allocation_ref,
        provider_ref=request.provider_binding.provider_ref,
        capability_ref=request.provider_binding.capability_ref,
        source_model_ref=request.provider_binding.source_model_ref,
        status=request.outcome,
        result_ref=result_ref,
        payload_ref=payload_ref,
        failure_owner_ref=failure_owner,
        parent_cognitive_problem_ref=session.parent_cognitive_problem_ref,
        source_state_ref=session.source_state_ref,
        lineage_refs=_unique((*session.lineage_refs, invocation_ref)),
        provenance_refs=_unique((*session.provenance_refs, *request.provenance_refs)),
        trace_ref=request.trace_ref,
        controlled_invocation_completed=completed,
    )
    transitioned = replace(session, status=session_status, execution_started=True)
    return ProviderInvocationResultV1(
        request.invocation_request_ref, f"PROVIDER_INVOCATION_{request.outcome}", transitioned,
        invocation, (), request.trace_ref,
    )


__all__ = [
    "OWNER", "SESSION_STATUSES", "INVOCATION_STATUSES", "INVOCATION_OUTCOMES",
    "ProviderRuntimeSessionInputV1", "ProviderRuntimeSessionV1", "ProviderRuntimeSessionResultV1",
    "ProviderInvocationInputV1", "ProviderInvocationRecordV1", "ProviderInvocationResultV1",
    "create_provider_runtime_session", "start_controlled_provider_invocation",
]
