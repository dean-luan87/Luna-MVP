"""Execution state transition candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ExecutionStateTransitionCandidateV1:
    execution_id: str
    from_state: str
    to_state: str
    reason: str
    provenance_refs: Tuple[str, ...]


@dataclass(frozen=True)
class ExecutionStateSnapshotV1:
    execution_id: str
    state: str
    terminal: bool
    attempt_count: int
    candidate_only: bool = True
