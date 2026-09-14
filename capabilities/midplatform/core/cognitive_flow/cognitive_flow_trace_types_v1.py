"""Trace and provenance types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class CognitiveFlowTraceV1:
    root_cycle_trace_id: str
    cycle_id: str
    previous_cycle_id: str | None
    context_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_ref: str | None
    cognitive_state_vector_ref: str | None
    regulation_candidate_ref: str | None
    field_refs: Tuple[str, ...]
    causal_refs: Tuple[str, ...]
    transition_trace: Tuple[str, ...]
    interrupt_trace: Tuple[str, ...]
    reconsideration_trace: Tuple[str, ...]
    inheritance_trace: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    reverse_lookup: Dict[str, Tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class CognitiveFlowProvenanceV1:
    resulting_cycle_ref: str
    previous_cycle_ref: str | None
    source_snapshot_ref: str
    source_refs: Tuple[str, ...]
    reverse_locatable: bool
    source_owner_mutation: bool = False
