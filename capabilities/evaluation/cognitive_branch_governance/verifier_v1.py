"""Verifier for candidate-only Cognitive Branch Governance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def _check(checks: Dict[str, bool], name: str, value: object) -> None:
    checks[name] = bool(value)


def _decisions(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("result") or {}).get("governance_decisions") or [])


def _statuses(case: Dict[str, Any]) -> tuple[str, ...]:
    return tuple(item.get("governance_status") for item in _decisions(case))


def _decision_pairs(case: Dict[str, Any]) -> tuple[tuple[str, str], ...]:
    return tuple(
        (item.get("branch_ref"), item.get("governance_status"))
        for item in _decisions(case)
    )


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = summary.get("cases") or []
    required_cases = {
        "MULTIPLE_VALID_BRANCHES",
        "ONE_VALID_ONE_INVALID_BASIS",
        "CURRENTLY_NOT_NEEDED_BUT_VALID",
        "NO_CANONICAL_EQUIVALENCE_RETAIN_BOTH",
        "NO_BRANCHES",
        "IRRELEVANT_CONTEXT_CHANGE",
        "BASIS_REMOVED:base",
        "BASIS_REMOVED:changed",
        "NEED_BECOMES_CURRENTLY_SATISFIED:base",
        "NEED_BECOMES_CURRENTLY_SATISFIED:changed",
        "RESOURCE_AVAILABILITY_CHANGE:available",
        "RESOURCE_AVAILABILITY_CHANGE:unavailable",
        "INVALID_CANDIDATE",
    }
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_COGNITIVE_BRANCH_GOVERNANCE_TEST")
    _check(checks, "required_cases", {item.get("case_id") for item in cases} == required_cases)

    multiple_valid = _case(cases, "MULTIPLE_VALID_BRANCHES")
    _check(checks, "multiple_valid_branches_can_all_be_admitted", _statuses(multiple_valid) == ("ADMITTED", "ADMITTED"))
    _check(checks, "no_winner_take_all", multiple_valid["result"]["admitted_branch_refs"] == multiple_valid["result"]["input_branch_refs"])

    one_invalid = _case(cases, "ONE_VALID_ONE_INVALID_BASIS")
    _check(checks, "invalid_basis_rejected_locally", _statuses(one_invalid) == ("ADMITTED", "REJECTED"))
    _check(checks, "valid_branch_unchanged_by_other_rejection", one_invalid["result"]["admitted_branch_refs"] == one_invalid["result"]["input_branch_refs"][:1])
    _check(checks, "basis_rejection_reason", _decisions(one_invalid)[1].get("reason_code") == "BASIS_NOT_CURRENT")

    not_needed = _case(cases, "CURRENTLY_NOT_NEEDED_BUT_VALID")
    _check(checks, "currently_not_needed_is_deferred", _statuses(not_needed) == ("DEFERRED",))
    _check(checks, "deferred_not_rejected", not_needed["result"]["deferred_branch_refs"] == [not_needed["result"]["input_branch_refs"][0]])
    _check(checks, "deferred_preserves_identity", _decisions(not_needed)[0].get("candidate_retained") is True and _decisions(not_needed)[0].get("recoverable") is True)

    no_equivalence = _case(cases, "NO_CANONICAL_EQUIVALENCE_RETAIN_BOTH")
    _check(checks, "no_canonical_equivalence_retains_both", _statuses(no_equivalence) == ("ADMITTED", "ADMITTED") and len(no_equivalence["result"]["input_branch_refs"]) == 2)

    _check(checks, "no_branches_empty_result", not (_case(cases, "NO_BRANCHES")["result"].get("admitted_branch_refs") or _case(cases, "NO_BRANCHES")["result"].get("deferred_branch_refs") or _case(cases, "NO_BRANCHES")["result"].get("rejected_branch_refs")))

    context_base = _case(cases, "MULTIPLE_VALID_BRANCHES")
    context_changed = _case(cases, "IRRELEVANT_CONTEXT_CHANGE")
    _check(checks, "irrelevant_context_stable", _decision_pairs(context_base) == _decision_pairs(context_changed))

    basis_base = _case(cases, "BASIS_REMOVED:base")
    basis_changed = _case(cases, "BASIS_REMOVED:changed")
    _check(checks, "basis_removal_changes_governance", _statuses(basis_base) == ("ADMITTED",) and _statuses(basis_changed) == ("REJECTED",))

    need_base = _case(cases, "NEED_BECOMES_CURRENTLY_SATISFIED:base")
    need_changed = _case(cases, "NEED_BECOMES_CURRENTLY_SATISFIED:changed")
    _check(checks, "satisfied_need_is_deferred_not_rejected", _statuses(need_base) == ("ADMITTED",) and _statuses(need_changed) == ("DEFERRED",))

    resource_available = _case(cases, "RESOURCE_AVAILABILITY_CHANGE:available")
    resource_unavailable = _case(cases, "RESOURCE_AVAILABILITY_CHANGE:unavailable")
    _check(checks, "resource_availability_does_not_change_governance", _decision_pairs(resource_available) == _decision_pairs(resource_unavailable))

    invalid_candidate = _case(cases, "INVALID_CANDIDATE")
    _check(checks, "invalid_candidate_rejected", _statuses(invalid_candidate) == ("REJECTED",) and _decisions(invalid_candidate)[0].get("reason_code") == "INVALID_CANDIDATE")

    for case in cases:
        result = case.get("result") or {}
        _check(checks, f"{case['case_id']}:expected_statuses", _statuses(case) == tuple(case.get("expected_statuses") or ()))
        _check(checks, f"{case['case_id']}:candidate_immutable", case.get("candidate_snapshot_before") == case.get("candidate_snapshot_after"))
        _check(checks, f"{case['case_id']}:candidate_only", result.get("candidate_only") is True)
        _check(checks, f"{case['case_id']}:read_only", result.get("read_only") is True)
        _check(checks, f"{case['case_id']}:no_formation", result.get("formation_executed") is False)
        _check(checks, f"{case['case_id']}:no_new_branch", result.get("new_branch_generated") is False)
        _check(checks, f"{case['case_id']}:no_governance_lifecycle_expansion", result.get("merge_executed") is False and result.get("convergence_executed") is False and result.get("close_executed") is False and result.get("reopen_executed") is False)
        for decision in _decisions(case):
            _check(checks, f"{case['case_id']}:{decision.get('branch_ref')}:non_truth", decision.get("truth_declared") is False and decision.get("world_truth_declared") is False)
            _check(checks, f"{case['case_id']}:{decision.get('branch_ref')}:retained", decision.get("candidate_retained") is True)

    for name in (
        "winner_take_all",
        "execution_priority_assigned",
        "resource_governance_executed",
        "resource_acquisition",
        "observation_demand_formed",
        "capability_requirement_formed",
        "current_world_mutation",
        "field_mutation",
        "truth_declared",
        "world_truth_declared",
        "decision_formed",
        "task_formed",
        "action_formed",
        "provider_invocation",
        "model_invocation",
        "memory_pcn_mutation",
        "formation_executed",
        "new_branch_generated",
        "merge_executed",
        "convergence_executed",
        "close_executed",
        "reopen_executed",
        "goal_string_governance",
        "question_string_governance",
        "scenario_id_semantic_driver",
        "case_id_semantic_driver",
        "fixture_specific_mapping",
        "semantic_string_similarity",
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
    parser = argparse.ArgumentParser(description="Verify controlled Cognitive Branch Governance.")
    parser.add_argument("summary", nargs="?", default="_eval_out/cognitive_branch_governance_v1/runner_summary_v1.json")
    args = parser.parse_args()
    result = verify(json.loads(Path(args.summary).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
