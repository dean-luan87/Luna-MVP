"""Input/output envelopes and negative guards for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.midplatform.core.cognitive_learning.learning_admission_types_v1 import (
    LearningAdmissionDecisionCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.learning_candidate_types_v1 import (
    LearningCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.learning_contradiction_types_v1 import (
    LearningContradictionCandidateV1,
    LearningCounterexampleCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.learning_generalization_types_v1 import (
    GeneralizationAssessmentCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.learning_influence_types_v1 import (
    EmotionEngineEvidenceCandidateV1,
    PersonalityEvolutionEvidenceCandidateV1,
    SelfEvolutionEvidenceCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.learning_lifecycle_types_v1 import (
    LearningExpirationCandidateV1,
    LearningRevisionCandidateV1,
    LearningRevocationCandidateV1,
    LearningSupersessionCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.learning_evidence_types_v1 import (
    LearningEvidenceCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.parameter_update_candidate_types_v1 import (
    ParameterUpdateCandidateV1,
)
from capabilities.midplatform.core.cognitive_learning.cognitive_learning_trace_types_v1 import (
    CognitiveLearningProvenanceV1,
    CognitiveLearningTraceV1,
)


@dataclass(frozen=True)
class NegativeGuardStatusV1:
    learning_can_create_fact: bool
    learning_can_mutate_memory: bool
    learning_can_mutate_context: bool
    learning_can_mutate_pcn: bool
    learning_can_mutate_intent: bool
    learning_can_mutate_attention: bool
    learning_can_declare_hypothesis_truth: bool
    learning_can_mutate_current_world: bool
    learning_can_mutate_state_vector: bool
    learning_can_mutate_causal: bool
    learning_can_mutate_regulation_parameter: bool
    learning_can_bypass_parameter_bounds: bool
    learning_can_activate_parameter: bool
    learning_can_activate_genome: bool
    learning_can_mutate_self: bool
    learning_can_mutate_personality: bool
    learning_can_mutate_emotion: bool
    learning_can_create_task: bool
    learning_can_control_device: bool
    learning_can_run_scheduler: bool
    learning_can_call_model: bool
    database_write: bool
    vector_store_write: bool
    embedding_execution: bool
    runtime_training: bool
    model_weight_update: bool
    source_owner_mutation: bool
    cross_user_transfer: bool
    semantic_compression_execution: bool
    real_side_effect: bool
    planning_only: bool


@dataclass(frozen=True)
class CognitiveLearningInputV1:
    scenario_id: str
    source_experience_refs: Tuple[str, ...]
    source_memory_refs: Tuple[str, ...]
    outcome_refs: Tuple[str, ...]
    feedback_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    cognitive_state_vector_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    causal_refs: Tuple[str, ...]
    semantic_compression_ref: str | None = None
    affective_memory_summary_ref: str | None = None
    emotional_context_summary_ref: str | None = None
    user_specific_learning_candidate: bool = True
    sensitivity_level: str = "NORMAL"
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveLearningOutputV1:
    scenario_id: str
    learning_evidence_candidate: LearningEvidenceCandidateV1
    learning_candidate: LearningCandidateV1
    admission_decision_candidate: LearningAdmissionDecisionCandidateV1
    parameter_update_candidate: ParameterUpdateCandidateV1
    generalization_assessment: GeneralizationAssessmentCandidateV1
    contradiction_candidate: LearningContradictionCandidateV1 | None = None
    counterexample_candidate: LearningCounterexampleCandidateV1 | None = None
    revision_candidate: LearningRevisionCandidateV1 | None = None
    supersession_candidate: LearningSupersessionCandidateV1 | None = None
    revocation_candidate: LearningRevocationCandidateV1 | None = None
    expiration_candidate: LearningExpirationCandidateV1 | None = None
    self_evolution_evidence_candidate: SelfEvolutionEvidenceCandidateV1 | None = None
    personality_evolution_evidence_candidate: (
        PersonalityEvolutionEvidenceCandidateV1 | None
    ) = None
    emotion_engine_evidence_candidate: EmotionEngineEvidenceCandidateV1 | None = None
    trace: CognitiveLearningTraceV1 | None = None
    provenance: CognitiveLearningProvenanceV1 | None = None
    negative_guard_status: NegativeGuardStatusV1 | None = None
    synthetic_only: bool = True
    candidate_only: bool = True
    runtime_training: bool = False
    source_owner_mutation: bool = False
