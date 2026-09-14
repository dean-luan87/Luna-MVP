"""Side-effect-free types for the Luna cognitive runtime skeleton."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional, Tuple
from uuid import uuid4


EVENT_TYPES = {"observation", "system", "capability", "failure", "lifecycle"}
RUNTIME_STATES = {"created", "ready", "running", "paused", "stopped"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class RuntimeEvent:
    event_type: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    source: str = "runtime"

    def __post_init__(self) -> None:
        if self.event_type not in EVENT_TYPES:
            raise ValueError(f"unsupported event type: {self.event_type}")


@dataclass(frozen=True)
class StateChange:
    domain: str
    before: Any
    after: Any
    reason: str
    event_id: Optional[str] = None


@dataclass(frozen=True)
class TraceRecord:
    kind: str
    event_id: Optional[str]
    state_changes: Tuple[StateChange, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class RuntimeSnapshot:
    snapshot_id: str
    state: Mapping[str, Any]
    lifecycle_state: str
    trace_length: int
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class RuntimeHealth:
    status: str
    lifecycle_state: str
    queued_events: int
    trace_records: int
    state_version: int
    reason: str = ""
