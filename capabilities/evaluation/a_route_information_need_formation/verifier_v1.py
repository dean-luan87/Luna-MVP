"""Fail-closed verifier for controlled A-Route Need formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-A-Route-Information-Need-Formation-v1-001"


def _check(checks: Dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = {item.get("case_id"): item for item in summary.get("cases", ())}
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_A_ROUTE_INFORMATION_NEED_FORMATION_TEST")
    _check(checks, "provider_model_not_invoked", summary.get("provider_invoked") is False and summary.get("model_invoked") is False)
    _check(checks, "no_observation_path", summary.get("observation_execution") is False and summary.get("observation_demand_formed") is False)
    _check(checks, "no_capability_selection", summary.get("capability_selection_executed") is False)
    required = {
        "SAME_GOAL_DIFFERENT_CURRENT_WORLD",
        "SAME_GOAL_NEED_ALREADY_SATISFIED",
        "SAME_GOAL_PARTIAL_COGNITIVE_COVERAGE",
        "SAME_GOAL_DIFFERENT_GOVERNED_ROLE_OWNER",
        "SAME_GOAL_DIFFERENT_GOVERNED_ROLE_VISITOR",
        "SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_A",
        "SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_B",
        "DIFFERENT_GOAL_SAME_CURRENT_WORLD",
    }
    _check(checks, "required_cases", set(cases) == required)

    for case_id, item in cases.items():
        result = item.get("result") or {}
        need = result.get("need") or {}
        _check(checks, f"{case_id}:status", result.get("status") == item.get("expected_status"))
        _check(checks, f"{case_id}:unknown_difference", result.get("necessary_unknown_refs") == item.get("expected_unknown"))
        _check(checks, f"{case_id}:current_world_consumed", result.get("current_world_ref") == (item.get("request") or {}).get("current_world_ref"))
        _check(checks, f"{case_id}:goal_preserved", result.get("goal_ref") == (item.get("request") or {}).get("goal_ref"))
        _check(checks, f"{case_id}:candidate_only", result.get("candidate_only") is True)
        _check(checks, f"{case_id}:no_mutation", not any(result.get(name) for name in ("goal_mutation", "intent_mutation", "concern_mutation", "field_mutation", "current_world_mutation")))
        _check(checks, f"{case_id}:no_static_lookup", result.get("static_goal_need_lookup") is False and result.get("scenario_id_semantic_driver") is False)
        if item.get("expected_status") == "NEED_FORMED":
            _check(checks, f"{case_id}:need_present", bool(need.get("need_id")))
            _check(checks, f"{case_id}:need_is_candidate", need.get("candidate_only") is True and need.get("materialization_status") == "CURRENT_MINIMUM_NECESSARY_NEED")
            _check(checks, f"{case_id}:need_not_goal", need.get("need_id") != result.get("goal_ref"))
            _check(checks, f"{case_id}:state_version", need.get("state_version_ref") == result.get("current_world_ref"))
        else:
            _check(checks, f"{case_id}:satisfied_has_no_need", result.get("need") is None)

    by_id = cases
    _check(checks, "same_goal_current_world_changes_need", by_id["SAME_GOAL_DIFFERENT_CURRENT_WORLD"]["result"]["necessary_unknown_refs"] != by_id["SAME_GOAL_PARTIAL_COGNITIVE_COVERAGE"]["result"]["necessary_unknown_refs"])
    _check(checks, "satisfied_need_suppressed", by_id["SAME_GOAL_NEED_ALREADY_SATISFIED"]["result"]["status"] == "NO_ACTIVE_NEED")
    _check(checks, "role_condition_changes_need", by_id["SAME_GOAL_DIFFERENT_GOVERNED_ROLE_OWNER"]["result"]["necessary_unknown_refs"] != by_id["SAME_GOAL_DIFFERENT_GOVERNED_ROLE_VISITOR"]["result"]["necessary_unknown_refs"])
    _check(checks, "irrelevant_context_stable", by_id["SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_A"]["result"]["necessary_unknown_refs"] == by_id["SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_B"]["result"]["necessary_unknown_refs"] and by_id["SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_A"]["result"]["need"]["need_id"] == by_id["SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_B"]["result"]["need"]["need_id"])
    _check(checks, "different_goal_changes_need", by_id["SAME_GOAL_NEED_ALREADY_SATISFIED"]["result"]["status"] != by_id["DIFFERENT_GOAL_SAME_CURRENT_WORLD"]["result"]["status"])

    negative = {item.get("case_id"): item.get("result") or {} for item in summary.get("negative_cases", ())}
    _check(checks, "negative_candidate_only_rejected", negative.get("CANDIDATE_ONLY_FALSE", {}).get("status") == "REJECTED")
    _check(checks, "negative_world_mutation_rejected", negative.get("CURRENT_WORLD_MUTATION_FLAG", {}).get("status") == "REJECTED")
    _check(checks, "no_truth_or_side_effect_path", all(not (result.get(name)) for result in negative.values() for name in ("world_truth_declared", "memory_mutation", "pcn_mutation", "decision_execution", "task_execution", "action_execution", "provider_invocation", "model_invocation", "observation_demand_formed", "capability_selection_executed")))
    failed = [name for name, passed in checks.items() if not passed]
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
    parser = argparse.ArgumentParser(description="Verify controlled A-Route Need formation.")
    parser.add_argument("--summary", type=Path, default=Path("_eval_out/a_route_information_need_formation_v1/runner_summary_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("_eval_out/a_route_information_need_formation_v1/verifier_result_v1.json"))
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
