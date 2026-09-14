"""A-Route information-need formation adapter contracts.

The adapter in this module is intentionally smaller than a new Need ontology.
It consumes governed objective-condition and Current World coverage signals and
reuses ``CognitiveNeedCandidateV1`` for the candidate that it forms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)


FORMATION_OWNER = "A-Route Cognitive Responsibility"
FORMATION_SCHEMA_VERSION = "luna.a_route.information_need_formation.v1"
NEED_FORMED = "NEED_FORMED"
NO_ACTIVE_NEED = "NO_ACTIVE_NEED"
REJECTED = "REJECTED"


@dataclass(frozen=True)
class ARouteInformationNeedFormationRequestV1:
    """Read-only inputs for state-sensitive Need formation.

    ``goal_context.success_condition_refs`` and the optional condition tuples
    are governed condition signals, not predeclared Information Need refs.
    ``current_cognitive_coverage_refs`` is a read-only coverage projection of
    the supplied Current World; the adapter never derives meaning from opaque
    context or scenario identifiers.
    """

    goal_context: GoalContextV1
    current_world: CurrentWorldCandidateV1
    current_cognitive_coverage_refs: Tuple[str, ...] = field(default_factory=tuple)
    intent_ref: Optional[str] = None
    concern_ref: Optional[str] = None
    task_ref: Optional[str] = None
    context_ref: Optional[str] = None
    field_ref: Optional[str] = None
    role_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_role_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_objective_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    hypothesis_ref: Optional[str] = None
    attention_ref: Optional[str] = None
    urgency: str = "NORMAL"
    safety_relevance: str = "NONE"
    formation_trace_ref: Optional[str] = None
    candidate_only: bool = True


@dataclass(frozen=True)
class ARouteInformationNeedFormationResultV1:
    """Formation result, including the state-difference evidence."""

    status: str
    need: CognitiveNeedCandidateV1 | None
    owner_ref: str
    goal_ref: str
    intent_ref: Optional[str]
    concern_ref: Optional[str]
    task_ref: Optional[str]
    context_ref: Optional[str]
    field_ref: Optional[str]
    role_refs: Tuple[str, ...]
    current_world_ref: str
    current_world_trace_ref: str
    required_cognitive_condition_refs: Tuple[str, ...]
    current_cognitive_coverage_refs: Tuple[str, ...]
    necessary_unknown_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    goal_mutation: bool = False
    intent_mutation: bool = False
    concern_mutation: bool = False
    field_mutation: bool = False
    current_world_mutation: bool = False
    observation_demand_formed: bool = False
    capability_selection_executed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    world_truth_declared: bool = False
    memory_mutation: bool = False
    pcn_mutation: bool = False
    decision_execution: bool = False
    task_execution: bool = False
    action_execution: bool = False
    scenario_id_semantic_driver: bool = False
    opaque_context_semantic_guess: bool = False
    static_goal_need_lookup: bool = False
    schema_version: str = FORMATION_SCHEMA_VERSION
