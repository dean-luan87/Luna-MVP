"""Types for governance-only A3 Cognitive Analysis Learning Candidates v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


LEARNING_CANDIDATE_SCHEMA_VERSION_V1 = (
    "luna.cognitive_analysis.learning_candidate_governance.v1"
)

ALLOWED_REVIEW_STATUSES_V1 = (
    "review_required",
    "pending_review",
    "under_review",
    "review_rejected",
    "review_approved_for_admission_candidate",
)

ALLOWED_ADMISSION_STATUSES_V1 = (
    "not_submitted",
    "review_required",
    "admission_candidate_ready",
    "admission_deferred",
    "admission_rejected",
)

FORBIDDEN_OPERATION_FLAGS_V1 = (
    "direct_training",
    "model_update",
    "memory_write",
    "case_library_write",
    "runtime_executed",
)


@dataclass(frozen=True)
class CognitiveAnalysisLearningCandidateV1:
    """A review-bound candidate; never a training, memory, case, Fact, or State write."""

    candidate_id: str
    source_analysis_ref: str
    evidence_refs: Tuple[str, ...]
    confidence: float | None
    uncertainty: Mapping[str, object]
    provenance: Mapping[str, object]
    review_status: str
    admission_status: str
    operation_flags: Mapping[str, bool]
    candidate_only: bool = True
    runtime_authorized: bool = False
    schema_version: str = LEARNING_CANDIDATE_SCHEMA_VERSION_V1
