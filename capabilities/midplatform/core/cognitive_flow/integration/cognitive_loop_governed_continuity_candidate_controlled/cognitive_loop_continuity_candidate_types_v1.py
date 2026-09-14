"""Minimal candidate-only Loop envelope around existing Cognitive Flow types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import SourceRefV1
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_interrupt_types_v1 import (
    ResumeCandidateV1,
    SuspendCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveStateVersionCandidateV1,
    DynamicCognitiveLoopTransitionCandidateV1,
)


LOOP_LIFECYCLE_STATES = ("ACTIVE", "PAUSED", "WAITING", "DEFERRED", "STOPPED", "COMPLETED")
RESUME_DECISIONS = ("KEEP", "SUPERSEDE", "REPLAN", "COMPLETE", "WAITING")
CONTINUITY_SIGNALS = (
    "INTENT",
    "TASK_BEHAVIOR",
    "TEMPORAL",
    "SPATIAL",
    "FIELD",
    "ROLE_PERSPECTIVE",
)


@dataclass(frozen=True)
class LoopIdentityCandidateV1:
    """Concrete Loop process identity plus references to canonical owners."""

    loop_id: str
    cognitive_concern_ref: str
    goal_ref: str
    lineage_refs: Tuple[str, ...]
    parent_loop_ref: Optional[str]
    derived_from_ref: Optional[str]
    dependency_refs: Tuple[str, ...]
    shared_context_refs: Tuple[str, ...]
    inherited_evidence_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    current_state_version_ref: str
    current_need_ref: Optional[str]
    hypothesis_refs: Tuple[str, ...]
    expectation_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    task_behavior_refs: Tuple[str, ...]
    priority_refs: Tuple[str, ...]
    resource_envelope_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    emotion_modulation_refs: Tuple[str, ...]
    spatial_continuity_refs: Tuple[str, ...]
    temporal_continuity_refs: Tuple[str, ...]
    pending_candidate_refs: Tuple[str, ...]
    requirement_refs: Tuple[str, ...]
    observation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    lifecycle_state: str
    canonical_lifecycle_ref: str
    candidate_only: bool = True
    authoritative_state_duplicated: bool = False


@dataclass(frozen=True)
class LoopLocalStateCandidateV1:
    loop_id: str
    local_disposition: str
    current_minimum_need_ref: Optional[str]
    hypothesis_lineage_refs: Tuple[str, ...]
    pending_candidate_refs: Tuple[str, ...]
    state_versions: Tuple[CognitiveStateVersionCandidateV1, ...]
    transitions: Tuple[DynamicCognitiveLoopTransitionCandidateV1, ...]
    last_disposition: str
    pause_reason: Optional[str]
    waiting_reason: Optional[str]
    suspend_candidate: Optional[SuspendCandidateV1]
    local_sufficiency_ref: Optional[str]
    closure_state: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class LoopMaterializationCandidateV1:
    loop_id: str
    cognitive_concern_ref: str
    materialization_reason_refs: Tuple[str, ...]
    brain_subject_ref: str
    brain_materialization_authority_ref: str
    parallel_brain_path_candidate_ref: Optional[str]
    parallel_brain_path_blocked: bool
    non_duplication_guard_passed: bool
    materialization_allowed: bool
    candidate_only: bool = True
    runtime_materialization_executed: bool = False


@dataclass(frozen=True)
class ContinuityAssessmentCandidateV1:
    loop_id: str
    source_state_version_ref: str
    comparison_state_version_ref: str
    signal_status: Dict[str, str]
    signal_refs: Tuple[str, ...]
    changed_signal_refs: Tuple[str, ...]
    same_cognitive_concern_preserved: bool
    authoritative_comparison_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ResumeAssessmentCandidateV1:
    loop_id: str
    source_lifecycle_state: str
    continuity_assessment_ref: str
    source_state_version_ref: str
    comparison_state_version_ref: str
    current_need_ref: Optional[str]
    prior_requirement_refs: Tuple[str, ...]
    stale_requirement_refs: Tuple[str, ...]
    decision: str
    next_need_reassessment_ref: str
    resume_candidate: ResumeCandidateV1
    reconsideration_candidate: Optional[ReconsiderationCandidateV1]
    stale_requirement_forces_invocation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityCandidatePathV1:
    loop_id: str
    need_ref: str
    requirement_ref: str
    scope_ref: str
    resolution_ref: str
    resource_ref: str
    permission_ref: str
    safety_ref: str
    observation_admission_ref: str
    observation_candidate_ref: str
    requirement_state_version_ref: str
    path_status: str
    provider_invocation: bool = False
    model_inference: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityGrowthGuardCandidateV1:
    loop_id: str
    minimum_sufficient_cognition: bool
    resource_envelope_respected: bool
    sufficiency_threshold_respected: bool
    stale_requirement_blocked: bool
    diminishing_information_value_blocked: bool
    duplicate_requirement_blocked: bool
    growth_allowed: bool
    blocked_reason_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class BranchReservationCandidateV1:
    loop_id: str
    parent_loop_ref: Optional[str]
    derived_from_ref: Optional[str]
    dependency_refs: Tuple[str, ...]
    shared_context_refs: Tuple[str, ...]
    inherited_evidence_refs: Tuple[str, ...]
    branch_reason: Optional[str]
    supersede_ref: Optional[str]
    merge_candidate_ref: Optional[str]
    child_loop_runtime_created: bool = False
    autonomous_spawn: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class LoopClosureRecordCandidateV1:
    loop_id: str
    cognitive_concern_ref: str
    final_disposition: str
    final_state_version_ref: str
    need_lineage_refs: Tuple[str, ...]
    hypothesis_lineage_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    closure_reason_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveOutcomeCandidateV1:
    outcome_ref: str
    loop_id: str
    cognitive_concern_ref: str
    final_disposition: str
    final_state_version_ref: str
    closure_record_ref: str
    evidence_refs: Tuple[str, ...]
    sufficiency_reason_ref: str
    current_world_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    world_truth_declared: bool = False
    decision_created: bool = False
    action_executed: bool = False
    memory_mutation: bool = False
    experience_mutation: bool = False
    intent_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class LoopPackageReservationCandidateV1:
    loop_id: str
    runtime_trace_refs: Tuple[str, ...]
    closure_record_ref: str
    loop_package_ref: str
    experience_candidate_ref: str
    future_cognitive_prior_ref: Optional[str]
    package_runtime_executed: bool = False
    experience_governance_executed: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class ControlledLoopScenarioResultV1:
    scenario_id: str
    title: str
    loops: Tuple[LoopIdentityCandidateV1, ...]
    local_states: Tuple[LoopLocalStateCandidateV1, ...]
    materializations: Tuple[LoopMaterializationCandidateV1, ...]
    continuity_assessments: Tuple[ContinuityAssessmentCandidateV1, ...]
    resume_assessments: Tuple[ResumeAssessmentCandidateV1, ...]
    capability_paths: Tuple[CapabilityCandidatePathV1, ...]
    growth_guards: Tuple[CapabilityGrowthGuardCandidateV1, ...]
    closures: Tuple[LoopClosureRecordCandidateV1, ...]
    outcomes: Tuple[CognitiveOutcomeCandidateV1, ...]
    package_reservations: Tuple[LoopPackageReservationCandidateV1, ...]
    branch_reservations: Tuple[BranchReservationCandidateV1, ...]
    checks: Tuple[Dict[str, object], ...]
    negative_guards: Dict[str, bool]
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_execution: bool = False
    provider_invocation: bool = False
    scheduler_execution: bool = False
    autonomous_loop_spawn: bool = False


__all__ = [
    "LOOP_LIFECYCLE_STATES",
    "RESUME_DECISIONS",
    "CONTINUITY_SIGNALS",
    "LoopIdentityCandidateV1",
    "LoopLocalStateCandidateV1",
    "LoopMaterializationCandidateV1",
    "ContinuityAssessmentCandidateV1",
    "ResumeAssessmentCandidateV1",
    "CapabilityCandidatePathV1",
    "CapabilityGrowthGuardCandidateV1",
    "BranchReservationCandidateV1",
    "LoopClosureRecordCandidateV1",
    "CognitiveOutcomeCandidateV1",
    "LoopPackageReservationCandidateV1",
    "ControlledLoopScenarioResultV1",
]
