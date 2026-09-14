"""Retry request and authority boundary types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryRequestCandidateV1:
    retry_requested: bool
    retry_authorized: bool
    retry_authorized_by: str | None
    failure_classification: str | None
    previous_attempt_ref: str | None
    blocked_reason: str | None
    candidate_only: bool = True
