"""Evidence and admission candidates for Personality Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class PersonalityEvidenceCandidateV1:
    evidence_id: str
    evidence_kind: str
    source_refs: Tuple[str, ...]
    memory_refs: Tuple[str, ...]
    learning_refs: Tuple[str, ...]
    self_refs: Tuple[str, ...]
    emotion_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    interaction_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    sensitivity: str
    temporal_span: int
    repetition: int
    user_correction: bool
    user_confirmed: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    admission_state: str
    candidate_only: bool = True
    semantic_compression_execution: bool = False


@dataclass(frozen=True)
class PersonalityAdmissionDecisionCandidateV1:
    decision_id: str
    evidence_ref: str
    trait_candidate_ref: str
    admission_state: str
    reason_codes: Tuple[str, ...]
    user_correction_precedence: bool
    duplicate_evidence_guard_triggered: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityUserCorrectionCandidateV1:
    correction_id: str
    target_candidate_ref: str
    correction_ref: str
    precedence: str = "USER_CORRECTION_OVER_INFERENCE"
    candidate_only: bool = True
