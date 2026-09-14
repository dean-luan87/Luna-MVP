# -*- coding: utf-8 -*-
"""Field State Reducer controlled dryrun types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class FieldStateReducerDryRunCaseV1:
    case_id: str
    case_type: str
    fixture_refs: Tuple[str, ...]
    input_overrides: Dict[str, Any] = field(default_factory=dict)
    expected_validation: bool = True
    expected_error_code: Optional[str] = None
    expected_reduction_decision: str = "skeleton_no_state_change"
    expected_resulting_state: Optional[Dict[str, Any]] = None
    expected_state_mutation_executed: bool = False
    expected_runtime_execution: bool = False
    deterministic_comparison_required: bool = False


@dataclass(frozen=True)
class FieldStateReducerDeterminismComparisonV1:
    case_id: str
    baseline_case_id: str
    compared_case_id: str
    compared_fields: Tuple[str, ...]
    excluded_fields: Tuple[str, ...]
    passed: bool
    differences: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class FieldStateReducerBoundaryObservationV1:
    state_mutation_executed: bool
    runtime_execution: bool
    database_access_executed: bool
    provider_recall_executed: bool
    external_lookup_executed: bool
    model_call_executed: bool
    action_trigger_executed: bool
    resulting_active_state_created: bool


@dataclass(frozen=True)
class FieldStateReducerDryRunCaseResultV1:
    case_id: str
    case_type: str
    validation_passed: bool
    skeleton_called: bool
    structured_error_codes: Tuple[str, ...]
    reduction_decision: Optional[str]
    resulting_state: Optional[Dict[str, Any]]
    ordered_event_ids: Tuple[str, ...]
    accepted_event_ids: Tuple[str, ...]
    rejected_event_ids: Tuple[str, ...]
    ignored_event_ids: Tuple[str, ...]
    conflict_ids: Tuple[str, ...]
    replay_key: Optional[str]
    state_change_type: Optional[str]
    boundary: FieldStateReducerBoundaryObservationV1
    unhandled_exception: Optional[str] = None


@dataclass(frozen=True)
class FieldStateReducerDryRunReportV1:
    phase: str
    stage: str
    total_cases: int
    positive_cases_passed: int
    negative_cases_passed: int
    unhandled_exceptions: int
    deterministic_comparison_passed: bool
    fixture_immutability_passed: bool
    resulting_active_states_created: int
    state_mutations_executed: int
    case_results: Tuple[FieldStateReducerDryRunCaseResultV1, ...]
    determinism_comparisons: Tuple[FieldStateReducerDeterminismComparisonV1, ...]
