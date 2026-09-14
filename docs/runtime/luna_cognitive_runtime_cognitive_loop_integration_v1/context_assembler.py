"""Assemble a bounded context package for one cognitive tick."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
from uuid import uuid4


@dataclass(frozen=True)
class ContextPackage:
    context_id: str
    situation: str
    available_information: tuple[Any, ...]
    self_state_ref: Mapping[str, Any]
    capability_state_ref: Mapping[str, Any]
    unknowns: tuple[Any, ...]
    event_context: Mapping[str, Any] = field(default_factory=dict)
    global_state_ref: Mapping[str, Any] = field(default_factory=dict)
    runtime_state_ref: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "situation": self.situation,
            "available_information": list(self.available_information),
            "self_state_ref": dict(self.self_state_ref),
            "capability_state_ref": dict(self.capability_state_ref),
            "unknowns": list(self.unknowns),
            "event_context": dict(self.event_context),
            "global_state_ref": dict(self.global_state_ref),
            "runtime_state_ref": dict(self.runtime_state_ref),
        }


class ContextAssembler:
    """Read-only composer; it does not write Reality or any source domain."""

    def assemble(self, state: Mapping[str, Any], event_context: Optional[Mapping[str, Any]] = None) -> ContextPackage:
        global_state = dict(state.get("global", {}))
        self_state = dict(state.get("self", {}))
        capability_state = dict(state.get("capability", {}))
        runtime_state = dict(state.get("runtime", {}))
        event = dict(event_context or {})
        available = tuple(event.get("available_information", ()))
        unknowns = tuple(event.get("unknowns", ()))
        situation = str(event.get("situation") or global_state.get("situation") or "unspecified")
        return ContextPackage(
            context_id=str(uuid4()),
            situation=situation,
            available_information=available,
            self_state_ref=self_state,
            capability_state_ref=capability_state,
            unknowns=unknowns,
            event_context=event,
            global_state_ref=global_state,
            runtime_state_ref=runtime_state,
        )
