# -*- coding: utf-8 -*-
"""Health Watchdog types v1 - enums and candidate dataclasses only."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class HealthWatchdogState(str, Enum):
    RECEIVED = "received"
    VALIDATING = "validating"
    HEALTH_SIGNAL_REVIEW = "health_signal_review"
    STALE_CONTEXT_REVIEW = "stale_context_review"
    LOW_CONFIDENCE_REVIEW = "low_confidence_review"
    P0_SAFETY_REVIEW = "p0_safety_review"
    GOVERNANCE_REVIEW = "governance_review"
    DEGRADATION_CANDIDATE_GENERATED = "degradation_candidate_generated"
    RECOVERY_RECOMMENDATION_CANDIDATE_GENERATED = "recovery_recommendation_candidate_generated"
    REQUIRED_OBSERVATION_GENERATED = "required_observation_generated"
    HOLD = "hold"
    BLOCKED = "blocked"
    NOT_READY = "not_ready"
    WATCHDOG_HANDOFF_READY = "watchdog_handoff_ready"
    DISCARDED_INVALID = "discarded_invalid"


class HealthSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class HealthSignalCandidate:
    candidate_id: str
    source_decision_ref: str
    signal_type: str
    severity: str
    health_refs: Tuple[str, ...]
    stale_refs: Tuple[str, ...]
    low_confidence_refs: Tuple[str, ...]
    p0_safety_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class DegradationCandidate:
    candidate_id: str
    degradation_type: str
    degradation_level: str
    affected_module_refs: Tuple[str, ...]
    reason: str
    recommended_hold: bool
    trace_ref: str
    fact_status: str = "not_fact"
    real_degradation: bool = False
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class RecoveryRecommendationCandidate:
    candidate_id: str
    recommendation_type: str
    recommendation_reason: str
    affected_module_refs: Tuple[str, ...]
    governance_required: bool
    governance_ref: Optional[str]
    trace_ref: str
    fact_status: str = "not_fact"
    recovery_execution: bool = False
    restart_allowed: bool = False
    process_control_allowed: bool = False
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class RequiredObservationCandidate:
    candidate_id: str
    observation_reason: str
    target_refs: Tuple[str, ...]
    urgency: str
    source_health_signal_ref: str
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class ModuleHealthReviewCandidate:
    candidate_id: str
    module_ref: str
    issue_type: str
    severity: str
    evidence_refs: Tuple[str, ...]
    recommended_status: str
    trace_ref: str
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class WatchdogHandoffCandidate:
    candidate_id: str
    source_candidate_refs: Tuple[str, ...]
    module_adapter_refs: Tuple[str, ...]
    task_manager_refs: Tuple[str, ...]
    decision_center_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    output_gate_refs: Tuple[str, ...]
    handoff_allowed: bool
    trace_ref: str
    fact_status: str = "not_fact"
    direct_mount: bool = False
    candidate_not_fact: bool = True
