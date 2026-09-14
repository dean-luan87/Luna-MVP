"""Rollback context candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RollbackContextCandidateV1:
    rollback_required: bool
    rollback_reason: str | None
    rollback_policy_ref: str
    rollback_trigger_ref: str | None
    rollback_execution_claimed: bool = False
    candidate_only: bool = True
