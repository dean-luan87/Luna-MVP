"""Resource constraint types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceConstraintStatusV1:
    state: str
    reaction: str
