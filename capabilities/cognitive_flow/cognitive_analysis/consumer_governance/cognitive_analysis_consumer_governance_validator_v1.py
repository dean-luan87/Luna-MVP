"""Pure structural validator for A3 Result Consumer Governance declarations v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_analysis_consumer_governance_types_v1 import (
    ALLOWED_CONSUMER_TYPES_V1,
    FORBIDDEN_ACCESS_V1,
    REQUIRED_READ_ACCESS_V1,
    CognitiveAnalysisConsumerGovernanceDeclarationV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisConsumerGovernanceIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisConsumerGovernanceValidationResultV1:
    issues: Tuple[CognitiveAnalysisConsumerGovernanceIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_analysis_consumer_governance_declaration_v1(
    declaration: CognitiveAnalysisConsumerGovernanceDeclarationV1,
) -> CognitiveAnalysisConsumerGovernanceValidationResultV1:
    """Validate identity, read-only permissions, trace, and authority without side effects."""
    issues = []
    for field_ref, value in {
        "consumer_id": declaration.consumer_id,
        "consumer_type": declaration.consumer_type,
        "source_result_reference": declaration.source_result_reference,
    }.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
                "consumer_identity_missing", field_ref, f"{field_ref} must be non-empty"
            ))
    if declaration.consumer_type not in ALLOWED_CONSUMER_TYPES_V1:
        issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
            "consumer_type_not_allowed", "consumer_type", "consumer type is outside this governance contract"
        ))
    if not set(REQUIRED_READ_ACCESS_V1).issubset(declaration.allowed_access):
        issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
            "required_read_access_missing", "allowed_access", "candidate, evidence, uncertainty, and provenance reads are required"
        ))
    if not set(FORBIDDEN_ACCESS_V1).issubset(declaration.forbidden_access):
        issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
            "forbidden_access_incomplete", "forbidden_access", "all mutation and execution prohibitions are required"
        ))
    if not declaration.required_evidence:
        issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
            "evidence_requirement_missing", "required_evidence", "consumer must require evidence references"
        ))
    if not declaration.required_trace:
        issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
            "trace_requirement_missing", "required_trace", "consumer must require trace/provenance"
        ))
    for authority in FORBIDDEN_ACCESS_V1:
        if declaration.authority_flags.get(authority) is not False:
            issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
                "forbidden_authority_present", f"authority_flags.{authority}", f"{authority} must be explicitly false"
            ))
    if declaration.runtime_authorized:
        issues.append(CognitiveAnalysisConsumerGovernanceIssueV1(
            "runtime_authorization_claimed", "runtime_authorized", "consumer governance cannot authorize Runtime"
        ))
    return CognitiveAnalysisConsumerGovernanceValidationResultV1(tuple(issues))
