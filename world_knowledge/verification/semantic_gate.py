from __future__ import annotations

from world_knowledge.schema import InterpretationExperienceCard


def allow_interpretation_experience(card: InterpretationExperienceCard) -> bool:
    if card.confidence < 0.5:
        return False
    if card.stability < 0.65:
        return False
    if card.evidence.get("appear_count", 0) < 6:
        return False
    return True
