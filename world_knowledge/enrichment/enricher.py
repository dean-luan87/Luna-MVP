from typing import Optional, List

from world_knowledge.schema import ObjectCard, ObservationSignal
from world_knowledge.profile import EnvironmentProfile
from world_knowledge.sources.local_source import LocalTrustedSource
from world_knowledge.sources.library_source import CuratedLibrarySource


class ObjectEnricher:
    """
    Merge local trusted cards and curated library.
    External signals are appended to sources without trust upgrade.
    """

    def __init__(self, local: LocalTrustedSource, library: CuratedLibrarySource):
        self.local = local
        self.library = library

    def enrich(
        self,
        object_type: str,
        profile: EnvironmentProfile,
        extra_signals: Optional[List[ObservationSignal]] = None,
    ) -> Optional[ObjectCard]:
        card = self.local.get_card(object_type, profile) or self.library.get(
            object_type, profile
        )
        if card is None:
            return None
        if extra_signals:
            srcs = list(card.sources) + [
                {"provider": s.provider, "type": s.signal_type} for s in extra_signals
            ]
            return ObjectCard(
                object_type=card.object_type,
                tags=card.tags,
                possible_states=card.possible_states,
                change_types=card.change_types,
                notes=card.notes,
                trust_level=card.trust_level,
                sources=srcs,
            )
        return card
