"""Candidate-only contextual projections used by controlled cognition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveEvidenceRelevanceCandidateV1:
    """Contextual relevance of stable Evidence; it never changes Evidence."""

    relevance_ref: str
    evidence_ref: str
    role_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    goal_refs: Tuple[str, ...]
    information_need_refs: Tuple[str, ...]
    relevance_state: str
    relevance_score_candidate: float
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveRelationInterpretationCandidateV1:
    """Role/Task-conditioned interpretation of a stable Field relation."""

    relation_interpretation_ref: str
    relation_ref: str
    role_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    goal_refs: Tuple[str, ...]
    information_need_refs: Tuple[str, ...]
    interpretation_candidate: str
    relevance_state: str
    candidate_only: bool = True
    # Optional read-only typed semantics supplied by a governed Field State
    # projection.  Legacy relation callers continue to provide only
    # relation_ref and the contextual interpretation fields above.
    field_state_candidate_ref: str | None = None
    subject_ref: str | None = None
    predicate: str | None = None
    object_ref: str | None = None
    relation_candidate_ref: str | None = None
    relation_semantic_kind: str | None = None
    evidence_refs: Tuple[str, ...] = ()
    source_refs: Tuple[str, ...] = ()
    provenance_refs: Tuple[str, ...] = ()
    identity_resolution_status: str = "UNRESOLVED"
    fact_admitted: bool = False
    truth_declared: bool = False
    persistent_relation_declared: bool = False
