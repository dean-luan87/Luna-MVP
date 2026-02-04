from typing import Optional

from .types import ObservationState
from .entity import ObservedEntity


class ObservationStateMachine:
    def __init__(self, invisible_ttl: float = 3.0, evidence_window: float = 0.5):
        self.invisible_ttl = invisible_ttl
        self.evidence_window = evidence_window

    def has_recent_evidence(self, entity: ObservedEntity, now: float) -> bool:
        if entity.last_seen_ts is None:
            return False
        return (now - entity.last_seen_ts) <= self.evidence_window

    def step(
        self,
        entity: ObservedEntity,
        now: float,
        invisible_timeout: Optional[float] = None,
        recovery_grace_time: Optional[float] = None,
    ):
        has_evidence = self.has_recent_evidence(entity, now)
        invisible_ttl = invisible_timeout if invisible_timeout is not None else self.evidence_window
        if entity.state == ObservationState.NOT_SEEN:
            if has_evidence:
                entity.transition(ObservationState.APPEARED, now)

        elif entity.state == ObservationState.APPEARED:
            if has_evidence:
                entity.transition(ObservationState.STABLE, now)

        elif entity.state == ObservationState.STABLE:
            if not has_evidence:
                if entity.last_seen_ts and (now - entity.last_seen_ts) > invisible_ttl:
                    entity.transition(ObservationState.INVISIBLE, now)

        elif entity.state == ObservationState.INVISIBLE:
            if has_evidence:
                if recovery_grace_time is None:
                    entity.transition(ObservationState.RECOVERED, now)
                else:
                    within_grace = (now - entity.state_enter_ts) <= recovery_grace_time
                    if within_grace:
                        entity.transition(ObservationState.RECOVERED, now)
                    else:
                        entity.transition(ObservationState.APPEARED, now)
            elif entity.last_seen_ts and (now - entity.last_seen_ts) > self.invisible_ttl:
                entity.transition(ObservationState.DISAPPEARED, now)

        elif entity.state == ObservationState.RECOVERED:
            entity.transition(ObservationState.STABLE, now)
