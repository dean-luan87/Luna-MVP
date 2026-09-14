"""Non-executing builder, validator, and serializer for Primitive candidates."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Mapping, Type

from .cognitive_primitive_skeleton_types_v1 import (
    PRIMITIVE_TYPES_V1,
    CognitivePrimitiveCandidateV1,
    CognitivePrimitiveSkeletonFlagsV1,
    EntityPrimitiveCandidateV1,
    EventPrimitiveCandidateV1,
    RelationPrimitiveCandidateV1,
    SituationPrimitiveCandidateV1,
    StatePrimitiveCandidateV1,
)
from .cognitive_primitive_skeleton_validator_v1 import (
    CognitivePrimitiveValidationResultV1,
    validate_cognitive_primitive_candidate_v1,
)


_TYPE_CLASS_V1: Mapping[str, Type[CognitivePrimitiveCandidateV1]] = {
    "entity_primitive_candidate": EntityPrimitiveCandidateV1,
    "relation_primitive_candidate": RelationPrimitiveCandidateV1,
    "state_primitive_candidate": StatePrimitiveCandidateV1,
    "event_primitive_candidate": EventPrimitiveCandidateV1,
    "situation_primitive_candidate": SituationPrimitiveCandidateV1,
}
_FORBIDDEN_INPUT_KEYS_V1 = {
    "fact_id", "decision_id", "action_id", "state_write_target", "memory_target",
}


class CognitivePrimitiveControlledSkeletonV1:
    """Creates only in-memory, candidate-only structures with no external behavior."""

    @staticmethod
    def create_candidate(value: Mapping[str, Any]) -> CognitivePrimitiveCandidateV1:
        if not isinstance(value, Mapping):
            raise ValueError("primitive candidate input must be a mapping")
        forbidden = set(value) & _FORBIDDEN_INPUT_KEYS_V1
        if forbidden:
            raise ValueError("forbidden authority field: " + ", ".join(sorted(forbidden)))
        primitive_type = value.get("primitive_type")
        if primitive_type not in PRIMITIVE_TYPES_V1:
            raise ValueError("unsupported primitive_type")
        required = ("primitive_id", "source_refs", "context_refs", "provenance", "uncertainty", "candidate_status", "trace_ref")
        missing = [name for name in required if name not in value]
        if missing:
            raise ValueError("missing required field: " + ", ".join(missing))
        if value.get("candidate_only", True) is not True or value.get("fact_status", "not_fact") != "not_fact":
            raise ValueError("primitive must remain candidate-only and not_fact")
        primitive_class = _TYPE_CLASS_V1[primitive_type]
        base = {
            "primitive_id": str(value["primitive_id"]),
            "primitive_type": primitive_type,
            "source_refs": tuple(value["source_refs"]),
            "context_refs": tuple(value["context_refs"]),
            "provenance": dict(value["provenance"]),
            "confidence": value.get("confidence"),
            "uncertainty": dict(value["uncertainty"]),
            "candidate_status": str(value["candidate_status"]),
            "trace_ref": str(value["trace_ref"]),
        }
        extras = {
            "entity_primitive_candidate": {"entity_kind": str(value.get("entity_kind", "unspecified_candidate")), "attributes": dict(value.get("attributes", {}))},
            "relation_primitive_candidate": {"subject_ref": str(value.get("subject_ref", "")), "predicate": str(value.get("predicate", "")), "object_ref": str(value.get("object_ref", ""))},
            "state_primitive_candidate": {"target_ref": str(value.get("target_ref", "")), "state_kind": str(value.get("state_kind", "unspecified_candidate")), "value": dict(value.get("value", {}))},
            "event_primitive_candidate": {"event_kind": str(value.get("event_kind", "unspecified_candidate")), "temporal_context": dict(value.get("temporal_context", {}))},
            "situation_primitive_candidate": {"situation_kind": str(value.get("situation_kind", "unspecified_candidate")), "member_refs": tuple(value.get("member_refs", ()))},
        }
        return primitive_class(**base, **extras[primitive_type])

    @staticmethod
    def validate_candidate(candidate: CognitivePrimitiveCandidateV1) -> CognitivePrimitiveValidationResultV1:
        return validate_cognitive_primitive_candidate_v1(candidate)

    @staticmethod
    def serialize_candidate(candidate: CognitivePrimitiveCandidateV1) -> str:
        return json.dumps(asdict(candidate), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def flags() -> CognitivePrimitiveSkeletonFlagsV1:
        return CognitivePrimitiveSkeletonFlagsV1()
