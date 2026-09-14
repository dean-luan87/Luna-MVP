"""Static registries for Action Governance controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple


ACTION_OWNER = "Action Governance"
LEGACY_ALIASES: Tuple[str, ...] = (
    "Action Boundary",
    "Action Control",
    "Action Commitment",
    "Action Execution Governance",
    "Action Boundary Governance",
)
RUNTIME_EXECUTOR_OWNER = "Runtime Executor"
TASK_MANAGER_OWNER = "Task Manager"

ACTION_STATE_SET = {
    "PROPOSED",
    "ELIGIBLE",
    "PRECONDITION_PENDING",
    "CONSTRAINED",
    "NEEDS_PERMISSION",
    "NEEDS_CONFIRMATION",
    "READY_CANDIDATE",
    "SUSPENDED",
    "BLOCKED",
    "CANCELLED",
    "ROLLBACK_REQUIRED",
    "FAILED_CANDIDATE",
    "REVISED",
    "REVOKED",
}

NEGATIVE_GUARD_FLAGS: Dict[str, bool] = {
    "decision_not_action": True,
    "selected_decision_not_action_execution": True,
    "action_candidate_not_runtime_command": True,
    "eligible_not_executed": True,
    "ready_not_executed": True,
    "authorized_not_executed": True,
    "action_governance_not_executor": True,
    "action_governance_not_task_manager": True,
    "permission_context_not_permanent_authorization": True,
    "safety_context_not_permanent_authorization": True,
    "confirmation_cannot_be_fabricated": True,
    "stale_confirmation_cannot_be_reused": True,
    "unknown_precondition_not_satisfied": True,
    "rollback_candidate_not_execution": True,
    "failure_result_not_retry_authority": True,
    "no_runtime_side_effect": True,
    "no_database_write": True,
    "no_device_control": True,
    "no_task_creation": True,
    "no_scheduler_execution": True,
    "no_permission_bypass": True,
    "no_safety_bypass": True,
}
