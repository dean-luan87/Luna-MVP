"""Execution result candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionResultCandidateV1:
    execution_id: str
    request_id: str
    status: str
    attempt_count: int
    started_at: str
    ended_at: str
    trace_ref: str
    failure_ref: str | None
    partial_result_ref: str | None
    candidate_only: bool = True
    planning_only: bool = True
