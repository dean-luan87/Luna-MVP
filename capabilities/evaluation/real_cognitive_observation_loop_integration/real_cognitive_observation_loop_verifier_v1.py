"""Fail-closed user-terminal Verifier for the real cognitive observation loop."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import GOVERNANCE_ASSERTION_IDS


ROOT = next(
    candidate
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents)
    if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md"))
)
DEFAULT_SUMMARY = ROOT / "_eval_out/real_cognitive_observation_loop_integration_v1/runner_summary_v1.json"


def _check(checks: Dict[str, bool], name: str, passed: bool) -> None:
    checks[name] = bool(passed)


def _cycle_base(cycle: Dict[str, Any]) -> bool:
    native = cycle.get("provider_native_result") or {}
    runtime = cycle.get("provider_runtime_result") or {}
    output_candidate = runtime.get("output_candidate") if isinstance(runtime, dict) else None
    return all(
        (
            cycle.get("execution_mode", "LIVE_RUNTIME") == "LIVE_RUNTIME",
            cycle.get("provider_real_execution_attempted") is True,
            cycle.get("provider_real_execution_verified") is True,
            cycle.get("provider_invoked") is True,
            cycle.get("model_invoked") is True,
            cycle.get("recorded_provider_result_used") is False,
            cycle.get("runtime_observation_ref"),
            cycle.get("gateway_admission_ref"),
            cycle.get("evidence_refs"),
            cycle.get("provider_request_ref"),
            cycle.get("provider_result_ref"),
            cycle.get("execution_instance_ref"),
            native.get("provider_id") or native.get("provider_invoked") is True,
            output_candidate is None or output_candidate.get("candidate_only") is True,
            output_candidate is None or output_candidate.get("truth_declared") is False,
        )
    )


def _no_downstream(cycle: Dict[str, Any]) -> bool:
    route = cycle.get("a_route") or {}
    return not any(
        item.get("stage_id") in {"DECISION", "TASK", "ACTION", "EXECUTION"}
        for item in route.get("stage_results", ())
        if isinstance(item, dict)
    )


def _plane_g_passed(cycle: Dict[str, Any]) -> bool:
    plane_g = (cycle.get("plane_g") or {}).get("result") or {}
    assertion_results = plane_g.get("assertion_results") or ()
    return (
        plane_g.get("compliance_status") == "COMPLIANT"
        and {item.get("assertion_id") for item in assertion_results} == set(GOVERNANCE_ASSERTION_IDS)
        and all(item.get("status") == "PASS" and item.get("passed") is True for item in assertion_results)
    )


def _case_checks(case: Dict[str, Any]) -> Dict[str, bool]:
    checks: Dict[str, bool] = {}
    cycles = list(case.get("observation_cycles") or ())
    case_id = case.get("case_id")
    _check(checks, "live_runtime", case.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "goal_and_need_present", bool(case.get("goal_ref") and case.get("information_need_ref") and case.get("required_information_refs")))
    _check(checks, "semantic_driver_is_not_scenario_or_cycle", case.get("semantic_driver") == "goal+information_need+required_and_admitted_evidence")
    _check(checks, "cycle_count_bounded", 1 <= len(cycles) <= 2)
    _check(checks, "recorded_result_unused", case.get("recorded_result_used") is False)
    _check(checks, "case_validation_errors_empty", not case.get("validation_errors"))
    for index, cycle in enumerate(cycles, start=1):
        _check(checks, f"cycle_{index}_real_runtime_contract", _cycle_base(cycle))
        _check(checks, f"cycle_{index}_evidence_relevance_present", bool(cycle.get("conditioned_evidence_relevance")))
        _check(checks, f"cycle_{index}_candidate_only", all(
            item is False for item in (
                (cycle.get("forbidden_behaviors") or {}).get("world_truth_declared", False),
                (cycle.get("forbidden_behaviors") or {}).get("fact_admitted", False),
                (cycle.get("forbidden_behaviors") or {}).get("field_mutation", False),
            )
        ))
        _check(checks, f"cycle_{index}_route_stops_before_downstream", _no_downstream(cycle))
        _check(checks, f"cycle_{index}_plane_g", _plane_g_passed(cycle))

    if case_id == "REAL_SINGLE_CYCLE_SUFFICIENT":
        _check(checks, "case_a_one_cycle", len(cycles) == 1)
        cycle = cycles[0] if cycles else {}
        _check(checks, "case_a_real_text_evidence", bool(cycle.get("recognized_text_candidates")))
        _check(checks, "case_a_sufficient", cycle.get("sufficiency_status") == "SUFFICIENT")
        _check(checks, "case_a_stop", bool(cycle.get("stop_ref")) and cycle.get("stop_reason") == "MINIMUM_SUFFICIENT_INFORMATION_REACHED")
        _check(checks, "case_a_no_gap_or_reobservation", not cycle.get("information_gap_ref") and not cycle.get("reobservation_request_ref"))
        _check(checks, "case_a_no_post_sufficiency_reobservation", case.get("post_sufficiency_reobservation") is False)
    elif case_id == "REAL_REOBSERVATION_REQUIRED":
        first, second = cycles if len(cycles) == 2 else ({}, {})
        _check(checks, "case_b_two_cycles", len(cycles) == 2 and case.get("observation_cycle_count") == 2)
        _check(checks, "case_b_cycle_1_real_text_evidence", bool(first.get("recognized_text_candidates")))
        _check(checks, "case_b_cycle_1_insufficient", first.get("sufficiency_status") == "INSUFFICIENT")
        _check(checks, "case_b_specific_gap", first.get("information_gap_ref") and set((first.get("information_gap_candidate") or {}).get("missing_information_refs", ())) == {"information:platform-location-text:v1"})
        _check(checks, "case_b_gap_to_reobservation", bool(first.get("reobservation_request_ref") and first.get("next_cycle_ingress_ref")))
        _check(checks, "case_b_cycle_2_prior_gap_link", second.get("prior_information_gap_ref") == first.get("information_gap_ref"))
        _check(checks, "case_b_cycle_2_prior_reobservation_link", second.get("prior_reobservation_ref") == first.get("reobservation_request_ref"))
        _check(checks, "case_b_cycle_2_prior_ingress_link", second.get("prior_next_cycle_ingress_ref") == first.get("next_cycle_ingress_ref"))
        _check(checks, "case_b_new_runtime_and_evidence", second.get("runtime_observation_ref") != first.get("runtime_observation_ref") and set(second.get("evidence_refs", ())).isdisjoint(first.get("evidence_refs", ())))
        _check(checks, "case_b_revision", bool(second.get("hypothesis_revision_ref")) and second.get("previous_cognitive_state_ref"))
        _check(checks, "case_b_sufficient_and_stop", second.get("sufficiency_status") == "SUFFICIENT" and bool(second.get("stop_ref")))
        _check(checks, "case_b_transition", first.get("sufficiency_status") == "INSUFFICIENT" and second.get("sufficiency_status") == "SUFFICIENT")
        _check(checks, "case_b_gap_reduced", not second.get("conditioned_missing_information_refs") and second.get("empty_result") is False)
        _check(checks, "case_b_no_cycle_3", len(cycles) == 2 and case.get("post_sufficiency_reobservation") is False)
    else:
        _check(checks, "known_case", False)
    return checks


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = list(summary.get("cases") or ())
    _check(checks, "phase", summary.get("phase") == "Phase-P1-Luna-Real-Cognitive-Observation-Loop-Integration-v1-001")
    _check(checks, "live_runtime", summary.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "canonical_capability", summary.get("capability_ref") == "text_recognition")
    _check(checks, "canonical_provider", summary.get("provider_ref") == "provider:ocr_v1")
    _check(checks, "canonical_model", summary.get("model_ref") == "model:ocr_v1")
    _check(checks, "two_cases", {case.get("case_id") for case in cases} == {"REAL_SINGLE_CYCLE_SUFFICIENT", "REAL_REOBSERVATION_REQUIRED"})
    _check(checks, "global_recorded_result_unused", summary.get("recorded_result_used") is False)
    _check(checks, "global_validation_errors_empty", not summary.get("validation_errors"))
    forbidden = summary.get("forbidden_behaviors") or {}
    _check(checks, "global_forbidden_behaviors_closed", all(value is False for value in forbidden.values()))
    for case in cases:
        for name, passed in _case_checks(case).items():
            checks[f"{case.get('case_id')}:{name}"] = passed
    failed = [name for name, passed in checks.items() if not passed]
    operational = not failed and all(
        cycle.get("provider_real_execution_verified") is True
        for case in cases
        for cycle in case.get("observation_cycles", ())
    )
    cognitive = not failed and all(
        case.get("final_sufficiency") == "SUFFICIENT" and bool(case.get("final_stop"))
        for case in cases
    )
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "operational_result": "PASS" if operational else "FAIL",
        "cognitive_logic_result": "PASS" if cognitive else "FAIL",
        "final_decision": "GO" if operational and cognitive else "NOT_GO",
        "checks": checks,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    summary = json.loads(path.read_text(encoding="utf-8"))
    result = verify(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
