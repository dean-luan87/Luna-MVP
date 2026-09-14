"""Static boundary validator; it never invokes Concept Skeleton behavior."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Mapping, Tuple

from .cognitive_concept_types_v1 import CONCEPT_TYPES_V1, COGNITIVE_CONCEPT_SCHEMA_VERSION_V1, CognitiveConceptCandidateV1


_FORBIDDEN_V1 = {"fact_id", "decision_id", "action_id", "state_write_target", "memory_target", "learning_target"}


@dataclass(frozen=True)
class CognitiveConceptValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveConceptValidationResultV1:
    issues: Tuple[CognitiveConceptValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_concept_candidate_v1(candidate: CognitiveConceptCandidateV1) -> CognitiveConceptValidationResultV1:
    issues = []
    if candidate.schema_version != COGNITIVE_CONCEPT_SCHEMA_VERSION_V1 or candidate.concept_type not in CONCEPT_TYPES_V1 or not candidate.concept_id.strip():
        issues.append(CognitiveConceptValidationIssueV1("schema_invalid", "concept_id", "known concept identity/type required"))
    for name, value in (("primitive_refs", candidate.primitive_refs), ("context_refs", candidate.context_refs)):
        if not value or any(not isinstance(item, str) or not item.strip() for item in value):
            issues.append(CognitiveConceptValidationIssueV1("reference_missing", name, "non-empty references required"))
    if not isinstance(candidate.provenance, Mapping) or not candidate.provenance.get("source_refs") or candidate.provenance.get("trace_ref") != candidate.trace_ref:
        issues.append(CognitiveConceptValidationIssueV1("traceability_invalid", "provenance", "source and matching trace required"))
    if not candidate.semantic_description.strip() or not isinstance(candidate.uncertainty, Mapping):
        issues.append(CognitiveConceptValidationIssueV1("semantic_or_uncertainty_invalid", "semantic_description", "candidate semantics and uncertainty required"))
    if candidate.candidate_only is not True or candidate.fact_status != "not_fact":
        issues.append(CognitiveConceptValidationIssueV1("candidate_boundary_invalid", "fact_status", "Concept must remain candidate-only/not_fact"))
    forbidden = {item.name for item in fields(candidate)} & _FORBIDDEN_V1
    if forbidden:
        issues.append(CognitiveConceptValidationIssueV1("forbidden_authority_field", ",".join(sorted(forbidden)), "authority field forbidden"))
    return CognitiveConceptValidationResultV1(tuple(issues))

