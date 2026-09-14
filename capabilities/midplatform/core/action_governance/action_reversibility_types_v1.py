"""Reversibility types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReversibilityStatusV1:
    level: str
    stronger_confirmation_required: bool
    stronger_safety_required: bool
    stronger_permission_required: bool
