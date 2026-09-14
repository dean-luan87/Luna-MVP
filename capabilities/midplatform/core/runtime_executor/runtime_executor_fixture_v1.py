"""Synthetic fixtures for Runtime Executor controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.runtime_executor.execution_request_types_v1 import (
    ExecutionRequestCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_io_types_v1 import (
    RuntimeExecutorInputV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_registry_v1 import (
    RUNTIME_EXECUTOR_OWNER,
)


@dataclass(frozen=True)
class RuntimeExecutorFixtureCaseV1:
    case_id: str
    description: str
    request: RuntimeExecutorInputV1
    expected_status: str
    expected_state: str
    expected_admitted: bool
    expected_retry_blocked: bool
    expected_idempotency_duplicate: bool
    expected_idempotency_scope_mismatch: bool
    expected_partial_present: bool
    expected_failure_present: bool
    expected_rollback_required: bool
    expected_negative_guards: Tuple[str, ...]
    synthetic_only: bool = True


def _ref(owner: str, ref_id: str, ref_type: str = "REFERENCE") -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _request(
    case_id: str, idempotency_key: str, scope_key: str
) -> ExecutionRequestCandidateV1:
    return ExecutionRequestCandidateV1(
        execution_request_id=f"execution-request:{case_id}",
        action_candidate_ref=_ref(
            "Action Governance", f"action:{case_id}", "ACTION_CANDIDATE"
        ),
        execution_readiness_ref=_ref(
            "Action Governance", f"readiness:{case_id}", "EXECUTION_READINESS"
        ),
        permission_recheck_ref=_ref(
            "Permission Governance", f"permission:{case_id}", "PERMISSION_RECHECK"
        ),
        safety_recheck_ref=_ref(
            "Safety Governance", f"safety:{case_id}", "SAFETY_RECHECK"
        ),
        confirmation_ref=_ref(
            "Human Oversight", f"confirmation:{case_id}", "CONFIRMATION"
        ),
        resource_constraint_ref=_ref(
            "Resource Governance", f"resource:{case_id}", "RESOURCE_CONSTRAINT"
        ),
        reversibility="reversible",
        request_time="2026-01-01T00:00:00Z",
        idempotency_key=idempotency_key,
        scope_key=scope_key,
        provenance_ref=_ref(
            RUNTIME_EXECUTOR_OWNER, f"prov:{case_id}:request", "PROVENANCE"
        ),
        scheduler_refs=(
            _ref("Scheduler", f"scheduler:{case_id}", "SCHEDULER_REFERENCE"),
        ),
        task_refs=(_ref("Task Manager", f"task:{case_id}", "TASK_REFERENCE"),),
        adapter_refs=(
            _ref("Execution Adapter", f"adapter:{case_id}", "ADAPTER_REFERENCE"),
        ),
        candidate_only=True,
        planning_only=True,
    )


def _mk(
    case_id: str,
    description: str,
    expected_status: str,
    expected_state: str,
    expected_admitted: bool,
    expected_retry_blocked: bool,
    expected_idempotency_duplicate: bool,
    expected_idempotency_scope_mismatch: bool,
    expected_partial_present: bool,
    expected_failure_present: bool,
    expected_rollback_required: bool,
    expected_negative_guards: Tuple[str, ...],
    *,
    idempotency_key: str,
    scope_key: str,
    readiness_fresh: bool = True,
    permission_valid: bool = True,
    safety_valid: bool = True,
    confirmation_valid: bool = True,
    final_scope_valid: bool = True,
    final_time_window_valid: bool = True,
    scheduler_delay: bool = False,
    start_requested: bool = True,
    force_failure: bool = False,
    force_timeout: bool = False,
    cancel_requested: bool = False,
    force_partial: bool = False,
    rollback_required: bool = False,
    retry_requested: bool = False,
    retry_authorized: bool = False,
    retry_authorized_by: str | None = None,
    previous_attempt_ref: str | None = None,
) -> RuntimeExecutorFixtureCaseV1:
    return RuntimeExecutorFixtureCaseV1(
        case_id=case_id,
        description=description,
        request=RuntimeExecutorInputV1(
            scenario_id=case_id,
            request=_request(
                case_id, idempotency_key=idempotency_key, scope_key=scope_key
            ),
            readiness_fresh=readiness_fresh,
            permission_valid=permission_valid,
            safety_valid=safety_valid,
            confirmation_valid=confirmation_valid,
            final_scope_valid=final_scope_valid,
            final_time_window_valid=final_time_window_valid,
            scheduler_delay=scheduler_delay,
            start_requested=start_requested,
            force_failure=force_failure,
            force_timeout=force_timeout,
            cancel_requested=cancel_requested,
            force_partial=force_partial,
            rollback_required=rollback_required,
            retry_requested=retry_requested,
            retry_authorized=retry_authorized,
            retry_authorized_by=retry_authorized_by,
            previous_attempt_ref=previous_attempt_ref,
        ),
        expected_status=expected_status,
        expected_state=expected_state,
        expected_admitted=expected_admitted,
        expected_retry_blocked=expected_retry_blocked,
        expected_idempotency_duplicate=expected_idempotency_duplicate,
        expected_idempotency_scope_mismatch=expected_idempotency_scope_mismatch,
        expected_partial_present=expected_partial_present,
        expected_failure_present=expected_failure_present,
        expected_rollback_required=expected_rollback_required,
        expected_negative_guards=expected_negative_guards,
        synthetic_only=True,
    )


def get_runtime_executor_synthetic_fixtures_v1() -> Tuple[
    RuntimeExecutorFixtureCaseV1, ...
]:
    return (
        _mk(
            "R01",
            "admission happy path candidate-only",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("candidate_only",),
            idempotency_key="idem-key-001",
            scope_key="scope-alpha",
        ),
        _mk(
            "R02",
            "permission revoked before final gate",
            expected_status="REJECTED_CANDIDATE",
            expected_state="REJECTED_CANDIDATE",
            expected_admitted=False,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("no_permission_bypass",),
            idempotency_key="idem-key-002",
            scope_key="scope-alpha",
            permission_valid=False,
        ),
        _mk(
            "R03",
            "safety veto before final gate",
            expected_status="REJECTED_CANDIDATE",
            expected_state="REJECTED_CANDIDATE",
            expected_admitted=False,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("no_safety_bypass",),
            idempotency_key="idem-key-003",
            scope_key="scope-alpha",
            safety_valid=False,
        ),
        _mk(
            "R04",
            "confirmation scope mismatch",
            expected_status="REJECTED_CANDIDATE",
            expected_state="REJECTED_CANDIDATE",
            expected_admitted=False,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("final_gate_required",),
            idempotency_key="idem-key-004",
            scope_key="scope-alpha",
            final_scope_valid=False,
        ),
        _mk(
            "R05",
            "resource degraded but admitted candidate",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("resource_reference_only",),
            idempotency_key="idem-key-005",
            scope_key="scope-alpha",
        ),
        _mk(
            "R06",
            "idempotency same key same scope reuses candidate result",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=True,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("no_second_attempt_on_duplicate",),
            idempotency_key="idem-key-001",
            scope_key="scope-alpha",
        ),
        _mk(
            "R07",
            "idempotency same key different scope is rejected",
            expected_status="REJECTED_CANDIDATE",
            expected_state="REJECTED_CANDIDATE",
            expected_admitted=False,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=True,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("idempotency_scope_mismatch",),
            idempotency_key="idem-key-001",
            scope_key="scope-beta",
        ),
        _mk(
            "R08",
            "retry requires explicit authority",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("retry_authority_required",),
            idempotency_key="idem-key-008",
            scope_key="scope-alpha",
            retry_requested=True,
            retry_authorized=True,
            retry_authorized_by="Runtime Executor",
            previous_attempt_ref="attempt:R08:0",
        ),
        _mk(
            "R09",
            "automatic retry is forbidden",
            expected_status="FAILED_CANDIDATE",
            expected_state="FAILED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=True,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=True,
            expected_rollback_required=False,
            expected_negative_guards=("automatic_retry_forbidden",),
            idempotency_key="idem-key-009",
            scope_key="scope-alpha",
            retry_requested=True,
            retry_authorized=False,
            force_failure=True,
            previous_attempt_ref="attempt:R09:0",
        ),
        _mk(
            "R10",
            "queue timeout to timeout candidate",
            expected_status="TIMEOUT_CANDIDATE",
            expected_state="TIMEOUT_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=True,
            expected_rollback_required=False,
            expected_negative_guards=("timeout_trace_required",),
            idempotency_key="idem-key-010",
            scope_key="scope-alpha",
            force_timeout=True,
            scheduler_delay=True,
        ),
        _mk(
            "R11",
            "running cancelled by user",
            expected_status="CANCELLED_CANDIDATE",
            expected_state="CANCELLED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("cancellation_trace_required",),
            idempotency_key="idem-key-011",
            scope_key="scope-alpha",
            cancel_requested=True,
        ),
        _mk(
            "R12",
            "partial result requires follow-up",
            expected_status="PARTIAL_RESULT_CANDIDATE",
            expected_state="PARTIAL_RESULT_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=True,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("partial_not_success",),
            idempotency_key="idem-key-012",
            scope_key="scope-alpha",
            force_partial=True,
        ),
        _mk(
            "R13",
            "partial failure triggers rollback required",
            expected_status="FAILED_CANDIDATE",
            expected_state="FAILED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=True,
            expected_failure_present=True,
            expected_rollback_required=True,
            expected_negative_guards=("rollback_requires_trigger",),
            idempotency_key="idem-key-013",
            scope_key="scope-alpha",
            force_partial=True,
            force_failure=True,
            rollback_required=True,
        ),
        _mk(
            "R14",
            "adapter failure surface",
            expected_status="FAILED_CANDIDATE",
            expected_state="FAILED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=True,
            expected_rollback_required=False,
            expected_negative_guards=("adapter_side_effect_forbidden",),
            idempotency_key="idem-key-014",
            scope_key="scope-alpha",
            force_failure=True,
        ),
        _mk(
            "R15",
            "scheduler is reference-only",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("scheduler_reference_only",),
            idempotency_key="idem-key-015",
            scope_key="scope-alpha",
            scheduler_delay=True,
        ),
        _mk(
            "R16",
            "task manager is reference-only",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("task_reference_only",),
            idempotency_key="idem-key-016",
            scope_key="scope-alpha",
        ),
        _mk(
            "R17",
            "result handoff no owner transfer",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("result_handoff_reference_only",),
            idempotency_key="idem-key-017",
            scope_key="scope-alpha",
        ),
        _mk(
            "R18",
            "diagnostics evidence only",
            expected_status="SUCCEEDED_CANDIDATE",
            expected_state="SUCCEEDED_CANDIDATE",
            expected_admitted=True,
            expected_retry_blocked=False,
            expected_idempotency_duplicate=False,
            expected_idempotency_scope_mismatch=False,
            expected_partial_present=False,
            expected_failure_present=False,
            expected_rollback_required=False,
            expected_negative_guards=("diagnostics_no_decision_authority",),
            idempotency_key="idem-key-018",
            scope_key="scope-alpha",
        ),
    )
