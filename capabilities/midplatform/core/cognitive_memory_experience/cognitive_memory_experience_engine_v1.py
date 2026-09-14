"""Deterministic synthetic engine for Cognitive Memory & Experience controlled implementation v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_registry_v1 import (
    CONTRACT_VERSION,
    NEGATIVE_GUARDS,
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
from capabilities.midplatform.core.cognitive_memory_experience.memory_io_types_v1 import (
    CognitiveMemoryExperienceInputV1,
    CognitiveMemoryExperienceOutputV1,
    NegativeGuardStatusV1,
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


class CognitiveMemoryExperienceEngineV1:
    def _memory_type(self, sid: str) -> str:
        mapping = {
            "M01": "EPISODIC",
            "M02": "EPISODIC",
            "M03": "EPISODIC",
            "M04": "ENVIRONMENTAL_CONTEXT",
            "M05": "UNRESOLVED_EXPERIENCE",
            "M06": "UNRESOLVED_EXPERIENCE",
            "M07": "EPISODIC",
            "M08": "SEMANTIC",
            "M09": "SEMANTIC",
            "M10": "SEMANTIC",
            "M11": "ENVIRONMENTAL_CONTEXT",
            "M12": "PREFERENCE",
            "M13": "PREFERENCE",
            "M14": "PREFERENCE",
            "M15": "RELATIONAL",
            "M16": "SELF_RELATED",
            "M17": "EPISODIC",
            "M18": "RELATIONAL",
            "M19": "PREFERENCE",
            "M20": "UNRESOLVED_EXPERIENCE",
            "M21": "TASK_EXPERIENCE",
            "M22": "TASK_EXPERIENCE",
            "M23": "EPISODIC",
            "M24": "EPISODIC",
            "M25": "SELF_RELATED",
            "M26": "EPISODIC",
            "M27": "ENVIRONMENTAL_CONTEXT",
            "M28": "UNRESOLVED_EXPERIENCE",
        }
        return mapping[sid]

    def _admission(self, sid: str) -> str:
        mapping = {
            "M01": "ELIGIBLE",
            "M02": "TEMPORARY",
            "M03": "ELIGIBLE",
            "M04": "TEMPORARY",
            "M05": "CONTESTED",
            "M06": "CONTESTED",
            "M07": "CONTESTED",
            "M08": "SUPERSEDED",
            "M09": "REVISED",
            "M10": "REVOKED",
            "M11": "EXPIRED",
            "M12": "ADMITTED_CANDIDATE",
            "M13": "REJECTED",
            "M14": "NEEDS_CONFIRMATION",
            "M15": "NEEDS_CONFIRMATION",
            "M16": "NEEDS_CONFIRMATION",
            "M17": "ELIGIBLE",
            "M18": "ELIGIBLE",
            "M19": "ELIGIBLE",
            "M20": "ELIGIBLE",
            "M21": "ELIGIBLE",
            "M22": "ELIGIBLE",
            "M23": "REJECTED",
            "M24": "ELIGIBLE",
            "M25": "NEEDS_CONFIRMATION",
            "M26": "CONTESTED",
            "M27": "EXPIRED",
            "M28": "CONTESTED",
        }
        return mapping[sid]

    def _experience(
        self, request: CognitiveMemoryExperienceInputV1
    ) -> ExperienceCandidateV1:
        sid = request.scenario_id
        return ExperienceCandidateV1(
            experience_candidate_id=f"experience:{sid}",
            cycle_id=request.cycle_id,
            root_cycle_trace_id=request.root_cycle_trace_id,
            timestamp_or_temporal_ref=f"time:{sid}",
            context_refs=request.context_refs,
            field_refs=request.field_refs,
            pcn_refs=request.pcn_refs,
            intent_refs=request.intent_refs,
            attention_refs=request.attention_refs,
            hypothesis_refs=request.hypothesis_refs,
            current_world_ref=request.current_world_ref,
            cognitive_state_vector_ref=request.cognitive_state_vector_ref,
            regulation_candidate_ref=request.regulation_candidate_ref,
            causal_refs=request.causal_refs,
            decision_refs_optional=request.decision_refs_optional,
            action_refs_optional=request.action_refs_optional,
            execution_result_refs_optional=request.execution_result_refs_optional,
            salience_candidate="HIGH"
            if sid in {"M03", "M25"}
            else "LOW"
            if sid == "M04"
            else "MEDIUM",
            uncertainty_refs=(f"uncertainty:{sid}",)
            if sid in {"M05", "M06", "M20", "M28"}
            else tuple(),
            contradiction_refs=(f"contradiction:{sid}",)
            if sid in {"M07", "M26"}
            else tuple(),
            user_feedback_refs=request.user_feedback_refs,
            source_evidence_refs=request.source_evidence_refs,
            provenance_refs=(f"prov:{sid}:experience",),
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
        )

    def _memory(
        self,
        request: CognitiveMemoryExperienceInputV1,
        experience: ExperienceCandidateV1,
    ) -> MemoryCandidateV1:
        sid = request.scenario_id
        sensitivity = (
            "HIGH_SENSITIVITY"
            if sid in {"M16", "M25"}
            else "SENSITIVE"
            if sid in {"M14", "M15"}
            else "NORMAL"
        )
        return MemoryCandidateV1(
            memory_candidate_id=f"memory:{sid}",
            memory_type=self._memory_type(sid),
            source_experience_candidate_refs=(experience.experience_candidate_id,),
            cycle_refs=(request.cycle_id,),
            salience_candidate=experience.salience_candidate,
            retention_candidate="STRONG"
            if sid in {"M03", "M12"}
            else "WEAK"
            if sid in {"M04", "M11", "M27"}
            else "MEDIUM",
            decay_candidate="FAST" if sid in {"M04", "M11", "M27"} else "SLOW",
            refresh_candidate="ELIGIBLE" if sid in {"M02", "M24"} else "NONE",
            revision_parent_ref=f"memory:{sid}:old" if sid == "M09" else None,
            superseded_ref=f"memory:{sid}:prior" if sid == "M08" else None,
            revocation_ref=f"memory:{sid}:revoked" if sid in {"M07", "M10"} else None,
            uncertainty_refs=experience.uncertainty_refs,
            contradiction_refs=experience.contradiction_refs,
            privacy_sensitivity_level=sensitivity,
            requires_user_confirmation=sid in {"M12", "M14", "M15", "M16", "M25"},
            do_not_persist_candidate=sid
            in {"M04", "M05", "M06", "M11", "M13", "M20", "M25", "M27", "M28"},
            future_retrieval_eligibility="ELIGIBLE"
            if sid not in {"M11", "M13", "M27"}
            else "NOT_ELIGIBLE",
            provenance_refs=(f"prov:{sid}:memory",),
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
        )

    def _admission_decision(
        self, request: CognitiveMemoryExperienceInputV1, memory: MemoryCandidateV1
    ) -> MemoryAdmissionDecisionCandidateV1:
        sid = request.scenario_id
        state = self._admission(sid)
        reasons = [state.lower()]
        if sid in {"M12", "M25"}:
            reasons.append("user_confirmation_required")
        if sid in {"M07", "M26"}:
            reasons.append("contradiction_present")
        return MemoryAdmissionDecisionCandidateV1(
            decision_id=f"decision:{sid}",
            memory_candidate_ref=memory.memory_candidate_id,
            admission_state=state,
            evidence_sufficiency="HIGH"
            if sid not in {"M04", "M05", "M06", "M13", "M23"}
            else "LOW",
            provenance_completeness="COMPLETE",
            uncertainty_level="HIGH" if sid in {"M05", "M06", "M28"} else "LOW",
            contradiction_level="HIGH" if sid in {"M07", "M26"} else "NONE",
            repetition_level="REPEATED" if sid in {"M02", "M23"} else "SINGLE",
            salience_level=memory.salience_candidate,
            temporal_validity="EXPIRED" if sid in {"M11", "M27"} else "ACTIVE",
            authority_status="OK",
            decision_reasons=tuple(reasons),
            trace_ref=f"trace:{sid}:admission",
        )

    def _persistence_handoff(
        self, sid: str, memory: MemoryCandidateV1
    ) -> FuturePersistenceHandoffCandidateV1:
        return FuturePersistenceHandoffCandidateV1(
            handoff_id=f"handoff:{sid}:persistence",
            memory_candidate_ref=memory.memory_candidate_id,
            persistence_target_kind="FUTURE_STORAGE_ADAPTER",
            trace_ref=f"trace:{sid}:persistence_handoff",
        )

    def _trace(
        self,
        request: CognitiveMemoryExperienceInputV1,
        experience: ExperienceCandidateV1,
        memory: MemoryCandidateV1,
    ) -> CognitiveMemoryExperienceTraceV1:
        sid = request.scenario_id
        reverse_lookup = {
            memory.memory_candidate_id: (
                experience.experience_candidate_id,
                request.cycle_id,
                *request.source_evidence_refs,
            ),
            experience.experience_candidate_id: (
                request.cycle_id,
                *request.source_evidence_refs,
            ),
        }
        return CognitiveMemoryExperienceTraceV1(
            root_cycle_trace_id=request.root_cycle_trace_id,
            cycle_id=request.cycle_id,
            experience_candidate_id=experience.experience_candidate_id,
            memory_candidate_id=memory.memory_candidate_id,
            source_context_refs=request.context_refs,
            source_field_refs=request.field_refs,
            source_intent_refs=request.intent_refs,
            source_hypothesis_refs=request.hypothesis_refs,
            current_world_ref=request.current_world_ref,
            regulation_ref=request.regulation_candidate_ref,
            decision_action_execution_refs_optional=request.decision_refs_optional
            + request.action_refs_optional
            + request.execution_result_refs_optional,
            user_feedback_refs=request.user_feedback_refs,
            contradiction_refs=experience.contradiction_refs,
            revision_parent_ref=memory.revision_parent_ref,
            superseded_ref=memory.superseded_ref,
            revocation_ref=memory.revocation_ref,
            provenance_refs=(f"prov:{sid}:trace",),
            admission_trace=(f"trace:{sid}:admission",),
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
            reverse_lookup=reverse_lookup,
        )

    def _provenance(
        self,
        request: CognitiveMemoryExperienceInputV1,
        experience: ExperienceCandidateV1,
        memory: MemoryCandidateV1,
    ) -> CognitiveMemoryExperienceProvenanceV1:
        return CognitiveMemoryExperienceProvenanceV1(
            memory_candidate_ref=memory.memory_candidate_id,
            experience_candidate_ref=experience.experience_candidate_id,
            cycle_ref=request.cycle_id,
            source_evidence_refs=request.source_evidence_refs,
            reverse_locatable=True,
            source_owner_mutation=False,
        )

    def _negative_guards(self) -> NegativeGuardStatusV1:
        return NegativeGuardStatusV1(**NEGATIVE_GUARDS)

    def run_case(
        self, request: CognitiveMemoryExperienceInputV1
    ) -> CognitiveMemoryExperienceOutputV1:
        sid = request.scenario_id
        experience = self._experience(request)
        memory = self._memory(request, experience)
        decision = self._admission_decision(request, memory)
        persistence = self._persistence_handoff(sid, memory)

        retrieval = None
        if sid in {"M17", "M26", "M27"}:
            retrieval = MemoryRetrievalCandidateV1(
                memory_ref=memory.memory_candidate_id,
                retrieval_reason=f"retrieval:{sid}",
                relevance_candidate="MEDIUM",
                confidence_reference_status="REFERENCE_ONLY",
                temporal_status="STALE" if sid == "M27" else "ACTIVE",
                contradiction_refs=experience.contradiction_refs,
                provenance_refs=(f"prov:{sid}:retrieval",),
            )

        pcn_influence = (
            MemoryInfluenceCandidateV1(
                influence_id=f"influence:{sid}:pcn",
                target_owner="Personal Cognitive Network Governance",
                target_kind="PCN_INFLUENCE_REFERENCE",
                memory_refs=(memory.memory_candidate_id,),
                experience_refs=(experience.experience_candidate_id,),
                influence_reason="pcn_influence",
            )
            if sid == "M18"
            else None
        )

        intent_influence = (
            MemoryInfluenceCandidateV1(
                influence_id=f"influence:{sid}:intent",
                target_owner="Intent Governance",
                target_kind="INTENT_INFLUENCE_REFERENCE",
                memory_refs=(memory.memory_candidate_id,),
                experience_refs=(experience.experience_candidate_id,),
                influence_reason="intent_influence",
            )
            if sid == "M19"
            else None
        )

        state_form_influence = (
            MemoryInfluenceCandidateV1(
                influence_id=f"influence:{sid}:state_formation",
                target_owner="Cognitive State Formation Governance",
                target_kind="STATE_FORMATION_INFLUENCE_REFERENCE",
                memory_refs=(memory.memory_candidate_id,),
                experience_refs=(experience.experience_candidate_id,),
                influence_reason="state_formation_influence",
            )
            if sid == "M20"
            else None
        )

        regulation_influence = (
            MemoryInfluenceCandidateV1(
                influence_id=f"influence:{sid}:regulation",
                target_owner="Dynamic Cognitive Regulation Governance",
                target_kind="REGULATION_HISTORY_REFERENCE",
                memory_refs=(memory.memory_candidate_id,),
                experience_refs=(experience.experience_candidate_id,),
                influence_reason="regulation_history",
            )
            if sid == "M21"
            else None
        )

        learning = (
            LearningEvidenceCandidateV1(
                learning_evidence_id=f"learning:{sid}",
                memory_refs=(memory.memory_candidate_id,),
                experience_refs=(experience.experience_candidate_id,),
            )
            if sid == "M22"
            else None
        )

        self_evidence = (
            SelfPersonalityEvolutionEvidenceCandidateV1(
                evidence_id=f"self_evidence:{sid}",
                memory_refs=(memory.memory_candidate_id,),
                experience_refs=(experience.experience_candidate_id,),
            )
            if sid == "M16"
            else None
        )

        revision = (
            MemoryRevisionCandidateV1(
                revision_id=f"revision:{sid}",
                prior_memory_candidate_ref=f"memory:{sid}:old",
                new_memory_candidate_ref=memory.memory_candidate_id,
                reason="updated_evidence",
                trace_ref=f"trace:{sid}:revision",
            )
            if sid == "M09"
            else None
        )

        supersession = (
            MemorySupersessionCandidateV1(
                supersession_id=f"supersession:{sid}",
                superseded_memory_candidate_ref=f"memory:{sid}:prior",
                superseding_memory_candidate_ref=memory.memory_candidate_id,
                reason="newer_context_better_fit",
                trace_ref=f"trace:{sid}:supersession",
            )
            if sid == "M08"
            else None
        )

        revocation = (
            MemoryRevocationCandidateV1(
                revocation_id=f"revocation:{sid}",
                memory_candidate_ref=memory.memory_candidate_id,
                reason="source_revoked",
                contradiction_refs=experience.contradiction_refs,
                trace_ref=f"trace:{sid}:revocation",
            )
            if sid in {"M07", "M10", "M26"}
            else None
        )

        expiration = (
            MemoryExpirationCandidateV1(
                expiration_id=f"expiration:{sid}",
                memory_candidate_ref=memory.memory_candidate_id,
                temporal_reason="stale_or_expired",
                trace_ref=f"trace:{sid}:expiration",
            )
            if sid in {"M11", "M27"}
            else None
        )

        return CognitiveMemoryExperienceOutputV1(
            scenario_id=sid,
            experience_candidate=experience,
            memory_candidate=memory,
            admission_decision_candidate=decision,
            persistence_handoff_candidate=persistence,
            retrieval_candidate=retrieval,
            pcn_influence_candidate=pcn_influence,
            intent_influence_candidate=intent_influence,
            state_formation_influence_candidate=state_form_influence,
            dynamic_regulation_influence_candidate=regulation_influence,
            learning_evidence_candidate=learning,
            self_personality_evidence_candidate=self_evidence,
            revision_candidate=revision,
            supersession_candidate=supersession,
            revocation_candidate=revocation,
            expiration_candidate=expiration,
            trace=self._trace(request, experience, memory),
            provenance=self._provenance(request, experience, memory),
            negative_guard_status=self._negative_guards(),
            synthetic_only=True,
            candidate_only=True,
            runtime_execution=False,
            source_owner_mutation=False,
        )
