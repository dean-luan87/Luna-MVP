"""Deterministic, inspectable, side-effect-free regulation candidate engine."""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_bounds_types_v1 import (
    CognitiveParameterBoundsV1,
    ParameterBoundsEvaluationV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_types_v1 import (
    CognitiveParameterCandidateV1,
    ParameterConflictCandidateV1,
    ParameterModulationCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_core_types_v1 import (
    NegativeGuardStatusV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_io_types_v1 import (
    DynamicCognitiveRegulationInputV1,
    DynamicCognitiveRegulationOutputV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_registry_v1 import (
    CANONICAL_OWNER,
    MODULE_VERSION,
    PARAMETER_CLASSES,
    REGULATION_FUNCTION_ID,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_candidate_types_v1 import (
    DynamicRegulationCandidateV1,
    InfluenceCandidateV1,
    RegulationRevisionCandidateV1,
    RegulationRevocationCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_handoff_types_v1 import (
    DynamicRegulationHandoffCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_trace_types_v1 import (
    DynamicRegulationProvenanceV1,
    DynamicRegulationTraceV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.self_regulation_state_types_v1 import (
    SelfRegulationStateCandidateV1,
)


INFLUENCE_TARGETS: Dict[str, Tuple[str, str]] = {
    "attention_modulation": (
        "attention_modulation_candidate",
        "Attention Governance",
    ),
    "salience_modulation": (
        "salience_modulation_candidate",
        "Attention Governance",
    ),
    "explore_exploit_tendency": (
        "exploration_exploitation_bias_candidate",
        "Cognitive Processing Governance",
    ),
    "confidence_threshold": (
        "confidence_threshold_candidate",
        "Cognitive State Formation Governance",
    ),
    "persistence_decay": (
        "persistence_decay_candidate",
        "Cognitive State Formation Governance",
    ),
    "resource_allocation": (
        "resource_allocation_candidate",
        "Self Regulation / Runtime Governance",
    ),
    "interaction_intensity": (
        "interaction_intensity_candidate",
        "Social Interaction Governance",
    ),
    "reconsideration_sensitivity": (
        "reconsideration_sensitivity_candidate",
        "Cognitive State Formation Governance",
    ),
}


class DynamicCognitiveRegulationEngineV1:
    """Evaluate immutable synthetic inputs into bounded candidates only."""

    def _evaluate_bounds(
        self,
        parameter: CognitiveParameterCandidateV1,
        bounds: Optional[CognitiveParameterBoundsV1],
    ) -> ParameterBoundsEvaluationV1:
        requested = parameter.requested_value
        if bounds is None:
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=False,
                within_step_bound=False,
                boundary_action="REJECT",
                reason_codes=("MISSING_FROZEN_BOUNDS",),
                rejected=True,
                constrained=False,
            )

        if parameter.parameter_class not in PARAMETER_CLASSES:
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=False,
                within_step_bound=False,
                boundary_action="REJECT",
                reason_codes=("UNKNOWN_PARAMETER_CLASS",),
                rejected=True,
                constrained=False,
            )

        if isinstance(requested, bool) or not isinstance(requested, (int, float)):
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=False,
                within_step_bound=False,
                boundary_action="REJECT",
                reason_codes=("INVALID_NON_NUMERIC_VALUE", "NO_SILENT_COERCION"),
                rejected=True,
                constrained=False,
            )

        requested_float = float(requested)
        if not math.isfinite(requested_float):
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=False,
                within_step_bound=False,
                boundary_action="REJECT",
                reason_codes=("INVALID_NON_FINITE_VALUE", "NO_SILENT_COERCION"),
                rejected=True,
                constrained=False,
            )

        if parameter.parameter_class == "A":
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=(
                    bounds.lower_bound <= requested_float <= bounds.upper_bound
                ),
                within_step_bound=False,
                boundary_action="REJECT",
                reason_codes=("IMMUTABLE_CLASS_A_MUTATION_REJECTED",),
                rejected=True,
                constrained=False,
            )

        if parameter.parameter_class == "E":
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=(
                    bounds.lower_bound <= requested_float <= bounds.upper_bound
                ),
                within_step_bound=False,
                boundary_action="CANDIDATE_ONLY",
                reason_codes=("LEARNED_CLASS_E_CANDIDATE_NO_AUTO_APPLY",),
                rejected=False,
                constrained=True,
            )

        if parameter.parameter_class == "D" and parameter.expired:
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=(
                    bounds.lower_bound <= requested_float <= bounds.upper_bound
                ),
                within_step_bound=False,
                boundary_action="EXPIRE",
                reason_codes=("TEMPORARY_CLASS_D_EXPIRED_NOT_REUSED",),
                rejected=False,
                constrained=True,
            )

        class_policy = PARAMETER_CLASSES[parameter.parameter_class]
        approval_missing = (
            class_policy["owner_approval_required"] and not parameter.owner_approved
        )
        human_missing = (
            class_policy["human_confirmation_required"]
            and not parameter.human_confirmed
        )
        if approval_missing or human_missing:
            reasons: List[str] = []
            if approval_missing:
                reasons.append("OWNER_APPROVAL_REQUIRED")
            if human_missing:
                reasons.append("HUMAN_CONFIRMATION_REQUIRED")
            return ParameterBoundsEvaluationV1(
                parameter_id=parameter.parameter_id,
                requested_value=requested,
                effective_value=None,
                within_absolute_bounds=(
                    bounds.lower_bound <= requested_float <= bounds.upper_bound
                ),
                within_step_bound=False,
                boundary_action="DEFER",
                reason_codes=tuple(reasons),
                rejected=False,
                constrained=True,
            )

        effective = requested_float
        reasons = []
        within_absolute = bounds.lower_bound <= effective <= bounds.upper_bound
        if effective > bounds.upper_bound:
            effective = bounds.upper_bound
            reasons.append("CLAMPED_TO_FROZEN_UPPER_BOUND")
        elif effective < bounds.lower_bound:
            effective = bounds.lower_bound
            reasons.append("CLAMPED_TO_FROZEN_LOWER_BOUND")

        step_delta = effective - float(parameter.current_value)
        within_step = abs(step_delta) <= bounds.step_bound
        if not within_step:
            if step_delta > 0:
                effective = min(
                    float(parameter.current_value) + bounds.step_bound,
                    bounds.upper_bound,
                )
                reasons.append("CONSTRAINED_TO_POSITIVE_STEP_BOUND")
            else:
                effective = max(
                    float(parameter.current_value) - bounds.step_bound,
                    bounds.lower_bound,
                )
                reasons.append("CONSTRAINED_TO_NEGATIVE_STEP_BOUND")

        no_change = effective == float(parameter.current_value)
        boundary_action = "NO_CHANGE" if no_change else "ACCEPT_BOUNDED"
        if reasons:
            boundary_action = "CONSTRAIN_EXPLICITLY"
        return ParameterBoundsEvaluationV1(
            parameter_id=parameter.parameter_id,
            requested_value=requested,
            effective_value=effective,
            within_absolute_bounds=within_absolute,
            within_step_bound=within_step,
            boundary_action=boundary_action,
            reason_codes=tuple(reasons or (("NO_CHANGE",) if no_change else ("WITHIN_FROZEN_BOUNDS",))),
            rejected=False,
            constrained=bool(reasons),
        )

    def _modulation(
        self,
        scenario_id: str,
        index: int,
        parameter: CognitiveParameterCandidateV1,
        bounds: Optional[CognitiveParameterBoundsV1],
        evaluation: ParameterBoundsEvaluationV1,
    ) -> ParameterModulationCandidateV1:
        status = "BOUNDED_ELIGIBLE"
        if evaluation.boundary_action == "NO_CHANGE":
            status = "NO_CHANGE"
        elif evaluation.rejected:
            status = "REJECTED"
        elif evaluation.boundary_action == "DEFER":
            status = "DEFERRED"
        elif evaluation.boundary_action == "EXPIRE":
            status = "EXPIRED_NOT_REUSED"
        elif evaluation.boundary_action == "CANDIDATE_ONLY":
            status = "CANDIDATE_ONLY_NO_AUTO_APPLY"
        elif evaluation.constrained:
            status = "CONSTRAINED"
        return ParameterModulationCandidateV1(
            modulation_id=f"modulation:{scenario_id}:{index}:{parameter.parameter_id}",
            parameter_id=parameter.parameter_id,
            parameter_kind=parameter.parameter_kind,
            parameter_class=parameter.parameter_class,
            requested_value=parameter.requested_value,
            effective_value=evaluation.effective_value,
            prior_value=float(parameter.current_value),
            evaluation_status=status,
            boundary_action=evaluation.boundary_action,
            reason_codes=evaluation.reason_codes,
            evidence_refs=parameter.evidence_refs,
            policy_ref=parameter.policy_ref,
            bounds_ref=(bounds.bounds_id if bounds else "missing-bounds"),
            parameter_version=parameter.parameter_version,
            trace_ref=f"trace:{scenario_id}",
        )

    def _conflicts(
        self,
        scenario_id: str,
        modulations: Sequence[ParameterModulationCandidateV1],
    ) -> Tuple[ParameterConflictCandidateV1, ...]:
        grouped: Dict[str, List[ParameterModulationCandidateV1]] = {}
        for item in modulations:
            grouped.setdefault(item.parameter_id, []).append(item)
        output: List[ParameterConflictCandidateV1] = []
        for parameter_id, items in grouped.items():
            values = {repr(item.requested_value) for item in items}
            if len(items) > 1 and len(values) > 1:
                output.append(
                    ParameterConflictCandidateV1(
                        conflict_id=f"conflict:{scenario_id}:{parameter_id}",
                        parameter_id=parameter_id,
                        modulation_refs=tuple(item.modulation_id for item in items),
                        requested_values=tuple(item.requested_value for item in items),
                    )
                )
        return tuple(output)

    def _influences(
        self,
        scenario_id: str,
        regulation_id: str,
        modulations: Sequence[ParameterModulationCandidateV1],
        request: DynamicCognitiveRegulationInputV1,
    ) -> Tuple[InfluenceCandidateV1, ...]:
        output: List[InfluenceCandidateV1] = []
        for item in modulations:
            if item.effective_value is None or item.evaluation_status in {
                "NO_CHANGE",
                "REJECTED",
                "DEFERRED",
                "EXPIRED_NOT_REUSED",
                "CANDIDATE_ONLY_NO_AUTO_APPLY",
            }:
                continue
            kind, target = INFLUENCE_TARGETS[item.parameter_kind]
            output.append(
                InfluenceCandidateV1(
                    influence_id=f"influence:{scenario_id}:{item.modulation_id}",
                    influence_kind=kind,
                    target_owner=target,
                    source_regulation_ref=regulation_id,
                    parameter_modulation_ref=item.modulation_id,
                    reason_codes=item.reason_codes,
                    trace_ref=f"handoff-trace:{scenario_id}",
                )
            )
        if request.emotion_refs:
            output.append(
                InfluenceCandidateV1(
                    influence_id=f"influence:{scenario_id}:emotion-aware",
                    influence_kind="emotion_aware_modulation_candidate",
                    target_owner="Emotion / Integration Governance",
                    source_regulation_ref=regulation_id,
                    parameter_modulation_ref=None,
                    reason_codes=("EMOTION_REFERENCE_INFLUENCE_ONLY",),
                    trace_ref=f"handoff-trace:{scenario_id}",
                )
            )
        if request.intent_refs:
            output.append(
                InfluenceCandidateV1(
                    influence_id=f"influence:{scenario_id}:intent-pressure",
                    influence_kind="intent_pressure_influence_candidate",
                    target_owner="Intent Governance",
                    source_regulation_ref=regulation_id,
                    parameter_modulation_ref=None,
                    reason_codes=("INTENT_REFERENCE_INFLUENCE_ONLY",),
                    trace_ref=f"handoff-trace:{scenario_id}",
                )
            )
        return tuple(output)

    def _status(
        self,
        request: DynamicCognitiveRegulationInputV1,
        modulations: Sequence[ParameterModulationCandidateV1],
        conflicts: Sequence[ParameterConflictCandidateV1],
    ) -> Tuple[str, str, Tuple[str, ...]]:
        if request.revocation_requested or request.source_revoked:
            return "REVOKED", "REVOKED", ("REVOCATION_REQUESTED",)
        if request.revision_requested:
            return "REVISED", "REVISED", ("REVISION_REQUESTED",)
        if not request.cognitive_state_vector_candidate.provenance_refs:
            return "REVOKED", "REJECTED", ("STATE_VECTOR_PROVENANCE_MISSING",)
        if request.cognitive_state_vector_candidate.stale:
            return "DEFERRED", "DEFERRED", ("STATE_VECTOR_STALE",)
        if conflicts:
            return "UNDER_REVIEW", "CONFLICTS_PRESERVED", ("CONFLICTS_PRESERVED",)
        statuses = {item.evaluation_status for item in modulations}
        if "REJECTED" in statuses:
            return "REVOKED", "REJECTED", ("PARAMETER_REQUEST_REJECTED",)
        if "DEFERRED" in statuses:
            return "DEFERRED", "DEFERRED", ("APPROVAL_OR_REVIEW_REQUIRED",)
        if "EXPIRED_NOT_REUSED" in statuses:
            return "REVOKED", "EXPIRED_NOT_REUSED", ("TEMPORARY_PARAMETER_EXPIRED",)
        if "CANDIDATE_ONLY_NO_AUTO_APPLY" in statuses:
            return (
                "UNDER_REVIEW",
                "CANDIDATE_ONLY_NO_AUTO_APPLY",
                ("LEARNING_CANDIDATE_REQUIRES_GOVERNANCE",),
            )
        if statuses == {"NO_CHANGE"}:
            return "UNDER_REVIEW", "NO_CHANGE", ("STABLE_STATE_NO_CHANGE",)
        if "CONSTRAINED" in statuses:
            return "UNDER_REVIEW", "CONSTRAINED", ("BOUNDS_CONSTRAINT_APPLIED",)
        return "UNDER_REVIEW", "BOUNDED_ELIGIBLE", ("BOUNDED_CANDIDATE_AVAILABLE",)

    def evaluate(
        self, request: DynamicCognitiveRegulationInputV1
    ) -> DynamicCognitiveRegulationOutputV1:
        regulation_id = f"regulation:{request.scenario_id}:{MODULE_VERSION}"
        bounds_by_parameter = {item.parameter_id: item for item in request.parameter_bounds}
        modulations: List[ParameterModulationCandidateV1] = []
        for index, parameter in enumerate(request.parameter_candidates, start=1):
            bounds = bounds_by_parameter.get(parameter.parameter_id)
            evaluation = self._evaluate_bounds(parameter, bounds)
            modulations.append(
                self._modulation(
                    request.scenario_id, index, parameter, bounds, evaluation
                )
            )

        conflicts = self._conflicts(request.scenario_id, modulations)
        state, status, status_reasons = self._status(
            request, modulations, conflicts
        )
        influences = self._influences(
            request.scenario_id, regulation_id, modulations, request
        )

        all_source_refs = (
            request.context_refs
            + request.pcn_refs
            + request.intent_refs
            + request.hypothesis_refs
            + request.emotion_refs
            + request.resource_refs
            + request.learning_update_refs
        )
        source_ids = tuple(ref.ref_id for ref in all_source_refs)
        source_owner_refs = tuple(
            f"{ref.owner}:{ref.ref_id}" for ref in all_source_refs
        )
        policy_ids = tuple(ref.policy_id for ref in request.policy_refs)
        bound_ids = tuple(item.bounds_id for item in request.parameter_bounds)
        parameter_ids = tuple(item.parameter_id for item in request.parameter_candidates)
        provenance_refs = (
            tuple(request.cognitive_state_vector_candidate.provenance_refs)
            + tuple(ref.provenance_ref for ref in all_source_refs)
        )

        candidate = DynamicRegulationCandidateV1(
            regulation_id=regulation_id,
            owner=CANONICAL_OWNER,
            state_vector_ref=request.cognitive_state_vector_candidate.state_vector_id,
            context_refs=tuple(ref.ref_id for ref in request.context_refs),
            pcn_refs=tuple(ref.ref_id for ref in request.pcn_refs),
            intent_refs=tuple(ref.ref_id for ref in request.intent_refs),
            hypothesis_refs=tuple(ref.ref_id for ref in request.hypothesis_refs),
            emotion_refs=tuple(ref.ref_id for ref in request.emotion_refs),
            resource_refs=tuple(ref.ref_id for ref in request.resource_refs),
            learning_refs=tuple(ref.ref_id for ref in request.learning_update_refs),
            policy_refs=policy_ids,
            parameter_bound_refs=bound_ids,
            modulation_candidates=tuple(modulations),
            conflict_candidates=conflicts,
            influence_candidates=influences,
            state_candidate=state,
            evaluation_status=status,
            reason_codes=status_reasons
            + tuple(reason for item in modulations for reason in item.reason_codes),
            unknowns=(
                ("state_vector_provenance_missing",)
                if not request.cognitive_state_vector_candidate.provenance_refs
                else ()
            ),
            trace_ref=f"trace:{request.scenario_id}",
            provenance_refs=provenance_refs,
            revision_parent_ref=(
                request.prior_regulation_candidate_ref
                if request.revision_requested
                else None
            ),
            revocation_parent_ref=(
                request.prior_regulation_candidate_ref
                if request.revocation_requested or request.source_revoked
                else None
            ),
        )

        handoff = DynamicRegulationHandoffCandidateV1(
            handoff_id=f"handoff:{request.scenario_id}",
            producer_owner=CANONICAL_OWNER,
            regulation_candidate_ref=regulation_id,
            influence_candidate_refs=tuple(item.influence_id for item in influences),
            consumer_owner_refs=tuple(
                sorted({item.target_owner for item in influences})
            ),
            trace_ref=f"handoff-trace:{request.scenario_id}",
            provenance_refs=provenance_refs,
        )

        reverse_chain = (
            (request.cognitive_state_vector_candidate.state_vector_id,)
            + source_ids
            + parameter_ids
            + bound_ids
            + policy_ids
        )
        trace = DynamicRegulationTraceV1(
            root_trace_id=f"trace:{request.scenario_id}",
            scenario_id=request.scenario_id,
            cognitive_state_vector_ref=request.cognitive_state_vector_candidate.state_vector_id,
            state_vector_trace_ref=request.cognitive_state_vector_candidate.trace_ref,
            source_influence_refs=source_ids,
            parameter_refs=parameter_ids,
            parameter_bounds_refs=bound_ids,
            policy_refs=policy_ids,
            regulation_function_id=REGULATION_FUNCTION_ID,
            regulation_function_version=MODULE_VERSION,
            prior_regulation_candidate_ref=request.prior_regulation_candidate_ref,
            resulting_regulation_candidate_ref=regulation_id,
            influence_handoff_trace_ref=handoff.trace_ref,
            revision_lineage_refs=(
                (f"revision:{request.scenario_id}",)
                if request.revision_requested
                else ()
            ),
            revocation_lineage_refs=(
                (f"revocation:{request.scenario_id}",)
                if request.revocation_requested or request.source_revoked
                else ()
            ),
            source_version_lineage_refs=tuple(
                item.parameter_version for item in request.parameter_candidates
            ),
            reverse_lookup={regulation_id: reverse_chain},
        )
        provenance = DynamicRegulationProvenanceV1(
            source_owner_refs=source_owner_refs,
            source_ref_chain=(
                request.cognitive_state_vector_candidate.state_vector_id,
            )
            + source_ids,
            parameter_version_refs=tuple(
                item.parameter_version for item in request.parameter_candidates
            ),
            policy_ref_chain=policy_ids,
            resulting_candidate_ref=regulation_id,
        )
        state_candidate = SelfRegulationStateCandidateV1(
            regulation_ref=regulation_id,
            current_state=state,
            transition_trace=(
                "OBSERVED",
                "ASSESSED",
                "CANDIDATE",
                state,
            ),
            reason_codes=status_reasons,
        )
        revision_candidate = None
        if request.revision_requested and request.prior_regulation_candidate_ref:
            revision_candidate = RegulationRevisionCandidateV1(
                revision_id=f"revision:{request.scenario_id}",
                prior_regulation_ref=request.prior_regulation_candidate_ref,
                revised_regulation_ref=regulation_id,
                reason_codes=("NEW_EVIDENCE_OR_CONFLICT",),
                source_version_lineage=trace.source_version_lineage_refs,
                trace_ref=trace.root_trace_id,
            )
        revocation_candidate = None
        if (
            request.revocation_requested or request.source_revoked
        ) and request.prior_regulation_candidate_ref:
            revocation_candidate = RegulationRevocationCandidateV1(
                revocation_id=f"revocation:{request.scenario_id}",
                revoked_regulation_ref=request.prior_regulation_candidate_ref,
                reason_codes=("SOURCE_REVOKED_OR_BOUNDARY_VIOLATION",),
                source_version_lineage=trace.source_version_lineage_refs,
                trace_ref=trace.root_trace_id,
            )

        return DynamicCognitiveRegulationOutputV1(
            scenario_id=request.scenario_id,
            regulation_candidate=candidate,
            state_candidate=state_candidate,
            handoff_candidate=handoff,
            trace=trace,
            provenance=provenance,
            negative_guard_status=NegativeGuardStatusV1(),
            genome_candidate=request.genome_candidate,
            revision_candidate=revision_candidate,
            revocation_candidate=revocation_candidate,
            issues=candidate.unknowns,
        )
