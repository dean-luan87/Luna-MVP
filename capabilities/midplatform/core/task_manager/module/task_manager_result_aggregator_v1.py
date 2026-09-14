from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple


def aggregate_task_result_v1(
    *,
    task_id: str,
    task_status: str,
    subtasks: Sequence[Mapping[str, Any]],
    execution_request_candidates: Sequence[Mapping[str, Any]],
    dependency_status: Mapping[str, Any],
    interruption_state: Mapping[str, Any],
    recovery_candidates: Sequence[Mapping[str, Any]],
    current_blocking_reasons: Iterable[str],
    historical_blocking_reasons: Iterable[str],
    status_resolution: Mapping[str, Any],
) -> Dict[str, Any]:
    total = max(len(subtasks), 1)
    done = sum(1 for s in subtasks if str(s.get("status", "")) == "completed")
    failed = sum(1 for s in subtasks if str(s.get("status", "")) == "failed")

    unresolved: Tuple[str, ...] = tuple(str(x) for x in current_blocking_reasons)
    unresolved += tuple(
        str(x) for x in dependency_status.get("waiting_dependency_refs", ())
    )
    unresolved = tuple(dict.fromkeys(unresolved))

    failed_subtask_refs = tuple(
        str(s.get("subtask_id", ""))
        for s in subtasks
        if str(s.get("status", "")) == "failed"
    )
    unresolved_subtask_refs = tuple(
        str(s.get("subtask_id", ""))
        for s in subtasks
        if str(s.get("status", "")) not in {"completed", "cancelled", "terminated"}
    )

    return {
        "task_id": task_id,
        "task_status": task_status,
        "task_plan": {
            "task_id": task_id,
            "planned_subtask_count": len(subtasks),
        },
        "subtasks": tuple(dict(s) for s in subtasks),
        "execution_request_candidates": tuple(
            dict(c) for c in execution_request_candidates
        ),
        "dependency_status": dict(dependency_status),
        "progress": {
            "completed_subtasks": done,
            "failed_subtasks": failed,
            "total_subtasks": len(subtasks),
            "completion_ratio": done / total,
        },
        "interruption_state": dict(interruption_state),
        "recovery_candidates": tuple(dict(c) for c in recovery_candidates),
        "result_summary": {
            "task_status": task_status,
            "has_unresolved_items": len(unresolved) > 0,
            "execution_candidate_count": len(execution_request_candidates),
            "current_blocking_reasons": tuple(str(x) for x in current_blocking_reasons),
            "historical_blocking_reasons": tuple(
                str(x) for x in historical_blocking_reasons
            ),
            "failed_subtask_refs": failed_subtask_refs,
            "unresolved_subtask_refs": unresolved_subtask_refs,
        },
        "unresolved_items": unresolved,
        "failed_subtask_refs": failed_subtask_refs,
        "unresolved_subtask_refs": unresolved_subtask_refs,
        "status_resolution": dict(status_resolution),
    }
