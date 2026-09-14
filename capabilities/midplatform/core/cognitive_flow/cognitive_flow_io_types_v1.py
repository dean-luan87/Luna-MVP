"""Input and output envelopes for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import (
    CycleMetadataV1,
    CycleSnapshotV1,
    NegativeGuardStatusV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_inheritance_types_v1 import (
    CognitiveMemoryObservationCandidateV1,
    CycleInheritanceCandidateV1,
    FutureLearningHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_interrupt_types_v1 import (
    AbortCandidateV1,
    InterruptCandidateV1,
    ResumeCandidateV1,
    SuspendCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_state_types_v1 import (
    CognitiveCycleStateCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    CognitiveCycleTransitionCandidateV1,
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_handoff_types_v1 import (
    ModuleHandoffEnvelopeV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_trace_types_v1 import (
    CognitiveFlowProvenanceV1,
    CognitiveFlowTraceV1,
)


@dataclass(frozen=True)
class CognitiveFlowInputV1:
    scenario_id: str
    cycle_snapshot: CycleSnapshotV1
    context_refs: Tuple[SourceRefV1, ...]
    pcn_refs: Tuple[SourceRefV1, ...]
    intent_refs: Tuple[SourceRefV1, ...]
    state_formation_refs: Tuple[SourceRefV1, ...]
    attention_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    hypothesis_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    current_world_ref: Optional[SourceRefV1] = None
    cognitive_state_vector_ref: Optional[SourceRefV1] = None
    regulation_candidate_ref: Optional[SourceRefV1] = None
    field_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    causal_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveFlowOutputV1:
    scenario_id: str
    final_state: CognitiveCycleStateCandidateV1
    transition_candidates: Tuple[CognitiveCycleTransitionCandidateV1, ...]
    handoff_envelopes: Tuple[ModuleHandoffEnvelopeV1, ...]
    reconsideration_candidates: Tuple[ReconsiderationCandidateV1, ...]
    interrupt_candidate: Optional[InterruptCandidateV1] = None
    suspend_candidate: Optional[SuspendCandidateV1] = None
    resume_candidate: Optional[ResumeCandidateV1] = None
    abort_candidate: Optional[AbortCandidateV1] = None
    inheritance_candidate: Optional[CycleInheritanceCandidateV1] = None
    memory_observation_candidate: Optional[CognitiveMemoryObservationCandidateV1] = None
    learning_handoff_candidate: Optional[FutureLearningHandoffCandidateV1] = None
    trace: Optional[CognitiveFlowTraceV1] = None
    provenance: Optional[CognitiveFlowProvenanceV1] = None
    negative_guard_status: Optional[NegativeGuardStatusV1] = None
    metadata: Optional[CycleMetadataV1] = None
    issues: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_executed: bool = False
    source_owner_mutation: bool = False
