"""Execution readiness types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionReadinessCandidateV1:
    state: str
    reason: str
    candidate_only: bool = True
    executed: bool = False
