"""Fail-closed verifier for bounded Dynamic Situated Observation regulation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


PHASE = "Phase-P1-Luna-Dynamic-Situated-Observation-Regulation-Loop-Integration-v1-001"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
DEFAULT_SUMMARY = ROOT / "_eval_out/dynamic_situated_observation_regulation_loop_integration_v1/runner_summary_v1.json"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _states(summary: Dict[str, Any], case_id: str) -> List[Dict[str, Any]]:
    for case in summary.get("cases", ()):
        if case.get("case_id") == case_id:
            return list(case.get("states") or ())
    return []


def _pre(state: Dict[str, Any]) -> Dict[str, Any]:
    return state.get("situated_precondition_result") or {}


def _feasibility(state: Dict[str, Any]) -> Dict[str, Any]:
    return _pre(state).get("feasibility") or {}


def _opportunity(state: Dict[str, Any]) -> Dict[str, Any]:
    return _pre(state).get("opportunity") or {}


def _eligibility(state: Dict[str, Any]) -> Dict[str, Any]:
    return _pre(state).get("eligibility") or {}


def _admission(state: Dict[str, Any]) -> Dict[str, Any]:
    return state.get("execution_admission") or {}


def _runtime(state: Dict[str, Any]) -> Dict[str, Any]:
    return state.get("provider_runtime_result") or {}


def _runtime_provider_request(state: Dict[str, Any]) -> Dict[str, Any]:
    return _runtime(state).get("provider_request") or {}


def _runtime_provider_result(state: Dict[str, Any]) -> Dict[str, Any]:
    return _runtime(state).get("provider_result") or {}


def _all_states(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [state for case in summary.get("cases", ()) for state in case.get("states", ())]


def _same_need(states: Iterable[Dict[str, Any]]) -> bool:
    values = list(states)
    if not values:
        return False
    semantic_keys = (
        "goal_ref",
        "intent_ref",
        "concern_ref",
        "information_need_ref",
        "capability_requirement_ref",
        "required_information_refs",
    )

    def semantic_value(state: Dict[str, Any], key: str) -> Any:
        if key in state:
            return state.get(key)
        need = ((_pre(state).get("request") or {}).get("capability_need") or {})
        return need.get(key)

    return all(
        all(semantic_value(state, key) == semantic_value(values[0], key) for key in semantic_keys)
        for state in values
    )


def _source_ref(state: Dict[str, Any]) -> str | None:
    request = (_pre(state).get("request") or {})
    refs = request.get("source_refs") or ()
    return refs[0] if refs else None


def _has_current_adjustment_only(state: Dict[str, Any]) -> bool:
    pre = _pre(state)
    gaps = pre.get("condition_gaps") or ()
    adjustments = pre.get("adjustment_needs") or ()
    gap_refs = {gap.get("condition_gap_ref") for gap in gaps}
    adjustment_gap_refs = {item.get("condition_gap_ref") for item in adjustments}
    satisfied = set((_feasibility(state).get("satisfied_condition_refs") or ()))
    active_missing = {
        gap.get("missing_condition_ref")
        for gap in gaps
        if gap.get("condition_gap_ref") in adjustment_gap_refs
    }
    return adjustment_gap_refs == gap_refs and not active_missing.intersection(satisfied)


def _runtime_events_in_order(state: Dict[str, Any]) -> bool:
    events = list(state.get("execution_events") or ())
    required = ("SITUATED_STATE_REEVALUATED", "SITUATED_ELIGIBILITY_EVALUATED", "EXECUTION_ADMISSION", "PROVIDER_RUNTIME")
    positions = [events.index(event) for event in required if event in events]
    return len(positions) == len(required) and positions == sorted(positions)


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    expected_cases = {
        "CONDITION_GAP_WAITS_WITHOUT_PROVIDER",
        "DYNAMIC_CONDITION_CHANGE_OPENS_OBSERVATION",
        "MULTI_STATE_WAIT_THEN_OBSERVE_ONCE",
        "OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION",
        "OBSERVATION_NOT_REQUIRED_EXITS_REGULATION",
    }
    all_states = _all_states(summary)
    gap_case = _states(summary, "CONDITION_GAP_WAITS_WITHOUT_PROVIDER")
    dynamic_case = _states(summary, "DYNAMIC_CONDITION_CHANGE_OPENS_OBSERVATION")
    multi_case = _states(summary, "MULTI_STATE_WAIT_THEN_OBSERVE_ONCE")
    lost_case = _states(summary, "OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION")
    not_required_case = _states(summary, "OBSERVATION_NOT_REQUIRED_EXITS_REGULATION")

    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "live_runtime", summary.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "controlled_situated_state_mode", summary.get("situated_state_mode") == "CONTROLLED_SITUATED_STATE_CANDIDATES")
    _check(checks, "required_cases", {case.get("case_id") for case in summary.get("cases", ())} == expected_cases)
    _check(checks, "same_source", len({_source_ref(state) for state in all_states}) == 1)
    _check(checks, "same_information_need_across_regulation_states", _same_need(dynamic_case + multi_case + lost_case))
    _check(checks, "same_capability_requirement_across_regulation_states", _same_need(dynamic_case + multi_case + lost_case))

    _check(checks, "condition_gap_causes_wait", bool(gap_case) and gap_case[0].get("regulation_status") == "WAITING_FOR_CONDITION_CHANGE" and bool(gap_case[0].get("condition_gap_refs")))
    _check(checks, "adjustment_need_matches_current_gap", all(_has_current_adjustment_only(state) for state in all_states))
    _check(
        checks,
        "stale_adjustment_not_active",
        all(
            all(
                ref not in (_feasibility(state).get("satisfied_condition_refs") or ())
                for ref in (
                    gap.get("missing_condition_ref")
                    for gap in (_pre(state).get("condition_gaps") or ())
                )
            )
            for state in all_states
        ),
    )

    waiting_states = [state for state in all_states if state.get("regulation_status") == "WAITING_FOR_CONDITION_CHANGE"]
    _check(checks, "waiting_state_provider_not_invoked", all(state.get("provider_invoked") is False for state in waiting_states))
    _check(checks, "waiting_state_model_not_invoked", all(state.get("model_invoked") is False for state in waiting_states))
    _check(checks, "waiting_state_provider_attempted_false", all(state.get("provider_real_execution_attempted") is False for state in waiting_states))

    _check(checks, "state_change_drives_feasibility_change", (
        len(dynamic_case) == 2
        and _feasibility(dynamic_case[0]).get("status") == "NOT_FEASIBLE"
        and _feasibility(dynamic_case[1]).get("status") == "FEASIBLE"
        and len(multi_case) == 3
        and _feasibility(multi_case[0]).get("status") == "NOT_FEASIBLE"
        and _feasibility(multi_case[1]).get("status") == "NOT_FEASIBLE"
        and _feasibility(multi_case[2]).get("status") == "FEASIBLE"
        and len(lost_case) == 3
        and _feasibility(lost_case[1]).get("status") == "FEASIBLE"
        and _feasibility(lost_case[2]).get("status") == "NOT_FEASIBLE"
    ))
    _check(checks, "opportunity_opens_when_conditions_met", bool(dynamic_case) and _opportunity(dynamic_case[-1]).get("status") == "OPEN" and bool(multi_case) and _opportunity(multi_case[-1]).get("status") == "OPEN" and bool(lost_case) and _opportunity(lost_case[1]).get("status") == "OPEN")
    _check(checks, "opportunity_closes_when_conditions_lost", len(lost_case) == 3 and _opportunity(lost_case[2]).get("status") == "CLOSED")
    _check(checks, "stale_opportunity_does_not_authorize_provider_execution", len(lost_case) == 3 and lost_case[1].get("execution_admission") is None and lost_case[1].get("provider_invoked") is False and lost_case[2].get("provider_execution_admitted") is False and lost_case[2].get("provider_invoked") is False)

    _check(checks, "eligibility_precedes_execution_admission", all(
        not state.get("execution_admission")
        or _admission(state).get("eligible_now") == _eligibility(state).get("eligible_now")
        for state in all_states
    ))
    _check(checks, "execution_admission_precedes_provider_runtime", all(
        not state.get("provider_real_execution_attempted")
        or (_admission(state).get("provider_execution_admitted") is True and _runtime_events_in_order(state))
        for state in all_states
    ))

    _check(checks, "dynamic_single_real_provider_invocation", len(dynamic_case) == 2 and sum(state.get("provider_invocation_count", 0) for state in dynamic_case) == 1 and dynamic_case[0].get("provider_invocation_count") == 0 and dynamic_case[1].get("provider_invocation_count") == 1)
    _check(checks, "multi_state_wait_invokes_provider_once", len(multi_case) == 3 and [state.get("provider_invocation_count") for state in multi_case] == [0, 0, 1] and sum(state.get("provider_invocation_count", 0) for state in multi_case) == 1)
    _check(checks, "observation_cycle_count_matches_real_invocations", all(
        case.get("observation_cycle_count") == sum(state.get("provider_invocation_count", 0) for state in case.get("states", ()))
        for case in summary.get("cases", ())
    ))
    _check(checks, "regulation_and_cognitive_cycles_are_distinct", (
        len(multi_case) == 3
        and multi_case[2].get("cycle_index") == 2
        and multi_case[2].get("observation_cycle_index") == 1
    ))
    _check(checks, "not_required_exits_without_provider", len(not_required_case) == 1 and not_required_case[0].get("regulation_status") == "OBSERVATION_NOT_REQUIRED" and not_required_case[0].get("provider_invocation_count") == 0 and not_required_case[0].get("adjustment_need_refs") == [])

    executed_states = [state for state in all_states if state.get("provider_invocation_count") == 1]
    _check(checks, "real_provider_invoked_when_currently_eligible", bool(executed_states) and all(_eligibility(state).get("eligible_now") is True and state.get("provider_invoked") is True and state.get("model_invoked") is True and state.get("provider_real_execution_attempted") is True and state.get("provider_real_execution_verified") is True for state in executed_states))
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False and all(state.get("recorded_provider_result_used") is False for state in all_states))
    _check(checks, "canonical_provider_model", all(
        _runtime_provider_request(state).get("provider_ref") == "provider:ocr_v1"
        and _runtime_provider_request(state).get("model_ref") == "model:ocr_v1"
        and _runtime_provider_result(state).get("provider_ref") == "provider:ocr_v1"
        and _runtime_provider_result(state).get("model_ref") == "model:ocr_v1"
        for state in executed_states
    ))
    _check(checks, "gateway_admission_present", all(bool(state.get("gateway_admission_ref")) for state in executed_states))
    _check(checks, "evidence_candidate_present", all(bool(state.get("evidence_refs")) for state in executed_states))
    _check(checks, "cognitive_state_present", all(bool(state.get("cognitive_state_ref")) and bool(state.get("a_route_execution_ref")) for state in executed_states))
    _check(checks, "post_observation_sufficiency_present", all(bool(state.get("sufficiency_ref")) and state.get("sufficiency_status") in {"SUFFICIENT", "INSUFFICIENT"} for state in executed_states))
    _check(checks, "sufficient_state_does_not_continue_observation", all(
        not any(state.get("regulation_status") == "INFORMATION_SUFFICIENT" for state in case.get("states", ())[:-1])
        for case in summary.get("cases", ())
    ))

    _check(checks, "scenario_id_not_semantic_driver", summary.get("scenario_id_semantic_driver") is False and all((_pre(state).get("behavior") or {}).get("scenario_id_semantic_driver") is False for state in all_states))
    _check(checks, "cycle_index_not_semantic_driver", summary.get("cycle_index_semantic_driver") is False and all((_pre(state).get("behavior") or {}).get("cycle_index_semantic_driver") is False for state in all_states))

    forbidden = summary.get("forbidden_behaviors") or {}
    forbidden_names = (
        "decision_execution", "task_execution", "action_execution", "device_control",
        "camera_control", "movement_control", "field_mutation", "world_truth_declared",
        "memory_mutation", "autonomous_background_loop",
    )
    _check(checks, "candidate_only", all(
        state.get("candidate_only") is True
        and _pre(state).get("candidate_only") is True
        and (not state.get("execution_admission") or _admission(state).get("candidate_only") is True)
        and (not state.get("provider_runtime_result") or (_runtime_provider_result(state).get("candidate_only", True) is True and _runtime_provider_result(state).get("truth_declared", False) is False))
        for state in all_states
    ))
    _check(checks, "no_forbidden_behaviors", all(forbidden.get(name) is False for name in forbidden_names))
    _check(checks, "no_world_truth", forbidden.get("world_truth_declared") is False)
    _check(checks, "no_field_mutation", forbidden.get("field_mutation") is False)
    _check(checks, "no_decision_execution", forbidden.get("decision_execution") is False)
    _check(checks, "no_task_execution", forbidden.get("task_execution") is False)
    _check(checks, "no_action_execution", forbidden.get("action_execution") is False)
    _check(checks, "no_device_control", forbidden.get("device_control") is False)
    _check(checks, "no_camera_control", forbidden.get("camera_control") is False)
    _check(checks, "no_movement_control", forbidden.get("movement_control") is False)
    _check(checks, "traceability_complete", all(
        bool(state.get("regulation_ref"))
        and bool(state.get("current_situated_state_ref"))
        and bool(state.get("feasibility_ref"))
        and bool(state.get("opportunity_ref"))
        and bool(state.get("eligibility_ref"))
        and bool(state.get("trace_refs"))
        and bool(state.get("provenance_refs"))
        and (state.get("previous_regulation_ref") is not None or state.get("state_id") == "t0")
        for state in all_states
    ))
    _check(checks, "validation_errors_empty", not summary.get("validation_errors") and all(not state.get("validation_errors") and not (_runtime(state).get("errors") if _runtime(state) else ()) for state in all_states))

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "failed_checks": failed,
        "checks": checks,
        "controlled_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "NOT_APPLICABLE",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failed else "VERIFICATION_FAILED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify bounded Dynamic Situated Observation regulation.")
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    print(json.dumps(verify(summary), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["verify"]
