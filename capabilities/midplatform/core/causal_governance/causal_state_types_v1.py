"""Lifecycle and transition metadata for Causal Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


STATE_CANDIDATES_V1: Tuple[str, ...] = (
    "PROPOSED",
    "SUPPORTED",
    "CONTESTED",
    "INSUFFICIENT_EVIDENCE",
    "SUSPENDED",
    "REVISED",
    "REJECTED",
    "REVOKED",
)


@dataclass(frozen=True)
class StateTransitionCandidateV1:
    hypothesis_id: str
    from_state: str
    to_state: str
    reason_candidate: str
    supporting_refs: Tuple[str, ...]
    opposing_refs: Tuple[str, ...]
    revision_or_revocation_trace: str
