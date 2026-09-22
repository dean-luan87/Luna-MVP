"""Reference-only Task-to-Action handoff envelope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


TASK_MANAGER_OWNER = "Task Manager"
ACTION_BOUNDARY_OWNER = "Action Governance"


@dataclass(frozen=True)
class TaskToActionHandoffCandidateV1:
    handoff_ref: str
    case_id: str
    producer_owner: str
    consumer_owner: str
    task_state_ref: str
    task_trace_ref: str
    task_status: str
    decision_candidate_ref: str
    decision_trace_ref: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    context_ref: str
    cognitive_loop_ref: str
    option_ref: str
    final_cognition_execution_ref: str
    final_sufficiency_ref: str
    final_stop_ref: str
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None
    candidate_only: bool = True
    action_execution: bool = False
    runtime_dispatch: bool = False
    device_control: bool = False
    resource_state: str = "unknown"


__all__ = [
    "ACTION_BOUNDARY_OWNER",
    "TASK_MANAGER_OWNER",
    "TaskToActionHandoffCandidateV1",
]
