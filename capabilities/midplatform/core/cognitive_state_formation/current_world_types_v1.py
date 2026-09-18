"""Current world candidate types for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


SourceVersionPairsV1 = Tuple[Tuple[str, str], ...]


def _validate_source_versions(value: object) -> None:
    if not isinstance(value, tuple):
        raise TypeError("source_versions_must_be_tuple_of_pairs")
    keys = set()
    for item in value:
        if not isinstance(item, tuple) or len(item) != 2:
            raise TypeError("source_versions_pair_must_be_two_tuple")
        key, version = item
        if not isinstance(key, str) or not key.strip():
            raise ValueError("source_versions_key_must_be_non_empty_string")
        if not isinstance(version, str) or not version.strip():
            raise ValueError("source_versions_value_must_be_non_empty_string")
        if key in keys:
            raise ValueError("source_versions_duplicate_key")
        keys.add(key)


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
    source_versions: SourceVersionPairsV1
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

    def __post_init__(self) -> None:
        _validate_source_versions(self.source_versions)
