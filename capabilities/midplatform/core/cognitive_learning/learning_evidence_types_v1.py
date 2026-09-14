"""Learning evidence types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LearningEvidenceCandidateV1:
    learning_evidence_id: str
    source_experience_refs: Tuple[str, ...]
    source_memory_refs: Tuple[str, ...]
    outcome_refs: Tuple[str, ...]
    feedback_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    cognitive_state_vector_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    causal_refs: Tuple[str, ...]
    evidence_strength_candidate: str
    repetition_count_candidate: str
    novelty_candidate: str
    consistency_candidate: str
    contradiction_level_candidate: str
    temporal_span_candidate: str
    scope_candidate: str
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    fact_admitted: bool = False
