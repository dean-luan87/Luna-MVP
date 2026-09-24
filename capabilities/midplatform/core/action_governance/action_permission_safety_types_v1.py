"""Permission and safety status types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PermissionSafetyStatusV1:
    permission_valid: bool
    permission_scope_match: bool
    safety_valid: bool
    safety_scope_match: bool
    permission_recheck_required: bool = True
    safety_recheck_required: bool = True


@dataclass(frozen=True)
class RuntimeSafetyPrerequisiteDecisionV1:
    """Owner-issued, execution-scoped Safety prerequisite.

    ``binding_key`` identifies the stable Safety subject. ``result_ref``
    identifies one evaluation occurrence, not a recoverable binding state.
    A new evaluation (including BLOCKED) has a new ref; revoked occurrences
    cannot become current again. Snapshots/lineage are not currentness proof.
    Invalid input returns an identity-less, non-authoritative diagnostic,
    not a completed evaluation and not an owner-state transition.

    This is not Runtime Authorization and cannot authorize provider effects.
    """

    result_ref: str
    binding_key: Tuple[str, ...]
    effect_class: str
    status: str
    policy_version_ref: str
    reason: str
    expiry_boundary_ref: str
    owner_ref: str = "Brain-owned Safety Governance / Action Boundary"
    authoritative: bool = True
    candidate_only: bool = False
    read_only: bool = True
    revoked: bool = False
