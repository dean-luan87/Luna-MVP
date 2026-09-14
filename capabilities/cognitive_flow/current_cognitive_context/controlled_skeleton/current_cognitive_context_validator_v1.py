"""Static validator for Current Cognitive Context Candidate Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Tuple

from .current_cognitive_context_skeleton_types_v1 import (
    CURRENT_COGNITIVE_CONTEXT_SKELETON_SCHEMA_VERSION_V1,
    CurrentCognitiveContextCandidateV1,
    is_context_type_v1,
)


_REQUIRED_REFERENCE_FIELDS_V1 = (
    "context_id", "field_reference", "field_view_reference", "survival_context_reference",
    "task_context_reference", "attention_context_reference", "uncertainty_reference",
    "information_gap_reference", "spatial_scope_reference", "temporal_scope_reference",
    "experience_reference", "provenance_reference", "trace_reference",
)
_FORBIDDEN_AUTHORITY_FIELDS_V1 = frozenset((
    "fact_id", "state_id", "snapshot_write_target", "decision_id", "action_id", "permission_scope",
    "memory_target", "learning_target", "reducer_command", "state_write_target",
))


@dataclass(frozen=True)
class CurrentCognitiveContextValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CurrentCognitiveContextValidationResultV1:
    issues: Tuple[CurrentCognitiveContextValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def _valid_ref_v1(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_current_cognitive_context_candidate_v1(
    candidate: CurrentCognitiveContextCandidateV1,
) -> CurrentCognitiveContextValidationResultV1:
    """Validate schema and boundaries without resolving or generating context."""

    issues = []
    if candidate.schema_version != CURRENT_COGNITIVE_CONTEXT_SKELETON_SCHEMA_VERSION_V1:
        issues.append(CurrentCognitiveContextValidationIssueV1("schema_version_invalid", "schema_version", "known schema version required"))
    for field_name in _REQUIRED_REFERENCE_FIELDS_V1:
        if not _valid_ref_v1(getattr(candidate, field_name)):
            issues.append(CurrentCognitiveContextValidationIssueV1("reference_invalid", field_name, "non-empty declared reference required"))
    if not is_context_type_v1(candidate.context_type):
        issues.append(CurrentCognitiveContextValidationIssueV1("context_type_invalid", "context_type", "only frozen candidate context types are permitted"))
    if not all(getattr(candidate, name) is True for name in ("candidate_only", "not_fact", "not_state", "not_decision", "not_action", "not_memory")):
        issues.append(CurrentCognitiveContextValidationIssueV1("candidate_boundary_invalid", "candidate_only", "context must remain non-fact, non-state, non-decision, non-action, and non-memory"))
    forbidden = {item.name for item in fields(candidate)} & _FORBIDDEN_AUTHORITY_FIELDS_V1
    if forbidden:
        issues.append(CurrentCognitiveContextValidationIssueV1("forbidden_authority_field", ",".join(sorted(forbidden)), "authority-bearing fields are prohibited"))
    return CurrentCognitiveContextValidationResultV1(tuple(issues))
