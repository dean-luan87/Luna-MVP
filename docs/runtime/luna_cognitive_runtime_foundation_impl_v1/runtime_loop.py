"""Minimal deterministic cognitive runtime loop skeleton.

The loop processes events into owned state and trace records. It intentionally
does not invoke Brain, providers, models, hardware, or action execution.
"""
from __future__ import annotations

from typing import Any, Mapping, Optional

from .event_bus import EventBus
from .runtime_health_monitor import RuntimeHealthMonitor
from .runtime_lifecycle import RuntimeLifecycle
from .runtime_types import RuntimeEvent, RuntimeHealth, RuntimeSnapshot
from .snapshot_manager import SnapshotManager
from .state_container import StateContainer
from .trace_manager import TraceManager


class CognitiveRuntime:
    """Side-effect-free runtime coordinator; callers explicitly drive ticks."""

    def __init__(self, initial_state: Optional[Mapping[str, Any]] = None) -> None:
        self.events = EventBus()
        self.state = StateContainer(initial_state)
        self.trace = TraceManager()
        self.snapshots = SnapshotManager()
        self.lifecycle = RuntimeLifecycle()
        self.health = RuntimeHealthMonitor()
        self.tick_count = 0

    def prepare(self) -> str:
        return self.lifecycle.transition("ready")

    def enqueue(self, event: RuntimeEvent) -> None:
        self.events.publish(event)

    def tick(self) -> Optional[RuntimeEvent]:
        if self.lifecycle.state == "created":
            self.prepare()
        if self.lifecycle.state == "ready":
            self.lifecycle.transition("running")
        if self.lifecycle.state != "running":
            return None
        event = self.events.receive()
        if event is not None:
            self.trace.record_event(event.event_id, {"event_type": event.event_type})
            self._apply_event(event)
        self.tick_count += 1
        self.trace.record_tick({"tick": self.tick_count, "event_id": event.event_id if event else None})
        return event

    def run(self, max_ticks: int = 1) -> int:
        if max_ticks < 0:
            raise ValueError("max_ticks must be non-negative")
        processed = 0
        for _ in range(max_ticks):
            if self.tick() is not None:
                processed += 1
            elif not self.events:
                self.tick_count += 0
        return processed

    def pause(self) -> str:
        return self.lifecycle.transition("paused")

    def stop(self) -> str:
        return self.lifecycle.transition("stopped")

    def create_snapshot(self) -> RuntimeSnapshot:
        return self.snapshots.create(self.state.read(), self.lifecycle.state, len(self.trace))

    def restore_snapshot(self, snapshot: RuntimeSnapshot) -> None:
        restored = self.snapshots.restore(snapshot)
        self.state = StateContainer(restored)
        if self.lifecycle.state != snapshot.lifecycle_state:
            self.lifecycle = RuntimeLifecycle()
            if snapshot.lifecycle_state != "created":
                self.lifecycle.transition("ready")
            if snapshot.lifecycle_state == "running":
                self.lifecycle.transition("running")
            elif snapshot.lifecycle_state == "paused":
                self.lifecycle.transition("ready")
                self.lifecycle.transition("running")
                self.lifecycle.transition("paused")

    def health_report(self) -> RuntimeHealth:
        return self.health.assess(self.lifecycle.state, len(self.events), len(self.trace), self.state.version)

    def _apply_event(self, event: RuntimeEvent) -> None:
        domain = "runtime"
        if event.event_type == "observation":
            domain = "global"
        elif event.event_type == "capability":
            domain = "capability"
        elif event.event_type == "failure":
            domain = "runtime"
        elif event.event_type == "lifecycle":
            domain = "runtime"
        current = self.state.read_domain(domain)
        current["last_event_id"] = event.event_id
        current["last_event_type"] = event.event_type
        current["payload"] = dict(event.payload)
        change = self.state.update(domain, current, reason="runtime event intake", event_id=event.event_id)
        self.trace.record_state_change(event.event_id, [change])
