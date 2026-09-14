"""Pure structural validator for A3 Cognitive Analysis Learning Candidates v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_analysis_learning_candidate_types_v1 import (
    ALLOWED_ADMISSION_STATUSES_V1,
    ALLOWED_REVIEW_STATUSES_V1,
    FORBIDDEN_OPERATION_FLAGS_V1,
    CognitiveAnalysisLearningCandidateV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisLearningCandidateIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisLearningCandidateValidationResultV1:
    issues: Tuple[CognitiveAnalysisLearningCandidateIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_analysis_learning_candidate_v1(
    candidate: CognitiveAnalysisLearningCandidateV1,
) -> CognitiveAnalysisLearningCandidateValidationResultV1:
    """Validate schema and governance flags only; never train, write, or execute Runtime."""
    issues = []
    for field_ref, value in {
        "candidate_id": candidate.candidate_id,
        "source_analysis_ref": candidate.source_analysis_ref,
        "review_status": candidate.review_status,
        "admission_status": candidate.admission_status,
    }.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisLearningCandidateIssueV1(
                "required_field_missing", field_ref, f"{field_ref} must be non-empty"
            ))
    if not candidate.evidence_refs or not all(
        isinstance(reference, str) and reference.strip() for reference in candidate.evidence_refs
    ):
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "evidence_requirement_missing", "evidence_refs", "at least one traceable evidence reference is required"
        ))
    if not isinstance(candidate.uncertainty, dict) or not candidate.uncertainty:
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "uncertainty_missing", "uncertainty", "uncertainty must remain explicit"
        ))
    if not isinstance(candidate.provenance, dict) or not candidate.provenance:
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "traceability_missing", "provenance", "provenance and trace must remain explicit"
        ))
    if candidate.confidence is not None and (
        not isinstance(candidate.confidence, (int, float)) or isinstance(candidate.confidence, bool)
        or not 0.0 <= float(candidate.confidence) <= 1.0
    ):
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "confidence_out_of_range", "confidence", "confidence is optional and must be within [0, 1]"
        ))
    if candidate.review_status not in ALLOWED_REVIEW_STATUSES_V1:
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "review_status_invalid", "review_status", "a governed review state is required"
        ))
    if candidate.admission_status not in ALLOWED_ADMISSION_STATUSES_V1:
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "admission_status_invalid", "admission_status", "actual admission is outside this candidate contract"
        ))
    if not candidate.candidate_only:
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "candidate_boundary_violated", "candidate_only", "Learning Candidate must remain candidate-only"
        ))
    for flag in FORBIDDEN_OPERATION_FLAGS_V1:
        if candidate.operation_flags.get(flag) is not False:
            issues.append(CognitiveAnalysisLearningCandidateIssueV1(
                "forbidden_operation_present", f"operation_flags.{flag}", f"{flag} must be explicitly false"
            ))
    if candidate.runtime_authorized:
        issues.append(CognitiveAnalysisLearningCandidateIssueV1(
            "runtime_authorization_claimed", "runtime_authorized", "Learning Candidate cannot authorize Runtime"
        ))
    return CognitiveAnalysisLearningCandidateValidationResultV1(tuple(issues))
