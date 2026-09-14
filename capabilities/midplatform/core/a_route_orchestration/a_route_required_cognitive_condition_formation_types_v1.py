"""Thin contracts for governed Required Cognitive Condition formation.

This is an A-Route formation boundary, not a condition ontology.  Objective
governance supplies explicit rule semantics; A-Route evaluates those rules
against a minimum, read-only cognitive situation and returns candidate-only
currently-required conditions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)


FORMATION_OWNER = "A-Route Cognitive Responsibility"
FORMATION_SCHEMA_VERSION = "luna.a_route.required_cognitive_condition_formation.v1"
ACTIVE_REQUIRED = "ACTIVE_REQUIRED"
SATISFIED = "SATISFIED"
DORMANT = "DORMANT"
NO_ACTIVE_REQUIRED_CONDITIONS = "NO_ACTIVE_REQUIRED_CONDITIONS"
CONDITIONS_FORMED = "CONDITIONS_FORMED"
REJECTED = "REJECTED"


@dataclass(frozen=True)
class GovernedObjectiveConditionRuleV1:
    """Governed objective semantics consumed by the formation boundary.

    The rule is supplied by the objective/intent/concern governance owner.
    Its explicit references are evaluated as sets; no goal string, scenario,
    case identifier, or opaque context reference is interpreted by A-Route.
    """

    rule_ref: str
    condition_ref: str
    objective_refs: Tuple[str, ...]
    activation_all_refs: Tuple[str, ...] = field(default_factory=tuple)
    activation_any_refs: Tuple[str, ...] = field(default_factory=tuple)
    suppress_if_any_refs: Tuple[str, ...] = field(default_factory=tuple)
    satisfaction_coverage_refs: Tuple[str, ...] = field(default_factory=tuple)
    alternative_satisfaction_basis_refs: Tuple[str, ...] = field(default_factory=tuple)
    minimum_set_ref: str = ""
    selection_rank: int = 0
    source_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.rule_ref.strip() or not self.condition_ref.strip():
            raise ValueError("governed condition rule refs are required")
        if not self.objective_refs:
            raise ValueError("governed condition rule needs an objective ref")
        if self.selection_rank < 0:
            raise ValueError("condition selection rank cannot be negative")


@dataclass(frozen=True)
class CurrentCognitiveSituationV1:
    """Minimum selected situation signals available to condition formation."""

    current_cognitive_view_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_cognitive_coverage_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_world_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_world_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    self_information_refs: Tuple[str, ...] = field(default_factory=tuple)
    external_information_refs: Tuple[str, ...] = field(default_factory=tuple)
    role_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    context_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    field_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    intent_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    concern_condition_refs: Tuple[str, ...] = field(default_factory=tuple)

    def governed_refs(self) -> Tuple[str, ...]:
        """Return explicit situation signals without interpreting opaque refs."""

        return tuple(
            dict.fromkeys(
                ref
                for group in (
                    self.current_cognitive_coverage_refs,
                    self.current_world_condition_refs,
                    self.self_information_refs,
                    self.external_information_refs,
                    self.role_condition_refs,
                    self.context_condition_refs,
                    self.field_condition_refs,
                    self.intent_condition_refs,
                    self.concern_condition_refs,
                )
                for ref in group
                if ref and ref.strip()
            )
        )


@dataclass(frozen=True)
class ARouteRequiredCognitiveConditionFormationRequestV1:
    """Read-only inputs for state-sensitive condition formation."""

    goal_context: GoalContextV1
    governed_condition_rules: Tuple[GovernedObjectiveConditionRuleV1, ...]
    current_situation: CurrentCognitiveSituationV1
    intent_ref: str | None = None
    concern_ref: str | None = None
    context_ref: str | None = None
    field_ref: str | None = None
    role_refs: Tuple[str, ...] = field(default_factory=tuple)
    formation_trace_ref: str | None = None
    candidate_only: bool = True


@dataclass(frozen=True)
class RequiredCognitiveConditionCandidateV1:
    """One formed condition candidate and its governed evaluation status."""

    condition_ref: str
    source_objective_refs: Tuple[str, ...]
    conditioning_refs: Tuple[str, ...]
    status: str
    reason: str
    rule_ref: str
    satisfaction_status: str
    satisfaction_coverage_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    current_situation_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ARouteRequiredCognitiveConditionFormationResultV1:
    """Minimum currently-required condition set plus recoverable alternatives."""

    status: str
    owner_ref: str
    goal_ref: str
    intent_ref: str | None
    concern_ref: str | None
    context_ref: str | None
    field_ref: str | None
    role_refs: Tuple[str, ...]
    active_required_condition_refs: Tuple[str, ...]
    satisfied_condition_refs: Tuple[str, ...]
    dormant_condition_refs: Tuple[str, ...]
    candidates: Tuple[RequiredCognitiveConditionCandidateV1, ...]
    current_situation_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    goal_mutation: bool = False
    intent_mutation: bool = False
    concern_mutation: bool = False
    role_mutation: bool = False
    context_mutation: bool = False
    field_mutation: bool = False
    self_mutation: bool = False
    current_world_mutation: bool = False
    memory_mutation: bool = False
    pcn_mutation: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    observation_execution: bool = False
    observation_demand_formed: bool = False
    capability_selection_executed: bool = False
    decision_execution: bool = False
    task_execution: bool = False
    action_execution: bool = False
    scenario_id_semantic_driver: bool = False
    fixture_specific_mapping: bool = False
    static_goal_condition_lookup: bool = False
    opaque_context_semantic_guess: bool = False
    information_need_input_used: bool = False
    schema_version: str = FORMATION_SCHEMA_VERSION


__all__ = [
    "ACTIVE_REQUIRED",
    "CONDITIONS_FORMED",
    "CurrentCognitiveSituationV1",
    "DORMANT",
    "FORMATION_OWNER",
    "FORMATION_SCHEMA_VERSION",
    "GovernedObjectiveConditionRuleV1",
    "NO_ACTIVE_REQUIRED_CONDITIONS",
    "REJECTED",
    "RequiredCognitiveConditionCandidateV1",
    "ARouteRequiredCognitiveConditionFormationRequestV1",
    "ARouteRequiredCognitiveConditionFormationResultV1",
    "SATISFIED",
]
