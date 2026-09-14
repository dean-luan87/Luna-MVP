"""PCN growth candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LinkGrowthCandidate:
    candidate_id: str
    growth_reason: str
    source_ref_a: str
    source_ref_b: str
    relation_type: str
    candidate_only: bool = True


@dataclass(frozen=True)
class LinkStrengtheningCandidate:
    candidate_id: str
    link_id: str
    strengthening_reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class LinkWeakeningCandidate:
    candidate_id: str
    link_id: str
    weakening_reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class DormancyCandidate:
    candidate_id: str
    link_id: str
    dormant_reason: str
    dormant_not_deleted: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class StructuralChangeCandidate:
    candidate_id: str
    structural_signal: str
    review_required: bool = True
    source_mutation_allowed: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class ReactivationCandidate:
    candidate_id: str
    link_id: str
    trigger_ref: str
    historical_state_ref: Optional[str] = None
    candidate_only: bool = True
