"""PCN link candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .personal_cognitive_network_types_v1 import (
    CognitiveObjectReference,
    PCNContextReference,
)


TRUTH_UNVERIFIED_OR_SUBJECTIVE = "UNVERIFIED_OR_SUBJECTIVE"


@dataclass(frozen=True)
class CognitiveLinkCandidate:
    link_id: str
    source_refs: Tuple[CognitiveObjectReference, ...]
    relation_type: str
    activation_state: str
    strength_state: str
    formation_source: str
    context_refs: Tuple[PCNContextReference, ...]
    temporal_validity: str
    provenance: str
    confidence: str
    uncertainty: str
    subjective: bool
    truth_status: str = TRUTH_UNVERIFIED_OR_SUBJECTIVE
    candidate_only: bool = True


def strength_not_equal_truth(link: CognitiveLinkCandidate) -> bool:
    """Strength models salience, not truth."""
    return not (
        link.strength_state.upper() in {"STRONG", "VERY_STRONG"}
        and link.truth_status.upper() in {"FACT", "VERIFIED_FACT"}
    )
