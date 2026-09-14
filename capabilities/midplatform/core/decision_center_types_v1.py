# -*- coding: utf-8 -*-
"""Decision Center types v1 — enums and candidate dataclasses only."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class DecisionState(str, Enum):
    RECEIVED = "received"
    VALIDATING = "validating"
    GOVERNANCE_PENDING = "governance_pending"
    HEALTH_PENDING = "health_pending"
    CONFLICT_REVIEW = "conflict_review"
    GAP_REVIEW = "gap_review"
    READY_FOR_CANDIDATE_DECISION = "ready_for_candidate_decision"
    DECISION_CANDIDATE_GENERATED = "decision_candidate_generated"
    BLOCKED = "blocked"
    NOT_READY = "not_ready"
    HOLD = "hold"
    REQUIRES_OBSERVATION = "requires_observation"
    REQUIRES_HEALTH_REVIEW = "requires_health_review"
    HANDOFF_READY = "handoff_ready"
    DISCARDED_INVALID = "discarded_invalid"


class DecisionReadiness(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"
    BLOCKED = "blocked"
    NEEDS_OBSERVATION = "needs_observation"
    NEEDS_HEALTH_REVIEW = "needs_health_review"


@dataclass(frozen=True)
class DecisionCandidate:
    candidate_id: str
    decision_context_ref: str
    readiness: str
    decision_state: str
    decision_summary: str
    recommended_handoff: str
    governance_check_ref: Optional[str]
    health_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    gap_refs: Tuple[str, ...]
    trace_ref: str
    fact_status: str = "not_fact"
    final_action: bool = False
    user_output: bool = False
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class DecisionReadinessCandidate:
    candidate_id: str
    decision_context_ref: str
    readiness: str
    readiness_reason: str
    blocker_refs: Tuple[str, ...]
    required_observation_refs: Tuple[str, ...]
    health_review_refs: Tuple[str, ...]
    governance_pending: bool
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class DecisionBlockCandidate:
    candidate_id: str
    block_type: str
    block_reason: str
    blocked_refs: Tuple[str, ...]
    forbidden_route: str
    recovery_or_hold_candidate: str
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class DecisionExplanationCandidate:
    candidate_id: str
    decision_candidate_ref: str
    explanation_summary: str
    evidence_refs: Tuple[str, ...]
    conflict_summary: str
    gap_summary: str
    health_summary: str
    governance_summary: str
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class DownstreamDecisionHandoffCandidate:
    candidate_id: str
    decision_candidate_ref: str
    task_manager_refs: Tuple[str, ...]
    output_gate_refs: Tuple[str, ...]
    health_watchdog_refs: Tuple[str, ...]
    module_adapter_refs: Tuple[str, ...]
    worldmodel_memory_bridge_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    handoff_allowed: bool
    trace_ref: str
    fact_status: str = "not_fact"
    direct_mount: bool = False
    candidate_not_fact: bool = True
