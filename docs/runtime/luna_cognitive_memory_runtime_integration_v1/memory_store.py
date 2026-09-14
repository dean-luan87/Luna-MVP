"""Separate in-memory Self and Social Memory stores; no external persistence."""
from __future__ import annotations

from copy import deepcopy

from .memory_candidate import MemoryCandidate


class MemoryStore:
    def __init__(self) -> None:
        self._entries = {"self": {}, "social": {}}

    def store(self, candidate: MemoryCandidate) -> None:
        if candidate.validation_status != "validated":
            raise ValueError("only validated candidates may be stored")
        self._entries[candidate.scope][candidate.candidate_id] = deepcopy(candidate)

    def entries(self, scope: str) -> tuple[MemoryCandidate, ...]:
        if scope not in self._entries:
            raise ValueError(f"unsupported memory scope: {scope}")
        return tuple(deepcopy(value) for value in self._entries[scope].values())

    def count(self, scope: str) -> int:
        return len(self.entries(scope))
