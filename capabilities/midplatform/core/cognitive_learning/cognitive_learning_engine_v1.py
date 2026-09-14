"""Deterministic synthetic engine for Cognitive Learning controlled implementation v1."""

from __future__ import annotations

from capabilities.midplatform.core.cognitive_learning.cognitive_learning_registry_v1 import (
    ADMISSION_STATES,
    CONTRACT_VERSION,
    GENERALIZATION_LEVELS,
    LEARNING_KINDS,
    NEGATIVE_GUARDS,
    SCHEMA_VERSION,
)
from capabilities.midplatform.core.cognitive_learning.cognitive_learning_io_types_v1 import (
    CognitiveLearningInputV1,
    CognitiveLearningOutputV1,
    NegativeGuardStatusV1,
)
from capabilities.midplatform.core.cognitive_learning.cognitive_learning_trace_types_v1 import (
    CognitiveLearningProvenanceV1,
    CognitiveLearningTraceV1,
)
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
from capabilities.midplatform.core.cognitive_learning.learning_evidence_types_v1 import (
    LearningEvidenceCandidateV1,
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
from capabilities.midplatform.core.cognitive_learning.parameter_update_candidate_types_v1 import (
    ParameterUpdateCandidateV1,
)


class CognitiveLearningEngineV1:
    def _learning_kind(self, sid: str) -> str:
        mapping = {
            "L01": "SUCCESS_PATTERN",
            "L02": "SUCCESS_PATTERN",
            "L03": "SUCCESS_PATTERN",
            "L04": "FAILURE_PATTERN",
            "L05": "FAILURE_PATTERN",
            "L06": "CONTRADICTION_PATTERN",
            "L07": "USER_FEEDBACK_PATTERN",
            "L08": "NEGATIVE_EVIDENCE_PATTERN",
            "L09": "USER_FEEDBACK_PATTERN",
            "L10": "NEGATIVE_EVIDENCE_PATTERN",
            "L11": "TEMPORAL_PATTERN",
            "L12": "SUCCESS_PATTERN",
            "L13": "SUCCESS_PATTERN",
            "L14": "PREFERENCE_PATTERN",
            "L15": "SOCIAL_PATTERN",
            "L16": "CONTEXT_DEPENDENT_PATTERN",
            "L17": "CONTEXT_DEPENDENT_PATTERN",
            "L18": "RESOURCE_PATTERN",
            "L19": "ATTENTION_PATTERN",
            "L20": "HYPOTHESIS_RESOLUTION_PATTERN",
            "L21": "UNRESOLVED_PATTERN",
            "L22": "SUCCESS_PATTERN",
            "L23": "SUCCESS_PATTERN",
            "L24": "REGULATION_EFFECT_PATTERN",
            "L25": "REGULATION_EFFECT_PATTERN",
            "L26": "REGULATION_EFFECT_PATTERN",
            "L27": "USER_FEEDBACK_PATTERN",
            "L28": "SUCCESS_PATTERN",
            "L29": "SUCCESS_PATTERN",
            "L30": "REGULATION_EFFECT_PATTERN",
            "L31": "CONTRADICTION_PATTERN",
            "L32": "NEGATIVE_EVIDENCE_PATTERN",
        }
        return mapping[sid]

    def _generalization(self, sid: str) -> str:
        mapping = {
            "L01": "INSTANCE_ONLY",
            "L02": "INSTANCE_ONLY",
            "L03": "LOCAL_CONTEXT",
            "L04": "INSTANCE_ONLY",
            "L05": "LOCAL_CONTEXT",
            "L06": "INSTANCE_ONLY",
            "L07": "LOCAL_CONTEXT",
            "L08": "LOCAL_CONTEXT",
            "L09": "INSTANCE_ONLY",
            "L10": "INSTANCE_ONLY",
            "L11": "INSTANCE_ONLY",
            "L12": "INSTANCE_ONLY",
            "L13": "LOCAL_CONTEXT",
            "L14": "LOCAL_CONTEXT",
            "L15": "RELATIONSHIP_CONTEXT",
            "L16": "ROLE_CONTEXT",
            "L17": "LOCAL_CONTEXT",
            "L18": "LOCAL_CONTEXT",
            "L19": "LOCAL_CONTEXT",
            "L20": "LOCAL_CONTEXT",
            "L21": "INSTANCE_ONLY",
            "L22": "LOCAL_CONTEXT",
            "L23": "INSTANCE_ONLY",
            "L24": "LOCAL_CONTEXT",
            "L25": "LOCAL_CONTEXT",
            "L26": "LOCAL_CONTEXT",
            "L27": "INSTANCE_ONLY",
            "L28": "INSTANCE_ONLY",
            "L29": "INSTANCE_ONLY",
            "L30": "LOCAL_CONTEXT",
            "L31": "LOCAL_CONTEXT",
            "L32": "INSTANCE_ONLY",
        }
        return mapping[sid]

    def _admission_state(self, sid: str) -> str:
        mapping = {
            "L01": "LEARNING_CANDIDATE_READY",
            "L02": "ELIGIBLE",
            "L03": "LEARNING_CANDIDATE_READY",
            "L04": "ELIGIBLE",
            "L05": "LEARNING_CANDIDATE_READY",
            "L06": "CONTESTED",
            "L07": "ELIGIBLE",
            "L08": "ELIGIBLE",
            "L09": "INSUFFICIENT_EVIDENCE",
            "L10": "REVOKED",
            "L11": "SUPERSEDED",
            "L12": "INSUFFICIENT_EVIDENCE",
            "L13": "ELIGIBLE",
            "L14": "LEARNING_CANDIDATE_READY",
            "L15": "LEARNING_CANDIDATE_READY",
            "L16": "LEARNING_CANDIDATE_READY",
            "L17": "LEARNING_CANDIDATE_READY",
            "L18": "ELIGIBLE",
            "L19": "LEARNING_CANDIDATE_READY",
            "L20": "LEARNING_CANDIDATE_READY",
            "L21": "CONTESTED",
            "L22": "LEARNING_CANDIDATE_READY",
            "L23": "ELIGIBLE",
            "L24": "PARAMETER_UPDATE_CANDIDATE_READY",
            "L25": "CONTESTED",
            "L26": "PARAMETER_UPDATE_CANDIDATE_READY",
            "L27": "NEEDS_CONFIRMATION",
            "L28": "LEARNING_CANDIDATE_READY",
            "L29": "REJECTED",
            "L30": "REJECTED",
            "L31": "REVISED",
            "L32": "REVOKED",
        }
        return mapping[sid]

    def _learning_evidence(
        self, request: CognitiveLearningInputV1
    ) -> LearningEvidenceCandidateV1:
        sid = request.scenario_id
        return LearningEvidenceCandidateV1(
            learning_evidence_id=f"learning_evidence:{sid}",
            source_experience_refs=request.source_experience_refs,
            source_memory_refs=request.source_memory_refs,
            outcome_refs=request.outcome_refs,
            feedback_refs=request.feedback_refs,
            contradiction_refs=request.contradiction_refs,
            counterexample_refs=request.counterexample_refs,
            context_refs=request.context_refs,
            intent_refs=request.intent_refs,
            hypothesis_refs=request.hypothesis_refs,
            current_world_refs=request.current_world_refs,
            cognitive_state_vector_refs=request.cognitive_state_vector_refs,
            regulation_refs=request.regulation_refs,
            causal_refs=request.causal_refs,
            evidence_strength_candidate="HIGH"
            if sid in {"L03", "L05", "L22", "L24"}
            else "LOW"
            if sid in {"L04", "L12", "L23"}
            else "MEDIUM",
            repetition_count_candidate="REPEATED"
            if sid in {"L02", "L03", "L05", "L13", "L29", "L30"}
            else "SINGLE",
            novelty_candidate="LOW" if sid in {"L02", "L03", "L05", "L13"} else "HIGH",
            consistency_candidate="LOW"
            if sid in {"L06", "L21", "L31", "L32"}
            else "HIGH",
            contradiction_level_candidate="HIGH"
            if sid in {"L06", "L31", "L32"}
            else "NONE",
            temporal_span_candidate="LONG" if sid in {"L03", "L05", "L13"} else "SHORT",
            scope_candidate=self._generalization(sid),
            provenance_refs=(f"prov:{sid}:evidence",),
            trace_ref=f"trace:{sid}:learning_evidence",
        )

    def _learning_candidate(
        self, request: CognitiveLearningInputV1, evidence: LearningEvidenceCandidateV1
    ) -> LearningCandidateV1:
        sid = request.scenario_id
        return LearningCandidateV1(
            learning_candidate_id=f"learning_candidate:{sid}",
            learning_evidence_refs=(evidence.learning_evidence_id,),
            learning_kind=self._learning_kind(sid),
            candidate_statement=f"candidate_statement:{sid}",
            scope=self._generalization(sid),
            confidence_candidate="LOW"
            if sid in {"L04", "L09", "L12", "L21", "L23"}
            else "MEDIUM"
            if sid in {"L01", "L02", "L07", "L08", "L13", "L18", "L22", "L24"}
            else "HIGH",
            generalization_level_candidate=self._generalization(sid),
            transferability_candidate="LOW"
            if self._generalization(sid) == "INSTANCE_ONLY"
            else "MEDIUM",
            reversibility_candidate="HIGH",
            uncertainty_refs=(f"uncertainty:{sid}",)
            if sid in {"L21", "L23", "L28"}
            else (),
            counterexample_refs=request.counterexample_refs,
            contradiction_refs=request.contradiction_refs,
            temporal_validity_candidate="STALE" if sid == "L09" else "ACTIVE",
            revision_of_ref=f"learning_candidate:{sid}:old" if sid == "L31" else None,
            supersedes_ref=f"learning_candidate:{sid}:prior" if sid == "L31" else None,
            revoked_ref=f"learning_candidate:{sid}:revoked" if sid == "L32" else None,
            provenance_refs=(f"prov:{sid}:candidate",),
            trace_ref=f"trace:{sid}:learning_candidate",
        )

    def _admission_decision(
        self, sid: str, candidate: LearningCandidateV1
    ) -> LearningAdmissionDecisionCandidateV1:
        return LearningAdmissionDecisionCandidateV1(
            decision_id=f"decision:{sid}",
            learning_candidate_ref=candidate.learning_candidate_id,
            admission_state=self._admission_state(sid),
            evidence_strength="HIGH"
            if sid in {"L03", "L05", "L24"}
            else "LOW"
            if sid in {"L04", "L12"}
            else "MEDIUM",
            repetition="REPEATED"
            if sid in {"L02", "L03", "L05", "L13", "L29", "L30"}
            else "SINGLE",
            consistency="LOW" if sid in {"L06", "L31", "L32"} else "HIGH",
            diversity_of_context="DIVERSE" if sid == "L03" else "NARROW",
            counterexample_density="HIGH" if sid in {"L06", "L25"} else "LOW",
            contradiction_level="HIGH" if sid in {"L06", "L31", "L32"} else "NONE",
            recency="STALE" if sid == "L09" else "RECENT",
            temporal_span="LONG" if sid in {"L03", "L05", "L13"} else "SHORT",
            user_confirmation="REQUIRED" if sid == "L27" else "NOT_REQUIRED",
            causal_support_status="PRESENT" if sid == "L22" else "ABSENT",
            decision_reasons=(self._admission_state(sid).lower(),),
            trace_ref=f"trace:{sid}:admission",
        )

    def _parameter_update(
        self, sid: str, candidate: LearningCandidateV1
    ) -> ParameterUpdateCandidateV1:
        return ParameterUpdateCandidateV1(
            parameter_update_candidate_id=f"parameter_update:{sid}",
            learning_candidate_refs=(candidate.learning_candidate_id,),
            target_regulation_parameter_refs=(f"regulation_parameter:{sid}:1",),
            parameter_class_refs=("C",),
            proposed_direction="INCREASE"
            if sid not in {"L04", "L08", "L25"}
            else "DECREASE",
            proposed_delta_candidate="SMALL",
            proposed_bounds_ref=f"bounds:{sid}:1",
            expected_effect_candidate="candidate_effect",
            risk_candidate="MEDIUM",
            reversibility_candidate="HIGH",
            approval_requirement_candidate="REGULATION_REVIEW_REQUIRED",
            trace_ref=f"trace:{sid}:parameter_update",
            provenance_refs=(f"prov:{sid}:parameter_update",),
        )

    def _generalization_assessment(
        self, sid: str
    ) -> GeneralizationAssessmentCandidateV1:
        level = self._generalization(sid)
        return GeneralizationAssessmentCandidateV1(
            assessment_id=f"generalization:{sid}",
            generalization_level_candidate=level,
            evidence_diversity_sufficient=sid == "L03",
            counterexample_blocking=sid in {"L06", "L25"},
            contradiction_visible=sid in {"L06", "L21", "L31", "L32"},
        )

    def _negative_guards(self) -> NegativeGuardStatusV1:
        return NegativeGuardStatusV1(**NEGATIVE_GUARDS)

    def _trace(
        self,
        request: CognitiveLearningInputV1,
        evidence: LearningEvidenceCandidateV1,
        learning: LearningCandidateV1,
        update: ParameterUpdateCandidateV1,
    ) -> CognitiveLearningTraceV1:
        sid = request.scenario_id
        reverse_lookup = {
            update.parameter_update_candidate_id: (
                learning.learning_candidate_id,
                evidence.learning_evidence_id,
                *request.source_memory_refs,
                *request.source_experience_refs,
            ),
            learning.learning_candidate_id: (
                evidence.learning_evidence_id,
                *request.source_memory_refs,
                *request.source_experience_refs,
            ),
        }
        return CognitiveLearningTraceV1(
            root_cycle_trace_id=f"trace:{sid}:root_cycle",
            learning_trace_id=f"trace:{sid}:learning",
            learning_evidence_id=evidence.learning_evidence_id,
            learning_candidate_id=learning.learning_candidate_id,
            parameter_update_candidate_id=update.parameter_update_candidate_id,
            source_experience_refs=request.source_experience_refs,
            source_memory_refs=request.source_memory_refs,
            outcome_refs=request.outcome_refs,
            feedback_refs=request.feedback_refs,
            contradiction_refs=request.contradiction_refs,
            counterexample_refs=request.counterexample_refs,
            regulation_refs=request.regulation_refs,
            revision_refs=(learning.revision_of_ref,)
            if learning.revision_of_ref
            else (),
            provenance_refs=(f"prov:{sid}:trace",),
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
            reverse_lookup=reverse_lookup,
        )

    def _provenance(
        self,
        request: CognitiveLearningInputV1,
        evidence: LearningEvidenceCandidateV1,
        learning: LearningCandidateV1,
        update: ParameterUpdateCandidateV1,
    ) -> CognitiveLearningProvenanceV1:
        return CognitiveLearningProvenanceV1(
            parameter_update_candidate_ref=update.parameter_update_candidate_id,
            learning_candidate_ref=learning.learning_candidate_id,
            learning_evidence_ref=evidence.learning_evidence_id,
            memory_refs=request.source_memory_refs,
            experience_refs=request.source_experience_refs,
            cycle_refs=(f"cycle:{request.scenario_id}",),
            reverse_locatable=True,
            source_owner_mutation=False,
        )

    def run_case(self, request: CognitiveLearningInputV1) -> CognitiveLearningOutputV1:
        sid = request.scenario_id
        evidence = self._learning_evidence(request)
        learning = self._learning_candidate(request, evidence)
        decision = self._admission_decision(sid, learning)
        update = self._parameter_update(sid, learning)
        contradiction = (
            LearningContradictionCandidateV1(
                contradiction_id=f"contradiction:{sid}",
                learning_candidate_refs=(learning.learning_candidate_id,),
                contradiction_reason="contradiction_detected",
            )
            if sid in {"L06", "L21", "L31", "L32"}
            else None
        )
        counterexample = (
            LearningCounterexampleCandidateV1(
                counterexample_id=f"counterexample:{sid}",
                learning_candidate_refs=(learning.learning_candidate_id,),
                counterexample_reason="counterexample_detected",
            )
            if sid in {"L06", "L25"}
            else None
        )
        revision = (
            LearningRevisionCandidateV1(
                revision_id=f"revision:{sid}",
                prior_learning_candidate_ref=f"learning_candidate:{sid}:old",
                new_learning_candidate_ref=learning.learning_candidate_id,
                reason="updated_evidence",
                trace_ref=f"trace:{sid}:revision",
            )
            if sid == "L31"
            else None
        )
        supersession = (
            LearningSupersessionCandidateV1(
                supersession_id=f"supersession:{sid}",
                superseded_learning_candidate_ref=f"learning_candidate:{sid}:prior",
                superseding_learning_candidate_ref=learning.learning_candidate_id,
                reason="newer_pattern_better_fit",
                trace_ref=f"trace:{sid}:supersession",
            )
            if sid == "L31"
            else None
        )
        revocation = (
            LearningRevocationCandidateV1(
                revocation_id=f"revocation:{sid}",
                learning_candidate_ref=learning.learning_candidate_id,
                reason="source_revoked",
                trace_ref=f"trace:{sid}:revocation",
            )
            if sid in {"L10", "L32"}
            else None
        )
        expiration = (
            LearningExpirationCandidateV1(
                expiration_id=f"expiration:{sid}",
                learning_candidate_ref=learning.learning_candidate_id,
                reason="expired_or_stale",
                trace_ref=f"trace:{sid}:expiration",
            )
            if sid in {"L09", "L32"}
            else None
        )
        self_evolution = (
            SelfEvolutionEvidenceCandidateV1(
                evidence_id=f"self:{sid}",
                learning_candidate_refs=(learning.learning_candidate_id,),
            )
            if sid == "L16"
            else None
        )
        personality_evolution = (
            PersonalityEvolutionEvidenceCandidateV1(
                evidence_id=f"personality:{sid}",
                learning_candidate_refs=(learning.learning_candidate_id,),
            )
            if sid == "L16"
            else None
        )
        emotion_evidence = (
            EmotionEngineEvidenceCandidateV1(
                evidence_id=f"emotion:{sid}",
                learning_candidate_refs=(learning.learning_candidate_id,),
            )
            if sid == "L27"
            else None
        )
        return CognitiveLearningOutputV1(
            scenario_id=sid,
            learning_evidence_candidate=evidence,
            learning_candidate=learning,
            admission_decision_candidate=decision,
            parameter_update_candidate=update,
            generalization_assessment=self._generalization_assessment(sid),
            contradiction_candidate=contradiction,
            counterexample_candidate=counterexample,
            revision_candidate=revision,
            supersession_candidate=supersession,
            revocation_candidate=revocation,
            expiration_candidate=expiration,
            self_evolution_evidence_candidate=self_evolution,
            personality_evolution_evidence_candidate=personality_evolution,
            emotion_engine_evidence_candidate=emotion_evidence,
            trace=self._trace(request, evidence, learning, update),
            provenance=self._provenance(request, evidence, learning, update),
            negative_guard_status=self._negative_guards(),
            synthetic_only=True,
            candidate_only=True,
            runtime_training=False,
            source_owner_mutation=False,
        )
