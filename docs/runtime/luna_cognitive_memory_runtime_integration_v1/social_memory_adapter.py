"""Social Self Memory scope adapter."""
from __future__ import annotations

from .memory_candidate import MemoryCandidate


class SocialMemoryAdapter:
    scope = "social"

    def accept(self, candidate: MemoryCandidate) -> MemoryCandidate:
        if candidate.scope != self.scope:
            raise ValueError("Social Memory adapter cannot accept Self Memory")
        return candidate
