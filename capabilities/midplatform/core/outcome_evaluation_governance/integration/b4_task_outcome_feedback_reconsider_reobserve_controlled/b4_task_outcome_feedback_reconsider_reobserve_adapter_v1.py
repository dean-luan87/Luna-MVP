"""Narrow B3 -> Action/Outcome/Feedback mapping for B4."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.action_governance.action_confirmation_types_v1 import (
    ConfirmationStatusV1,
)
from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    SourceRefV1 as ActionSourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_dependency_types_v1 import (
    ActionDependencyCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    ActionPreconditionCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.outcome_evaluation_governance.outcome_evaluation_core_types_v1 import (
    ActualResultInputV1,
    ExpectedOutcomeInputV1,
    OutcomeEvaluationRequestV1,
)
from capabilities.midplatform.core.outcome_evaluation_governance.outcome_evaluation_engine_v1 import (
    OutcomeEvaluationEngineV1,
)
from capabilities.midplatform.core.runtime_executor.execution_result_types_v1 import (
    ExecutionResultCandidateV1,
)

from .b4_task_outcome_feedback_reconsider_reobserve_types_v1 import (
    B3TaskDecisionReferenceV1,
    ControlledRuntimeResultCandidateV1,
    ReobserveCandidateV1,
    TaskLifecycleFeedbackHandoffCandidateV1,
)


def _ref(owner: str, ref_id: str, ref_type: str) -> ActionSourceRefV1:
    return ActionSourceRefV1(
        owner=owner,
        ref_id=ref_id,
        ref_type=ref_type,
        read_only=True,
        reference_only=True,
        source_mutation_allowed=False,
    )


def validate_b3_reference(source: B3TaskDecisionReferenceV1) -> Tuple[str, ...]:
    issues = []
    required = {
        "task_ref": source.task_ref,
        "task_readiness_ref": source.task_readiness_ref,
        "decision_ref": source.decision_ref,
        "current_world_ref": source.current_world_ref,
        "trace_ref": source.trace_ref,
    }
    issues.extend(name for name, value in required.items() if not str(value).strip())
    if source.mode not in {"REAL_B3_TASK_DECISION_INPUT", "SYNTHETIC_B3_TASK_DECISION_INPUT"}:
        issues.append("unsupported_b3_input_mode")
    if not source.candidate_only:
        issues.append("b3_input_not_candidate_only")
    if not source.read_only:
        issues.append("b3_input_not_read_only")
    if source.provider_invocation:
        issues.append("b3_provider_invocation_present")
    if source.task_mutation:
        issues.append("b3_task_mutation_present")
    if not source.temporal_refs or not source.provenance_refs:
        issues.append("missing_b3_lineage_refs")
    return tuple(issues)


def build_action_input(
    source: B3TaskDecisionReferenceV1,
    *,
    permission_valid: bool = True,
    safety_valid: bool = True,
    resource_state: str = "available",
    cancellation_requested: bool = False,
) -> ActionGovernanceInputV1:
    case_id = source.case_id
    return ActionGovernanceInputV1(
        scenario_id=f"B4-ACTION-{case_id}",
        selected_decision_refs=(_ref("Decision Governance", source.decision_ref, "DECISION_CANDIDATE"),),
        intent_refs=tuple(_ref("Intent Governance", ref, "INTENT_REFERENCE") for ref in source.intent_refs),
        causal_refs=(_ref("Cognitive Flow Governance", source.trace_ref, "COGNITIVE_FLOW"),),
        target_refs=(_ref("Task Manager", source.task_ref, "TASK_CANDIDATE"),),
        context_refs=tuple(_ref("Context Foundation", ref, "CONTEXT") for ref in source.context_refs),
        field_refs=tuple(_ref("Field State Reducer", ref, "FIELD_REFERENCE") for ref in source.field_refs),
        permission_refs=(_ref("Permission Governance", f"permission:{case_id}", "PERMISSION"),),
        safety_refs=(_ref("Safety Governance", f"safety:{case_id}", "SAFETY"),),
        confirmation_refs=(_ref("Human Oversight", f"confirmation:{case_id}", "CONFIRMATION"),),
        preconditions=(ActionPreconditionCandidateV1(
            precondition_id=f"precondition:{case_id}:b3-task-ready",
            domain="b3_task_readiness",
            status="satisfied" if source.task_readiness == "ready" else "unknown",
            required=True,
            provenance_refs=source.provenance_refs,
        ),),
        dependencies=(ActionDependencyCandidateV1(
            dependency_id=f"dependency:{case_id}:controlled-result",
            dependency_type="controlled_runtime_result_fixture",
            status="satisfied",
            blocking=True,
            provenance_refs=source.provenance_refs,
        ),),
        resource_refs=(_ref("Resource Governance", f"resource:{case_id}", "RESOURCE"),),
        resource_state=resource_state,
        permission_valid=permission_valid,
        safety_valid=safety_valid,
        confirmation=ConfirmationStatusV1(
            state="not_required",
            is_stale=False,
            is_fabricated=False,
            strong_confirmation=False,
        ),
        reversibility="reversible",
        target_valid=True,
        cancellation_requested=cancellation_requested,
        rollback_required=False,
        failure_result=None,
        revision_requested=False,
        prefer_eligible_state=True,
        task_reference_context_refs=(_ref("Task Manager", source.task_ref, "TASK_REFERENCE"),),
        synthetic_only=True,
        candidate_only=True,
    )


def run_action(source: B3TaskDecisionReferenceV1, **kwargs):
    return ActionGovernanceEngineV1().run_case(build_action_input(source, **kwargs))


def build_controlled_runtime_result(
    source: B3TaskDecisionReferenceV1,
    action_output,
    *,
    runtime_status: str,
) -> ControlledRuntimeResultCandidateV1:
    case_id = source.case_id
    result = ExecutionResultCandidateV1(
        execution_id=f"controlled-execution:{case_id}",
        request_id=f"controlled-runtime-request:{case_id}",
        status=runtime_status,
        attempt_count=1,
        started_at=f"controlled-start:{case_id}",
        ended_at=f"controlled-end:{case_id}",
        trace_ref=f"trace:{case_id}:controlled-runtime-result",
        failure_ref=f"controlled-failure:{case_id}" if runtime_status in {"FAILED_CANDIDATE", "TIMEOUT_CANDIDATE", "CANCELLED_CANDIDATE"} else None,
        partial_result_ref=f"controlled-partial:{case_id}" if runtime_status == "PARTIAL_CANDIDATE" else None,
        candidate_only=True,
        planning_only=True,
    )
    return ControlledRuntimeResultCandidateV1(
        result=result,
        action_ref=action_output.action_candidate.action_candidate_id,
        task_ref=source.task_ref,
        decision_ref=source.decision_ref,
        runtime_request_ref=result.request_id,
        controlled_fixture=True,
        real_runtime_execution=False,
        device_side_effect=False,
        scheduler_execution=False,
        candidate_only=True,
        provenance_refs=(
            f"provenance:{case_id}:b3",
            f"provenance:{case_id}:action",
            f"provenance:{case_id}:controlled-runtime-fixture",
        ),
    )


def build_expected_outcome(source: B3TaskDecisionReferenceV1, *, expected_value: str) -> ExpectedOutcomeInputV1:
    return ExpectedOutcomeInputV1(
        expectation_ref=f"expectation:{source.case_id}",
        expectation_kind="B3_TASK_ACTION_EXPECTATION_CANDIDATE",
        source_owner="Decision Governance",
        source_ref=source.decision_ref,
        target_ref=source.task_ref,
        semantic_scope="task_candidate_effect",
        temporal_scope="controlled-candidate-window",
        spatial_scope="task-candidate-scope",
        expected_attributes=("task_candidate", "action_candidate", "candidate_result"),
        completion_criteria=("candidate_only", "governance_feedback_available"),
        expected_value=expected_value,
        uncertainty_refs=source.uncertainty_refs,
        trace_ref=f"trace:{source.case_id}:expected-outcome",
        provenance_refs=source.provenance_refs,
        candidate_only=True,
        truth_declared=False,
    )


def build_actual_result(
    source: B3TaskDecisionReferenceV1,
    controlled: ControlledRuntimeResultCandidateV1,
    *,
    actual_value: str,
) -> ActualResultInputV1:
    result = controlled.result
    return ActualResultInputV1(
        actual_result_ref=result.execution_id,
        source_owner="Runtime Executor",
        source_ref=controlled.runtime_request_ref,
        result_kind="CONTROLLED_RUNTIME_RESULT_FIXTURE",
        target_ref=source.task_ref,
        observed_at=result.ended_at,
        valid_from=result.started_at,
        valid_until="controlled-candidate-window-end",
        status_candidate=result.status,
        observed_attributes=("controlled_fixture", "candidate_only", "no_device_side_effect"),
        actual_value=actual_value,
        uncertainty_refs=source.uncertainty_refs,
        contradiction_refs=source.conflict_refs,
        trace_ref=result.trace_ref,
        provenance_refs=controlled.provenance_refs,
        source_valid=True,
        candidate_only=True,
        truth_declared=False,
    )


def build_outcome_request(
    source: B3TaskDecisionReferenceV1,
    expected: ExpectedOutcomeInputV1,
    actual: ActualResultInputV1,
    *,
    intended_status: str,
    evidence_sufficient: bool,
    contradictory: bool,
    recommendation: str,
    duplicate_kinds: Tuple[str, ...] = (),
    task_completion_candidate: str = "",
) -> OutcomeEvaluationRequestV1:
    return OutcomeEvaluationRequestV1(
        scenario_id=source.case_id,
        root_cycle_trace_id=source.trace_ref,
        expected=expected,
        actual=actual,
        intended_status=intended_status,
        evidence_sufficient=evidence_sufficient,
        contradictory=contradictory,
        recommendation=recommendation,
        observation_information_gap="controlled runtime result does not verify external effect" if not evidence_sufficient else None,
        expected_evidence_kinds=("RESULT_OBSERVATION",) if not evidence_sufficient else (),
        duplicate_kinds=duplicate_kinds,
        task_completion_candidate=task_completion_candidate,
        context_refs=source.context_refs,
        intent_refs=source.intent_refs,
        current_world_refs=(source.current_world_ref,),
        feedback_refs=(f"feedback:{source.case_id}",),
        counterexample_refs=source.conflict_refs,
        learning_signal_allowed=False,
        synthetic_only=True,
        candidate_only=True,
    )


def run_outcome(request):
    return OutcomeEvaluationEngineV1().run_case(request)


def build_task_feedback(source, outcome_output, action_output=None) -> TaskLifecycleFeedbackHandoffCandidateV1:
    recommendation = outcome_output.reconsideration.recommendation if outcome_output.reconsideration else "NO_ACTION"
    proposed = {
        "REOBSERVE": "requires_observation",
        "RECONSIDER_DECISION": "deferred",
        "REPLAN_TASK": "deferred",
        "RETRY_EXECUTION": "deferred",
        "REQUEST_USER_CONFIRMATION": "blocked",
        "DEFER": "deferred",
    }.get(recommendation, "completed_candidate" if outcome_output.deviation.status == "MATCH" else "pending")
    if action_output is not None and action_output.readiness.state != "candidate_ready":
        proposed = "blocked"
        recommendation = "ACTION_GATE_BLOCKED"
    reasons = outcome_output.comparability.blocked_reason_refs or (f"deviation:{source.case_id}",)
    if action_output is not None and action_output.readiness.state != "candidate_ready":
        reasons = (*reasons, f"action-state:{action_output.action_candidate.action_state}")
    return TaskLifecycleFeedbackHandoffCandidateV1(
        feedback_id=f"task-feedback:{source.case_id}",
        task_ref=source.task_ref,
        outcome_ref=outcome_output.evaluation.evaluation_id,
        proposed_lifecycle_state=proposed,
        feedback_kind=recommendation,
        reason_refs=reasons,
        trace_ref=f"trace:{source.case_id}:task-feedback",
        provenance_refs=(f"provenance:{source.case_id}:task-feedback",),
    )


def build_reconsideration(source, outcome_output):
    handoff = outcome_output.reconsideration
    if handoff is None:
        return None
    return ReconsiderationCandidateV1(
        cycle_id=f"cycle:{source.case_id}",
        source_stage="Outcome Evaluation Governance",
        target_stage="Cognitive Flow Governance",
        reconsideration_reason=handoff.recommendation,
        related_refs=(handoff.evaluation_ref, *handoff.expected_refs, *handoff.actual_refs, *handoff.reason_refs),
        candidate_only=True,
        runtime_execution=False,
        trace_ref=handoff.trace_ref,
    )


def build_reobserve(source, outcome_output):
    need = outcome_output.observation_need
    if need is None:
        return None
    return ReobserveCandidateV1(
        reobserve_id=f"reobserve:{source.case_id}",
        observation_need_ref=need.observation_need_id,
        evaluation_ref=need.evaluation_ref,
        reason_refs=(need.information_gap,),
        trace_ref=need.trace_ref,
        provenance_refs=need.provenance_refs,
        candidate_only=True,
        provider_invocation=False,
        camera_activation=False,
    )
