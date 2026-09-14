"""Verifier for candidate-only governed cognitive branch formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def _check(checks: Dict[str, bool], name: str, value: object) -> None:
    checks[name] = bool(value)


def _branches(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("result") or {}).get("branches") or [])


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = summary.get("cases") or []
    negative = summary.get("negative_cases") or []
    required_cases = {
        "SINGLE_SUFFICIENT_EXPLANATION",
        "MULTIPLE_HYPOTHESIS_ALTERNATIVES",
        "MULTIPLE_UNRESOLVED_GAPS",
        "EXPLICIT_CONFLICT_WITH_EXISTING_ALTERNATIVES",
        "IRRELEVANT_CONTEXT_CHANGE",
        "SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES:base",
        "SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES:changed",
        "NO_EXPLICIT_BRANCH_BASIS",
    }
    actual_cases = {item.get("case_id") for item in cases}
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_GOVERNED_COGNITIVE_BRANCH_FORMATION_TEST")
    _check(checks, "required_cases", actual_cases == required_cases)
    _check(checks, "branch_formation_not_mandatory", len(_branches(_case(cases, "SINGLE_SUFFICIENT_EXPLANATION"))) <= 1)
    _check(checks, "multiple_hypotheses_form_distinct_branches", len({item["branch_ref"] for item in _branches(_case(cases, "MULTIPLE_HYPOTHESIS_ALTERNATIVES"))}) == 2)
    _check(checks, "hypothesis_refs_preserved", {ref for item in _branches(_case(cases, "MULTIPLE_HYPOTHESIS_ALTERNATIVES")) for ref in item["hypothesis_refs"]} == {"hypothesis:controlled:a", "hypothesis:controlled:b"})
    _check(checks, "multiple_gaps_form_distinct_branches", len(_branches(_case(cases, "MULTIPLE_UNRESOLVED_GAPS"))) == 2)
    _check(checks, "gap_refs_preserved", {item["basis_ref"] for item in _branches(_case(cases, "MULTIPLE_UNRESOLVED_GAPS"))} == {"gap:controlled:location", "gap:controlled:access"})
    _check(checks, "conflict_uses_existing_alternatives_only", len(_branches(_case(cases, "EXPLICIT_CONFLICT_WITH_EXISTING_ALTERNATIVES"))) == 2 and all(item["conflict_refs"] == ["conflict:controlled:ab"] for item in _branches(_case(cases, "EXPLICIT_CONFLICT_WITH_EXISTING_ALTERNATIVES"))))
    _check(checks, "irrelevant_context_stable", [item["result"]["branch_refs"] for item in cases if item["case_id"] in {"MULTIPLE_HYPOTHESIS_ALTERNATIVES", "IRRELEVANT_CONTEXT_CHANGE"}][0] == [item["result"]["branch_refs"] for item in cases if item["case_id"] in {"MULTIPLE_HYPOTHESIS_ALTERNATIVES", "IRRELEVANT_CONTEXT_CHANGE"}][1])
    _check(checks, "basis_change_changes_branches", _case(cases, "SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES:base")["result"]["branch_refs"] != _case(cases, "SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES:changed")["result"]["branch_refs"])
    _check(checks, "no_explicit_basis_no_branches", len(_branches(_case(cases, "NO_EXPLICIT_BRANCH_BASIS"))) == 0)
    _check(checks, "lineage_preserved", all(item["parent_cognitive_problem_ref"] and item["source_state_ref"] and item["basis_ref"] in item["lineage_refs"] for case in cases for item in _branches(case)))
    _check(checks, "branch_status_is_formation_only", all(item["formation_status"] == "FORMED_CANDIDATE" for case in cases for item in _branches(case)))

    for case in cases:
        result = case.get("result") or {}
        _check(checks, f"{case['case_id']}:expected_count", len(result.get("branches") or []) == case.get("expected_branch_count"))
        _check(checks, f"{case['case_id']}:expected_basis", tuple(item.get("formation_basis") for item in _branches(case)) == tuple(case.get("expected_basis") or ()))
        _check(checks, f"{case['case_id']}:candidate_only", result.get("candidate_only") is True)
        _check(checks, f"{case['case_id']}:read_only", result.get("read_only") is True)
        _check(checks, f"{case['case_id']}:no_governance", result.get("governance_executed") is False)
        for branch in _branches(case):
            _check(checks, f"{case['case_id']}:{branch.get('branch_ref')}:candidate_only", branch.get("candidate_only") is True)
            _check(checks, f"{case['case_id']}:{branch.get('branch_ref')}:read_only", branch.get("read_only") is True)
            _check(checks, f"{case['case_id']}:{branch.get('branch_ref')}:non_truth", branch.get("truth_declared") is False and branch.get("world_truth_declared") is False)
            _check(checks, f"{case['case_id']}:{branch.get('branch_ref')}:no_mutation", branch.get("current_world_mutation") is False and branch.get("field_mutation") is False)

    for case in negative:
        result = case.get("result") or {}
        _check(checks, f"{case['case_id']}:invalid_input", result.get("formation_status") == "INVALID_INPUT")
        _check(checks, f"{case['case_id']}:no_branches", not result.get("branches"))

    for name in (
        "provider_invocation",
        "model_invocation",
        "resource_acquisition",
        "observation_demand_formed",
        "capability_requirement_formed",
        "governance_executed",
        "decision_formed",
        "task_formed",
        "action_formed",
        "current_world_mutation",
        "field_mutation",
        "world_truth_declared",
        "autonomous_child_runtime_spawn",
        "scenario_id_semantic_driver",
        "case_id_semantic_driver",
        "goal_string_branch_lookup",
        "question_string_branch_lookup",
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
    parser = argparse.ArgumentParser(description="Verify governed cognitive branch formation.")
    parser.add_argument("summary", nargs="?", default="_eval_out/governed_cognitive_branch_formation_v1/runner_summary_v1.json")
    args = parser.parse_args()
    result = verify(json.loads(Path(args.summary).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
