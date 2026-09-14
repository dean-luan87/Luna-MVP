"""In-memory trace collection for deterministic replay-oriented inspection."""
from __future__ import annotations

from typing import Iterable

from .runtime_types import StateChange, TraceRecord


class TraceManager:
    def __init__(self) -> None:
        self._records: list[TraceRecord] = []

    def record_event(self, event_id: str, details: dict | None = None) -> TraceRecord:
        return self._append(TraceRecord(kind="event", event_id=event_id, details=details or {}))

    def record_state_change(self, event_id: str | None, changes: Iterable[StateChange]) -> TraceRecord:
        return self._append(TraceRecord(kind="state_change", event_id=event_id, state_changes=tuple(changes)))

    def record_tick(self, details: dict | None = None) -> TraceRecord:
        return self._append(TraceRecord(kind="tick", event_id=None, details=details or {}))

    def records(self) -> tuple[TraceRecord, ...]:
        return tuple(self._records)

    def __len__(self) -> int:
        return len(self._records)

    def _append(self, record: TraceRecord) -> TraceRecord:
        self._records.append(record)
        return record
