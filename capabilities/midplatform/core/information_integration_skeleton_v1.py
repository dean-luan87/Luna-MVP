# -*- coding: utf-8 -*-
"""Information Integration skeleton v1 — pure functions only, candidate generators."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from capabilities.midplatform.core.information_integration_types_v1 import (
    ConflictCandidate,
    DecisionContextCandidate,
    GapCandidate,
    InformationAllocationCandidate,
    LiveWorldStateCandidate,
    PriorityAttentionMapCandidate,
    RequiredObservationCandidate,
    SlotGroupCandidate,
    TaskWorldSliceCandidate,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import (
    PriorityClass,
    SchedulingDecisionCandidate,
    ValidationResult,
    WorkingMemoryEntry,
    WorkingMemoryEntryState,
)
from capabilities.midplatform.core.micro_os_static_validators_v1 import (
    validate_candidate_not_fact,
    validate_required_trace,
    validate_required_ttl,
)


def _entry_blocked(entry: WorkingMemoryEntry, guards: Optional[Mapping[str, Any]] = None) -> bool:
    if entry.state in (WorkingMemoryEntryState.STALE, WorkingMemoryEntryState.EXPIRED, WorkingMemoryEntryState.BLOCKED):
        return True
    if entry.freshness_status == "stale":
        return True
    if not validate_required_ttl(entry).valid:
        return True
    if not validate_required_trace(entry).valid:
        return True
    if guards and guards.get("governance_invalid"):
        return True
    return False


def collect_eligible_entries(
    entries: Sequence[WorkingMemoryEntry],
    scheduling_decisions: Sequence[SchedulingDecisionCandidate],
    guards: Optional[Mapping[str, Any]] = None,
) -> List[WorkingMemoryEntry]:
    blocked_refs = {d.request_ref for d in scheduling_decisions if d.blocked}
    eligible: List[WorkingMemoryEntry] = []
    for entry in entries:
        if _entry_blocked(entry, guards):
            continue
        if entry.working_memory_entry_id in blocked_refs:
            continue
        if not entry.candidate_not_fact:
            continue
        eligible.append(entry)
    return eligible


def group_entries_by_spatiotemporal_slot(entries: Sequence[WorkingMemoryEntry]) -> List[SlotGroupCandidate]:
    groups: Dict[str, List[str]] = {}
    for entry in entries:
        slot = entry.spatiotemporal_slot_ref or "slot_unassigned"
        groups.setdefault(slot, []).append(entry.working_memory_entry_id)
    return [
        SlotGroupCandidate(
            candidate_id=f"slot_group_{slot_id}",
            slot_id=slot_id,
            entry_refs=tuple(refs),
            trace_ref=entries[0].trace_id if entries else "",
            candidate_only=True,
        )
        for slot_id, refs in sorted(groups.items())
    ]


def build_live_world_state_candidate(
    slot_group: SlotGroupCandidate,
    context: Optional[Mapping[str, Any]] = None,
) -> LiveWorldStateCandidate:
    _ = context
    trace_ref = (context or {}).get("trace_ref", f"trace_{slot_group.slot_id}")
    return LiveWorldStateCandidate(
        candidate_id=f"lws_{slot_group.slot_id}",
        source_entry_refs=slot_group.entry_refs,
        spatiotemporal_slot_ref=slot_group.slot_id,
        observed_state_summary=f"observed_state_candidate for {slot_group.slot_id}",
        freshness_status="fresh",
        confidence_summary="medium",
        trace_ref=trace_ref,
        health_refs=(),
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def extract_task_world_slice_candidate(
    entries: Sequence[WorkingMemoryEntry],
    task_context: Optional[Mapping[str, Any]] = None,
) -> TaskWorldSliceCandidate:
    task_ref = (task_context or {}).get("task_ref") or (entries[0].task_ref if entries else "task_unknown")
    refs = tuple(e.working_memory_entry_id for e in entries)
    priority = entries[0].priority_class if entries else PriorityClass.P2
    trace_ref = entries[0].trace_id if entries else ""
    return TaskWorldSliceCandidate(
        candidate_id=f"tws_{task_ref}",
        task_ref=task_ref,
        relevant_entry_refs=refs,
        task_relevance_summary=f"task slice for {task_ref}",
        priority_class=priority,
        trace_ref=trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def build_priority_attention_map_candidate(
    entries: Sequence[WorkingMemoryEntry],
    scheduling_decisions: Sequence[SchedulingDecisionCandidate],
) -> PriorityAttentionMapCandidate:
    buckets: Dict[PriorityClass, List[str]] = {p: [] for p in PriorityClass}
    for entry in entries:
        buckets[entry.priority_class].append(entry.working_memory_entry_id)
    trace_ref = entries[0].trace_id if entries else ""
    survival = "P0/P1 present" if buckets[PriorityClass.P0] or buckets[PriorityClass.P1] else "none"
    return PriorityAttentionMapCandidate(
        candidate_id="pam_default",
        p0_refs=tuple(buckets[PriorityClass.P0]),
        p1_refs=tuple(buckets[PriorityClass.P1]),
        p2_refs=tuple(buckets[PriorityClass.P2]),
        p3_refs=tuple(buckets[PriorityClass.P3]),
        p4_refs=tuple(buckets[PriorityClass.P4]),
        p5_refs=tuple(buckets[PriorityClass.P5]),
        survival_relevance_summary=survival,
        task_relevance_summary=f"{len(scheduling_decisions)} scheduling refs",
        trace_ref=trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def detect_conflict_candidate(
    entries: Sequence[WorkingMemoryEntry],
    recall_context: Optional[Mapping[str, Any]] = None,
) -> List[ConflictCandidate]:
    conflicts: List[ConflictCandidate] = []
    if recall_context and recall_context.get("conflicts_with_realtime"):
        conflicts.append(
            ConflictCandidate(
                candidate_id="conflict_recall_realtime",
                conflict_type="recall_realtime_mismatch",
                involved_entry_refs=tuple(e.working_memory_entry_id for e in entries),
                conflict_summary="recall context conflicts with realtime safety candidate",
                severity="high",
                requires_confirmation=True,
                decision_readiness="not_ready",
                trace_ref=entries[0].trace_id if entries else "",
                fact_status="not_fact",
                candidate_not_fact=True,
            )
        )
    seen_tasks: Dict[str, str] = {}
    for entry in entries:
        if entry.task_ref in seen_tasks and seen_tasks[entry.task_ref] != entry.priority_class.value:
            conflicts.append(
                ConflictCandidate(
                    candidate_id=f"conflict_prio_{entry.working_memory_entry_id}",
                    conflict_type="priority_mismatch",
                    involved_entry_refs=(entry.working_memory_entry_id, seen_tasks[entry.task_ref]),
                    conflict_summary="priority mismatch within task slice",
                    severity="medium",
                    requires_confirmation=True,
                    decision_readiness="not_ready",
                    trace_ref=entry.trace_id,
                    fact_status="not_fact",
                    candidate_not_fact=True,
                )
            )
        seen_tasks[entry.task_ref] = entry.priority_class.value
    return conflicts


def detect_gap_candidate(
    entries: Sequence[WorkingMemoryEntry],
    task_context: Optional[Mapping[str, Any]] = None,
) -> Tuple[List[GapCandidate], List[RequiredObservationCandidate]]:
    gaps: List[GapCandidate] = []
    observations: List[RequiredObservationCandidate] = []
    required_fields = (task_context or {}).get("required_fields") or []
    for field_name in required_fields:
        obs_id = f"req_obs_{field_name}"
        obs = RequiredObservationCandidate(
            candidate_id=obs_id,
            observation_target=field_name,
            requested_module=(task_context or {}).get("requested_module", "module_adapter"),
            reason=f"missing {field_name}",
            priority_class=PriorityClass.P2,
            ttl=120,
            trace_ref=entries[0].trace_id if entries else "",
            fact_status="not_fact",
            candidate_not_fact=True,
        )
        observations.append(obs)
        gaps.append(
            GapCandidate(
                candidate_id=f"gap_{field_name}",
                gap_type="missing_information",
                missing_information=field_name,
                affected_task_ref=(task_context or {}).get("task_ref", "task_unknown"),
                required_observation_candidate_ref=obs_id,
                severity="medium",
                trace_ref=entries[0].trace_id if entries else "",
                fact_status="not_fact",
                candidate_not_fact=True,
            )
        )
    return gaps, observations


def allocate_information_candidate(
    live_world_state: LiveWorldStateCandidate,
    task_world_slice: TaskWorldSliceCandidate,
    conflicts: Sequence[ConflictCandidate],
    gaps: Sequence[GapCandidate],
    attention_map: PriorityAttentionMapCandidate,
) -> InformationAllocationCandidate:
    hold = bool(conflicts) or bool(gaps)
    if hold:
        return InformationAllocationCandidate(
            candidate_id="alloc_hold",
            hold_refs=(live_world_state.candidate_id, task_world_slice.candidate_id),
            health_watchdog_refs=tuple(attention_map.p0_refs),
            trace_ref=live_world_state.trace_ref,
            fact_status="not_fact",
            candidate_not_fact=True,
        )
    return InformationAllocationCandidate(
        candidate_id="alloc_default",
        decision_center_refs=(live_world_state.candidate_id,),
        task_manager_refs=(task_world_slice.candidate_id,),
        module_adapter_refs=(attention_map.candidate_id,),
        trace_ref=live_world_state.trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def build_decision_context_candidate(
    live_world_state: LiveWorldStateCandidate,
    task_world_slice: TaskWorldSliceCandidate,
    attention_map: PriorityAttentionMapCandidate,
    allocation: InformationAllocationCandidate,
    conflicts: Optional[Sequence[ConflictCandidate]] = None,
    gaps: Optional[Sequence[GapCandidate]] = None,
    governance_ref: Optional[str] = None,
    high_risk: bool = False,
) -> DecisionContextCandidate:
    conflict_list = tuple(c.candidate_id for c in (conflicts or ()))
    gap_list = tuple(g.candidate_id for g in (gaps or ()))
    obs_refs = tuple(
        g.required_observation_candidate_ref
        for g in (gaps or ())
        if g.required_observation_candidate_ref
    )
    blocked = False
    readiness = "ready"
    if high_risk and not governance_ref:
        blocked = True
        readiness = "not_ready"
    if any(c.decision_readiness == "not_ready" for c in (conflicts or ())):
        blocked = True
        readiness = "not_ready"
    elif allocation.hold_refs:
        readiness = "hold"
    return DecisionContextCandidate(
        candidate_id="dcc_default",
        live_world_state_ref=live_world_state.candidate_id,
        task_world_slice_ref=task_world_slice.candidate_id,
        priority_attention_map_ref=attention_map.candidate_id,
        conflict_refs=conflict_list,
        gap_refs=gap_list,
        required_observation_refs=obs_refs,
        governance_check_ref=governance_ref,
        health_refs=live_world_state.health_refs,
        readiness_status=readiness,
        trace_ref=live_world_state.trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
        high_risk=high_risk,
        blocked=blocked,
    )


def validate_information_integration_candidate(obj: Any) -> ValidationResult:
    issues: List[str] = []
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    trace_ref = getattr(obj, "trace_ref", None) or getattr(obj, "trace_id", None)
    if not trace_ref:
        issues.append("missing_trace")
    fact_status = getattr(obj, "fact_status", None)
    if fact_status and fact_status != "not_fact":
        issues.append("fact_status_not_candidate")
    if hasattr(obj, "ttl") and obj.ttl is None and isinstance(obj, RequiredObservationCandidate):
        issues.append("ttl_missing")
    if hasattr(obj, "high_risk") and obj.high_risk and not getattr(obj, "governance_check_ref", None):
        issues.append("governance_ref_missing_for_high_risk")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked="governance_ref_missing_for_high_risk" in issues)
