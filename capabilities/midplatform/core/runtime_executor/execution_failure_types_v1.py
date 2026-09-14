"""Failure and error result candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ExecutionFailureCandidateV1:
    failure_id: str
    execution_id: str
    failure_class: str
    failure_stage: str
    cause_candidate_refs: Tuple[str, ...]
    trace_ref: str
    retry_authority_granted: bool
    candidate_only: bool = True
