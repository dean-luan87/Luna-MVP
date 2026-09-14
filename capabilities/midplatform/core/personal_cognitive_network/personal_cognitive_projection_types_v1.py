"""PCN active projection candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ActiveCognitiveProjectionCandidate:
    projection_id: str
    active_reference_set: Tuple[str, ...]
    active_link_set: Tuple[str, ...]
    related_context_refs: Tuple[str, ...]
    unresolved_links: Tuple[str, ...]
    interaction_refs: Tuple[str, ...]
    activation_trace_ref: str
    confidence: str
    uncertainty: str
    resource_constraint_ref: str
    provenance: str
    candidate_only: bool = True
    decision_output: bool = False
    causal_output: bool = False
    intent_output: bool = False
