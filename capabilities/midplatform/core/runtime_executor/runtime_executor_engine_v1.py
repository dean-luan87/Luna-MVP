"""Deterministic Runtime Executor engine for synthetic controlled implementation."""

from __future__ import annotations

from capabilities.midplatform.core.runtime_executor.admission_result_types_v1 import (
    AdmissionResultCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_adapter_reference_types_v1 import (
    AdapterReferenceCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_attempt_types_v1 import (
    ExecutionAttemptCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_cancellation_types_v1 import (
    CancellationCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_diagnostics_handoff_types_v1 import (
    DiagnosticsHandoffCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_failure_types_v1 import (
    ExecutionFailureCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_final_gate_types_v1 import (
    ExecutionFinalGateResultV1,
)
from capabilities.midplatform.core.runtime_executor.execution_idempotency_types_v1 import (
    IdempotencyRecordV1,
    IdempotencyRegistryV1,
)
from capabilities.midplatform.core.runtime_executor.execution_partial_result_types_v1 import (
    PartialExecutionResultCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_result_types_v1 import (
    ExecutionResultCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_retry_types_v1 import (
    RetryRequestCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_rollback_types_v1 import (
    RollbackContextCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_scheduler_reference_types_v1 import (
    SchedulerReferenceCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_state_types_v1 import (
    ExecutionStateSnapshotV1,
    ExecutionStateTransitionCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_task_reference_types_v1 import (
    TaskReferenceCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_timeout_types_v1 import (
    TimeoutCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_trace_types_v1 import (
    ExecutionTraceCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_io_types_v1 import (
    RuntimeExecutorInputV1,
    RuntimeExecutorOutputV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_registry_v1 import (
    ACTION_GOVERNANCE_OWNER,
    DIAGNOSTICS_OWNER,
    RUNTIME_EXECUTOR_OWNER,
    TASK_MANAGER_OWNER,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_handoff_types_v1 import (
    ResultHandoffCandidateV1,
)


class RuntimeExecutorEngineV1:
    def __init__(self) -> None:
        self._idempotency = IdempotencyRegistryV1()

    def _make_handoff(
        self,
        scenario_id: str,
        consumer: str,
        result_ref: str,
        failure_ref: str | None,
        partial_ref: str | None,
    ) -> ResultHandoffCandidateV1:
        return ResultHandoffCandidateV1(
            handoff_id=f"handoff:{scenario_id}:{consumer.lower().replace(' ', '-')}",
            producer_owner=RUNTIME_EXECUTOR_OWNER,
            consumer_owner=consumer,
            handoff_kind="RUNTIME_EXECUTOR_RESULT_CANDIDATE_HANDOFF",
            execution_result_candidate_ref=result_ref,
            failure_candidate_ref_optional=failure_ref,
            partial_result_candidate_ref_optional=partial_ref,
            trace_ref=f"trace:{scenario_id}",
            provenance_ref=f"prov:{scenario_id}:handoff:{consumer.lower().replace(' ', '-')}",
            reference_only=True,
            owner_mutation=False,
        )

    def run_case(self, request: RuntimeExecutorInputV1) -> RuntimeExecutorOutputV1:
        scenario_id = request.scenario_id
        execution_id = f"execution:{scenario_id}"

        existing = self._idempotency.get(request.request.idempotency_key)
        idempotency_duplicate = False
        idempotency_scope_mismatch = False
        duplicate_attempt_created = False

        if existing is not None:
            if existing.scope_key == request.request.scope_key:
                idempotency_duplicate = True
            else:
                idempotency_scope_mismatch = True

        admitted = (
            request.readiness_fresh
            and request.permission_valid
            and request.safety_valid
            and request.confirmation_valid
            and request.final_scope_valid
            and not idempotency_scope_mismatch
        )
        admission_reason = "admitted"
        if not admitted:
            if idempotency_scope_mismatch:
                admission_reason = "idempotency_scope_mismatch"
            elif not request.permission_valid:
                admission_reason = "permission_recheck_failed"
            elif not request.safety_valid:
                admission_reason = "safety_recheck_failed"
            elif not request.confirmation_valid:
                admission_reason = "confirmation_invalid"
            elif not request.final_scope_valid:
                admission_reason = "confirmation_scope_mismatch"
            elif not request.readiness_fresh:
                admission_reason = "readiness_stale"

        admission = AdmissionResultCandidateV1(
            execution_request_id=request.request.execution_request_id,
            admitted=admitted,
            state="ADMITTED_CANDIDATE" if admitted else "REJECTED_CANDIDATE",
            reason=admission_reason,
            permission_valid=request.permission_valid,
            safety_valid=request.safety_valid,
            confirmation_valid=request.confirmation_valid,
            readiness_fresh=request.readiness_fresh,
            candidate_only=True,
        )

        final_gate = ExecutionFinalGateResultV1(
            passed=(
                admitted
                and request.final_scope_valid
                and request.final_time_window_valid
            ),
            permission_valid=request.permission_valid,
            safety_valid=request.safety_valid,
            confirmation_valid=request.confirmation_valid,
            scope_valid=request.final_scope_valid,
            time_window_valid=request.final_time_window_valid,
            reason="passed"
            if admitted
            and request.final_scope_valid
            and request.final_time_window_valid
            else "blocked_before_execution",
            candidate_only=True,
        )

        retry_blocked = request.retry_requested and not request.retry_authorized
        retry = RetryRequestCandidateV1(
            retry_requested=request.retry_requested,
            retry_authorized=request.retry_authorized,
            retry_authorized_by=request.retry_authorized_by,
            failure_classification="runtime_failure" if request.force_failure else None,
            previous_attempt_ref=request.previous_attempt_ref,
            blocked_reason="retry_without_authority" if retry_blocked else None,
            candidate_only=True,
        )

        timeout = TimeoutCandidateV1(
            admission_timeout_ms=300,
            queue_timeout_ms=1200,
            execution_timeout_ms=4000,
            timed_out=request.force_timeout,
            timeout_stage="queue"
            if request.force_timeout and request.scheduler_delay
            else ("execution" if request.force_timeout else None),
            trace_required=True,
            candidate_only=True,
        )

        cancellation = CancellationCandidateV1(
            cancel_requested=request.cancel_requested,
            cancel_reason="user_requested" if request.cancel_requested else None,
            cancelled=request.cancel_requested,
            cancelled_state="CANCELLED_CANDIDATE"
            if request.cancel_requested
            else "NOT_CANCELLED",
            trace_required=True,
            candidate_only=True,
        )

        status = "SUCCEEDED_CANDIDATE"
        if not admitted or not final_gate.passed:
            status = "REJECTED_CANDIDATE"
        elif idempotency_duplicate:
            status = existing.status if existing else "SUCCEEDED_CANDIDATE"
        elif retry_blocked and request.force_failure:
            status = "FAILED_CANDIDATE"
        elif timeout.timed_out:
            status = "TIMEOUT_CANDIDATE"
        elif cancellation.cancelled:
            status = "CANCELLED_CANDIDATE"
        elif request.force_partial and request.force_failure:
            status = "FAILED_CANDIDATE"
        elif request.force_partial:
            status = "PARTIAL_RESULT_CANDIDATE"
        elif request.force_failure:
            status = "FAILED_CANDIDATE"

        attempt_number = 1
        if request.retry_requested and request.retry_authorized:
            attempt_number = 2

        attempt = ExecutionAttemptCandidateV1(
            execution_id=execution_id,
            attempt_id=f"attempt:{scenario_id}:{attempt_number}",
            attempt_number=attempt_number,
            previous_attempt_ref=request.previous_attempt_ref,
            retry_requested=request.retry_requested,
            retry_authorized=request.retry_authorized,
            retry_authorized_by=request.retry_authorized_by,
            candidate_only=True,
        )

        if idempotency_duplicate:
            duplicate_attempt_created = False
            attempt = ExecutionAttemptCandidateV1(
                execution_id=existing.execution_id if existing else execution_id,
                attempt_id=f"attempt:{scenario_id}:duplicate-reuse",
                attempt_number=1,
                previous_attempt_ref=None,
                retry_requested=False,
                retry_authorized=False,
                retry_authorized_by=None,
                candidate_only=True,
            )

        state = ExecutionStateSnapshotV1(
            execution_id=execution_id,
            state=status,
            terminal=status
            in {
                "SUCCEEDED_CANDIDATE",
                "FAILED_CANDIDATE",
                "TIMEOUT_CANDIDATE",
                "CANCELLED_CANDIDATE",
            },
            attempt_count=attempt.attempt_number,
            candidate_only=True,
        )

        transition = ExecutionStateTransitionCandidateV1(
            execution_id=execution_id,
            from_state="REQUESTED",
            to_state=status,
            reason=status.lower(),
            provenance_refs=(f"prov:{scenario_id}:transition",),
        )

        partial = None
        if request.force_partial:
            partial = PartialExecutionResultCandidateV1(
                execution_id=execution_id,
                attempt_number=attempt.attempt_number,
                completed_substeps=("substep:1",),
                remaining_substeps=("substep:2",),
                confidence=0.5,
                trace_ref=f"trace:{scenario_id}",
                candidate_only=True,
            )

        failure = None
        if status in {"FAILED_CANDIDATE", "TIMEOUT_CANDIDATE"}:
            failure = ExecutionFailureCandidateV1(
                failure_id=f"failure:{scenario_id}",
                execution_id=execution_id,
                failure_class="timeout"
                if status == "TIMEOUT_CANDIDATE"
                else "adapter_or_runtime_failure",
                failure_stage="queue" if status == "TIMEOUT_CANDIDATE" else "execution",
                cause_candidate_refs=(f"cause:{scenario_id}",),
                trace_ref=f"trace:{scenario_id}",
                retry_authority_granted=request.retry_authorized,
                candidate_only=True,
            )

        rollback = RollbackContextCandidateV1(
            rollback_required=request.rollback_required,
            rollback_reason="partial_failure_requires_rollback"
            if request.rollback_required
            else None,
            rollback_policy_ref="rollback-policy:reference-only",
            rollback_trigger_ref=failure.failure_id
            if request.rollback_required and failure
            else None,
            rollback_execution_claimed=False,
            candidate_only=True,
        )

        scheduler_ref = SchedulerReferenceCandidateV1(
            scheduler_ref=request.request.scheduler_refs[0].ref_id,
            delay_reason="synthetic_queue_delay" if request.scheduler_delay else None,
            semantic_mutation=False,
            candidate_only=True,
        )

        task_ref = TaskReferenceCandidateV1(
            task_ref=request.request.task_refs[0].ref_id,
            dependency_ref=request.previous_attempt_ref,
            cancellation_ref="cancel:requested" if request.cancel_requested else None,
            task_mutation=False,
            candidate_only=True,
        )

        adapter_ok = status not in {"FAILED_CANDIDATE"}
        if request.force_failure:
            adapter_ok = False

        adapter_ref = AdapterReferenceCandidateV1(
            adapter_ref=request.request.adapter_refs[0].ref_id,
            capability_match=adapter_ok,
            mismatch_reason=None if adapter_ok else "adapter_failure_surface",
            real_adapter_call_executed=False,
            real_device_call_executed=False,
            real_provider_call_executed=False,
            candidate_only=True,
        )

        result = ExecutionResultCandidateV1(
            execution_id=execution_id,
            request_id=request.request.execution_request_id,
            status=status,
            attempt_count=attempt.attempt_number,
            started_at="2026-01-01T00:00:00Z",
            ended_at="2026-01-01T00:00:01Z",
            trace_ref=f"trace:{scenario_id}",
            failure_ref=failure.failure_id if failure else None,
            partial_result_ref=f"partial:{scenario_id}" if partial else None,
            candidate_only=True,
            planning_only=True,
        )

        diagnostics = DiagnosticsHandoffCandidateV1(
            diagnostics_ref=f"diagnostics:{scenario_id}",
            health_state_candidate="degraded"
            if status in {"FAILED_CANDIDATE", "TIMEOUT_CANDIDATE"}
            else "healthy",
            error_code_candidate=(failure.failure_class if failure else None),
            latency_candidate_ms=1300 if request.scheduler_delay else 150,
            failure_rate_candidate=1.0 if failure else 0.0,
            evidence_only=True,
            candidate_only=True,
        )

        trace = ExecutionTraceCandidateV1(
            trace_id=f"trace:{scenario_id}",
            execution_request_ref=request.request.execution_request_id,
            action_candidate_ref=request.request.action_candidate_ref.ref_id,
            readiness_ref=request.request.execution_readiness_ref.ref_id,
            admission_ref=f"admission:{scenario_id}",
            attempt_refs=(attempt.attempt_id,),
            result_ref=result.execution_id,
            failure_refs=(failure.failure_id,) if failure else (),
            timeout_refs=(f"timeout:{scenario_id}",) if request.force_timeout else (),
            cancellation_refs=(f"cancel:{scenario_id}",)
            if request.cancel_requested
            else (),
            rollback_refs=(rollback.rollback_trigger_ref,)
            if rollback.rollback_trigger_ref
            else (),
            adapter_event_refs=(adapter_ref.adapter_ref,),
            scheduler_refs=tuple(ref.ref_id for ref in request.request.scheduler_refs),
            task_refs=tuple(ref.ref_id for ref in request.request.task_refs),
            diagnostics_refs=(diagnostics.diagnostics_ref,),
            provenance=(
                f"prov:{scenario_id}:request",
                f"prov:{scenario_id}:admission",
                f"prov:{scenario_id}:final-gate",
                f"prov:{scenario_id}:attempt",
                f"prov:{scenario_id}:result",
            ),
            candidate_only=True,
        )

        action_handoff = self._make_handoff(
            scenario_id,
            ACTION_GOVERNANCE_OWNER,
            result.execution_id,
            failure.failure_id if failure else None,
            result.partial_result_ref,
        )
        task_handoff = self._make_handoff(
            scenario_id,
            TASK_MANAGER_OWNER,
            result.execution_id,
            failure.failure_id if failure else None,
            result.partial_result_ref,
        )
        diagnostics_handoff = self._make_handoff(
            scenario_id,
            DIAGNOSTICS_OWNER,
            result.execution_id,
            failure.failure_id if failure else None,
            result.partial_result_ref,
        )

        if admitted and final_gate.passed and not idempotency_duplicate:
            self._idempotency.put(
                IdempotencyRecordV1(
                    idempotency_key=request.request.idempotency_key,
                    scope_key=request.request.scope_key,
                    execution_id=execution_id,
                    status=status,
                    result_ref=result.execution_id,
                )
            )

        return RuntimeExecutorOutputV1(
            scenario_id=scenario_id,
            execution_id=execution_id,
            admission=admission,
            final_gate=final_gate,
            state=state,
            transition=transition,
            attempt=attempt,
            retry=retry,
            timeout=timeout,
            cancellation=cancellation,
            partial_result=partial,
            failure=failure,
            rollback=rollback,
            scheduler_ref=scheduler_ref,
            task_ref=task_ref,
            adapter_ref=adapter_ref,
            result=result,
            diagnostics_handoff=diagnostics,
            trace=trace,
            action_handoff=action_handoff,
            task_handoff=task_handoff,
            diagnostics_result_handoff=diagnostics_handoff,
            idempotency_duplicate=idempotency_duplicate,
            idempotency_scope_mismatch=idempotency_scope_mismatch,
            duplicate_attempt_created=duplicate_attempt_created,
            candidate_only=True,
            runtime_executed=False,
            device_control_executed=False,
            provider_call_executed=False,
            adapter_call_executed=False,
            scheduler_runtime_executed=False,
            task_mutation_executed=False,
            database_write_executed=False,
        )
