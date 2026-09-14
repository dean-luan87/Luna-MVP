"""Immutable candidate-only types for the A3 Cognitive Concept skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


COGNITIVE_CONCEPT_SCHEMA_VERSION_V1 = "luna.cognitive_concept.controlled_skeleton.v1"
CONCEPT_TYPES_V1 = (
    "pattern_concept_candidate", "situation_concept_candidate",
    "relationship_concept_candidate", "context_concept_candidate",
    "risk_candidate_concept", "goal_candidate_concept",
)


@dataclass(frozen=True)
class CognitiveConceptCandidateV1:
    concept_id: str
    concept_type: str
    primitive_refs: Tuple[str, ...]
    pattern_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    semantic_description: str
    confidence: float | None
    uncertainty: Mapping[str, object]
    provenance: Mapping[str, object]
    trace_ref: str
    candidate_status: str
    candidate_only: bool = True
    fact_status: str = "not_fact"
    schema_version: str = COGNITIVE_CONCEPT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveConceptSkeletonFlagsV1:
    runtime_executed: bool = False
    model_invoked: bool = False
    external_call: bool = False
    database_written: bool = False
    field_kernel_mutated: bool = False
    reducer_invoked: bool = False
    fact_created: bool = False
    decision_created: bool = False
    action_created: bool = False
    state_writeback: bool = False
    memory_updated: bool = False
    learning_integrated: bool = False

