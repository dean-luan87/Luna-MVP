"""Candidate-only lifecycle closure and Brain assimilation contracts.

These envelopes extend the existing Cognitive Flow Loop candidates.  They do
not create a lifecycle owner, mutate canonical state, or imply execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .cognitive_loop_continuity_candidate_types_v1 import (
    CognitiveOutcomeCandidateV1,
    LoopClosureRecordCandidateV1,
    LoopPackageReservationCandidateV1,
)


CLOSURE_REASONS = (
    "STOP_SUFFICIENT",
    "COGNITIVE_CONCERN_RESOLVED",
    "INTENT_SUPERSEDED",
    "TASK_OR_BEHAVIOR_COMPLETED",
    "CONTEXT_INVALIDATED_CONCERN",
    "BRAIN_GOVERNED_STOP",
    "RESOURCE_VALUE_TOO_LOW",
    "CONTINUITY_STALE",
    "UNRECOVERABLE_CAPABILITY_GAP",
    "SAFETY_GOVERNED_TERMINATION",
    "PARENT_SUPERSEDED_BY_BRANCH_OR_MERGE",
)

CLOSURE_LIFECYCLE_DISPOSITIONS = (
    "COMPLETED",
    "STOPPED",
    "SUPERSEDED",
    "ABANDONED_BY_VALUE",
    "FAILED",
)

ASSIMILATION_DISPOSITIONS = (
    "ACCEPT_AS_COGNITIVE_REFERENCE",
    "KEEP_AS_LOCAL_RESULT",
    "USE_FOR_REPLANNING",
    "FORWARD_TO_EXPERIENCE_GOVERNANCE",
    "DISCARD_AS_LOW_VALUE",
    "DEFER_ASSIMILATION",
)

REQUIREMENT_DISPOSITIONS = (
    "SUPERSEDED",
    "NOT_REQUIRED_AFTER_SUFFICIENCY",
    "CLOSED_STALE",
    "CLOSED",
    "DEFERRED",
    "BLOCKED",
)

OBSERVATION_DISPOSITIONS = (
    "NOT_REQUIRED_AFTER_SUFFICIENCY",
    "SUPERSEDED",
    "DEFERRED",
    "CLOSED",
)


@dataclass(frozen=True)
class ClosureAssessmentCandidateV1:
    """Loop-local evidence that closure may be worth asking governance to assess."""

    assessment_ref: str
    loop_id: str
    cognitive_concern_ref: str
    local_closure_state: str
    local_state_version_ref: str
    current_need_ref: Optional[str]
    closure_reason: str
    local_sufficiency_ref: Optional[str]
    evidence_refs: Tuple[str, ...]
    outstanding_requirement_refs: Tuple[str, ...]
    outstanding_observation_refs: Tuple[str, ...]
    suggested_lifecycle_disposition: str
    eligible_for_governance: bool
    closure_candidate_created: bool
    reason_refs: Tuple[str, ...]
    candidate_only: bool = True
    lifecycle_closure_accepted: bool = False
    loop_self_authorized_closure: bool = False


@dataclass(frozen=True)
class ClosureDecisionCandidateV1:
    """Brain/Cognitive Flow governance decision over a closure assessment."""

    decision_ref: str
    loop_id: str
    assessment_ref: str
    governing_owner_ref: str
    accepted: bool
    lifecycle_disposition: str
    closure_reason: str
    acceptance_state_version_ref: str
    decision_reason_refs: Tuple[str, ...]
    candidate_only: bool = True
    loop_self_authorized_closure: bool = False


@dataclass(frozen=True)
class FinalStateFreezeCandidateV1:
    """Bounded references frozen when Brain accepts lifecycle closure."""

    freeze_ref: str
    loop_id: str
    final_state_version_ref: str
    current_need_ref: Optional[str]
    need_lineage_refs: Tuple[str, ...]
    hypothesis_lineage_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    task_behavior_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    capability_path_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    requirement_dispositions: Tuple[Tuple[str, str], ...]
    observation_dispositions: Tuple[Tuple[str, str], ...]
    pending_candidate_dispositions: Tuple[Tuple[str, str], ...]
    final_state_frozen: bool
    candidate_only: bool = True
    authoritative_state_copied: bool = False


@dataclass(frozen=True)
class LifecycleClosureCandidateV1:
    """The accepted/rejected lifecycle transition, separate from its record."""

    lifecycle_closure_ref: str
    loop_id: str
    source_closure_state: str
    target_closure_state: str
    accepted: bool
    lifecycle_disposition: str
    closure_reason: str
    closure_decision_ref: str
    final_state_version_ref: str
    final_state_freeze_ref: Optional[str]
    outstanding_requirements_disposed: bool
    outstanding_observations_disposed: bool
    candidate_only: bool = True
    loop_self_authorized_closure: bool = False


@dataclass(frozen=True)
class LoopPackageCandidateV1:
    """Reference-only bounded package surface for an accepted closure."""

    package_ref: str
    reservation: LoopPackageReservationCandidateV1
    loop_id: str
    cognitive_concern_ref: str
    parent_loop_ref: Optional[str]
    derived_from_ref: Optional[str]
    final_lifecycle_disposition: str
    final_state_version_ref: str
    need_lineage_refs: Tuple[str, ...]
    hypothesis_lineage_refs: Tuple[str, ...]
    evidence_lineage_refs: Tuple[str, ...]
    capability_path_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    task_behavior_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    continuity_history_refs: Tuple[str, ...]
    pause_wait_resume_refs: Tuple[str, ...]
    closure_reason: str
    cognitive_outcome_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    semantic_compression: bool = False
    authoritative_state_copied: bool = False


@dataclass(frozen=True)
class BrainAssimilationCandidateV1:
    """Governed handoff from a Cognitive Outcome Candidate back to Brain."""

    assimilation_ref: str
    brain_subject_ref: str
    loop_id: str
    cognitive_outcome_ref: str
    closure_record_ref: str
    disposition: str
    source_state_version_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    world_truth_declared: bool = False
    decision_created: bool = False
    action_executed: bool = False
    intent_mutation: bool = False
    memory_mutation: bool = False
    experience_mutation: bool = False
    learning_executed: bool = False
    automatic_loop_generation: bool = False
    automatic_task_generation: bool = False


@dataclass(frozen=True)
class HistoryBoundaryCandidateV1:
    """Reference policy separating trace history, package, and future Experience."""

    history_ref: str
    loop_id: str
    runtime_trace_refs: Tuple[str, ...]
    closure_record_ref: str
    loop_package_ref: str
    future_experience_candidate_ref: Optional[str]
    runtime_history_preserved: bool
    package_is_bounded_handoff: bool
    future_reference_prefers_package: bool
    deep_audit_may_reference_trace: bool
    history_deleted: bool = False
    semantic_compression: bool = False
    experience_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class ClosureScenarioResultV1:
    scenario_id: str
    title: str
    closure_assessment: ClosureAssessmentCandidateV1
    closure_decision: ClosureDecisionCandidateV1
    lifecycle_closure: LifecycleClosureCandidateV1
    closure_record: Optional[LoopClosureRecordCandidateV1]
    cognitive_outcome: Optional[CognitiveOutcomeCandidateV1]
    final_state_freeze: Optional[FinalStateFreezeCandidateV1]
    loop_package: Optional[LoopPackageCandidateV1]
    assimilation: Optional[BrainAssimilationCandidateV1]
    history_boundary: HistoryBoundaryCandidateV1
    branch_reservation_present: bool
    parent_closed_by_reservation: bool
    child_loop_runtime_created: bool
    checks: Tuple[Tuple[str, bool], ...]
    negative_guards: Tuple[Tuple[str, bool], ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_execution: bool = False
    provider_invocation: bool = False


__all__ = [
    "CLOSURE_REASONS",
    "CLOSURE_LIFECYCLE_DISPOSITIONS",
    "ASSIMILATION_DISPOSITIONS",
    "REQUIREMENT_DISPOSITIONS",
    "OBSERVATION_DISPOSITIONS",
    "ClosureAssessmentCandidateV1",
    "ClosureDecisionCandidateV1",
    "FinalStateFreezeCandidateV1",
    "LifecycleClosureCandidateV1",
    "LoopPackageCandidateV1",
    "BrainAssimilationCandidateV1",
    "HistoryBoundaryCandidateV1",
    "ClosureScenarioResultV1",
]
