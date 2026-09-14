"""Cancellation and suspension types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CancellationSuspensionStatusV1:
    cancelled: bool
    suspended: bool
    reason: str
