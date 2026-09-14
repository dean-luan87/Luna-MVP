"""Action lifecycle state candidates for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


STATE_CANDIDATES_V1: Tuple[str, ...] = (
    "PROPOSED",
    "ELIGIBLE",
    "PRECONDITION_PENDING",
    "CONSTRAINED",
    "NEEDS_PERMISSION",
    "NEEDS_CONFIRMATION",
    "READY_CANDIDATE",
    "SUSPENDED",
    "BLOCKED",
    "CANCELLED",
    "ROLLBACK_REQUIRED",
    "FAILED_CANDIDATE",
    "REVISED",
    "REVOKED",
)


@dataclass(frozen=True)
class ActionStateTransitionCandidateV1:
    action_candidate_id: str
    from_state: str
    to_state: str
    reason_candidate: str
    precondition_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    provenance_ref: str
