"""Partial execution result candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PartialExecutionResultCandidateV1:
    execution_id: str
    attempt_number: int
    completed_substeps: Tuple[str, ...]
    remaining_substeps: Tuple[str, ...]
    confidence: float
    trace_ref: str
    candidate_only: bool = True
