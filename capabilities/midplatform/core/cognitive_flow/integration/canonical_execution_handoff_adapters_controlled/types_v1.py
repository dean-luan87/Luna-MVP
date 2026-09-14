"""Local candidate records for canonical execution handoff seams."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.canonical_source_state_outcome_return_controlled.types_v1 import EdgeObservabilityCandidateV1
from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_types_v1 import ExecutableCapabilityCandidateV1, RuntimeAdmissionAssessmentCandidateV1


@dataclass(frozen=True)
class ACognitiveRequirementInputV1:
    concern_ref: Optional[str]
    reasoning_cycle_ref: Optional[str]
    cognitive_need_ref: Optional[str]
    cognitive_requirement_ref: Optional[str]
    target_ref: Optional[str]
    expected_evidence_refs: Tuple[str, ...]
    semantic_relevance_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    grant_ref: Optional[str]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    status: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class AttentionAllocationInputCandidateV1:
    allocation_ref: str
    allocation_version: str
    concern_ref: str
    reasoning_cycle_ref: str
    cognitive_need_ref: str
    cognitive_requirement_ref: str
    target_ref: str
    expected_evidence_refs: Tuple[str, ...]
    semantic_relevance_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    grant_ref: str
    priority_input_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Attention"
    responsibility_owner: str = "A→Attention handoff adapter"
    candidate_only: bool = True
    final_priority_assigned: bool = False
    need_mutated: bool = False
    attention_execution_executed: bool = False


@dataclass(frozen=True)
class RuntimeObservationInputV1:
    executable_candidate: Optional[ExecutableCapabilityCandidateV1]
    runtime_assessment: Optional[RuntimeAdmissionAssessmentCandidateV1]
    cognitive_requirement_ref: Optional[str]
    concern_ref: Optional[str]
    attention_refs: Tuple[str, ...]
    target_refs: Tuple[str, ...]
    focus_refs: Tuple[str, ...]
    grant_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    model_binding_ref: Optional[str]
    provider_binding_ref: Optional[str]
    expected_capability_ref: Optional[str]
    expected_model_binding_ref: Optional[str]
    expected_provider_binding_ref: Optional[str]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    permission_status: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationRequestCandidateV1:
    request_ref: str
    request_version: str
    concern_ref: str
    cognitive_requirement_ref: str
    executable_capability_ref: str
    capability_ref: str
    model_binding_ref: str
    provider_binding_ref: str
    attention_refs: Tuple[str, ...]
    target_refs: Tuple[str, ...]
    focus_refs: Tuple[str, ...]
    grant_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Observation"
    responsibility_owner: str = "Runtime→Observation handoff adapter"
    candidate_only: bool = True
    observation_execution_executed: bool = False
    provider_admission_executed: bool = False
    provider_invocation_executed: bool = False


@dataclass(frozen=True)
class DecisionActionInputV1:
    decision_ref: Optional[str]
    decision_version: Optional[str]
    decision_status: str
    concern_ref: Optional[str]
    intent_ref: Optional[str]
    action_type: Optional[str]
    target_ref: Optional[str]
    precondition_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    grant_refs: Tuple[str, ...]
    confirmation_refs: Tuple[str, ...]
    idempotency_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    bounded_direct: bool = True
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class TaskActionInputV1:
    task_ref: Optional[str]
    task_version: Optional[str]
    task_status: str
    source_decision_ref: Optional[str]
    action_type: Optional[str]
    target_ref: Optional[str]
    dependency_refs: Tuple[str, ...]
    blocker_refs: Tuple[str, ...]
    precondition_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    grant_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class ActionAdmissionInputCandidateV1:
    admission_input_ref: str
    admission_input_version: str
    source_kind: str
    decision_ref: Optional[str]
    task_ref: Optional[str]
    concern_ref: Optional[str]
    intent_ref: Optional[str]
    action_type: str
    target_ref: str
    precondition_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    grant_refs: Tuple[str, ...]
    confirmation_refs: Tuple[str, ...]
    idempotency_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Action Governance"
    responsibility_owner: str = "Decision/Task→Action handoff adapter"
    candidate_only: bool = True
    action_admission_executed: bool = False
    action_execution_executed: bool = False
    provider_admission_executed: bool = False
    provider_invocation_executed: bool = False


@dataclass(frozen=True)
class ActionResultInputV1:
    action_result_ref: Optional[str]
    action_result_version: Optional[str]
    task_ref: Optional[str]
    concern_ref: Optional[str]
    status: str
    progress_refs: Tuple[str, ...]
    completion_evidence_refs: Tuple[str, ...]
    effect_evidence_refs: Tuple[str, ...]
    failure_refs: Tuple[str, ...]
    source_state_update_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    partiality: str
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    synthetic_only: bool = True
    candidate_only: bool = True
    action_execution_executed: bool = False


@dataclass(frozen=True)
class TaskResultReturnCandidateV1:
    return_ref: str
    action_result_ref: str
    task_ref: str
    progress_refs: Tuple[str, ...]
    completion_evidence_refs: Tuple[str, ...]
    failure_refs: Tuple[str, ...]
    partiality: str
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Task"
    responsibility_owner: str = "Action Result→Task return adapter"
    candidate_only: bool = True
    task_completion_adjudicated: bool = False
    task_completed: bool = False


@dataclass(frozen=True)
class AReassessmentInputCandidateV1:
    reassessment_ref: str
    action_result_ref: str
    concern_ref: str
    task_ref: Optional[str]
    effect_evidence_refs: Tuple[str, ...]
    source_state_update_refs: Tuple[str, ...]
    failure_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    partiality: str
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "A"
    responsibility_owner: str = "Action Result→A reassessment adapter"
    candidate_only: bool = True
    a_sufficiency_set: bool = False
    concern_resolved: bool = False


@dataclass(frozen=True)
class HandoffEdgeV1:
    edge: EdgeObservabilityCandidateV1
    attention_execution_executed: bool = False
    observation_execution_executed: bool = False
    provider_admission_executed: bool = False
    provider_invocation_executed: bool = False
    action_admission_executed: bool = False
    action_execution_executed: bool = False
    runtime_execution_executed: bool = False
    source_mutation_executed: bool = False
    world_truth_declared: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class HandoffFailureV1:
    failure_ref: str
    classification: str
    reason: str
    responsible_owner: str
    semantic_consequence_owner: str
    global_consequence_owner: str
    next_target: str
    source_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...] = ()
    candidate_only: bool = True


@dataclass(frozen=True)
class HandoffOutputV1:
    output_kind: str
    output: Optional[Any]
    edge: HandoffEdgeV1
    failure: Optional[HandoffFailureV1]
