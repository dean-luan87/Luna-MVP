# -*- coding: utf-8 -*-
"""Task Manager types v1 - enums and candidate dataclasses only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum


class TaskState(str, Enum):
    RECEIVED = "received"
    VALIDATING = "validating"
    HEALTH_GATE_REVIEW = "health_gate_review"
    GOVERNANCE_REVIEW = "governance_review"
    DECISION_READINESS_REVIEW = "decision_readiness_review"
    OBSERVATION_REQUIREMENT_REVIEW = "observation_requirement_review"
    TASK_CANDIDATE_GENERATED = "task_candidate_generated"
    TASK_PLAN_CANDIDATE_GENERATED = "task_plan_candidate_generated"
    TASK_STEP_CANDIDATE_GENERATED = "task_step_candidate_generated"
    TASK_HANDOFF_READY = "task_handoff_ready"
    HOLD = "hold"
    BLOCKED = "blocked"
    PAUSED = "paused"
    NOT_READY = "not_ready"
    REQUIRES_OBSERVATION = "requires_observation"
    DISCARDED_INVALID = "discarded_invalid"


class TaskReadiness(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"
    BLOCKED = "blocked"
    HOLD = "hold"
    PAUSED = "paused"
    REQUIRES_OBSERVATION = "requires_observation"


@dataclass(frozen=True)
class TaskCandidate:
    candidate_id: str
    source_decision_ref: str
    source_health_refs: Tuple[str, ...]
    task_context_refs: Tuple[str, ...]
    readiness: str
    task_state: str
    task_summary: str
    governance_ref: Optional[str]
    health_gate_refs: Tuple[str, ...]
    blocker_refs: Tuple[str, ...]
    trace_ref: str
    fact_status: str = "not_fact"
    task_execution: bool = False
    user_output: bool = False
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class TaskReadinessCandidate:
    candidate_id: str
    task_candidate_ref: str
    readiness: str
    readiness_reason: str
    blocker_refs: Tuple[str, ...]
    health_gate_refs: Tuple[str, ...]
    required_observation_refs: Tuple[str, ...]
    governance_pending: bool
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class TaskBlockCandidate:
    candidate_id: str
    block_type: str
    block_reason: str
    blocked_refs: Tuple[str, ...]
    forbidden_route: str
    hold_or_reobserve_candidate: str
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class TaskPlanCandidate:
    candidate_id: str
    task_candidate_ref: str
    plan_summary: str
    planned_step_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    blocker_refs: Tuple[str, ...]
    trace_ref: str
    fact_status: str = "not_fact"
    task_execution: bool = False
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class TaskStepCandidate:
    candidate_id: str
    task_candidate_ref: str
    step_order: int
    step_summary: str
    required_capability_refs: Tuple[str, ...]
    required_observation_refs: Tuple[str, ...]
    blocker_refs: Tuple[str, ...]
    trace_ref: str
    fact_status: str = "not_fact"
    executed_step: bool = False
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class TaskHandoffCandidate:
    candidate_id: str
    task_candidate_ref: str
    module_adapter_refs: Tuple[str, ...]
    output_gate_refs: Tuple[str, ...]
    worldmodel_memory_bridge_refs: Tuple[str, ...]
    decision_center_refs: Tuple[str, ...]
    health_watchdog_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    handoff_allowed: bool
    trace_ref: str
    fact_status: str = "not_fact"
    direct_mount: bool = False
    candidate_not_fact: bool = True
