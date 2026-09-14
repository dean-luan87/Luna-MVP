from __future__ import annotations

from typing import List, Optional, Tuple

from .a_route_product_loop_integration_core_types_v1 import (
    CONTRACT_VERSION,
    INGRESS_KINDS,
    OWNER,
    ProductCycleV1,
    ProductLoopInputV1,
    ProductLoopResultV1,
    ProductLoopTraceV1,
    ProductOutputCandidateV1,
    ProductStageHandoffV1,
    RuntimeAdmissionCandidateV1,
    ControlledExecutionRequestV1,
    ControlledExecutionResultV1,
    OutcomeFeedbackRouteV1,
    ObservationReentryCandidateV1,
    ReconsiderationCandidateV1,
    NextCycleIngressV1,
)
from .a_route_product_loop_integration_error_types_v1 import ProductLoopIntegrationErrorV1
from .a_route_product_loop_integration_ownership_guard_v1 import build_negative_guards


MAX_RECONSIDERATION_DEPTH = 2
MAX_REOBSERVATION_DEPTH = 2


class ARouteProductLoopIntegrationEngineV1:
    """Deterministic controlled product-loop caller.

    This engine only assembles immutable candidate handoffs. It never invokes
    providers, models, devices, persistence, or downstream mutation methods.
    """

    def _ref(self, request: ProductLoopInputV1, kind: str) -> str:
        return f"{kind}:{request.scenario_id}"

    def _trace_ref(self, request: ProductLoopInputV1, kind: str) -> str:
        return f"trace:{request.scenario_id}:{kind.lower()}"

    def _provenance(self, request: ProductLoopInputV1, kind: str) -> Tuple[str, ...]:
        return (f"prov:{request.scenario_id}:{kind.lower()}",)

    def _stage(
        self,
        request: ProductLoopInputV1,
        stage_id: str,
        producer: str,
        consumer: str,
        inputs: Tuple[str, ...],
        outputs: Tuple[str, ...],
        status: str = "CONTROLLED_HANDOFF_READY",
        runtime: bool = False,
        errors: Tuple[str, ...] = (),
    ) -> ProductStageHandoffV1:
        return ProductStageHandoffV1(
            stage_id=stage_id,
            producer_owner=producer,
            consumer_owner=consumer,
            input_refs=inputs,
            output_refs=outputs,
            status=status,
            handoff_contract_ref=f"contract:{stage_id.lower()}:v1",
            trace_ref=self._trace_ref(request, stage_id),
            provenance_refs=self._provenance(request, stage_id),
            mutation_authority=False,
            candidate_only=True,
            runtime_handoff_ready=runtime,
            error_refs=errors,
        )

    def _error(self, request: ProductLoopInputV1, code: str, stage: str, message: str) -> ProductLoopIntegrationErrorV1:
        return ProductLoopIntegrationErrorV1(
            code=code,
            stage_id=stage,
            message=message,
            trace_ref=self._trace_ref(request, stage),
            provenance_refs=self._provenance(request, stage),
        )

    def _trace(
        self,
        request: ProductLoopInputV1,
        stages: List[ProductStageHandoffV1],
        output: Optional[ProductOutputCandidateV1],
        errors: List[ProductLoopIntegrationErrorV1],
    ) -> ProductLoopTraceV1:
        stage_refs = tuple(item.trace_ref for item in stages)
        source_refs = (request.source_ref, self._ref(request, "ingress"))
        provenance_refs = tuple(ref for item in stages for ref in item.provenance_refs)
        error_refs = tuple(item.trace_ref for item in errors)
        terminal_ref = output.output_id if output else self._ref(request, "cycle")
        reverse = [
            (terminal_ref, tuple(item.output_refs for item in stages)[-1] if stages else (self._ref(request, "ingress"),)),
            (self._ref(request, "cycle"), source_refs + stage_refs),
        ]
        for item in stages:
            reverse.append((item.stage_id, item.input_refs + item.output_refs))
        return ProductLoopTraceV1(
            root_cycle_trace_id=f"root-trace:{request.scenario_id}",
            stage_trace_refs=stage_refs,
            handoff_trace_refs=stage_refs,
            source_refs=source_refs,
            provenance_refs=provenance_refs,
            reverse_lookup=tuple(reverse),
            correction_lineage=(request.correction_ref,) if request.correction_ref else (),
            error_refs=error_refs,
            provenance_grants_authority=False,
        )

    def _result(
        self,
        request: ProductLoopInputV1,
        state: str,
        stages: List[ProductStageHandoffV1],
        errors: List[ProductLoopIntegrationErrorV1],
        output: Optional[ProductOutputCandidateV1] = None,
        runtime_admission: Optional[RuntimeAdmissionCandidateV1] = None,
        execution_request: Optional[ControlledExecutionRequestV1] = None,
        execution_result: Optional[ControlledExecutionResultV1] = None,
        feedback: Optional[OutcomeFeedbackRouteV1] = None,
        observation_reentry: Optional[ObservationReentryCandidateV1] = None,
        reconsideration: Optional[ReconsiderationCandidateV1] = None,
        next_cycle: Optional[NextCycleIngressV1] = None,
        failure_signatures: Tuple[str, ...] = (),
    ) -> ProductLoopResultV1:
        cycle_id = self._ref(request, "cycle")
        previous = stages[-2].stage_id if len(stages) > 1 else "IDLE"
        current = stages[-1].stage_id if stages else "IDLE"
        cycle = ProductCycleV1(
            cycle_id=cycle_id,
            previous_cycle_id=request.previous_cycle_id,
            cycle_revision=1,
            current_stage=state,
            previous_stage=previous,
            pending_handoff=stages[-1].stage_id if stages else "",
            observation_need_refs=(observation_reentry.observation_need_id,) if observation_reentry else (),
            decision_ref=self._ref(request, "decision") if any(item.stage_id == "DECISION" for item in stages) else "",
            task_ref=self._ref(request, "task") if any(item.stage_id == "TASK" for item in stages) else "",
            action_ref=self._ref(request, "action") if any(item.stage_id == "ACTION" for item in stages) else "",
            execution_result_ref=execution_result.execution_result_id if execution_result else "",
            outcome_evaluation_ref=self._ref(request, "outcome-evaluation") if feedback else "",
            reconsideration_depth=request.reconsideration_depth,
            reobservation_depth=request.reobservation_depth,
            failure_signatures=failure_signatures,
            correction_refs=(request.correction_ref,) if request.correction_ref else (),
            trace_ref=f"root-trace:{request.scenario_id}",
            immutable=state in {"COMPLETED", "ABORTED"},
        )
        return ProductLoopResultV1(
            scenario_id=request.scenario_id,
            title=request.title,
            state=state,
            cycle=cycle,
            stages=tuple(stages),
            runtime_admission=runtime_admission,
            execution_request=execution_request,
            execution_result=execution_result,
            feedback=feedback,
            observation_reentry=observation_reentry,
            reconsideration=reconsideration,
            next_cycle=next_cycle,
            output=output,
            trace=self._trace(request, stages, output, errors),
            error_refs=tuple(item.code for item in errors),
            guards=build_negative_guards(),
            candidate_only=request.candidate_only,
            synthetic_only=request.synthetic_only,
        )

    def _terminal_error(self, request: ProductLoopInputV1, stages: List[ProductStageHandoffV1], code: str, stage: str, message: str, state: str) -> ProductLoopResultV1:
        error = self._error(request, code, stage, message)
        if stages:
            stages.append(self._stage(request, stage, OWNER, OWNER, stages[-1].output_refs, (), "FAILED", errors=(code,)))
        else:
            stages.append(self._stage(request, stage, "Product Input Adapter", OWNER, (request.source_ref,), (), "FAILED", errors=(code,)))
        output = ProductOutputCandidateV1(
            output_id=self._ref(request, "output"),
            output_kind="TASK_FAILED" if state == "FAILED" else "STATUS",
            content_ref=f"content:{request.scenario_id}:{state.lower()}",
            source_cycle_id=self._ref(request, "cycle"),
            trace_ref=self._trace_ref(request, "OUTPUT"),
            provenance_refs=self._provenance(request, "OUTPUT"),
        )
        return self._result(request, state, stages, [error], output=output, failure_signatures=(code,))

    def run_case(self, request: ProductLoopInputV1) -> ProductLoopResultV1:
        stages: List[ProductStageHandoffV1] = []

        if not request.synthetic_only or not request.controlled_integration_only or not request.candidate_only:
            return self._terminal_error(request, stages, "INVALID_PRODUCT_INGRESS", "INPUT", "controlled candidate mode is required", "FAILED")
        if request.ingress_kind not in INGRESS_KINDS:
            return self._terminal_error(request, stages, "INVALID_PRODUCT_INGRESS", "INPUT", "unsupported product ingress kind", "FAILED")
        if request.completed_cycle_probe:
            return self._terminal_error(request, stages, "COMPLETED_CYCLE_IMMUTABLE", "INPUT", "completed cycle is immutable", "FAILED")
        if request.aborted_cycle_probe:
            return self._terminal_error(request, stages, "ABORTED_CYCLE_IMMUTABLE", "INPUT", "aborted cycle is immutable", "FAILED")
        if request.duplicate_kind:
            code_map = {
                "input": "DUPLICATE_INPUT", "observation_demand": "DUPLICATE_INPUT", "observation_feedback": "DUPLICATE_FEEDBACK",
                "decision_handoff": "DUPLICATE_INPUT", "task": "DUPLICATE_TASK", "action": "DUPLICATE_ACTION",
                "execution_request": "DUPLICATE_EXECUTION_REQUEST", "execution_result": "DUPLICATE_RESULT",
                "evaluation": "DUPLICATE_EVALUATION", "feedback": "DUPLICATE_FEEDBACK", "user_correction": "DUPLICATE_FEEDBACK",
                "next_cycle": "DUPLICATE_NEXT_CYCLE_INGRESS",
            }
            code = code_map.get(request.duplicate_kind, "INVALID_PRODUCT_INGRESS")
            return self._terminal_error(request, stages, code, "INPUT", f"duplicate {request.duplicate_kind} is idempotently rejected", "FAILED")
        if request.reconsideration_depth > request.max_reconsideration_depth:
            return self._terminal_error(request, stages, "RECONSIDERATION_DEPTH_EXCEEDED", "FEEDBACK", "reconsideration depth exceeded", "FAILED")
        if request.reobservation_depth > request.max_reobservation_depth:
            return self._terminal_error(request, stages, "REOBSERVATION_DEPTH_EXCEEDED", "OBSERVATION", "re-observation depth exceeded", "FAILED")

        ingress_ref = self._ref(request, "ingress")
        stages.append(self._stage(request, "INPUT", "Product Input Adapter", OWNER, (request.source_ref,), (ingress_ref,)))

        if request.task_cancelled or request.safety_interrupted:
            code = "TASK_CANCELLED" if request.task_cancelled else "SAFETY_INTERRUPTION"
            return self._terminal_error(request, stages, code, "INPUT", "cycle is explicitly interrupted", "ABORTED")

        if request.requires_observation:
            stages.append(self._stage(request, "OBSERVATION_REQUIRED", OWNER, "Field Perception Orchestrator", (ingress_ref,), (self._ref(request, "observation-demand"),)))
            if request.provider_failure:
                return self._deferred(request, stages, "provider failure requires bounded fallback", "PROVIDER_FAILURE")
            if not request.provider_available:
                return self._deferred(request, stages, "no provider is available", "PROVIDER_UNAVAILABLE")
            if not request.observation_available:
                return self._reobserve(request, stages, "observation evidence is unavailable")
            stages.append(self._stage(request, "OBSERVING", "Field Perception Orchestrator", "Observation Gateway", (self._ref(request, "observation-demand"),), (self._ref(request, "observation-session"),)))
            stages.append(self._stage(request, "OBSERVATION_READY", "Observation Gateway", "Context Foundation / Field State Reducer", (self._ref(request, "observation-session"),), (self._ref(request, "observation"),)))

        context_inputs = (ingress_ref,) + ((self._ref(request, "observation"),) if request.requires_observation else ())
        stages.append(self._stage(request, "WORLD_CONTEXT_READY", "Context Foundation / Field State Reducer", "Cognitive State Formation", context_inputs, (self._ref(request, "context"), self._ref(request, "current-world"))))
        stages.append(self._stage(request, "COGNITION_READY", "Cognitive State Formation / Cognitive Flow", "Intent / Causal / Decision Governance", (self._ref(request, "context"), self._ref(request, "current-world")), (self._ref(request, "cognitive-state"), self._ref(request, "intent"), self._ref(request, "regulation"))))
        stages.append(self._stage(request, "DECISION_READY", "Causal / Decision Governance", "Task Manager", (self._ref(request, "cognitive-state"), self._ref(request, "intent")), (self._ref(request, "decision"),)))

        if request.controlled_only_fallback:
            stages.append(self._stage(request, "DEFERRED", OWNER, "Product Output Adapter", (self._ref(request, "decision"),), (self._ref(request, "output"),), "DEFERRED"))
            output = self._output(request, "GUIDANCE", "controlled-only fallback")
            error = self._error(request, "CONTROLLED_ONLY_FALLBACK", "DEFERRED", "real runtime is intentionally unavailable")
            feedback = OutcomeFeedbackRouteV1(self._ref(request, "feedback"), self._ref(request, "outcome-evaluation"), "DEFER", ("controlled-only fallback",), trace_ref=self._trace_ref(request, "FEEDBACK"), provenance_refs=self._provenance(request, "FEEDBACK"))
            return self._result(request, "DEFERRED", stages, [error], output=output, feedback=feedback)
        if not request.requires_action:
            output = self._output(request, "RESPONSE", "cognitive response candidate")
            feedback = OutcomeFeedbackRouteV1(
                feedback_id=self._ref(request, "feedback"),
                evaluation_ref=self._ref(request, "outcome-evaluation"),
                route="COMPLETE",
                reason_refs=("response-candidate-complete",),
                trace_ref=self._trace_ref(request, "FEEDBACK"),
                provenance_refs=self._provenance(request, "FEEDBACK"),
            )
            stages.append(self._stage(request, "FEEDBACK", OWNER, OWNER, (self._ref(request, "decision"),), (feedback.feedback_id,)))
            stages.append(self._stage(request, "COMPLETED", OWNER, "Product Output Adapter", (feedback.feedback_id,), (output.output_id,)))
            return self._result(request, "COMPLETED", stages, [], output=output, feedback=feedback)

        stages.append(self._stage(request, "TASK_READY", "Task Manager", "Action Governance", (self._ref(request, "decision"),), (self._ref(request, "task"),)))
        stages.append(self._stage(request, "ACTION_READY", "Action Governance", "Runtime Executor", (self._ref(request, "task"),), (self._ref(request, "action"),)))

        if request.resource_constrained or not request.runtime_available:
            return self._deferred(request, stages, "runtime admission is unavailable or resource constrained", "RUNTIME_NOT_ADMITTED")

        admission = RuntimeAdmissionCandidateV1(
            admission_id=self._ref(request, "runtime-admission"),
            action_ref=self._ref(request, "action"),
            consumer_owner="Runtime Executor",
            permission_ref=self._ref(request, "permission"),
            resource_budget_ref=self._ref(request, "resource-budget"),
            trace_ref=self._trace_ref(request, "RUNTIME_ADMISSION"),
            provenance_refs=self._provenance(request, "RUNTIME_ADMISSION"),
        )
        stages.append(self._stage(request, "EXECUTION_PENDING", "A Route Orchestration Governance", "Runtime Executor", (self._ref(request, "action"),), (admission.admission_id,)))
        execution_request = ControlledExecutionRequestV1(
            execution_request_id=self._ref(request, "execution-request"),
            admission_ref=admission.admission_id,
            action_ref=admission.action_ref,
            expected_outcome_ref=self._ref(request, "expected-outcome"),
            trace_ref=self._trace_ref(request, "EXECUTION_REQUEST"),
            provenance_refs=self._provenance(request, "EXECUTION_REQUEST"),
        )
        stages.append(self._stage(request, "EXECUTING", "Runtime Executor", "Controlled Result Adapter", (execution_request.execution_request_id,), (self._ref(request, "execution-result"),)))
        result = ControlledExecutionResultV1(
            execution_result_id=self._ref(request, "execution-result"),
            execution_request_ref=execution_request.execution_request_id,
            status=request.execution_status,
            actual_result_ref=self._ref(request, "actual-result"),
            trace_ref=self._trace_ref(request, "RESULT"),
            provenance_refs=self._provenance(request, "RESULT"),
            temporal_refs=("stale",) if request.stale_result else ("within-window",),
            failure_refs=("execution-failure",) if request.execution_status == "FAILED" else (),
        )
        stages.append(self._stage(request, "RESULT_READY", "Controlled Result Adapter", "Outcome Evaluation Governance", (result.execution_result_id,), (result.actual_result_ref,)))
        stages.append(self._stage(request, "EVALUATING", "Outcome Evaluation Governance", OWNER, (self._ref(request, "expected-outcome"), result.actual_result_ref), (self._ref(request, "outcome-evaluation"),)))

        if request.repeated_failure_signature:
            stages.append(self._stage(request, "FEEDBACK", "Outcome Evaluation Governance", OWNER, (self._ref(request, "outcome-evaluation"),), (self._ref(request, "feedback"),), "FAILED", errors=("REPEATED_FAILURE_SIGNATURE",)))
            feedback = OutcomeFeedbackRouteV1(self._ref(request, "feedback"), self._ref(request, "outcome-evaluation"), "FAIL", ("repeated failure signature",), trace_ref=self._trace_ref(request, "FEEDBACK"), provenance_refs=self._provenance(request, "FEEDBACK"))
            output = self._output(request, "TASK_FAILED", "repeated failure signature")
            stages.append(self._stage(request, "FAILED", OWNER, "Product Output Adapter", (feedback.feedback_id,), (output.output_id,), "FAILED", errors=("REPEATED_FAILURE_SIGNATURE",)))
            error = self._error(request, "REPEATED_FAILURE_SIGNATURE", "FEEDBACK", "repeated failure signature is terminal")
            return self._result(request, "FAILED", stages, [error], output=output, runtime_admission=admission, execution_request=execution_request, execution_result=result, feedback=feedback, failure_signatures=("REPEATED_FAILURE_SIGNATURE",))

        if request.stale_result or not request.observation_sufficient:
            return self._reobserve(request, stages, "outcome evidence is stale or insufficient", result=result, admission=admission, execution_request=execution_request)
        if request.user_correction or request.contradiction or request.unresolved_hypothesis or request.execution_status in {"FAILED", "PARTIAL"}:
            reason = "user correction" if request.user_correction else "contradictory or non-complete outcome"
            return self._reconsider(request, stages, reason, result, admission, execution_request)

        stages.append(self._stage(request, "FEEDBACK", "Outcome Evaluation Governance", OWNER, (self._ref(request, "outcome-evaluation"),), (self._ref(request, "feedback"),)))
        route = "NEXT_CYCLE" if request.next_cycle_requested or request.learning_signal else "COMPLETE"
        feedback = OutcomeFeedbackRouteV1(
            feedback_id=self._ref(request, "feedback"),
            evaluation_ref=self._ref(request, "outcome-evaluation"),
            route=route,
            reason_refs=("sufficient-outcome",),
            learning_signal_ref=self._ref(request, "learning-signal") if request.learning_signal else "",
            trace_ref=self._trace_ref(request, "FEEDBACK"),
            provenance_refs=self._provenance(request, "FEEDBACK"),
        )
        next_cycle = self._next_cycle(request, feedback) if route == "NEXT_CYCLE" else None
        final_state = "NEXT_CYCLE_READY" if next_cycle else "COMPLETED"
        output = self._output(request, "TASK_COMPLETED" if request.requires_action else "RESPONSE", "controlled outcome evaluated")
        stages.append(self._stage(request, "COMPLETED" if final_state == "COMPLETED" else "NEXT_CYCLE_READY", OWNER, "Product Output Adapter", (feedback.feedback_id,), (output.output_id,)))
        return self._result(request, final_state, stages, [], output=output, runtime_admission=admission, execution_request=execution_request, execution_result=result, feedback=feedback, next_cycle=next_cycle)

    def _output(self, request: ProductLoopInputV1, kind: str, content: str) -> ProductOutputCandidateV1:
        return ProductOutputCandidateV1(
            output_id=self._ref(request, "output"),
            output_kind=kind,
            content_ref=f"content:{request.scenario_id}:{content.replace(' ', '-')}",
            source_cycle_id=self._ref(request, "cycle"),
            trace_ref=self._trace_ref(request, "OUTPUT"),
            provenance_refs=self._provenance(request, "OUTPUT"),
        )

    def _deferred(self, request: ProductLoopInputV1, stages: List[ProductStageHandoffV1], reason: str, code: str) -> ProductLoopResultV1:
        stages.append(self._stage(request, "DEFERRED", OWNER, "Product Output Adapter", stages[-1].output_refs, (self._ref(request, "output"),), "DEFERRED"))
        output = self._output(request, "DEFERRED", reason)
        error = self._error(request, code, "DEFERRED", reason)
        feedback = OutcomeFeedbackRouteV1(self._ref(request, "feedback"), self._ref(request, "outcome-evaluation"), "DEFER", (code,), trace_ref=self._trace_ref(request, "FEEDBACK"), provenance_refs=self._provenance(request, "FEEDBACK"))
        return self._result(request, "DEFERRED", stages, [error], output=output, feedback=feedback)

    def _reobserve(self, request: ProductLoopInputV1, stages: List[ProductStageHandoffV1], reason: str, result: Optional[ControlledExecutionResultV1] = None, admission: Optional[RuntimeAdmissionCandidateV1] = None, execution_request: Optional[ControlledExecutionRequestV1] = None) -> ProductLoopResultV1:
        if request.reobservation_depth >= request.max_reobservation_depth:
            return self._terminal_error(request, stages, "REOBSERVATION_DEPTH_EXCEEDED", "FEEDBACK", reason, "FAILED")
        evaluation_ref = self._ref(request, "outcome-evaluation")
        need = ObservationReentryCandidateV1(self._ref(request, "observation-need"), evaluation_ref, request.information_need or "unresolved outcome", request.observation_modality or "TARGETED", self._ref(request, "observation-budget"), self._trace_ref(request, "OBSERVATION_REENTRY"), self._provenance(request, "OBSERVATION_REENTRY"))
        feedback = OutcomeFeedbackRouteV1(self._ref(request, "feedback"), evaluation_ref, "REOBSERVE", (reason,), observation_need_ref=need.observation_need_id, trace_ref=self._trace_ref(request, "FEEDBACK"), provenance_refs=self._provenance(request, "FEEDBACK"))
        stages.append(self._stage(request, "REOBSERVATION_REQUIRED", "Outcome Evaluation Governance", "Field Perception Orchestrator", (evaluation_ref,), (need.observation_need_id,), "CONTROLLED_HANDOFF_READY"))
        output = self._output(request, "OBSERVATION_REQUIRED", reason)
        stages.append(self._stage(request, "REOBSERVATION_REQUIRED_OUTPUT", OWNER, "Product Output Adapter", (need.observation_need_id,), (output.output_id,)))
        errors = [self._error(request, "INSUFFICIENT_OUTCOME_EVIDENCE", "REOBSERVATION_REQUIRED", reason)]
        return self._result(request, "REOBSERVATION_REQUIRED", stages, errors, output=output, runtime_admission=admission, execution_request=execution_request, execution_result=result, feedback=feedback, observation_reentry=need)

    def _reconsider(self, request: ProductLoopInputV1, stages: List[ProductStageHandoffV1], reason: str, result: ControlledExecutionResultV1, admission: RuntimeAdmissionCandidateV1, execution_request: ControlledExecutionRequestV1) -> ProductLoopResultV1:
        if request.reconsideration_depth >= request.max_reconsideration_depth:
            return self._terminal_error(request, stages, "RECONSIDERATION_DEPTH_EXCEEDED", "FEEDBACK", reason, "FAILED")
        evaluation_ref = self._ref(request, "outcome-evaluation")
        reconsider = ReconsiderationCandidateV1(self._ref(request, "reconsideration"), evaluation_ref, reason, request.reconsideration_depth + 1, request.max_reconsideration_depth, self._trace_ref(request, "RECONSIDERATION"), self._provenance(request, "RECONSIDERATION"))
        feedback = OutcomeFeedbackRouteV1(self._ref(request, "feedback"), evaluation_ref, "RECONSIDER", (reason,), reconsideration_ref=reconsider.reconsideration_id, learning_signal_ref=self._ref(request, "learning-signal") if request.learning_signal else "", trace_ref=self._trace_ref(request, "FEEDBACK"), provenance_refs=self._provenance(request, "FEEDBACK"))
        stages.append(self._stage(request, "RECONSIDERING", "Outcome Evaluation Governance", OWNER, (evaluation_ref, result.actual_result_ref), (reconsider.reconsideration_id,)))
        output = self._output(request, "GUIDANCE", reason)
        stages.append(self._stage(request, "RECONSIDERING_OUTPUT", OWNER, "Product Output Adapter", (reconsider.reconsideration_id,), (output.output_id,)))
        errors = [self._error(request, "OUTCOME_REQUIRES_RECONSIDERATION", "RECONSIDERING", reason)]
        return self._result(request, "RECONSIDERING", stages, errors, output=output, runtime_admission=admission, execution_request=execution_request, execution_result=result, feedback=feedback, reconsideration=reconsider)

    def _next_cycle(self, request: ProductLoopInputV1, feedback: OutcomeFeedbackRouteV1) -> NextCycleIngressV1:
        return NextCycleIngressV1(self._ref(request, "next-cycle"), self._ref(request, "cycle"), feedback.feedback_id, (self._ref(request, "context"), self._ref(request, "feedback")), self._trace_ref(request, "NEXT_CYCLE"), self._provenance(request, "NEXT_CYCLE"))
