"""Non-executing builder, validator, and canonical serializer for Context Skeleton v1."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Mapping

from .current_cognitive_context_skeleton_types_v1 import (
    CurrentCognitiveContextCandidateV1,
    CurrentCognitiveContextSkeletonFlagsV1,
)
from .current_cognitive_context_validator_v1 import (
    CurrentCognitiveContextValidationResultV1,
    validate_current_cognitive_context_candidate_v1,
)


_REQUIRED_INPUT_FIELDS_V1 = (
    "context_id", "context_type", "field_reference", "field_view_reference", "survival_context_reference",
    "task_context_reference", "attention_context_reference", "uncertainty_reference", "information_gap_reference",
    "spatial_scope_reference", "temporal_scope_reference", "experience_reference", "provenance_reference", "trace_reference",
)
_FORBIDDEN_INPUT_FIELDS_V1 = frozenset((
    "raw_model_output", "provider_payload", "memory", "fact", "decision", "action", "reducer_command",
    "state_mutation", "state_write_target", "fact_id", "state_id", "decision_id", "action_id",
    "permission_scope", "memory_target", "learning_target",
))
_BOUNDARY_FIELDS_V1 = ("candidate_only", "not_fact", "not_state", "not_decision", "not_action", "not_memory")


class CurrentCognitiveContextControlledSkeletonV1:
    """Creates a supplied reference envelope only; it never forms or changes context."""

    @staticmethod
    def create_candidate(value: Mapping[str, Any]) -> CurrentCognitiveContextCandidateV1:
        if not isinstance(value, Mapping):
            raise ValueError("context candidate input must be a mapping")
        forbidden = set(value) & _FORBIDDEN_INPUT_FIELDS_V1
        if forbidden:
            raise ValueError("forbidden input: " + ", ".join(sorted(forbidden)))
        missing = [name for name in _REQUIRED_INPUT_FIELDS_V1 if name not in value]
        if missing:
            raise ValueError("missing required field: " + ", ".join(missing))
        if any(value.get(name, True) is not True for name in _BOUNDARY_FIELDS_V1):
            raise ValueError("context candidate must remain candidate-only and non-authoritative")
        return CurrentCognitiveContextCandidateV1(**{name: str(value[name]) for name in _REQUIRED_INPUT_FIELDS_V1})

    @staticmethod
    def validate_candidate(candidate: CurrentCognitiveContextCandidateV1) -> CurrentCognitiveContextValidationResultV1:
        return validate_current_cognitive_context_candidate_v1(candidate)

    @staticmethod
    def serialize_candidate(candidate: CurrentCognitiveContextCandidateV1) -> str:
        return json.dumps(asdict(candidate), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def flags() -> CurrentCognitiveContextSkeletonFlagsV1:
        return CurrentCognitiveContextSkeletonFlagsV1()
