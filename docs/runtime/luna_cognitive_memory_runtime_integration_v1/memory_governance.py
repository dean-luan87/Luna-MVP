"""Admission boundary for memory candidates."""
from __future__ import annotations

from dataclasses import dataclass

from .memory_candidate import MemoryCandidate


@dataclass(frozen=True)
class MemoryReview:
    candidate_id: str
    approved: bool
    reason: str
    status: str


class MemoryGovernance:
    """Requires an explicit review decision; no automatic learning occurs."""

    def review(self, candidate: MemoryCandidate, approved: bool, reason: str) -> MemoryReview:
        if not reason.strip():
            raise ValueError("memory review requires a reason")
        status = "validated" if approved else "rejected"
        return MemoryReview(candidate.candidate_id, approved, reason, status)

    def apply_review(self, candidate: MemoryCandidate, review: MemoryReview) -> MemoryCandidate:
        if review.candidate_id != candidate.candidate_id:
            raise ValueError("review does not match candidate")
        return candidate.validated() if review.approved else candidate.rejected()

    @staticmethod
    def can_store(candidate: MemoryCandidate) -> bool:
        return candidate.validation_status == "validated" and candidate.scope in {"self", "social"}
