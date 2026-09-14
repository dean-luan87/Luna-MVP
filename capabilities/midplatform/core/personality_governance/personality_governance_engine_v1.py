"""Deterministic candidate-only Personality Governance engine."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

from .personality_admission_types_v1 import (
    PersonalityAdmissionDecisionCandidateV1,
    PersonalityEvidenceCandidateV1,
    PersonalityUserCorrectionCandidateV1,
)
from .personality_governance_ownership_guard_v1 import validate_input_ownership
from .personality_governance_registry_v1 import (
    ADMISSION_STATES,
    CANONICAL_OWNER,
    CONTRACT_VERSION,
    NEGATIVE_GUARDS,
    SCHEMA_VERSION,
    SEMANTIC_COMPRESSION_STATUS,
    STABILITY_STATES,
)
from .personality_influence_types_v1 import (
    EmotionToPersonalityEvidenceCandidateV1,
    PersonalityEvidenceHandoffCandidateV1,
    PersonalityToEmotionContextCandidateV1,
)
from .personality_io_types_v1 import PersonalityGovernanceInputV1, PersonalityGovernanceOutputV1, PersonalityNegativeGuardStatusV1
from .personality_profile_types_v1 import PersonalityProfileCandidateV1, PersonalityProfileUpdateCandidateV1
from .personality_revision_types_v1 import (
    PersonalityExpirationCandidateV1,
    PersonalityRevisionCandidateV1,
    PersonalityRevocationCandidateV1,
    PersonalitySupersessionCandidateV1,
)
from .personality_stability_types_v1 import PersonalityStabilityAssessmentCandidateV1
from .personality_trace_types_v1 import PersonalityProvenanceV1, PersonalityTraceV1
from .personality_trait_types_v1 import PersonalityTraitCandidateV1


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(values))


class PersonalityGovernanceEngineV1:
    """Produce immutable candidates without hidden mutable state or side effects."""

    def run_case(self, request: PersonalityGovernanceInputV1) -> PersonalityGovernanceOutputV1:
        input_issues = validate_input_ownership(request)
        trait_id = f"trait:{request.scenario_id}:{request.trait_dimension}:{request.trait_value_candidate}"
        trace_id = f"trace:personality:{request.scenario_id}"
        cycle_ref = f"cycle:{request.scenario_id}"
        source_refs = _unique(request.source_refs)
        evidence_refs = _unique(request.evidence_refs)
        duplicate_evidence = request.duplicate_evidence or len(evidence_refs) != len(request.evidence_refs)
        stability = self._stability(request)
        admission_state = self._admission_state(request)
        sensitivity = request.sensitivity

        evidence = PersonalityEvidenceCandidateV1(
            evidence_id=f"personality-evidence:{request.scenario_id}",
            evidence_kind=request.evidence_kind,
            source_refs=source_refs,
            memory_refs=_unique(request.memory_refs),
            learning_refs=_unique(request.learning_refs),
            self_refs=_unique(request.self_refs),
            emotion_refs=_unique(request.emotion_refs),
            regulation_refs=_unique(request.regulation_refs),
            interaction_refs=_unique(request.interaction_refs),
            context_refs=_unique(request.context_refs),
            uncertainty_refs=_unique(request.uncertainty_refs),
            contradiction_refs=_unique(request.contradiction_refs),
            counterexample_refs=_unique(request.counterexample_refs),
            sensitivity=sensitivity,
            temporal_span=request.temporal_span,
            repetition=request.repetition,
            user_correction=request.user_correction,
            user_confirmed=request.user_confirmed,
            trace_ref=trace_id,
            provenance_refs=(f"provenance:{request.scenario_id}",),
            admission_state=admission_state,
        )

        trait = PersonalityTraitCandidateV1(
            trait_candidate_id=trait_id,
            trait_dimension=request.trait_dimension,
            trait_value_candidate=request.trait_value_candidate,
            source_refs=source_refs,
            evidence_refs=evidence_refs,
            memory_refs=_unique(request.memory_refs),
            learning_refs=_unique(request.learning_refs),
            self_refs=_unique(request.self_refs),
            emotion_refs=_unique(request.emotion_refs),
            regulation_refs=_unique(request.regulation_refs),
            interaction_refs=_unique(request.interaction_refs),
            confidence_candidate=request.confidence_candidate,
            evidence_strength=request.evidence_strength,
            repetition=request.repetition,
            context_diversity=len(_unique(request.context_refs)),
            temporal_span=request.temporal_span,
            stability_candidate=stability,
            uncertainty_refs=_unique(request.uncertainty_refs),
            contradiction_refs=_unique(request.contradiction_refs),
            counterexample_refs=_unique(request.counterexample_refs),
            revision_parent_ref=request.revision_parent_ref,
            supersedes_ref=request.supersedes_ref,
            revocation_refs=_unique(request.revocation_refs),
            sensitivity=sensitivity,
            trace_ref=trace_id,
            provenance_refs=(f"provenance:{request.scenario_id}",),
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
        )

        profile = self._profile(request, trait, trace_id)
        profile_update = self._profile_update(request, profile, trace_id)
        stability_assessment = PersonalityStabilityAssessmentCandidateV1(
            assessment_id=f"stability:{request.scenario_id}",
            trait_candidate_ref=trait_id,
            stability_candidate=stability,
            repetition=request.repetition,
            context_diversity=trait.context_diversity,
            temporal_span=request.temporal_span,
            contradiction_refs=trait.contradiction_refs,
            counterexample_refs=trait.counterexample_refs,
            reason_codes=self._stability_reasons(request, stability),
        )
        admission = PersonalityAdmissionDecisionCandidateV1(
            decision_id=f"admission:{request.scenario_id}",
            evidence_ref=evidence.evidence_id,
            trait_candidate_ref=trait_id,
            admission_state=admission_state,
            reason_codes=self._admission_reasons(request, admission_state),
            user_correction_precedence=request.user_correction or request.user_confirmed,
            duplicate_evidence_guard_triggered=duplicate_evidence,
        )

        revision = None
        if request.revision_parent_ref is not None or request.user_correction:
            revision = PersonalityRevisionCandidateV1(
                revision_id=f"revision:{request.scenario_id}",
                prior_candidate_ref=request.revision_parent_ref or trait_id,
                revised_candidate_ref=trait_id,
                reason_codes=("explicit_user_correction",) if request.user_correction else ("new_evidence",),
                correction_precedence=request.user_correction,
                trace_ref=trace_id,
            )
        supersession = None
        if request.supersedes_ref is not None:
            supersession = PersonalitySupersessionCandidateV1(
                supersession_id=f"supersession:{request.scenario_id}",
                superseded_candidate_ref=request.supersedes_ref,
                superseding_candidate_ref=trait_id,
                trace_ref=trace_id,
            )
        revocation = None
        if request.revocation_refs:
            revocation = PersonalityRevocationCandidateV1(
                revocation_id=f"revocation:{request.scenario_id}",
                revoked_candidate_ref=trait_id,
                revocation_refs=_unique(request.revocation_refs),
                trace_ref=trace_id,
            )
        expiration = None
        if request.expired:
            expiration = PersonalityExpirationCandidateV1(
                expiration_id=f"expiration:{request.scenario_id}",
                expired_candidate_ref=trait_id,
                temporal_scope=f"scenario:{request.scenario_id}",
                trace_ref=trace_id,
            )
        correction = None
        if request.user_correction:
            correction = PersonalityUserCorrectionCandidateV1(
                correction_id=f"correction:{request.scenario_id}",
                target_candidate_ref=request.revision_parent_ref or trait_id,
                correction_ref=f"user-correction:{request.scenario_id}",
            )

        emotion_to_personality = None
        personality_to_emotion = None
        if request.emotion_refs:
            emotion_to_personality = EmotionToPersonalityEvidenceCandidateV1(
                influence_id=f"emotion-to-personality:{request.scenario_id}",
                source_owner="Emotion Governance",
                source_refs=_unique(request.emotion_refs),
                evidence_kind="emotion_evidence_reference",
                trace_ref=trace_id,
                provenance_refs=(f"provenance:{request.scenario_id}",),
                emotion_refs=_unique(request.emotion_refs),
            )
            personality_to_emotion = PersonalityToEmotionContextCandidateV1(
                context_id=f"personality-to-emotion:{request.scenario_id}",
                personality_candidate_refs=(trait_id,),
                emotion_context_refs=_unique(request.emotion_refs),
            )

        handoffs = self._handoffs(request, evidence, trace_id)
        profile_refs = (profile.profile_candidate_id,) if profile else ()
        trace = PersonalityTraceV1(
            trace_id=trace_id,
            root_cycle_trace_id=f"root:{cycle_ref}",
            cognitive_cycle_ref=cycle_ref,
            personality_evidence_refs=(evidence.evidence_id,),
            trait_candidate_refs=(trait_id,),
            profile_candidate_refs=profile_refs,
            source_refs=source_refs,
            memory_refs=_unique(request.memory_refs),
            learning_refs=_unique(request.learning_refs),
            self_refs=_unique(request.self_refs),
            emotion_refs=_unique(request.emotion_refs),
            regulation_refs=_unique(request.regulation_refs),
            pcn_refs=_unique(ref for ref in request.context_refs if ref.startswith("pcn:")),
            contradiction_refs=trait.contradiction_refs,
            counterexample_refs=trait.counterexample_refs,
            revision_refs=(revision.revision_id,) if revision else (),
            supersession_refs=(supersession.supersession_id,) if supersession else (),
            revocation_refs=(revocation.revocation_id,) if revocation else (),
            expiration_refs=(expiration.expiration_id,) if expiration else (),
        )
        provenance = PersonalityProvenanceV1(
            provenance_id=f"provenance:{request.scenario_id}",
            source_owner="Personality Evidence Gateway",
            original_source_refs=source_refs,
            evidence_refs=evidence_refs,
            owner_trace_refs=(trace_id, cycle_ref),
        )
        guard_status = PersonalityNegativeGuardStatusV1(tuple(NEGATIVE_GUARDS.items()))
        output = PersonalityGovernanceOutputV1(
            scenario_id=request.scenario_id,
            evidence=evidence,
            trait_candidate=trait,
            profile_candidate=profile,
            stability_assessment=stability_assessment,
            admission_decision=admission,
            revision_candidate=revision,
            supersession_candidate=supersession,
            revocation_candidate=revocation,
            expiration_candidate=expiration,
            user_correction_candidate=correction,
            emotion_to_personality_candidate=emotion_to_personality,
            personality_to_emotion_candidate=personality_to_emotion,
            evidence_handoff_candidates=handoffs,
            profile_update_candidate=profile_update,
            trace=trace,
            provenance=provenance,
            negative_guard_status=guard_status,
            semantic_compression_status=SEMANTIC_COMPRESSION_STATUS,
            issues=tuple(f"{issue.code}:{issue.message}" for issue in input_issues),
        )
        return output

    def _stability(self, request: PersonalityGovernanceInputV1) -> str:
        if request.expired:
            return "EXPIRED"
        if request.revocation_refs:
            return "REVOKED"
        if request.user_correction or request.revision_parent_ref:
            return "REVISING"
        if request.contradiction_refs:
            return "CONTESTED"
        if request.counterexample_refs:
            return "TENTATIVE"
        if request.uncertainty_refs:
            return "EMERGING"
        if request.repetition <= 1:
            return "EMERGING"
        context_count = len(_unique(request.context_refs))
        if request.sensitivity == "DO_NOT_GENERALIZE" or context_count <= 1:
            return "TENTATIVE"
        if request.repetition >= 4 and request.temporal_span >= 3:
            return "STABLE_CANDIDATE"
        return "SEMI_STABLE"

    def _admission_state(self, request: PersonalityGovernanceInputV1) -> str:
        if request.expired:
            return "EXPIRED"
        if request.revocation_refs:
            return "REVOKED"
        if request.user_correction or request.revision_parent_ref:
            return "REVISED"
        if request.contradiction_refs:
            return "CONTESTED"
        if request.sensitivity in {"HIGH_SENSITIVITY", "USER_CONFIRMATION_REQUIRED"} and not request.user_confirmed:
            return "NEEDS_CONFIRMATION"
        if request.uncertainty_refs and not request.user_confirmed:
            return "NEEDS_CONFIRMATION"
        if request.counterexample_refs:
            return "EVIDENCE_ACCUMULATING"
        if request.repetition <= 1:
            return "INSUFFICIENT_EVIDENCE"
        if request.user_confirmed and len(_unique(request.context_refs)) >= 2 and request.temporal_span >= 3 and request.repetition >= 2:
            return "ADMITTED_CANDIDATE"
        if len(_unique(request.context_refs)) >= 2 and request.temporal_span >= 3 and request.repetition >= 4:
            return "ADMITTED_CANDIDATE"
        return "EVIDENCE_ACCUMULATING"

    def _stability_reasons(self, request: PersonalityGovernanceInputV1, stability: str) -> Tuple[str, ...]:
        reasons = []
        if request.repetition <= 1:
            reasons.append("single_event_insufficient")
        if len(_unique(request.context_refs)) <= 1:
            reasons.append("context_diversity_limited")
        if request.temporal_span < 3:
            reasons.append("temporal_span_limited")
        if request.counterexample_refs:
            reasons.append("counterexample_retained")
        if request.contradiction_refs:
            reasons.append("contradiction_preserved")
        if request.user_correction:
            reasons.append("user_correction_precedence")
        reasons.append(f"stability:{stability}")
        return tuple(reasons)

    def _admission_reasons(self, request: PersonalityGovernanceInputV1, state: str) -> Tuple[str, ...]:
        reasons = [f"admission:{state}"]
        if request.user_correction:
            reasons.append("explicit_user_correction_precedence")
        if request.uncertainty_refs:
            reasons.append("uncertainty_preserved")
        if request.contradiction_refs:
            reasons.append("contradiction_preserved")
        if request.counterexample_refs:
            reasons.append("counterexample_preserved")
        return tuple(reasons)

    def _profile(self, request: PersonalityGovernanceInputV1, trait: PersonalityTraitCandidateV1, trace_id: str) -> Optional[PersonalityProfileCandidateV1]:
        if not request.profile_dimensions:
            return None
        extra_refs = tuple(f"trait:{request.scenario_id}:{dimension}:candidate" for dimension in request.profile_dimensions if dimension != request.trait_dimension)
        trait_refs = _unique((trait.trait_candidate_id, *request.profile_trait_refs, *extra_refs))
        uncertain_refs = (trait.trait_candidate_id,) if request.uncertainty_refs else ()
        contested_refs = (trait.trait_candidate_id,) if request.contradiction_refs else ()
        groups = ((trait.trait_candidate_id, *request.profile_trait_refs),) if request.contradiction_refs else ()
        return PersonalityProfileCandidateV1(
            profile_candidate_id=f"profile:{request.scenario_id}",
            trait_candidate_refs=trait_refs,
            uncertain_trait_refs=uncertain_refs,
            contested_trait_refs=contested_refs,
            contradictory_trait_groups=groups,
            context_scope_refs=_unique(request.profile_context_refs or request.context_refs),
            temporal_scope=f"span:{request.temporal_span}",
            confidence_candidate=request.confidence_candidate,
            stability_summary_candidate=trait.stability_candidate,
            revision_parent_ref=request.revision_parent_ref,
            supersedes_ref=request.supersedes_ref,
            revocation_refs=trait.revocation_refs,
            trace_ref=trace_id,
            provenance_refs=trait.provenance_refs,
            sensitivity=trait.sensitivity,
        )

    def _profile_update(self, request: PersonalityGovernanceInputV1, profile: Optional[PersonalityProfileCandidateV1], trace_id: str) -> Optional[PersonalityProfileUpdateCandidateV1]:
        if profile is None or not request.duplicate_profile_update:
            return None
        return PersonalityProfileUpdateCandidateV1(
            update_id=f"profile-update:{request.scenario_id}",
            prior_profile_ref=profile.profile_candidate_id,
            next_profile_ref=profile.profile_candidate_id,
            changed_trait_refs=profile.trait_candidate_refs,
            duplicate_guard_triggered=True,
            trace_ref=trace_id,
        )

    def _handoffs(self, request: PersonalityGovernanceInputV1, evidence: PersonalityEvidenceCandidateV1, trace_id: str) -> Tuple[PersonalityEvidenceHandoffCandidateV1, ...]:
        source_groups = (
            ("Self Governance", request.self_refs),
            ("Cognitive Memory & Experience Governance", request.memory_refs),
            ("Cognitive Learning Governance", request.learning_refs),
            ("Dynamic Cognitive Regulation Governance", request.regulation_refs),
            ("Personal Cognitive Network Governance", tuple(ref for ref in request.context_refs if ref.startswith("pcn:"))),
            ("Intent Governance", tuple(ref for ref in request.context_refs if ref.startswith("intent:"))),
        )
        return tuple(
            PersonalityEvidenceHandoffCandidateV1(
                handoff_id=f"handoff:{request.scenario_id}:{index}",
                producer_owner=owner,
                consumer_owner=CANONICAL_OWNER,
                evidence_refs=_unique(refs),
                trace_ref=trace_id,
                provenance_refs=(f"provenance:{request.scenario_id}",),
            )
            for index, (owner, refs) in enumerate(source_groups)
            if refs
        )
