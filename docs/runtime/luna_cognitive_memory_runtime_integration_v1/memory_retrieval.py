"""Context-bound retrieval from separate Self and Social Memory stores."""
from __future__ import annotations

from typing import Iterable

from .memory_candidate import MemoryCandidate
from .memory_store import MemoryStore


class MemoryRetrieval:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def retrieve(self, scope: str, terms: Iterable[str] = (), limit: int = 8) -> tuple[MemoryCandidate, ...]:
        if limit < 0:
            raise ValueError("limit must be non-negative")
        normalized = {term.lower() for term in terms}
        matches = []
        for entry in self.store.entries(scope):
            searchable = str(entry.content).lower()
            if not normalized or any(term in searchable for term in normalized):
                matches.append(entry)
        return tuple(matches[:limit])
