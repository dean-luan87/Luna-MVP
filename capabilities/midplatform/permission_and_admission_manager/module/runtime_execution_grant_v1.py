"""Pre-execution Runtime Grant owned by Permission / Admission Manager.

This module is the authoritative, non-runtime authorization boundary.  It
consumes already formed Provider Binding, Runtime Allocation Preparation, and
Execution Instance Preparation candidates.  A granted decision permits a
future execution boundary to proceed; it does not bind, allocate, create an
execution instance, start a session, submit to Gateway, or invoke a provider.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field, replace
from typing import Iterable, Mapping, Optional, Tuple

from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationCandidateV1,
    RuntimeAllocationPreparationCandidateV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_module_facade_v1 import (
    run_permission_and_admission_manager_module_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    RuntimeAuthorizationScopeV1,
    RuntimeAuthorizationStateV1,
    _authorize_canonical_runtime_authorization,
    _invalidate_canonical_runtime_authorization,
    query_active_authorization_for_grant,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF,
    evaluate_provider_runtime_eligibility_v1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF,
    evaluate_runtime_capability_admission_v1,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    evaluate_runtime_protocol_compliance_v1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    query_current_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    query_current_admitted_action_v1,
)


OWNER = "Permission / Admission Manager"
AUTHORITY_REF = "authority:runtime-execution-authorization"
RESPONSIBILITY_REF = "responsibility:runtime-execution-authorization-decision"
REQUEST_TYPE = "runtime_access_admission"

FORMATION_STATUSES = (
    "RUNTIME_EXECUTION_GRANTS_FORMED",
    "NO_RUNTIME_EXECUTION_GRANT",
    "INVALID_INPUT",
)
DECISIONS = ("GRANTED", "DENIED", "DEFERRED", "REVOKED")
VALIDITY_STATUSES = ("FRESH", "STALE", "EXPIRED", "REVOKED")
PREGRANT_BINDING_KEY_LENGTH = 5
CANONICAL_PREGRANT_BINDING_KEY_LENGTH = 7


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class RuntimeExecutionGrantInputV1:
    """Explicit authorization inputs; all upstream objects remain read-only."""

    grant_request_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    provider_binding_candidates: Tuple[ProviderBindingCandidateV1, ...] = field(
        default_factory=tuple
    )
    runtime_allocation_candidates: Tuple[
        RuntimeAllocationPreparationCandidateV1, ...
    ] = field(default_factory=tuple)
    execution_instance_preparation_candidates: Tuple[
        ExecutionInstancePreparationCandidateV1, ...
    ] = field(default_factory=tuple)
    permission_refs: Tuple[str, ...] = field(default_factory=tuple)
    safety_refs: Tuple[str, ...] = field(default_factory=tuple)
    protocol_refs: Tuple[str, ...] = field(default_factory=tuple)
    governance_refs: Tuple[str, ...] = field(default_factory=tuple)
    constraint_refs: Tuple[str, ...] = field(default_factory=tuple)
    validity_scope: Tuple[str, ...] = field(default_factory=tuple)
    expiry_boundary_ref: str = ""
    revocation_ref: Optional[str] = None
    safety_prerequisite_ref: Optional[str] = None
    safety_prerequisite_refs: Tuple[str, ...] = field(default_factory=tuple)
    effect_class: str = "runtime-execution"
    provider_evaluation_profile_ref: str = PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF
    capability_evaluation_profile_ref: str = PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF
    # Deprecated diagnostic fields. They are retained for controlled caller
    # migration but never participate in authorization.
    provider_binding_status: str = "ELIGIBLE"
    capability_admission_status: str = "ADMITTED"
    permission_status: str = "ALLOWED"
    safety_status: str = "ALLOWED"
    constitution_status: str = "ALLOWED"
    resource_feasibility_status: str = "SATISFIABLE"
    runtime_boundary_status: str = "VALID"
    freshness_status: str = "FRESH"
    validity_status: str = "FRESH"
    execution_ready: bool = True
    requester_ref: str = "requester:runtime-execution"
    grant_authority_ref: str = AUTHORITY_REF
    grant_responsibility_ref: str = RESPONSIBILITY_REF
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    candidate_only: bool = True
    admitted_action_ref: Optional[str] = None
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


@dataclass(frozen=True)
class RuntimeExecutionGrantDecisionV1:
    """Decision record/projection backed by owner-controlled auth state."""

    grant_ref: str
    request_ref: str
    owner_ref: str
    authority_ref: str
    responsibility_ref: str
    decision: str
    source_provider_binding_candidate_ref: str
    source_runtime_allocation_preparation_ref: str
    source_execution_instance_preparation_ref: str
    provider_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    source_observation_demand_ref: str
    source_capability_requirement_ref: str
    source_capability_resolution_candidate_ref: str
    source_perception_routing_candidate_ref: str
    source_admission_compatibility_candidate_ref: str
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    protocol_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    validity_scope: Tuple[str, ...]
    validity_status: str
    expiry_boundary_ref: str
    revocation_ref: Optional[str]
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
    denial_reason: Optional[str] = None
    failure_owner_ref: Optional[str] = None
    authoritative: bool = True
    candidate_only: bool = False
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    provider_bound: bool = False
    binding_decision_formed: bool = False
    model_binding: bool = False
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    gateway_submission: bool = False
    provider_invoked: bool = False
    provider_invocation: bool = False
    model_invoked: bool = False
    model_invocation: bool = False
    capability_activated: bool = False
    capability_activation: bool = False
    slot_reserved: bool = False
    resource_allocated: bool = False
    resource_scheduling: bool = False
    observation_execution: bool = False
    execution_authorized: bool = False
    authorization_ref: str = ""
    freshness_status: str = "FRESH"
    provider_evaluation_profile_ref: str = ""
    capability_evaluation_profile_ref: str = ""
    admitted_action_ref: Optional[str] = None
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


@dataclass(frozen=True)
class RuntimeExecutionGrantResultV1:
    grant_request_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    runtime_execution_grant_refs: Tuple[str, ...]
    decisions: Tuple[RuntimeExecutionGrantDecisionV1, ...]
    excluded_execution_instance_preparation_refs: Tuple[str, ...]
    owner_ref: str = OWNER
    authoritative: bool = True
    candidate_only: bool = False
    read_only: bool = True
    runtime_allocated: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    gateway_submission: bool = False
    provider_invoked: bool = False
    model_invoked: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    admitted_action_ref: Optional[str] = None
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


def _result(
    request: object,
    status: str,
    decisions: Tuple[RuntimeExecutionGrantDecisionV1, ...] = (),
    errors: Tuple[str, ...] = (),
    source_refs: Tuple[str, ...] = (),
) -> RuntimeExecutionGrantResultV1:
    return RuntimeExecutionGrantResultV1(
        grant_request_ref=getattr(request, "grant_request_ref", ""),
        parent_cognitive_problem_ref=getattr(request, "parent_cognitive_problem_ref", ""),
        source_state_ref=getattr(request, "source_state_ref", ""),
        formation_status=status,
        runtime_execution_grant_refs=tuple(item.grant_ref for item in decisions),
        decisions=decisions,
        excluded_execution_instance_preparation_refs=tuple(
            ref for ref in source_refs if ref not in {
                item.source_execution_instance_preparation_ref for item in decisions
            }
        ),
        trace_ref=getattr(request, "trace_ref", ""),
        provenance_refs=_unique(
            (
                "provenance:runtime-execution-grant:v1",
                *getattr(request, "provenance_refs", ()),
                (
                    f"provider-evaluation-profile:{getattr(request, 'provider_evaluation_profile_ref', '')}"
                    if getattr(request, "provider_evaluation_profile_ref", "")
                    else ""
                ),
                (
                    f"capability-evaluation-profile:{getattr(request, 'capability_evaluation_profile_ref', '')}"
                    if getattr(request, "capability_evaluation_profile_ref", "")
                    else ""
                ),
            )
        ),
        validation_errors=errors,
        admitted_action_ref=getattr(request, "admitted_action_ref", None),
        working_envelope_ref=getattr(request, "working_envelope_ref", None),
        working_envelope_version_ref=getattr(
            request, "working_envelope_version_ref", None
        ),
    )


def _collection_errors(request: RuntimeExecutionGrantInputV1) -> list[str]:
    errors: list[str] = []
    collections = (
        ("provider_binding_candidates", request.provider_binding_candidates),
        ("runtime_allocation_candidates", request.runtime_allocation_candidates),
        (
            "execution_instance_preparation_candidates",
            request.execution_instance_preparation_candidates,
        ),
        ("permission_refs", request.permission_refs),
        ("safety_refs", request.safety_refs),
        ("safety_prerequisite_refs", request.safety_prerequisite_refs),
        ("protocol_refs", request.protocol_refs),
        ("governance_refs", request.governance_refs),
        ("constraint_refs", request.constraint_refs),
        ("validity_scope", request.validity_scope),
        ("context_refs", request.context_refs),
        ("lineage_refs", request.lineage_refs),
        ("provenance_refs", request.provenance_refs),
    )
    for name, value in collections:
        if not isinstance(value, tuple):
            errors.append(f"{name}_must_be_tuple")
    return errors


def build_pregrant_authority_binding_key(
    *,
    execution_instance_preparation_candidate_ref: str,
    provider_candidate_ref: str,
    capability_candidate_ref: str,
    admitted_action_ref: Optional[str] = None,
    working_envelope_ref: Optional[str] = None,
    working_envelope_version_ref: Optional[str] = None,
    parent_cognitive_problem_ref: str = "",
    source_state_ref: str = "",
) -> Tuple[str, ...]:
    """Build the only authority-bearing Runtime Scope key.

    The legacy parent/source pair remains accepted by the DTO for data-shape
    compatibility, but it is deliberately not a fallback authority key.
    Incomplete v2 scope is represented by an empty key so every downstream
    owner prerequisite fails closed.
    """
    canonical_scope = (
        admitted_action_ref,
        working_envelope_ref,
        working_envelope_version_ref,
    )
    if all(isinstance(value, str) and value.strip() for value in canonical_scope):
        return (
            "runtime-scope:v2",
            admitted_action_ref,
            working_envelope_ref,
            working_envelope_version_ref,
            execution_instance_preparation_candidate_ref,
            provider_candidate_ref,
            capability_candidate_ref,
        )
    return ()


def _validate(request: object) -> Tuple[str, ...]:
    if not isinstance(request, RuntimeExecutionGrantInputV1):
        return ("request_type_invalid",)
    errors = _collection_errors(request)
    canonical_scope = (
        request.admitted_action_ref,
        request.working_envelope_ref,
        request.working_envelope_version_ref,
    )
    canonical_scope_complete = all(
        isinstance(value, str) and value.strip() for value in canonical_scope
    )
    required = (
        request.grant_request_ref,
        request.expiry_boundary_ref,
        request.trace_ref,
        request.grant_authority_ref,
        request.grant_responsibility_ref,
    )
    if not all(required):
        errors.append("grant_request_incomplete")
    if not canonical_scope_complete:
        errors.append("canonical_runtime_scope_incomplete")
    if not request.candidate_only:
        errors.append("input_candidate_only_required")
    if all(isinstance(value, str) and value.strip() for value in canonical_scope):
        admitted_action = query_current_admitted_action_v1(
            request.admitted_action_ref or ""
        )
        if admitted_action is None:
            errors.append("admitted_action_not_current")
        elif (
            admitted_action.working_envelope_ref != request.working_envelope_ref
            or admitted_action.working_envelope_version_ref
            != request.working_envelope_version_ref
        ):
            errors.append("admitted_action_envelope_scope_mismatch")
    if not request.permission_refs or not request.safety_refs or not request.protocol_refs:
        errors.append("authorization_basis_refs_incomplete")
    if not request.safety_prerequisite_ref and not request.safety_prerequisite_refs:
        errors.append("safety_prerequisite_missing")
    if not request.effect_class:
        errors.append("effect_class_missing")
    if not isinstance(request.provider_evaluation_profile_ref, str) or not request.provider_evaluation_profile_ref.strip():
        errors.append("provider_evaluation_profile_invalid")
    if not isinstance(request.capability_evaluation_profile_ref, str) or not request.capability_evaluation_profile_ref.strip():
        errors.append("capability_evaluation_profile_invalid")
    if not request.governance_refs or not request.validity_scope:
        errors.append("governance_or_validity_refs_incomplete")
    if request.grant_authority_ref != AUTHORITY_REF:
        errors.append("runtime_grant_authority_invalid")
    if request.grant_responsibility_ref != RESPONSIBILITY_REF:
        errors.append("runtime_grant_responsibility_invalid")
    if request.validity_status not in VALIDITY_STATUSES:
        errors.append("validity_status_invalid")
    if request.provider_binding_status not in {"ELIGIBLE", "DENIED", "UNAVAILABLE", "NOT_ADMITTED"}:
        errors.append("provider_binding_status_invalid")
    if request.capability_admission_status not in {"ADMITTED", "NOT_ADMITTED"}:
        errors.append("capability_admission_status_invalid")
    for name, value in (
        ("permission_status", request.permission_status),
        ("safety_status", request.safety_status),
    ):
        if value not in {"ALLOWED", "DENIED", "DEFERRED"}:
            errors.append(f"{name}_invalid")
    if request.constitution_status not in {"ALLOWED", "BLOCKED"}:
        errors.append("constitution_status_invalid")
    if request.resource_feasibility_status not in {"SATISFIABLE", "UNAVAILABLE"}:
        errors.append("resource_feasibility_status_invalid")
    if request.runtime_boundary_status not in {"VALID", "INVALID"}:
        errors.append("runtime_boundary_status_invalid")
    if request.freshness_status not in {"FRESH", "STALE"}:
        errors.append("freshness_status_invalid")
    if not isinstance(request.execution_ready, bool):
        errors.append("execution_ready_invalid")
    if not isinstance(request.provider_binding_candidates, tuple):
        return tuple(dict.fromkeys(errors))
    if not isinstance(request.runtime_allocation_candidates, tuple):
        return tuple(dict.fromkeys(errors))
    if not isinstance(request.execution_instance_preparation_candidates, tuple):
        return tuple(dict.fromkeys(errors))
    bindings = {
        item.provider_binding_candidate_ref: item
        for item in request.provider_binding_candidates
        if isinstance(item, ProviderBindingCandidateV1)
    }
    allocations = {
        item.runtime_allocation_preparation_candidate_ref: item
        for item in request.runtime_allocation_candidates
        if isinstance(item, RuntimeAllocationPreparationCandidateV1)
    }
    if len(bindings) != len(request.provider_binding_candidates):
        errors.append("provider_binding_candidate_type_invalid")
    if len(allocations) != len(request.runtime_allocation_candidates):
        errors.append("runtime_allocation_candidate_type_invalid")
    execution_refs = []
    for item in request.execution_instance_preparation_candidates:
        if not isinstance(item, ExecutionInstancePreparationCandidateV1):
            errors.append("execution_instance_preparation_candidate_type_invalid")
            continue
        execution_refs.append(item.execution_instance_preparation_candidate_ref)
        allocation = allocations.get(item.source_runtime_allocation_preparation_candidate_ref)
        if allocation is None:
            errors.append(f"execution_source_allocation_missing:{item.execution_instance_preparation_candidate_ref}")
            continue
        binding = bindings.get(allocation.source_provider_binding_candidate_ref)
        if binding is None:
            errors.append(f"allocation_source_binding_missing:{item.execution_instance_preparation_candidate_ref}")
            continue
        if (
            allocation.provider_binding_candidate_ref != binding.provider_binding_candidate_ref
            or item.source_provider_binding_candidate_ref != binding.provider_binding_candidate_ref
        ):
            errors.append(f"lineage_mismatch:{item.execution_instance_preparation_candidate_ref}")
        if all(
            isinstance(value, str) and value.strip() for value in canonical_scope
        ) and any(
            (
                binding.admitted_action_ref != request.admitted_action_ref,
                binding.working_envelope_ref != request.working_envelope_ref,
                binding.working_envelope_version_ref
                != request.working_envelope_version_ref,
                allocation.admitted_action_ref != request.admitted_action_ref,
                allocation.working_envelope_ref != request.working_envelope_ref,
                allocation.working_envelope_version_ref
                != request.working_envelope_version_ref,
                item.admitted_action_ref != request.admitted_action_ref,
                item.working_envelope_ref != request.working_envelope_ref,
                item.working_envelope_version_ref
                != request.working_envelope_version_ref,
            )
        ):
            errors.append(
                f"canonical_runtime_scope_mismatch:{item.execution_instance_preparation_candidate_ref}"
            )
        for candidate in (binding, allocation, item):
            if (
                not candidate.candidate_only
                or not candidate.read_only
                or candidate.truth_declared
                or candidate.world_truth_declared
            ):
                errors.append(f"upstream_boundary_invalid:{item.execution_instance_preparation_candidate_ref}")
    if len(execution_refs) != len(set(execution_refs)):
        errors.append("duplicate_execution_instance_preparation_ref")
    return tuple(dict.fromkeys(errors))


def _permission_assessment(request: RuntimeExecutionGrantInputV1) -> Mapping[str, object]:
    payload = {
        "request_id": request.grant_request_ref,
        "request_type": REQUEST_TYPE,
        "subject_ref": request.requester_ref,
        "resource_ref": request.grant_request_ref,
        "source_ref": request.grant_request_ref,
        "owner_ref": request.requester_ref,
        "evidence_refs": request.permission_refs,
        "provenance_refs": request.provenance_refs,
        "requested_authority": "runtime_execution_authorization",
        "requested_operation": "runtime_execution_authorization",
        "policy_snapshot": {
            "request_type_policies": {
                REQUEST_TYPE: {
                    "policy_found": True,
                    "evidence_required": True,
                    "provenance_required": True,
                    "consent_required": False,
                    "ownership_required": True,
                    "authority_required": True,
                    "allow_runtime_dispatch": False,
                    "decision_mode": "allow",
                    "allowed_authorities": ("runtime_execution_authorization",),
                    "allowed_operations": ("runtime_execution_authorization",),
                }
            }
        },
        "risk_context": {},
        "temporal_snapshot": {},
        "trace_ref": request.trace_ref,
    }
    return run_permission_and_admission_manager_module_v1(payload)


def _grant_ref(request_ref: str, execution_ref: str) -> str:
    digest = hashlib.sha256(f"{request_ref}|{execution_ref}".encode("utf-8")).hexdigest()[:24]
    return f"runtime-execution-grant:{digest}"


def _authorization_ref(_request_ref: str, _execution_ref: str) -> str:
    # This identifies one authorization occurrence.  The owner-controlled
    # state transition, rather than this value, establishes authority.
    return f"runtime-authorization:{uuid.uuid4().hex}"


def _decision_for(
    request: RuntimeExecutionGrantInputV1,
    binding: ProviderBindingCandidateV1,
    allocation: RuntimeAllocationPreparationCandidateV1,
    execution: ExecutionInstancePreparationCandidateV1,
) -> RuntimeExecutionGrantDecisionV1:
    binding_key = build_pregrant_authority_binding_key(
        execution_instance_preparation_candidate_ref=execution.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=binding.provider_candidate_ref,
        capability_candidate_ref=binding.capability_candidate_ref,
        admitted_action_ref=request.admitted_action_ref,
        working_envelope_ref=request.working_envelope_ref,
        working_envelope_version_ref=request.working_envelope_version_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
    )
    provider_eligibility = evaluate_provider_runtime_eligibility_v1(
        binding_key=binding_key,
        provider_candidate_ref=binding.provider_candidate_ref,
        capability_candidate_ref=binding.capability_candidate_ref,
        execution_instance_preparation_candidate_ref=execution.execution_instance_preparation_candidate_ref,
        profile_ref=request.provider_evaluation_profile_ref,
    )
    capability_admission = evaluate_runtime_capability_admission_v1(
        binding_key=binding_key,
        capability_candidate_ref=binding.capability_candidate_ref,
        provider_candidate_ref=binding.provider_candidate_ref,
        execution_instance_preparation_candidate_ref=execution.execution_instance_preparation_candidate_ref,
        profile_ref=request.capability_evaluation_profile_ref,
    )
    protocol_compliance = evaluate_runtime_protocol_compliance_v1(
        binding_key=binding_key,
        protocol_refs=request.protocol_refs,
    )
    safety_binding_key = (*binding_key, request.effect_class)
    safety_refs = tuple(
        ref for ref in (
            request.safety_prerequisite_ref,
            *request.safety_prerequisite_refs,
        ) if ref
    )
    safety_prerequisite = None
    for result_ref in safety_refs:
        current = query_current_runtime_safety_prerequisite_v1(
            binding_key=safety_binding_key,
            result_ref=result_ref,
        )
        if current is not None:
            safety_prerequisite = current
            break
    permission = _permission_assessment(request)
    permission_eligible = bool(permission.get("eligibility", {}).get("eligible"))
    decision = "GRANTED"
    reason: Optional[str] = None
    failure_owner: Optional[str] = None
    if provider_eligibility.status != "ELIGIBLE":
        decision, reason, failure_owner = "DENIED", "provider_binding_not_eligible", "Provider Governance"
    elif capability_admission.status != "ADMITTED":
        decision, reason, failure_owner = "DENIED", "capability_not_admitted", "Capability Governance"
    elif not permission_eligible:
        decision, reason, failure_owner = "DENIED", "permission_not_allowed", OWNER
    elif safety_prerequisite is None:
        decision, reason, failure_owner = "DENIED", "safety_prerequisite_not_current", "Safety Governance"
    elif safety_prerequisite.status != "ALLOWED":
        decision, reason, failure_owner = "DENIED", "safety_blocked", "Safety Governance"
    elif protocol_compliance.status != "COMPLIANT":
        decision, reason, failure_owner = "DENIED", "protocol_not_compliant", "Protocol Manager"
    elif not allocation.resource_class_refs or not allocation.execution_class_refs:
        decision, reason, failure_owner = "DENIED", "resource_unavailable", "Resource Governance"
    elif not execution.runtime_envelope_shape_refs:
        decision, reason, failure_owner = "DENIED", "runtime_boundary_invalid", "Runtime Executor"

    return RuntimeExecutionGrantDecisionV1(
        grant_ref=_grant_ref(request.grant_request_ref, execution.execution_instance_preparation_candidate_ref),
        request_ref=request.grant_request_ref,
        owner_ref=OWNER,
        authority_ref=AUTHORITY_REF,
        responsibility_ref=RESPONSIBILITY_REF,
        decision=decision,
        source_provider_binding_candidate_ref=binding.provider_binding_candidate_ref,
        source_runtime_allocation_preparation_ref=allocation.runtime_allocation_preparation_candidate_ref,
        source_execution_instance_preparation_ref=execution.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=binding.provider_candidate_ref,
        capability_candidate_ref=binding.capability_candidate_ref,
        capability_class_ref=binding.capability_class_ref,
        source_observation_demand_ref=binding.source_observation_demand_ref,
        source_capability_requirement_ref=binding.source_capability_requirement_ref,
        source_capability_resolution_candidate_ref=binding.source_capability_resolution_candidate_ref,
        source_perception_routing_candidate_ref=binding.source_perception_routing_candidate_ref,
        source_admission_compatibility_candidate_ref=binding.source_admission_compatibility_candidate_ref,
        permission_refs=request.permission_refs,
        safety_refs=_unique(
            (
                *request.safety_refs,
                request.safety_prerequisite_ref or "",
                *request.safety_prerequisite_refs,
            )
        ),
        protocol_refs=_unique((*request.protocol_refs, protocol_compliance.result_ref)),
        governance_refs=request.governance_refs,
        constraint_refs=request.constraint_refs,
        validity_scope=request.validity_scope,
        validity_status="FRESH",
        expiry_boundary_ref=request.expiry_boundary_ref,
        revocation_ref=None,
        observation_class=binding.observation_class,
        observation_target_refs=binding.observation_target_refs,
        observation_constraint_refs=binding.observation_constraint_refs,
        expected_information_contribution_refs=binding.expected_information_contribution_refs,
        information_need_refs=binding.information_need_refs,
        information_gap_refs=binding.information_gap_refs,
        source_strategy_ref=binding.source_strategy_ref,
        source_branch_ref=binding.source_branch_ref,
        parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
        source_state_ref=binding.source_state_ref,
        context_refs=binding.context_refs,
        lineage_refs=_unique((*binding.lineage_refs, *allocation.lineage_refs, *execution.lineage_refs)),
        provenance_refs=_unique(
            (
                *binding.provenance_refs,
                *allocation.provenance_refs,
                *execution.provenance_refs,
                *request.provenance_refs,
                f"provider-evaluation-profile:{provider_eligibility.evaluation_profile_ref}",
                f"capability-evaluation-profile:{capability_admission.evaluation_profile_ref}",
            )
        ),
        trace_ref=request.trace_ref,
        denial_reason=reason,
        failure_owner_ref=failure_owner,
        execution_authorized=decision == "GRANTED",
        authorization_ref=_authorization_ref(
            request.grant_request_ref,
            execution.execution_instance_preparation_candidate_ref,
        ),
        freshness_status="FRESH",
        provider_evaluation_profile_ref=provider_eligibility.evaluation_profile_ref,
        capability_evaluation_profile_ref=capability_admission.evaluation_profile_ref,
        admitted_action_ref=request.admitted_action_ref,
        working_envelope_ref=request.working_envelope_ref,
        working_envelope_version_ref=request.working_envelope_version_ref,
    )


def form_runtime_execution_grants(
    request: object,
) -> RuntimeExecutionGrantResultV1:
    """Form deterministic grant decisions; never execute the granted request."""

    errors = _validate(request)
    if errors:
        return _result(request, "INVALID_INPUT", errors=errors)
    assert isinstance(request, RuntimeExecutionGrantInputV1)
    if not request.execution_instance_preparation_candidates:
        return _result(request, "NO_RUNTIME_EXECUTION_GRANT")
    bindings = {item.provider_binding_candidate_ref: item for item in request.provider_binding_candidates}
    allocations = {
        item.runtime_allocation_preparation_candidate_ref: item
        for item in request.runtime_allocation_candidates
    }
    decisions = []
    for execution in request.execution_instance_preparation_candidates:
        allocation = allocations[execution.source_runtime_allocation_preparation_candidate_ref]
        binding = bindings[allocation.source_provider_binding_candidate_ref]
        decision = _decision_for(request, binding, allocation, execution)
        if decision.decision == "GRANTED":
            state = _authorize_canonical_runtime_authorization(
                authorization_ref=decision.authorization_ref,
                scope=RuntimeAuthorizationScopeV1.from_grant(decision),
            )
            if state is None:
                decision = replace(
                    decision,
                    decision="DENIED",
                    denial_reason="authorization_state_transition_failed",
                    failure_owner_ref=OWNER,
                    execution_authorized=False,
                )
        decision = replace(
            decision,
            execution_authorized=(
                decision.decision == "GRANTED"
                and query_active_authorization_for_grant(decision) is not None
            ),
        )
        decisions.append(decision)
    return _result(
        request,
        "RUNTIME_EXECUTION_GRANTS_FORMED",
        decisions=tuple(decisions),
        source_refs=tuple(
            item.execution_instance_preparation_candidate_ref
            for item in request.execution_instance_preparation_candidates
        ),
    )


def invalidate_runtime_authorization_state(
    *,
    authorization_ref: str,
    subject_ref: str,
    reason: str,
) -> Optional[RuntimeAuthorizationStateV1]:
    """Request owner-controlled invalidation by canonical identifiers."""

    return _invalidate_canonical_runtime_authorization(
        authorization_ref=authorization_ref,
        subject_ref=subject_ref,
        reason=reason,
    )


__all__ = [
    "OWNER",
    "AUTHORITY_REF",
    "RESPONSIBILITY_REF",
    "FORMATION_STATUSES",
    "RuntimeExecutionGrantInputV1",
    "RuntimeExecutionGrantDecisionV1",
    "RuntimeExecutionGrantResultV1",
    "build_pregrant_authority_binding_key",
    "CANONICAL_PREGRANT_BINDING_KEY_LENGTH",
    "form_runtime_execution_grants",
    "invalidate_runtime_authorization_state",
]
