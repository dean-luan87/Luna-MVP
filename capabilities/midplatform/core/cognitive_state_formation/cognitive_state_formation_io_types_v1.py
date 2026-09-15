"""Input and output contracts for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Tuple

from capabilities.midplatform.core.cognitive_state_formation.attention_types_v1 import (
    AttentionCandidateV1,
    AttentionSelectionCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
    HypothesisCompetitionResultV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    NegativeGuardStatusV1,
    ProvenanceEnvelopeV1,
    CognitiveReferenceSemanticV1,
    SourceRefV1,
    TraceEnvelopeV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_handoff_types_v1 import (
    CognitiveToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_vector_types_v1 import (
    CognitiveStateVectorCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    CognitiveHypothesisRevisionCandidateV1,
    CognitiveInformationGapCandidateV1,
    CognitiveReobservationCandidateV1,
    CognitiveStopCandidateV1,
    CognitiveSufficiencyCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_conditioning_types_v1 import (
    CognitiveEvidenceRelevanceCandidateV1,
    CognitiveRelationInterpretationCandidateV1,
)
if TYPE_CHECKING:
    from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
        ARouteRequiredCognitiveConditionFormationResultV1,
    )
from capabilities.midplatform.core.execution_mode_v1 import SYNTHETIC_CONTROLLED
from .cognitive_loop_types_v1 import (
    CognitiveInformationGapCandidateV1,
    CognitiveReobservationCandidateV1,
    CognitiveSufficiencyCandidateV1,
)


@dataclass(frozen=True)
class CognitiveStateFormationInputV1:
    scenario_id: str
    context_refs: Tuple[SourceRefV1, ...]
    pcn_refs: Tuple[SourceRefV1, ...]
    intent_refs: Tuple[SourceRefV1, ...]
    field_refs: Tuple[SourceRefV1, ...]
    observation_refs: Tuple[SourceRefV1, ...]
    # Optional read-only upstream Current World reference.  Existing
    # synthetic callers omit it, preserving the v1 contract behavior.
    current_world_ref: SourceRefV1 | None = None
    risk_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    uncertainty_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    task_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    role_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    memory_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    synthetic_only: bool = True
    candidate_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED
    replay_input_ref: str | None = None
    runtime_observation_ref: str | None = None
    execution_ref: str | None = None
    evidence_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    required_information_refs: Tuple[str, ...] = field(default_factory=tuple)
    available_information_refs: Tuple[str, ...] = field(default_factory=tuple)
    # Explicit read-only binding from an admitted Evidence ref to the
    # information refs that the upstream observation declares it can support.
    # An empty binding preserves legacy callers; LIVE provider ingress uses it
    # so relevance can gate information coverage without changing Evidence.
    evidence_information_refs: Tuple[Tuple[str, Tuple[str, ...]], ...] = field(default_factory=tuple)
    inherited_information_refs: Tuple[str, ...] = field(default_factory=tuple)
    prior_current_world_ref: SourceRefV1 | None = None
    prior_hypothesis_refs: Tuple[str, ...] = field(default_factory=tuple)
    prior_information_gap_ref: str | None = None
    prior_reobservation_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    prior_sufficiency_candidate: CognitiveSufficiencyCandidateV1 | None = None
    prior_information_gap_candidate: CognitiveInformationGapCandidateV1 | None = None
    prior_reobservation_candidate: CognitiveReobservationCandidateV1 | None = None
    cycle_index: int = 1
    # Reference-only conditioning inputs.  Existing callers retain the
    # synthetic defaults; controlled replay may carry the active context.
    goal_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    concern_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    information_need_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    relation_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    # Optional typed, read-only relation projections produced by an upstream
    # governed Field State adapter.  Empty preserves legacy callers.
    relation_interpretation_candidates: Tuple[CognitiveRelationInterpretationCandidateV1, ...] = field(default_factory=tuple)
    requirement_establishment_status: str = "NOT_ESTABLISHED"
    requirement_establishment_ref: str | None = None
    requirement_establishment_basis: str | None = None
    semantic_reference_values: Tuple[CognitiveReferenceSemanticV1, ...] = field(default_factory=tuple)
    required_cognitive_condition_formation_result: ARouteRequiredCognitiveConditionFormationResultV1 | None = None


@dataclass(frozen=True)
class CognitiveStateFormationOutputV1:
    scenario_id: str
    attention_candidates: Tuple[AttentionCandidateV1, ...]
    attention_selection_candidate: AttentionSelectionCandidateV1
    cognitive_hypotheses: Tuple[CognitiveHypothesisCandidateV1, ...]
    hypothesis_competition_result: HypothesisCompetitionResultV1
    current_world_candidate: CurrentWorldCandidateV1
    cognitive_state_vector_candidate: CognitiveStateVectorCandidateV1
    causal_handoff_candidate: CognitiveToCausalHandoffCandidateV1
    trace: TraceEnvelopeV1
    provenance: ProvenanceEnvelopeV1
    negative_guard_status: NegativeGuardStatusV1
    candidate_only: bool = True
    runtime_executed: bool = False
    source_mutation_executed: bool = False
    execution_mode: str = SYNTHETIC_CONTROLLED
    execution_ref: str | None = None
    cognitive_transition_refs: Tuple[str, ...] = field(default_factory=tuple)
    execution_owner_ref: str = "Cognitive State Formation Governance"
    sufficiency_candidate: CognitiveSufficiencyCandidateV1 | None = None
    information_gap_candidate: CognitiveInformationGapCandidateV1 | None = None
    reobservation_candidate: CognitiveReobservationCandidateV1 | None = None
    hypothesis_revision_candidate: CognitiveHypothesisRevisionCandidateV1 | None = None
    stop_candidate: CognitiveStopCandidateV1 | None = None
    next_cycle_ingress_ref: str | None = None
    cognitive_cycle_index: int = 1
    evidence_relevance_candidates: Tuple[CognitiveEvidenceRelevanceCandidateV1, ...] = field(default_factory=tuple)
    relation_interpretation_candidates: Tuple[CognitiveRelationInterpretationCandidateV1, ...] = field(default_factory=tuple)
    requirement_establishment_status: str = "NOT_ESTABLISHED"
    requirement_establishment_ref: str | None = None
    requirement_establishment_basis: str | None = None
    required_cognitive_condition_formation_result: ARouteRequiredCognitiveConditionFormationResultV1 | None = None
