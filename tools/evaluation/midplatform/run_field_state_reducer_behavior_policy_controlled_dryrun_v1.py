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

from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_controlled_dryrun_cases_v1 import (  # noqa: E402
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_controlled_dryrun_types_v1 import (  # noqa: E402
    BehaviorPolicyBoundaryObservationV1,
    BehaviorPolicyDeterminismComparisonV1,
    BehaviorPolicyDryRunCaseResultV1,
    BehaviorPolicyDryRunReportV1,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_decision_skeleton_v1 import (  # noqa: E402
    build_behavior_policy_decision_skeleton,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_fixture_v1 import (  # noqa: E402
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_FIXTURES_V1,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_registry_skeleton_v1 import (  # noqa: E402
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_static_validators_v1 import (  # noqa: E402
    validate_no_action_trigger_request,
    validate_no_external_lookup_request,
    validate_no_fact_promotion_request,
    validate_no_provider_recall_request,
    validate_no_runtime_request,
    validate_no_state_write_request,
    validate_policy_ids_known,
    validate_policy_registry_complete,
    validate_policy_snapshots_present,
    validate_state_type_known,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_policy_composition_skeleton_v1 import (  # noqa: E402
    build_placeholder_composition_sequence,
    composition_execution_executed,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_policy_eligibility_skeleton_v1 import (  # noqa: E402
    BehaviorPolicyEligibilityInputV1,
    build_placeholder_eligibility_results,
    list_candidate_policies,
    validate_eligibility_input,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_policy_precedence_skeleton_v1 import (  # noqa: E402
    build_placeholder_precedence_sequence,
    precedence_execution_executed,
)

CORE_DETERMINISTIC_FIELDS: Tuple[str, ...] = (
    "candidate_policy_ids",
    "eligible_policy_ids",
    "rejected_policy_ids",
    "selected_policy_ids",
    "precedence_steps",
    "composition_sequence",
    "decision_outcome",
    "resulting_state_candidate",
    "replay_key",
    "policy_execution_executed",
    "state_mutation_executed",
    "fact_promotion_executed",
    "action_trigger_executed",
    "runtime_execution",
)

NONDETERMINISTIC_EXCLUDED_FIELDS: Tuple[str, ...] = (
    "created_at",
    "run_id",
    "process_id",
    "memory_address",
    "wall_clock_duration",
)


def _fixture_map() -> Dict[str, Dict[str, Any]]:
    return {
        str(x.get("fixture_id", "")): dict(x)
        for x in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_FIXTURES_V1
        if isinstance(x, dict)
    }


def _policy_id_from_fixture(fixture: Dict[str, Any]) -> str:
    return str(fixture.get("policy_id", ""))


def _state_type_from_fixture(fixture: Dict[str, Any]) -> str:
    return str(fixture.get("state_type", ""))


def _build_snapshots(overrides: Dict[str, Any]) -> Dict[str, Any]:
    snapshots = {
        "policy_registry_snapshot": "v1",
        "eligibility_matrix_snapshot": "v1",
        "precedence_snapshot": "v1",
        "composition_snapshot": "v1",
    }
    snapshots.update(dict(overrides.get("snapshot_overrides", {})))
    return snapshots


def _first_error_from_issues(issues: Tuple[str, ...]) -> str:
    if not issues:
        return ""
    first = issues[0]
    mapping = {
        "missing_policy_registry_snapshot": "missing_policy_registry_snapshot",
        "missing_eligibility_matrix_snapshot": "missing_eligibility_matrix_snapshot",
        "missing_precedence_snapshot": "missing_precedence_snapshot",
        "missing_composition_snapshot": "missing_composition_snapshot",
        "runtime_execution_forbidden": "runtime_execution_forbidden",
        "direct_state_write_forbidden": "direct_state_write_forbidden",
        "fact_promotion_forbidden": "fact_promotion_forbidden",
        "action_trigger_forbidden": "action_trigger_forbidden",
        "provider_recall_forbidden": "provider_recall_forbidden",
        "external_lookup_forbidden": "external_lookup_forbidden",
        "unknown_state_type": "unknown_state_type",
    }
    if first.startswith("unknown_policy_id:"):
        return "unknown_policy_id"
    return mapping.get(first, first)


def _boundary_from_decision() -> BehaviorPolicyBoundaryObservationV1:
    return BehaviorPolicyBoundaryObservationV1(
        policy_execution_executed=False,
        precedence_execution_executed=bool(precedence_execution_executed),
        composition_execution_executed=bool(composition_execution_executed),
        confidence_aggregation_executed=False,
        conflict_resolution_executed=False,
        active_state_created=False,
        state_mutation_executed=False,
        fact_promotion_executed=False,
        action_trigger_executed=False,
        runtime_execution=False,
    )


def _core_payload(result: BehaviorPolicyDryRunCaseResultV1) -> Dict[str, Any]:
    return {
        "candidate_policy_ids": tuple(result.candidate_policy_ids),
        "eligible_policy_ids": tuple(result.eligible_policy_ids),
        "rejected_policy_ids": tuple(result.rejected_policy_ids),
        "selected_policy_ids": tuple(result.selected_policy_ids),
        "precedence_steps": tuple(
            tuple(sorted(step.items())) for step in result.precedence_steps
        ),
        "composition_sequence": tuple(result.composition_sequence),
        "decision_outcome": result.decision_outcome,
        "resulting_state_candidate": result.resulting_state_candidate,
        "replay_key": result.replay_key,
        "policy_execution_executed": result.boundary.policy_execution_executed,
        "state_mutation_executed": result.boundary.state_mutation_executed,
        "fact_promotion_executed": result.boundary.fact_promotion_executed,
        "action_trigger_executed": result.boundary.action_trigger_executed,
        "runtime_execution": result.boundary.runtime_execution,
    }


def _execute_case(
    case: Any, fixture_map: Dict[str, Dict[str, Any]]
) -> BehaviorPolicyDryRunCaseResultV1:
    fixtures = [copy.deepcopy(fixture_map[r]) for r in case.fixture_refs]
    state_type = str(
        case.input_overrides.get("state_type") or _state_type_from_fixture(fixtures[0])
    )

    candidate_policy_ids = tuple(
        str(x)
        for x in case.input_overrides.get(
            "candidate_policy_ids",
            tuple(_policy_id_from_fixture(f) for f in fixtures),
        )
    )

    ok, issues = validate_policy_registry_complete(
        FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
    )
    if not ok:
        return BehaviorPolicyDryRunCaseResultV1(
            case_id=case.case_id,
            category=case.category,
            validation_passed=False,
            skeleton_called=False,
            structured_error_code="missing_policy_registry_snapshot",
            decision_outcome=None,
            boundary=_boundary_from_decision(),
        )

    ok, issues = validate_state_type_known(state_type)
    if not ok:
        return BehaviorPolicyDryRunCaseResultV1(
            case_id=case.case_id,
            category=case.category,
            validation_passed=False,
            skeleton_called=False,
            structured_error_code="unknown_state_type",
            decision_outcome=None,
            boundary=_boundary_from_decision(),
        )

    ok, issues = validate_policy_ids_known(candidate_policy_ids)
    if not ok:
        return BehaviorPolicyDryRunCaseResultV1(
            case_id=case.case_id,
            category=case.category,
            validation_passed=False,
            skeleton_called=False,
            structured_error_code="unknown_policy_id",
            decision_outcome=None,
            boundary=_boundary_from_decision(),
        )

    snapshots = _build_snapshots(case.input_overrides)
    ok, issues = validate_policy_snapshots_present(snapshots)
    if not ok:
        return BehaviorPolicyDryRunCaseResultV1(
            case_id=case.case_id,
            category=case.category,
            validation_passed=False,
            skeleton_called=False,
            structured_error_code=_first_error_from_issues(issues),
            decision_outcome=None,
            boundary=_boundary_from_decision(),
        )

    for fn in (
        validate_no_runtime_request,
        validate_no_state_write_request,
        validate_no_fact_promotion_request,
        validate_no_action_trigger_request,
        validate_no_provider_recall_request,
        validate_no_external_lookup_request,
    ):
        ok, issues = fn(case.input_overrides)
        if not ok:
            return BehaviorPolicyDryRunCaseResultV1(
                case_id=case.case_id,
                category=case.category,
                validation_passed=False,
                skeleton_called=False,
                structured_error_code=_first_error_from_issues(issues),
                decision_outcome=None,
                boundary=_boundary_from_decision(),
            )

    eligibility_input = BehaviorPolicyEligibilityInputV1(
        state_type=state_type,
        admitted_field_events=tuple(fixtures),
        temporal_snapshot={"snapshot": "v1"},
        no_provider_recall=True,
        no_external_lookup=True,
        no_action_trigger=True,
    )
    ok, issues = validate_eligibility_input(eligibility_input)
    if not ok:
        return BehaviorPolicyDryRunCaseResultV1(
            case_id=case.case_id,
            category=case.category,
            validation_passed=False,
            skeleton_called=False,
            structured_error_code=_first_error_from_issues(issues),
            decision_outcome=None,
            boundary=_boundary_from_decision(),
        )

    canonical_candidates = tuple(sorted(list_candidate_policies(state_type)))
    eligibility_rows = build_placeholder_eligibility_results(canonical_candidates)
    eligible_policy_ids = tuple(row.policy_id for row in eligibility_rows)
    rejected_policy_ids: Tuple[str, ...] = tuple()
    precedence_sequence = build_placeholder_precedence_sequence(eligible_policy_ids)
    composition_sequence = build_placeholder_composition_sequence(precedence_sequence)

    decision, trace = build_behavior_policy_decision_skeleton(
        field_id=str(case.input_overrides.get("field_id", "field_dryrun_v1")),
        state_type=state_type,
        temporal_inputs=dict(
            case.input_overrides.get("temporal_inputs", {"status": "active"})
        ),
        confidence_inputs=dict(
            case.input_overrides.get("confidence_inputs", {"mode": "dryrun"})
        ),
        conflict_inputs=dict(
            case.input_overrides.get("conflict_inputs", {"mode": "preserve"})
        ),
        owner_correction_inputs=dict(
            case.input_overrides.get(
                "owner_correction_inputs", {"candidate_only": True}
            )
        ),
        overlay_inputs=dict(
            case.input_overrides.get("overlay_inputs", {"layered": True})
        ),
    )

    return BehaviorPolicyDryRunCaseResultV1(
        case_id=case.case_id,
        category=case.category,
        validation_passed=True,
        skeleton_called=True,
        structured_error_code=None,
        decision_outcome=decision.decision_outcome,
        selected_policy_ids=tuple(decision.selected_policy_ids),
        resulting_state_candidate=decision.resulting_state_candidate,
        replay_key=trace.replay_key,
        precedence_steps=tuple(
            {
                "higher_policy": step.higher_policy,
                "lower_policy": step.lower_policy,
                "applied": step.applied,
            }
            for step in trace.precedence_steps
        ),
        composition_sequence=composition_sequence,
        candidate_policy_ids=canonical_candidates,
        eligible_policy_ids=eligible_policy_ids,
        rejected_policy_ids=rejected_policy_ids,
        boundary=BehaviorPolicyBoundaryObservationV1(
            policy_execution_executed=decision.policy_execution_executed,
            precedence_execution_executed=False,
            composition_execution_executed=False,
            confidence_aggregation_executed=False,
            conflict_resolution_executed=False,
            active_state_created=False,
            state_mutation_executed=decision.state_mutation_executed,
            fact_promotion_executed=decision.fact_promotion_executed,
            action_trigger_executed=decision.action_trigger_executed,
            runtime_execution=decision.runtime_execution,
        ),
    )


def run_field_state_reducer_behavior_policy_controlled_dryrun_v1() -> Dict[str, Any]:
    fixture_map = _fixture_map()
    fixture_before = copy.deepcopy(FIELD_STATE_REDUCER_BEHAVIOR_POLICY_FIXTURES_V1)
    registry_before = copy.deepcopy(
        FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
    )

    case_results: List[BehaviorPolicyDryRunCaseResultV1] = []
    unhandled_exceptions = 0

    for case in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1:
        try:
            case_results.append(_execute_case(case, fixture_map))
        except Exception:
            unhandled_exceptions += 1
            case_results.append(
                BehaviorPolicyDryRunCaseResultV1(
                    case_id=case.case_id,
                    category=case.category,
                    validation_passed=False,
                    skeleton_called=False,
                    structured_error_code="invalid_policy_input",
                    decision_outcome=None,
                    boundary=_boundary_from_decision(),
                )
            )

    by_case = {r.case_id: r for r in case_results}
    repeated_a = by_case.get("repeated_identical_input_case")
    repeated_b = _execute_case(
        next(
            c
            for c in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1
            if c.case_id == "repeated_identical_input_case"
        ),
        fixture_map,
    )

    mismatches: List[str] = []
    if repeated_a and repeated_b:
        payload_a = _core_payload(repeated_a)
        payload_b = _core_payload(repeated_b)
        for field_name in CORE_DETERMINISTIC_FIELDS:
            if payload_a[field_name] != payload_b[field_name]:
                mismatches.append(field_name)

    reversed_case = by_case.get("reversed_candidate_order_case")
    reversed_passed = False
    if reversed_case and repeated_a:
        reversed_passed = (
            tuple(reversed_case.candidate_policy_ids)
            == tuple(repeated_a.candidate_policy_ids)
            and reversed_case.replay_key == repeated_a.replay_key
        )

    determinism = BehaviorPolicyDeterminismComparisonV1(
        case_id="repeated_identical_input_case",
        core_fields=CORE_DETERMINISTIC_FIELDS,
        excluded_nondeterministic_fields=NONDETERMINISTIC_EXCLUDED_FIELDS,
        passed=len(mismatches) == 0,
        mismatch_fields=tuple(mismatches),
    )

    fixture_immutability_passed = (
        fixture_before == FIELD_STATE_REDUCER_BEHAVIOR_POLICY_FIXTURES_V1
    )
    registry_immutability_passed = (
        registry_before == FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
    )

    positive_total = sum(
        1
        for c in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1
        if c.category == "positive"
    )
    negative_total = sum(
        1
        for c in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1
        if c.category == "negative"
    )

    positive_passed = 0
    negative_passed = 0
    failed_cases: List[str] = []

    for case in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1:
        row = by_case.get(case.case_id)
        passed = True
        if row is None:
            passed = False
        elif row.validation_passed != case.expected_validation:
            passed = False
        elif row.structured_error_code != case.expected_error_code:
            passed = False
        elif row.decision_outcome != case.expected_decision_outcome:
            passed = False
        elif tuple(row.selected_policy_ids) != tuple(case.expected_selected_policy_ids):
            passed = False
        elif row.resulting_state_candidate != case.expected_resulting_state_candidate:
            passed = False
        elif (
            row.boundary.policy_execution_executed
            != case.expected_policy_execution_executed
        ):
            passed = False
        elif (
            row.boundary.state_mutation_executed
            != case.expected_state_mutation_executed
        ):
            passed = False
        elif row.boundary.runtime_execution != case.expected_runtime_execution:
            passed = False

        if case.category == "positive":
            positive_passed += 1 if passed else 0
        else:
            negative_passed += 1 if passed else 0

        if not passed:
            failed_cases.append(case.case_id)

    active_states_created = 0
    state_mutations_executed = sum(
        1 for r in case_results if r.boundary.state_mutation_executed
    )

    report = BehaviorPolicyDryRunReportV1(
        phase="Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-DryRun-v1-001",
        stage="Behavior Policy Controlled DryRun",
        dryrun_only=True,
        total_cases=len(FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_CASES_V1),
        positive_total=positive_total,
        negative_total=negative_total,
        positive_passed=positive_passed,
        negative_passed=negative_passed,
        failed_cases=tuple(failed_cases),
        unhandled_exceptions=unhandled_exceptions,
        deterministic_comparison=determinism,
        reversed_candidate_order_passed=reversed_passed,
        fixture_immutability_passed=fixture_immutability_passed,
        registry_immutability_passed=registry_immutability_passed,
        active_states_created=active_states_created,
        state_mutations_executed=state_mutations_executed,
        case_results=tuple(case_results),
    )

    payload = asdict(report)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run_field_state_reducer_behavior_policy_controlled_dryrun_v1()
