"""Non-executing controlled skeleton for Minimum Sufficient Field Understanding v1."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Mapping

from .minimum_sufficient_field_understanding_types_v1 import (
    BehaviorBoundaryCandidateV1,
    MinimumSufficientFieldUnderstandingCandidateV1,
    MinimumSufficientFieldUnderstandingSkeletonFlagsV1,
)
from .minimum_sufficient_field_understanding_validator_v1 import (
    MinimumSufficientFieldUnderstandingValidationResultV1,
    validate_minimum_sufficient_field_understanding_candidate_v1,
)


_REQUIRED_INPUT_FIELDS_V1 = (
    "field_reference", "identity_status", "constraint_reference", "behavior_boundary", "information_gap",
    "uncertainty", "temporal_scope", "spatial_scope", "task_reference", "provenance", "trace_ref", "candidate_status",
)
_FORBIDDEN_INPUT_FIELDS_V1 = frozenset((
    "raw_model_output", "provider_payload", "action_command", "decision_output", "fact_store", "memory",
    "learning", "reducer_command", "state_mutation", "state_write_target", "fact_id", "decision_id",
    "action_id", "memory_target", "learning_target", "permission_scope",
))
_BOUNDARY_FIELDS_V1 = ("candidate_only", "not_fact", "not_state", "not_decision", "not_action")


class MinimumSufficientFieldUnderstandingControlledSkeletonV1:
    """Build, validate, and canonically serialize a declared candidate only."""

    @staticmethod
    def create_candidate(value: Mapping[str, Any]) -> MinimumSufficientFieldUnderstandingCandidateV1:
        if not isinstance(value, Mapping):
            raise ValueError("minimum sufficient field understanding input must be a mapping")
        forbidden = set(value) & _FORBIDDEN_INPUT_FIELDS_V1
        if forbidden:
            raise ValueError("forbidden input: " + ", ".join(sorted(forbidden)))
        missing = [name for name in _REQUIRED_INPUT_FIELDS_V1 if name not in value]
        if missing:
            raise ValueError("missing required field: " + ", ".join(missing))
        if any(value.get(name, True) is not True for name in _BOUNDARY_FIELDS_V1):
            raise ValueError("candidate must remain not-fact, not-state, not-decision, and not-action")
        boundary = value["behavior_boundary"]
        if not isinstance(boundary, Mapping):
            raise ValueError("behavior_boundary must be a mapping")
        boundary_required = ("allowed_behavior_candidate", "forbidden_behavior_candidate", "risk_boundary", "exploration_boundary")
        missing_boundary = [name for name in boundary_required if name not in boundary]
        if missing_boundary:
            raise ValueError("missing behavior_boundary field: " + ", ".join(missing_boundary))
        return MinimumSufficientFieldUnderstandingCandidateV1(
            field_reference=str(value["field_reference"]),
            identity_status=str(value["identity_status"]),
            constraint_reference=str(value["constraint_reference"]),
            behavior_boundary=BehaviorBoundaryCandidateV1(
                allowed_behavior_candidate=tuple(boundary["allowed_behavior_candidate"]),
                forbidden_behavior_candidate=tuple(boundary["forbidden_behavior_candidate"]),
                risk_boundary=dict(boundary["risk_boundary"]),
                exploration_boundary=dict(boundary["exploration_boundary"]),
            ),
            information_gap=tuple(value["information_gap"]),
            uncertainty=dict(value["uncertainty"]),
            temporal_scope=dict(value["temporal_scope"]),
            spatial_scope=dict(value["spatial_scope"]),
            task_reference=str(value["task_reference"]),
            provenance=dict(value["provenance"]),
            trace_ref=str(value["trace_ref"]),
            candidate_status=str(value["candidate_status"]),
        )

    @staticmethod
    def validate_candidate(candidate: MinimumSufficientFieldUnderstandingCandidateV1) -> MinimumSufficientFieldUnderstandingValidationResultV1:
        return validate_minimum_sufficient_field_understanding_candidate_v1(candidate)

    @staticmethod
    def serialize_candidate(candidate: MinimumSufficientFieldUnderstandingCandidateV1) -> str:
        return json.dumps(asdict(candidate), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def flags() -> MinimumSufficientFieldUnderstandingSkeletonFlagsV1:
        return MinimumSufficientFieldUnderstandingSkeletonFlagsV1()
