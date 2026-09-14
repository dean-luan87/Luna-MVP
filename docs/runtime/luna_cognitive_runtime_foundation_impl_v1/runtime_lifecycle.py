"""Explicit lifecycle state machine for the runtime skeleton."""
from __future__ import annotations

from .runtime_types import RUNTIME_STATES


TRANSITIONS = {
    "created": {"ready", "stopped"},
    "ready": {"running", "stopped"},
    "running": {"paused", "stopped"},
    "paused": {"running", "stopped"},
    "stopped": set(),
}


class RuntimeLifecycle:
    def __init__(self) -> None:
        self._state = "created"

    @property
    def state(self) -> str:
        return self._state

    def transition(self, target: str) -> str:
        if target not in RUNTIME_STATES:
            raise ValueError(f"unknown lifecycle state: {target}")
        if target not in TRANSITIONS[self._state]:
            raise ValueError(f"invalid transition: {self._state} -> {target}")
        self._state = target
        return self._state
