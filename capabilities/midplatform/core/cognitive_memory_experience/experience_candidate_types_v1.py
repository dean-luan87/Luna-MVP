"""Experience candidate types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ExperienceCandidateV1:
    experience_candidate_id: str
    cycle_id: str
    root_cycle_trace_id: str
    timestamp_or_temporal_ref: str
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_ref: str | None
    cognitive_state_vector_ref: str | None
    regulation_candidate_ref: str | None
    causal_refs: Tuple[str, ...]
    decision_refs_optional: Tuple[str, ...]
    action_refs_optional: Tuple[str, ...]
    execution_result_refs_optional: Tuple[str, ...]
    salience_candidate: str
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    user_feedback_refs: Tuple[str, ...]
    source_evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    candidate_only: bool = True
    fact_admitted: bool = False
    persisted: bool = False
