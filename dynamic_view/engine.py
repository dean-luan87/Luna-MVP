import time
from typing import Dict, List, Optional

from .entity import ObservedEntity
from .events import ObservationEvent
from .scope import scope_for_entity
from .state_machine import ObservationStateMachine
from .types import ObservationState
from .descriptors import EntityDescriptor
from .binder.base import DescriptorBinder


class ObservationEngine:
    def __init__(self, scheduler=None, binder: Optional[DescriptorBinder] = None):
        self.entities: Dict[str, ObservedEntity] = {}
        self.sm = ObservationStateMachine()
        self._events: List[ObservationEvent] = []
        self.scheduler = scheduler
        self.binder = binder

    def ingest_descriptor(self, descriptor: EntityDescriptor, ts: Optional[float] = None) -> Optional[str]:
        """
        A11-lite：descriptor → entity_id → ingest
        返回使用的 entity_id（便于任务绑定/调试）；若被 scope gate 丢弃则返回 None
        """
        if ts is None:
            ts = time.time()

        if self.binder is None:
            entity_id = f"{descriptor.kind}_{int(ts * 1000)}"
        else:
            entity_id = self.binder.match_or_create(descriptor)

        before = len(self.entities)
        self.ingest(entity_id, ts)
        after = len(self.entities)

        if after == before and entity_id not in self.entities:
            return None
        return entity_id

    def ingest(self, entity_id: str, ts: Optional[float] = None):
        if scope_for_entity(entity_id) is None:
            return
        if ts is None:
            ts = time.time()
        ent = self.entities.get(entity_id)
        if ent is None:
            ent = ObservedEntity(entity_id)
            self.entities[entity_id] = ent
        ent.mark_seen(ts)

    def tick(self, now: Optional[float] = None):
        if now is None:
            now = time.time()
        self._events.clear()
        for ent in self.entities.values():
            prev = ent.state
            timeout = self._invisible_timeout(ent.entity_id, self.sm.evidence_window)
            recovery_grace_time = self._recovery_grace_time(ent.entity_id)
            self.sm.step(
                ent,
                now,
                invisible_timeout=timeout,
                recovery_grace_time=recovery_grace_time,
            )
            if ent.state != prev:
                self._events.append(
                    ObservationEvent(
                        entity_id=ent.entity_id,
                        prev_state=prev,
                        new_state=ent.state,
                        timestamp=now,
                    )
                )

    def _invisible_timeout(self, entity_id: str, default: float) -> float:
        if not self.scheduler:
            return default
        policy = self.scheduler.effective_policy(entity_id)
        if not policy:
            return default
        return policy.max_invisible_time

    def _recovery_grace_time(self, entity_id: str) -> Optional[float]:
        if not self.scheduler:
            return None
        policy = self.scheduler.effective_policy(entity_id)
        if not policy:
            return None
        return policy.recovery_grace_time

    def pop_events(self) -> List[ObservationEvent]:
        return list(self._events)

    def stable_world_state(self):
        return {
            eid: ent
            for eid, ent in self.entities.items()
            if ent.state == ObservationState.STABLE
        }
