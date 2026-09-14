"""Core candidate types for Intent Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str = "REFERENCE"
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class UncertaintyV1:
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    confidence_is_not_truth: bool = True


@dataclass(frozen=True)
class PotentialIntentCandidateV1:
    potential_intent_id: str
    owner: str
    candidate_kind: str
    source_refs: Tuple[SourceRefV1, ...]
    context_refs: Tuple[SourceRefV1, ...]
    pcn_refs: Tuple[SourceRefV1, ...]
    why_candidate: str
    supporting_refs: Tuple[SourceRefV1, ...]
    uncertainty: UncertaintyV1
    alternative_candidates: Tuple[SourceRefV1, ...]
    provenance: Tuple[SourceRefV1, ...]
    formation_trace: Tuple[str, ...]
    temporal_validity_observed_at: str
    temporal_validity_candidate: str
    resource_constraint_ref: Optional[SourceRefV1]
    status: str
    candidate_only: bool = True


@dataclass(frozen=True)
class IntentCandidateV1:
    intent_id: str
    owner: str
    candidate_kind: str
    source_refs: Tuple[SourceRefV1, ...]
    context_refs: Tuple[SourceRefV1, ...]
    pcn_refs: Tuple[SourceRefV1, ...]
    self_refs: Tuple[SourceRefV1, ...]
    field_refs: Tuple[SourceRefV1, ...]
    role_refs: Tuple[SourceRefV1, ...]
    relationship_refs: Tuple[SourceRefV1, ...]
    memory_refs: Tuple[SourceRefV1, ...]
    experience_refs: Tuple[SourceRefV1, ...]
    emotion_refs: Tuple[SourceRefV1, ...]
    direction_candidate: str
    future_state_relation: str
    strength_candidate: Optional[str] = None
    confidence_candidate: Optional[str] = None
    priority_candidate: Optional[str] = None
    truth_status: str = "UNKNOWN"
    uncertainty: Tuple[str, ...] = field(default_factory=tuple)
    alternative_candidates: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    provenance: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    formation_trace: Tuple[str, ...] = field(default_factory=tuple)
    state_candidate: str = "POTENTIAL"
    interaction_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    carryover_candidate: bool = False
    resource_constraint_ref: Optional[SourceRefV1] = None
    causal_handoff_eligible: bool = False
    candidate_only: bool = True
    reference_only: bool = True
    decision_output: bool = False
    action_output: bool = False
    task_output: bool = False
    causal_output: bool = False
    runtime_executed: bool = False
    source_mutation_executed: bool = False
