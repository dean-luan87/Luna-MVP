from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Set

_ALLOWED_TRANSITIONS = {
    "received": {"admitted", "blocked", "failed", "cancelled", "terminated"},
    "admitted": {"planned", "blocked", "failed", "cancelled", "terminated"},
    "planned": {
        "ready",
        "waiting_dependency",
        "blocked",
        "failed",
        "cancelled",
        "terminated",
    },
    "waiting_dependency": {"ready", "blocked", "cancelled", "terminated"},
    "ready": {"running_candidate", "paused", "blocked", "cancelled", "terminated"},
    "running_candidate": {
        "paused",
        "completed",
        "partially_completed",
        "failed",
        "cancelled",
        "terminated",
        "blocked",
    },
    "paused": {"resuming", "cancelled", "terminated", "blocked"},
    "resuming": {"running_candidate", "failed", "cancelled", "terminated", "blocked"},
    "partially_completed": {
        "running_candidate",
        "failed",
        "cancelled",
        "terminated",
        "blocked",
    },
    "failed": {"planned", "terminated", "blocked"},
    "blocked": {"planned", "terminated"},
    "completed": set(),
    "cancelled": set(),
    "terminated": set(),
}

_TERMINAL = {"completed", "cancelled", "terminated"}


def _set(items: Iterable[str]) -> Set[str]:
    return {str(x) for x in items}


def next_status_v1(
    *,
    current_status: str,
    dependency_unresolved: bool,
    interruption_reason: str,
    recovery_decision: str,
    completion_status: str,
    requested_control: str,
    has_blocking_reason: bool,
) -> Dict[str, Any]:
    reasons = []
    nxt = current_status

    if current_status in _TERMINAL:
        return {
            "task_status": current_status,
            "transition_allowed": False,
            "transition_reason": "terminal_state_no_transition",
            "blocking_reasons": tuple(),
            "invariant_violations": tuple(),
        }

    if current_status == "waiting_dependency" and not dependency_unresolved:
        nxt = "ready"
        reasons.append("dependency_resolved")
    elif dependency_unresolved and current_status in _set(("planned", "ready")):
        nxt = "waiting_dependency"
        reasons.append("dependency_unresolved")

    if requested_control == "pause" and current_status in _set(
        ("ready", "running_candidate")
    ):
        nxt = "paused"
        reasons.append("pause_requested")
    elif requested_control == "resume" and current_status == "paused":
        nxt = "resuming"
        reasons.append("resume_requested")
    elif requested_control == "cancel":
        nxt = "cancelled"
        reasons.append("cancel_requested")
    elif requested_control == "terminate":
        nxt = "terminated"
        reasons.append("terminate_requested")

    if interruption_reason and nxt in _set(("ready", "running_candidate")):
        nxt = "paused"
        reasons.append(f"interruption:{interruption_reason}")

    if completion_status in _set(("completed", "partially_completed")):
        nxt = completion_status
        reasons.append(f"completion:{completion_status}")

    if completion_status == "failed":
        nxt = "failed"
        reasons.append("completion:failed")

    if current_status == "failed" and recovery_decision:
        if recovery_decision in _set(
            ("retry_candidate", "replan_candidate", "wait_candidate")
        ):
            nxt = "planned"
            reasons.append(f"recovery:{recovery_decision}")
        elif recovery_decision == "terminate_candidate":
            nxt = "terminated"
            reasons.append("recovery:terminate")

    if has_blocking_reason and nxt not in _TERMINAL:
        nxt = "blocked"
        reasons.append("blocking_reason_present")

    allowed = (
        nxt in _ALLOWED_TRANSITIONS.get(current_status, set()) or nxt == current_status
    )
    violations = []
    if current_status == "completed" and nxt == "running_candidate":
        violations.append("completed_to_running_forbidden")
    if current_status == "cancelled" and nxt not in _set(("cancelled",)):
        violations.append("cancelled_autorecover_forbidden")
    if current_status == "terminated" and nxt not in _set(("terminated",)):
        violations.append("terminated_autorecover_forbidden")
    if current_status == "failed" and nxt == "planned" and not recovery_decision:
        violations.append("failed_requires_recovery_decision")
    if current_status == "paused" and nxt == "running_candidate":
        violations.append("paused_requires_resuming_stage")

    if violations:
        allowed = False

    return {
        "task_status": nxt if allowed else current_status,
        "transition_allowed": allowed,
        "transition_reason": ",".join(reasons) if reasons else "no_change",
        "blocking_reasons": tuple(["task_blocked"] if has_blocking_reason else []),
        "invariant_violations": tuple(violations),
    }


def build_state_manager_snapshot_v1(
    *,
    task_id: str,
    task_status: str,
    subtasks: Iterable[Mapping[str, Any]],
    blocking_reasons: Iterable[str],
    waiting_dependencies: Iterable[str],
    recovery_point: str,
    failure_reason: str,
    cancel_reason: str,
    terminate_reason: str,
) -> Dict[str, Any]:
    rows = list(subtasks)
    total = max(len(rows), 1)
    completed = sum(1 for r in rows if str(r.get("status", "")) == "completed")
    progress_ratio = completed / total
    return {
        "task_id": task_id,
        "current_task_status": task_status,
        "subtask_statuses": {
            str(r.get("subtask_id", "")): str(r.get("status", "")) for r in rows
        },
        "completion_ratio": progress_ratio,
        "current_blocking_items": tuple(str(x) for x in blocking_reasons),
        "current_waiting_dependencies": tuple(str(x) for x in waiting_dependencies),
        "last_state_change": {
            "task_status": task_status,
        },
        "recovery_point": recovery_point,
        "failure_reason": failure_reason,
        "cancel_reason": cancel_reason,
        "terminate_reason": terminate_reason,
    }
