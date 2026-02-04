from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class GateMode(str, Enum):
    ACTIVE = "ACTIVE"
    READ_ONLY = "READ_ONLY"
    SUSPENDED = "SUSPENDED"


class ComputeLevel(str, Enum):
    NONE = "NONE"
    LIGHT = "LIGHT"
    FULL = "FULL"


@dataclass(frozen=True)
class GateRuntimeProfile:
    """
    v0.5 frozen runtime control object.
    This is the single source of truth for whether/how B2 executes at runtime.
    """
    version: str
    gate_mode: GateMode
    compute_level: ComputeLevel
    tick_interval_ms: int
    allow_future_probe: bool
    authority_scope: str  # frozen to "ADVISORY_ONLY" in v0.5
    blocked_by: Optional[str] = None
    human_reason: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "gate_mode": self.gate_mode.value,
            "compute_level": self.compute_level.value,
            "tick_interval_ms": int(self.tick_interval_ms),
            "allow_future_probe": bool(self.allow_future_probe),
            "authority_scope": str(self.authority_scope),
            "blocked_by": self.blocked_by,
            "human_reason": self.human_reason,
            "meta": self.meta,
        }
