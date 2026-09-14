"""Governed experience records produced from cognitive outcomes."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


MEMORY_SCOPES = {"self", "social"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ExperienceRecord:
    scope: str
    event: Mapping[str, Any]
    outcome: Mapping[str, Any]
    context: Mapping[str, Any]
    rhythm_mode: str
    record_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    provenance: str = "cognitive_loop_outcome"

    def __post_init__(self) -> None:
        if self.scope not in MEMORY_SCOPES:
            raise ValueError(f"unsupported memory scope: {self.scope}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "scope": self.scope,
            "event": dict(self.event),
            "outcome": dict(self.outcome),
            "context": dict(self.context),
            "rhythm_mode": self.rhythm_mode,
            "created_at": self.created_at,
            "provenance": self.provenance,
        }
