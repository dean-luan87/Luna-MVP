from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set


@dataclass
class ContextPcnIntentIdempotencyRegistryV1:
    consumed_context_handoffs: Set[str] = field(default_factory=set)
    consumed_pcn_handoffs: Set[str] = field(default_factory=set)

    def consume_context_handoff_once(self, handoff_id: str) -> bool:
        if handoff_id in self.consumed_context_handoffs:
            return False
        self.consumed_context_handoffs.add(handoff_id)
        return True

    def consume_pcn_handoff_once(self, handoff_id: str) -> bool:
        if handoff_id in self.consumed_pcn_handoffs:
            return False
        self.consumed_pcn_handoffs.add(handoff_id)
        return True
