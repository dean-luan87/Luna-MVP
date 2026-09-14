# -*- coding: utf-8 -*-
"""Event Bus skeleton v1 — pure functions only, no event loop."""

from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.core.micro_os_common_types_v1 import (
    EVENT_STATE_TRANSITIONS,
    Event,
    EventState,
    EventType,
    GovernanceCheckRef,
    HealthTag,
    PriorityClass,
    RouteCandidate,
    TraceRef,
    ValidationResult,
)


def normalize_event(raw_event: Mapping[str, Any]) -> Event:
    event_type = raw_event.get("event_type")
    if isinstance(event_type, EventType):
        et = event_type
    else:
        et = EventType(str(event_type))
    priority_hint = raw_event.get("priority_hint")
    if priority_hint is not None and not isinstance(priority_hint, PriorityClass):
        priority_hint = PriorityClass(str(priority_hint))
    health_raw = raw_event.get("health_tag")
    health_tag = None
    if isinstance(health_raw, HealthTag):
        health_tag = health_raw
    elif isinstance(health_raw, dict) and health_raw.get("tag"):
        health_tag = HealthTag(tag=str(health_raw["tag"]), status=str(health_raw.get("status", "known")))
    gov_raw = raw_event.get("governance_check_ref")
    governance_check_ref = None
    if isinstance(gov_raw, GovernanceCheckRef):
        governance_check_ref = gov_raw
    elif isinstance(gov_raw, dict) and gov_raw.get("check_id"):
        governance_check_ref = GovernanceCheckRef(
            check_id=str(gov_raw["check_id"]),
            cleared=bool(gov_raw.get("cleared", False)),
            risk_level=str(gov_raw.get("risk_level", "low")),
        )
    trace_id = str(raw_event.get("trace_id") or raw_event.get("event_id", ""))
    return Event(
        event_id=str(raw_event.get("event_id", "")),
        event_type=et,
        source_module=str(raw_event.get("source_module", "")),
        source_chain=str(raw_event.get("source_chain", "")),
        timestamp=str(raw_event.get("timestamp", "")),
        health_tag=health_tag,
        priority_hint=priority_hint,
        ttl_hint=raw_event.get("ttl_hint"),
        governance_required=bool(raw_event.get("governance_required", False)),
        governance_check_ref=governance_check_ref,
        routing_targets=tuple(raw_event.get("routing_targets") or ()),
        event_state=EventState.NORMALIZED,
        trace_id=trace_id,
        candidate_payload_ref=str(raw_event.get("candidate_payload_ref", "")),
        spatial_anchor_ref=raw_event.get("spatial_anchor_ref"),
        missing_spatial_anchor=bool(raw_event.get("missing_spatial_anchor", False)),
        trace=TraceRef(trace_id=trace_id),
    )


def validate_event_schema(event: Event) -> ValidationResult:
    issues = []
    if not event.event_id:
        issues.append("missing_event_id")
    if not event.source_module:
        issues.append("missing_source_module")
    if not event.source_chain:
        issues.append("missing_source_chain")
    if not event.timestamp:
        issues.append("missing_timestamp")
    if event.health_tag is None:
        issues.append("missing_health_tag")
    if event.governance_required and event.governance_check_ref is None:
        issues.append("missing_governance_check_ref")
    blocked = "missing_source_chain" in issues or "missing_timestamp" in issues
    if event.governance_required and event.governance_check_ref is None:
        blocked = True
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=blocked)


def validate_event_state_transition(from_state: EventState, to_state: EventState) -> ValidationResult:
    allowed = EVENT_STATE_TRANSITIONS.get(from_state, ())
    ok = to_state in allowed or from_state == to_state
    return ValidationResult(valid=ok, issues=() if ok else (f"invalid_transition:{from_state.value}->{to_state.value}",))


def route_event_candidate(event: Event) -> RouteCandidate:
    if event.event_state == EventState.BLOCKED:
        return RouteCandidate(event_ref=event.event_id, targets=())
    targets = list(event.routing_targets)
    if "working_memory" not in targets:
        targets.append("working_memory")
    if "scheduler" not in targets:
        targets.append("scheduler")
    return RouteCandidate(event_ref=event.event_id, targets=tuple(targets), candidate_only=True)


def append_trace(event: Event, trace_note: str) -> Event:
    notes = event.trace.notes + (trace_note,)
    event.trace = TraceRef(trace_id=event.trace_id, notes=notes)
    return event
