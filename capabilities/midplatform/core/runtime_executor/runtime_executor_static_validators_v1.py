"""Static and behavior validators for Runtime Executor outputs."""

from __future__ import annotations

from capabilities.midplatform.core.runtime_executor.runtime_executor_io_types_v1 import (
    RuntimeExecutorOutputV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_ownership_guard_v1 import (
    validate_result_handoff_reference_only,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_registry_v1 import (
    EXECUTION_STATES,
    NEGATIVE_GUARD_FLAGS,
)


def validate_state(output: RuntimeExecutorOutputV1) -> bool:
    return output.state.state in EXECUTION_STATES and output.state.attempt_count >= 1


def validate_final_gate(output: RuntimeExecutorOutputV1) -> bool:
    if output.final_gate.passed:
        return (
            output.final_gate.permission_valid
            and output.final_gate.safety_valid
            and output.final_gate.confirmation_valid
            and output.final_gate.scope_valid
            and output.final_gate.time_window_valid
        )
    return True


def validate_idempotency_behavior(output: RuntimeExecutorOutputV1) -> bool:
    if output.idempotency_scope_mismatch:
        return output.admission.admitted is False
    if output.idempotency_duplicate:
        return output.duplicate_attempt_created is False
    return True


def validate_retry_boundary(output: RuntimeExecutorOutputV1) -> bool:
    if output.retry.retry_requested and not output.retry.retry_authorized:
        return output.retry.blocked_reason == "retry_without_authority"
    return True


def validate_timeout_cancel(output: RuntimeExecutorOutputV1) -> bool:
    if output.timeout.timed_out:
        return output.result.status == "TIMEOUT_CANDIDATE"
    if output.cancellation.cancelled:
        return output.result.status == "CANCELLED_CANDIDATE"
    return True


def validate_partial_not_success(output: RuntimeExecutorOutputV1) -> bool:
    if output.partial_result is not None:
        return output.result.status != "SUCCEEDED_CANDIDATE"
    return True


def validate_result_handoffs(output: RuntimeExecutorOutputV1) -> bool:
    return (
        validate_result_handoff_reference_only(output.action_handoff)
        and validate_result_handoff_reference_only(output.task_handoff)
        and validate_result_handoff_reference_only(output.diagnostics_result_handoff)
    )


def validate_no_side_effects(output: RuntimeExecutorOutputV1) -> bool:
    return (
        output.candidate_only is True
        and output.runtime_executed is False
        and output.adapter_call_executed is False
        and output.provider_call_executed is False
        and output.device_control_executed is False
        and output.scheduler_runtime_executed is False
        and output.task_mutation_executed is False
        and output.database_write_executed is False
    )


def validate_trace(output: RuntimeExecutorOutputV1) -> bool:
    return (
        bool(output.trace.attempt_refs)
        and bool(output.trace.result_ref)
        and bool(output.trace.scheduler_refs)
        and bool(output.trace.task_refs)
        and bool(output.trace.diagnostics_refs)
        and bool(output.trace.provenance)
    )


def validate_negative_guards() -> bool:
    return all(NEGATIVE_GUARD_FLAGS.values())
