"""Candidate-only contracts for the A-Route minimum cognitive view.

The view is a read-only selection over already governed information references.
It deliberately does not create Self, Field, Entity, Relation, or Goal truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)


VIEW_OWNER = "A-Route Cognitive Responsibility"
VIEW_SCHEMA_VERSION = "luna.a_route.minimum_relevant_cognitive_view.v1"
SELF_INFORMATION = "SELF"
EXTERNAL_INFORMATION = "EXTERNAL"
VIEW_FORMED = "VIEW_FORMED"
NO_ACTIVE_RELEVANT_VIEW = "NO_ACTIVE_RELEVANT_VIEW"
REJECTED = "REJECTED"


@dataclass(frozen=True)
class AvailableCognitiveInformationItemV1:
    """A governed information item eligible for common Self/External selection."""

    information_ref: str
    object_type: str
    information_kind: str
    support_condition_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    recoverable: bool = True
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.object_type not in {SELF_INFORMATION, EXTERNAL_INFORMATION}:
            raise ValueError("unsupported cognitive information object_type")
        if not self.information_ref.strip():
            raise ValueError("cognitive information ref is required")
        if not self.candidate_only:
            raise ValueError("available cognitive information must remain candidate-only")


@dataclass(frozen=True)
class ARouteMinimumRelevantCognitiveViewRequestV1:
    """Inputs to common Self/External relevance selection.

    Only explicit governed condition references may affect selection. Opaque
    context, goal, role, intent, and concern references are retained as
    provenance/conditioning context and are never parsed for meaning.
    """

    goal_context: GoalContextV1
    available_information: Tuple[AvailableCognitiveInformationItemV1, ...]
    governed_objective_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_role_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_intent_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_concern_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_context_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    intent_ref: str | None = None
    concern_ref: str | None = None
    context_ref: str | None = None
    field_ref: str | None = None
    role_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_world_ref: str | None = None
    current_cognitive_state_ref: str | None = None
    candidate_only: bool = True


@dataclass(frozen=True)
class ARouteMinimumRelevantCognitiveViewCandidateV1:
    """The minimum relevant view and recoverable exclusions."""

    view_ref: str
    owner_ref: str
    status: str
    goal_ref: str
    intent_ref: str | None
    concern_ref: str | None
    context_ref: str | None
    field_ref: str | None
    role_refs: Tuple[str, ...]
    current_world_ref: str | None
    current_cognitive_state_ref: str | None
    active_condition_refs: Tuple[str, ...]
    selected_information_refs: Tuple[str, ...]
    selected_self_information_refs: Tuple[str, ...]
    selected_external_information_refs: Tuple[str, ...]
    excluded_information_refs: Tuple[str, ...]
    recoverable_information_refs: Tuple[str, ...]
    current_cognitive_coverage_refs: Tuple[str, ...]
    selected_source_refs: Tuple[str, ...]
    selected_provenance_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    self_mutation: bool = False
    field_mutation: bool = False
    world_truth_declared: bool = False
    memory_mutation: bool = False
    pcn_mutation: bool = False
    decision_execution: bool = False
    task_execution: bool = False
    action_execution: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    observation_execution: bool = False
    observation_demand_formed: bool = False
    scenario_id_semantic_driver: bool = False
    opaque_context_semantic_guess: bool = False
    validation_errors: Tuple[str, ...] = ()
    schema_version: str = VIEW_SCHEMA_VERSION
