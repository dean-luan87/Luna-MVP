import time
from typing import Optional

from .types import ObservationState


class ObservedEntity:
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self.state = ObservationState.NOT_SEEN
        self.last_seen_ts: Optional[float] = None
        self.state_enter_ts: float = time.time()

    def transition(self, new_state: ObservationState, ts: Optional[float] = None):
        if ts is None:
            ts = time.time()
        self.state = new_state
        self.state_enter_ts = ts

    def mark_seen(self, ts: float):
        self.last_seen_ts = ts
