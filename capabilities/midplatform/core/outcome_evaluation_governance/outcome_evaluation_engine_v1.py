"""Deterministic, synthetic-only Outcome Evaluation candidate engine."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

from .outcome_evaluation_core_types_v1 import (
    ActualResultInputV1,
    AttributionCandidateV1,
    ComparabilityGateCandidateV1,
    DeviationCandidateV1,
    ExpectedOutcomeInputV1,
    IdempotencyGuardCandidateV1,
    LearningSignalHandoffCandidateV1,
    ObservationNeedHandoffCandidateV1,
    OutcomeEvaluationCandidateV1,
    OutcomeEvaluationOutputV1,
    OutcomeEvaluationRequestV1,
    ReconsiderationHandoffCandidateV1,
    TraceProvenanceV1,
)
from .outcome_evaluation_registry_v1 import (
    ATTRIBUTION_KINDS,
    COMPARABILITY_STATES,
    CONTRACT_VERSION,
    DEVIATION_STATUSES,
    MODULE_VERSION,
    NEGATIVE_GUARDS,
    RECOMMENDATIONS,
    SCHEMA_VERSION,
)


class OutcomeEvaluationEngineV1:
    """Build immutable candidates from an explicit request snapshot.

    The engine has no registry, cache, provider, model, persistence, or
    runtime side effect. Duplicate and replay information is part of the
    request so behavior remains inspectable and does not depend on hidden
    mutable state.
    """

    def _refs(self, *groups: Iterable[str]) -> Tuple[str, ...]:
        values: list[str] = []
        for group in groups:
            for value in group:
                if value and value not in values:
                    values.append(value)
        return tuple(values)

    def _comparability_state(self, request: OutcomeEvaluationRequestV1) -> str:
        expected = request.expected
        actual = request.actual
        if request.revoked_actual or not actual.source_valid:
            return "STALE_ACTUAL"
        if request.superseded_expectation or expected.revocation_ref:
            return "STALE_EXPECTATION"
        if request.temporal_status in {"STALE_RESULT", "EXPIRED_EXPECTATION", "OBSERVATION_AFTER_EXPECTED_WINDOW"}:
            return "STALE_ACTUAL" if request.temporal_status == "STALE_RESULT" else "STALE_EXPECTATION"
        if not request.schema_comparable or not request.target_comparable:
            return "NOT_COMPARABLE"
        if not request.spatial_comparable:
            return "PARTIALLY_COMPARABLE"
        if not actual.actual_result_ref or not expected.expectation_ref:
            return "INSUFFICIENT_EVIDENCE"
        if not request.evidence_sufficient:
            return "INSUFFICIENT_EVIDENCE"
        if request.contradictory or actual.contradiction_refs:
            return "CONTESTED"
        if request.needs_confirmation:
            return "NEEDS_CONFIRMATION"
        if request.temporal_status in {"RESULT_TOO_EARLY", "RESULT_TOO_LATE"}:
            return "PARTIALLY_COMPARABLE"
        return "COMPARABLE"

    def _comparability(
        self, request: OutcomeEvaluationRequestV1
    ) -> ComparabilityGateCandidateV1:
        state = self._comparability_state(request)
        passed = {
            "same_target": request.target_comparable,
            "compatible_schema": request.schema_comparable,
            "compatible_spatial_scope": request.spatial_comparable,
            "evidence_present": bool(request.actual.actual_result_ref),
            "source_valid": request.actual.source_valid,
            "temporal_reference_present": bool(request.temporal_status),
        }
        checks = tuple(name for name, value in passed.items() if value)
        blocked = tuple(name for name, value in passed.items() if not value)
        if state == "INSUFFICIENT_EVIDENCE":
            blocked = self._refs(blocked, ("evidence_sufficiency",))
        if state == "CONTESTED":
            blocked = self._refs(blocked, ("contradictory_evidence",))
        if state == "STALE_ACTUAL":
            blocked = self._refs(blocked, ("stale_actual",))
        if state == "STALE_EXPECTATION":
            blocked = self._refs(blocked, ("stale_expectation",))
        if state == "NEEDS_CONFIRMATION":
            blocked = self._refs(blocked, ("user_confirmation_required",))
        basis = (
            f"expectation:{request.expected.expectation_ref}",
            f"actual:{request.actual.actual_result_ref}",
            f"temporal:{request.temporal_status}",
        )
        return ComparabilityGateCandidateV1(
            comparability_id=f"comparability:{request.scenario_id}",
            state=state,
            expectation_ref=request.expected.expectation_ref,
            actual_result_ref=request.actual.actual_result_ref,
            checks_passed=checks,
            blocked_reason_refs=blocked,
            comparison_basis_refs=basis,
            uncertainty_refs=self._refs(request.expected.uncertainty_refs, request.actual.uncertainty_refs),
            contradiction_refs=request.actual.contradiction_refs,
            trace_ref=f"trace:{request.scenario_id}:comparability",
            provenance_refs=(f"prov:{request.scenario_id}:comparability",),
        )

    def _deviation_status(
        self, request: OutcomeEvaluationRequestV1, comparability: ComparabilityGateCandidateV1
    ) -> str:
        if comparability.state == "CONTESTED":
            return "CONTESTED"
        if comparability.state in {"NOT_COMPARABLE", "INSUFFICIENT_EVIDENCE", "STALE_ACTUAL", "STALE_EXPECTATION", "NEEDS_CONFIRMATION"}:
            return "UNKNOWN"
        requested = request.intended_status
        return requested if requested in DEVIATION_STATUSES else "UNKNOWN"

    def _deviation(
        self, request: OutcomeEvaluationRequestV1, comparability: ComparabilityGateCandidateV1
    ) -> DeviationCandidateV1:
        status = self._deviation_status(request, comparability)
        dimensions: list[str] = []
        if status == "MATCH":
            dimensions.append("all_comparable_dimensions_match")
        if status == "PARTIAL_MATCH":
            dimensions.extend(("partial_completion", "missing_expected_effect"))
        if status == "MISMATCH":
            dimensions.append("semantic_or_value_mismatch")
        if comparability.state in {"STALE_ACTUAL", "STALE_EXPECTATION"}:
            dimensions.append("temporal_mismatch")
        if request.temporal_status in {"RESULT_TOO_EARLY", "RESULT_TOO_LATE", "OBSERVATION_AFTER_EXPECTED_WINDOW"}:
            dimensions.append("temporal_mismatch")
        if request.actual.actual_value != request.expected.expected_value and request.expected.expected_value is not None:
            dimensions.append("value_mismatch")
        if request.actual.status_candidate in {"FAILED_CANDIDATE", "REJECTED_CANDIDATE", "TIMEOUT_CANDIDATE"}:
            dimensions.append("execution_or_completion_mismatch")
        return DeviationCandidateV1(
            deviation_id=f"deviation:{request.scenario_id}",
            expectation_ref=request.expected.expectation_ref,
            actual_result_ref=request.actual.actual_result_ref,
            comparability_ref=comparability.comparability_id,
            status=status,
            dimension_statuses=tuple(dict.fromkeys(dimensions)),
            comparison_basis_refs=comparability.comparison_basis_refs,
            magnitude_candidate="candidate-scale" if status in {"MISMATCH", "PARTIAL_MATCH"} else None,
            uncertainty_refs=self._refs(comparability.uncertainty_refs, request.actual.uncertainty_refs),
            contradiction_refs=self._refs(comparability.contradiction_refs, ("contradiction:pending",) if request.contradictory else ()),
            counterevidence_refs=request.counterexample_refs,
            temporal_refs=(f"temporal:{request.temporal_status}",),
            trace_ref=f"trace:{request.scenario_id}:deviation",
            provenance_refs=(f"prov:{request.scenario_id}:deviation",),
            revision_parent_ref=f"deviation:{request.scenario_id}:prior" if request.user_correction_ref else None,
            supersedes_ref=f"deviation:{request.scenario_id}:superseded" if request.superseded_expectation else None,
            revocation_ref=f"deviation:{request.scenario_id}:revoked" if request.revoked_actual else None,
        )

    def _attributions(
        self, request: OutcomeEvaluationRequestV1, deviation: DeviationCandidateV1
    ) -> Tuple[AttributionCandidateV1, ...]:
        kinds = list(request.attribution_kinds)
        if request.user_correction_ref and "USER_CORRECTION_CANDIDATE" not in kinds:
            kinds.append("USER_CORRECTION_CANDIDATE")
        if (
            deviation.status == "UNKNOWN"
            and not kinds
            and request.schema_comparable
            and request.target_comparable
        ):
            kinds.append("INSUFFICIENT_EVIDENCE")
        if deviation.status in {"MISMATCH", "CONTESTED"} and not kinds:
            kinds.append("UNRESOLVED_ATTRIBUTION")
        valid = [kind for kind in kinds if kind in ATTRIBUTION_KINDS]
        refs = tuple(f"attribution:{request.scenario_id}:{idx}" for idx, _ in enumerate(valid, start=1))
        items: list[AttributionCandidateV1] = []
        for idx, kind in enumerate(valid):
            competing = tuple(ref for ref in refs if ref != refs[idx])
            items.append(
                AttributionCandidateV1(
                    attribution_id=refs[idx],
                    attribution_kind=kind,
                    support_refs=(deviation.deviation_id, request.actual.actual_result_ref),
                    counterevidence_refs=request.counterexample_refs,
                    related_expectation_refs=(request.expected.expectation_ref,),
                    related_actual_result_refs=(request.actual.actual_result_ref,),
                    confidence_candidate="LOW" if kind in {"UNRESOLVED_ATTRIBUTION", "INSUFFICIENT_EVIDENCE"} else "CANDIDATE",
                    uncertainty_refs=self._refs(request.expected.uncertainty_refs, request.actual.uncertainty_refs),
                    competing_attribution_refs=competing,
                    partial_cause_refs=tuple(f"partial-cause:{request.scenario_id}:{n}" for n in range(1, len(valid))) if len(valid) > 1 else (),
                    revision_parent_ref=f"attribution:{request.scenario_id}:prior" if request.user_correction_ref else None,
                    supersedes_ref=f"attribution:{request.scenario_id}:superseded" if request.superseded_expectation else None,
                    revocation_ref=f"attribution:{request.scenario_id}:revoked" if request.revoked_actual else None,
                    trace_ref=f"trace:{request.scenario_id}:attribution:{idx + 1}",
                    provenance_refs=(f"prov:{request.scenario_id}:attribution:{idx + 1}",),
                )
            )
        return tuple(items)

    def _recommendation(self, request: OutcomeEvaluationRequestV1, comparability: ComparabilityGateCandidateV1) -> str:
        if request.completed_evaluation:
            return "DEFER"
        if request.reconsideration_depth >= request.max_reconsideration_depth and request.recommendation != "NO_ACTION":
            return "DEFER"
        if request.recommendation != "NO_ACTION" and request.recommendation in RECOMMENDATIONS:
            return request.recommendation
        if comparability.state in {"INSUFFICIENT_EVIDENCE", "STALE_ACTUAL", "STALE_EXPECTATION", "CONTESTED"}:
            return "REOBSERVE"
        if comparability.state == "NEEDS_CONFIRMATION":
            return "REQUEST_USER_CONFIRMATION"
        return "NO_ACTION"

    def _reconsideration(
        self,
        request: OutcomeEvaluationRequestV1,
        comparability: ComparabilityGateCandidateV1,
        attributions: Tuple[AttributionCandidateV1, ...],
        evaluation_id: str,
    ) -> Optional[ReconsiderationHandoffCandidateV1]:
        recommendation = self._recommendation(request, comparability)
        if recommendation == "NO_ACTION":
            return None
        return ReconsiderationHandoffCandidateV1(
            reconsideration_id=f"reconsideration:{request.scenario_id}",
            evaluation_ref=evaluation_id,
            recommendation=recommendation,
            reason_refs=comparability.blocked_reason_refs or (f"deviation:{request.scenario_id}",),
            expected_refs=(request.expected.expectation_ref,),
            actual_refs=(request.actual.actual_result_ref,),
            attribution_refs=tuple(item.attribution_id for item in attributions),
            budget_state="DEPTH_EXHAUSTED" if recommendation == "DEFER" else "CANDIDATE_BUDGET",
            reconsideration_depth_candidate=request.reconsideration_depth,
            max_depth_ref=f"max-reconsideration-depth:{request.max_reconsideration_depth}",
            trace_ref=f"trace:{request.scenario_id}:reconsideration",
            provenance_refs=(f"prov:{request.scenario_id}:reconsideration",),
        )

    def _learning_signal(
        self,
        request: OutcomeEvaluationRequestV1,
        deviation: DeviationCandidateV1,
        attributions: Tuple[AttributionCandidateV1, ...],
        evaluation_id: str,
    ) -> Optional[LearningSignalHandoffCandidateV1]:
        if not request.learning_signal_allowed or deviation.status == "UNKNOWN" or request.duplicate_kinds:
            return None
        return LearningSignalHandoffCandidateV1(
            learning_signal_id=f"learning-signal:{request.scenario_id}",
            evaluation_ref=evaluation_id,
            deviation_refs=(deviation.deviation_id,),
            attribution_refs=tuple(item.attribution_id for item in attributions),
            outcome_refs=(request.actual.actual_result_ref,),
            feedback_refs=request.feedback_refs,
            context_refs=request.context_refs,
            intent_refs=request.intent_refs,
            hypothesis_refs=request.hypothesis_refs,
            current_world_refs=request.current_world_refs,
            contradiction_refs=deviation.contradiction_refs,
            counterexample_refs=request.counterexample_refs,
            temporal_refs=deviation.temporal_refs,
            status="CONTESTED" if deviation.status == "CONTESTED" else "PROPOSED",
            provenance_refs=(f"prov:{request.scenario_id}:learning-signal",),
            trace_ref=f"trace:{request.scenario_id}:learning-signal",
        )

    def _observation_need(
        self,
        request: OutcomeEvaluationRequestV1,
        comparability: ComparabilityGateCandidateV1,
        evaluation_id: str,
    ) -> Optional[ObservationNeedHandoffCandidateV1]:
        if comparability.state not in {"INSUFFICIENT_EVIDENCE", "CONTESTED", "STALE_ACTUAL", "STALE_EXPECTATION"}:
            return None
        return ObservationNeedHandoffCandidateV1(
            observation_need_id=f"observation-need:{request.scenario_id}",
            evaluation_ref=evaluation_id,
            information_gap=request.observation_information_gap or "outcome evidence remains insufficient or contested",
            expected_evidence_kinds=request.expected_evidence_kinds,
            target_scope=request.expected.target_ref,
            temporal_scope=request.expected.temporal_scope,
            budget_candidate="bounded-candidate-budget",
            stop_conditions=("evidence_sufficient", "budget_exhausted", "user_cancelled", "target_lost"),
            provenance_refs=(f"prov:{request.scenario_id}:observation-need",),
            trace_ref=f"trace:{request.scenario_id}:observation-need",
        )

    def _guards(self, request: OutcomeEvaluationRequestV1) -> Tuple[IdempotencyGuardCandidateV1, ...]:
        duplicate = set(request.duplicate_kinds)
        pairs = (
            ("duplicate_result", "result"),
            ("duplicate_comparison", "comparison"),
            ("duplicate_evaluation", "evaluation"),
            ("duplicate_attribution", "attribution"),
            ("duplicate_reconsideration", "reconsideration"),
            ("duplicate_learning_signal", "learning_signal"),
            ("correction_replay", "correction"),
            ("revocation_replay", "revocation"),
            ("supersession_replay", "supersession"),
            ("completed_evaluation_mutation", "completed_evaluation"),
        )
        return tuple(
            IdempotencyGuardCandidateV1(
                guard_id=f"guard:{request.scenario_id}:{kind}",
                guard_kind=kind,
                signature=f"{kind}:{request.scenario_id}:{request.expected.expectation_ref}:{request.actual.actual_result_ref}",
                triggered=key in duplicate or (key == "completed_evaluation" and request.completed_evaluation),
                action="REJECT_REPLAY_OR_CREATE_REVISION" if key in duplicate or (key == "completed_evaluation" and request.completed_evaluation) else "ALLOW_CANDIDATE",
            )
            for kind, key in pairs
        )

    def _evaluation(
        self,
        request: OutcomeEvaluationRequestV1,
        comparability: ComparabilityGateCandidateV1,
        deviation: DeviationCandidateV1,
        attributions: Tuple[AttributionCandidateV1, ...],
        reconsideration: Optional[ReconsiderationHandoffCandidateV1],
        learning_signal: Optional[LearningSignalHandoffCandidateV1],
        observation_need: Optional[ObservationNeedHandoffCandidateV1],
    ) -> OutcomeEvaluationCandidateV1:
        evaluation_id = f"evaluation:{request.scenario_id}"
        status = deviation.status if comparability.state in {"COMPARABLE", "PARTIALLY_COMPARABLE"} else comparability.state
        return OutcomeEvaluationCandidateV1(
            evaluation_id=evaluation_id,
            root_cycle_trace_id=request.root_cycle_trace_id,
            expected_outcome_refs=(request.expected.expectation_ref,),
            actual_result_refs=(request.actual.actual_result_ref,),
            comparability_ref=comparability.comparability_id,
            deviation_refs=(deviation.deviation_id,),
            intended_outcome_observed_candidate="YES" if deviation.status == "MATCH" else "NO" if deviation.status == "MISMATCH" else "UNKNOWN",
            task_completion_candidate=request.task_completion_candidate or ("PARTIAL" if deviation.status == "PARTIAL_MATCH" else "UNKNOWN" if deviation.status in {"UNKNOWN", "CONTESTED"} else "CANDIDATE"),
            action_effect_observed_candidate="YES" if deviation.status == "MATCH" else "PARTIAL" if deviation.status == "PARTIAL_MATCH" else "UNKNOWN",
            world_change_observed_candidate="YES" if deviation.status == "MATCH" else "UNKNOWN" if deviation.status in {"UNKNOWN", "CONTESTED"} else "NO",
            evidence_sufficiency_candidate="SUFFICIENT" if request.evidence_sufficient and comparability.state in {"COMPARABLE", "PARTIALLY_COMPARABLE"} else "INSUFFICIENT",
            uncertainty_refs=self._refs(request.expected.uncertainty_refs, request.actual.uncertainty_refs),
            contradiction_refs=self._refs(request.actual.contradiction_refs, deviation.contradiction_refs),
            attribution_candidate_refs=tuple(item.attribution_id for item in attributions),
            reconsideration_candidate_refs=(reconsideration.reconsideration_id,) if reconsideration else (),
            learning_signal_candidate_refs=(learning_signal.learning_signal_id,) if learning_signal else (),
            observation_need_candidate_refs=(observation_need.observation_need_id,) if observation_need else (),
            evaluation_status=status,
            correction_refs=(request.user_correction_ref,) if request.user_correction_ref else request.actual.correction_refs,
            revision_parent_ref=f"evaluation:{request.scenario_id}:prior" if request.user_correction_ref else None,
            supersedes_ref=f"evaluation:{request.scenario_id}:superseded" if request.superseded_expectation else None,
            revocation_ref=f"evaluation:{request.scenario_id}:revoked" if request.revoked_actual else None,
            trace_ref=f"trace:{request.scenario_id}:evaluation",
            provenance_refs=(f"prov:{request.scenario_id}:evaluation",),
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
        )

    def _trace(
        self,
        request: OutcomeEvaluationRequestV1,
        evaluation: OutcomeEvaluationCandidateV1,
        comparability: ComparabilityGateCandidateV1,
        attributions: Tuple[AttributionCandidateV1, ...],
        reconsideration: Optional[ReconsiderationHandoffCandidateV1],
        learning_signal: Optional[LearningSignalHandoffCandidateV1],
        observation_need: Optional[ObservationNeedHandoffCandidateV1],
    ) -> TraceProvenanceV1:
        reverse = (
            (evaluation.evaluation_id, (comparability.comparability_id, *evaluation.deviation_refs)),
            (comparability.comparability_id, (request.expected.expectation_ref, request.actual.actual_result_ref)),
            (request.actual.actual_result_ref, (*request.actual.provenance_refs, request.actual.source_ref)),
            (request.expected.expectation_ref, (*request.expected.provenance_refs, request.expected.source_ref)),
        )
        return TraceProvenanceV1(
            root_cycle_trace_id=request.root_cycle_trace_id,
            evaluation_trace_id=evaluation.trace_ref,
            comparison_trace_id=comparability.trace_ref,
            expected_trace_refs=(request.expected.trace_ref,),
            actual_trace_refs=(request.actual.trace_ref,),
            attribution_trace_refs=tuple(item.trace_ref for item in attributions),
            reconsideration_trace_refs=(reconsideration.trace_ref,) if reconsideration else (),
            learning_signal_trace_refs=(learning_signal.trace_ref,) if learning_signal else (),
            observation_need_trace_refs=(observation_need.trace_ref,) if observation_need else (),
            source_owner_refs=(request.expected.source_owner, request.actual.source_owner),
            provenance_refs=self._refs(request.expected.provenance_refs, request.actual.provenance_refs, evaluation.provenance_refs),
            correction_lineage=(request.user_correction_ref,) if request.user_correction_ref else (),
            contradiction_lineage=request.actual.contradiction_refs,
            reverse_lookup=reverse,
        )

    def run_case(self, request: OutcomeEvaluationRequestV1) -> OutcomeEvaluationOutputV1:
        comparability = self._comparability(request)
        deviation = self._deviation(request, comparability)
        attributions = self._attributions(request, deviation)
        evaluation_id = f"evaluation:{request.scenario_id}"
        reconsideration = self._reconsideration(request, comparability, attributions, evaluation_id)
        learning_signal = self._learning_signal(request, deviation, attributions, evaluation_id)
        observation_need = self._observation_need(request, comparability, evaluation_id)
        evaluation = self._evaluation(request, comparability, deviation, attributions, reconsideration, learning_signal, observation_need)
        guards = self._guards(request)
        trace = self._trace(request, evaluation, comparability, attributions, reconsideration, learning_signal, observation_need)
        return OutcomeEvaluationOutputV1(
            scenario_id=request.scenario_id,
            comparability=comparability,
            deviation=deviation,
            evaluation=evaluation,
            attributions=attributions,
            reconsideration=reconsideration,
            learning_signal=learning_signal,
            observation_need=observation_need,
            idempotency_guards=guards,
            trace=trace,
            guards=dict(NEGATIVE_GUARDS),
        )
