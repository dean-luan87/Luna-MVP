"""Trace and provenance types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class CognitiveLearningTraceV1:
    root_cycle_trace_id: str
    learning_trace_id: str
    learning_evidence_id: str
    learning_candidate_id: str
    parameter_update_candidate_id: str
    source_experience_refs: Tuple[str, ...]
    source_memory_refs: Tuple[str, ...]
    outcome_refs: Tuple[str, ...]
    feedback_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    revision_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    reverse_lookup: Dict[str, Tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class CognitiveLearningProvenanceV1:
    parameter_update_candidate_ref: str
    learning_candidate_ref: str
    learning_evidence_ref: str
    memory_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    cycle_refs: Tuple[str, ...]
    reverse_locatable: bool
    source_owner_mutation: bool = False
