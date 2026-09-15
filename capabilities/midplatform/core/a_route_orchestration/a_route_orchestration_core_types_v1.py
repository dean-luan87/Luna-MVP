from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Tuple

from capabilities.midplatform.core.execution_mode_v1 import (
    SYNTHETIC_CONTROLLED,
    ControlledReplayAdmissionV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    CognitiveInformationGapCandidateV1,
    CognitiveReobservationCandidateV1,
    CognitiveSufficiencyCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    CognitiveReferenceSemanticV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_conditioning_types_v1 import (
    CognitiveRelationInterpretationCandidateV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationGatewayRuntimeAdmissionV1,
)
if TYPE_CHECKING:
    from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
        ARouteRequiredCognitiveConditionFormationResultV1,
    )

SCHEMA_VERSION = "a-route-orchestration-schema-v1"
CONTRACT_VERSION = "a-route-orchestration-contract-v1"

LIFECYCLE_STAGES = (
    "IDLE",
    "INGRESS_READY",
    "CONTEXT_READY",
    "PCN_READY",
    "INTENT_READY",
    "COGNITIVE_STATE_READY",
    "REGULATION_READY",
    "DECISION_READY",
    "TASK_READY",
    "ACTION_READY",
    "EXECUTION_READY",
    "RESULT_READY",
    "FEEDBACK_READY",
    "MEMORY_EXPERIENCE_READY",
    "LEARNING_READY",
    "SELF_CONTINUITY_READY",
    "PERSONALITY_CONTEXT_READY",
    "CYCLE_COMPLETE",
)
CONTROL_STATES = ("STOPPED", "DEFERRED", "RECONSIDERING", "FAILED", "SUSPENDED")
HANDOFF_STATUSES = (
    "CONTRACT_AVAILABLE",
    "ADAPTER_AVAILABLE",
    "CONTROLLED_HANDOFF_READY",
    "RUNTIME_HANDOFF_READY",
    "BLOCKED",
    "DEFERRED",
)


@dataclass(frozen=True)
class ARouteStageResultV1:
    stage_id: str
    producer_owner: str
    consumer_owner: str
    input_refs: Tuple[str, ...]
    output_refs: Tuple[str, ...]
    handoff_contract_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    status: str
    stop_reason: str = ""
    defer_reason: str = ""
    error_ref: str = ""
    reconsideration_ref: str = ""
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class ARouteHandoffRecordV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    status: str
    contract_ref: str
    adapter_ref: str
    controlled_handoff_ready: bool
    runtime_handoff_ready: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...]


@dataclass(frozen=True)
class ARouteIngressRefsV1:
    observation_refs: Tuple[str, ...] = ()
    perception_refs: Tuple[str, ...] = ()
    user_input_refs: Tuple[str, ...] = ()
    field_refs: Tuple[str, ...] = ()
    relation_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ARouteCognitiveExecutionEvidenceV1:
    """Canonical proof emitted by A-Route after Cognitive State Formation runs."""

    execution_ref: str
    execution_mode: str
    owner_ref: str
    ingress_refs: Tuple[str, ...]
    cognitive_transition_refs: Tuple[str, ...]
    current_world_ref: str | None
    hypothesis_refs: Tuple[str, ...]
    current_world_availability: str
    hypothesis_availability: str
    sufficiency_ref: str | None
    sufficiency_availability: str
    information_gap_ref: str | None
    information_gap_availability: str
    stop_ref: str | None
    stop_availability: str
    decision_handoff_ref: str | None
    decision_handoff_availability: str
    runtime_executed: bool
    candidate_only: bool = True
    field_mutation: bool = False
    world_truth_declared: bool = False
    model_invocation: bool = False
    provider_invocation: bool = False
    live_observation_execution: bool = False
    action_execution: bool = False
    execution_proof_source: str = "CognitiveStateFormationEngineV1.run_case"
    cognitive_cycle_index: int = 1
    sufficiency_status: str = "not_observed"
    sufficiency_owner_ref: str | None = None
    sufficiency_candidate: CognitiveSufficiencyCandidateV1 | None = None
    information_gap_owner_ref: str | None = None
    information_gap_candidate: CognitiveInformationGapCandidateV1 | None = None
    reobservation_ref: str | None = None
    reobservation_owner_ref: str | None = None
    reobservation_candidate: CognitiveReobservationCandidateV1 | None = None
    reobservation_information_gap_ref: str | None = None
    next_cycle_ingress_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    hypothesis_revision_ref: str | None = None
    hypothesis_revision_owner_ref: str | None = None
    hypothesis_revision_information_gap_ref: str | None = None
    hypothesis_revision_reobservation_ref: str | None = None
    stop_reason: str | None = None
    stop_owner_ref: str | None = None
    role_refs: Tuple[str, ...] = ()
    task_refs: Tuple[str, ...] = ()
    goal_refs: Tuple[str, ...] = ()
    concern_refs: Tuple[str, ...] = ()
    information_need_refs: Tuple[str, ...] = ()
    conditioned_attention_refs: Tuple[str, ...] = ()
    conditioned_evidence_relevance_refs: Tuple[str, ...] = ()
    relation_interpretation_refs: Tuple[str, ...] = ()
    conditioned_attention_priority_candidate: float | None = None
    conditioned_attention_relevance_candidate: float | None = None
    conditioned_hypothesis_statement: str | None = None
    conditioned_hypothesis_state: str | None = None
    conditioned_world_kind_candidate: str | None = None
    conditioned_missing_information_refs: Tuple[str, ...] = ()
    field_refs: Tuple[str, ...] = ()
    selected_attention_count: int = 0
    conditioned_evidence_relevance: Tuple[str, ...] = ()
    relation_interpretation_candidates: Tuple[str, ...] = ()
    relation_interpretation_semantic_candidates: Tuple[CognitiveRelationInterpretationCandidateV1, ...] = ()
    current_world_relation_interpretation_refs: Tuple[str, ...] = ()
    conditioned_conflict_refs: Tuple[str, ...] = ()
    requirement_establishment_status: str = "NOT_ESTABLISHED"
    requirement_establishment_ref: str | None = None
    requirement_establishment_basis: str | None = None
    required_cognitive_condition_formation_result: ARouteRequiredCognitiveConditionFormationResultV1 | None = None


@dataclass(frozen=True)
class ARouteOrchestrationRequestV1:
    scenario_id: str
    ingress: ARouteIngressRefsV1
    context_ref: str = ""
    pcn_ref: str = ""
    intent_ref: str = ""
    cognitive_state_ref: str = ""
    regulation_ref: str = ""
    decision_ref: str = ""
    task_ref: str = ""
    action_ref: str = ""
    runtime_ref: str = ""
    result_ref: str = ""
    memory_experience_ref: str = ""
    learning_ref: str = ""
    self_ref: str = ""
    personality_ref: str = ""
    previous_cycle_id: str = ""
    missing_ingress: bool = False
    missing_context: bool = False
    missing_pcn: bool = False
    missing_intent: bool = False
    missing_cognitive_state: bool = False
    missing_regulation: bool = False
    missing_decision: bool = False
    defer_task: bool = False
    defer_action: bool = False
    defer_runtime: bool = False
    result_returned: bool = True
    duplicate_cycle: bool = False
    duplicate_handoff: bool = False
    duplicate_feedback: bool = False
    duplicate_reconsideration: bool = False
    reconsideration_requested: bool = False
    reconsideration_depth: int = 0
    completed_cycle_mutation_probe: bool = False
    contract_mismatch: bool = False
    version_mismatch: bool = False
    owner_authority_violation: bool = False
    upstream_failure: bool = False
    repeated_failure_signature: bool = False
    real_ingress_unavailable: bool = False
    emotion_deferred: bool = False
    b_route_deferred: bool = False
    semantic_compression_deferred: bool = False
    synthetic_only: bool = True
    candidate_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED
    execution_identity_ref: str | None = None
    replay_admission: ControlledReplayAdmissionV1 | None = None
    runtime_admission: ObservationGatewayRuntimeAdmissionV1 | None = None
    role_refs: Tuple[str, ...] = ()
    task_refs: Tuple[str, ...] = ()
    goal_refs: Tuple[str, ...] = ()
    concern_refs: Tuple[str, ...] = ()
    information_need_refs: Tuple[str, ...] = ()
    relation_interpretation_candidates: Tuple[CognitiveRelationInterpretationCandidateV1, ...] = ()
    semantic_reference_values: Tuple[CognitiveReferenceSemanticV1, ...] = ()
    required_cognitive_condition_formation_result: ARouteRequiredCognitiveConditionFormationResultV1 | None = None


@dataclass(frozen=True)
class ARouteNegativeGuardsV1:
    orchestration_can_mutate_context: bool = False
    orchestration_can_mutate_pcn: bool = False
    orchestration_can_mutate_intent: bool = False
    orchestration_can_mutate_cognitive_state: bool = False
    orchestration_can_mutate_regulation: bool = False
    orchestration_can_mutate_decision: bool = False
    orchestration_can_mutate_task: bool = False
    orchestration_can_mutate_memory: bool = False
    orchestration_can_execute_learning: bool = False
    orchestration_can_mutate_self: bool = False
    orchestration_can_mutate_personality: bool = False
    orchestration_can_mutate_emotion: bool = False
    emotion_engine_execution: bool = False
    b_route_execution: bool = False
    semantic_compression_execution: bool = False
    database_write: bool = False
    vector_store_write: bool = False
    embedding_execution: bool = False
    model_call: bool = False
    device_control: bool = False
    real_side_effect: bool = False
    synthetic_only: bool = True
    controlled_integration_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED


@dataclass(frozen=True)
class ARouteOrchestrationResultV1:
    scenario_id: str
    cycle_id: str
    lifecycle_state: str
    control_state: str
    stage_results: Tuple[ARouteStageResultV1, ...]
    handoffs: Tuple[ARouteHandoffRecordV1, ...]
    trace: "ARouteTraceV1"
    errors: Tuple[object, ...]
    negative_guards: ARouteNegativeGuardsV1 = field(default_factory=ARouteNegativeGuardsV1)
    next_cycle_ingress_refs: Tuple[str, ...] = ()
    deferred_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    synthetic_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED
    cognitive_execution: ARouteCognitiveExecutionEvidenceV1 | None = None


@dataclass(frozen=True)
class ARouteRunSummaryV1:
    phase: str
    scenario_count: int
    passed_case_count: int
    failed_case_count: int
    candidate_only: bool
    synthetic_only: bool
    runtime_execution: bool
    database_write: bool
    model_call: bool
    device_control: bool
    source_owner_mutation: bool
    emotion_engine_execution: bool
    b_route_execution: bool
    semantic_compression_execution: bool
    status: str


@dataclass(frozen=True)
class ARouteRunPayloadV1:
    summary: ARouteRunSummaryV1
    case_results: Tuple[Dict[str, object], ...]
    trace: Dict[str, object]
