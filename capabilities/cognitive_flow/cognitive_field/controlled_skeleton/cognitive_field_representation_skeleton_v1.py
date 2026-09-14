"""Non-executing builder, static validator, and serializer for Field Representation v1."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Mapping

from .cognitive_field_representation_types_v1 import (
    CognitiveFieldRepresentationCandidateV1,
    CognitiveFieldRepresentationSkeletonFlagsV1,
)
from .cognitive_field_representation_validator_v1 import (
    CognitiveFieldRepresentationValidationResultV1,
    validate_cognitive_field_representation_candidate_v1,
)


_FORBIDDEN_INPUT_FIELDS_V1 = {
    "state_id", "snapshot_write_target", "fact_id", "decision_id", "action_id", "memory_target",
    "raw_model_output", "provider_payload", "model_response", "memory", "fact", "decision", "action",
    "state_handle", "field_state_handle", "database_reference", "reducer_command",
}
_REQUIRED_INPUT_FIELDS_V1 = (
    "field_candidate_id", "context_refs", "snapshot_refs", "primitive_refs", "concept_refs",
    "temporal_scope", "spatial_scope", "task_scope", "attention_scope", "relevance_partition",
    "uncertainty", "provenance", "trace_ref", "candidate_status",
)


class CognitiveFieldRepresentationControlledSkeletonV1:
    """Creates a declared candidate envelope only; it performs no field composition or mutation."""

    @staticmethod
    def create_field_representation_candidate(value: Mapping[str, Any]) -> CognitiveFieldRepresentationCandidateV1:
        if not isinstance(value, Mapping):
            raise ValueError("field representation input must be a mapping")
        forbidden = set(value) & _FORBIDDEN_INPUT_FIELDS_V1
        if forbidden:
            raise ValueError("forbidden input: " + ", ".join(sorted(forbidden)))
        missing = [name for name in _REQUIRED_INPUT_FIELDS_V1 if name not in value]
        if missing:
            raise ValueError("missing required field: " + ", ".join(missing))
        if value.get("candidate_only", True) is not True or value.get("field_state", False) is not False or value.get("not_state", True) is not True or value.get("not_fact", True) is not True:
            raise ValueError("Field Representation must remain candidate-only, not-state, and not-fact")
        return CognitiveFieldRepresentationCandidateV1(
            field_candidate_id=str(value["field_candidate_id"]),
            context_refs=tuple(value["context_refs"]),
            snapshot_refs=tuple(value["snapshot_refs"]),
            primitive_refs=tuple(value["primitive_refs"]),
            concept_refs=tuple(value["concept_refs"]),
            temporal_scope=dict(value["temporal_scope"]),
            spatial_scope=dict(value["spatial_scope"]),
            task_scope=dict(value["task_scope"]),
            attention_scope=dict(value["attention_scope"]),
            relevance_partition={name: tuple(refs) for name, refs in value["relevance_partition"].items()},
            uncertainty=dict(value["uncertainty"]),
            provenance=dict(value["provenance"]),
            trace_ref=str(value["trace_ref"]),
            candidate_status=str(value["candidate_status"]),
        )

    @staticmethod
    def validate_field_representation_candidate(
        candidate: CognitiveFieldRepresentationCandidateV1,
    ) -> CognitiveFieldRepresentationValidationResultV1:
        return validate_cognitive_field_representation_candidate_v1(candidate)

    @staticmethod
    def serialize_field_representation_candidate(candidate: CognitiveFieldRepresentationCandidateV1) -> str:
        return json.dumps(asdict(candidate), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def flags() -> CognitiveFieldRepresentationSkeletonFlagsV1:
        return CognitiveFieldRepresentationSkeletonFlagsV1()
