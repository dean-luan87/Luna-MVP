from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple


def build_interruption_state_v1(
    *,
    interruption_policy: Mapping[str, Any],
    requested_control: str,
    interruption_reason: str,
    current_status: str,
) -> Dict[str, Any]:
    resumable = current_status in {"paused", "resuming", "running_candidate", "ready"}
    checkpoint = f"checkpoint_{current_status}"
    required_revalidation = bool(interruption_policy.get("required_revalidation", True))
    displaced_task_ref = str(interruption_policy.get("displaced_task_ref", ""))
    interrupted_stage = current_status if interruption_reason else ""
    return {
        "interruption_reason": interruption_reason,
        "interrupted_stage": interrupted_stage,
        "resumable": resumable,
        "resume_checkpoint": checkpoint if resumable else "",
        "required_revalidation": required_revalidation,
        "displaced_task_ref": displaced_task_ref,
        "requested_control": requested_control,
    }


def build_recovery_candidates_v1(
    *,
    failure_type: str,
    recovery_policy: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    base = {
        "invalid_input": ("human_review_required", "terminate_candidate"),
        "dependency_unavailable": ("wait_candidate", "replan_candidate"),
        "capability_unavailable": ("fallback_candidate", "replan_candidate"),
        "permission_denied": ("human_review_required", "terminate_candidate"),
        "timeout": ("retry_candidate", "replan_candidate"),
        "execution_candidate_rejected": ("replan_candidate", "fallback_candidate"),
        "partial_failure": (
            "retry_candidate",
            "replan_candidate",
            "human_review_required",
        ),
        "unrecoverable_failure": ("terminate_candidate",),
        "cancellation": ("terminate_candidate",),
        "termination": ("terminate_candidate",),
        "": ("wait_candidate",),
    }
    strategy = tuple(str(x) for x in recovery_policy.get("preferred_recovery", ()))
    options = strategy or base.get(failure_type, base[""])
    return tuple(
        {
            "candidate": option,
            "reason": failure_type or "none",
        }
        for option in options
    )
