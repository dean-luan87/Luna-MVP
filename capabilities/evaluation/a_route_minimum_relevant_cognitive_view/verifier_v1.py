"""Verifier for controlled minimum relevant Self/External view behavior."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _result(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("result") or {}


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = summary.get("cases") or []
    negative = summary.get("negative_cases") or []
    seat = _case(cases, "SAME_INFORMATION_DIFFERENT_GOAL:seat")
    exit_goal = _case(cases, "SAME_INFORMATION_DIFFERENT_GOAL:exit")
    irrelevant_external = _case(cases, "SAME_GOAL_IRRELEVANT_EXTERNAL_CHANGE")
    irrelevant_self = _case(cases, "SAME_GOAL_IRRELEVANT_SELF_CHANGE")
    relevant_self = _case(cases, "SAME_GOAL_RELEVANT_SELF_CHANGE")
    relevant_external = _case(cases, "SAME_GOAL_RELEVANT_EXTERNAL_CHANGE")
    owner = _case(cases, "SAME_GOAL_DIFFERENT_GOVERNED_ROLE:owner")
    visitor = _case(cases, "SAME_GOAL_DIFFERENT_GOVERNED_ROLE:visitor")
    reactivated_seat = _case(cases, "GOAL_CHANGE_REACTIVATES_EXCLUDED_INFORMATION:seat")
    reactivated_exit = _case(cases, "GOAL_CHANGE_REACTIVATES_EXCLUDED_INFORMATION:exit")

    seat_result = _result(seat)
    exit_result = _result(exit_goal)
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_A_ROUTE_MINIMUM_RELEVANT_COGNITIVE_VIEW_TEST")
    _check(checks, "goal_changes_selected_view", seat_result.get("selected_information_refs") != exit_result.get("selected_information_refs"))
    _check(checks, "self_and_external_selected", bool(seat_result.get("selected_self_information_refs")) and bool(seat_result.get("selected_external_information_refs")))
    _check(checks, "irrelevant_external_stable", _result(irrelevant_external).get("selected_information_refs") == seat_result.get("selected_information_refs"))
    _check(checks, "irrelevant_self_stable", _result(irrelevant_self).get("selected_information_refs") == seat_result.get("selected_information_refs"))
    _check(checks, "relevant_self_changes_view", _result(relevant_self).get("selected_information_refs") != seat_result.get("selected_information_refs"))
    _check(checks, "relevant_external_changes_view", _result(relevant_external).get("selected_information_refs") != seat_result.get("selected_information_refs"))
    _check(checks, "role_condition_changes_view", _result(owner).get("selected_information_refs") != _result(visitor).get("selected_information_refs"))
    _check(checks, "goal_reactivates_excluded", "external:exit:relation" in _result(reactivated_seat).get("excluded_information_refs", ()) and "external:exit:relation" in _result(reactivated_exit).get("selected_information_refs", ()))
    _check(checks, "excluded_is_recoverable", set(_result(reactivated_seat).get("excluded_information_refs", ())).issubset(set(_result(reactivated_seat).get("recoverable_information_refs", ()))))
    _check(checks, "coverage_equals_selected", seat_result.get("current_cognitive_coverage_refs") == seat_result.get("selected_information_refs"))
    _check(checks, "self_external_use_same_algorithm", summary.get("selection_algorithm") == "declared governed condition intersection; object type does not select")
    for name in (
        "candidate_only",
        "read_only",
        "truth_declared",
        "self_mutation",
        "field_mutation",
        "world_truth_declared",
        "memory_mutation",
        "pcn_mutation",
        "decision_execution",
        "task_execution",
        "action_execution",
        "provider_invocation",
        "model_invocation",
        "observation_execution",
        "observation_demand_formed",
        "scenario_id_semantic_driver",
        "opaque_context_semantic_guess",
    ):
        expected = True if name in {"candidate_only", "read_only"} else False
        _check(checks, f"positive:{name}", seat_result.get(name) is expected)
    _check(checks, "context_opaque_change_stable", _result(_case(cases, "SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE")).get("selected_information_refs") == seat_result.get("selected_information_refs"))
    for item in negative:
        result = _result(item)
        case_id = item.get("case_id")
        if case_id == "CANDIDATE_ONLY_REQUIRED":
            _check(checks, "negative_candidate_only_rejected", result.get("status") == "REJECTED")
        elif case_id == "DUPLICATE_INFORMATION_REJECTED":
            _check(checks, "negative_duplicate_rejected", result.get("status") == "REJECTED")
        elif case_id == "NO_GOVERNED_CONDITION_NO_SELECTION":
            _check(checks, "negative_no_condition_no_selection", result.get("status") == "NO_ACTIVE_RELEVANT_VIEW" and not result.get("selected_information_refs"))
    for name in (
        "provider_invoked", "model_invoked", "observation_execution",
        "observation_demand_formed", "capability_selection_executed",
        "goal_mutation", "self_mutation", "field_mutation", "world_truth_declared",
        "memory_mutation", "pcn_mutation", "decision_execution", "task_execution",
        "action_execution", "scenario_id_semantic_driver", "opaque_context_semantic_guess",
        "static_goal_need_lookup",
    ):
        _check(checks, f"summary:{name}_false", summary.get(name) is False)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "all_checks_passed": not failed,
        "checks": checks,
        "failed_checks": failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "validation_errors_empty": not failed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled minimum cognitive view evaluation.")
    parser.add_argument("summary", nargs="?", default="_eval_out/a_route_minimum_relevant_cognitive_view_v1/runner_summary_v1.json")
    args = parser.parse_args()
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    print(json.dumps(verify(summary), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
