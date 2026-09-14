"""Admission decision types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MemoryAdmissionDecisionCandidateV1:
    decision_id: str
    memory_candidate_ref: str
    admission_state: str
    evidence_sufficiency: str
    provenance_completeness: str
    uncertainty_level: str
    contradiction_level: str
    repetition_level: str
    salience_level: str
    temporal_validity: str
    authority_status: str
    decision_reasons: Tuple[str, ...]
    candidate_only: bool = True
    persisted: bool = False
    trace_ref: str = ""
