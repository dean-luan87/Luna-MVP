"""Decision Candidate data flow; candidates never become Action commands."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True)
class DecisionCandidate:
    decision_candidate_id: str
    context_id: str
    decision_candidate: str
    reasoning_ref: str
    confidence: float
    unknowns: tuple[Any, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_candidate_id": self.decision_candidate_id,
            "context_id": self.context_id,
            "decision_candidate": self.decision_candidate,
            "reasoning_ref": self.reasoning_ref,
            "confidence": self.confidence,
            "unknowns": list(self.unknowns),
            "metadata": dict(self.metadata),
        }


class DecisionCandidateFlow:
    @staticmethod
    def unresolved(context_id: str, unknowns: tuple[Any, ...] = ()) -> DecisionCandidate:
        return DecisionCandidate(
            decision_candidate_id=str(uuid4()),
            context_id=context_id,
            decision_candidate="unresolved_candidate",
            reasoning_ref="brain_boundary_placeholder",
            confidence=0.0,
            unknowns=unknowns,
            metadata={"action_command": False, "reality_mutation": False, "memory_mutation": False},
        )
