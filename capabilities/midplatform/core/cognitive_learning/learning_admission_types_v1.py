"""Admission/lifecycle state types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LearningAdmissionDecisionCandidateV1:
    decision_id: str
    learning_candidate_ref: str
    admission_state: str
    evidence_strength: str
    repetition: str
    consistency: str
    diversity_of_context: str
    counterexample_density: str
    contradiction_level: str
    recency: str
    temporal_span: str
    user_confirmation: str
    causal_support_status: str
    decision_reasons: Tuple[str, ...]
    candidate_only: bool = True
    trace_ref: str = ""
