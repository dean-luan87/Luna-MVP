"""Input/output envelopes for the controlled Personality Governance module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from .personality_admission_types_v1 import (
    PersonalityAdmissionDecisionCandidateV1,
    PersonalityEvidenceCandidateV1,
    PersonalityUserCorrectionCandidateV1,
)
from .personality_influence_types_v1 import (
    EmotionToPersonalityEvidenceCandidateV1,
    PersonalityEvidenceHandoffCandidateV1,
    PersonalityToEmotionContextCandidateV1,
)
from .personality_profile_types_v1 import (
    PersonalityProfileCandidateV1,
    PersonalityProfileUpdateCandidateV1,
)
from .personality_revision_types_v1 import (
    PersonalityExpirationCandidateV1,
    PersonalityRevisionCandidateV1,
    PersonalityRevocationCandidateV1,
    PersonalitySupersessionCandidateV1,
)
from .personality_stability_types_v1 import PersonalityStabilityAssessmentCandidateV1
from .personality_trace_types_v1 import PersonalityProvenanceV1, PersonalityTraceV1
from .personality_trait_types_v1 import PersonalityTraitCandidateV1


@dataclass(frozen=True)
class PersonalityGovernanceInputV1:
    scenario_id: str
    title: str
    trait_dimension: str
    trait_value_candidate: str
    evidence_kind: str
    source_refs: Tuple[str, ...] = ()
    evidence_refs: Tuple[str, ...] = ()
    memory_refs: Tuple[str, ...] = ()
    learning_refs: Tuple[str, ...] = ()
    self_refs: Tuple[str, ...] = ()
    emotion_refs: Tuple[str, ...] = ()
    regulation_refs: Tuple[str, ...] = ()
    interaction_refs: Tuple[str, ...] = ()
    context_refs: Tuple[str, ...] = ()
    uncertainty_refs: Tuple[str, ...] = ()
    contradiction_refs: Tuple[str, ...] = ()
    counterexample_refs: Tuple[str, ...] = ()
    repetition: int = 1
    temporal_span: int = 1
    evidence_strength: str = "LOW"
    confidence_candidate: str = "LOW"
    sensitivity: str = "NORMAL"
    user_correction: bool = False
    user_confirmed: bool = False
    revision_parent_ref: Optional[str] = None
    supersedes_ref: Optional[str] = None
    revocation_refs: Tuple[str, ...] = ()
    expired: bool = False
    profile_dimensions: Tuple[str, ...] = ()
    profile_trait_refs: Tuple[str, ...] = ()
    profile_context_refs: Tuple[str, ...] = ()
    duplicate_evidence: bool = False
    duplicate_profile_update: bool = False
    semantic_compression_ref: Optional[str] = None
    affective_memory_summary_ref: Optional[str] = None
    emotion_memory_summary_ref: Optional[str] = None
    personality_memory_fusion_ref: Optional[str] = None
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityNegativeGuardStatusV1:
    guards: Tuple[Tuple[str, bool], ...]

    def as_dict(self):
        return dict(self.guards)


@dataclass(frozen=True)
class PersonalityGovernanceOutputV1:
    scenario_id: str
    evidence: PersonalityEvidenceCandidateV1
    trait_candidate: PersonalityTraitCandidateV1
    profile_candidate: Optional[PersonalityProfileCandidateV1]
    stability_assessment: PersonalityStabilityAssessmentCandidateV1
    admission_decision: PersonalityAdmissionDecisionCandidateV1
    revision_candidate: Optional[PersonalityRevisionCandidateV1]
    supersession_candidate: Optional[PersonalitySupersessionCandidateV1]
    revocation_candidate: Optional[PersonalityRevocationCandidateV1]
    expiration_candidate: Optional[PersonalityExpirationCandidateV1]
    user_correction_candidate: Optional[PersonalityUserCorrectionCandidateV1]
    emotion_to_personality_candidate: Optional[EmotionToPersonalityEvidenceCandidateV1]
    personality_to_emotion_candidate: Optional[PersonalityToEmotionContextCandidateV1]
    evidence_handoff_candidates: Tuple[PersonalityEvidenceHandoffCandidateV1, ...]
    profile_update_candidate: Optional[PersonalityProfileUpdateCandidateV1]
    trace: PersonalityTraceV1
    provenance: PersonalityProvenanceV1
    negative_guard_status: PersonalityNegativeGuardStatusV1
    semantic_compression_status: str
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_execution: bool = False
    database_write: bool = False
    source_owner_mutation: bool = False
    trait_activation: bool = False
    issues: Tuple[str, ...] = field(default_factory=tuple)
