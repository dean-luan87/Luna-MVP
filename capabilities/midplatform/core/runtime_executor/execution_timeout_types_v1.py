"""Timeout candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutCandidateV1:
    admission_timeout_ms: int
    queue_timeout_ms: int
    execution_timeout_ms: int
    timed_out: bool
    timeout_stage: str | None
    trace_required: bool = True
    candidate_only: bool = True
