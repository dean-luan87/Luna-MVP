"""Rollback context types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RollbackContextCandidateV1:
    rollback_required: bool
    rollback_trigger_refs: Tuple[str, ...]
    rollback_executor_responsibility_ref: str
    rollback_result_reference: str
    candidate_only: bool = True
    rollback_executed: bool = False
