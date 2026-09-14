"""Current world candidate types for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class CurrentWorldCandidateV1:
    current_world_id: str
    attention_refs: Tuple[str, ...]
    active_hypothesis_refs: Tuple[str, ...]
    alternative_hypothesis_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    field_state_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    observation_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    source_versions: Dict[str, str]
    world_state_kind_candidate: str
    world_stability_candidate: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    field_mutation: bool = False
    field_entity_creation: bool = False
    field_confidence_mutation: bool = False
    field_transition: bool = False
    event_admission: bool = False
    reducer_invocation_as_mutation_authority: bool = False
    field_truth_declaration: bool = False
    evidence_relevance_refs: Tuple[str, ...] = ()
    relation_interpretation_refs: Tuple[str, ...] = ()
