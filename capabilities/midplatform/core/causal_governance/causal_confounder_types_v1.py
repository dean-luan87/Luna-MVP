"""Confounder candidate types for Causal Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ConfounderCandidateV1:
    confounder_id: str
    related_hypothesis_refs: Tuple[str, ...]
    confounder_ref: str
    plausibility_candidate: str
    supporting_refs: Tuple[str, ...]
    opposing_refs: Tuple[str, ...]
    uncertainty: Tuple[str, ...]
    provenance: Tuple[str, ...]
