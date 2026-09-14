"""Reference-only Decision-to-Task handoff envelope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


DECISION_OWNER = "Decision Governance"
TASK_MANAGER_OWNER = "Task Manager"


@dataclass(frozen=True)
class DecisionToTaskManagerHandoffCandidateV1:
    """Candidate input to the existing Task Manager controlled boundary."""

    handoff_ref: str
    case_id: str
    producer_owner_ref: str
    consumer_owner_ref: str
    source_decision_handoff_ref: str
    decision_candidate_ref: str
    decision_trace_ref: str
    selected_candidate_ref: str
    option_ref: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    context_ref: str
    cognitive_loop_ref: str
    constraint_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    execution_instance_ref: str
    candidate_only: bool = True
    task_execution: bool = False
    action_execution: bool = False


__all__ = [
    "DECISION_OWNER",
    "TASK_MANAGER_OWNER",
    "DecisionToTaskManagerHandoffCandidateV1",
]

