"""Pure structural validator for A3 Cognitive Analysis Result Candidates v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_analysis_result_contract_types_v1 import (
    ALLOWED_ANALYSIS_TYPES_V1,
    FORBIDDEN_AUTHORITY_FLAGS_V1,
    CognitiveAnalysisResultCandidateV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisResultContractIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisResultContractValidationResultV1:
    issues: Tuple[CognitiveAnalysisResultContractIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_analysis_result_candidate_v1(
    candidate: CognitiveAnalysisResultCandidateV1,
) -> CognitiveAnalysisResultContractValidationResultV1:
    """Validate declared structure and authority only; never execute analysis or Runtime."""
    issues = []
    for field_ref, value in {
        "analysis_id": candidate.analysis_id,
        "input_reference": candidate.input_reference,
        "analysis_type": candidate.analysis_type,
    }.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisResultContractIssueV1(
                "required_field_missing", field_ref, f"{field_ref} must be non-empty"
            ))
    if not candidate.evidence_reference or not all(
        isinstance(reference, str) and reference.strip()
        for reference in candidate.evidence_reference
    ):
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "evidence_reference_missing", "evidence_reference", "at least one traceable evidence reference is required"
        ))
    if not isinstance(candidate.candidate_output, dict) or not candidate.candidate_output:
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "candidate_output_missing", "candidate_output", "candidate output must be explicitly present"
        ))
    if not isinstance(candidate.uncertainty, dict) or not candidate.uncertainty:
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "uncertainty_missing", "uncertainty", "uncertainty must remain explicit"
        ))
    if not isinstance(candidate.provenance, dict) or not candidate.provenance:
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "provenance_missing", "provenance", "provenance must remain explicit"
        ))
    if candidate.analysis_type not in ALLOWED_ANALYSIS_TYPES_V1:
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "analysis_type_not_allowed", "analysis_type", "only declared candidate analysis types are permitted"
        ))
    if candidate.confidence is not None and (
        not isinstance(candidate.confidence, (int, float)) or isinstance(candidate.confidence, bool)
        or not 0.0 <= float(candidate.confidence) <= 1.0
    ):
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "confidence_out_of_range", "confidence", "confidence is an optional candidate attribute in [0, 1]"
        ))
    if not isinstance(candidate.warning, tuple) or not all(
        isinstance(code, str) and code.strip() for code in candidate.warning
    ):
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "warning_invalid", "warning", "warning must be a tuple of stable non-empty codes"
        ))
    if not candidate.candidate_only or candidate.fact_status != "not_fact":
        issues.append(CognitiveAnalysisResultContractIssueV1(
            "candidate_boundary_violated", "candidate_only", "result must remain candidate-only and not_fact"
        ))
    for flag in FORBIDDEN_AUTHORITY_FLAGS_V1:
        if candidate.authority_flags.get(flag) is not False:
            issues.append(CognitiveAnalysisResultContractIssueV1(
                "forbidden_authority_present", f"authority_flags.{flag}", f"{flag} must be explicitly false"
            ))
    return CognitiveAnalysisResultContractValidationResultV1(tuple(issues))
