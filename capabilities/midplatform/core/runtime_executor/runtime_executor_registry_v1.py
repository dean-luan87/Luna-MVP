"""Static registry and policy metadata for Runtime Executor controlled implementation."""

from __future__ import annotations

from typing import Dict, Tuple


RUNTIME_EXECUTOR_OWNER = "Runtime Executor"
LEGACY_ALIASES: Tuple[str, ...] = (
    "Action Runtime Governance",
    "Action Executor",
)

ACTION_GOVERNANCE_OWNER = "Action Governance"
DECISION_GOVERNANCE_OWNER = "Decision Governance"
TASK_MANAGER_OWNER = "Task Manager"
SCHEDULER_OWNER = "Scheduler"
DIAGNOSTICS_OWNER = "Diagnostics"

EXECUTION_STATES = {
    "REQUESTED",
    "ADMISSION_PENDING",
    "ADMITTED_CANDIDATE",
    "REJECTED_CANDIDATE",
    "QUEUED_CANDIDATE",
    "RUNNING_CANDIDATE",
    "SUCCEEDED_CANDIDATE",
    "FAILED_CANDIDATE",
    "TIMEOUT_CANDIDATE",
    "CANCELLED_CANDIDATE",
    "PARTIAL_RESULT_CANDIDATE",
    "ROLLBACK_REQUIRED_CANDIDATE",
}

TERMINAL_STATES = {
    "SUCCEEDED_CANDIDATE",
    "FAILED_CANDIDATE",
    "TIMEOUT_CANDIDATE",
    "CANCELLED_CANDIDATE",
}

NEGATIVE_GUARD_FLAGS: Dict[str, bool] = {
    "action_candidate_not_execution_request": True,
    "execution_readiness_not_execution": True,
    "executor_not_decision_governance": True,
    "executor_not_action_governance": True,
    "executor_not_task_manager": True,
    "executor_not_scheduler": True,
    "permission_bypass_forbidden": True,
    "safety_bypass_forbidden": True,
    "final_gate_skip_forbidden": True,
    "silent_retry_forbidden": True,
    "real_adapter_call_forbidden": True,
    "real_device_call_forbidden": True,
    "real_provider_call_forbidden": True,
    "db_write_forbidden": True,
    "scheduler_runtime_forbidden": True,
    "task_mutation_forbidden": True,
}
