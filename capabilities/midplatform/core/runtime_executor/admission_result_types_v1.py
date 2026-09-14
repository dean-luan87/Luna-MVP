"""Admission result candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionResultCandidateV1:
    execution_request_id: str
    admitted: bool
    state: str
    reason: str
    permission_valid: bool
    safety_valid: bool
    confirmation_valid: bool
    readiness_fresh: bool
    candidate_only: bool = True
