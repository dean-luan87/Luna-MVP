"""Candidate-only types for scoped authority grants and Loop mechanics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class CognitiveAuthorityGrantCandidateV1:
    grant_ref: str
    issuer_ref: str
    receiver_ref: str
    receiver_role: str
    concern_ref: str
    work_ref: str
    granted_authority_refs: Tuple[str, ...]
    capability_boundary_ref: str
    goal_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_envelope_refs: Tuple[str, ...]
    valid_from_state_ref: str
    valid_until_condition_refs: Tuple[str, ...]
    revocation_condition_refs: Tuple[str, ...]
    result_receiver_ref: str
    responsibility_owner_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AuthorityGrantStatusCandidateV1:
    grant_ref: str
    status: str
    reason_refs: Tuple[str, ...]
    checked_state_version_ref: str
    valid: bool
    revoked: bool
    expired: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AuthorityRevocationCandidateV1:
    revocation_ref: str
    grant_ref: str
    reason: str
    issuer_ref: str
    effective_state_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AuthorityExpiryCandidateV1:
    expiry_ref: str
    grant_ref: str
    condition_ref: str
    effective_state_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class MechanicalCommandCandidateV1:
    command_ref: str
    command_kind: str
    issuer_ref: str
    issuer_role: str
    receiver_ref: str
    grant_ref: str
    loop_grant_ref: str
    concern_ref: str
    work_ref: str
    source_state_version_ref: str
    target_refs: Tuple[str, ...]
    reason_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class MechanicalCommandValidationCandidateV1:
    command_ref: str
    grant_ref: str
    loop_grant_ref: str
    status: str
    failure_class: Optional[str]
    accepted: bool
    capability_boundary_ok: bool
    grant_active: bool
    scope_ok: bool
    state_version_ok: bool
    responsibility_binding_ok: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class LoopMechanicalStateCandidateV1:
    loop_ref: str
    concern_ref: str
    work_ref: str
    current_mechanical_state: str
    state_version_ref: str
    pending_refs: Tuple[str, ...] = field(default_factory=tuple)
    pause_reason_ref: Optional[str] = None
    wait_reason_ref: Optional[str] = None
    requirement_refs: Tuple[str, ...] = field(default_factory=tuple)
    b_branch_refs: Tuple[str, ...] = field(default_factory=tuple)
    closure_state: str = "OPEN"
    final_freeze_ref: Optional[str] = None
    history_boundary_ref: Optional[str] = None
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class LoopMechanicalReturnCandidateV1:
    loop_ref: str
    current_mechanical_state: str
    state_version_ref: str
    pending_refs: Tuple[str, ...]
    pause_reason_ref: Optional[str]
    wait_reason_ref: Optional[str]
    requirement_refs: Tuple[str, ...]
    b_branch_refs: Tuple[str, ...]
    closure_state: str
    final_freeze_ref: Optional[str]
    history_boundary_ref: Optional[str]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    supplied_semantic_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class DerivedAuthorityGrantCandidateV1:
    derived_grant_ref: str
    source_grant_ref: str
    request_ref: str
    grant: Optional[CognitiveAuthorityGrantCandidateV1]
    inherited_authority_refs: Tuple[str, ...]
    derived_authority_refs: Tuple[str, ...]
    rejected_authority_refs: Tuple[str, ...]
    bounded_by_refs: Tuple[str, ...]
    accepted: bool
    failure_class: Optional[str]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AuthorityResponsibilityBindingCandidateV1:
    binding_ref: str
    authority_ref: str
    decision_authority_ref: str
    responsibility_owner_ref: str
    result_receiver_ref: str
    error_owner_ref: str
    expiry_ref: str
    revocation_authority_ref: str
    valid: bool
    reason_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


__all__ = [
    "CognitiveAuthorityGrantCandidateV1",
    "AuthorityGrantStatusCandidateV1",
    "AuthorityRevocationCandidateV1",
    "AuthorityExpiryCandidateV1",
    "MechanicalCommandCandidateV1",
    "MechanicalCommandValidationCandidateV1",
    "LoopMechanicalStateCandidateV1",
    "LoopMechanicalReturnCandidateV1",
    "DerivedAuthorityGrantCandidateV1",
    "AuthorityResponsibilityBindingCandidateV1",
]
