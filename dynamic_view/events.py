from dataclasses import dataclass

from .types import ObservationState


@dataclass
class ObservationEvent:
    entity_id: str
    prev_state: ObservationState
    new_state: ObservationState
    timestamp: float
