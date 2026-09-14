"""PCN activation candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .personal_cognitive_network_types_v1 import (
    CognitiveObjectReference,
    PCNContextReference,
)


ACTIVATION_STATES = ("ACTIVE", "WEAK", "DORMANT", "REACTIVATED")


@dataclass(frozen=True)
class ActivationConstraintReference:
    constraint_id: str
    source: str
    detail: str


@dataclass(frozen=True)
class ActivationRequest:
    request_id: str
    context_ref: PCNContextReference
    source_refs: Tuple[CognitiveObjectReference, ...]
    resource_budget_label: str
    unknown_preserved: bool = True


@dataclass(frozen=True)
class ActivationCandidate:
    candidate_id: str
    activation_state: str
    active_refs: Tuple[CognitiveObjectReference, ...]
    constraint_refs: Tuple[ActivationConstraintReference, ...]
    temporal_validity: str
    confidence: str
    uncertainty: str
    fixed_time_threshold_used: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class ActivationProjection:
    projection_id: str
    activation_ref: str
    active_ref_ids: Tuple[str, ...]
    active_link_ids: Tuple[str, ...]
    unresolved_links: Tuple[str, ...]
    resource_constraint_ref: Optional[str]
    candidate_only: bool = True
