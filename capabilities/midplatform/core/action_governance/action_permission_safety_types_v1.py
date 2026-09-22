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
