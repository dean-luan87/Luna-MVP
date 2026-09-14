# -*- coding: utf-8 -*-
"""Scheduler skeleton v1 — pure functions only, no worker/thread."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional

from capabilities.midplatform.core.micro_os_common_types_v1 import (
    PRIORITY_HINT_MAP,
    DeferralOrDropCandidate,
    Event,
    EventType,
    PreemptionCandidate,
    PriorityClass,
    SchedulingDecisionCandidate,
    SchedulingRequest,
    WorkingMemoryEntry,
)


def assign_priority_candidate(entry: WorkingMemoryEntry, context: Optional[Mapping[str, Any]] = None) -> SchedulingRequest:
    _ = context
    return SchedulingRequest(
        scheduling_request_id=f"sched_{entry.working_memory_entry_id}",
        event_ref=entry.event_ref,
        working_memory_entry_ref=entry.working_memory_entry_id,
        priority_class=entry.priority_class,
        task_relevance="high" if entry.priority_class in (PriorityClass.P0, PriorityClass.P1) else "normal",
        survival_relevance="high" if entry.priority_class == PriorityClass.P0 else "normal",
        health_status="known",
        resource_status="normal",
        ttl_status="valid" if entry.ttl is not None else "missing",
        blockage_status="blocked" if entry.state.value == "blocked" else "clear",
        preemption_allowed=entry.priority_class == PriorityClass.P0,
        defer_allowed=entry.priority_class in (PriorityClass.P2, PriorityClass.P3, PriorityClass.P4),
        drop_allowed=entry.priority_class == PriorityClass.P5,
        routing_decision="hold" if entry.state.value == "blocked" else "route_candidate",
        scheduling_state="candidate",
        trace_id=entry.trace_id,
    )


def evaluate_preemption_candidate(
    request: SchedulingRequest,
    active_requests: Optional[Iterable[SchedulingRequest]] = None,
) -> PreemptionCandidate:
    active = list(active_requests or [])
    if request.priority_class != PriorityClass.P0:
        return PreemptionCandidate(preempt=False)
    deferred = [
        r.scheduling_request_id
        for r in active
        if r.priority_class in (PriorityClass.P1, PriorityClass.P2, PriorityClass.P3, PriorityClass.P4, PriorityClass.P5)
    ]
    return PreemptionCandidate(preempt=True, deferred_request_refs=tuple(deferred), reason="p0_preempts_lower")


def evaluate_deferral_or_drop_candidate(
    request: SchedulingRequest,
    resource_state: Optional[str] = None,
) -> DeferralOrDropCandidate:
    if resource_state == "resource_overload" and request.drop_allowed:
        return DeferralOrDropCandidate(defer=False, drop=True, reason="p5_drop_under_overload")
    if resource_state == "resource_overload" and request.defer_allowed:
        return DeferralOrDropCandidate(defer=True, drop=False, reason="defer_under_overload")
    if resource_state == "cloud_unavailable":
        return DeferralOrDropCandidate(defer=True, drop=False, reason="local_or_hold")
    if resource_state == "model_unavailable":
        return DeferralOrDropCandidate(defer=True, drop=False, reason="fallback_or_hold")
    if resource_state == "health_unknown":
        return DeferralOrDropCandidate(defer=True, drop=False, reason="conservative_hold")
    return DeferralOrDropCandidate(defer=False, drop=False)


def produce_scheduling_decision_candidate(
    request: SchedulingRequest,
    guards: Optional[Mapping[str, Any]] = None,
) -> SchedulingDecisionCandidate:
    guards = dict(guards or {})
    blocked = request.blockage_status == "blocked" or guards.get("blocked", False)
    preemption = request.preemption_allowed and not blocked
    defer = request.defer_allowed and guards.get("resource_state") in ("resource_overload", "cloud_unavailable", "model_unavailable")
    drop = request.drop_allowed and guards.get("resource_state") == "resource_overload"
    routing = "blocked_candidate" if blocked else ("drop_candidate" if drop else ("defer_candidate" if defer else "route_candidate"))
    return SchedulingDecisionCandidate(
        decision_id=f"decision_{request.scheduling_request_id}",
        request_ref=request.scheduling_request_id,
        priority_class=request.priority_class,
        routing_decision=routing,
        preemption_candidate=preemption,
        defer_candidate=defer,
        drop_candidate=drop,
        blocked=blocked,
        candidate_only=True,
        runtime_execution=False,
    )


def priority_from_event(event: Event) -> PriorityClass:
    if event.priority_hint:
        return event.priority_hint
    return PRIORITY_HINT_MAP.get(event.event_type, PriorityClass.P2)


def is_safety_event(event: Event) -> bool:
    return event.event_type in (EventType.HEALTH_REPORT, EventType.RECOVERY_CANDIDATE) or event.priority_hint == PriorityClass.P0
