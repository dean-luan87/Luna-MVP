from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class SelectionHandoffInput:
    reducer_run_id: str
    field_id: str
    state_type: str
    selection_status: str
    selected_policy_ids: Tuple[str, ...]
    composition_sequence: Tuple[str, ...]
    policy_evaluation_refs: Tuple[str, ...]
    selection_trace_ref: str
    selection_replay_key: str
    existing_state_snapshot: Dict[str, Any]
    admitted_event_refs: Tuple[str, ...]
    temporal_snapshot: Dict[str, Any]
    conflict_snapshot: Dict[str, Any]
    overlay_snapshot: Dict[str, Any]
    owner_correction_snapshot: Dict[str, Any]
    version_snapshots: Dict[str, str]
    selected_policy_metadata: Dict[str, Dict[str, Any]]
    direct_state_write_requested: bool = False
    action_trigger_requested: bool = False
    admitted_events: Tuple[Dict[str, Any], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PolicyApplicationPlan:
    application_plan_id: str
    selected_policy_ids: Tuple[str, ...]
    ordered_application_steps: Tuple[Dict[str, Any], ...]
    intended_change_type: str
    target_state_status: str
    supporting_event_refs: Tuple[str, ...]
    blocking_reasons: Tuple[str, ...]
    deferred_actions: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class StateTransitionResult:
    requested_transition: str
    transition_allowed: bool
    transition_status: str
    required_evidence: Tuple[str, ...]
    rejection_reasons: Tuple[str, ...]
    transition_trace: Tuple[Dict[str, Any], ...]


@dataclass(frozen=True)
class ConflictReductionResult:
    conflict_status: str
    preserve_conflict: bool
    provisional_candidate_allowed: bool
    conflicting_event_refs: Tuple[str, ...]
    rejection_reasons: Tuple[str, ...]
    decision_steps: Tuple[Dict[str, Any], ...]


@dataclass(frozen=True)
class OverlayReductionResult:
    overlay_status: str
    overlay_refs: Tuple[str, ...]
    substrate_mutated: bool
    refresh_evidence_required: bool
    rejection_reasons: Tuple[str, ...]
    decision_steps: Tuple[Dict[str, Any], ...]


@dataclass(frozen=True)
class FieldStateCandidate:
    state_candidate_id: str
    field_id: str
    state_type: str
    candidate_status: str
    candidate_value: Dict[str, Any]
    temporal_status: str
    confidence_snapshot: Dict[str, Any]
    supporting_event_refs: Tuple[str, ...]
    conflicting_event_refs: Tuple[str, ...]
    overlay_refs: Tuple[str, ...]
    owner_correction_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    selected_policy_ids: Tuple[str, ...]
    policy_application_plan_ref: str
    previous_state_ref: str | None
    transition_result: Dict[str, Any]
    trace_ref: str
    replay_key: str
    candidate_only: bool = True
    fact_admitted: bool = False
    persisted: bool = False


@dataclass(frozen=True)
class StateReductionTrace:
    trace_id: str
    evaluation_refs: Tuple[str, ...]
    selection_refs: Tuple[str, ...]
    application_steps: Tuple[Dict[str, Any], ...]
    state_reduction_steps: Tuple[Dict[str, Any], ...]
    transition_steps: Tuple[Dict[str, Any], ...]
    conflict_decisions: Tuple[Dict[str, Any], ...]
    overlay_decisions: Tuple[Dict[str, Any], ...]
    rejected_operations: Tuple[str, ...]
    version_snapshots: Dict[str, str]
    resulting_candidate_hash: str
    replay_key: str


@dataclass(frozen=True)
class StateReductionResult:
    reducer_run_id: str
    field_id: str
    state_type: str
    reduction_status: str
    handoff_status: str
    selected_policy_ids: Tuple[str, ...]
    policy_application_plan: PolicyApplicationPlan
    state_candidate: FieldStateCandidate | None
    transition_result: StateTransitionResult
    conflict_result: ConflictReductionResult
    overlay_result: OverlayReductionResult
    rejection_reasons: Tuple[str, ...]
    trace_ref: str
    replay_key: str
    version_snapshots: Dict[str, str]
    real_state_store_write_implemented: bool = False
    fact_admission_implemented: bool = False
    action_trigger_implemented: bool = False
    runtime_implemented: bool = False
