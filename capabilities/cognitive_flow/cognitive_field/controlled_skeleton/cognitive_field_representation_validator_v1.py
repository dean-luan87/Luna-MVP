"""Static validator; it does not invoke Field Kernel, Reducer, or runtime behavior."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Mapping, Tuple

from .cognitive_field_representation_types_v1 import (
    COGNITIVE_FIELD_REPRESENTATION_SCHEMA_VERSION_V1,
    CognitiveFieldRepresentationCandidateV1,
)


_FORBIDDEN_FIELD_NAMES_V1 = {
    "state_id", "snapshot_write_target", "fact_id", "decision_id", "action_id", "memory_target",
}
_ALLOWED_RELEVANCE_KEYS_V1 = {
    "primary_now", "peripheral_now", "deferred_candidate", "excluded_for_current_context_only",
}


@dataclass(frozen=True)
class CognitiveFieldRepresentationValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveFieldRepresentationValidationResultV1:
    issues: Tuple[CognitiveFieldRepresentationValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def _valid_refs_v1(value: object, required: bool = False) -> bool:
    if not isinstance(value, tuple):
        return False
    if required and not value:
        return False
    return all(isinstance(item, str) and item.strip() for item in value)


def validate_cognitive_field_representation_candidate_v1(
    candidate: CognitiveFieldRepresentationCandidateV1,
) -> CognitiveFieldRepresentationValidationResultV1:
    """Check structural, reference, trace, temporal/spatial, and candidate boundaries."""

    issues = []
    if candidate.schema_version != COGNITIVE_FIELD_REPRESENTATION_SCHEMA_VERSION_V1 or not candidate.field_candidate_id.strip():
        issues.append(CognitiveFieldRepresentationValidationIssueV1("schema_invalid", "field_candidate_id", "known schema and non-empty candidate identity required"))
    for name, value, required in (
        ("context_refs", candidate.context_refs, True),
        ("snapshot_refs", candidate.snapshot_refs, False),
        ("primitive_refs", candidate.primitive_refs, False),
        ("concept_refs", candidate.concept_refs, False),
    ):
        if not _valid_refs_v1(value, required):
            issues.append(CognitiveFieldRepresentationValidationIssueV1("reference_invalid", name, "reference tuple is malformed or required references are absent"))
    if not candidate.primitive_refs and not candidate.concept_refs:
        issues.append(CognitiveFieldRepresentationValidationIssueV1("cognitive_source_missing", "primitive_refs/concept_refs", "at least one candidate cognitive reference is required"))
    for name, scope in (
        ("temporal_scope", candidate.temporal_scope),
        ("spatial_scope", candidate.spatial_scope),
        ("task_scope", candidate.task_scope),
        ("attention_scope", candidate.attention_scope),
    ):
        if not isinstance(scope, Mapping) or not scope:
            issues.append(CognitiveFieldRepresentationValidationIssueV1("scope_invalid", name, "declared reference scope required; unknowns must remain explicit"))
    if not isinstance(candidate.relevance_partition, Mapping) or not candidate.relevance_partition or not set(candidate.relevance_partition).issubset(_ALLOWED_RELEVANCE_KEYS_V1):
        issues.append(CognitiveFieldRepresentationValidationIssueV1("relevance_partition_invalid", "relevance_partition", "only declared relevance classes are allowed"))
    elif any(not isinstance(refs, tuple) or any(not isinstance(ref, str) or not ref.strip() for ref in refs) for refs in candidate.relevance_partition.values()):
        issues.append(CognitiveFieldRepresentationValidationIssueV1("relevance_reference_invalid", "relevance_partition", "relevance entries must be valid reference tuples"))
    if not isinstance(candidate.uncertainty, Mapping):
        issues.append(CognitiveFieldRepresentationValidationIssueV1("uncertainty_invalid", "uncertainty", "explicit uncertainty mapping required"))
    if not isinstance(candidate.provenance, Mapping) or not candidate.provenance.get("source_refs") or candidate.provenance.get("trace_ref") != candidate.trace_ref:
        issues.append(CognitiveFieldRepresentationValidationIssueV1("traceability_invalid", "provenance", "source references and matching trace required"))
    if candidate.candidate_only is not True or candidate.field_state is not False or candidate.not_state is not True or candidate.not_fact is not True:
        issues.append(CognitiveFieldRepresentationValidationIssueV1("candidate_boundary_invalid", "candidate_only", "representation must remain candidate-only, not-state, and not-fact"))
    forbidden = {item.name for item in fields(candidate)} & _FORBIDDEN_FIELD_NAMES_V1
    if forbidden:
        issues.append(CognitiveFieldRepresentationValidationIssueV1("forbidden_authority_field", ",".join(sorted(forbidden)), "authority-bearing fields are prohibited"))
    return CognitiveFieldRepresentationValidationResultV1(tuple(issues))
