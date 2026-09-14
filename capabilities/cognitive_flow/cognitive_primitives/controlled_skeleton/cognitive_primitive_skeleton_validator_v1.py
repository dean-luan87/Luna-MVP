"""Static candidate boundary validator; it never invokes the primitive skeleton."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Mapping, Tuple

from .cognitive_primitive_skeleton_types_v1 import (
    COGNITIVE_PRIMITIVE_SKELETON_SCHEMA_VERSION_V1,
    PRIMITIVE_TYPES_V1,
    CognitivePrimitiveCandidateV1,
)


_FORBIDDEN_FIELD_NAMES_V1 = {
    "fact_id", "decision_id", "action_id", "state_write_target", "memory_target",
}


@dataclass(frozen=True)
class CognitivePrimitiveValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitivePrimitiveValidationResultV1:
    issues: Tuple[CognitivePrimitiveValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_primitive_candidate_v1(
    candidate: CognitivePrimitiveCandidateV1,
) -> CognitivePrimitiveValidationResultV1:
    """Validate schema, traceability, candidate-only and no-authority boundaries."""
    issues = []
    if candidate.schema_version != COGNITIVE_PRIMITIVE_SKELETON_SCHEMA_VERSION_V1:
        issues.append(CognitivePrimitiveValidationIssueV1(
            "schema_version_invalid", "schema_version", "unsupported primitive skeleton schema"
        ))
    if not candidate.primitive_id.strip() or candidate.primitive_type not in PRIMITIVE_TYPES_V1:
        issues.append(CognitivePrimitiveValidationIssueV1(
            "primitive_identity_invalid", "primitive_id", "primitive identity and type are required"
        ))
    for field_ref, refs in (("source_refs", candidate.source_refs), ("context_refs", candidate.context_refs)):
        if not refs or any(not isinstance(value, str) or not value.strip() for value in refs):
            issues.append(CognitivePrimitiveValidationIssueV1(
                "reference_missing", field_ref, f"{field_ref} must retain non-empty references"
            ))
    if not isinstance(candidate.provenance, Mapping) or not candidate.provenance.get("source_refs") or not candidate.provenance.get("trace_ref"):
        issues.append(CognitivePrimitiveValidationIssueV1(
            "provenance_missing", "provenance", "source and trace provenance are required"
        ))
    if not candidate.trace_ref.strip() or candidate.provenance.get("trace_ref") != candidate.trace_ref:
        issues.append(CognitivePrimitiveValidationIssueV1(
            "trace_missing_or_mismatched", "trace_ref", "trace must be retained end-to-end"
        ))
    if candidate.candidate_only is not True or candidate.fact_status != "not_fact":
        issues.append(CognitivePrimitiveValidationIssueV1(
            "candidate_fact_boundary", "fact_status", "primitive must remain candidate-only and not_fact"
        ))
    if not isinstance(candidate.uncertainty, Mapping):
        issues.append(CognitivePrimitiveValidationIssueV1(
            "uncertainty_invalid", "uncertainty", "uncertainty mapping is required"
        ))
    actual_fields = {item.name for item in fields(candidate)}
    forbidden = actual_fields & _FORBIDDEN_FIELD_NAMES_V1
    if forbidden:
        issues.append(CognitivePrimitiveValidationIssueV1(
            "forbidden_authority_field", ",".join(sorted(forbidden)), "authority fields are forbidden"
        ))
    return CognitivePrimitiveValidationResultV1(tuple(issues))
