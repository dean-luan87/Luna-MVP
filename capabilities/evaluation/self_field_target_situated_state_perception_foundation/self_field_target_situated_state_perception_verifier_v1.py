"""Fail-closed verifier for derived situated condition candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-Self-Field-Target-Situated-State-Perception-Foundation-v1-001"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
DEFAULT_SUMMARY = ROOT / "_eval_out/self_field_target_situated_state_perception_foundation_v1/runner_summary_v1.json"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _group(summary: Dict[str, Any]) -> Dict[str, list]:
    grouped: Dict[str, list] = {}
    for item in summary.get("cases", ()):
        grouped.setdefault(item.get("case_id"), []).append(item)
    return grouped


def _condition_map(item: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        row.get("condition_ref"): row
        for row in (item.get("perception", {}).get("condition_candidates") or ())
    }


def _result(item: Dict[str, Any]) -> Dict[str, Any]:
    return item.get("precondition_result") or {}


def _state(item: Dict[str, Any]) -> Dict[str, Any]:
    return item.get("perception", {}).get("situated_state") or {}


def _trace_complete(item: Dict[str, Any]) -> bool:
    perception = item.get("perception") or {}
    request = perception.get("request") or {}
    state = perception.get("situated_state") or {}
    result = _result(item)
    need = result.get("request", {}).get("capability_need") or {}
    minimum = result.get("request", {}).get("minimum_condition_requirement") or {}
    refs = set(perception.get("trace_refs") or ()) | set(perception.get("provenance_refs") or ())
    required = (
        request.get("situated_state_ref"),
        request.get("capability_requirement_ref"),
        request.get("temporal_ref"),
        request.get("self_state", {}).get("state_ref"),
        request.get("relative_state", {}).get("relative_state_ref"),
        state.get("situated_state_ref"),
        need.get("capability_need_ref"),
        minimum.get("requirement_ref"),
        (result.get("feasibility") or {}).get("feasibility_ref"),
        (result.get("eligibility") or {}).get("eligibility_ref"),
    )
    return all(bool(ref) for ref in required) and len(refs) >= 2


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    grouped = _group(summary)
    expected = {
        "TARGET_NOT_VISIBLE",
        "TARGET_BECOMES_VISIBLE",
        "TARGET_PARTIALLY_VISIBLE",
        "TARGET_SCALE_INADEQUATE",
        "RELATION_UNSTABLE",
        "RELATION_BECOMES_STABLE",
        "UNKNOWN_STATE_DOES_NOT_PASS",
        "SAME_INFORMATION_NEED_DIFFERENT_SITUATED_STATE",
        "OBSERVATION_NOT_NECESSARY_FROM_SITUATED_INPUT",
    }
    all_items = [item for values in grouped.values() for item in values]
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_situated_state_perception", summary.get("execution_mode") == "CONTROLLED_SITUATED_STATE_PERCEPTION")
    _check(checks, "required_cases", set(grouped) == expected)
    _check(checks, "condition_not_directly_fixture_declared", all(
        not (item.get("perception", {}).get("request") or {}).get("satisfied_condition_refs")
        and bool(item.get("perception", {}).get("condition_candidates"))
        for item in all_items
    ))
    _check(checks, "condition_derived_from_situated_inputs", all(
        all(
            row.get("condition_ref") in {
                "condition:target-visible:v1",
                "condition:target-complete:v1",
                "condition:target-scale-adequate:v1",
                "condition:stable-relation:v1",
            }
            and row.get("status") in {"SATISFIED", "UNSATISFIED", "UNKNOWN"}
            and row.get("candidate_only") is True
            and row.get("self_state_refs")
            and row.get("field_state_refs")
            and row.get("target_refs")
            and row.get("relation_refs")
            and row.get("temporal_ref")
            and row.get("source_refs")
            for row in (item.get("perception", {}).get("condition_candidates") or ())
        )
        for item in all_items
    ))
    _check(checks, "unknown_condition_not_satisfied", all(
        not set(_state(item).get("satisfied_condition_refs", ())) & {
            ref for ref, condition in _condition_map(item).items() if condition.get("status") == "UNKNOWN"
        }
        and not set((_result(item).get("feasibility") or {}).get("satisfied_condition_refs", ())) & {
            ref for ref, condition in _condition_map(item).items() if condition.get("status") == "UNKNOWN"
        }
        for item in all_items
    ))

    visible = grouped.get("TARGET_BECOMES_VISIBLE") or []
    _check(checks, "target_visibility_change_changes_condition", len(visible) == 2 and
           _condition_map(visible[0]).get("condition:target-visible:v1", {}).get("status") == "UNSATISFIED" and
           _condition_map(visible[1]).get("condition:target-visible:v1", {}).get("status") == "SATISFIED" and
           (_result(visible[0]).get("feasibility") or {}).get("status") == "NOT_FEASIBLE" and
           (_result(visible[1]).get("feasibility") or {}).get("status") == "FEASIBLE")
    stable = grouped.get("RELATION_BECOMES_STABLE") or []
    _check(checks, "relative_stability_change_changes_condition", len(stable) == 2 and
           _condition_map(stable[0]).get("condition:stable-relation:v1", {}).get("status") == "UNSATISFIED" and
           _condition_map(stable[1]).get("condition:stable-relation:v1", {}).get("status") == "SATISFIED" and
           (_result(stable[0]).get("feasibility") or {}).get("status") == "NOT_FEASIBLE" and
           (_result(stable[1]).get("feasibility") or {}).get("status") == "FEASIBLE")
    _check(checks, "same_need_different_situated_state_changes_feasibility", len(grouped.get("SAME_INFORMATION_NEED_DIFFERENT_SITUATED_STATE") or []) == 2 and
           (_result((grouped.get("SAME_INFORMATION_NEED_DIFFERENT_SITUATED_STATE") or [{}, {}])[0]).get("feasibility", {}).get("status") !=
            _result((grouped.get("SAME_INFORMATION_NEED_DIFFERENT_SITUATED_STATE") or [{}, {}])[1]).get("feasibility", {}).get("status")))
    _check(checks, "minimum_conditions_consumed", all(
        set((_result(item).get("feasibility") or {}).get("satisfied_condition_refs", ())) |
        set((_result(item).get("feasibility") or {}).get("unsatisfied_condition_refs", ())) |
        set((_result(item).get("feasibility") or {}).get("unknown_condition_refs", ())) ==
        set((_result(item).get("request", {}).get("minimum_condition_requirement") or {}).get("required_condition_refs", ()))
        for item in all_items
    ))
    _check(checks, "condition_gap_generated_from_derived_state", all(
        all(
            gap.get("missing_condition_ref") in _condition_map(item)
            and _state(item).get("situated_state_ref") in set(gap.get("trace_refs") or ())
            for gap in (_result(item).get("condition_gaps") or ())
        )
        for item in all_items
    ))
    _check(checks, "derived_state_satisfaction_matches_candidates", all(
        set(_state(item).get("satisfied_condition_refs", ())) == {
            ref for ref, condition in _condition_map(item).items() if condition.get("status") == "SATISFIED"
        }
        for item in all_items
    ))
    unknown_item = (grouped.get("UNKNOWN_STATE_DOES_NOT_PASS") or [{}])[0]
    _check(checks, "unknown_state_does_not_pass", (_result(unknown_item).get("feasibility") or {}).get("status") == "NOT_FEASIBLE")
    not_needed = (grouped.get("OBSERVATION_NOT_NECESSARY_FROM_SITUATED_INPUT") or [{}])[0]
    _check(checks, "need_false_does_not_eligible", (_result(not_needed).get("eligibility") or {}).get("eligible_now") is False)
    _check(checks, "scenario_id_not_semantic_driver", summary.get("scenario_id_semantic_driver") is False)
    _check(checks, "cycle_index_not_semantic_driver", summary.get("cycle_index_semantic_driver") is False)
    _check(checks, "self_does_not_own_capability_decision", all((_result(item).get("behavior") or {}).get("self_owns_capability_decision") is False for item in all_items))
    _check(checks, "no_provider_invocation", summary.get("forbidden_behaviors", {}).get("provider_invocation") is False)
    _check(checks, "no_model_invocation", summary.get("forbidden_behaviors", {}).get("model_invocation") is False)
    _check(checks, "no_decision_execution", summary.get("forbidden_behaviors", {}).get("decision_execution") is False)
    _check(checks, "no_task_execution", summary.get("forbidden_behaviors", {}).get("task_execution") is False)
    _check(checks, "no_action_execution", summary.get("forbidden_behaviors", {}).get("action_execution") is False)
    _check(checks, "no_device_control", summary.get("forbidden_behaviors", {}).get("device_control") is False)
    _check(checks, "no_device_control_perception", all(
        (item.get("perception", {}).get("behavior") or {}).get("device_control") is False
        for item in all_items
    ))
    _check(checks, "no_device_control_precondition_result", all(
        (_result(item).get("behavior") or {}).get("device_control") is False
        for item in all_items
    ))
    _check(checks, "no_world_truth", summary.get("forbidden_behaviors", {}).get("world_truth_declared") is False)
    _check(checks, "no_field_mutation", summary.get("forbidden_behaviors", {}).get("field_mutation") is False)
    _check(checks, "candidate_only", all(item.get("perception", {}).get("candidate_only") is True and _result(item).get("candidate_only") is True for item in all_items))
    _check(checks, "traceability_complete", all(_trace_complete(item) for item in all_items))
    _check(checks, "validation_errors_empty", not summary.get("validation_errors") and all(not _result(item).get("validation_errors") for item in all_items))

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "failed_checks": failed,
        "checks": checks,
        "controlled_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "NOT_APPLICABLE_CONTROLLED_ONLY",
        "final_decision": "NOT_APPLICABLE",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failed else "CONTROLLED_VERIFICATION_FAILED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify derived situated condition candidates.")
    parser.add_argument("summary", nargs="?", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    if not args.summary.exists():
        print(json.dumps({"all_checks_passed": False, "failed_checks": [f"summary_not_found:{args.summary}"]}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_passed"] else 1)


if __name__ == "__main__":
    main()
