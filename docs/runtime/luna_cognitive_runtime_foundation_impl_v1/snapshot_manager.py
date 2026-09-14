"""In-memory snapshot creation and restoration; persistence is intentionally absent."""
from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

from .runtime_types import RuntimeSnapshot


class SnapshotManager:
    def create(self, state: dict, lifecycle_state: str, trace_length: int) -> RuntimeSnapshot:
        return RuntimeSnapshot(
            snapshot_id=str(uuid4()),
            state=deepcopy(state),
            lifecycle_state=lifecycle_state,
            trace_length=trace_length,
        )

    def validate(self, snapshot: RuntimeSnapshot) -> bool:
        return bool(snapshot.snapshot_id and isinstance(snapshot.state, dict) and snapshot.trace_length >= 0)

    def restore(self, snapshot: RuntimeSnapshot) -> dict:
        if not self.validate(snapshot):
            raise ValueError("invalid runtime snapshot")
        return deepcopy(dict(snapshot.state))
