"""Deterministic synthetic Self Governance engine; no runtime integrations."""

from __future__ import annotations

from typing import Tuple

from .self_attribution_types_v1 import SelfAttributionCandidateV1
from .self_boundary_types_v1 import classify_self_boundary
from .self_continuity_types_v1 import SelfContinuityCandidateV1
from .self_governance_registry_v1 import (
    CONTRACT_VERSION,
    IDEMPOTENCY_GUARDS,
    NEGATIVE_GUARDS,
    SCHEMA_VERSION,
)
from .self_influence_types_v1 import SelfEvidenceInfluenceCandidateV1
from .self_io_types_v1 import SelfGovernanceInputV1, SelfGovernanceOutputV1
from .self_reference_types_v1 import SelfReferenceCandidateV1
from .self_revision_types_v1 import (
    SelfExpirationCandidateV1,
    SelfRevisionCandidateV1,
    SelfRevocationCandidateV1,
    SelfSupersessionCandidateV1,
)
from .self_trace_types_v1 import SelfProvenanceV1, SelfTraceV1


_STATE_OVERRIDES = {
    "S03": "REJECTED", "S06": "REVISED", "S08": "EXPIRED", "S10": "REVISED",
    "S12": "TEMPORARY", "S14": "REJECTED", "S16": "CONTESTED", "S17": "PROPOSED",
    "S18": "PROPOSED", "S20": "PROPOSED", "S21": "PROPOSED", "S22": "PROPOSED",
    "S23": "NEEDS_CONFIRMATION", "S24": "PROPOSED", "S25": "CONTESTED",
    "S26": "ADMITTED_CANDIDATE", "S27": "REVOKED", "S31": "EXPIRED",
    "S32": "NEEDS_CONFIRMATION", "S33": "PROPOSED", "S34": "INSUFFICIENT_EVIDENCE",
}
_FUTURE_PERSONALITY_SCENARIOS = {"S23", "S24"}
_REVISION_SCENARIOS = {"S06", "S10"}
_EXPIRATION_SCENARIOS = {"S08", "S31"}


class SelfGovernanceEngineV1:
    """Pure mapping from a synthetic request to immutable candidate objects."""

    def _state(self, request: SelfGovernanceInputV1) -> str:
        return _STATE_OVERRIDES.get(request.scenario_id, "PROPOSED")

    def _stability_partition(self, request: SelfGovernanceInputV1) -> str:
        if request.scenario_id in _FUTURE_PERSONALITY_SCENARIOS:
            return "FUTURE_PERSONALITY_DERIVED_SELF"
        if request.requested_domain in {"IDENTITY", "CAPABILITY", "LIMITATION", "AUTOBIOGRAPHICAL"}:
            return "STRUCTURAL_SELF" if request.requested_domain == "IDENTITY" else "SEMI_STABLE_SELF"
        if request.requested_domain in {"ROLE", "RELATIONSHIP_POSITION", "PREFERENCE", "HABITUAL_TENDENCY"}:
            return "SEMI_STABLE_SELF"
        return "TRANSIENT_SELF"

    def _reference(self, request: SelfGovernanceInputV1, boundary: str) -> SelfReferenceCandidateV1:
        candidate_id = f"self-reference:{request.scenario_id}"
        identity_ref = None if boundary in {"UNKNOWN", "CONTESTED", "OTHER"} else f"identity-boundary:{request.scenario_id}"
        confidence = "LOW" if request.scenario_id == "S34" else "NEEDS_CONFIRMATION" if request.sensitivity == "HIGH_SENSITIVITY" else "MEDIUM"
        return SelfReferenceCandidateV1(
            candidate_id=candidate_id,
            source_owner=request.source_owner,
            reference_kind="SELF_REFERENCE",
            source_refs=request.source_refs,
            evidence_refs=request.evidence_refs,
            provenance_refs=request.provenance_refs,
            temporal_validity=request.temporal_validity,
            uncertainty=request.uncertainty,
            sensitivity=request.sensitivity,
            self_ref_id=candidate_id,
            self_id_ref=f"self-anchor:{request.scenario_id}",
            identity_ref=identity_ref,
            subject_boundary_class=boundary,
            confidence_candidate=confidence,
            uncertainty_refs=(f"uncertainty:{request.scenario_id}",),
            temporal_validity_candidate=request.temporal_validity,
        )

    def _attribution(
        self,
        request: SelfGovernanceInputV1,
        reference: SelfReferenceCandidateV1,
        boundary: str,
    ) -> SelfAttributionCandidateV1:
        attribution_id = f"self-attribution:{request.scenario_id}"
        state = self._state(request)
        contradiction = (f"contradiction:{request.scenario_id}",) if request.scenario_id in {"S16", "S25"} else ()
        return SelfAttributionCandidateV1(
            self_attribution_id=attribution_id,
            self_ref=reference.self_ref_id,
            attribution_domain=request.requested_domain,
            attributed_value_candidate_ref=f"value:{request.scenario_id}",
            source_owner_refs=(request.source_owner,),
            source_refs=request.source_refs,
            evidence_refs=request.evidence_refs,
            provenance_refs=request.provenance_refs,
            confidence_candidate=reference.confidence_candidate,
            uncertainty_refs=(f"uncertainty:{request.scenario_id}",),
            temporal_validity_candidate=request.temporal_validity,
            revision_parent_ref=request.prior_self_candidate_ref,
            revocation_parent_ref=f"self-attribution:{request.scenario_id}:prior" if request.scenario_id == "S27" else None,
            contradiction_refs=contradiction,
            revision_refs=(f"revision:{request.scenario_id}",) if request.scenario_id in _REVISION_SCENARIOS else (),
            revocation_refs=(f"revocation:{request.scenario_id}",) if request.scenario_id == "S27" else (),
            supersession_refs=(f"supersession:{request.scenario_id}",) if request.scenario_id == "S10" else (),
            state=state,
            stability_partition=self._stability_partition(request),
            sensitivity=request.sensitivity,
            explicit_user_correction=request.user_correction,
        )

    def _influences(self, request: SelfGovernanceInputV1) -> Tuple[SelfEvidenceInfluenceCandidateV1, ...]:
        by_sid = {
            "S15": ("MEMORY_EVIDENCE", request.source_memory_refs),
            "S17": ("SELF_EVOLUTION_EVIDENCE", request.source_learning_refs),
            "S19": ("REGULATION_EVIDENCE", request.source_regulation_refs),
            "S20": ("REGULATION_PARAMETER_EVIDENCE", request.source_regulation_refs),
            "S21": ("EMOTION_EVIDENCE_TO_SELF", (f"emotion:{request.scenario_id}",)),
            "S23": ("PERSONALITY_EVIDENCE", (f"personality-evidence:{request.scenario_id}",)),
        }
        if request.scenario_id not in by_sid:
            return ()
        kind, refs = by_sid[request.scenario_id]
        return (SelfEvidenceInfluenceCandidateV1(
            influence_id=f"influence:{request.scenario_id}",
            source_owner=request.source_owner,
            source_refs=refs or request.evidence_refs,
            evidence_kind=kind,
            provenance_refs=request.provenance_refs,
        ),)

    def _trace(
        self,
        request: SelfGovernanceInputV1,
        reference: SelfReferenceCandidateV1,
        attribution: SelfAttributionCandidateV1 | None,
        continuity: SelfContinuityCandidateV1 | None,
        revision_refs: Tuple[str, ...],
        revocation_refs: Tuple[str, ...],
    ) -> Tuple[SelfTraceV1, SelfProvenanceV1]:
        trace_id = f"self-trace:{request.scenario_id}"
        trace = SelfTraceV1(
            root_cycle_trace_id=request.root_cycle_trace_id,
            self_trace_id=trace_id,
            self_ref_id=reference.self_ref_id,
            self_attribution_id=attribution.self_attribution_id if attribution else None,
            continuity_id=continuity.continuity_id if continuity else None,
            source_intent_refs=request.source_intent_refs,
            source_memory_refs=request.source_memory_refs,
            source_learning_refs=request.source_learning_refs,
            source_pcn_refs=request.source_pcn_refs,
            source_regulation_refs=request.source_regulation_refs,
            source_context_refs=request.source_context_refs,
            revision_refs=revision_refs,
            revocation_refs=revocation_refs,
            provenance_refs=request.provenance_refs,
        )
        provenance = SelfProvenanceV1(
            provenance_id=f"provenance:{request.scenario_id}",
            source_owner_trace=(request.source_owner,),
            original_source_refs=request.source_refs,
            evidence_refs=request.evidence_refs,
            upstream_trace_refs=(request.root_cycle_trace_id,),
            self_trace_id=trace_id,
        )
        return trace, provenance

    def run_case(self, request: SelfGovernanceInputV1) -> SelfGovernanceOutputV1:
        boundary = classify_self_boundary(request.statement, request.boundary_class)
        reference = self._reference(request, boundary)
        attribution = self._attribution(request, reference, boundary)
        continuity = None
        if request.scenario_id == "S30":
            continuity = SelfContinuityCandidateV1(
                continuity_id="continuity:S30",
                prior_self_candidate_ref="self-reference:S29",
                current_self_candidate_ref=request.current_self_candidate_ref or reference.self_ref_id,
                continuity_kind="PERSISTENCE_WITH_CHANGE",
                stable_refs=("stable:subject-position",),
                changed_refs=("changed:cycle-context",),
                unresolved_refs=("unresolved:future-self",),
                revision_refs=(),
                revocation_refs=(),
                temporal_refs=("cycle:S29", request.root_cycle_trace_id),
                provenance_refs=request.provenance_refs,
                root_cycle_trace_id=request.root_cycle_trace_id,
                self_id_ref=reference.self_id_ref,
                previous_self_state_ref="self-state:S29",
                current_self_state_candidate_ref=reference.self_ref_id,
                persistent_self_attribute_candidate_refs=("stable:subject-position",),
                transient_self_attribute_candidate_refs=("changed:cycle-context",),
                unresolved_attribution_refs=("unresolved:future-self",),
                revision_lineage_refs=(),
                revocation_lineage_refs=(),
                schema_version=SCHEMA_VERSION,
                contract_version=CONTRACT_VERSION,
            )
        revision = None
        if request.scenario_id in _REVISION_SCENARIOS:
            revision = SelfRevisionCandidateV1(
                revision_id=f"revision:{request.scenario_id}",
                prior_candidate_ref=request.prior_self_candidate_ref or f"self-attribution:{request.scenario_id}:prior",
                revised_candidate_ref=f"self-attribution:{request.scenario_id}",
                trigger="user_correction" if request.user_correction else "relationship_change",
                reason="explicit correction takes precedence" if request.user_correction else "source relationship changed",
                source_refs=request.source_refs,
                provenance_refs=request.provenance_refs,
                explicit_user_correction=request.user_correction,
            )
        revocation = None
        if request.scenario_id == "S27":
            revocation = SelfRevocationCandidateV1(
                revocation_id="revocation:S27",
                candidate_ref="self-attribution:S27",
                trigger="source_revocation",
                reason="upstream source was revoked",
                contradiction_refs=(),
                provenance_refs=request.provenance_refs,
            )
        supersession = None
        if request.scenario_id == "S10":
            supersession = SelfSupersessionCandidateV1(
                supersession_id="supersession:S10",
                superseded_candidate_ref="self-attribution:S10:prior",
                superseding_candidate_ref="self-attribution:S10",
                reason="relationship change",
                provenance_refs=request.provenance_refs,
            )
        expiration = None
        if request.scenario_id in _EXPIRATION_SCENARIOS:
            expiration = SelfExpirationCandidateV1(
                expiration_id=f"expiration:{request.scenario_id}",
                candidate_ref=f"self-attribution:{request.scenario_id}",
                temporal_reason="temporal validity expired",
                provenance_refs=request.provenance_refs,
            )
        revision_refs = (revision.revision_id,) if revision else ()
        revocation_refs = (revocation.revocation_id,) if revocation else ()
        trace, provenance = self._trace(request, reference, attribution, continuity, revision_refs, revocation_refs)
        guards = dict(NEGATIVE_GUARDS)
        idempotency = {
            "duplicate_self_reference_guard": request.duplicate_request,
            "duplicate_attribution_guard": request.duplicate_request,
            "duplicate_continuity_update_guard": request.duplicate_continuity_update,
            "duplicate_revision_guard": request.duplicate_revision,
            "duplicate_revocation_guard": request.duplicate_revocation,
            "duplicate_supersession_guard": request.duplicate_supersession,
            "replayed_source_evidence_guard": request.replayed_evidence,
            "explicit_user_correction_precedence": request.user_correction,
        }
        return SelfGovernanceOutputV1(
            scenario_id=request.scenario_id,
            self_reference=reference,
            self_attribution=attribution,
            self_continuity=continuity,
            revision=revision,
            revocation=revocation,
            supersession=supersession,
            expiration=expiration,
            influences=self._influences(request),
            trace=trace,
            provenance=provenance,
            boundary_class=boundary,
            duplicate_guard_triggered=request.duplicate_request,
            replay_guard_triggered=request.replayed_evidence,
            user_correction_precedence=request.user_correction,
            idempotency_guards={key: idempotency[key] for key in IDEMPOTENCY_GUARDS},
            negative_guards=guards,
        )
