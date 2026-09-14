from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class BehaviorPolicyDryRunCaseV1:
    case_id: str
    category: str
    fixture_refs: Tuple[str, ...]
    input_overrides: Dict[str, Any]
    expected_validation: bool
    expected_error_code: Optional[str]
    expected_decision_outcome: Optional[str]
    expected_selected_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    expected_resulting_state_candidate: Any = None
    expected_policy_execution_executed: bool = False
    expected_state_mutation_executed: bool = False
    expected_runtime_execution: bool = False
    deterministic_comparison_required: bool = False


@dataclass(frozen=True)
class BehaviorPolicyBoundaryObservationV1:
    policy_execution_executed: bool = False
    precedence_execution_executed: bool = False
    composition_execution_executed: bool = False
    confidence_aggregation_executed: bool = False
    conflict_resolution_executed: bool = False
    active_state_created: bool = False
    state_mutation_executed: bool = False
    fact_promotion_executed: bool = False
    action_trigger_executed: bool = False
    runtime_execution: bool = False


@dataclass(frozen=True)
class BehaviorPolicyDryRunCaseResultV1:
    case_id: str
    category: str
    validation_passed: bool
    skeleton_called: bool
    structured_error_code: Optional[str]
    decision_outcome: Optional[str]
    selected_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    resulting_state_candidate: Any = None
    replay_key: str = ""
    precedence_steps: Tuple[Dict[str, Any], ...] = field(default_factory=tuple)
    composition_sequence: Tuple[str, ...] = field(default_factory=tuple)
    candidate_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    eligible_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    rejected_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    boundary: BehaviorPolicyBoundaryObservationV1 = field(
        default_factory=BehaviorPolicyBoundaryObservationV1
    )


@dataclass(frozen=True)
class BehaviorPolicyDeterminismComparisonV1:
    case_id: str
    core_fields: Tuple[str, ...]
    excluded_nondeterministic_fields: Tuple[str, ...]
    passed: bool
    mismatch_fields: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class BehaviorPolicyDryRunReportV1:
    phase: str
    stage: str
    dryrun_only: bool
    total_cases: int
    positive_total: int
    negative_total: int
    positive_passed: int
    negative_passed: int
    failed_cases: Tuple[str, ...]
    unhandled_exceptions: int
    deterministic_comparison: BehaviorPolicyDeterminismComparisonV1
    reversed_candidate_order_passed: bool
    fixture_immutability_passed: bool
    registry_immutability_passed: bool
    active_states_created: int
    state_mutations_executed: int
    case_results: Tuple[BehaviorPolicyDryRunCaseResultV1, ...]
