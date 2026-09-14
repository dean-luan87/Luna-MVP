"""Static/contract verifier for controlled Observation Demand formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/observation_demand_v1")
REQUIRED_CASES = {
    "SINGLE_ADMITTED_PERCEPTION_STRATEGY",
    "TWO_INDEPENDENT_ADMITTED_STRATEGIES",
    "DEFERRED_STRATEGY",
    "BLOCKED_DEPENDENCY_STRATEGY",
    "SUPPRESSED_REDUNDANT_STRATEGY",
    "INCOMPATIBLE_STRATEGIES",
    "NO_STRATEGY_CANDIDATES",
    "REQUIREMENT_ALREADY_SATISFIED",
    "MULTIPLE_COGNITIVE_GAPS",
    "SCENARIO_12_SHAPE",
    "UNSUPPORTED_ACQUISITION_MODE",
    "INVALID_COORDINATION_INPUT",
}


def _check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _case(cases: dict[str, dict[str, Any]], case_id: str) -> dict[str, Any]:
    return cases.get(case_id, {})


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    cases_list = summary.get("cases", [])
    cases = {case.get("case_id"): case for case in cases_list}
    _check(checks, "required_fixture_cases_present", REQUIRED_CASES.issubset(cases))
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)
    _check(checks, "no_downstream_execution", all(summary.get(key) is False for key in (
        "capability_resolution_executed", "capability_execution", "provider_invocation",
        "model_invocation", "ocr_execution", "camera_execution", "slam_execution",
        "runtime_observation_executed", "resource_acquisition_executed", "resource_scheduling_executed",
        "decision_formed", "task_formed", "action_formed", "attention_formed",
    )))
    _check(checks, "no_mutation_or_truth", all(summary.get(key) is False for key in (
        "current_world_mutation", "field_mutation", "memory_pcn_mutation",
        "truth_declared", "world_truth_declared",
    )))

    expected_counts = {
        "SINGLE_ADMITTED_PERCEPTION_STRATEGY": ("OBSERVATION_DEMANDS_FORMED", 1),
        "TWO_INDEPENDENT_ADMITTED_STRATEGIES": ("OBSERVATION_DEMANDS_FORMED", 2),
        "DEFERRED_STRATEGY": ("NO_OBSERVATION_DEMAND", 0),
        "BLOCKED_DEPENDENCY_STRATEGY": ("NO_OBSERVATION_DEMAND", 0),
        "SUPPRESSED_REDUNDANT_STRATEGY": ("OBSERVATION_DEMANDS_FORMED", 1),
        "INCOMPATIBLE_STRATEGIES": ("NO_OBSERVATION_DEMAND", 0),
        "NO_STRATEGY_CANDIDATES": ("NO_OBSERVATION_DEMAND", 0),
        "REQUIREMENT_ALREADY_SATISFIED": ("NO_OBSERVATION_DEMAND", 0),
        "MULTIPLE_COGNITIVE_GAPS": ("OBSERVATION_DEMANDS_FORMED", 2),
        "SCENARIO_12_SHAPE": ("OBSERVATION_DEMANDS_FORMED", 2),
        "UNSUPPORTED_ACQUISITION_MODE": ("UNSUPPORTED_ACQUISITION_MODE", 0),
        "INVALID_COORDINATION_INPUT": ("INVALID_INPUT", 0),
    }
    for case_id, (status, count) in expected_counts.items():
        case = _case(cases, case_id)
        result = case.get("result", {})
        _check(checks, f"{case_id}:status", result.get("formation_status") == status)
        _check(checks, f"{case_id}:demand_count", len(result.get("demands", [])) == count)

    two = _case(cases, "TWO_INDEPENDENT_ADMITTED_STRATEGIES").get("result", {})
    _check(checks, "two_admitted_strategies_form_two_demands", len(two.get("demand_refs", [])) == 2)
    _check(checks, "no_merge_of_independent_strategies", len(set(two.get("demand_refs", []))) == 2)
    for case_id in ("DEFERRED_STRATEGY", "BLOCKED_DEPENDENCY_STRATEGY", "INCOMPATIBLE_STRATEGIES"):
        case = _case(cases, case_id)
        result = case.get("result", {})
        _check(checks, f"{case_id}:non_admitted_not_demanded", not result.get("demands"))

    suppressed_case = _case(cases, "SUPPRESSED_REDUNDANT_STRATEGY")
    suppressed_result = suppressed_case.get("result", {})
    suppressed_refs = set(
        suppressed_case.get("request", {})
        .get("coordination_result", {})
        .get("suppressed_redundant_strategy_refs", [])
    )
    suppressed_demand_sources = {
        demand.get("source_strategy_ref")
        for demand in suppressed_result.get("demands", [])
    }
    _check(
        checks,
        "SUPPRESSED_REDUNDANT_STRATEGY:non_admitted_not_demanded",
        bool(suppressed_refs) and suppressed_refs.isdisjoint(suppressed_demand_sources),
        "Every suppressed strategy ref is absent from demand source refs; admitted sibling demands remain allowed.",
    )

    all_demands_source_from_admitted = True
    for case in cases_list:
        coordination = case.get("request", {}).get("coordination_result", {})
        decisions_by_strategy = {
            decision.get("strategy_ref"): decision.get("coordination_status")
            for decision in coordination.get("coordination_decisions", [])
        }
        if any(
            decisions_by_strategy.get(demand.get("source_strategy_ref")) != "ADMITTED"
            for demand in case.get("result", {}).get("demands", [])
        ):
            all_demands_source_from_admitted = False
            break
    _check(
        checks,
        "all_demands_source_from_admitted_coordination_decisions",
        all_demands_source_from_admitted,
    )

    gaps = _case(cases, "MULTIPLE_COGNITIVE_GAPS").get("result", {}).get("demands", [])
    _check(checks, "multiple_gap_lineage_preserved", len(gaps) == 2 and len({d.get("source_branch_ref") for d in gaps}) == 2 and len({tuple(d.get("information_gap_refs", [])) for d in gaps}) == 2)
    scenario12 = _case(cases, "SCENARIO_12_SHAPE").get("result", {}).get("demands", [])
    _check(checks, "scenario12_two_demands", len(scenario12) == 2 and len({d.get("source_strategy_ref") for d in scenario12}) == 2)
    _check(checks, "unsupported_mode_fails_closed", not _case(cases, "UNSUPPORTED_ACQUISITION_MODE").get("result", {}).get("demands"))
    _check(checks, "invalid_input_fails_closed", not _case(cases, "INVALID_COORDINATION_INPUT").get("result", {}).get("demands"))

    immutable = all(
        case.get("strategy_snapshot_before") == case.get("strategy_snapshot_after")
        and case.get("coordination_snapshot_before") == case.get("coordination_snapshot_after")
        for case in cases_list
    )
    _check(checks, "strategy_snapshot_unchanged", immutable)
    _check(checks, "coordination_snapshot_unchanged", immutable)
    deterministic = all(
        case.get("result", {}).get("demand_refs", []) == case.get("deterministic_replay_demand_refs", [])
        for case in cases_list
    )
    _check(checks, "deterministic_refs", deterministic)

    all_demands = [d for case in cases_list for d in case.get("result", {}).get("demands", [])]
    _check(checks, "all_demands_candidate_only", all(d.get("candidate_only") is True for d in all_demands))
    _check(checks, "all_demands_read_only_non_truth", all(d.get("read_only") is True and d.get("truth_declared") is False and d.get("world_truth_declared") is False for d in all_demands))
    _check(checks, "lineage_integrity", all(d.get("source_strategy_ref") and d.get("source_branch_ref") and d.get("information_need_refs") and d.get("information_gap_refs") and d.get("acquisition_basis_refs") and d.get("lineage_refs") and d.get("provenance_refs") for d in all_demands))
    _check(checks, "no_capability_resolution", all(d.get("capability_requirement_formed") is False and d.get("capability_resolution_executed") is False for d in all_demands))
    _check(checks, "no_attention_or_execution", all(all(d.get(key) is False for key in (
        "attention_formed", "runtime_observation_executed", "capability_execution",
        "provider_invocation", "model_invocation", "ocr_execution", "camera_execution",
        "slam_execution", "resource_acquisition_executed", "decision_formed", "task_formed", "action_formed",
    )) for d in all_demands))
    _check(checks, "no_strategy_ranking_or_winner", summary.get("strategy_priority_assigned") is False and summary.get("winner_selected") is False)

    failed = [item["check_id"] for item in checks if not item["passed"]]
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "checks": checks,
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Observation Demand formation.")
    parser.add_argument("--smoke-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary_path = args.smoke_root / "runner_summary_v1.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    report = verify(summary)
    (args.smoke_root / "verifier_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["main", "verify"]
