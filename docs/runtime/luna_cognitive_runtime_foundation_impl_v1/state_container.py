"""Owned state container for the runtime skeleton."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .runtime_types import StateChange


DOMAINS = ("global", "self", "capability", "runtime")


class StateContainer:
    """Keeps runtime state behind one explicit writer boundary."""

    def __init__(self, initial: Mapping[str, Any] | None = None) -> None:
        self._state: dict[str, Any] = {domain: {} for domain in DOMAINS}
        self._version = 0
        if initial:
            for domain, value in initial.items():
                self.update(domain, value, reason="initialization")

    @property
    def version(self) -> int:
        return self._version

    def read(self) -> dict[str, Any]:
        return deepcopy(self._state)

    def read_domain(self, domain: str) -> dict[str, Any]:
        self._check_domain(domain)
        return deepcopy(self._state[domain])

    def update(self, domain: str, value: Mapping[str, Any], reason: str, event_id: str | None = None) -> StateChange:
        self._check_domain(domain)
        if not isinstance(value, Mapping):
            raise TypeError("state domain value must be a mapping")
        before = deepcopy(self._state[domain])
        after = deepcopy(dict(value))
        self._state[domain] = after
        self._version += 1
        return StateChange(domain=domain, before=before, after=after, reason=reason, event_id=event_id)

    def update_runtime_status(self, status: str, event_id: str | None = None) -> StateChange:
        runtime = self.read_domain("runtime")
        runtime["status"] = status
        return self.update("runtime", runtime, reason="lifecycle transition", event_id=event_id)

    @staticmethod
    def _check_domain(domain: str) -> None:
        if domain not in DOMAINS:
            raise ValueError(f"unknown state domain: {domain}")
