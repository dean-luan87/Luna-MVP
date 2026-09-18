"""Minimum Brain-to-A-Route closure and assimilation contracts.

These are reference-oriented integration envelopes.  They do not replace the
canonical A-Route, Cognitive State Formation, or existing closure candidates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Tuple

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteCognitiveExecutionEvidenceV1,
    ARouteOrchestrationResultV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationGatewayAdmissionQueryV1,
    ObservationGatewayResultV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_lifecycle_closure_types_v1 import (
    BrainAssimilationCandidateV1,
    ClosureAssessmentCandidateV1,
    ClosureDecisionCandidateV1,
    LifecycleClosureCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_continuity_candidate_types_v1 import (
    CognitiveOutcomeCandidateV1,
    LoopClosureRecordCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)


PHASE = "Phase-P1-Luna-Brain-Cognitive-Loop-Closure-And-Assimilation-Contract-Integration-v1-001"
BRAIN_RESPONSIBILITY_DOMAIN = "BRAIN"
BRAIN_CANONICAL_OWNER_STATUS = "OWNER_UNRESOLVED"
LOOP_LIFECYCLE_OWNER = "Cognitive Flow Governance"
SUFFICIENCY_OWNER = "Cognitive State Formation Governance"
REOBSERVATION_OWNER = "Field Perception Orchestrator"


@dataclass(frozen=True)
class BrainCognitiveRequestV1:
    """Brain-domain candidate request with unresolved runtime ownership."""

    brain_request_ref: str
    brain_subject_ref: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    context_ref: str
    role_ref: Optional[str]
    information_need_ref: str
    required_information_refs: Tuple[str, ...]
    execution_instance_ref: str
    candidate_only: bool = True
    model_invocation: bool = False
    provider_invocation: bool = False
    live_observation_execution: bool = False
    action_execution: bool = False
    task_execution: bool = False
    responsibility_domain: str = BRAIN_RESPONSIBILITY_DOMAIN
    canonical_owner_status: str = BRAIN_CANONICAL_OWNER_STATUS


@dataclass(frozen=True)
class BrainInformationNeedCandidateV1:
    """Goal/Intent/Concern to current Information Need binding."""

    information_need_ref: str
    responsibility_domain: str
    canonical_owner_status: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    context_ref: str
    required_information_refs: Tuple[str, ...]
    need_candidate: CognitiveNeedCandidateV1
    candidate_only: bool = True


@dataclass(frozen=True)
class BrainCognitiveLoopInstanceV1:
    """Mechanical loop identity; semantic cognition remains with A owners."""

    cognitive_loop_ref: str
    brain_request_ref: str
    lifecycle_owner_ref: str
    information_need_ref: str
    cycle_count: int
    execution_refs: Tuple[str, ...]
    candidate_only: bool = True
    state_mutation: bool = False


@dataclass(frozen=True)
class BrainCognitiveCaseResultV1:
    case_id: str
    title: str
    brain_request: BrainCognitiveRequestV1
    information_need: BrainInformationNeedCandidateV1
    loop_instance: BrainCognitiveLoopInstanceV1
    gateway_results: Tuple[ObservationGatewayResultV1, ...]
    gateway_admission_queries: Tuple[ObservationGatewayAdmissionQueryV1, ...]
    route_results: Tuple[ARouteOrchestrationResultV1, ...]
    cognitive_proofs: Tuple[ARouteCognitiveExecutionEvidenceV1, ...]
    closure_assessment: Optional[ClosureAssessmentCandidateV1]
    closure_acceptance: Optional[ClosureDecisionCandidateV1]
    lifecycle_closure: Optional[LifecycleClosureCandidateV1]
    closure_record: Optional[LoopClosureRecordCandidateV1]
    cognitive_outcome: Optional[CognitiveOutcomeCandidateV1]
    assimilation_candidate: Optional[BrainAssimilationCandidateV1]
    negative_guards: Mapping[str, bool]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    brain_responsibility_domain: str = BRAIN_RESPONSIBILITY_DOMAIN
    brain_canonical_owner_status: str = BRAIN_CANONICAL_OWNER_STATUS


__all__ = [
    "PHASE",
    "BRAIN_RESPONSIBILITY_DOMAIN",
    "BRAIN_CANONICAL_OWNER_STATUS",
    "LOOP_LIFECYCLE_OWNER",
    "SUFFICIENCY_OWNER",
    "REOBSERVATION_OWNER",
    "BrainCognitiveRequestV1",
    "BrainInformationNeedCandidateV1",
    "BrainCognitiveLoopInstanceV1",
    "BrainCognitiveCaseResultV1",
]
