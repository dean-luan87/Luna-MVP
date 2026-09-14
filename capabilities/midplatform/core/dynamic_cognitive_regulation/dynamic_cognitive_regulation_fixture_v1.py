"""Deterministic synthetic R01-R20 fixtures frozen by planning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_bounds_types_v1 import (
    CognitiveParameterBoundsV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_genome_types_v1 import (
    CognitiveParameterGenomeCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_types_v1 import (
    CognitiveParameterCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_core_types_v1 import (
    RegulationPolicyRefV1,
    SourceRefV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_io_types_v1 import (
    CognitiveStateVectorInputCandidateV1,
    DynamicCognitiveRegulationInputV1,
)


@dataclass(frozen=True)
class DynamicRegulationFixtureCaseV1:
    scenario_id: str
    name: str
    expected_behavior: str
    request: DynamicCognitiveRegulationInputV1
    expected_status: str
    expected_reason_tokens: Tuple[str, ...] = ()
    expected_influence_kinds: Tuple[str, ...] = ()
    synthetic_only: bool = True


def _ref(owner: str, scenario_id: str, ref_type: str) -> SourceRefV1:
    return SourceRefV1(
        owner=owner,
        ref_id=f"{ref_type.lower()}:{scenario_id}",
        ref_type=ref_type,
        trace_ref=f"source-trace:{scenario_id}:{ref_type.lower()}",
        provenance_ref=f"source-prov:{scenario_id}:{ref_type.lower()}",
    )


def _parameter(
    scenario_id: str,
    kind: str,
    current: float,
    requested: object,
    parameter_class: str = "C",
    *,
    approved: bool = True,
    human_confirmed: bool = True,
    expired: bool = False,
    learning: bool = False,
    suffix: str = "1",
) -> CognitiveParameterCandidateV1:
    parameter_id = f"parameter:{scenario_id}:{kind}:{suffix}"
    return CognitiveParameterCandidateV1(
        parameter_id=parameter_id,
        parameter_kind=kind,
        parameter_class=parameter_class,
        current_value=current,
        requested_value=requested,
        field_scope=f"synthetic-field:{scenario_id}",
        evidence_refs=(f"evidence:{scenario_id}:{kind}:{suffix}",),
        policy_ref=f"policy:{scenario_id}",
        trace_ref=f"parameter-trace:{scenario_id}:{kind}:{suffix}",
        parameter_version="1.0-candidate",
        owner_approved=approved,
        human_confirmed=human_confirmed,
        expiry_ref=(f"expiry:{scenario_id}" if parameter_class == "D" else None),
        expired=expired,
        learning_update_candidate=learning,
    )


def _bounds(
    parameter: CognitiveParameterCandidateV1,
    lower: float = 0.0,
    upper: float = 1.0,
    step: float = 0.25,
) -> CognitiveParameterBoundsV1:
    return CognitiveParameterBoundsV1(
        bounds_id=f"bounds:{parameter.parameter_id}",
        parameter_id=parameter.parameter_id,
        parameter_class=parameter.parameter_class,
        lower_bound=lower,
        upper_bound=upper,
        step_bound=step,
        policy_ref=parameter.policy_ref,
        trace_ref=f"bounds-trace:{parameter.parameter_id}",
    )


def _request(
    scenario_id: str,
    parameters: Tuple[CognitiveParameterCandidateV1, ...],
    *,
    stale: bool = False,
    missing_provenance: bool = False,
    include_emotion: bool = False,
    include_intent: bool = False,
    include_learning: bool = False,
    genome: Optional[CognitiveParameterGenomeCandidateV1] = None,
    revision: bool = False,
    revocation: bool = False,
    source_revoked: bool = False,
) -> DynamicCognitiveRegulationInputV1:
    return DynamicCognitiveRegulationInputV1(
        scenario_id=scenario_id,
        cognitive_state_vector_candidate=CognitiveStateVectorInputCandidateV1(
            state_vector_id=f"state-vector:{scenario_id}",
            attention_distribution_refs=(f"attention-state:{scenario_id}",),
            hypothesis_state_refs=(f"hypothesis-state:{scenario_id}",),
            uncertainty_level_candidate="HIGH" if "R03" in scenario_id else "LOW",
            conflict_level_candidate="HIGH" if "R13" in scenario_id else "LOW",
            world_stability_candidate="STALE" if stale else "STABLE_CANDIDATE",
            intent_pressure_candidate="HIGH" if include_intent else "LOW",
            resource_pressure_candidate="HIGH" if "R05" in scenario_id else "LOW",
            trace_ref=f"state-vector-trace:{scenario_id}",
            provenance_refs=(
                () if missing_provenance else (f"state-vector-prov:{scenario_id}",)
            ),
            stale=stale,
        ),
        context_refs=(_ref("Context Governance", scenario_id, "CONTEXT"),),
        pcn_refs=(
            _ref("Personal Cognitive Network Governance", scenario_id, "PCN"),
        ),
        intent_refs=(
            (_ref("Intent Governance", scenario_id, "INTENT"),)
            if include_intent
            else ()
        ),
        hypothesis_refs=(
            _ref("Cognitive State Formation Governance", scenario_id, "HYPOTHESIS"),
        ),
        emotion_refs=(
            (_ref("Emotion / Integration Governance", scenario_id, "EMOTION"),)
            if include_emotion
            else ()
        ),
        resource_refs=(
            _ref("Self Regulation / Runtime Governance", scenario_id, "RESOURCE"),
        ),
        learning_update_refs=(
            (_ref("Selective Learning Governance", scenario_id, "LEARNING_UPDATE"),)
            if include_learning
            else ()
        ),
        policy_refs=(
            RegulationPolicyRefV1(
                policy_id=f"policy:{scenario_id}",
                version="1.0-frozen",
                owner="Dynamic Cognitive Regulation Governance",
                trace_ref=f"policy-trace:{scenario_id}",
            ),
        ),
        parameter_candidates=parameters,
        parameter_bounds=tuple(_bounds(item) for item in parameters),
        genome_candidate=genome,
        prior_regulation_candidate_ref=(
            f"regulation:prior:{scenario_id}"
            if revision or revocation or source_revoked
            else None
        ),
        revision_requested=revision,
        revocation_requested=revocation,
        source_revoked=source_revoked,
    )


def _genome(scenario_id: str, parameters: Tuple[CognitiveParameterCandidateV1, ...]) -> CognitiveParameterGenomeCandidateV1:
    return CognitiveParameterGenomeCandidateV1(
        genome_candidate_id=f"genome-candidate:{scenario_id}",
        version="1.0-candidate",
        parameter_refs=tuple(item.parameter_id for item in parameters),
        parameter_class_refs=tuple(item.parameter_class for item in parameters),
        field_scope=f"synthetic-field:{scenario_id}",
        evidence_refs=(f"evidence:{scenario_id}:learning",),
        risk_refs=(f"risk:{scenario_id}:candidate",),
        rollback_ref=f"rollback:{scenario_id}",
        trace_ref=f"genome-trace:{scenario_id}",
        provenance_refs=(f"genome-prov:{scenario_id}",),
        user_scope_ref=f"synthetic-user:{scenario_id}",
    )


def get_dynamic_regulation_synthetic_fixtures_v1() -> Tuple[DynamicRegulationFixtureCaseV1, ...]:
    r01_params = tuple(
        _parameter("R01", kind, 0.5, 0.5, suffix=str(index))
        for index, kind in enumerate(
            (
                "attention_modulation",
                "salience_modulation",
                "explore_exploit_tendency",
                "confidence_threshold",
                "persistence_decay",
                "resource_allocation",
                "interaction_intensity",
                "reconsideration_sensitivity",
            ),
            start=1,
        )
    )
    r02 = (_parameter("R02", "attention_modulation", 0.5, 0.8),)
    r03 = (_parameter("R03", "explore_exploit_tendency", 0.4, 0.6),)
    r04 = (_parameter("R04", "reconsideration_sensitivity", 0.4, 0.65),)
    r05 = (_parameter("R05", "resource_allocation", 0.7, 0.4),)
    r06 = (_parameter("R06", "interaction_intensity", 0.5, 0.5),)
    r07 = (_parameter("R07", "reconsideration_sensitivity", 0.5, 0.5),)
    r08 = (_parameter("R08", "salience_modulation", 0.8, 1.4),)
    r09 = (_parameter("R09", "persistence_decay", 0.2, -0.4),)
    r10 = (_parameter("R10", "confidence_threshold", 0.5, 0.6, "A"),)
    r11 = (
        _parameter(
            "R11",
            "confidence_threshold",
            0.5,
            0.6,
            "B",
            approved=False,
            human_confirmed=False,
        ),
    )
    r12 = (
        _parameter(
            "R12",
            "interaction_intensity",
            0.4,
            0.6,
            "D",
            expired=True,
        ),
    )
    r13 = (
        _parameter("R13", "attention_modulation", 0.5, 0.7, suffix="a"),
        _parameter("R13", "attention_modulation", 0.5, 0.3, suffix="b"),
    )
    # Preserve a single logical parameter identity so the engine exposes conflict.
    r13 = (
        r13[0],
        CognitiveParameterCandidateV1(
            parameter_id=r13[0].parameter_id,
            parameter_kind=r13[1].parameter_kind,
            parameter_class=r13[1].parameter_class,
            current_value=r13[1].current_value,
            requested_value=r13[1].requested_value,
            field_scope=r13[1].field_scope,
            evidence_refs=r13[1].evidence_refs,
            policy_ref=r13[1].policy_ref,
            trace_ref=r13[1].trace_ref,
            parameter_version=r13[1].parameter_version,
            owner_approved=r13[1].owner_approved,
            human_confirmed=r13[1].human_confirmed,
        ),
    )
    r14 = (_parameter("R14", "attention_modulation", 0.5, 0.6),)
    r15 = (_parameter("R15", "attention_modulation", 0.5, 0.6),)
    r16 = (
        _parameter(
            "R16",
            "confidence_threshold",
            0.5,
            0.7,
            "E",
            approved=False,
            human_confirmed=False,
            learning=True,
        ),
    )
    r17 = (_parameter("R17", "reconsideration_sensitivity", 0.4, 0.6),)
    r18 = (_parameter("R18", "salience_modulation", 0.5, 0.6),)
    r19 = (_parameter("R19", "persistence_decay", 0.5, 0.6),)
    r20 = (_parameter("R20", "attention_modulation", 0.5, 0.65),)

    return (
        DynamicRegulationFixtureCaseV1(
            "R01", "normal_stable_state_no_regulation_needed", "no_change_candidate",
            _request("R01", r01_params), "NO_CHANGE", ("NO_CHANGE",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R02", "attention_overload_bounded_attention_modulation", "attention_modulation_candidate_bounded",
            _request("R02", r02), "CONSTRAINED", (), ("attention_modulation_candidate",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R03", "uncertainty_high_exploration_bias_candidate", "exploration_bias_candidate",
            _request("R03", r03), "BOUNDED_ELIGIBLE", (), ("exploration_exploitation_bias_candidate",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R04", "repeated_unresolved_hypothesis_reconsideration_sensitivity", "reconsideration_sensitivity_candidate",
            _request("R04", r04), "BOUNDED_ELIGIBLE", (), ("reconsideration_sensitivity_candidate",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R05", "resource_pressure_resource_allocation_modulation", "resource_allocation_candidate",
            _request("R05", r05), "CONSTRAINED", (), ("resource_allocation_candidate",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R06", "emotional_spike_influence_no_authority_takeover", "emotion_influence_only",
            _request("R06", r06, include_emotion=True), "NO_CHANGE", ("NO_CHANGE",), ("emotion_aware_modulation_candidate",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R07", "intent_priority_influence_no_intent_mutation", "intent_influence_only",
            _request("R07", r07, include_intent=True), "NO_CHANGE", ("NO_CHANGE",), ("intent_pressure_influence_candidate",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R08", "parameter_reaches_upper_bound", "clamped_upper_bound_with_reason",
            _request("R08", r08), "CONSTRAINED", ("CLAMPED_TO_FROZEN_UPPER_BOUND",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R09", "parameter_reaches_lower_bound", "clamped_lower_bound_with_reason",
            _request("R09", r09), "CONSTRAINED", ("CLAMPED_TO_FROZEN_LOWER_BOUND",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R10", "immutable_parameter_mutation_rejected", "rejected",
            _request("R10", r10), "REJECTED", ("IMMUTABLE_CLASS_A_MUTATION_REJECTED",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R11", "governance_controlled_parameter_requires_approval", "deferred_or_under_review",
            _request("R11", r11), "DEFERRED", ("OWNER_APPROVAL_REQUIRED",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R12", "temporary_parameter_expires", "expired_and_not_reused",
            _request("R12", r12), "EXPIRED_NOT_REUSED", ("TEMPORARY_CLASS_D_EXPIRED_NOT_REUSED",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R13", "conflicting_regulation_candidates_coexist", "conflicts_preserved",
            _request("R13", r13), "CONFLICTS_PRESERVED", ("CONFLICTS_PRESERVED",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R14", "state_vector_stale_regulation_rejected_or_deferred", "rejected_or_deferred",
            _request("R14", r14, stale=True), "DEFERRED", ("STATE_VECTOR_STALE",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R15", "missing_provenance_reject", "rejected",
            _request("R15", r15, missing_provenance=True), "REJECTED", ("STATE_VECTOR_PROVENANCE_MISSING",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R16", "learned_parameter_candidate_cannot_auto_apply", "candidate_only_no_auto_apply",
            _request("R16", r16, include_learning=True, genome=_genome("R16", r16)),
            "CANDIDATE_ONLY_NO_AUTO_APPLY", ("LEARNED_CLASS_E_CANDIDATE_NO_AUTO_APPLY",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R17", "regulation_revision", "revision_lineage_present",
            _request("R17", r17, revision=True), "REVISED", ("REVISION_REQUESTED",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R18", "regulation_revocation", "revocation_lineage_present",
            _request("R18", r18, revocation=True), "REVOKED", ("REVOCATION_REQUESTED",),
        ),
        DynamicRegulationFixtureCaseV1(
            "R19", "duplicate_regulation_candidate_idempotency", "idempotent_result",
            _request("R19", r19), "BOUNDED_ELIGIBLE",
        ),
        DynamicRegulationFixtureCaseV1(
            "R20", "downstream_influence_candidate_handoff", "candidate_only_handoff",
            _request("R20", r20), "BOUNDED_ELIGIBLE", (), ("attention_modulation_candidate",),
        ),
    )
