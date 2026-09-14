"""Planning-preserved lifecycle for self-regulation candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


SELF_REGULATION_STATES_V1: Tuple[str, ...] = (
    "OBSERVED",
    "ASSESSED",
    "CANDIDATE",
    "UNDER_REVIEW",
    "DEFERRED",
    "REVISED",
    "REVOKED",
)

SELF_REGULATION_TRANSITIONS_V1: Tuple[Tuple[str, str, str], ...] = (
    ("OBSERVED", "ASSESSED", "input_contract_valid"),
    ("ASSESSED", "CANDIDATE", "bounded_modulation_available"),
    ("CANDIDATE", "UNDER_REVIEW", "trace_and_provenance_present"),
    ("UNDER_REVIEW", "DEFERRED", "approval_missing_or_state_vector_stale"),
    ("UNDER_REVIEW", "REVISED", "new_evidence_or_conflict"),
    ("UNDER_REVIEW", "REVOKED", "boundary_violation_or_source_revoked"),
)


@dataclass(frozen=True)
class SelfRegulationStateCandidateV1:
    regulation_ref: str
    current_state: str
    transition_trace: Tuple[str, ...]
    reason_codes: Tuple[str, ...]
    candidate_only: bool = True
    runtime_activation: bool = False
