"""Decision lifecycle state candidates for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


STATE_CANDIDATES_V1: Tuple[str, ...] = (
    "PROPOSED",
    "ELIGIBLE",
    "CONSTRAINED",
    "CONTESTED",
    "DEFERRED",
    "ABSTAINED",
    "NEEDS_MORE_EVIDENCE",
    "NEEDS_CONFIRMATION",
    "SELECTED_CANDIDATE",
    "REJECTED",
    "SUSPENDED",
    "REVISED",
    "REVOKED",
)


@dataclass(frozen=True)
class DecisionStateTransitionCandidateV1:
    decision_candidate_id: str
    from_state: str
    to_state: str
    reason_candidate: str
    constraint_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    provenance_ref: str
