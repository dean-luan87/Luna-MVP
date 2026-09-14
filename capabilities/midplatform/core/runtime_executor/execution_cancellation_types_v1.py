"""Cancellation candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CancellationCandidateV1:
    cancel_requested: bool
    cancel_reason: str | None
    cancelled: bool
    cancelled_state: str
    trace_required: bool = True
    candidate_only: bool = True
