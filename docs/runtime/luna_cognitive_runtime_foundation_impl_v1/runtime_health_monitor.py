"""Read-only runtime health projection."""
from __future__ import annotations

from .runtime_types import RuntimeHealth


class RuntimeHealthMonitor:
    def assess(self, lifecycle_state: str, queued_events: int, trace_records: int, state_version: int) -> RuntimeHealth:
        status = "healthy" if lifecycle_state in {"ready", "running", "paused"} else "inactive"
        return RuntimeHealth(
            status=status,
            lifecycle_state=lifecycle_state,
            queued_events=queued_events,
            trace_records=trace_records,
            state_version=state_version,
        )
