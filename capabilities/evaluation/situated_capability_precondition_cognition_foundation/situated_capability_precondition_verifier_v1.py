"""Fail-closed verifier for controlled situated capability preconditions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-Situated-Capability-Precondition-Cognition-Foundation-v1-001"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
DEFAULT_SUMMARY = ROOT / "_eval_out/situated_capability_precondition_cognition_foundation_v1/runner_summary_v1.json"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _group(summary: Dict[str, Any]) -> Dict[str, list]:
    grouped: Dict[str, list] = {}
    for item in summary.get("cases", ()):
        grouped.setdefault(item.get("case_id"), []).append(item)
    return grouped


def _trace_complete(item: Dict[str, Any]) -> bool:
    request = item.get("request") or {}
    need = request.get("capability_need") or {}
    definition = request.get("precondition_definition") or {}
    minimum = request.get("minimum_condition_requirement") or {}
    state = request.get("situated_state") or {}
    refs = set(item.get("trace_refs") or ()) | set(item.get("provenance_refs") or ())
    required = (
        item.get("necessity", {}).get("necessity_ref"),
        item.get("feasibility", {}).get("feasibility_ref"),
        item.get("opportunity", {}).get("opportunity_ref"),
        item.get("eligibility", {}).get("eligibility_ref"),
        need.get("capability_need_ref"),
        need.get("capability_requirement_ref"),
        definition.get("capability_requirement_ref"),
        definition.get("capability_ref"),
        minimum.get("requirement_ref"),
        minimum.get("information_need_ref"),
        state.get("situated_state_ref"),
        state.get("temporal_ref"),
    )
    return all(bool(ref) for ref in required) and len(refs) >= 2


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    grouped = _group(summary)
    expected = {
        "TEXT_PRESENCE_ONLY",
        "READ_PRIMARY_SIGN_TEXT",
        "SAME_CAPABILITY_DIFFERENT_INFORMATION_NEED",
    }
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_situated_state", summary.get("execution_mode") == "CONTROLLED_SITUATED_STATE")
    _check(checks, "required_cases", set(grouped) == expected)
    _check(checks, "no_provider_invocation", summary.get("provider_invocation") is False)
    _check(checks, "no_model_invocation", summary.get("model_invocation") is False)
    _check(checks, "scenario_id_not_semantic_driver", summary.get("scenario_id_semantic_driver") is False and summary.get("cycle_index_semantic_driver") is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))

    all_items = [item for values in grouped.values() for item in values]
    case_a = (grouped.get("TEXT_PRESENCE_ONLY") or [{}])[0]
    case_b = (grouped.get("READ_PRIMARY_SIGN_TEXT") or [{}])[0]
    contrast = grouped.get("SAME_CAPABILITY_DIFFERENT_INFORMATION_NEED") or []
    left = contrast[0] if len(contrast) > 0 else {}
    right = contrast[1] if len(contrast) > 1 else {}

    _check(checks, "same_capability_different_information_need_changes_conditions", len(contrast) == 2 and left.get("request", {}).get("precondition_definition", {}).get("capability_ref") == right.get("request", {}).get("precondition_definition", {}).get("capability_ref") and left.get("request", {}).get("minimum_condition_requirement", {}).get("information_need_ref") != right.get("request", {}).get("minimum_condition_requirement", {}).get("information_need_ref") and left.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs") != right.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs"))
    _check(checks, "condition_resolution_not_scenario_driven", summary.get("resolution_policy") == "information_need+goal+capability_supported_dimensions" and summary.get("scenario_id_semantic_driver") is False and all(item.get("request", {}).get("minimum_condition_requirement", {}).get("requirement_ref", "").startswith("minimum-situated-condition-requirement:information:") for item in all_items))
    _check(checks, "minimum_conditions_feed_feasibility", all(item.get("feasibility", {}).get("minimum_condition_requirement_ref") == (item.get("request", {}).get("minimum_condition_requirement") or {}).get("requirement_ref") and (set(item.get("feasibility", {}).get("satisfied_condition_refs", ())) | set(item.get("feasibility", {}).get("unsatisfied_condition_refs", ()))) == set((item.get("request", {}).get("minimum_condition_requirement") or {}).get("required_condition_refs", ())) for item in all_items))
    _check(checks, "weaker_requirement_does_not_inherit_stronger_conditions", case_a.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs") == ["condition:target-visible:v1"] and case_a.get("feasibility", {}).get("status") == "FEASIBLE")
    _check(checks, "stronger_information_need_requires_materially_stronger_conditions", len(set(case_b.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs", ()))) > len(set(case_a.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs", ()))) and set(case_a.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs", ())).issubset(set(case_b.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs", ()))))
    _check(checks, "capability_definition_does_not_own_current_cognitive_need", len({tuple(item.get("request", {}).get("precondition_definition", {}).get("supported_condition_refs", ())) for item in all_items}) == 1 and all(not item.get("request", {}).get("precondition_definition", {}).get("required_condition_refs") for item in all_items) and len({tuple(item.get("request", {}).get("minimum_condition_requirement", {}).get("required_condition_refs", ())) for item in all_items}) > 1)
    _check(checks, "self_does_not_own_capability_decision", all((item.get("behavior") or {}).get("self_owns_capability_decision") is False for item in all_items))
    _check(checks, "field_not_mutated", summary.get("forbidden_behaviors", {}).get("field_mutation") is False)
    _check(checks, "no_world_truth", summary.get("forbidden_behaviors", {}).get("world_truth_declared") is False)
    _check(checks, "no_provider_invocation_per_case", all((item.get("behavior") or {}).get("provider_invocation") is False for item in all_items))
    _check(checks, "no_model_invocation_per_case", all((item.get("behavior") or {}).get("model_invocation") is False for item in all_items))
    _check(checks, "no_decision_execution", summary.get("forbidden_behaviors", {}).get("decision_execution") is False)
    _check(checks, "no_task_execution", summary.get("forbidden_behaviors", {}).get("task_execution") is False)
    _check(checks, "no_action_execution", summary.get("forbidden_behaviors", {}).get("action_execution") is False)
    _check(checks, "no_device_control", summary.get("forbidden_behaviors", {}).get("device_control") is False)
    _check(checks, "candidate_only", all(item.get("candidate_only") is True for item in all_items))
    _check(checks, "traceability_complete", all(_trace_complete(item) for item in all_items))
    _check(checks, "validation_errors_empty_per_case", all(not item.get("validation_errors") for item in all_items))

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "failed_checks": failed,
        "checks": checks,
        "controlled_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "NOT_APPLICABLE_EXECUTION_NOT_REQUESTED",
        "final_decision": "NOT_APPLICABLE",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failed else "CONTROLLED_VERIFICATION_FAILED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled situated capability precondition cases.")
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
