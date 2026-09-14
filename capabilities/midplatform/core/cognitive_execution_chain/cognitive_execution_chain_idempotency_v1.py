from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set


@dataclass
class CrossLayerIdempotencyRegistryV1:
    consumed_handoffs: Set[str] = field(default_factory=set)
    action_execution_keys: Set[str] = field(default_factory=set)
    feedback_signatures: Set[str] = field(default_factory=set)

    def consume_handoff_once(self, handoff_id: str) -> bool:
        if handoff_id in self.consumed_handoffs:
            return False
        self.consumed_handoffs.add(handoff_id)
        return True

    def register_execution_request(
        self, action_candidate_ref: str, handoff_id: str
    ) -> bool:
        key = f"{action_candidate_ref}::{handoff_id}"
        if key in self.action_execution_keys:
            return False
        self.action_execution_keys.add(key)
        return True

    def register_feedback(self, signature: str) -> bool:
        if signature in self.feedback_signatures:
            return False
        self.feedback_signatures.add(signature)
        return True
