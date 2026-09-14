"""PCN interaction reference/candidate types only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


INTERACTION_TYPES = (
    "RESONANCE",
    "COMPETITION",
    "TEMPORARY_OCCUPATION",
    "OVERLAP",
    "COEXISTENCE",
    "FUSION_CANDIDATE",
    "HISTORICAL_REACTIVATION",
)


@dataclass(frozen=True)
class InteractionReferenceCandidate:
    interaction_reference: str
    interaction_type: str
    related_refs: Tuple[str, ...]
    source_context_ref: str
    status: str
    candidate_only: bool = True
    pcn_owns_interaction_kernel: bool = False
