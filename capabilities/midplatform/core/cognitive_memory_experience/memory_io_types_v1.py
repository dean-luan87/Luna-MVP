"""Input and output envelopes for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_registry_v1 import (
    CONTRACT_VERSION,
    SCHEMA_VERSION,
)
from capabilities.midplatform.core.cognitive_memory_experience.experience_candidate_types_v1 import (
    ExperienceCandidateV1,
)
from capabilities.midplatform.core.cognitive_memory_experience.memory_admission_types_v1 import (
    MemoryAdmissionDecisionCandidateV1,
)
from capabilities.midplatform.core.cognitive_memory_experience.memory_candidate_types_v1 import (
    FuturePersistenceHandoffCandidateV1,
    MemoryCandidateV1,
)
from capabilities.midplatform.core.cognitive_memory_experience.memory_influence_types_v1 import (
    LearningEvidenceCandidateV1,
    MemoryInfluenceCandidateV1,
    MemoryRetrievalCandidateV1,
    SelfPersonalityEvolutionEvidenceCandidateV1,
)
from capabilities.midplatform.core.cognitive_memory_experience.memory_lifecycle_types_v1 import (
    MemoryExpirationCandidateV1,
    MemoryRevisionCandidateV1,
    MemoryRevocationCandidateV1,
    MemorySupersessionCandidateV1,
)
from capabilities.midplatform.core.cognitive_memory_experience.memory_trace_types_v1 import (
    CognitiveMemoryExperienceProvenanceV1,
    CognitiveMemoryExperienceTraceV1,
)


@dataclass(frozen=True)
class CognitiveMemoryExperienceInputV1:
    scenario_id: str
    cycle_id: str
    root_cycle_trace_id: str
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_ref: str | None
    cognitive_state_vector_ref: str | None
    regulation_candidate_ref: str | None
    causal_refs: Tuple[str, ...]
    decision_refs_optional: Tuple[str, ...] = field(default_factory=tuple)
    action_refs_optional: Tuple[str, ...] = field(default_factory=tuple)
    execution_result_refs_optional: Tuple[str, ...] = field(default_factory=tuple)
    user_feedback_refs: Tuple[str, ...] = field(default_factory=tuple)
    source_evidence_refs: Tuple[str, ...] = field(default_factory=tuple)
    prior_memory_refs: Tuple[str, ...] = field(default_factory=tuple)
    synthetic_only: bool = True
    candidate_only: bool = True
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class NegativeGuardStatusV1:
    memory_can_create_fact_directly: bool
    memory_can_mutate_field: bool
    memory_can_mutate_context: bool
    memory_can_mutate_pcn: bool
    memory_can_mutate_intent: bool
    memory_can_mutate_attention: bool
    memory_can_mutate_hypothesis: bool
    memory_can_mutate_current_world: bool
    memory_can_mutate_state_vector: bool
    memory_can_mutate_regulation_parameter: bool
    memory_can_activate_parameter_genome: bool
    memory_can_execute_learning: bool
    memory_can_mutate_personality: bool
    memory_can_create_task: bool
    memory_can_control_device: bool
    memory_can_run_scheduler: bool
    memory_can_call_model: bool
    database_write: bool
    vector_store_write: bool
    embedding_execution: bool
    runtime_execution: bool
    model_call: bool
    source_owner_mutation: bool
    real_side_effect: bool
    synthetic_only: bool
    candidate_only: bool
    learning_execution: bool
    personality_mutation: bool


@dataclass(frozen=True)
class CognitiveMemoryExperienceOutputV1:
    scenario_id: str
    experience_candidate: ExperienceCandidateV1
    memory_candidate: MemoryCandidateV1
    admission_decision_candidate: MemoryAdmissionDecisionCandidateV1
    persistence_handoff_candidate: FuturePersistenceHandoffCandidateV1
    retrieval_candidate: MemoryRetrievalCandidateV1 | None = None
    pcn_influence_candidate: MemoryInfluenceCandidateV1 | None = None
    intent_influence_candidate: MemoryInfluenceCandidateV1 | None = None
    state_formation_influence_candidate: MemoryInfluenceCandidateV1 | None = None
    dynamic_regulation_influence_candidate: MemoryInfluenceCandidateV1 | None = None
    learning_evidence_candidate: LearningEvidenceCandidateV1 | None = None
    self_personality_evidence_candidate: (
        SelfPersonalityEvolutionEvidenceCandidateV1 | None
    ) = None
    revision_candidate: MemoryRevisionCandidateV1 | None = None
    supersession_candidate: MemorySupersessionCandidateV1 | None = None
    revocation_candidate: MemoryRevocationCandidateV1 | None = None
    expiration_candidate: MemoryExpirationCandidateV1 | None = None
    trace: CognitiveMemoryExperienceTraceV1 | None = None
    provenance: CognitiveMemoryExperienceProvenanceV1 | None = None
    negative_guard_status: NegativeGuardStatusV1 | None = None
    issues: Tuple[str, ...] = field(default_factory=tuple)
    synthetic_only: bool = True
    candidate_only: bool = True
    runtime_execution: bool = False
    source_owner_mutation: bool = False
