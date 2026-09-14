from typing import Dict, Optional

from world_knowledge.schema import ObjectCard
from world_knowledge.profile import EnvironmentProfile


class LocalTrustedSource:
    """
    100% trusted: human-written or verified packs.
    Can be used for reasoning; observation still comes from ChangeDemand.
    """

    def __init__(self, cards: Dict[str, ObjectCard]):
        self._cards = cards

    def get_card(
        self, object_type: str, profile: EnvironmentProfile
    ) -> Optional[ObjectCard]:
        return self._cards.get(object_type)
