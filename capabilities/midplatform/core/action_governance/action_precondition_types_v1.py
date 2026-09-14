"""Precondition types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


PRECONDITION_STATUS_SET: Tuple[str, ...] = (
    "missing",
    "unknown",
    "satisfied",
    "violated",
    "stale",
)


@dataclass(frozen=True)
class ActionPreconditionCandidateV1:
    precondition_id: str
    domain: str
    status: str
    required: bool
    provenance_refs: Tuple[str, ...]
