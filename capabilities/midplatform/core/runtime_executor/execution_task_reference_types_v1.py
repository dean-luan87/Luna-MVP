"""Task manager reference candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskReferenceCandidateV1:
    task_ref: str
    dependency_ref: str | None
    cancellation_ref: str | None
    task_mutation: bool = False
    candidate_only: bool = True
