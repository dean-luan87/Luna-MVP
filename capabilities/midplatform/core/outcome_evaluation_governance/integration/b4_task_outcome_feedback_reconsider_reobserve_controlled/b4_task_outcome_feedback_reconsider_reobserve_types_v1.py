"""B4 integration envelopes; canonical owners remain unchanged."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple

from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    ActionCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.outcome_evaluation_governance.outcome_evaluation_core_types_v1 import (
    ActualResultInputV1,
    ExpectedOutcomeInputV1,
    OutcomeEvaluationOutputV1,
)
from capabilities.midplatform.core.runtime_executor.execution_result_types_v1 import (
    ExecutionResultCandidateV1,
)


@dataclass(frozen=True)
class B3TaskDecisionReferenceV1:
    """Validated read-only reference to an already-produced B3 result."""

    case_id: str
    mode: str
    task_ref: str
    task_readiness_ref: str
    task_readiness: str
    decision_ref: str
    intent_refs: Tuple[str, ...]
    current_world_ref: str
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    observation_need_refs: Tuple[str, ...] = ()
    reconsideration_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    read_only: bool = True
    provider_invocation: bool = False
    task_mutation: bool = False


@dataclass(frozen=True)
class ControlledRuntimeResultCandidateV1:
    """Controlled result metadata; this is not an external runtime result."""

    result: ExecutionResultCandidateV1
    action_ref: str
    task_ref: str
    decision_ref: str
    runtime_request_ref: str
    controlled_fixture: bool = True
    real_runtime_execution: bool = False
    device_side_effect: bool = False
    scheduler_execution: bool = False
    candidate_only: bool = True
    provenance_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class TaskLifecycleFeedbackHandoffCandidateV1:
    """Feedback consumed by Task Manager; it does not mutate a Task."""

    feedback_id: str
    task_ref: str
    outcome_ref: str
    proposed_lifecycle_state: str
    feedback_kind: str
    reason_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    consumer_owner: str = "Task Manager"
    candidate_only: bool = True
    task_mutation_executed: bool = False
    external_success_verified: bool = False


@dataclass(frozen=True)
class ReobserveCandidateV1:
    """B4 integration reference to the canonical Observation Need handoff."""

    reobserve_id: str
    observation_need_ref: str
    evaluation_ref: str
    reason_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    consumer_owner: str = "Field Perception Orchestrator / Active Observation Control"
    candidate_only: bool = True
    provider_invocation: bool = False
    camera_activation: bool = False


@dataclass(frozen=True)
class B4ControlledRunResultV1:
    case_id: str
    mode: str
    source: B3TaskDecisionReferenceV1
    action_candidate: ActionCandidateV1
    controlled_runtime_result: ControlledRuntimeResultCandidateV1
    expected_outcome: ExpectedOutcomeInputV1
    actual_result: ActualResultInputV1
    outcome: OutcomeEvaluationOutputV1
    task_feedback: TaskLifecycleFeedbackHandoffCandidateV1
    reconsideration_candidate: Optional[ReconsiderationCandidateV1]
    reobserve_candidate: Optional[ReobserveCandidateV1]
    real_b3_task_input_accepted: bool
    task_lifecycle_owner_preserved: bool
    action_execution: bool = False
    runtime_execution: bool = False
    provider_invocation: bool = False
    automatic_retry: bool = False
    memory_write: bool = False
    experience_learning: bool = False
    online_learning: bool = False
    semantic_compression: bool = False
    dynamic_cognitive_function_execution: bool = False
    uncertainty_refs_preserved: bool = True
    conflict_refs_preserved: bool = True
    provenance_chain_complete: bool = True
    temporal_refs_preserved: bool = True
    synthetic_regression_preserved: bool = True
    differential_validation_passed: bool = True
    candidate_only: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
