"""Candidate-only types for the minimum dynamic Cognitive Flow loop.

This module extends the existing Cognitive Flow owner with a small set of
references needed to express re-entry and early sufficiency.  It deliberately
does not model a world snapshot, a planner queue, or an execution runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CapabilityRequirementFormationCandidateV1,
    CognitiveNeedCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityInvocationCandidateV1,
    CapabilityOutcomeAssessmentV1,
    CapabilityResolutionCandidateV1,
)

from .cognitive_cycle_transition_types_v1 import ReconsiderationCandidateV1


COGNITIVE_DISPOSITIONS = ("SUFFICIENT", "INSUFFICIENT", "RECONSIDER", "DEFER")
SUFFICIENCY_STATUSES = ("SUFFICIENT", "INSUFFICIENT", "UNKNOWN")
NEXT_STEP_DISPOSITIONS = (
    "STOP_SUFFICIENT",
    "CONTINUE",
    "REPLAN",
    "DEFER",
    "REQUEST_MORE_EVIDENCE",
)
CAPABILITY_AVAILABILITY = ("AVAILABLE", "DEGRADED", "UNAVAILABLE")


@dataclass(frozen=True)
class CognitiveGoalCandidateV1:
    """A goal reference used for sufficiency evaluation, never execution."""

    goal_ref: str
    goal_statement_candidate: str
    success_condition_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    execution_commitment: bool = False


@dataclass(frozen=True)
class ProvisionalPlanCandidateV1:
    """An ordered set of possible steps, not an execution queue."""

    plan_ref: str
    goal_ref: str
    candidate_step_refs: Tuple[str, ...]
    plan_completeness_status: str
    trace_ref: str
    candidate_only: bool = True
    execution_queue: bool = False
    binding: bool = False


@dataclass(frozen=True)
class CognitiveStateVersionCandidateV1:
    """A versioned cognitive disposition with reference-only lineage."""

    state_version_ref: str
    parent_state_version_ref: Optional[str]
    evidence_update_ref: Optional[str]
    current_disposition: str
    current_minimum_need_ref: Optional[str]
    active_hypothesis_refs: Tuple[str, ...]
    invalidated_hypothesis_refs: Tuple[str, ...]
    sufficiency_ref: Optional[str]
    reconsideration_ref: Optional[str]
    trace_ref: str
    candidate_only: bool = True
    state_mutation_executed: bool = False


@dataclass(frozen=True)
class CognitiveEvidenceUpdateCandidateV1:
    """Evidence/outcome input that can revise the next cognitive step."""

    evidence_update_ref: str
    source_state_version_ref: str
    evidence_refs: Tuple[str, ...]
    evidence_kind: str
    establishes_goal_sufficiency: bool = False
    invalidates_hypothesis: bool = False
    replacement_hypothesis_refs: Tuple[str, ...] = ()
    replacement_need_ref: Optional[str] = None
    capability_result_ref: Optional[str] = None
    execution_outcome: Optional[str] = None
    requirement_satisfaction: Optional[str] = None
    task_contribution: Optional[str] = None
    capability_availability: Optional[str] = None
    trace_ref: str = ""
    candidate_only: bool = True


@dataclass(frozen=True)
class GoalSufficiencyCandidateV1:
    """Goal-level sufficiency, intentionally separate from capability outcome."""

    sufficiency_ref: str
    goal_ref: str
    state_version_ref: str
    status: str
    evidence_refs: Tuple[str, ...]
    reason: str
    stop_disposition: str
    terminates_remaining_plan: bool
    candidate_only: bool = True
    failure: bool = False


@dataclass(frozen=True)
class DynamicCognitiveLoopTransitionCandidateV1:
    """One candidate transition in the dynamic loop."""

    transition_ref: str
    source_state_version_ref: str
    target_state_version_ref: str
    source_disposition: str
    target_disposition: str
    next_step_disposition: str
    current_minimum_need_ref: Optional[str]
    selected_next_need_ref: Optional[str]
    superseded_requirement_refs: Tuple[str, ...]
    non_materialized_plan_refs: Tuple[str, ...]
    related_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    runtime_transition_executed: bool = False
    owner_mutation: bool = False


@dataclass(frozen=True)
class DynamicCognitiveLoopInputV1:
    """Reference-only input for a bounded, synthetic cognitive loop."""

    scenario_id: str
    goal: CognitiveGoalCandidateV1
    provisional_plan: ProvisionalPlanCandidateV1
    initial_state_version_ref: str
    initial_disposition: str
    initial_hypothesis_refs: Tuple[str, ...]
    initial_minimum_need_ref: Optional[str]
    evidence_updates: Tuple[CognitiveEvidenceUpdateCandidateV1, ...]
    needs: Tuple[CognitiveNeedCandidateV1, ...] = field(default_factory=tuple)
    requirements: Tuple[CapabilityRequirementFormationCandidateV1, ...] = field(default_factory=tuple)
    resolutions: Tuple[CapabilityResolutionCandidateV1, ...] = field(default_factory=tuple)
    invocations: Tuple[CapabilityInvocationCandidateV1, ...] = field(default_factory=tuple)
    capability_outcomes: Tuple[CapabilityOutcomeAssessmentV1, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class DynamicCognitiveLoopOutputV1:
    """Candidate-only output for STOP/CONTINUE/REPLAN/DEFER."""

    scenario_id: str
    goal: CognitiveGoalCandidateV1
    provisional_plan: ProvisionalPlanCandidateV1
    state_versions: Tuple[CognitiveStateVersionCandidateV1, ...]
    transitions: Tuple[DynamicCognitiveLoopTransitionCandidateV1, ...]
    needs_materialized: Tuple[str, ...]
    current_minimum_need_ref: Optional[str]
    requirement_refs: Tuple[str, ...]
    resolution_refs: Tuple[str, ...]
    invocation_candidate_refs: Tuple[str, ...]
    eligible_invocation_refs: Tuple[str, ...]
    stale_requirement_refs: Tuple[str, ...]
    capability_outcome_refs: Tuple[str, ...]
    sufficiency_candidates: Tuple[GoalSufficiencyCandidateV1, ...]
    reconsiderations: Tuple[ReconsiderationCandidateV1, ...]
    evidence_update_refs: Tuple[str, ...]
    ignored_evidence_update_refs: Tuple[str, ...]
    non_materialized_plan_refs: Tuple[str, ...]
    final_disposition: str
    next_step_disposition: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_execution: bool = False
    provider_invocation: bool = False
    camera_activation: bool = False
    scheduler_execution: bool = False
    owner_mutation: bool = False
    capability_failure_is_task_failure: bool = False
    stop_sufficient_not_failure: bool = True
