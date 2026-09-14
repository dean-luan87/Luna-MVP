"""Self Memory scope adapter."""
from __future__ import annotations

from .memory_candidate import MemoryCandidate


class SelfMemoryAdapter:
    scope = "self"

    def accept(self, candidate: MemoryCandidate) -> MemoryCandidate:
        if candidate.scope != self.scope:
            raise ValueError("Self Memory adapter cannot accept Social Memory")
        return candidate
