"""Attention candidate types for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class AttentionCandidateV1:
    attention_id: str
    subject_ref: str
    source_refs: Tuple[str, ...]
    reason_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    observation_refs: Tuple[str, ...]
    risk_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    memory_refs: Tuple[str, ...]
    relevance_score_candidate: float
    salience_score_candidate: float
    risk_score_candidate: float
    urgency_score_candidate: float
    uncertainty_score_candidate: float
    intent_alignment_candidate: float
    attention_priority_candidate: float
    attention_state: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    score_semantics: str = "candidate_heuristic"
    candidate_only: bool = True
    decision_priority: bool = False
    action_priority: bool = False


@dataclass(frozen=True)
class AttentionSelectionCandidateV1:
    selection_id: str
    selected_attention_refs: Tuple[str, ...]
    alternative_attention_refs: Tuple[str, ...]
    risk_override_applied: bool
    uncertainty_retained: bool
    conflicting_focus: bool
    source_missing: bool
    selection_mode: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
