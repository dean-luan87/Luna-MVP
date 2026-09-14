"""Cognitive hypothesis types for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveHypothesisCandidateV1:
    hypothesis_id: str
    hypothesis_statement_candidate: str
    subject_refs: Tuple[str, ...]
    supporting_evidence_refs: Tuple[str, ...]
    opposing_evidence_refs: Tuple[str, ...]
    alternative_hypothesis_refs: Tuple[str, ...]
    unknown_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    confidence_candidate: str
    state: str
    revision_parent_ref: str | None
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    causal_truth: bool = False
    decision_output: bool = False
    action_output: bool = False


@dataclass(frozen=True)
class HypothesisCompetitionResultV1:
    competition_id: str
    active_hypothesis_refs: Tuple[str, ...]
    suspended_hypothesis_refs: Tuple[str, ...]
    revoked_hypothesis_refs: Tuple[str, ...]
    insufficient_evidence_refs: Tuple[str, ...]
    alternative_explanation_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    support_accumulation_refs: Tuple[str, ...]
    opposition_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    single_truth_collapsed: bool = False
    candidate_only: bool = True
