"""Dependency types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


DEPENDENCY_STATUS_SET: Tuple[str, ...] = (
    "missing",
    "unknown",
    "satisfied",
    "violated",
    "stale",
)


@dataclass(frozen=True)
class ActionDependencyCandidateV1:
    dependency_id: str
    dependency_type: str
    status: str
    blocking: bool
    provenance_refs: Tuple[str, ...]
