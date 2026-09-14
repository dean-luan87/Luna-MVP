# -*- coding: utf-8 -*-
"""Run Field State Reducer controlled dryrun v1."""

from __future__ import annotations

import copy
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.field_state_reducer_controlled_dryrun_cases_v1 import (
    FIELD_STATE_REDUCER_CONTROLLED_DRYRUN_CASES_V1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_controlled_dryrun_types_v1 import (
    FieldStateReducerBoundaryObservationV1,
    FieldStateReducerDeterminismComparisonV1,
    FieldStateReducerDryRunCaseResultV1,
    FieldStateReducerDryRunReportV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_fixture_v1 import (
    FIELD_STATE_REDUCER_FIXTURES_V1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_skeleton_v1 import (
    FieldStateReducerSkeletonV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_static_validators_v1 import (
    validate_reducer_input_contract,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_types_v1 import (
    FieldStateReducerConfigSnapshotV1,
    FieldStateReducerInputV1,
    FieldStateReducerVersionSnapshotV1,
)

DETERMINISTIC_FIELDS: Tuple[str, ...] = (
    "ordered_event_ids",
    "reduction_decision",
    "resulting_state",
    "state_change_type",
    "replay_key",
    "accepted_event_ids",
    "rejected_event_ids",
    "ignored_event_ids",
    "conflict_ids",
    "state_mutation_executed",
    "runtime_execution",
)
EXCLUDED_NONDETERMINISTIC_FIELDS: Tuple[str, ...] = (
    "created_at",
    "reducer_run_id",
    "process_id",
    "memory_address",
    "wall_clock_duration",
)

FIELD_ACCESSOR_MAP = {
    "state_mutation_executed": lambda r: r.boundary.state_mutation_executed,
    "runtime_execution": lambda r: r.boundary.runtime_execution,
}


def _event_key(event: Dict[str, Any]) -> str:
    return str(event.get("event_type", ""))


def _fixture_registry_map() -> Dict[str, Dict[str, Any]]:
    return {_event_key(e): dict(e) for e in FIELD_STATE_REDUCER_FIXTURES_V1}


def _normalize_error_codes(issues: Tuple[str, ...]) -> Tuple[str, ...]:
    normalized: List[str] = []
    for issue in issues:
        if issue.startswith("event_not_admitted:"):
            normalized.append("non_admitted_event_not_allowed")
            continue
        if issue.startswith("raw_observation_not_allowed:"):
            normalized.append("raw_observation_not_allowed")
            continue
        if issue in ("missing_event_id", "duplicate_event_id"):
            normalized.append("unstable_event_order")
            continue
        if issue.startswith("missing_") and issue in (
            "missing_reducer_version",
            "missing_reduction_policy_version",
            "missing_registry_version",
        ):
            normalized.append("missing_version_snapshot")
            continue
        normalized.append(issue)
    deduped = []
    for code in normalized:
        if code not in deduped:
            deduped.append(code)
    return tuple(deduped)


def _build_input_events(
    fixture_map: Dict[str, Dict[str, Any]],
    fixture_refs: Tuple[str, ...],
    overrides: Dict[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    events = [copy.deepcopy(fixture_map[ref]) for ref in fixture_refs]
    if overrides.get("set_first_event_admitted") is False and events:
        events[0]["admitted"] = False
    if overrides.get("set_first_event_raw_observation") is True and events:
        events[0]["raw_observation"] = True
    if "duplicate_event_id" in overrides and len(events) >= 2:
        events[0]["event_id"] = str(overrides["duplicate_event_id"])
        events[1]["event_id"] = str(overrides["duplicate_event_id"])
    return tuple(events)


def _build_reducer_input(
    case_id: str, events: Tuple[Dict[str, Any], ...], overrides: Dict[str, Any]
) -> FieldStateReducerInputV1:
    temporal_snapshot = overrides.get(
        "temporal_snapshot",
        {
            "snapshot_id": "temporal_snapshot_xiaobeimen_dryrun_v1",
            "scope": "field_state_reducer_controlled_dryrun",
            "synthetic": True,
        },
    )
    version_snapshot = overrides.get(
        "version_snapshot",
        FieldStateReducerVersionSnapshotV1(
            reducer_version="field_state_reducer_skeleton_v1",
            reduction_policy_version="v1",
            registry_version="v1",
            configuration_snapshot_ref="cfg_dryrun_v1",
        ),
    )
    return FieldStateReducerInputV1(
        admitted_field_events=events,
        temporal_validity_snapshot=temporal_snapshot,
        reducer_config_snapshot=FieldStateReducerConfigSnapshotV1(
            reduction_policy_version="v1",
            event_type_registry_version="v1",
            conflict_resolution_matrix_version="v1",
            deterministic_evaluation_timestamp="2026-07-15T00:00:00Z",
        ),
        reducer_version_snapshot=version_snapshot,
        direct_state_mutation_requested=bool(
            overrides.get("direct_state_mutation_requested", False)
        ),
        skeleton_only=True,
        no_external_lookup=bool(overrides.get("no_external_lookup", True)),
        no_provider_recall=bool(overrides.get("no_provider_recall", True)),
        no_action_trigger=bool(overrides.get("no_action_trigger", True)),
    )


def _extract_result_payload(output: Any) -> Dict[str, Any]:
    return {
        "reduction_decision": output.reduction_decision,
        "resulting_state": output.resulting_state,
        "ordered_event_ids": tuple(
            output.reducer_trace.get("ordered_event_ids", tuple())
        ),
        "accepted_event_ids": tuple(output.applied_event_ids),
        "rejected_event_ids": tuple(output.rejected_event_ids),
        "ignored_event_ids": tuple(output.ignored_event_ids),
        "conflict_ids": tuple(output.conflict_ids),
        "replay_key": output.deterministic_replay_key,
        "state_change_type": output.state_change_type,
        "state_mutation_executed": output.state_mutation_executed,
        "runtime_execution": output.runtime_executed,
    }


def _get_result_field(
    result_obj: FieldStateReducerDryRunCaseResultV1, field_name: str
) -> Any:
    accessor = FIELD_ACCESSOR_MAP.get(field_name)
    if accessor is not None:
        return accessor(result_obj)
    return getattr(result_obj, field_name)


def run_field_state_reducer_controlled_dryrun_v1() -> Dict[str, Any]:
    reducer = FieldStateReducerSkeletonV1()
    fixture_map = _fixture_registry_map()
    fixture_snapshot_before = copy.deepcopy(FIELD_STATE_REDUCER_FIXTURES_V1)

    case_results: List[FieldStateReducerDryRunCaseResultV1] = []
    unhandled_exceptions = 0

    for case in FIELD_STATE_REDUCER_CONTROLLED_DRYRUN_CASES_V1:
        try:
            events = _build_input_events(
                fixture_map, case.fixture_refs, case.input_overrides
            )
            reducer_input = _build_reducer_input(
                case.case_id, events, case.input_overrides
            )

            contract_ok, contract_issues = validate_reducer_input_contract(
                reducer_input
            )
            valid, issues = reducer.validate_input(reducer_input)
            normalized_codes = _normalize_error_codes(contract_issues + issues)

            if valid and contract_ok and case.expected_validation:
                output = reducer.reduce(reducer_input)
                payload = _extract_result_payload(output)
                case_result = FieldStateReducerDryRunCaseResultV1(
                    case_id=case.case_id,
                    case_type=case.case_type,
                    validation_passed=True,
                    skeleton_called=True,
                    structured_error_codes=tuple(),
                    reduction_decision=payload["reduction_decision"],
                    resulting_state=payload["resulting_state"],
                    ordered_event_ids=payload["ordered_event_ids"],
                    accepted_event_ids=payload["accepted_event_ids"],
                    rejected_event_ids=payload["rejected_event_ids"],
                    ignored_event_ids=payload["ignored_event_ids"],
                    conflict_ids=payload["conflict_ids"],
                    replay_key=payload["replay_key"],
                    state_change_type=payload["state_change_type"],
                    boundary=FieldStateReducerBoundaryObservationV1(
                        state_mutation_executed=payload["state_mutation_executed"],
                        runtime_execution=payload["runtime_execution"],
                        database_access_executed=False,
                        provider_recall_executed=False,
                        external_lookup_executed=False,
                        model_call_executed=False,
                        action_trigger_executed=False,
                        resulting_active_state_created=payload["resulting_state"]
                        is not None,
                    ),
                )
            else:
                case_result = FieldStateReducerDryRunCaseResultV1(
                    case_id=case.case_id,
                    case_type=case.case_type,
                    validation_passed=False,
                    skeleton_called=False,
                    structured_error_codes=normalized_codes,
                    reduction_decision=None,
                    resulting_state=None,
                    ordered_event_ids=tuple(),
                    accepted_event_ids=tuple(),
                    rejected_event_ids=tuple(),
                    ignored_event_ids=tuple(),
                    conflict_ids=tuple(),
                    replay_key=None,
                    state_change_type=None,
                    boundary=FieldStateReducerBoundaryObservationV1(
                        state_mutation_executed=False,
                        runtime_execution=False,
                        database_access_executed=False,
                        provider_recall_executed=False,
                        external_lookup_executed=False,
                        model_call_executed=False,
                        action_trigger_executed=False,
                        resulting_active_state_created=False,
                    ),
                )
            case_results.append(case_result)
        except Exception as exc:
            unhandled_exceptions += 1
            case_results.append(
                FieldStateReducerDryRunCaseResultV1(
                    case_id=case.case_id,
                    case_type=case.case_type,
                    validation_passed=False,
                    skeleton_called=False,
                    structured_error_codes=tuple(),
                    reduction_decision=None,
                    resulting_state=None,
                    ordered_event_ids=tuple(),
                    accepted_event_ids=tuple(),
                    rejected_event_ids=tuple(),
                    ignored_event_ids=tuple(),
                    conflict_ids=tuple(),
                    replay_key=None,
                    state_change_type=None,
                    boundary=FieldStateReducerBoundaryObservationV1(
                        state_mutation_executed=False,
                        runtime_execution=False,
                        database_access_executed=False,
                        provider_recall_executed=False,
                        external_lookup_executed=False,
                        model_call_executed=False,
                        action_trigger_executed=False,
                        resulting_active_state_created=False,
                    ),
                    unhandled_exception=f"{type(exc).__name__}: {exc}",
                )
            )

    by_case = {r.case_id: r for r in case_results}
    comparisons: List[FieldStateReducerDeterminismComparisonV1] = []
    for case_id in ("repeated_identical_input_case", "reversed_input_order_case"):
        left = by_case.get("baseline_all_fixtures_case")
        right = by_case.get(case_id)
        diffs: List[str] = []
        if left is None or right is None:
            diffs.append("missing_case_result")
        else:
            for field_name in DETERMINISTIC_FIELDS:
                if _get_result_field(left, field_name) != _get_result_field(
                    right, field_name
                ):
                    diffs.append(field_name)
        comparisons.append(
            FieldStateReducerDeterminismComparisonV1(
                case_id=f"determinism_compare_{case_id}",
                baseline_case_id="baseline_all_fixtures_case",
                compared_case_id=case_id,
                compared_fields=DETERMINISTIC_FIELDS,
                excluded_fields=EXCLUDED_NONDETERMINISTIC_FIELDS,
                passed=len(diffs) == 0,
                differences=tuple(diffs),
            )
        )

    fixture_snapshot_after = copy.deepcopy(FIELD_STATE_REDUCER_FIXTURES_V1)
    fixture_immutability_passed = fixture_snapshot_before == fixture_snapshot_after

    positive_passed = 0
    negative_passed = 0
    active_state_created_count = 0
    state_mutations_executed_count = 0

    for case in FIELD_STATE_REDUCER_CONTROLLED_DRYRUN_CASES_V1:
        result = by_case[case.case_id]
        if result.boundary.resulting_active_state_created:
            active_state_created_count += 1
        if result.boundary.state_mutation_executed:
            state_mutations_executed_count += 1

        case_ok = True
        if case.expected_validation != result.validation_passed:
            case_ok = False
        if (
            case.expected_error_code
            and case.expected_error_code not in result.structured_error_codes
        ):
            case_ok = False
        if case.expected_validation:
            if result.reduction_decision != case.expected_reduction_decision:
                case_ok = False
            if result.resulting_state is not case.expected_resulting_state:
                case_ok = False
        if (
            result.boundary.state_mutation_executed
            != case.expected_state_mutation_executed
        ):
            case_ok = False
        if result.boundary.runtime_execution != case.expected_runtime_execution:
            case_ok = False

        if case.case_type == "positive" and case_ok:
            positive_passed += 1
        if case.case_type == "negative" and case_ok:
            negative_passed += 1

    deterministic_passed = all(c.passed for c in comparisons)

    report = FieldStateReducerDryRunReportV1(
        phase="Phase-Luna-Field-State-Reducer-Controlled-DryRun-v1-001",
        stage="Controlled DryRun",
        total_cases=len(FIELD_STATE_REDUCER_CONTROLLED_DRYRUN_CASES_V1),
        positive_cases_passed=positive_passed,
        negative_cases_passed=negative_passed,
        unhandled_exceptions=unhandled_exceptions,
        deterministic_comparison_passed=deterministic_passed,
        fixture_immutability_passed=fixture_immutability_passed,
        resulting_active_states_created=active_state_created_count,
        state_mutations_executed=state_mutations_executed_count,
        case_results=tuple(case_results),
        determinism_comparisons=tuple(comparisons),
    )

    return {
        "phase": report.phase,
        "stage": report.stage,
        "dryrun_only": True,
        "total_cases": report.total_cases,
        "positive_cases_passed": report.positive_cases_passed,
        "negative_cases_passed": report.negative_cases_passed,
        "unhandled_exceptions": report.unhandled_exceptions,
        "deterministic_comparison_passed": report.deterministic_comparison_passed,
        "fixture_immutability_passed": report.fixture_immutability_passed,
        "resulting_active_states_created": report.resulting_active_states_created,
        "state_mutations_executed": report.state_mutations_executed,
        "case_results": [asdict(i) for i in report.case_results],
        "determinism_comparisons": [asdict(i) for i in report.determinism_comparisons],
    }


def main() -> int:
    report = run_field_state_reducer_controlled_dryrun_v1()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
