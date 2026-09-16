"""Authoritative Provider Binding decision contract.

Provider Governance owns this boundary.  The contract binds an already
governed provider candidate for a controlled execution request; it does not
allocate resources, create an execution instance, start a session, or invoke
the provider.  A valid Runtime Execution Grant is a hard prerequisite.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantDecisionV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
)
from .provider_binding_candidate_v1 import ProviderBindingCandidateV1


OWNER = "Provider Governance"
AUTHORITY_REF = "authority:provider-binding-decision"
RESPONSIBILITY_REF = "responsibility:provider-binding-decision"
DECISIONS = ("BOUND", "DENIED", "DEFERRED", "REVOKED")


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class ProviderBindingDecisionV1:
    binding_ref: str
    source_binding_candidate_ref: str
    source_runtime_grant_ref: str
    provider_ref: str
    capability_ref: str
    capability_class_ref: str
    source_model_ref: Optional[str]
    source_observation_demand_ref: str
    source_capability_requirement_ref: str
    source_capability_resolution_candidate_ref: str
    source_perception_routing_candidate_ref: str
    source_admission_compatibility_candidate_ref: str
    decision: str
    owner_ref: str
    authority_ref: str
    responsibility_ref: str
    binding_scope_refs: Tuple[str, ...]
    validity_status: str
    constraint_refs: Tuple[str, ...]
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
    truth_declared: bool = False
    world_truth_declared: bool = False
    provider_bound: bool = False
    binding_decision_formed: bool = True
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
class ProviderBindingDecisionInputV1:
    decision_request_ref: str
    binding_candidates: Tuple[ProviderBindingCandidateV1, ...] = field(default_factory=tuple)
    runtime_grants: Tuple[RuntimeExecutionGrantDecisionV1, ...] = field(default_factory=tuple)
    provider_eligibility_status: str = "ELIGIBLE"
    binding_status: str = "BOUND"
    validity_status: str = "FRESH"
    constraint_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderBindingDecisionResultV1:
    decision_request_ref: str
    formation_status: str
    binding_decision_refs: Tuple[str, ...]
    decisions: Tuple[ProviderBindingDecisionV1, ...]
    excluded_binding_candidate_refs: Tuple[str, ...]
    owner_ref: str = OWNER
    authoritative: bool = True
    read_only: bool = True
    provider_bound: bool = False
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = ()
    validation_errors: Tuple[str, ...] = ()


def _ref(request_ref: str, candidate_ref: str) -> str:
    digest = hashlib.sha256(f"{request_ref}|{candidate_ref}".encode("utf-8")).hexdigest()[:24]
    return f"provider-binding:decision:{digest}"


def _validate(request: object) -> Tuple[str, ...]:
    if not isinstance(request, ProviderBindingDecisionInputV1):
        return ("request_type_invalid",)
    errors = []
    for name, value in (
        ("binding_candidates", request.binding_candidates),
        ("runtime_grants", request.runtime_grants),
        ("constraint_refs", request.constraint_refs),
        ("provenance_refs", request.provenance_refs),
    ):
        if not isinstance(value, tuple):
            errors.append(f"{name}_must_be_tuple")
    if not request.decision_request_ref or not request.trace_ref:
        errors.append("decision_request_incomplete")
    if not request.candidate_only:
        errors.append("input_candidate_only_required")
    if request.provider_eligibility_status not in {"ELIGIBLE", "DENIED", "UNAVAILABLE", "NOT_ADMITTED"}:
        errors.append("provider_eligibility_status_invalid")
    if request.binding_status not in DECISIONS:
        errors.append("binding_status_invalid")
    if request.validity_status not in {"FRESH", "STALE", "EXPIRED", "REVOKED"}:
        errors.append("validity_status_invalid")
    if not isinstance(request.binding_candidates, tuple) or not isinstance(request.runtime_grants, tuple):
        return tuple(dict.fromkeys(errors))
    candidate_refs = [
        item.provider_binding_candidate_ref
        for item in request.binding_candidates
        if isinstance(item, ProviderBindingCandidateV1)
    ]
    if len(candidate_refs) != len(request.binding_candidates):
        errors.append("binding_candidate_type_invalid")
    if len(candidate_refs) != len(set(candidate_refs)):
        errors.append("duplicate_binding_candidate_ref")
    grant_refs = [
        item.grant_ref
        for item in request.runtime_grants
        if isinstance(item, RuntimeExecutionGrantDecisionV1)
    ]
    if len(grant_refs) != len(request.runtime_grants):
        errors.append("runtime_grant_type_invalid")
    if len(grant_refs) != len(set(grant_refs)):
        errors.append("duplicate_runtime_grant_ref")
    for candidate in request.binding_candidates:
        if not isinstance(candidate, ProviderBindingCandidateV1):
            continue
        if (
            not candidate.candidate_only or not candidate.read_only
            or candidate.truth_declared or candidate.world_truth_declared
            or candidate.provider_bound or candidate.binding_decision_formed
            or candidate.runtime_allocated or candidate.execution_instance_created
            or candidate.provider_session_started or candidate.gateway_submission
            or candidate.provider_invocation or candidate.model_invocation
        ):
            errors.append(f"binding_candidate_boundary_invalid:{candidate.provider_binding_candidate_ref}")
        if not all((candidate.provider_binding_candidate_ref, candidate.provider_candidate_ref, candidate.capability_candidate_ref, candidate.capability_class_ref, candidate.trace_ref)):
            errors.append(f"binding_candidate_incomplete:{candidate.provider_binding_candidate_ref}")
        matching = [
            grant for grant in request.runtime_grants
            if isinstance(grant, RuntimeExecutionGrantDecisionV1)
            and grant.source_provider_binding_candidate_ref == candidate.provider_binding_candidate_ref
        ]
        if len(matching) != 1:
            errors.append(f"runtime_grant_lineage_missing:{candidate.provider_binding_candidate_ref}")
        elif (
            matching[0].decision != "GRANTED"
            or matching[0].validity_status != "FRESH"
            or not matching[0].authoritative
            or matching[0].candidate_only
            or query_active_authorization_for_grant(matching[0]) is None
        ):
            errors.append(f"runtime_grant_not_valid:{candidate.provider_binding_candidate_ref}")
    return tuple(dict.fromkeys(errors))


def form_provider_binding_decisions(request: object) -> ProviderBindingDecisionResultV1:
    errors = _validate(request)
    if not isinstance(request, ProviderBindingDecisionInputV1):
        return ProviderBindingDecisionResultV1("", "INVALID_INPUT", (), (), (), validation_errors=errors)
    candidate_refs = tuple(
        item.provider_binding_candidate_ref
        for item in request.binding_candidates
        if isinstance(item, ProviderBindingCandidateV1)
    )
    if errors:
        return ProviderBindingDecisionResultV1(
            request.decision_request_ref, "INVALID_INPUT", (), (), candidate_refs,
            trace_ref=request.trace_ref, validation_errors=errors,
        )
    if not request.binding_candidates:
        return ProviderBindingDecisionResultV1(
            request.decision_request_ref, "NO_PROVIDER_BINDING_DECISION", (), (), (),
            trace_ref=request.trace_ref,
        )
    grants = {
        item.source_provider_binding_candidate_ref: item
        for item in request.runtime_grants
    }
    decisions = []
    for candidate in request.binding_candidates:
        grant = grants[candidate.provider_binding_candidate_ref]
        decision = request.binding_status
        reason = None
        failure_owner = None
        if request.provider_eligibility_status != "ELIGIBLE":
            decision = "DENIED"
            reason = f"provider_{request.provider_eligibility_status.lower()}"
            failure_owner = OWNER
        elif request.validity_status == "REVOKED":
            decision, reason, failure_owner = "REVOKED", "binding_revoked", OWNER
        elif request.validity_status != "FRESH":
            decision, reason, failure_owner = "DENIED", "binding_not_fresh", OWNER
        decisions.append(
            ProviderBindingDecisionV1(
                binding_ref=_ref(request.decision_request_ref, candidate.provider_binding_candidate_ref),
                source_binding_candidate_ref=candidate.provider_binding_candidate_ref,
                source_runtime_grant_ref=grant.grant_ref,
                provider_ref=candidate.provider_candidate_ref,
                capability_ref=candidate.capability_candidate_ref,
                capability_class_ref=candidate.capability_class_ref,
                source_model_ref=candidate.source_model_ref,
                source_observation_demand_ref=candidate.source_observation_demand_ref,
                source_capability_requirement_ref=candidate.source_capability_requirement_ref,
                source_capability_resolution_candidate_ref=candidate.source_capability_resolution_candidate_ref,
                source_perception_routing_candidate_ref=candidate.source_perception_routing_candidate_ref,
                source_admission_compatibility_candidate_ref=candidate.source_admission_compatibility_candidate_ref,
                decision=decision,
                owner_ref=OWNER,
                authority_ref=AUTHORITY_REF,
                responsibility_ref=RESPONSIBILITY_REF,
                binding_scope_refs=candidate.binding_scope_refs,
                validity_status=request.validity_status,
                constraint_refs=request.constraint_refs,
                parent_cognitive_problem_ref=candidate.parent_cognitive_problem_ref,
                source_state_ref=candidate.source_state_ref,
                context_refs=candidate.context_refs,
                lineage_refs=_unique((*candidate.lineage_refs, grant.grant_ref)),
                provenance_refs=_unique((*candidate.provenance_refs, *request.provenance_refs)),
                trace_ref=request.trace_ref,
                denial_reason=reason,
                failure_owner_ref=failure_owner,
                provider_bound=decision == "BOUND",
                model_binding=False,
            )
        )
    return ProviderBindingDecisionResultV1(
        request.decision_request_ref,
        "PROVIDER_BINDING_DECISIONS_FORMED",
        tuple(item.binding_ref for item in decisions),
        tuple(decisions),
        (),
        trace_ref=request.trace_ref,
        provenance_refs=_unique(("provenance:provider-binding-decision:v1", *request.provenance_refs)),
        provider_bound=all(item.provider_bound for item in decisions),
    )


__all__ = [
    "OWNER", "AUTHORITY_REF", "RESPONSIBILITY_REF", "DECISIONS",
    "ProviderBindingDecisionV1", "ProviderBindingDecisionInputV1",
    "ProviderBindingDecisionResultV1", "form_provider_binding_decisions",
]
