from enum import Enum
from typing import Optional


class ObservationScope(Enum):
    SAFETY = "safety"
    TASK = "task"


def scope_for_entity(entity_id: str) -> Optional[ObservationScope]:
    if entity_id.startswith(
        ("traffic_light", "elevator", "exit", "obstacle", "crosswalk")
    ):
        return ObservationScope.SAFETY
    if entity_id.startswith(("person", "cat", "dog", "vehicle")):
        return ObservationScope.TASK
    return None
