from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from ..field_state_reducer_behavior_policy_trace_types_v1 import BehaviorPolicyTraceV1


@dataclass(frozen=True)
class EvaluationInput:
    evaluation_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    policy_id: str
    admitted_events: Tuple[Dict[str, Any], ...]
    existing_state_snapshot: Dict[str, Any]
    temporal_snapshot: Dict[str, Any]
    confidence_policy_snapshot: Dict[str, Any]
    conflict_snapshot: Dict[str, Any]
    owner_correction_snapshot: Dict[str, Any]
    overlay_snapshot: Dict[str, Any]
    provenance_snapshot: Dict[str, Any]
    governance_snapshot: Dict[str, Any]
    policy_registry_version: str
    eligibility_matrix_version: str
    evaluation_contract_version: str
    evaluation_requested_at: str
    runtime_state_dependency_requested: bool = False
    provider_recall_requested: bool = False
    external_lookup_requested: bool = False
    model_call_requested: bool = False
    state_write_requested: bool = False
    action_trigger_requested: bool = False


@dataclass(frozen=True)
class EvaluationStatus:
    status_id: str
    description: str
    terminal: bool
    selectable: bool
    selection_candidate_allowed: bool


@dataclass(frozen=True)
class ConditionRule:
    rule_id: str
    policy_id: str
    condition_type: str
    operator: str
    expected_value: Any
    input_path: str
    required: bool
    blocking: bool
    rejection_reason: str
    evaluation_order: int
    short_circuit_allowed: bool
    trace_required: bool
    candidate_only: bool = True
    fact_promotion_allowed: bool = False


@dataclass(frozen=True)
class ConditionResult:
    rule_id: str
    policy_id: str
    passed: bool
    blocking: bool
    missing_inputs: Tuple[str, ...] = field(default_factory=tuple)
    rejection_reason: Optional[str] = None
    actual_value: Any = None


@dataclass(frozen=True)
class EvidenceSufficiencyResult:
    status: str
    sufficient: bool
    missing_inputs: Tuple[str, ...] = field(default_factory=tuple)
    rejection_reasons: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemporalEvaluationResult:
    status: str
    support_eligible: bool
    blocking: bool
    refresh_required: bool
    new_event_required: bool
    rejection_reason: Optional[str] = None


@dataclass(frozen=True)
class ConfidenceEvaluationResult:
    status: str
    passed: bool
    measured_confidence: Optional[float]
    threshold: Optional[float]
    rejection_reason: Optional[str] = None


@dataclass(frozen=True)
class ConflictEvaluationResult:
    status: str
    unresolved: bool
    policy_eligibility_allowed: bool
    preserve_conflict: bool
    rejection_reason: Optional[str] = None


@dataclass(frozen=True)
class GovernanceEvaluationResult:
    status: str
    passed: bool
    missing_dependencies: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EvaluationReplayKey:
    replay_key: str
    snapshot_versions: Dict[str, str]


@dataclass(frozen=True)
class EvaluationTrace:
    trace_id: str
    evaluation_id: str
    policy_id: str
    ordered_rule_ids: Tuple[str, ...]
    evaluated_rule_ids: Tuple[str, ...]
    rule_results: Tuple[Dict[str, Any], ...]
    short_circuit_steps: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    confidence_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    rejection_reason_refs: Tuple[str, ...]
    snapshot_versions: Dict[str, str]
    replay_key: str
    created_at: str
    base_trace: Optional[BehaviorPolicyTraceV1] = None


@dataclass(frozen=True)
class PolicyEvaluationResult:
    evaluation_id: str
    policy_id: str
    state_type: str
    evaluation_status: str
    satisfied_rule_ids: Tuple[str, ...]
    unsatisfied_rule_ids: Tuple[str, ...]
    blocked_rule_ids: Tuple[str, ...]
    skipped_rule_ids: Tuple[str, ...]
    missing_input_fields: Tuple[str, ...]
    evidence_sufficiency_status: str
    temporal_evaluation_status: str
    confidence_evaluation_status: str
    conflict_evaluation_status: str
    governance_evaluation_status: str
    rejection_reasons: Tuple[str, ...]
    selection_candidate_allowed: bool
    evaluation_trace_ref: str
    replay_key: str
    evaluated_contract_versions: Dict[str, str]
    policy_selection_executed: bool = False
    policy_execution_executed: bool = False
    state_mutation_executed: bool = False
    fact_promotion_executed: bool = False
    action_trigger_executed: bool = False
    runtime_execution: bool = False
