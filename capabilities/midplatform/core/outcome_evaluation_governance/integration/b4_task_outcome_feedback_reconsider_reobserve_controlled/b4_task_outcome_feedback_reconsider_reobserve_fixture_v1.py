"""Compact B4 fixtures; only the B3 input boundary is real-shaped."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .b4_task_outcome_feedback_reconsider_reobserve_types_v1 import (
    B3TaskDecisionReferenceV1,
)


@dataclass(frozen=True)
class B4FixtureCaseV1:
    case_id: str
    title: str
    real: bool = True
    runtime_status: str = "SUCCEEDED_CANDIDATE"
    expected_value: str = "SUCCESS"
    actual_value: str = "SUCCESS"
    intended_status: str = "MATCH"
    evidence_sufficient: bool = True
    contradictory: bool = False
    recommendation: str = "NO_ACTION"
    permission_valid: bool = True
    safety_valid: bool = True
    resource_state: str = "available"
    cancellation_requested: bool = False
    duplicate_kinds: Tuple[str, ...] = ()
    expected_reconsideration: bool = False
    expected_observation_need: bool = False
    expected_reobserve: bool = False
    expected_proposed_task_state: str = "completed_candidate"
    differential: bool = False


def build_b4_cases_v1() -> Tuple[B4FixtureCaseV1, ...]:
    return (
        B4FixtureCaseV1("B4-01", "real B3 Task input accepted"),
        B4FixtureCaseV1("B4-02", "Task remains read-only outside Task Manager"),
        B4FixtureCaseV1("B4-03", "Action candidate created"),
        B4FixtureCaseV1("B4-04", "Action candidate is not execution"),
        B4FixtureCaseV1("B4-05", "controlled Runtime Result candidate created"),
        B4FixtureCaseV1("B4-06", "controlled result explicitly not real runtime"),
        B4FixtureCaseV1("B4-07", "ExpectedOutcomeInput created"),
        B4FixtureCaseV1("B4-08", "ActualResultInput created"),
        B4FixtureCaseV1("B4-09", "Outcome candidate created"),
        B4FixtureCaseV1("B4-10", "Outcome is not World truth"),
        B4FixtureCaseV1("B4-11", "success candidate is not external success fact"),
        B4FixtureCaseV1(
            "B4-12", "failure candidate does not directly fail Task",
            runtime_status="FAILED_CANDIDATE", expected_value="SUCCESS", actual_value="FAILURE",
            intended_status="MISMATCH", recommendation="RECONSIDER_DECISION",
            expected_reconsideration=True, expected_proposed_task_state="deferred",
        ),
        B4FixtureCaseV1("B4-13", "Task feedback handoff created"),
        B4FixtureCaseV1("B4-14", "Task Manager retains lifecycle ownership"),
        B4FixtureCaseV1(
            "B4-15", "reconsideration candidate created",
            expected_value="SUCCESS", actual_value="FAILURE", intended_status="MISMATCH",
            recommendation="RECONSIDER_DECISION", expected_reconsideration=True,
            expected_proposed_task_state="deferred",
        ),
        B4FixtureCaseV1(
            "B4-16", "reconsideration is not retry",
            expected_value="SUCCESS", actual_value="FAILURE", intended_status="MISMATCH",
            recommendation="RECONSIDER_DECISION", expected_reconsideration=True,
            expected_proposed_task_state="deferred",
        ),
        B4FixtureCaseV1(
            "B4-17", "Observation Need candidate created",
            evidence_sufficient=False, recommendation="REOBSERVE",
            expected_reconsideration=True, expected_observation_need=True,
            expected_reobserve=True, expected_proposed_task_state="requires_observation",
        ),
        B4FixtureCaseV1(
            "B4-18", "reobserve candidate does not invoke provider",
            evidence_sufficient=False, recommendation="REOBSERVE",
            expected_reconsideration=True, expected_observation_need=True,
            expected_reobserve=True, expected_proposed_task_state="requires_observation",
        ),
        B4FixtureCaseV1(
            "B4-19", "partial result path",
            runtime_status="PARTIAL_CANDIDATE", expected_value="SUCCESS", actual_value="PARTIAL",
            intended_status="PARTIAL_MATCH", recommendation="REOBSERVE",
            evidence_sufficient=False, expected_reconsideration=True,
            expected_observation_need=True, expected_reobserve=True,
            expected_proposed_task_state="requires_observation",
        ),
        B4FixtureCaseV1(
            "B4-20", "timeout and cancel path",
            runtime_status="TIMEOUT_CANDIDATE", expected_value="SUCCESS", actual_value="TIMEOUT",
            intended_status="MISMATCH", recommendation="DEFER", expected_reconsideration=True,
            expected_proposed_task_state="deferred",
        ),
        B4FixtureCaseV1(
            "B4-21", "recovery candidate boundary",
            runtime_status="CANCELLED_CANDIDATE", expected_value="SUCCESS", actual_value="CANCELLED",
            intended_status="MISMATCH", recommendation="REPLAN_TASK", expected_reconsideration=True,
            expected_proposed_task_state="deferred",
        ),
        B4FixtureCaseV1(
            "B4-22", "safety permission resource guards preserved",
            permission_valid=False, safety_valid=False, resource_state="unknown",
            expected_proposed_task_state="blocked",
        ),
        B4FixtureCaseV1(
            "B4-23", "no automatic retry",
            runtime_status="FAILED_CANDIDATE", expected_value="SUCCESS", actual_value="FAILURE",
            intended_status="MISMATCH", recommendation="RETRY_EXECUTION",
            expected_reconsideration=True, expected_proposed_task_state="deferred",
        ),
        B4FixtureCaseV1("B4-24", "no Memory or Learning"),
        B4FixtureCaseV1("B4-25", "no semantic compression"),
        B4FixtureCaseV1("B4-26", "synthetic regression preserved", real=False),
        B4FixtureCaseV1("B4-27", "differential governance compatibility", differential=True),
        B4FixtureCaseV1(
            "B4-28", "real B3 Task to Outcome to Feedback to Reobserve end-to-end candidate",
            runtime_status="PARTIAL_CANDIDATE", expected_value="SUCCESS", actual_value="PARTIAL",
            intended_status="PARTIAL_MATCH", recommendation="REOBSERVE", evidence_sufficient=False,
            expected_reconsideration=True, expected_observation_need=True,
            expected_reobserve=True, expected_proposed_task_state="requires_observation",
        ),
    )


def build_b3_task_decision_reference(case: B4FixtureCaseV1) -> B3TaskDecisionReferenceV1:
    prefix = "real" if case.real else "synthetic"
    return B3TaskDecisionReferenceV1(
        case_id=case.case_id,
        mode="REAL_B3_TASK_DECISION_INPUT" if case.real else "SYNTHETIC_B3_TASK_DECISION_INPUT",
        task_ref=f"task:{prefix}:{case.case_id}",
        task_readiness_ref=f"task-readiness:{prefix}:{case.case_id}",
        task_readiness="ready",
        decision_ref=f"decision:{prefix}:{case.case_id}",
        intent_refs=(f"intent:{prefix}:{case.case_id}",),
        current_world_ref=f"current-world:{prefix}:{case.case_id}",
        context_refs=(f"context:{prefix}:{case.case_id}",),
        field_refs=(f"field:{prefix}:{case.case_id}",),
        uncertainty_refs=(f"uncertainty:{prefix}:{case.case_id}",),
        conflict_refs=(f"conflict:{prefix}:{case.case_id}",) if case.contradictory else (),
        temporal_refs=(f"temporal:{prefix}:{case.case_id}",),
        trace_ref=f"trace:{prefix}:{case.case_id}:b3",
        provenance_refs=(f"provenance:{prefix}:{case.case_id}:b3",),
        observation_need_refs=(f"observation-need:{prefix}:{case.case_id}",) if case.expected_observation_need else (),
        candidate_only=True,
        read_only=True,
        provider_invocation=False,
        task_mutation=False,
    )
