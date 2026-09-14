"""Final permission/safety/confirmation gate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionFinalGateResultV1:
    passed: bool
    permission_valid: bool
    safety_valid: bool
    confirmation_valid: bool
    scope_valid: bool
    time_window_valid: bool
    reason: str
    candidate_only: bool = True
