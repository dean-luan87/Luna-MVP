"""Execution attempt candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionAttemptCandidateV1:
    execution_id: str
    attempt_id: str
    attempt_number: int
    previous_attempt_ref: str | None
    retry_requested: bool
    retry_authorized: bool
    retry_authorized_by: str | None
    candidate_only: bool = True
