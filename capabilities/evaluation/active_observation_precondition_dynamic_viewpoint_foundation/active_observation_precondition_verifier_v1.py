"""Fail-closed verifier for controlled active observation preconditions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-Active-Observation-Precondition-And-Dynamic-Viewpoint-Foundation-v1-001"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
DEFAULT_SUMMARY = ROOT / "_eval_out/active_observation_precondition_dynamic_viewpoint_foundation_v1/runner_summary_v1.json"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: Dict[str, Any]) -> Dict[str, list]:
    grouped: Dict[str, list] = {}
    for item in summary.get("cases", ()):
        grouped.setdefault(item.get("case_id"), []).append(item)
    return grouped


def _trace_complete(item: Dict[str, Any]) -> bool:
    result = item.get("result") or item
    request = result.get("request") or {}
    requirement = request.get("observation_requirement") or {}
    refs = set(result.get("trace_refs") or ())
    refs.update(result.get("provenance_refs") or ())
    return all(
        bool(value)
        for value in (
            request.get("observation_demand_ref"),
            request.get("observation_request_ref"),
            requirement.get("observation_requirement_ref"),
            requirement.get("capability_requirement_ref"),
            requirement.get("capability_ref"),
            requirement.get("target_ref"),
            requirement.get("field_ref"),
            request.get("self_state", {}).get("state_ref"),
            request.get("relative_state", {}).get("relative_state_ref"),
            result.get("necessity", {}).get("necessity_ref"),
            result.get("feasibility", {}).get("feasibility_ref"),
            result.get("window", {}).get("window_ref"),
            result.get("capability_eligibility", {}).get("eligibility_ref"),
        )
    ) and len(refs) >= 2


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    grouped = _cases(summary)
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_dynamic_state", summary.get("execution_mode") == "CONTROLLED_DYNAMIC_STATE")
    _check(checks, "provider_not_invoked", summary.get("provider_invocation") is False)
    _check(checks, "model_not_invoked", summary.get("model_invocation") is False)
    _check(checks, "scenario_id_not_semantic_driver", summary.get("scenario_id_semantic_driver") is False and summary.get("cycle_index_semantic_driver") is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))
    _check(checks, "four_required_cases", set(grouped) == {
        "OBSERVATION_NOT_NECESSARY",
        "NECESSARY_BUT_CONDITIONS_NOT_MET",
        "DYNAMIC_STATE_REACHES_OBSERVABLE",
        "OBSERVATION_WINDOW_LOST",
    })

    all_items = [item for values in grouped.values() for item in values]
    _check(checks, "unknown_does_not_imply_observation", (
        len(grouped.get("OBSERVATION_NOT_NECESSARY", ())) == 1
        and grouped["OBSERVATION_NOT_NECESSARY"][0]["necessity"]["status"] == "NOT_REQUIRED"
        and not grouped["OBSERVATION_NOT_NECESSARY"][0]["adjustment_needs"]
        and grouped["OBSERVATION_NOT_NECESSARY"][0]["capability_eligibility"]["eligible_now"] is False
    ))
    _check(checks, "observation_demand_does_not_imply_provider_invocation", all(
        (item.get("behavior") or {}).get("provider_invocation") is False for item in all_items
    ))

    case_b = (grouped.get("NECESSARY_BUT_CONDITIONS_NOT_MET") or [{}])[0]
    _check(checks, "unmet_conditions_close_window", case_b.get("window", {}).get("status") == "CLOSED")
    _check(checks, "unmet_conditions_block_capability_eligibility", case_b.get("capability_eligibility", {}).get("eligible_now") is False)
    _check(checks, "required_observation_with_gap_produces_adjustment_need", bool(case_b.get("condition_gaps")) and bool(case_b.get("adjustment_needs")))

    case_c = grouped.get("DYNAMIC_STATE_REACHES_OBSERVABLE") or []
    _check(checks, "relative_state_change_can_open_window", len(case_c) == 2 and [item["window"]["status"] for item in case_c] == ["CLOSED", "OPEN"])
    _check(checks, "same_requirement_different_relative_state_changes_feasibility", len(case_c) == 2 and case_c[0]["request"]["observation_requirement"]["observation_requirement_ref"] == case_c[1]["request"]["observation_requirement"]["observation_requirement_ref"] and case_c[0]["feasibility"]["status"] != case_c[1]["feasibility"]["status"])
    _check(checks, "relative_state_change_can_close_window", len(grouped.get("OBSERVATION_WINDOW_LOST", ())) == 2 and [item["window"]["status"] for item in grouped["OBSERVATION_WINDOW_LOST"]] == ["OPEN", "CLOSED"])

    _check(checks, "self_state_does_not_own_observation_decision", all((item.get("behavior") or {}).get("self_owns_observation_decision") is False for item in all_items))
    _check(checks, "no_field_truth_mutation", summary.get("forbidden_behaviors", {}).get("field_mutation") is False)
    _check(checks, "no_world_truth", summary.get("forbidden_behaviors", {}).get("world_truth_declared") is False)
    _check(checks, "no_decision_execution", summary.get("forbidden_behaviors", {}).get("decision_execution") is False)
    _check(checks, "no_task_execution", summary.get("forbidden_behaviors", {}).get("task_execution") is False)
    _check(checks, "no_action_execution", summary.get("forbidden_behaviors", {}).get("action_execution") is False)
    _check(checks, "no_device_control", summary.get("forbidden_behaviors", {}).get("device_control") is False)
    _check(checks, "capability_eligible_does_not_mean_provider_invoked", all(
        item.get("capability_eligibility", {}).get("eligible_now") is True
        and (item.get("behavior") or {}).get("provider_invocation") is False
        for item in (case_c[1:2] + (grouped.get("OBSERVATION_WINDOW_LOST") or [])[:1])
    ))
    _check(checks, "candidate_only", all(item.get("candidate_only") is True for item in all_items))
    _check(checks, "traceability_complete", all(_trace_complete(item) for item in all_items))
    _check(checks, "validation_errors_empty_per_case", all(not item.get("validation_errors") for item in all_items))

    case_d = grouped.get("OBSERVATION_WINDOW_LOST") or []
    _check(checks, "window_loss_is_relative_state_change", len(case_d) == 2 and case_d[0]["request"]["relative_state"]["relative_state_ref"] != case_d[1]["request"]["relative_state"]["relative_state_ref"] and case_d[1]["condition_gaps"][0]["kind"] == "OCCLUDED")

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "failed_checks": failed,
        "checks": checks,
        "controlled_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "NOT_APPLICABLE_REAL_RUNTIME_NOT_REQUESTED",
        "final_decision": "NOT_APPLICABLE",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failed else "CONTROLLED_VERIFICATION_FAILED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled active observation precondition cases.")
    parser.add_argument("summary", nargs="?", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    if not args.summary.exists():
        print(json.dumps({"all_checks_passed": False, "failed_checks": [f"summary_not_found:{args.summary}"]}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    result = verify(summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_passed"] else 1)


if __name__ == "__main__":
    main()
