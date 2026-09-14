"""Verifier for controlled acquisition strategy candidate formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def _check(checks: Dict[str, bool], name: str, value: object) -> None:
    checks[name] = bool(value)


def _strategies(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("result") or {}).get("strategies") or [])


def _strategy_keys(case: Dict[str, Any]) -> tuple[tuple[str, str, str], ...]:
    return tuple(
        (
            item.get("branch_ref"),
            tuple(item.get("acquisition_basis_refs") or ())[0],
            item.get("acquisition_mode_candidate"),
        )
        for item in _strategies(case)
    )


def _snapshot_unchanged(case: Dict[str, Any]) -> bool:
    return case.get("input_snapshot_before") == case.get("input_snapshot_after")


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = summary.get("cases") or []
    required_cases = {
        "ONE_BRANCH_ONE_STRATEGY",
        "ONE_BRANCH_MULTIPLE_STRATEGIES",
        "MULTIPLE_BRANCHES_MULTIPLE_STRATEGIES",
        "NO_GOVERNED_ACQUISITION_BASIS",
        "DEFERRED_BRANCH",
        "REJECTED_BRANCH",
        "IRRELEVANT_CONTEXT_CHANGE:base",
        "IRRELEVANT_CONTEXT_CHANGE:changed",
        "SAME_NEED_DIFFERENT_GOVERNED_BASES:base",
        "SAME_NEED_DIFFERENT_GOVERNED_BASES:changed",
        "UNKNOWN_MODE",
        "CAPABILITY_CLASS_REF_PRESERVATION",
        "OPPORTUNITY_REF_PRESERVATION",
        "NO_BRANCHES",
        "INVALID_INPUT",
    }
    _check(
        checks,
        "controlled_marker",
        summary.get("source_mode")
        == "CONTROLLED_INFORMATION_ACQUISITION_STRATEGY_CANDIDATE_FORMATION_TEST",
    )
    _check(
        checks,
        "required_cases",
        {item.get("case_id") for item in cases} == required_cases,
    )

    one = _case(cases, "ONE_BRANCH_ONE_STRATEGY")
    _check(
        checks,
        "one_branch_one_strategy",
        one["result"]["formation_status"] == "FORMED_CANDIDATES"
        and len(_strategies(one)) == 1,
    )
    many = _case(cases, "ONE_BRANCH_MULTIPLE_STRATEGIES")
    many_basis = {
        tuple(item.get("acquisition_basis_refs") or ())[0]
        for item in _strategies(many)
    }
    _check(
        checks,
        "multiple_strategies_allowed",
        len(_strategies(many)) == 3 and len(many_basis) == 3,
    )
    _check(checks, "no_winner_take_all", len(_strategies(many)) > 1)

    multi = _case(cases, "MULTIPLE_BRANCHES_MULTIPLE_STRATEGIES")
    _check(
        checks,
        "multi_branch_lineage_preserved",
        {item.get("branch_ref") for item in _strategies(multi)}
        == {"branch:controlled:a", "branch:controlled:b"},
    )
    _check(
        checks,
        "multi_branch_strategy_count",
        len(_strategies(multi)) == 3,
    )

    for case_id in ("NO_GOVERNED_ACQUISITION_BASIS", "DEFERRED_BRANCH", "REJECTED_BRANCH", "NO_BRANCHES"):
        item = _case(cases, case_id)
        _check(
            checks,
            f"{case_id}:no_strategies",
            len(_strategies(item)) == 0,
        )
    _check(
        checks,
        "no_basis_status",
        _case(cases, "NO_GOVERNED_ACQUISITION_BASIS")["result"]["formation_status"]
        == "NO_GOVERNED_ACQUISITION_BASIS",
    )
    _check(
        checks,
        "deferred_branch_excluded",
        _case(cases, "DEFERRED_BRANCH")["result"]["excluded_branch_refs"]
        == ["branch:controlled:a"],
    )
    _check(
        checks,
        "rejected_branch_excluded",
        _case(cases, "REJECTED_BRANCH")["result"]["excluded_branch_refs"]
        == ["branch:controlled:a"],
    )

    context_base = _case(cases, "IRRELEVANT_CONTEXT_CHANGE:base")
    context_changed = _case(cases, "IRRELEVANT_CONTEXT_CHANGE:changed")
    _check(checks, "irrelevant_context_stable", _strategy_keys(context_base) == _strategy_keys(context_changed))

    basis_base = _case(cases, "SAME_NEED_DIFFERENT_GOVERNED_BASES:base")
    basis_changed = _case(cases, "SAME_NEED_DIFFERENT_GOVERNED_BASES:changed")
    _check(checks, "basis_sensitive", _strategy_keys(basis_base) != _strategy_keys(basis_changed))

    unknown = _case(cases, "UNKNOWN_MODE")
    _check(
        checks,
        "unknown_mode_preserved_as_unknown",
        _strategies(unknown)[0].get("acquisition_mode_candidate") == "UNKNOWN",
    )
    cap_case = _case(cases, "CAPABILITY_CLASS_REF_PRESERVATION")
    _check(
        checks,
        "capability_class_ref_preserved",
        _strategies(cap_case)[0].get("required_capability_class_refs")
        == ["capability-class:controlled:evidence"],
    )
    _check(checks, "capability_requirement_not_formed", cap_case["result"].get("capability_requirement_formed") is False)
    opportunity = _case(cases, "OPPORTUNITY_REF_PRESERVATION")
    _check(
        checks,
        "opportunity_ref_preserved",
        _strategies(opportunity)[0].get("opportunity_refs")
        == ["opportunity:controlled:visible"],
    )

    invalid = _case(cases, "INVALID_INPUT")
    _check(
        checks,
        "invalid_input_fails_closed",
        invalid["result"]["formation_status"] == "INVALID_INPUT"
        and not _strategies(invalid),
    )

    for item in cases:
        result = item.get("result") or {}
        _check(
            checks,
            f"{item['case_id']}:expected_status",
            result.get("formation_status") == item.get("expected_status"),
        )
        _check(
            checks,
            f"{item['case_id']}:expected_count",
            len(_strategies(item)) == item.get("expected_strategy_count"),
        )
        _check(checks, f"{item['case_id']}:inputs_immutable", _snapshot_unchanged(item))
        for strategy in _strategies(item):
            _check(checks, f"{item['case_id']}:{strategy.get('strategy_ref')}:candidate_only", strategy.get("candidate_only") is True)
            _check(checks, f"{item['case_id']}:{strategy.get('strategy_ref')}:read_only", strategy.get("read_only") is True)
            _check(checks, f"{item['case_id']}:{strategy.get('strategy_ref')}:non_truth", strategy.get("truth_declared") is False and strategy.get("world_truth_declared") is False)

    for name in (
        "strategy_coordination_executed",
        "strategy_priority_assigned",
        "resource_merge_executed",
        "resource_acquisition_executed",
        "attention_formed",
        "observation_demand_formed",
        "capability_requirement_formed",
        "capability_resolution_executed",
        "provider_invocation",
        "model_invocation",
        "decision_formed",
        "task_formed",
        "action_formed",
        "field_mutation",
        "current_world_mutation",
        "memory_pcn_mutation",
        "truth_declared",
        "world_truth_declared",
        "goal_string_lookup",
        "question_string_lookup",
        "need_string_strategy_lookup",
        "scenario_id_semantic_driver",
        "case_id_semantic_driver",
        "fixture_specific_mapping",
        "opaque_context_semantic_guess",
    ):
        _check(checks, f"summary:{name}_false", summary.get(name) is False)

    failed_checks = sorted(name for name, passed in checks.items() if not passed)
    return {
        "phase": summary.get("phase"),
        "all_checks_passed": not failed_checks,
        "failed_checks": failed_checks,
        "checks": checks,
        "cognitive_logic_result": "PASS" if not failed_checks else "FAIL",
        "operational_result": "PASS" if not failed_checks else "FAIL",
        "final_decision": "GO" if not failed_checks else "NO-GO",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify controlled acquisition strategy candidate formation."
    )
    parser.add_argument(
        "summary",
        nargs="?",
        default="_eval_out/information_acquisition_strategy_candidate_formation_v1/runner_summary_v1.json",
    )
    args = parser.parse_args()
    result = verify(json.loads(Path(args.summary).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
