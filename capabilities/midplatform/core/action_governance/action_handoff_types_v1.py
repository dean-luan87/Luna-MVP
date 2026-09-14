"""Action handoff candidate types for Runtime Executor and Task Manager."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ActionToRuntimeExecutorHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    handoff_kind: str
    action_candidate_ref: str
    target_refs: Tuple[str, ...]
    precondition_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    confirmation_state: str
    resource_refs: Tuple[str, ...]
    reversibility: str
    rollback_context_ref: str
    provenance: Tuple[str, ...]
    execution_readiness: str
    candidate_only: bool = True
    action_executed: bool = False
    scheduler_executed: bool = False
    device_control_executed: bool = False


@dataclass(frozen=True)
class ActionToTaskManagerHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    handoff_kind: str
    action_candidate_ref: str
    task_reference_context_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    provenance: Tuple[str, ...]
    reference_only: bool = True
    task_created: bool = False
