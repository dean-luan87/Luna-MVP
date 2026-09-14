# -*- coding: utf-8 -*-
"""Micro-OS common types v1 — dataclass / enum skeleton only."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class EventType(str, Enum):
    MODULE_CANDIDATE = "module_candidate_event"
    USER_GOAL = "user_goal_event"
    DRIVE_SIGNAL = "drive_signal_event"
    HEALTH_REPORT = "health_report_event"
    RESOURCE_STATE = "resource_state_event"
    WORLDMODEL_RECALL = "worldmodel_recall_event"
    MEMORY_RECALL = "memory_recall_event"
    OUTPUT_CANDIDATE = "output_candidate_event"
    RECOVERY_CANDIDATE = "recovery_candidate_event"
    GOVERNANCE_CHECK = "governance_check_event"
    TTL_EXPIRY = "ttl_expiry_event"
    TASK_STATE = "task_state_event"


class EventState(str, Enum):
    RECEIVED = "received"
    NORMALIZED = "normalized"
    GOVERNANCE_PENDING = "governance_pending"
    HEALTH_PENDING = "health_pending"
    QUEUED = "queued"
    STORED_IN_WORKING_MEMORY = "stored_in_working_memory"
    SCHEDULED = "scheduled"
    ROUTED = "routed"
    COMPLETED = "completed"
    EXPIRED = "expired"
    DISCARDED = "discarded"
    BLOCKED = "blocked"
    FAILED = "failed"


class WorkingMemoryEntryState(str, Enum):
    NEW = "new"
    ACTIVE = "active"
    PENDING_CONFIRMATION = "pending_confirmation"
    INTEGRATED = "integrated"
    ALLOCATED = "allocated"
    WAITING_DOWNSTREAM = "waiting_downstream"
    STALE = "stale"
    EXPIRED = "expired"
    DISCARDED = "discarded"
    CONFIRMED = "confirmed"
    ADMISSION_CANDIDATE_GENERATED = "admission_candidate_generated"
    BLOCKED = "blocked"


class PriorityClass(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


class TerminalState(str, Enum):
    COMPLETED = "completed"
    EXPIRED = "expired"
    DISCARDED = "discarded"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class TraceRef:
    trace_id: str
    notes: Tuple[str, ...] = ()


@dataclass(frozen=True)
class HealthTag:
    tag: str
    status: str = "known"


@dataclass(frozen=True)
class GovernanceCheckRef:
    check_id: str
    cleared: bool = False
    risk_level: str = "low"


@dataclass(frozen=True)
class TTLPolicyCandidate:
    priority: PriorityClass
    ttl_seconds: Optional[int]
    on_expire: str
    policy_name: str


@dataclass
class Event:
    event_id: str
    event_type: EventType
    source_module: str
    source_chain: str
    timestamp: str
    health_tag: Optional[HealthTag]
    priority_hint: Optional[PriorityClass]
    ttl_hint: Optional[int]
    governance_required: bool
    governance_check_ref: Optional[GovernanceCheckRef]
    routing_targets: Tuple[str, ...]
    event_state: EventState
    trace_id: str
    candidate_payload_ref: str = ""
    spatial_anchor_ref: Optional[str] = None
    missing_spatial_anchor: bool = False
    trace: TraceRef = field(default_factory=lambda: TraceRef(trace_id=""))


@dataclass
class WorkingMemoryEntry:
    working_memory_entry_id: str
    event_ref: str
    candidate_ref: str
    task_ref: str
    priority_class: PriorityClass
    state: WorkingMemoryEntryState
    ttl: Optional[int]
    trace_id: str
    spatiotemporal_slot_ref: Optional[str] = None
    freshness_status: str = "fresh"
    confirmation_status: str = "pending"
    conflict_refs: Tuple[str, ...] = ()
    gap_refs: Tuple[str, ...] = ()
    health_refs: Tuple[str, ...] = ()
    downstream_refs: Tuple[str, ...] = ()
    admission_candidate_refs: Tuple[str, ...] = ()
    cleanup_policy: str = "expire_by_ttl"
    candidate_not_fact: bool = True


@dataclass
class SchedulingRequest:
    scheduling_request_id: str
    event_ref: str
    working_memory_entry_ref: str
    priority_class: PriorityClass
    task_relevance: str
    survival_relevance: str
    health_status: str
    resource_status: str
    ttl_status: str
    blockage_status: str
    preemption_allowed: bool
    defer_allowed: bool
    drop_allowed: bool
    routing_decision: str
    scheduling_state: str
    trace_id: str


@dataclass(frozen=True)
class SchedulingDecisionCandidate:
    decision_id: str
    request_ref: str
    priority_class: PriorityClass
    routing_decision: str
    preemption_candidate: bool
    defer_candidate: bool
    drop_candidate: bool
    blocked: bool
    candidate_only: bool = True
    runtime_execution: bool = False


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    issues: Tuple[str, ...] = ()
    blocked: bool = False


@dataclass(frozen=True)
class RouteCandidate:
    event_ref: str
    targets: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class WorkingMemoryEntryCandidate:
    entry: WorkingMemoryEntry
    candidate_only: bool = True


@dataclass(frozen=True)
class PreemptionCandidate:
    preempt: bool
    deferred_request_refs: Tuple[str, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class DeferralOrDropCandidate:
    defer: bool
    drop: bool
    reason: str = ""


@dataclass(frozen=True)
class CleanupPlanCandidate:
    actions: Tuple[Dict[str, Any], ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class HealthIssueCandidate:
    signal: str
    severity: str
    blocked: bool = False


EVENT_STATE_TRANSITIONS: Dict[EventState, Tuple[EventState, ...]] = {
    EventState.RECEIVED: (EventState.NORMALIZED, EventState.BLOCKED, EventState.FAILED),
    EventState.NORMALIZED: (EventState.GOVERNANCE_PENDING, EventState.QUEUED, EventState.BLOCKED),
    EventState.GOVERNANCE_PENDING: (EventState.HEALTH_PENDING, EventState.BLOCKED),
    EventState.HEALTH_PENDING: (EventState.QUEUED, EventState.BLOCKED),
    EventState.QUEUED: (EventState.STORED_IN_WORKING_MEMORY, EventState.DISCARDED, EventState.EXPIRED),
    EventState.STORED_IN_WORKING_MEMORY: (EventState.SCHEDULED, EventState.EXPIRED, EventState.BLOCKED),
    EventState.SCHEDULED: (EventState.ROUTED, EventState.BLOCKED),
    EventState.ROUTED: (EventState.COMPLETED, EventState.FAILED),
}

WM_STATE_TRANSITIONS: Dict[WorkingMemoryEntryState, Tuple[WorkingMemoryEntryState, ...]] = {
    WorkingMemoryEntryState.NEW: (WorkingMemoryEntryState.ACTIVE, WorkingMemoryEntryState.BLOCKED),
    WorkingMemoryEntryState.ACTIVE: (
        WorkingMemoryEntryState.PENDING_CONFIRMATION,
        WorkingMemoryEntryState.STALE,
        WorkingMemoryEntryState.EXPIRED,
        WorkingMemoryEntryState.ADMISSION_CANDIDATE_GENERATED,
    ),
    WorkingMemoryEntryState.PENDING_CONFIRMATION: (WorkingMemoryEntryState.CONFIRMED, WorkingMemoryEntryState.BLOCKED),
    WorkingMemoryEntryState.CONFIRMED: (WorkingMemoryEntryState.INTEGRATED, WorkingMemoryEntryState.ALLOCATED),
    WorkingMemoryEntryState.INTEGRATED: (WorkingMemoryEntryState.WAITING_DOWNSTREAM,),
    WorkingMemoryEntryState.ALLOCATED: (WorkingMemoryEntryState.WAITING_DOWNSTREAM,),
    WorkingMemoryEntryState.WAITING_DOWNSTREAM: (WorkingMemoryEntryState.DISCARDED, WorkingMemoryEntryState.STALE),
    WorkingMemoryEntryState.STALE: (WorkingMemoryEntryState.EXPIRED, WorkingMemoryEntryState.DISCARDED),
}

TTL_POLICY_BY_PRIORITY: Dict[PriorityClass, TTLPolicyCandidate] = {
    PriorityClass.P0: TTLPolicyCandidate(PriorityClass.P0, 5, "re_observe_required", "safety"),
    PriorityClass.P1: TTLPolicyCandidate(PriorityClass.P1, 30, "task_phase_revalidate", "active_task"),
    PriorityClass.P2: TTLPolicyCandidate(PriorityClass.P2, 120, "discard_or_reconfirm", "conversation"),
    PriorityClass.P3: TTLPolicyCandidate(PriorityClass.P3, 300, "stale_then_reobserve", "scene_continuity"),
    PriorityClass.P4: TTLPolicyCandidate(PriorityClass.P4, 600, "admission_later_or_discard", "memory_worldmodel_candidate"),
    PriorityClass.P5: TTLPolicyCandidate(PriorityClass.P5, 60, "discard_or_compress", "background"),
}

PRIORITY_HINT_MAP: Dict[EventType, PriorityClass] = {
    EventType.USER_GOAL: PriorityClass.P1,
    EventType.MODULE_CANDIDATE: PriorityClass.P2,
    EventType.HEALTH_REPORT: PriorityClass.P0,
    EventType.RECOVERY_CANDIDATE: PriorityClass.P0,
    EventType.MEMORY_RECALL: PriorityClass.P4,
    EventType.WORLDMODEL_RECALL: PriorityClass.P4,
    EventType.DRIVE_SIGNAL: PriorityClass.P2,
    EventType.RESOURCE_STATE: PriorityClass.P3,
    EventType.OUTPUT_CANDIDATE: PriorityClass.P2,
    EventType.GOVERNANCE_CHECK: PriorityClass.P1,
    EventType.TTL_EXPIRY: PriorityClass.P3,
    EventType.TASK_STATE: PriorityClass.P1,
}
