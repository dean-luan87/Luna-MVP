"""Fail-closed verifier for controlled Required Condition formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PHASE = "Phase-P1-Luna-Required-Cognitive-Condition-Formation-v1-001"


def _check(checks: dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    cases = {item.get("case_id"): item for item in summary.get("cases", ())}
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_A_ROUTE_REQUIRED_COGNITIVE_CONDITION_FORMATION_TEST")
    _check(checks, "provider_model_not_invoked", summary.get("provider_invoked") is False and summary.get("model_invoked") is False)
    _check(checks, "no_downstream_execution", summary.get("observation_execution") is False and summary.get("observation_demand_formed") is False and summary.get("capability_selection_executed") is False)
    required = {
        "SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION",
        "SAME_GOAL_RELEVANT_STATE_CHANGE",
        "SAME_GOAL_NEED_ALREADY_SATISFIED",
        "SAME_GOAL_DIFFERENT_GOVERNED_ROLE",
        "SAME_GOAL_SELF_STATE_CONDITIONED",
        "SAME_GOAL_IRRELEVANT_INFORMATION_CHANGE",
        "DIFFERENT_GOAL_SAME_SITUATION",
        "MINIMUM_REQUIRED_SET",
    }
    _check(checks, "required_cases", set(cases) == required)

    for case_id, item in cases.items():
        result = item.get("result") or {}
        _check(checks, f"{case_id}:status", result.get("status") == item.get("expected_status"))
        _check(checks, f"{case_id}:active_set", result.get("active_required_condition_refs") == item.get("expected_active"))
        _check(checks, f"{case_id}:satisfied_set", result.get("satisfied_condition_refs") == item.get("expected_satisfied"))
        _check(checks, f"{case_id}:candidate_only", result.get("candidate_only") is True)
        _check(checks, f"{case_id}:read_only", result.get("read_only") is True)
        _check(checks, f"{case_id}:no_truth", result.get("truth_declared") is False and result.get("world_truth_declared") is False)
        _check(checks, f"{case_id}:no_mutation", not any(result.get(name) for name in ("goal_mutation", "intent_mutation", "concern_mutation", "role_mutation", "context_mutation", "field_mutation", "self_mutation", "current_world_mutation", "memory_mutation", "pcn_mutation")))
        _check(checks, f"{case_id}:no_static_semantics", result.get("scenario_id_semantic_driver") is False and result.get("fixture_specific_mapping") is False and result.get("static_goal_condition_lookup") is False and result.get("opaque_context_semantic_guess") is False)
        downstream = item.get("downstream") or {}
        view = downstream.get("minimum_relevant_view") or {}
        need = downstream.get("information_need") or {}
        _check(checks, f"{case_id}:minimum_view_compatible", view.get("active_condition_refs") == result.get("active_required_condition_refs"))
        _check(checks, f"{case_id}:need_compatible", need.get("required_cognitive_condition_refs") == result.get("active_required_condition_refs"))

    _check(checks, "state_sensitive", cases["SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION"]["result"]["satisfied_condition_refs"] != cases["SAME_GOAL_RELEVANT_STATE_CHANGE"]["result"]["satisfied_condition_refs"])
    satisfied_case = cases["SAME_GOAL_NEED_ALREADY_SATISFIED"]["result"]
    _check(checks, "satisfied_conditions_preserve_requiredness", satisfied_case["active_required_condition_refs"] == cases["SAME_GOAL_NEED_ALREADY_SATISFIED"]["expected_active"] and satisfied_case["satisfied_condition_refs"] == cases["SAME_GOAL_NEED_ALREADY_SATISFIED"]["expected_satisfied"])
    satisfied_candidates = satisfied_case.get("candidates") or ()
    _check(checks, "satisfied_candidates_are_still_active", all(item.get("status") == "ACTIVE_REQUIRED" and item.get("satisfaction_status") == "SATISFIED" for item in satisfied_candidates if item.get("condition_ref") in satisfied_case.get("active_required_condition_refs", ())))
    _check(checks, "role_sensitive", cases["SAME_GOAL_DIFFERENT_GOVERNED_ROLE"]["result"]["active_required_condition_refs"] != cases["SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION"]["result"]["active_required_condition_refs"])
    _check(checks, "self_sensitive", cases["SAME_GOAL_SELF_STATE_CONDITIONED"]["result"]["active_required_condition_refs"] != cases["SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION"]["result"]["active_required_condition_refs"])
    _check(checks, "goal_sensitive", cases["DIFFERENT_GOAL_SAME_SITUATION"]["result"]["active_required_condition_refs"] != cases["SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION"]["result"]["active_required_condition_refs"])
    _check(checks, "irrelevant_stable", cases["SAME_GOAL_IRRELEVANT_INFORMATION_CHANGE"]["result"]["active_required_condition_refs"] == cases["SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION"]["result"]["active_required_condition_refs"])
    minimum_candidates = cases["MINIMUM_REQUIRED_SET"]["result"].get("candidates") or ()
    _check(checks, "minimum_set_selected", any(item.get("condition_ref") == "condition:seat:operator-access-required:v1" and item.get("status") == "ACTIVE_REQUIRED" for item in minimum_candidates) and any(item.get("condition_ref") == "condition:seat:operator-access-alternative:v1" and item.get("status") == "DORMANT" for item in minimum_candidates))
    _check(checks, "satisfied_need_delegated_downstream", (cases["SAME_GOAL_NEED_ALREADY_SATISFIED"].get("downstream") or {}).get("information_need", {}).get("status") == "NO_ACTIVE_NEED")
    negative = {item.get("case_id"): item.get("result") or {} for item in summary.get("negative_cases", ())}
    _check(checks, "negative_candidate_only_rejected", negative.get("CANDIDATE_ONLY_FALSE", {}).get("status") == "REJECTED")
    _check(checks, "no_need_cycle", summary.get("information_need_formation_reentered") is False and all(not result.get("information_need_input_used") for result in (item.get("result") or {} for item in summary.get("cases", ()))))
    _check(checks, "no_side_effect_path", all(not result.get(name) for result in (item.get("result") or {} for item in summary.get("cases", ())) for name in ("provider_invocation", "model_invocation", "observation_execution", "observation_demand_formed", "capability_selection_executed", "decision_execution", "task_execution", "action_execution")))
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
    parser = argparse.ArgumentParser(description="Verify controlled Required Cognitive Condition formation.")
    parser.add_argument("--summary", type=Path, default=Path("_eval_out/a_route_required_cognitive_condition_formation_v1/runner_summary_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("_eval_out/a_route_required_cognitive_condition_formation_v1/verifier_result_v1.json"))
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
