"""Diagnostics and maintenance handoff candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticsHandoffCandidateV1:
    diagnostics_ref: str
    health_state_candidate: str
    error_code_candidate: str | None
    latency_candidate_ms: int
    failure_rate_candidate: float
    evidence_only: bool = True
    candidate_only: bool = True
