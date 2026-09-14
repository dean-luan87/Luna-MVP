"""Reverse-locatable trace and provenance types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Tuple


@dataclass(frozen=True)
class DynamicRegulationTraceV1:
    root_trace_id: str
    scenario_id: str
    cognitive_state_vector_ref: str
    state_vector_trace_ref: str
    source_influence_refs: Tuple[str, ...]
    parameter_refs: Tuple[str, ...]
    parameter_bounds_refs: Tuple[str, ...]
    policy_refs: Tuple[str, ...]
    regulation_function_id: str
    regulation_function_version: str
    prior_regulation_candidate_ref: Optional[str]
    resulting_regulation_candidate_ref: str
    influence_handoff_trace_ref: str
    revision_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    revocation_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    source_version_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    reverse_lookup: Mapping[str, Tuple[str, ...]] = field(default_factory=dict)
    provenance_grants_authority: bool = False


@dataclass(frozen=True)
class DynamicRegulationProvenanceV1:
    source_owner_refs: Tuple[str, ...]
    source_ref_chain: Tuple[str, ...]
    parameter_version_refs: Tuple[str, ...]
    policy_ref_chain: Tuple[str, ...]
    resulting_candidate_ref: str
    reverse_locatable: bool = True
    source_mutation_authority: bool = False
