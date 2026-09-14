from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class PolicySelectionInput:
    selection_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    evaluation_results: Tuple[Dict[str, Any], ...]
    policy_registry_version: str
    eligibility_matrix_version: str
    precedence_matrix_version: str
    composition_contract_version: str
    replay_contract_version: str


@dataclass(frozen=True)
class EligiblePolicyCandidate:
    evaluation_id: str
    policy_id: str
    policy_version: str
    precedence_class: str
    evaluation_status: str
    selection_candidate_allowed: bool
    input_order_index: int


@dataclass(frozen=True)
class PolicyPrecedenceResult:
    ordered_candidates: Tuple[EligiblePolicyCandidate, ...]
    ordered_policy_ids: Tuple[str, ...]
    excluded_policy_ids: Tuple[str, ...]
    precedence_steps: Tuple[Dict[str, Any], ...]
    unresolved: bool
    rejection_reasons: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PolicyExclusionResult:
    kept_candidates: Tuple[EligiblePolicyCandidate, ...]
    excluded_policy_ids: Tuple[str, ...]
    exclusion_steps: Tuple[Dict[str, Any], ...]
    unresolved: bool
    rejection_reasons: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PolicyCompositionCandidate:
    policy_ids: Tuple[str, ...]
    composition_sequence: Tuple[str, ...]
    eligible: bool
    reason: str | None = None


@dataclass(frozen=True)
class PolicySelectionStatus:
    status_id: str
    terminal: bool
    selected: bool


@dataclass(frozen=True)
class PolicySelectionTrace:
    trace_id: str
    input_evaluation_ids: Tuple[str, ...]
    eligible_policy_ids: Tuple[str, ...]
    rejected_policy_ids: Tuple[str, ...]
    ordered_policy_ids: Tuple[str, ...]
    excluded_policy_ids: Tuple[str, ...]
    selected_policy_ids: Tuple[str, ...]
    composition_sequence: Tuple[str, ...]
    precedence_steps: Tuple[Dict[str, Any], ...]
    exclusion_steps: Tuple[Dict[str, Any], ...]
    tie_break_steps: Tuple[Dict[str, Any], ...]
    rejection_reasons: Tuple[str, ...]
    selection_status: str
    snapshot_versions: Dict[str, str]
    replay_key: str


@dataclass(frozen=True)
class PolicySelectionReplayKey:
    replay_key: str
    snapshot_versions: Dict[str, str]


@dataclass(frozen=True)
class PolicySelectionResult:
    selection_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    input_evaluation_ids: Tuple[str, ...]
    eligible_policy_ids: Tuple[str, ...]
    rejected_policy_ids: Tuple[str, ...]
    ordered_policy_ids: Tuple[str, ...]
    excluded_policy_ids: Tuple[str, ...]
    selected_policy_ids: Tuple[str, ...]
    composition_sequence: Tuple[str, ...]
    precedence_steps: Tuple[Dict[str, Any], ...]
    exclusion_steps: Tuple[Dict[str, Any], ...]
    tie_break_steps: Tuple[Dict[str, Any], ...]
    rejection_reasons: Tuple[str, ...]
    selection_status: str
    replay_key: str
    evaluated_contract_versions: Dict[str, str]
    selection_trace_ref: str
    policy_execution_executed: bool = False
    state_mutation_executed: bool = False
    fact_promotion_executed: bool = False
    action_trigger_executed: bool = False
    runtime_execution: bool = False
