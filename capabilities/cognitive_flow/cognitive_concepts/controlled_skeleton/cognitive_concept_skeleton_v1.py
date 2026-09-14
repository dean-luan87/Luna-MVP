"""Non-executing Concept Candidate builder, validator, and serializer."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Mapping

from .cognitive_concept_types_v1 import CONCEPT_TYPES_V1, CognitiveConceptCandidateV1, CognitiveConceptSkeletonFlagsV1
from .cognitive_concept_validator_v1 import CognitiveConceptValidationResultV1, validate_cognitive_concept_candidate_v1


_FORBIDDEN_INPUT_V1 = {"fact_id", "decision_id", "action_id", "state_write_target", "memory_target", "learning_target", "raw_model_payload", "image", "audio", "ocr_raw_result", "provider_output", "database_reference", "field_state_handle"}


class CognitiveConceptControlledSkeletonV1:
    """Builds declared Concept candidates only; it performs no pattern inference."""

    @staticmethod
    def create_concept_candidate(value: Mapping[str, Any]) -> CognitiveConceptCandidateV1:
        if not isinstance(value, Mapping): raise ValueError("concept input must be a mapping")
        forbidden = set(value) & _FORBIDDEN_INPUT_V1
        if forbidden: raise ValueError("forbidden input: " + ", ".join(sorted(forbidden)))
        required = ("concept_id", "concept_type", "primitive_refs", "pattern_refs", "context_refs", "semantic_description", "uncertainty", "provenance", "trace_ref", "candidate_status")
        missing = [name for name in required if name not in value]
        if missing: raise ValueError("missing required field: " + ", ".join(missing))
        if value.get("concept_type") not in CONCEPT_TYPES_V1: raise ValueError("unsupported concept_type")
        if value.get("candidate_only", True) is not True or value.get("fact_status", "not_fact") != "not_fact": raise ValueError("Concept must remain candidate-only/not_fact")
        return CognitiveConceptCandidateV1(concept_id=str(value["concept_id"]), concept_type=str(value["concept_type"]), primitive_refs=tuple(value["primitive_refs"]), pattern_refs=tuple(value["pattern_refs"]), context_refs=tuple(value["context_refs"]), semantic_description=str(value["semantic_description"]), confidence=value.get("confidence"), uncertainty=dict(value["uncertainty"]), provenance=dict(value["provenance"]), trace_ref=str(value["trace_ref"]), candidate_status=str(value["candidate_status"]))

    @staticmethod
    def validate_concept_candidate(candidate: CognitiveConceptCandidateV1) -> CognitiveConceptValidationResultV1:
        return validate_cognitive_concept_candidate_v1(candidate)

    @staticmethod
    def serialize_concept_candidate(candidate: CognitiveConceptCandidateV1) -> str:
        return json.dumps(asdict(candidate), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def flags() -> CognitiveConceptSkeletonFlagsV1:
        return CognitiveConceptSkeletonFlagsV1()
