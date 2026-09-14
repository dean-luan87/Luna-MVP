"""I/O contracts for Runtime Executor controlled implementation."""

from __future__ import annotations

from dataclasses import dataclass

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
from capabilities.midplatform.core.runtime_executor.execution_request_types_v1 import (
    ExecutionRequestCandidateV1,
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
from capabilities.midplatform.core.runtime_executor.execution_partial_result_types_v1 import (
    PartialExecutionResultCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.execution_trace_types_v1 import (
    ExecutionTraceCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_handoff_types_v1 import (
    ResultHandoffCandidateV1,
)


@dataclass(frozen=True)
class RuntimeExecutorInputV1:
    scenario_id: str
    request: ExecutionRequestCandidateV1
    readiness_fresh: bool
    permission_valid: bool
    safety_valid: bool
    confirmation_valid: bool
    final_scope_valid: bool
    final_time_window_valid: bool
    scheduler_delay: bool
    start_requested: bool
    force_failure: bool
    force_timeout: bool
    cancel_requested: bool
    force_partial: bool
    rollback_required: bool
    retry_requested: bool
    retry_authorized: bool
    retry_authorized_by: str | None
    previous_attempt_ref: str | None


@dataclass(frozen=True)
class RuntimeExecutorOutputV1:
    scenario_id: str
    execution_id: str
    admission: AdmissionResultCandidateV1
    final_gate: ExecutionFinalGateResultV1
    state: ExecutionStateSnapshotV1
    transition: ExecutionStateTransitionCandidateV1
    attempt: ExecutionAttemptCandidateV1
    retry: RetryRequestCandidateV1
    timeout: TimeoutCandidateV1
    cancellation: CancellationCandidateV1
    partial_result: PartialExecutionResultCandidateV1 | None
    failure: ExecutionFailureCandidateV1 | None
    rollback: RollbackContextCandidateV1
    scheduler_ref: SchedulerReferenceCandidateV1
    task_ref: TaskReferenceCandidateV1
    adapter_ref: AdapterReferenceCandidateV1
    result: ExecutionResultCandidateV1
    diagnostics_handoff: DiagnosticsHandoffCandidateV1
    trace: ExecutionTraceCandidateV1
    action_handoff: ResultHandoffCandidateV1
    task_handoff: ResultHandoffCandidateV1
    diagnostics_result_handoff: ResultHandoffCandidateV1
    idempotency_duplicate: bool
    idempotency_scope_mismatch: bool
    duplicate_attempt_created: bool
    candidate_only: bool
    runtime_executed: bool
    device_control_executed: bool
    provider_call_executed: bool
    adapter_call_executed: bool
    scheduler_runtime_executed: bool
    task_mutation_executed: bool
    database_write_executed: bool
