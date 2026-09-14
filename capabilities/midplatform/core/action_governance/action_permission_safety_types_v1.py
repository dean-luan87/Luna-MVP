"""Permission and safety status types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionSafetyStatusV1:
    permission_valid: bool
    permission_scope_match: bool
    safety_valid: bool
    safety_scope_match: bool
    permission_recheck_required: bool = True
    safety_recheck_required: bool = True
