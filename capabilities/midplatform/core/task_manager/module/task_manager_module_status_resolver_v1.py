from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple


_INVALID_INPUT_REASONS = {
    "missing_task_request_id",
    "unsupported_task_type",
    "invalid_priority",
    "missing_permission_snapshot",
    "direct_action_execution_forbidden",
    "direct_model_call_forbidden",
    "direct_field_state_write_forbidden",
    "bypass_capability_module_api_forbidden",
}

_STATUS_PRIORITY: Tuple[str, ...] = (
    "invalid_input",
    "internal_error",
    "terminated",
    "cancelled",
    "failed",
    "partially_completed",
    "completed",
    "paused",
    "waiting_dependency",
    "blocked",
    "ready",
    "planned",
    "admitted",
    "received",
)


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _uniq(items: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(x) for x in items if str(x)))


def resolve_task_manager_module_status(
    *,
    lifecycle_status: str,
    task_status: str,
    dependency_status: Mapping[str, Any],
    result_completion_status: str,
    interruption_status: Mapping[str, Any],
    recovery_status: Mapping[str, Any],
    blocking_reasons: Sequence[str],
    failed_subtasks: int,
    unresolved_subtasks: int,
    cancelled_reason: str,
    termination_reason: str,
    requested_control: str,
) -> Dict[str, Any]:
    lifecycle = _norm(lifecycle_status)
    task = _norm(task_status)
    completion = _norm(result_completion_status)
    control = _norm(requested_control)
    cancellation = _norm(cancelled_reason)
    termination = _norm(termination_reason)

    historical_blocking = _uniq(blocking_reasons)
    dependency_waiting = bool(dependency_status.get("dependency_waiting", False))

    is_invalid_input = any(x in _INVALID_INPUT_REASONS for x in historical_blocking)
    has_internal_error = bool(interruption_status.get("internal_error", False))

    explicit_terminated = (
        termination
        or control == "terminate"
        or task == "terminated"
        or lifecycle == "terminated"
        or completion == "terminated"
    )
    explicit_cancelled = (
        cancellation
        or control == "cancel"
        or task == "cancelled"
        or lifecycle == "cancelled"
        or completion == "cancelled"
    )
    explicit_failed = (
        task == "failed"
        or lifecycle == "failed"
        or completion == "failed"
        or failed_subtasks > 0
    )
    explicit_partial = (
        completion == "partially_completed"
        or task == "partially_completed"
        or lifecycle == "partially_completed"
    )
    explicit_completed = (
        completion == "completed" or task == "completed" or lifecycle == "completed"
    )

    status = "received"
    for candidate in _STATUS_PRIORITY:
        if candidate == "invalid_input" and is_invalid_input:
            status = "blocked"
            break
        if candidate == "internal_error" and has_internal_error:
            status = "failed"
            break
        if candidate == "terminated" and explicit_terminated:
            status = "terminated"
            break
        if candidate == "cancelled" and explicit_cancelled:
            status = "cancelled"
            break
        if (
            candidate == "failed"
            and explicit_failed
            and not explicit_partial
            and not explicit_completed
        ):
            status = "failed"
            break
        if candidate == "partially_completed" and explicit_partial:
            status = "partially_completed"
            break
        if (
            candidate == "completed"
            and explicit_completed
            and not explicit_failed
            and not explicit_partial
        ):
            status = "completed"
            break
        if candidate == "paused" and (task == "paused" or lifecycle == "paused"):
            status = "paused"
            break
        if candidate == "waiting_dependency" and dependency_waiting:
            status = "waiting_dependency"
            break
        if candidate == "blocked":
            if historical_blocking and status not in {
                "terminated",
                "cancelled",
                "failed",
                "partially_completed",
                "completed",
                "paused",
                "waiting_dependency",
            }:
                status = "blocked"
                break
        if candidate in {"ready", "planned", "admitted", "received"}:
            if task == candidate or lifecycle == candidate:
                status = candidate
                break

    current_blocking = (
        historical_blocking if status in {"blocked", "waiting_dependency"} else tuple()
    )
    if status in {
        "cancelled",
        "terminated",
        "completed",
        "partially_completed",
        "failed",
    }:
        current_blocking = tuple()

    return {
        "module_status": status,
        "current_blocking_reasons": current_blocking,
        "historical_blocking_reasons": historical_blocking,
        "failed_subtasks": int(failed_subtasks),
        "unresolved_subtasks": int(unresolved_subtasks),
        "dependency_waiting": dependency_waiting,
        "resolution_basis": {
            "lifecycle_status": lifecycle,
            "task_status": task,
            "completion_status": completion,
            "requested_control": control,
            "termination_reason": termination,
            "cancelled_reason": cancellation,
            "has_internal_error": has_internal_error,
            "recovery_status": dict(recovery_status),
        },
    }
