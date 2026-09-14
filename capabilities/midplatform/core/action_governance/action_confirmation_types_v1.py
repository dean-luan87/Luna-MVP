"""Human confirmation types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfirmationStatusV1:
    state: str
    is_stale: bool
    is_fabricated: bool
    strong_confirmation: bool
