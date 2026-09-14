"""Small result contract for Field relation state -> A-Route assimilation."""

from __future__ import annotations

from dataclasses import dataclass

from capabilities.midplatform.core.cognitive_state_formation.cognitive_conditioning_types_v1 import (
    CognitiveRelationInterpretationCandidateV1,
)


@dataclass(frozen=True)
class RelationStateAssimilationResultV1:
    accepted: bool
    reason: str
    field_state_candidate_ref: str | None = None
    relation_interpretation_candidate: CognitiveRelationInterpretationCandidateV1 | None = None


__all__ = ["RelationStateAssimilationResultV1"]
