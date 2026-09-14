"""Pure structural validation for the A3 Evidence Context Adapter boundary v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_analysis_evidence_adapter_types_v1 import (
    FORBIDDEN_ADAPTER_OPERATION_FLAGS_V1,
    CognitiveAnalysisEvidenceContextAdapterCandidateV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisEvidenceContextAdapterIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisEvidenceContextAdapterValidationResultV1:
    issues: Tuple[CognitiveAnalysisEvidenceContextAdapterIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_analysis_evidence_context_adapter_candidate_v1(
    candidate: CognitiveAnalysisEvidenceContextAdapterCandidateV1,
) -> CognitiveAnalysisEvidenceContextAdapterValidationResultV1:
    """Validate references and boundary flags without resolving, invoking, or mutating anything."""
    issues = []
    for field_ref, value in {
        "adapter_request_id": candidate.adapter_request_id,
        "input_reference": candidate.input_reference,
        "context_reference": candidate.context_reference,
    }.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
                "input_reference_missing", field_ref, f"{field_ref} must be non-empty"
            ))
    if not candidate.evidence_references or not all(
        isinstance(reference, str) and reference.strip()
        for reference in candidate.evidence_references
    ):
        issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
            "evidence_reference_missing", "evidence_references", "at least one Evidence reference is required"
        ))
    if not isinstance(candidate.provenance, dict) or not candidate.provenance:
        issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
            "provenance_missing", "provenance", "provenance must be explicitly attached"
        ))
    else:
        for key in ("source_refs", "trace_ref"):
            value = candidate.provenance.get(key)
            if not value:
                issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
                    "provenance_incomplete", f"provenance.{key}", f"{key} is required"
                ))
    if not isinstance(candidate.normalized_reference_mapping, dict) or not candidate.normalized_reference_mapping:
        issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
            "normalization_mapping_missing", "normalized_reference_mapping", "reference mapping must be explicit"
        ))
    else:
        forbidden_payload_keys = {"raw_payload", "fact", "decision", "state", "memory"}
        if forbidden_payload_keys.intersection(candidate.normalized_reference_mapping):
            issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
                "normalization_boundary_violated", "normalized_reference_mapping", "only references may be normalized"
            ))
    if not candidate.candidate_only or candidate.fact_status != "not_fact":
        issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
            "candidate_boundary_violated", "candidate_only", "adapter output must remain candidate-only and not_fact"
        ))
    for flag in FORBIDDEN_ADAPTER_OPERATION_FLAGS_V1:
        if candidate.permission_flags.get(flag) is not False:
            issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
                "forbidden_operation_present", f"permission_flags.{flag}", f"{flag} must be explicitly false"
            ))
    if candidate.runtime_authorized:
        issues.append(CognitiveAnalysisEvidenceContextAdapterIssueV1(
            "runtime_authorization_claimed", "runtime_authorized", "Adapter cannot authorize Runtime"
        ))
    return CognitiveAnalysisEvidenceContextAdapterValidationResultV1(tuple(issues))
