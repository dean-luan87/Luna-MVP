# -*- coding: utf-8 -*-
"""Information Integration candidate types v1 — dataclass skeleton only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.micro_os_common_types_v1 import PriorityClass


@dataclass(frozen=True)
class SlotGroupCandidate:
    candidate_id: str
    slot_id: str
    entry_refs: Tuple[str, ...]
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_only: bool = True
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class LiveWorldStateCandidate:
    candidate_id: str
    source_entry_refs: Tuple[str, ...]
    spatiotemporal_slot_ref: Optional[str]
    observed_state_summary: str
    freshness_status: str
    confidence_summary: str
    conflict_refs: Tuple[str, ...] = ()
    gap_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    health_refs: Tuple[str, ...] = ()
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class TaskWorldSliceCandidate:
    candidate_id: str
    task_ref: str
    relevant_entry_refs: Tuple[str, ...]
    task_relevance_summary: str
    priority_class: PriorityClass
    required_observation_refs: Tuple[str, ...] = ()
    blocked_reason: Optional[str] = None
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class PriorityAttentionMapCandidate:
    candidate_id: str
    p0_refs: Tuple[str, ...] = ()
    p1_refs: Tuple[str, ...] = ()
    p2_refs: Tuple[str, ...] = ()
    p3_refs: Tuple[str, ...] = ()
    p4_refs: Tuple[str, ...] = ()
    p5_refs: Tuple[str, ...] = ()
    survival_relevance_summary: str = ""
    task_relevance_summary: str = ""
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class InformationAllocationCandidate:
    candidate_id: str
    decision_center_refs: Tuple[str, ...] = ()
    task_manager_refs: Tuple[str, ...] = ()
    health_watchdog_refs: Tuple[str, ...] = ()
    module_adapter_refs: Tuple[str, ...] = ()
    worldmodel_memory_bridge_refs: Tuple[str, ...] = ()
    hold_refs: Tuple[str, ...] = ()
    discard_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class ConflictCandidate:
    candidate_id: str
    conflict_type: str
    involved_entry_refs: Tuple[str, ...]
    conflict_summary: str
    severity: str
    requires_confirmation: bool
    decision_readiness: str
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class GapCandidate:
    candidate_id: str
    gap_type: str
    missing_information: str
    affected_task_ref: str
    required_observation_candidate_ref: Optional[str] = None
    severity: str = "medium"
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class RequiredObservationCandidate:
    candidate_id: str
    observation_target: str
    requested_module: str
    reason: str
    priority_class: PriorityClass
    ttl: Optional[int]
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class DecisionContextCandidate:
    candidate_id: str
    live_world_state_ref: str
    task_world_slice_ref: str
    priority_attention_map_ref: str
    conflict_refs: Tuple[str, ...] = ()
    gap_refs: Tuple[str, ...] = ()
    required_observation_refs: Tuple[str, ...] = ()
    governance_check_ref: Optional[str] = None
    health_refs: Tuple[str, ...] = ()
    readiness_status: str = "ready"
    trace_ref: str = ""
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True
    high_risk: bool = False
    blocked: bool = False
