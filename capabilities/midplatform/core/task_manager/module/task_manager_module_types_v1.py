from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

TASK_MANAGER_LIFECYCLE_STATES_V1: Tuple[str, ...] = (
    "received",
    "admitted",
    "planned",
    "ready",
    "waiting_dependency",
    "running_candidate",
    "paused",
    "resuming",
    "completed",
    "partially_completed",
    "failed",
    "cancelled",
    "terminated",
    "blocked",
)

TASK_MANAGER_SUPPORTED_TYPES_V1: Tuple[str, ...] = (
    "atomic",
    "sequential",
    "parallel",
    "conditional",
    "verification",
    "recovery",
)


@dataclass(frozen=True)
class TaskManagerModuleRequestV1:
    task_request_id: str
    task_type: str
    task_goal: str
    requester_ref: str
    priority: str
    context_snapshot: Dict[str, Any]
    dependency_refs: Tuple[str, ...]
    resource_constraints: Dict[str, Any]
    permission_snapshot: Dict[str, Any]
    capability_requirements: Tuple[str, ...]
    deadline_or_timeout: str
    interruption_policy: Dict[str, Any]
    recovery_policy: Dict[str, Any]
    version_snapshots: Dict[str, str]


@dataclass(frozen=True)
class TaskManagerModuleResultV1:
    task_id: str
    task_status: str
    task_plan: Dict[str, Any]
    subtasks: Tuple[Dict[str, Any], ...]
    execution_request_candidates: Tuple[Dict[str, Any], ...]
    dependency_status: Dict[str, Any]
    progress: Dict[str, Any]
    interruption_state: Dict[str, Any]
    recovery_candidates: Tuple[Dict[str, Any], ...]
    result_summary: Dict[str, Any]
    unresolved_items: Tuple[str, ...]
    diagnostics: Dict[str, Any]
    trace_ref: str
    replay_key: str
    version_snapshots: Dict[str, str]
    action_execution_executed: bool
    model_call_executed: bool
    state_mutation_executed: bool
    fact_promotion_executed: bool
    runtime_dispatch_executed: bool
