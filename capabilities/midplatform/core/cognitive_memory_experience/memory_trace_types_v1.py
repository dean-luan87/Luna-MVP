"""Trace and provenance types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class CognitiveMemoryExperienceTraceV1:
    root_cycle_trace_id: str
    cycle_id: str
    experience_candidate_id: str
    memory_candidate_id: str
    source_context_refs: Tuple[str, ...]
    source_field_refs: Tuple[str, ...]
    source_intent_refs: Tuple[str, ...]
    source_hypothesis_refs: Tuple[str, ...]
    current_world_ref: str | None
    regulation_ref: str | None
    decision_action_execution_refs_optional: Tuple[str, ...]
    user_feedback_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    revision_parent_ref: str | None
    superseded_ref: str | None
    revocation_ref: str | None
    provenance_refs: Tuple[str, ...]
    admission_trace: Tuple[str, ...]
    schema_version: str
    contract_version: str
    reverse_lookup: Dict[str, Tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class CognitiveMemoryExperienceProvenanceV1:
    memory_candidate_ref: str
    experience_candidate_ref: str
    cycle_ref: str
    source_evidence_refs: Tuple[str, ...]
    reverse_locatable: bool
    source_owner_mutation: bool = False
