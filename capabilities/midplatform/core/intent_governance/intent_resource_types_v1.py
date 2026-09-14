"""Resource constraints and degradation candidates for Intent Governance v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class IntentResourceConstraintV1:
    constraint_id: str
    resource_dimensions: Tuple[str, ...]
    degradation_candidates: Tuple[str, ...]
    preserved_signals: Tuple[str, ...]
    omitted_due_to_resource: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    force_winner: bool = False
    delete_dormant_candidates: bool = False
    mutate_truth_status: bool = False


@dataclass(frozen=True)
class IntentProjectionScopeV1:
    intent_id: str
    active_projection_breadth: int
    alternative_expansion_breadth: int
    historical_retrieval_breadth: int
    low_resource_mode: bool
    candidate_only: bool = True
