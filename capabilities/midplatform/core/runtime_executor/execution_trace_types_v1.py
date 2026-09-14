"""Execution provenance and trace candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ExecutionTraceCandidateV1:
    trace_id: str
    execution_request_ref: str
    action_candidate_ref: str
    readiness_ref: str
    admission_ref: str
    attempt_refs: Tuple[str, ...]
    result_ref: str
    failure_refs: Tuple[str, ...]
    timeout_refs: Tuple[str, ...]
    cancellation_refs: Tuple[str, ...]
    rollback_refs: Tuple[str, ...]
    adapter_event_refs: Tuple[str, ...]
    scheduler_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    diagnostics_refs: Tuple[str, ...]
    provenance: Tuple[str, ...]
    candidate_only: bool = True
