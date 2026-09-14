from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


SCHEMA_VERSION = "a-route-product-loop-integration-schema-v1"
CONTRACT_VERSION = "a-route-product-loop-integration-contract-v1"
OWNER = "A Route Orchestration Governance"

STATES = (
    "IDLE", "INPUT_RECEIVED", "OBSERVATION_REQUIRED", "OBSERVING", "OBSERVATION_READY",
    "WORLD_CONTEXT_READY", "COGNITION_READY", "DECISION_READY", "TASK_READY", "ACTION_READY",
    "EXECUTION_PENDING", "EXECUTING", "RESULT_READY", "EVALUATING", "REOBSERVATION_REQUIRED",
    "RECONSIDERING", "NEXT_CYCLE_READY", "COMPLETED", "DEFERRED", "FAILED", "ABORTED",
)
FEEDBACK_ROUTES = ("COMPLETE", "NEXT_CYCLE", "REOBSERVE", "RECONSIDER", "DEFER", "FAIL")
OUTPUT_KINDS = ("RESPONSE", "GUIDANCE", "STATUS", "CLARIFICATION_REQUEST", "OBSERVATION_REQUIRED", "TASK_COMPLETED", "TASK_FAILED", "DEFERRED")
INGRESS_KINDS = ("USER_INPUT", "SYSTEM_EVENT", "TASK_CONTINUATION", "OBSERVATION_FEEDBACK", "USER_CORRECTION")


@dataclass(frozen=True)
class ProductLoopInputV1:
    scenario_id: str
    title: str
    ingress_kind: str
    source_ref: str
    information_need: str = ""
    requires_observation: bool = False
    observation_available: bool = True
    observation_sufficient: bool = True
    observation_modality: str = "NONE"
    provider_available: bool = True
    provider_failure: bool = False
    contradiction: bool = False
    stale_result: bool = False
    requires_action: bool = True
    runtime_available: bool = True
    execution_status: str = "SUCCEEDED"
    user_correction: bool = False
    task_cancelled: bool = False
    safety_interrupted: bool = False
    resource_constrained: bool = False
    unresolved_hypothesis: bool = False
    controlled_only_fallback: bool = False
    learning_signal: bool = False
    next_cycle_requested: bool = False
    previous_cycle_id: str = ""
    reconsideration_depth: int = 0
    reobservation_depth: int = 0
    max_reconsideration_depth: int = 2
    max_reobservation_depth: int = 2
    duplicate_kind: str = ""
    repeated_failure_signature: bool = False
    completed_cycle_probe: bool = False
    aborted_cycle_probe: bool = False
    no_hidden_retry_probe: bool = False
    deferred_workstream: str = ""
    correction_ref: str = ""
    synthetic_only: bool = True
    controlled_integration_only: bool = True
    candidate_only: bool = True
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class ProductCycleV1:
    cycle_id: str
    previous_cycle_id: str
    cycle_revision: int
    current_stage: str
    previous_stage: str
    pending_handoff: str
    observation_need_refs: Tuple[str, ...] = ()
    decision_ref: str = ""
    task_ref: str = ""
    action_ref: str = ""
    execution_result_ref: str = ""
    outcome_evaluation_ref: str = ""
    reconsideration_depth: int = 0
    reobservation_depth: int = 0
    failure_signatures: Tuple[str, ...] = ()
    correction_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    immutable: bool = False
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class ProductStageHandoffV1:
    stage_id: str
    producer_owner: str
    consumer_owner: str
    input_refs: Tuple[str, ...]
    output_refs: Tuple[str, ...]
    status: str
    handoff_contract_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    mutation_authority: bool = False
    candidate_only: bool = True
    runtime_handoff_ready: bool = False
    error_refs: Tuple[str, ...] = ()
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class RuntimeAdmissionCandidateV1:
    admission_id: str
    action_ref: str
    consumer_owner: str
    permission_ref: str
    resource_budget_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_authorized: bool = False
    provider_invocation: bool = False
    device_control: bool = False


@dataclass(frozen=True)
class ControlledExecutionRequestV1:
    execution_request_id: str
    admission_ref: str
    action_ref: str
    expected_outcome_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    real_execution: bool = False


@dataclass(frozen=True)
class ControlledExecutionResultV1:
    execution_result_id: str
    execution_request_ref: str
    status: str
    actual_result_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...] = ()
    failure_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    real_runtime_execution: bool = False
    external_reality_truth: bool = False


@dataclass(frozen=True)
class OutcomeFeedbackRouteV1:
    feedback_id: str
    evaluation_ref: str
    route: str
    reason_refs: Tuple[str, ...]
    observation_need_ref: str = ""
    reconsideration_ref: str = ""
    learning_signal_ref: str = ""
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    source_owner_mutation: bool = False


@dataclass(frozen=True)
class ObservationReentryCandidateV1:
    observation_need_id: str
    evaluation_ref: str
    information_need: str
    modality: str
    budget_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    provider_invocation: bool = False


@dataclass(frozen=True)
class ReconsiderationCandidateV1:
    reconsideration_id: str
    evaluation_ref: str
    reason: str
    depth_candidate: int
    max_depth: int
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    intent_mutation: bool = False
    decision_mutation: bool = False


@dataclass(frozen=True)
class NextCycleIngressV1:
    next_cycle_id: str
    previous_cycle_id: str
    source_feedback_ref: str
    ingress_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    starts_runtime: bool = False


@dataclass(frozen=True)
class ProductOutputCandidateV1:
    output_id: str
    output_kind: str
    content_ref: str
    source_cycle_id: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    user_delivery_executed: bool = False


@dataclass(frozen=True)
class ProductLoopTraceV1:
    root_cycle_trace_id: str
    stage_trace_refs: Tuple[str, ...]
    handoff_trace_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    reverse_lookup: Tuple[Tuple[str, Tuple[str, ...]], ...]
    correction_lineage: Tuple[str, ...] = ()
    error_refs: Tuple[str, ...] = ()
    provenance_grants_authority: bool = False


@dataclass(frozen=True)
class ProductLoopResultV1:
    scenario_id: str
    title: str
    state: str
    cycle: ProductCycleV1
    stages: Tuple[ProductStageHandoffV1, ...]
    runtime_admission: Optional[RuntimeAdmissionCandidateV1]
    execution_request: Optional[ControlledExecutionRequestV1]
    execution_result: Optional[ControlledExecutionResultV1]
    feedback: Optional[OutcomeFeedbackRouteV1]
    observation_reentry: Optional[ObservationReentryCandidateV1]
    reconsideration: Optional[ReconsiderationCandidateV1]
    next_cycle: Optional[NextCycleIngressV1]
    output: Optional[ProductOutputCandidateV1]
    trace: ProductLoopTraceV1
    error_refs: Tuple[str, ...] = ()
    guards: Dict[str, bool] = field(default_factory=dict)
    candidate_only: bool = True
    synthetic_only: bool = True
