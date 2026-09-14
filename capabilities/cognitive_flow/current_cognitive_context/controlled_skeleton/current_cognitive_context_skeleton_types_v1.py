"""Immutable candidate-only types for Current Cognitive Context Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass


CURRENT_COGNITIVE_CONTEXT_SKELETON_SCHEMA_VERSION_V1 = (
    "luna.current_cognitive_context.controlled_skeleton.v1"
)
_CONTEXT_TYPES_V1 = frozenset((
    "exploration_context",
    "navigation_context",
    "social_context",
    "task_context",
    "risk_awareness_context",
    "unknown_environment_context",
))


@dataclass(frozen=True)
class CurrentCognitiveContextCandidateV1:
    """A declared current cognitive stance; never Field State, Memory, Decision, or Action."""

    context_id: str
    context_type: str
    field_reference: str
    field_view_reference: str
    survival_context_reference: str
    task_context_reference: str
    attention_context_reference: str
    uncertainty_reference: str
    information_gap_reference: str
    spatial_scope_reference: str
    temporal_scope_reference: str
    experience_reference: str
    provenance_reference: str
    trace_reference: str
    candidate_only: bool = True
    not_fact: bool = True
    not_state: bool = True
    not_decision: bool = True
    not_action: bool = True
    not_memory: bool = True
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SKELETON_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CurrentCognitiveContextSkeletonFlagsV1:
    runtime_executed: bool = False
    context_inferred: bool = False
    model_invoked: bool = False
    external_call: bool = False
    field_kernel_integrated: bool = False
    reducer_integrated: bool = False
    state_mutation: bool = False
    decision_created: bool = False
    action_created: bool = False
    memory_updated: bool = False
    learning_integrated: bool = False
    hive_integrated: bool = False


def is_context_type_v1(value: str) -> bool:
    """Return whether a context classification belongs to the frozen v1 candidate set."""

    return value in _CONTEXT_TYPES_V1
