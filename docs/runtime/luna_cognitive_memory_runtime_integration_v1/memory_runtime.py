"""Governed in-memory Memory Runtime integration skeleton."""
from __future__ import annotations

from typing import Any, Mapping, Optional

from .experience_record import ExperienceRecord
from .memory_candidate import MemoryCandidate
from .memory_governance import MemoryGovernance, MemoryReview
from .memory_retrieval import MemoryRetrieval
from .memory_store import MemoryStore
from .rhythm_memory_policy import MemoryBudgetHint, RhythmMemoryPolicy


class MemoryRuntime:
    """Experience → Candidate → Review → Store → Retrieval, with explicit gates."""

    def __init__(self) -> None:
        self.governance = MemoryGovernance()
        self.rhythm_policy = RhythmMemoryPolicy()
        self.store = MemoryStore()
        self.retrieval = MemoryRetrieval(self.store)

    def budget_hint(self, rhythm_mode: str) -> MemoryBudgetHint:
        return self.rhythm_policy.from_mode(rhythm_mode)

    def capture_experience(
        self,
        scope: str,
        event: Mapping[str, Any],
        outcome: Mapping[str, Any],
        context: Mapping[str, Any],
        rhythm_mode: str,
    ) -> tuple[ExperienceRecord, MemoryCandidate]:
        record = ExperienceRecord(scope, dict(event), dict(outcome), dict(context), rhythm_mode)
        hint = self.budget_hint(rhythm_mode)
        retention_class = "high_value_only" if hint.retain_high_value_only else "normal"
        return record, MemoryCandidate.from_record(record, retention_class)

    def review(self, candidate: MemoryCandidate, approved: bool, reason: str) -> tuple[MemoryCandidate, MemoryReview]:
        review = self.governance.review(candidate, approved, reason)
        return self.governance.apply_review(candidate, review), review

    def commit(self, candidate: MemoryCandidate) -> None:
        if not self.governance.can_store(candidate):
            raise ValueError("memory candidate has not passed explicit governance")
        self.store.store(candidate)

    def retrieve(self, scope: str, terms: tuple[str, ...] = (), limit: int = 8) -> tuple[MemoryCandidate, ...]:
        return self.retrieval.retrieve(scope, terms, limit)
