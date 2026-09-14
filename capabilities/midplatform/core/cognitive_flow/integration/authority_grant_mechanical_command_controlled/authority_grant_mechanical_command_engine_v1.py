"""Deterministic candidate-only grant and Loop mechanics engine."""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, Mapping, Optional, Tuple

from .authority_grant_mechanical_command_registry_v1 import (
    A_AUTHORITIES,
    B_AUTHORITIES,
    FAILURE_CLASSES,
    GRANT_STATUSES,
    KNOWN_AUTHORITIES,
    LOOP_COMMAND_CAPABILITY,
    LOOP_FORBIDDEN_AUTHORITIES,
    MECHANICAL_COMMANDS,
    ROLE_A,
    ROLE_B,
    ROLE_BRAIN,
    ROLE_CAPABILITY_BOUNDARIES,
    ROLE_LOOP,
    capability_boundary,
)
from .authority_grant_mechanical_command_types_v1 import (
    AuthorityExpiryCandidateV1,
    AuthorityGrantStatusCandidateV1,
    AuthorityResponsibilityBindingCandidateV1,
    AuthorityRevocationCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    DerivedAuthorityGrantCandidateV1,
    LoopMechanicalReturnCandidateV1,
    LoopMechanicalStateCandidateV1,
    MechanicalCommandCandidateV1,
    MechanicalCommandValidationCandidateV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def _append_unique(items: Iterable[str], values: Iterable[str]) -> Tuple[str, ...]:
    result = list(items)
    for value in values:
        if value and value not in result:
            result.append(value)
    return tuple(result)


def validate_responsibility_binding(
    binding: AuthorityResponsibilityBindingCandidateV1,
) -> bool:
    required = (
        binding.authority_ref,
        binding.decision_authority_ref,
        binding.responsibility_owner_ref,
        binding.result_receiver_ref,
        binding.error_owner_ref,
        binding.expiry_ref,
        binding.revocation_authority_ref,
    )
    return (
        binding.candidate_only
        and binding.synthetic_only
        and all(required)
        and binding.valid
    )


def build_grant_status(
    grant: CognitiveAuthorityGrantCandidateV1,
    *,
    checked_state_version_ref: str,
    revoked: bool = False,
    expired: bool = False,
    binding: Optional[AuthorityResponsibilityBindingCandidateV1] = None,
) -> AuthorityGrantStatusCandidateV1:
    reasons = []
    status = "ACTIVE"
    valid = True
    boundary = capability_boundary(grant.receiver_role)

    if not grant.candidate_only or not grant.synthetic_only:
        status = "REJECTED"
        reasons.append("candidate_only_required")
    elif not grant.concern_ref or not grant.work_ref:
        status = "REJECTED"
        reasons.append("scope_ref_missing")
    elif grant.receiver_role not in ROLE_CAPABILITY_BOUNDARIES:
        status = "REJECTED"
        reasons.append("receiver_role_unknown")
    elif not grant.issuer_ref:
        status = "REJECTED"
        reasons.append("issuer_missing")
    elif grant.receiver_role == ROLE_A and not grant.issuer_ref.startswith("brain:"):
        status = "REJECTED"
        reasons.append("a_grant_requires_brain_issuer")
    elif grant.receiver_role == ROLE_B and not grant.issuer_ref.startswith("a:"):
        status = "REJECTED"
        reasons.append("b_grant_requires_a_issuer")
    elif grant.receiver_role == ROLE_LOOP and not grant.issuer_ref.startswith("brain:"):
        status = "REJECTED"
        reasons.append("loop_grant_requires_governed_issuer")
    elif any(authority not in KNOWN_AUTHORITIES for authority in grant.granted_authority_refs):
        status = "REJECTED"
        reasons.append("unsupported_authority")
    elif any(authority not in boundary for authority in grant.granted_authority_refs):
        status = "REJECTED"
        reasons.append("authority_outside_capability_boundary")
    elif checked_state_version_ref != grant.valid_from_state_ref:
        status = "STALE"
        reasons.append("source_state_version_stale")
    elif revoked:
        status = "REVOKED"
        reasons.append("grant_revoked")
    elif expired:
        status = "EXPIRED"
        reasons.append("grant_expired")
    elif not grant.permission_refs or not grant.resource_envelope_refs:
        status = "REJECTED"
        reasons.append("permission_or_resource_scope_missing")
    elif binding is None or not validate_responsibility_binding(binding):
        status = "REJECTED"
        reasons.append("responsibility_binding_invalid")

    valid = status == "ACTIVE"
    return AuthorityGrantStatusCandidateV1(
        grant_ref=grant.grant_ref,
        status=status,
        reason_refs=tuple(reasons) or ("grant_active",),
        checked_state_version_ref=checked_state_version_ref,
        valid=valid,
        revoked=revoked,
        expired=expired,
        trace_ref=_trace(grant.grant_ref),
        provenance_refs=_provenance(grant.grant_ref),
    )


def build_revocation_candidate(
    grant: CognitiveAuthorityGrantCandidateV1,
    *,
    reason: str,
    effective_state_ref: str,
) -> AuthorityRevocationCandidateV1:
    return AuthorityRevocationCandidateV1(
        revocation_ref=f"revocation:{grant.grant_ref}",
        grant_ref=grant.grant_ref,
        reason=reason,
        issuer_ref=grant.issuer_ref,
        effective_state_ref=effective_state_ref,
        trace_ref=_trace(f"revocation:{grant.grant_ref}"),
        provenance_refs=_provenance(f"revocation:{grant.grant_ref}"),
    )


def build_expiry_candidate(
    grant: CognitiveAuthorityGrantCandidateV1,
    *,
    condition_ref: str,
    effective_state_ref: str,
) -> AuthorityExpiryCandidateV1:
    return AuthorityExpiryCandidateV1(
        expiry_ref=f"expiry:{grant.grant_ref}",
        grant_ref=grant.grant_ref,
        condition_ref=condition_ref,
        effective_state_ref=effective_state_ref,
        trace_ref=_trace(f"expiry:{grant.grant_ref}"),
        provenance_refs=_provenance(f"expiry:{grant.grant_ref}"),
    )


def validate_mechanical_command(
    command: MechanicalCommandCandidateV1,
    *,
    issuer_grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    issuer_binding: AuthorityResponsibilityBindingCandidateV1,
    loop_binding: AuthorityResponsibilityBindingCandidateV1,
    current_state_version_ref: str,
    revoked_grant_refs: Iterable[str] = (),
    expired_grant_refs: Iterable[str] = (),
) -> MechanicalCommandValidationCandidateV1:
    revoked = set(revoked_grant_refs)
    expired = set(expired_grant_refs)
    issuer_status = build_grant_status(
        issuer_grant,
        checked_state_version_ref=current_state_version_ref,
        revoked=issuer_grant.grant_ref in revoked,
        expired=issuer_grant.grant_ref in expired,
        binding=issuer_binding,
    )
    loop_status = build_grant_status(
        loop_grant,
        checked_state_version_ref=current_state_version_ref,
        revoked=loop_grant.grant_ref in revoked,
        expired=loop_grant.grant_ref in expired,
        binding=loop_binding,
    )

    failure: Optional[str] = None
    capability_ok = command.command_kind in MECHANICAL_COMMANDS
    scope_ok = (
        command.grant_ref == issuer_grant.grant_ref
        and command.loop_grant_ref == loop_grant.grant_ref
        and command.issuer_ref == issuer_grant.receiver_ref
        and command.issuer_role == issuer_grant.receiver_role
        and command.receiver_ref == loop_grant.receiver_ref
        and command.concern_ref == issuer_grant.concern_ref == loop_grant.concern_ref
        and command.work_ref == issuer_grant.work_ref == loop_grant.work_ref
    )
    state_ok = (
        command.source_state_version_ref == current_state_version_ref
        and command.source_state_version_ref == issuer_grant.valid_from_state_ref
        and command.source_state_version_ref == loop_grant.valid_from_state_ref
    )
    binding_ok = validate_responsibility_binding(issuer_binding) and validate_responsibility_binding(loop_binding)
    active = issuer_status.valid and loop_status.valid

    if not capability_ok:
        failure = "CAPABILITY_BOUNDARY_VIOLATION"
    elif issuer_status.status == "REVOKED" or loop_status.status == "REVOKED":
        failure = "GRANT_REVOKED"
    elif issuer_status.status == "EXPIRED" or loop_status.status == "EXPIRED":
        failure = "GRANT_EXPIRED"
    elif issuer_status.status == "STALE" or loop_status.status == "STALE" or not state_ok:
        failure = "STALE_STATE_VERSION"
    elif not binding_ok:
        failure = "RESPONSIBILITY_BINDING_INVALID"
    elif not scope_ok:
        failure = "SCOPE_MISMATCH"
    elif not active:
        failure = "AUTHORITY_NOT_GRANTED"

    accepted = failure is None
    return MechanicalCommandValidationCandidateV1(
        command_ref=command.command_ref,
        grant_ref=command.grant_ref,
        loop_grant_ref=command.loop_grant_ref,
        status="MECHANICAL_COMMAND_ACCEPTED" if accepted else "REJECTED",
        failure_class=None if accepted else failure,
        accepted=accepted,
        capability_boundary_ok=capability_ok,
        grant_active=active,
        scope_ok=scope_ok,
        state_version_ok=state_ok,
        responsibility_binding_ok=binding_ok,
        trace_ref=_trace(command.command_ref),
        provenance_refs=_provenance(command.command_ref),
    )


def apply_mechanical_command(
    state: LoopMechanicalStateCandidateV1,
    command: MechanicalCommandCandidateV1,
    validation: MechanicalCommandValidationCandidateV1,
) -> Tuple[LoopMechanicalStateCandidateV1, LoopMechanicalReturnCandidateV1]:
    if not validation.accepted:
        return state, _return_from_state(state)

    target = command.target_refs[:1]
    reason = command.reason_refs[:1]
    next_state = state
    if command.command_kind == "RECORD_STATE_VERSION" and target:
        next_state = replace(next_state, state_version_ref=target[0])
    elif command.command_kind == "PAUSE":
        next_state = replace(next_state, current_mechanical_state="PAUSED", pause_reason_ref=reason[0] if reason else None)
    elif command.command_kind == "WAIT":
        next_state = replace(next_state, current_mechanical_state="WAITING", wait_reason_ref=reason[0] if reason else None)
    elif command.command_kind in {"RESUME_KEEP", "RESUME_REPLAN"}:
        next_state = replace(next_state, current_mechanical_state="ACTIVE", pause_reason_ref=None, wait_reason_ref=None)
    elif command.command_kind == "CLOSE":
        next_state = replace(next_state, closure_state="CLOSED", current_mechanical_state="COMPLETED")
    elif command.command_kind == "FREEZE_FINAL_STATE":
        next_state = replace(next_state, final_freeze_ref=target[0] if target else None)
    elif command.command_kind == "ARCHIVE_HISTORY_BOUNDARY":
        next_state = replace(next_state, history_boundary_ref=target[0] if target else None)

    if command.command_kind == "RECORD_NEED_REF":
        next_state = replace(next_state, pending_refs=_append_unique(next_state.pending_refs, target))
    elif command.command_kind == "RECORD_REQUIREMENT_REF":
        next_state = replace(next_state, requirement_refs=_append_unique(next_state.requirement_refs, target))
    elif command.command_kind == "RECORD_PENDING_CANDIDATE":
        next_state = replace(next_state, pending_refs=_append_unique(next_state.pending_refs, target))
    elif command.command_kind == "SUPERSEDE_REQUIREMENT":
        next_state = replace(next_state, pending_refs=_append_unique(next_state.pending_refs, (f"superseded:{target[0]}",) if target else ()))
    elif command.command_kind == "RECORD_B_BRANCH_REF":
        next_state = replace(next_state, b_branch_refs=_append_unique(next_state.b_branch_refs, target))
    elif command.command_kind == "RECORD_OUTCOME_REF":
        next_state = replace(next_state, pending_refs=_append_unique(next_state.pending_refs, tuple(f"outcome:{item}" for item in target)))

    next_state = replace(
        next_state,
        trace_refs=_append_unique(next_state.trace_refs, (command.trace_ref,)),
        provenance_refs=_append_unique(next_state.provenance_refs, command.provenance_refs),
    )
    return next_state, _return_from_state(next_state)


def _return_from_state(state: LoopMechanicalStateCandidateV1) -> LoopMechanicalReturnCandidateV1:
    return LoopMechanicalReturnCandidateV1(
        loop_ref=state.loop_ref,
        current_mechanical_state=state.current_mechanical_state,
        state_version_ref=state.state_version_ref,
        pending_refs=state.pending_refs,
        pause_reason_ref=state.pause_reason_ref,
        wait_reason_ref=state.wait_reason_ref,
        requirement_refs=state.requirement_refs,
        b_branch_refs=state.b_branch_refs,
        closure_state=state.closure_state,
        final_freeze_ref=state.final_freeze_ref,
        history_boundary_ref=state.history_boundary_ref,
        trace_refs=state.trace_refs,
        provenance_refs=state.provenance_refs,
    )


def derive_b_grant(
    a_grant: CognitiveAuthorityGrantCandidateV1,
    request: Mapping[str, object],
) -> DerivedAuthorityGrantCandidateV1:
    request_ref = str(request.get("request_ref", "request:missing"))
    requested_authorities = tuple(str(item) for item in request.get("requested_authorities", ()))
    rejected = []
    failure: Optional[str] = None
    if a_grant.receiver_role != ROLE_A or "REQUEST_B" not in a_grant.granted_authority_refs:
        failure = "AUTHORITY_NOT_GRANTED"
    elif str(request.get("requester_role", ROLE_A)) != ROLE_A:
        failure = "AUTHORITY_NOT_GRANTED"
    elif str(request.get("concern_ref", "")) != a_grant.concern_ref or str(request.get("work_ref", "")) != a_grant.work_ref:
        failure = "SCOPE_MISMATCH"
    elif str(request.get("source_state_version_ref", "")) != a_grant.valid_from_state_ref:
        failure = "STALE_STATE_VERSION"
    elif str(request.get("resource_ref", "")) not in a_grant.resource_envelope_refs:
        failure = "SCOPE_MISMATCH"
    elif int(request.get("requested_depth", 1)) > int(request.get("max_depth", 1)):
        failure = "SCOPE_MISMATCH"
    else:
        for authority in requested_authorities:
            if authority not in B_AUTHORITIES:
                rejected.append(authority)
        if rejected:
            failure = "CAPABILITY_BOUNDARY_VIOLATION"

    if failure:
        return DerivedAuthorityGrantCandidateV1(
            derived_grant_ref=f"derived:{request_ref}",
            source_grant_ref=a_grant.grant_ref,
            request_ref=request_ref,
            grant=None,
            inherited_authority_refs=tuple(a_grant.granted_authority_refs),
            derived_authority_refs=(),
            rejected_authority_refs=tuple(rejected),
            bounded_by_refs=(a_grant.grant_ref, a_grant.capability_boundary_ref),
            accepted=False,
            failure_class=failure,
            trace_ref=_trace(f"derived:{request_ref}"),
            provenance_refs=_provenance(f"derived:{request_ref}"),
        )

    grant = CognitiveAuthorityGrantCandidateV1(
        grant_ref=f"grant:b:{request_ref}",
        issuer_ref=a_grant.receiver_ref,
        receiver_ref=f"b:{request_ref}",
        receiver_role=ROLE_B,
        concern_ref=a_grant.concern_ref,
        work_ref=a_grant.work_ref,
        granted_authority_refs=requested_authorities,
        capability_boundary_ref="boundary:B_CONTINGENCY_ROLE",
        goal_refs=a_grant.goal_refs,
        role_refs=a_grant.role_refs,
        field_refs=a_grant.field_refs,
        safety_refs=a_grant.safety_refs,
        permission_refs=a_grant.permission_refs,
        resource_envelope_refs=(str(request.get("resource_ref")),),
        valid_from_state_ref=a_grant.valid_from_state_ref,
        valid_until_condition_refs=a_grant.valid_until_condition_refs + tuple(str(item) for item in request.get("stop_condition_refs", ())),
        revocation_condition_refs=a_grant.revocation_condition_refs,
        result_receiver_ref=a_grant.receiver_ref,
        responsibility_owner_ref=f"responsibility:b:{request_ref}",
        trace_ref=_trace(f"grant:b:{request_ref}"),
        provenance_refs=_provenance(f"grant:b:{request_ref}"),
    )
    return DerivedAuthorityGrantCandidateV1(
        derived_grant_ref=f"derived:{request_ref}",
        source_grant_ref=a_grant.grant_ref,
        request_ref=request_ref,
        grant=grant,
        inherited_authority_refs=tuple(a_grant.granted_authority_refs),
        derived_authority_refs=requested_authorities,
        rejected_authority_refs=(),
        bounded_by_refs=(a_grant.grant_ref, a_grant.capability_boundary_ref, "boundary:B_CONTINGENCY_ROLE"),
        accepted=True,
        failure_class=None,
        trace_ref=_trace(f"derived:{request_ref}"),
        provenance_refs=_provenance(f"derived:{request_ref}"),
    )


def known_failure_class(value: Optional[str]) -> bool:
    return value in FAILURE_CLASSES


__all__ = [
    "validate_responsibility_binding",
    "build_grant_status",
    "build_revocation_candidate",
    "build_expiry_candidate",
    "validate_mechanical_command",
    "apply_mechanical_command",
    "derive_b_grant",
    "known_failure_class",
]
