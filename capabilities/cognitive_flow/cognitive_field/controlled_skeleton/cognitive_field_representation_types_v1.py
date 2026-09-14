"""Immutable candidate-only types for the Cognitive Field Representation skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


COGNITIVE_FIELD_REPRESENTATION_SCHEMA_VERSION_V1 = (
    "luna.cognitive_field_representation.controlled_skeleton.v1"
)


@dataclass(frozen=True)
class CognitiveFieldRepresentationCandidateV1:
    """A scoped cognitive-query candidate; never Field State or a Snapshot writer."""

    field_candidate_id: str
    context_refs: Tuple[str, ...]
    snapshot_refs: Tuple[str, ...]
    primitive_refs: Tuple[str, ...]
    concept_refs: Tuple[str, ...]
    temporal_scope: Mapping[str, object]
    spatial_scope: Mapping[str, object]
    task_scope: Mapping[str, object]
    attention_scope: Mapping[str, object]
    relevance_partition: Mapping[str, Tuple[str, ...]]
    uncertainty: Mapping[str, object]
    provenance: Mapping[str, object]
    trace_ref: str
    candidate_status: str
    candidate_only: bool = True
    field_state: bool = False
    not_state: bool = True
    not_fact: bool = True
    schema_version: str = COGNITIVE_FIELD_REPRESENTATION_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveFieldRepresentationSkeletonFlagsV1:
    runtime_executed: bool = False
    model_invoked: bool = False
    provider_invoked: bool = False
    external_call: bool = False
    database_written: bool = False
    field_kernel_mutated: bool = False
    reducer_invoked: bool = False
    state_mutation: bool = False
    snapshot_updated: bool = False
    temporal_history_modified: bool = False
    fact_created: bool = False
    decision_created: bool = False
    action_created: bool = False
    memory_updated: bool = False
    learning_integrated: bool = False
