from typing import Dict, Optional

from world_knowledge.schema import ObjectCard
from world_knowledge.profile import EnvironmentProfile


class CuratedLibrarySource:
    """
    Curated knowledge store: can be rolled back/versioned later.
    """

    def __init__(self):
        self._store: Dict[str, ObjectCard] = {}

    def upsert(self, object_type: str, card: ObjectCard):
        self._store[object_type] = card

    def get(
        self, object_type: str, profile: EnvironmentProfile
    ) -> Optional[ObjectCard]:
        return self._store.get(object_type)
