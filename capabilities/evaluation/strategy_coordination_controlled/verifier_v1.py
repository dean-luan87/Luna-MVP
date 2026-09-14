"""Fail-closed verifier for controlled Strategy Coordination."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PHASE = "Phase-Strategy-Coordination-Controlled-Implementation-v1-001"
REQUIRED_CASES = {
    "SINGLE_STRATEGY",
    "TWO_INDEPENDENT_STRATEGIES",
    "EXPLICIT_DEFERRED",
    "MISSING_DEPENDENCY",
    "EXPLICIT_REDUNDANCY",
    "EXPLICIT_INCOMPATIBILITY",
    "DEFERRED_BRANCH_STRATEGY",
    "REJECTED_BRANCH_STRATEGY",
    "ZERO_STRATEGY",
    "MULTIPLE_GAPS",
    "SCENARIO_12_SHAPE",
    "REQUIREMENT_ALREADY_SATISFIED",
    "INVALID_INPUT",
}


def _check(checks: dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def _case(cases: dict[str, dict[str, Any]], case_id: str) -> dict[str, Any]:
    return cases[case_id]


def _decision_statuses(case: dict[str, Any]) -> list[str]:
    return [
        item.get("coordination_status")
        for item in (case.get("result") or {}).get("coordination_decisions") or []
    ]


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "required_cases", set(cases) == REQUIRED_CASES)
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)

    expected = {
        "SINGLE_STRATEGY": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED"]),
        "TWO_INDEPENDENT_STRATEGIES": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED", "ADMITTED"]),
        "EXPLICIT_DEFERRED": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED", "DEFERRED"]),
        "MISSING_DEPENDENCY": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED", "BLOCKED_DEPENDENCY"]),
        "EXPLICIT_REDUNDANCY": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED", "SUPPRESSED_REDUNDANT"]),
        "EXPLICIT_INCOMPATIBILITY": ("COORDINATION_DECISIONS_FORMED", ["INCOMPATIBLE", "INCOMPATIBLE"]),
        "DEFERRED_BRANCH_STRATEGY": ("NO_STRATEGY_CANDIDATES", []),
        "REJECTED_BRANCH_STRATEGY": ("NO_STRATEGY_CANDIDATES", []),
        "ZERO_STRATEGY": ("NO_STRATEGY_CANDIDATES", []),
        "MULTIPLE_GAPS": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED", "ADMITTED"]),
        "SCENARIO_12_SHAPE": ("COORDINATION_DECISIONS_FORMED", ["ADMITTED", "ADMITTED"]),
        "REQUIREMENT_ALREADY_SATISFIED": ("NO_STRATEGY_CANDIDATES", []),
        "INVALID_INPUT": ("INVALID_INPUT", []),
    }
    for case_id, (expected_result_status, expected_statuses) in expected.items():
        item = cases.get(case_id, {})
        result = item.get("result") or {}
        _check(checks, f"{case_id}:result_status", result.get("coordination_status") == expected_result_status)
        _check(checks, f"{case_id}:statuses", _decision_statuses(item) == expected_statuses)
        _check(checks, f"{case_id}:expected_statuses", item.get("expected_statuses") == expected_statuses)
        _check(
            checks,
            f"{case_id}:input_refs_coherent",
            result.get("input_strategy_refs")
            == [item.get("request", {}).get("strategy_candidates", [])[i].get("strategy_ref") for i in range(len(item.get("request", {}).get("strategy_candidates", [])))],
        )
        _check(
            checks,
            f"{case_id}:strategy_snapshot_unchanged",
            item.get("strategy_snapshot_before") == item.get("strategy_snapshot_after"),
        )

    independent = _case(cases, "TWO_INDEPENDENT_STRATEGIES")["result"]
    _check(checks, "no_winner_take_all", independent.get("admitted_strategy_refs") == [
        "strategy:controlled:a", "strategy:controlled:b"
    ])
    _check(checks, "multiple_valid_strategies_admitted", len(independent.get("admitted_strategy_refs") or []) == 2)

    dependency = _case(cases, "MISSING_DEPENDENCY")["result"]
    _check(checks, "dependency_block_local", dependency.get("blocked_dependency_strategy_refs") == ["strategy:controlled:b"])
    _check(checks, "dependency_does_not_block_sibling", dependency.get("admitted_strategy_refs") == ["strategy:controlled:a"])

    redundancy = _case(cases, "EXPLICIT_REDUNDANCY")["result"]
    _check(checks, "explicit_redundancy_only", redundancy.get("suppressed_redundant_strategy_refs") == ["strategy:controlled:b"])
    _check(checks, "redundancy_retention_deterministic", redundancy.get("admitted_strategy_refs") == ["strategy:controlled:a"])

    incompatible = _case(cases, "EXPLICIT_INCOMPATIBILITY")["result"]
    _check(checks, "incompatibility_no_winner", incompatible.get("incompatible_strategy_refs") == [
        "strategy:controlled:a", "strategy:controlled:b"
    ] and not incompatible.get("admitted_strategy_refs"))

    for case_id in ("DEFERRED_BRANCH_STRATEGY", "REJECTED_BRANCH_STRATEGY"):
        result = _case(cases, case_id)["result"]
        _check(checks, f"{case_id}:not_admitted", not result.get("admitted_strategy_refs"))
        _check(checks, f"{case_id}:excluded", result.get("excluded_strategy_refs") == ["strategy:controlled:a"])

    multiple_gaps = _case(cases, "MULTIPLE_GAPS")["result"]
    _check(checks, "multiple_gap_lineage", [item.get("branch_ref") for item in multiple_gaps.get("coordination_decisions") or []] == [
        "branch:controlled:strategy:a", "branch:controlled:strategy:b"
    ])

    invalid = _case(cases, "INVALID_INPUT")["result"]
    _check(checks, "invalid_input_fails_closed", invalid.get("coordination_status") == "INVALID_INPUT" and not invalid.get("coordination_decisions"))

    guard_names = (
        "strategy_execution",
        "observation_demand_formed",
        "capability_resolution_executed",
        "provider_invocation",
        "model_invocation",
        "decision_formed",
        "task_formed",
        "action_formed",
        "truth_declared",
        "world_truth_declared",
        "current_world_mutation",
        "field_mutation",
        "memory_pcn_mutation",
        "attention_formed",
        "resource_governance_executed",
        "resource_acquisition_executed",
        "priority_assigned",
        "ranking_executed",
        "winner_selected",
        "evidence_fusion_executed",
        "branch_mutation",
        "information_need_mutation",
        "requirement_satisfaction_mutation",
    )
    for name in guard_names:
        _check(checks, f"guard:{name}", summary.get(name) is False)
    _check(checks, "coordination_only", summary.get("strategy_coordination_only") is True)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Strategy Coordination.")
    parser.add_argument("--summary", type=Path, default=Path("_eval_out/strategy_coordination_v1/runner_summary_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("_eval_out/strategy_coordination_v1/verifier_result_v1.json"))
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["verify", "main"]
