# -*- coding: utf-8 -*-
"""Working Memory skeleton v1 — pure functions only, no persistence."""

from __future__ import annotations

from typing import Iterable, List, Optional

from capabilities.midplatform.core.micro_os_common_types_v1 import (
    TTL_POLICY_BY_PRIORITY,
    WM_STATE_TRANSITIONS,
    CleanupPlanCandidate,
    Event,
    EventType,
    PriorityClass,
    TTLPolicyCandidate,
    ValidationResult,
    WorkingMemoryEntry,
    WorkingMemoryEntryState,
)


def create_working_memory_entry(event: Event) -> WorkingMemoryEntry:
    priority = event.priority_hint or PriorityClass.P2
    if event.event_type == EventType.MEMORY_RECALL:
        priority = PriorityClass.P4
    elif event.event_type in (EventType.HEALTH_REPORT, EventType.RECOVERY_CANDIDATE):
        priority = PriorityClass.P0
    elif event.event_type == EventType.USER_GOAL:
        priority = PriorityClass.P1
    state = WorkingMemoryEntryState.BLOCKED if event.ttl_hint is None and event.event_type != EventType.MEMORY_RECALL else WorkingMemoryEntryState.NEW
    if event.event_state.value == "blocked":
        state = WorkingMemoryEntryState.BLOCKED
    return WorkingMemoryEntry(
        working_memory_entry_id=f"wm_{event.event_id}",
        event_ref=event.event_id,
        candidate_ref=event.candidate_payload_ref,
        task_ref=f"task_{event.event_id}",
        priority_class=priority,
        state=state,
        ttl=event.ttl_hint,
        trace_id=event.trace_id,
        candidate_not_fact=True,
    )


def validate_wm_entry(entry: WorkingMemoryEntry) -> ValidationResult:
    issues = []
    if not entry.working_memory_entry_id:
        issues.append("missing_entry_id")
    if not entry.event_ref:
        issues.append("missing_event_ref")
    if entry.ttl is None:
        issues.append("ttl_missing")
    blocked = "ttl_missing" in issues
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=blocked)


def validate_wm_state_transition(from_state: WorkingMemoryEntryState, to_state: WorkingMemoryEntryState) -> ValidationResult:
    allowed = WM_STATE_TRANSITIONS.get(from_state, ())
    ok = to_state in allowed or from_state == to_state
    return ValidationResult(valid=ok, issues=() if ok else (f"invalid_wm_transition:{from_state.value}->{to_state.value}",))


def apply_ttl_policy_candidate(entry: WorkingMemoryEntry, policy_ref: Optional[TTLPolicyCandidate] = None) -> TTLPolicyCandidate:
    policy = policy_ref or TTL_POLICY_BY_PRIORITY.get(entry.priority_class, TTL_POLICY_BY_PRIORITY[PriorityClass.P2])
    return TTLPolicyCandidate(
        priority=entry.priority_class,
        ttl_seconds=entry.ttl if entry.ttl is not None else policy.ttl_seconds,
        on_expire=policy.on_expire,
        policy_name=policy.policy_name,
    )


def mark_stale_or_expired_candidate(entry: WorkingMemoryEntry, now_ref: Optional[str] = None) -> WorkingMemoryEntry:
    _ = now_ref
    if entry.state == WorkingMemoryEntryState.ACTIVE:
        entry.state = WorkingMemoryEntryState.STALE
        entry.freshness_status = "stale"
    elif entry.state == WorkingMemoryEntryState.STALE:
        entry.state = WorkingMemoryEntryState.EXPIRED
        entry.freshness_status = "expired"
    return entry


def generate_cleanup_plan_candidate(entries: Iterable[WorkingMemoryEntry]) -> CleanupPlanCandidate:
    actions: List[dict] = []
    for entry in entries:
        if entry.priority_class == PriorityClass.P5:
            actions.append({"entry_ref": entry.working_memory_entry_id, "action": "discard"})
        elif entry.state == WorkingMemoryEntryState.EXPIRED:
            actions.append({"entry_ref": entry.working_memory_entry_id, "action": "expire"})
        elif entry.state == WorkingMemoryEntryState.STALE:
            actions.append({"entry_ref": entry.working_memory_entry_id, "action": "mark_stale"})
    return CleanupPlanCandidate(actions=tuple(actions), candidate_only=True)
