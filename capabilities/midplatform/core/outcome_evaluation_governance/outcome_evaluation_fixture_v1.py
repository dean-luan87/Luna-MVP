"""Synthetic O01-O36 requests and frozen expected behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .outcome_evaluation_core_types_v1 import (
    ActualResultInputV1,
    ExpectedOutcomeInputV1,
    OutcomeEvaluationRequestV1,
)


@dataclass(frozen=True)
class OutcomeEvaluationFixtureCaseV1:
    scenario_id: str
    title: str
    request: OutcomeEvaluationRequestV1
    expected_comparability: str
    expected_deviation: str
    expected_recommendation: str
    expected_attribution_kinds: Tuple[str, ...] = ()
    expected_observation_need: bool = False
    expected_learning_signal: bool = False
    expected_guard_kinds: Tuple[str, ...] = ()
    expected_revision: bool = False


def _request(
    scenario_id: str,
    *,
    title: str,
    intended_status: str = "MATCH",
    evidence_sufficient: bool = True,
    contradictory: bool = False,
    needs_confirmation: bool = False,
    temporal_status: str = "WITHIN_TEMPORAL_WINDOW",
    schema_comparable: bool = True,
    target_comparable: bool = True,
    spatial_comparable: bool = True,
    user_correction_ref: str | None = None,
    correction_precedence: bool = False,
    superseded_expectation: bool = False,
    revoked_actual: bool = False,
    attribution_kinds: Tuple[str, ...] = (),
    recommendation: str = "NO_ACTION",
    observation_information_gap: str | None = None,
    expected_evidence_kinds: Tuple[str, ...] = (),
    duplicate_kinds: Tuple[str, ...] = (),
    completed_evaluation: bool = False,
    reconsideration_depth: int = 0,
    learning_enabled: bool = True,
    task_completion_candidate: str = "",
    actual_ref: str | None = None,
    actual_status: str = "SUCCEEDED_CANDIDATE",
    actual_uncertainty: Tuple[str, ...] = (),
    contradiction_refs: Tuple[str, ...] = (),
    counterexample_refs: Tuple[str, ...] = (),
) -> OutcomeEvaluationRequestV1:
    expected = ExpectedOutcomeInputV1(
        expectation_ref=f"expectation:{scenario_id}",
        expectation_kind="DECLARED_EXPECTED_OUTCOME",
        source_owner="Decision Governance",
        source_ref=f"decision:{scenario_id}",
        target_ref="target:synthetic-route",
        semantic_scope="synthetic-route-effect",
        temporal_scope="synthetic-window",
        spatial_scope="synthetic-scope",
        expected_attributes=("route_effect", "completion"),
        completion_criteria=("candidate_condition",),
        expected_value="SUCCESS" if intended_status == "MATCH" else "EXPECTED_VALUE",
        trace_ref=f"trace:{scenario_id}:expected",
        provenance_refs=(f"prov:{scenario_id}:expected",),
    )
    actual = ActualResultInputV1(
        actual_result_ref=actual_ref if actual_ref is not None else f"actual:{scenario_id}",
        source_owner="Runtime Executor" if scenario_id not in {"O04", "O05", "O07", "O10", "O17", "O31", "O32", "O33", "O34"} else "Observation Gateway",
        source_ref=f"source:{scenario_id}",
        result_kind="EXECUTION_RESULT" if scenario_id not in {"O04", "O05", "O07", "O10", "O17", "O31", "O32", "O33", "O34"} else "OBSERVATION_RESULT",
        target_ref="target:synthetic-route",
        observed_at="synthetic-now",
        valid_from="synthetic-now",
        valid_until="synthetic-window-end",
        status_candidate=actual_status,
        observed_attributes=("route_effect", "completion"),
        actual_value="SUCCESS" if intended_status == "MATCH" else "DIFFERENT",
        uncertainty_refs=actual_uncertainty,
        contradiction_refs=contradiction_refs,
        correction_refs=(user_correction_ref,) if user_correction_ref else (),
        trace_ref=f"trace:{scenario_id}:actual",
        provenance_refs=(f"prov:{scenario_id}:actual",),
        source_valid=not revoked_actual,
    )
    return OutcomeEvaluationRequestV1(
        scenario_id=scenario_id,
        root_cycle_trace_id=f"trace:{scenario_id}:root-cycle",
        expected=expected,
        actual=actual,
        intended_status=intended_status,
        evidence_sufficient=evidence_sufficient,
        contradictory=contradictory,
        needs_confirmation=needs_confirmation,
        temporal_status=temporal_status,
        schema_comparable=schema_comparable,
        target_comparable=target_comparable,
        spatial_comparable=spatial_comparable,
        user_correction_ref=user_correction_ref,
        correction_precedence=correction_precedence,
        superseded_expectation=superseded_expectation,
        revoked_actual=revoked_actual,
        attribution_kinds=attribution_kinds,
        recommendation=recommendation,
        observation_information_gap=observation_information_gap,
        expected_evidence_kinds=expected_evidence_kinds,
        duplicate_kinds=duplicate_kinds,
        completed_evaluation=completed_evaluation,
        reconsideration_depth=reconsideration_depth,
        learning_signal_allowed=learning_enabled,
        task_completion_candidate=task_completion_candidate,
        context_refs=(f"context:{scenario_id}",),
        intent_refs=(f"intent:{scenario_id}",),
        hypothesis_refs=(f"hypothesis:{scenario_id}",),
        current_world_refs=(f"current-world:{scenario_id}",),
        feedback_refs=(f"feedback:{scenario_id}",),
        counterexample_refs=counterexample_refs,
        synthetic_only=True,
        candidate_only=True,
    )


def build_fixture_cases() -> Tuple[OutcomeEvaluationFixtureCaseV1, ...]:
    cases = (
        OutcomeEvaluationFixtureCaseV1("O01", "exact expected/actual match", _request("O01", title="match"), "COMPARABLE", "MATCH", "NO_ACTION", expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O02", "partial completion", _request("O02", title="partial", intended_status="PARTIAL_MATCH"), "COMPARABLE", "PARTIAL_MATCH", "NO_ACTION", expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O03", "execution failure", _request("O03", title="failure", intended_status="MISMATCH", actual_status="FAILED_CANDIDATE", attribution_kinds=("EXECUTION_ERROR_CANDIDATE",), recommendation="RETRY_EXECUTION"), "COMPARABLE", "MISMATCH", "RETRY_EXECUTION", ("EXECUTION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O04", "expected Field change not observed", _request("O04", title="field change", intended_status="MISMATCH", attribution_kinds=("WORLD_MODEL_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("WORLD_MODEL_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O05", "stale Field result", _request("O05", title="stale", temporal_status="STALE_RESULT", attribution_kinds=("STALE_INFORMATION_CANDIDATE",)), "STALE_ACTUAL", "UNKNOWN", "REOBSERVE", ("STALE_INFORMATION_CANDIDATE",), True),
        OutcomeEvaluationFixtureCaseV1("O06", "observation evidence insufficient", _request("O06", title="insufficient", evidence_sufficient=False, observation_information_gap="missing outcome evidence", expected_evidence_kinds=("FIELD_CHANGE",), recommendation="REOBSERVE"), "INSUFFICIENT_EVIDENCE", "UNKNOWN", "REOBSERVE", ("INSUFFICIENT_EVIDENCE",), True),
        OutcomeEvaluationFixtureCaseV1("O07", "contradictory observations", _request("O07", title="contradiction", contradictory=True, contradiction_refs=("contradiction:O07",), attribution_kinds=("UNRESOLVED_ATTRIBUTION",), recommendation="REQUEST_USER_CONFIRMATION"), "CONTESTED", "CONTESTED", "REQUEST_USER_CONFIRMATION", ("UNRESOLVED_ATTRIBUTION",), True, True),
        OutcomeEvaluationFixtureCaseV1("O08", "user confirms success", _request("O08", title="confirm", user_correction_ref="user-confirm:O08", correction_precedence=True), "COMPARABLE", "MATCH", "NO_ACTION", ("USER_CORRECTION_CANDIDATE",), expected_learning_signal=True, expected_revision=True),
        OutcomeEvaluationFixtureCaseV1("O09", "user corrects false success", _request("O09", title="correct", intended_status="MISMATCH", user_correction_ref="user-correction:O09", correction_precedence=True, attribution_kinds=("USER_CORRECTION_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("USER_CORRECTION_CANDIDATE",), expected_learning_signal=True, expected_revision=True),
        OutcomeEvaluationFixtureCaseV1("O10", "unexpected world change", _request("O10", title="world change", intended_status="MISMATCH", attribution_kinds=("EXTERNAL_WORLD_CHANGE_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("EXTERNAL_WORLD_CHANGE_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O11", "correct Decision but failed execution", _request("O11", title="decision right", intended_status="MISMATCH", actual_status="FAILED_CANDIDATE", attribution_kinds=("EXECUTION_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("EXECUTION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O12", "incorrect expectation but correct execution", _request("O12", title="expectation", intended_status="MISMATCH", attribution_kinds=("PREDICTION_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("PREDICTION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O13", "task completion criterion satisfied despite different path", _request("O13", title="criterion", intended_status="MATCH", task_completion_candidate="SATISFIED"), "COMPARABLE", "MATCH", "NO_ACTION", expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O14", "delayed result within allowed window", _request("O14", title="delayed", temporal_status="DELAYED_WITHIN_WINDOW"), "COMPARABLE", "MATCH", "NO_ACTION", expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O15", "result after expiration", _request("O15", title="expired", temporal_status="EXPIRED_EXPECTATION", superseded_expectation=True, attribution_kinds=("TEMPORAL_VALIDITY_ERROR_CANDIDATE",)), "STALE_EXPECTATION", "UNKNOWN", "REOBSERVE", ("TEMPORAL_VALIDITY_ERROR_CANDIDATE",), True),
        OutcomeEvaluationFixtureCaseV1("O16", "incomparable expected/actual schemas", _request("O16", title="schema", schema_comparable=False), "NOT_COMPARABLE", "UNKNOWN", "NO_ACTION"),
        OutcomeEvaluationFixtureCaseV1("O17", "missing actual evidence", _request("O17", title="missing", actual_ref="", evidence_sufficient=False), "INSUFFICIENT_EVIDENCE", "UNKNOWN", "REOBSERVE", ("INSUFFICIENT_EVIDENCE",), True),
        OutcomeEvaluationFixtureCaseV1("O18", "competing attribution candidates", _request("O18", title="competing", intended_status="MISMATCH", attribution_kinds=("STALE_INFORMATION_CANDIDATE", "EXECUTION_ERROR_CANDIDATE"), counterexample_refs=("counterexample:O18",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("STALE_INFORMATION_CANDIDATE", "EXECUTION_ERROR_CANDIDATE"), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O19", "re-observation required", _request("O19", title="reobserve", evidence_sufficient=False, recommendation="REOBSERVE", observation_information_gap="actual effect not covered", expected_evidence_kinds=("RESULT_OBSERVATION",)), "INSUFFICIENT_EVIDENCE", "UNKNOWN", "REOBSERVE", ("INSUFFICIENT_EVIDENCE",), True),
        OutcomeEvaluationFixtureCaseV1("O20", "reconsider Decision", _request("O20", title="decision", intended_status="MISMATCH", recommendation="RECONSIDER_DECISION", attribution_kinds=("DECISION_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "RECONSIDER_DECISION", ("DECISION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O21", "replan Task", _request("O21", title="task", intended_status="MISMATCH", recommendation="REPLAN_TASK", attribution_kinds=("TASK_PLANNING_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "REPLAN_TASK", ("TASK_PLANNING_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O22", "retry Execution candidate", _request("O22", title="retry", intended_status="MISMATCH", recommendation="RETRY_EXECUTION", attribution_kinds=("EXECUTION_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "RETRY_EXECUTION", ("EXECUTION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O23", "Learning Signal candidate", _request("O23", title="learning", intended_status="MISMATCH", attribution_kinds=("CAPABILITY_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("CAPABILITY_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O24", "Learning Signal rejected/deferred boundary", _request("O24", title="learning defer", intended_status="MISMATCH", attribution_kinds=("UNRESOLVED_ATTRIBUTION",), learning_enabled=False), "COMPARABLE", "MISMATCH", "NO_ACTION", ("UNRESOLVED_ATTRIBUTION",), expected_learning_signal=False),
        OutcomeEvaluationFixtureCaseV1("O25", "duplicate result", _request("O25", title="duplicate result", duplicate_kinds=("result",)), "COMPARABLE", "MATCH", "NO_ACTION", expected_guard_kinds=("duplicate_result",)),
        OutcomeEvaluationFixtureCaseV1("O26", "duplicate comparison", _request("O26", title="duplicate comparison", duplicate_kinds=("comparison",)), "COMPARABLE", "MATCH", "NO_ACTION", expected_guard_kinds=("duplicate_comparison",)),
        OutcomeEvaluationFixtureCaseV1("O27", "correction replay", _request("O27", title="correction replay", user_correction_ref="user-correction:O27", correction_precedence=True, duplicate_kinds=("correction",)), "COMPARABLE", "MATCH", "NO_ACTION", ("USER_CORRECTION_CANDIDATE",), expected_guard_kinds=("correction_replay",), expected_revision=True),
        OutcomeEvaluationFixtureCaseV1("O28", "superseded expectation", _request("O28", title="superseded", superseded_expectation=True, duplicate_kinds=("supersession",)), "STALE_EXPECTATION", "UNKNOWN", "REOBSERVE", ("INSUFFICIENT_EVIDENCE",), True, expected_guard_kinds=("supersession_replay",)),
        OutcomeEvaluationFixtureCaseV1("O29", "revoked result", _request("O29", title="revoked", revoked_actual=True, duplicate_kinds=("revocation",)), "STALE_ACTUAL", "UNKNOWN", "REOBSERVE", ("INSUFFICIENT_EVIDENCE",), True, expected_guard_kinds=("revocation_replay",)),
        OutcomeEvaluationFixtureCaseV1("O30", "safety outcome mismatch", _request("O30", title="safety", intended_status="MISMATCH", attribution_kinds=("CAPABILITY_ERROR_CANDIDATE",), recommendation="REQUEST_USER_CONFIRMATION", needs_confirmation=True), "NEEDS_CONFIRMATION", "UNKNOWN", "REQUEST_USER_CONFIRMATION", ("CAPABILITY_ERROR_CANDIDATE",), expected_observation_need=False),
        OutcomeEvaluationFixtureCaseV1("O31", "provider confidence high but outcome wrong", _request("O31", title="confidence high", intended_status="MISMATCH", attribution_kinds=("OBSERVATION_ERROR_CANDIDATE",), actual_uncertainty=("provider-confidence-high",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("OBSERVATION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O32", "provider confidence low but outcome confirmed", _request("O32", title="confidence low", actual_uncertainty=("provider-confidence-low",)), "COMPARABLE", "MATCH", "NO_ACTION", expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O33", "Observation Gateway admission does not prove success", _request("O33", title="gateway admission", intended_status="MISMATCH", attribution_kinds=("OBSERVATION_ERROR_CANDIDATE",)), "COMPARABLE", "MISMATCH", "NO_ACTION", ("OBSERVATION_ERROR_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O34", "no direct YOLO/OCR/SLAM invocation", _request("O34", title="provider boundary", evidence_sufficient=False, recommendation="REOBSERVE", expected_evidence_kinds=("OBSERVATION_EVIDENCE",)), "INSUFFICIENT_EVIDENCE", "UNKNOWN", "REOBSERVE", ("INSUFFICIENT_EVIDENCE",), True),
        OutcomeEvaluationFixtureCaseV1("O35", "A Route next-cycle feedback", _request("O35", title="next cycle", intended_status="MISMATCH", recommendation="START_NEXT_CYCLE", attribution_kinds=("EXTERNAL_WORLD_CHANGE_CANDIDATE",)), "COMPARABLE", "MISMATCH", "START_NEXT_CYCLE", ("EXTERNAL_WORLD_CHANGE_CANDIDATE",), expected_learning_signal=True),
        OutcomeEvaluationFixtureCaseV1("O36", "no runtime/mutation/deferred workstream activation", _request("O36", title="guards", learning_enabled=False), "COMPARABLE", "MATCH", "NO_ACTION"),
    )
    return cases
