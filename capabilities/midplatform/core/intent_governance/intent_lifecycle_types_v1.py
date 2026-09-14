"""Lifecycle candidates for Intent Governance v1 (planning-aligned, non-runtime)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


STATE_CANDIDATES_V1: Tuple[str, ...] = (
    "UNKNOWN",
    "POTENTIAL",
    "FORMING",
    "ACTIVE_CANDIDATE",
    "SUPPRESSED",
    "DORMANT",
    "REACTIVATED",
    "RESOLVED_CANDIDATE",
    "ABANDONED_CANDIDATE",
)


TEMPORAL_PATTERNS_V1: Tuple[str, ...] = (
    "SHORT_LIVED",
    "PERSISTENT",
    "RECURRING",
    "DORMANT",
    "REACTIVATED",
    "EVOLVING",
)


@dataclass(frozen=True)
class IntentStateTransitionCandidateV1:
    intent_id: str
    from_state: str
    to_state: str
    reason_candidate: str
    source_refs_present: bool
    context_refs_present: bool
    provenance_present: bool
    uncertainty_preserved: bool
    resource_condition_ref: str
    candidate_only: bool = True
