from typing import List

from world_knowledge.schema import ObjectCard, ObservationSignal, InterpretationExperienceCard
from world_knowledge.profile import EnvironmentProfile
from world_knowledge.sources.library_source import CuratedLibrarySource
from world_knowledge.verification.gate import VerificationGate
from world_knowledge.verification.semantic_gate import allow_interpretation_experience


class KnowledgeCurator:
    """
    The only path to write curated knowledge into the library.
    """

    def __init__(self, library: CuratedLibrarySource, gate: VerificationGate):
        self.library = library
        self.gate = gate

    def propose_and_maybe_commit(
        self,
        draft: ObjectCard,
        signals: List[ObservationSignal],
        profile: EnvironmentProfile,
    ) -> bool:
        res = self.gate.verify(signals, draft, profile)
        if not res.accepted:
            return False
        curated = ObjectCard(
            object_type=draft.object_type,
            tags=draft.tags,
            possible_states=draft.possible_states,
            change_types=draft.change_types,
            notes=draft.notes,
            trust_level=res.new_trust_level,
            sources=list(draft.sources) + [{"verified": True, "reasons": res.reasons}],
        )
        self.library.upsert(draft.object_type, curated)
        return True


def curate_interpretation_experience(
    library: CuratedLibrarySource, card: InterpretationExperienceCard
) -> str:
    if not allow_interpretation_experience(card):
        return "REJECTED"
    key = f"interpretation::{card.roi_kind}::{card.category}::{card.meaning}"
    library.upsert(key, card)
    return "CURATED"
