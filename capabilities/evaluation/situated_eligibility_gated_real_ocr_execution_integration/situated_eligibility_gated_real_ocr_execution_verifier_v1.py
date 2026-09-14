"""Fail-closed verifier for Situated Eligibility gated real OCR."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-Situated-Eligibility-Gated-Real-OCR-Execution-Integration-v1-001"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
DEFAULT_SUMMARY = ROOT / "_eval_out/situated_eligibility_gated_real_ocr_execution_integration_v1/runner_summary_v1.json"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _group(summary: Dict[str, Any]) -> Dict[str, list]:
    grouped: Dict[str, list] = {}
    for item in summary.get("records", ()):
        grouped.setdefault(item.get("case_id"), []).append(item)
    return grouped


def _pre(item: Dict[str, Any]) -> Dict[str, Any]:
    return item.get("situated_precondition_result") or {}


def _admission(item: Dict[str, Any]) -> Dict[str, Any]:
    return item.get("execution_admission") or {}


def _runtime(item: Dict[str, Any]) -> Dict[str, Any]:
    return item.get("runtime_result") or {}


def _eligible(item: Dict[str, Any]) -> bool:
    return (_pre(item).get("eligibility") or {}).get("eligible_now") is True


def _provider_request(item: Dict[str, Any]) -> Dict[str, Any]:
    return _runtime(item).get("provider_request") or {}


def _provider_result(item: Dict[str, Any]) -> Dict[str, Any]:
    return _runtime(item).get("provider_result") or {}


def _trace_complete(item: Dict[str, Any]) -> bool:
    pre = _pre(item)
    request = pre.get("request") or {}
    need = request.get("capability_need") or {}
    minimum = request.get("minimum_condition_requirement") or {}
    state = request.get("situated_state") or {}
    admission = _admission(item)
    runtime = _runtime(item)
    provider_request = _provider_request(item)
    provider_result = _provider_result(item)
    required = (
        need.get("goal_ref"),
        need.get("information_need_ref"),
        need.get("capability_requirement_ref"),
        minimum.get("requirement_ref"),
        state.get("situated_state_ref"),
        (pre.get("feasibility") or {}).get("feasibility_ref"),
        (pre.get("opportunity") or {}).get("opportunity_ref"),
        (pre.get("eligibility") or {}).get("eligibility_ref"),
        admission.get("admission_ref"),
    )
    if not all(bool(ref) for ref in required):
        return False
    if not _eligible(item):
        return True
    runtime_required = (
        provider_request.get("provider_request_ref"),
        provider_request.get("capability_requirement_ref"),
        provider_request.get("provider_ref"),
        provider_request.get("model_ref"),
        provider_result.get("provider_result_ref"),
        runtime.get("runtime_observation_ref"),
        runtime.get("gateway_admission_ref"),
        runtime.get("a_route_execution_ref"),
    )
    return all(bool(ref) for ref in runtime_required)


def _same_cognitive_need(left: Dict[str, Any], right: Dict[str, Any]) -> bool:
    left_request = (_pre(left).get("request") or {})
    right_request = (_pre(right).get("request") or {})
    left_need = left_request.get("capability_need") or {}
    right_need = right_request.get("capability_need") or {}
    return all(
        left_need.get(field) == right_need.get(field)
        for field in (
            "goal_ref",
            "intent_ref",
            "concern_ref",
            "information_need_ref",
            "capability_requirement_ref",
            "required_information_refs",
        )
    )


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    grouped = _group(summary)
    all_items = [item for values in grouped.values() for item in values]
    expected = {
        "SITUATED_INELIGIBLE_BLOCKS_REAL_OCR",
        "SITUATED_ELIGIBLE_ALLOWS_REAL_OCR",
        "DYNAMIC_SITUATED_STATE_OPENS_REAL_OCR_GATE",
        "OBSERVATION_NOT_NECESSARY_BLOCKS_REAL_OCR",
    }
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "live_runtime", summary.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "required_cases", set(grouped) == expected)
    _check(checks, "same_source", len({item.get("source_ref") for item in all_items}) == 1)
    _check(checks, "situated_eligibility_precedes_provider_execution", all(
        "SITUATED_ELIGIBILITY" in (item.get("execution_events") or ())
        and (
            not item.get("provider_real_execution_attempted")
            or (item.get("execution_events") or ()).index("SITUATED_ELIGIBILITY") <
            (item.get("execution_events") or ()).index("REAL_PROVIDER_INVOCATION")
        )
        for item in all_items
    ))

    ineligible = (grouped.get("SITUATED_INELIGIBLE_BLOCKS_REAL_OCR") or [{}])[0]
    _check(checks, "ineligible_blocks_provider_execution", not _eligible(ineligible) and _admission(ineligible).get("provider_execution_admitted") is False)
    _check(checks, "ineligible_provider_attempted_false", ineligible.get("provider_real_execution_attempted") is False)
    _check(checks, "ineligible_provider_invoked_false", ineligible.get("provider_invoked") is False)
    _check(checks, "ineligible_model_invoked_false", ineligible.get("model_invoked") is False)
    _check(checks, "ineligible_no_runtime_call_result", ineligible.get("runtime_result") is None)

    eligible = (grouped.get("SITUATED_ELIGIBLE_ALLOWS_REAL_OCR") or [{}])[0]
    _check(checks, "eligible_allows_provider_execution", _eligible(eligible) and _admission(eligible).get("provider_execution_admitted") is True)
    _check(checks, "eligible_real_provider_attempted_true", eligible.get("provider_real_execution_attempted") is True)
    _check(checks, "eligible_provider_invoked_true", eligible.get("provider_invoked") is True)
    _check(checks, "eligible_model_invoked_true", eligible.get("model_invoked") is True)
    _check(checks, "eligible_recorded_result_false", eligible.get("recorded_provider_result_used") is False)
    _check(checks, "eligible_canonical_provider_model", _provider_request(eligible).get("provider_ref") == "provider:ocr_v1" and _provider_request(eligible).get("model_ref") == "model:ocr_v1" and _provider_result(eligible).get("provider_ref") == "provider:ocr_v1" and _provider_result(eligible).get("model_ref") == "model:ocr_v1")
    _check(checks, "eligible_result_success_or_empty_success", _provider_result(eligible).get("status") in {"SUCCESS", "EMPTY_SUCCESS"})
    _check(checks, "gateway_admission_present_after_real_execution", bool(_runtime(eligible).get("gateway_admission_ref")))
    _check(checks, "evidence_candidate_present_after_real_execution", bool(_runtime(eligible).get("evidence_refs")))
    _check(checks, "cognitive_state_present_after_real_execution", bool((_runtime(eligible).get("cognitive_proof") or {})))

    dynamic = grouped.get("DYNAMIC_SITUATED_STATE_OPENS_REAL_OCR_GATE") or []
    dynamic_by_state = {item.get("state_id"): item for item in dynamic}
    t0 = dynamic_by_state.get("t0", {})
    t1 = dynamic_by_state.get("t1", {})
    _check(checks, "dynamic_same_cognitive_need", len(dynamic) == 2 and _same_cognitive_need(t0, t1))
    _check(checks, "dynamic_t0_ineligible", len(dynamic) == 2 and not _eligible(t0))
    _check(checks, "dynamic_t0_provider_not_invoked", len(dynamic) == 2 and t0.get("provider_invoked") is False and t0.get("runtime_result") is None)
    _check(checks, "dynamic_t1_eligible", len(dynamic) == 2 and _eligible(t1))
    _check(checks, "dynamic_t1_provider_invoked", len(dynamic) == 2 and t1.get("provider_invoked") is True and t1.get("model_invoked") is True)
    # The Runner's top-level counts aggregate independent eligible cases too.
    # The dynamic invariant is scoped to this case's t0/t1 records only.
    dynamic_provider_invocation_count = sum(
        1
        for item in dynamic
        if item.get("provider_real_execution_attempted") is True
        and item.get("provider_invoked") is True
        and item.get("model_invoked") is True
    )
    dynamic_model_invocation_count = sum(
        1
        for item in dynamic
        if item.get("provider_real_execution_attempted") is True
        and item.get("provider_invoked") is True
        and item.get("model_invoked") is True
    )
    _check(
        checks,
        "dynamic_real_provider_invocation_count_one",
        dynamic_provider_invocation_count == 1
        and dynamic_model_invocation_count == 1,
    )

    not_required = (grouped.get("OBSERVATION_NOT_NECESSARY_BLOCKS_REAL_OCR") or [{}])[0]
    _check(checks, "not_required_blocks_provider_execution", (_pre(not_required).get("necessity") or {}).get("status") == "NOT_REQUIRED" and _admission(not_required).get("provider_execution_admitted") is False and not_required.get("provider_invoked") is False)
    _check(checks, "minimum_conditions_feed_situated_feasibility", all(
        (_pre(item).get("feasibility") or {}).get("minimum_condition_requirement_ref") ==
        ((_pre(item).get("request") or {}).get("minimum_condition_requirement") or {}).get("requirement_ref")
        and bool(((_pre(item).get("request") or {}).get("situated_state") or {}).get("condition_state_candidates"))
        for item in all_items
    ))
    _check(checks, "derived_conditions_feed_eligibility", all(
        (_pre(item).get("eligibility") or {}).get("eligible_now") == bool(
            (_pre(item).get("necessity") or {}).get("status") == "REQUIRED"
            and (_pre(item).get("feasibility") or {}).get("status") == "FEASIBLE"
            and (_pre(item).get("opportunity") or {}).get("status") == "OPEN"
            and (_pre(item).get("request") or {}).get("capability_available_candidate") is True
        )
        for item in all_items
    ))
    _check(checks, "provider_runtime_admission_not_bypassed", all(
        (not _eligible(item)) or (_provider_request(item).get("execution_mode") == "LIVE_RUNTIME" and _admission(item).get("provider_execution_admitted") is True)
        for item in all_items
    ))

    _check(checks, "irrelevant_evidence_does_not_cover_required_information", all(
        not (
            any(str(value).startswith("IRRELEVANT") for value in ((_runtime(item).get("cognitive_proof") or {}).get("conditioned_evidence_relevance") or ()))
            and (_runtime(item).get("sufficiency_status") == "SUFFICIENT")
            and not ((_runtime(item).get("cognitive_proof") or {}).get("conditioned_missing_information_refs") or ())
        )
        for item in all_items if _eligible(item) and _runtime(item)
    ))
    _check(checks, "candidate_only", all(
        _pre(item).get("candidate_only") is True
        and _admission(item).get("candidate_only") is True
        and (_runtime(item).get("provider_result") or {}).get("candidate_only", True) is True
        for item in all_items
    ))
    _check(checks, "no_world_truth", summary.get("forbidden_behaviors", {}).get("world_truth_declared") is False)
    _check(checks, "no_field_mutation", summary.get("forbidden_behaviors", {}).get("field_mutation") is False)
    _check(checks, "no_decision_execution", summary.get("forbidden_behaviors", {}).get("decision_execution") is False)
    _check(checks, "no_task_execution", summary.get("forbidden_behaviors", {}).get("task_execution") is False)
    _check(checks, "no_action_execution", summary.get("forbidden_behaviors", {}).get("action_execution") is False)
    _check(checks, "no_device_control", summary.get("forbidden_behaviors", {}).get("device_control") is False)
    _check(checks, "no_camera_control", summary.get("forbidden_behaviors", {}).get("camera_control") is False)
    _check(checks, "no_movement_control", summary.get("forbidden_behaviors", {}).get("movement_control") is False)
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False and all(item.get("recorded_provider_result_used") is False for item in all_items))
    _check(checks, "traceability_complete", all(_trace_complete(item) for item in all_items))
    _check(checks, "validation_errors_empty", not summary.get("validation_errors") and all(not item.get("validation_errors") and not (_runtime(item).get("errors") if _runtime(item) else ()) for item in all_items))

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "failed_checks": failed,
        "checks": checks,
        "operational_result": "PASS" if not failed else "FAIL",
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "final_decision": "NOT_APPLICABLE",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failed else "VERIFICATION_FAILED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Situated Eligibility gated real OCR execution.")
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
