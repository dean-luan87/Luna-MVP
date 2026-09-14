"""Scheduler reference candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchedulerReferenceCandidateV1:
    scheduler_ref: str
    delay_reason: str | None
    semantic_mutation: bool = False
    candidate_only: bool = True
