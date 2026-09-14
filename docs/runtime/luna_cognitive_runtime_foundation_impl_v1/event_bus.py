"""Deterministic in-memory event bus; no threads, I/O, or external effects."""
from __future__ import annotations

from collections import deque
from typing import Deque, Iterable, Optional

from .runtime_types import RuntimeEvent


class EventBus:
    """FIFO event boundary used by the minimal runtime loop."""

    def __init__(self, events: Optional[Iterable[RuntimeEvent]] = None) -> None:
        self._queue: Deque[RuntimeEvent] = deque(events or ())

    def publish(self, event: RuntimeEvent) -> None:
        if not isinstance(event, RuntimeEvent):
            raise TypeError("event must be a RuntimeEvent")
        self._queue.append(event)

    def receive(self) -> Optional[RuntimeEvent]:
        return self._queue.popleft() if self._queue else None

    def drain(self, limit: Optional[int] = None) -> list[RuntimeEvent]:
        events: list[RuntimeEvent] = []
        while self._queue and (limit is None or len(events) < limit):
            events.append(self._queue.popleft())
        return events

    def __len__(self) -> int:
        return len(self._queue)
