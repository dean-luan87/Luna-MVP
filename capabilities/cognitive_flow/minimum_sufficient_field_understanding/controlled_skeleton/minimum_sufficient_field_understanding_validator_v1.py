"""Static validation for Minimum Sufficient Field Understanding candidates only."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Mapping, Tuple

from .minimum_sufficient_field_understanding_types_v1 import (
    MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_SCHEMA_VERSION_V1,
    MinimumSufficientFieldUnderstandingCandidateV1,
    is_identity_status_v1,
)


_FORBIDDEN_AUTHORITY_FIELDS_V1 = frozenset((
    "fact_id", "decision_id", "action_id", "action_command", "permission_scope",
    "state_write_target", "reducer_command", "memory_target", "learning_target",
))


@dataclass(frozen=True)
class MinimumSufficientFieldUnderstandingValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class MinimumSufficientFieldUnderstandingValidationResultV1:
    issues: Tuple[MinimumSufficientFieldUnderstandingValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def _valid_ref_v1(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_ref_tuple_v1(value: object) -> bool:
    return isinstance(value, tuple) and all(_valid_ref_v1(item) for item in value)


def validate_minimum_sufficient_field_understanding_candidate_v1(
    candidate: MinimumSufficientFieldUnderstandingCandidateV1,
) -> MinimumSufficientFieldUnderstandingValidationResultV1:
    """Validate structure and candidate-only authority boundaries without execution."""

    issues = []
    if candidate.schema_version != MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_SCHEMA_VERSION_V1:
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("schema_version_invalid", "schema_version", "known schema version required"))
    for name, value in (("field_reference", candidate.field_reference), ("constraint_reference", candidate.constraint_reference), ("task_reference", candidate.task_reference), ("trace_ref", candidate.trace_ref), ("candidate_status", candidate.candidate_status)):
        if not _valid_ref_v1(value):
            issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("reference_invalid", name, "non-empty reference required"))
    if not is_identity_status_v1(candidate.identity_status):
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("identity_status_invalid", "identity_status", "only known, partially_known, or unknown are permitted"))
    boundary = candidate.behavior_boundary
    if not _valid_ref_tuple_v1(boundary.allowed_behavior_candidate) or not _valid_ref_tuple_v1(boundary.forbidden_behavior_candidate):
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("behavior_candidate_invalid", "behavior_boundary", "behavior candidates must be reference tuples"))
    for name, value in (("risk_boundary", boundary.risk_boundary), ("exploration_boundary", boundary.exploration_boundary), ("uncertainty", candidate.uncertainty), ("temporal_scope", candidate.temporal_scope), ("spatial_scope", candidate.spatial_scope)):
        if not isinstance(value, Mapping) or not value:
            issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("scope_invalid", name, "explicit mapping required; unknowns remain explicit"))
    if not _valid_ref_tuple_v1(candidate.information_gap):
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("information_gap_invalid", "information_gap", "information gaps must remain reference tuples"))
    if not isinstance(candidate.provenance, Mapping) or not candidate.provenance.get("source_refs") or candidate.provenance.get("trace_ref") != candidate.trace_ref:
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("traceability_invalid", "provenance", "source references and matching trace required"))
    if (candidate.candidate_only is not True or candidate.not_fact is not True or candidate.not_state is not True or candidate.not_decision is not True or candidate.not_action is not True):
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("candidate_boundary_invalid", "candidate_only", "candidate must remain not-fact, not-state, not-decision, and not-action"))
    forbidden = {item.name for item in fields(candidate)} & _FORBIDDEN_AUTHORITY_FIELDS_V1
    if forbidden:
        issues.append(MinimumSufficientFieldUnderstandingValidationIssueV1("forbidden_authority_field", ",".join(sorted(forbidden)), "authority-bearing fields are prohibited"))
    return MinimumSufficientFieldUnderstandingValidationResultV1(tuple(issues))
