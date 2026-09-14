"""Coexistence/competition interaction candidates for Intent Governance v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


INTERACTION_TYPES_V1: Tuple[str, ...] = (
    "COEXISTENCE",
    "COMPETITION",
    "CONFLICT",
    "SUPPRESSION",
    "AMPLIFICATION",
    "INHIBITION",
    "TEMPORARY_DOMINANCE",
    "REACTIVATION",
)


@dataclass(frozen=True)
class IntentInteractionCandidateV1:
    interaction_id: str
    interaction_type: str
    participant_candidate_ids: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    resource_ref: str
    uncertainty: Tuple[str, ...] = field(default_factory=tuple)
    observed_relation: str = ""
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    decision_authority: bool = False
    action_authority: bool = False
