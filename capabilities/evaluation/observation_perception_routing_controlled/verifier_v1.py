"""Fail-closed verifier for candidate-only perception routing formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/observation_perception_routing_v1")
REQUIRED_CASES = {
    "SINGLE_DEMAND_SINGLE_CAPABILITY_SINGLE_ROUTE",
    "SINGLE_DEMAND_MULTIPLE_CAPABILITY_CANDIDATES",
    "TWO_INDEPENDENT_DEMANDS",
    "SAME_DEMAND_SAME_CLASS_TWO_CANDIDATES",
    "SAME_CAPABILITY_SUPPORTS_TWO_DEMANDS",
    "NO_OBSERVATION_DEMAND",
    "NO_CAPABILITY_REQUIREMENT",
    "NO_MATCHING_CAPABILITY",
    "CAPABILITY_UNAVAILABLE",
    "CAPABILITY_NOT_ADMITTED",
    "INVALID_RESOLUTION_CANDIDATE",
    "DEMAND_CAPABILITY_LINEAGE_MISMATCH",
    "SCENARIO_12_SIGNAGE",
    "SCENARIO_12_HUMAN_FLOW",
    "SCENARIO_12_BOTH_STRATEGIES",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
}


def _check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: Any = None) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _case(cases: dict[str, dict[str, Any]], case_id: str) -> dict[str, Any]:
    return cases.get(case_id, {})


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    cases_list = summary.get("cases") or []
    cases = {item.get("case_id"): item for item in cases_list}
    _check(checks, "required_cases_present", set(cases) == REQUIRED_CASES)
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_PERCEPTION_ROUTING_TEST")
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)
    _check(
        checks,
        "no_routing_or_downstream_execution",
        all(summary.get(key) is False for key in (
            "routing_executed", "routing_admitted", "route_priority_assigned",
            "route_ranking_executed", "route_winner_selected", "gateway_submission",
            "fpo_runtime_request", "provider_binding", "provider_invocation",
            "model_binding", "model_invocation", "capability_activation",
            "capability_reservation", "capability_scheduling", "observation_execution",
            "resource_scheduling", "resource_acquisition", "attention_formed",
            "evidence_ingress", "decision_formed", "task_formed", "action_formed",
        )),
    )
    _check(
        checks,
        "no_mutation_or_truth",
        all(summary.get(key) is False for key in (
            "truth_declared", "world_truth_declared", "current_world_mutation",
            "field_mutation", "memory_pcn_mutation",
        )),
    )

    expected = {
        "SINGLE_DEMAND_SINGLE_CAPABILITY_SINGLE_ROUTE": ("ROUTING_CANDIDATES_FORMED", 1),
        "SINGLE_DEMAND_MULTIPLE_CAPABILITY_CANDIDATES": ("ROUTING_CANDIDATES_FORMED", 2),
        "TWO_INDEPENDENT_DEMANDS": ("ROUTING_CANDIDATES_FORMED", 2),
        "SAME_DEMAND_SAME_CLASS_TWO_CANDIDATES": ("ROUTING_CANDIDATES_FORMED", 2),
        "SAME_CAPABILITY_SUPPORTS_TWO_DEMANDS": ("ROUTING_CANDIDATES_FORMED", 2),
        "NO_OBSERVATION_DEMAND": ("NO_ROUTING_CANDIDATE", 0),
        "NO_CAPABILITY_REQUIREMENT": ("NO_ROUTING_CANDIDATE", 0),
        "NO_MATCHING_CAPABILITY": ("NO_ROUTING_CANDIDATE", 0),
        "CAPABILITY_UNAVAILABLE": ("NO_ROUTING_CANDIDATE", 0),
        "CAPABILITY_NOT_ADMITTED": ("NO_ROUTING_CANDIDATE", 0),
        "INVALID_RESOLUTION_CANDIDATE": ("INVALID_INPUT", 0),
        "DEMAND_CAPABILITY_LINEAGE_MISMATCH": ("INVALID_INPUT", 0),
        "SCENARIO_12_SIGNAGE": ("ROUTING_CANDIDATES_FORMED", 1),
        "SCENARIO_12_HUMAN_FLOW": ("ROUTING_CANDIDATES_FORMED", 1),
        "SCENARIO_12_BOTH_STRATEGIES": ("ROUTING_CANDIDATES_FORMED", 2),
        "DETERMINISTIC_REPLAY": ("ROUTING_CANDIDATES_FORMED", 1),
        "MALFORMED_INPUT_SHAPE": ("INVALID_INPUT", 0),
    }
    for case_id, (status, count) in expected.items():
        item = _case(cases, case_id)
        result = item.get("result") or {}
        _check(checks, f"{case_id}:status", result.get("formation_status") == status)
        _check(checks, f"{case_id}:route_count", len(result.get("routes") or []) == count)
        _check(checks, f"{case_id}:expected_count", item.get("expected_route_count") == count)

    multiple = _case(cases, "SINGLE_DEMAND_MULTIPLE_CAPABILITY_CANDIDATES").get("result") or {}
    _check(
        checks,
        "multiple_capabilities_multiple_routes",
        len(multiple.get("routes") or []) == 2
        and multiple.get("route_winner_selected") is False
        and len({item.get("source_capability_resolution_candidate_ref") for item in multiple.get("routes")}) == 2,
    )
    _check(
        checks,
        "multiple_routes_no_winner",
        multiple.get("route_ranking_executed") is False
        and multiple.get("route_priority_assigned") is False,
    )

    independent = _case(cases, "TWO_INDEPENDENT_DEMANDS").get("result") or {}
    _check(
        checks,
        "two_demands_lineage_independent",
        len(independent.get("routes") or []) == 2
        and len({item.get("source_observation_demand_ref") for item in independent.get("routes")}) == 2
        and len({item.get("source_branch_ref") for item in independent.get("routes")}) == 2,
    )
    same_class = _case(cases, "SAME_DEMAND_SAME_CLASS_TWO_CANDIDATES").get("result") or {}
    same_class_routes = same_class.get("routes") or []
    _check(
        checks,
        "same_class_candidates_not_deduplicated",
        len(same_class_routes) == 2
        and len({item.get("source_observation_demand_ref") for item in same_class_routes}) == 1
        and len({item.get("capability_class_ref") for item in same_class_routes}) == 1
        and len({item.get("capability_candidate_ref") for item in same_class_routes}) == 2
        and len({item.get("source_capability_resolution_candidate_ref") for item in same_class_routes}) == 2
        and len({item.get("perception_routing_candidate_ref") for item in same_class_routes}) == 2,
    )
    shared = _case(cases, "SAME_CAPABILITY_SUPPORTS_TWO_DEMANDS").get("result") or {}
    _check(
        checks,
        "same_capability_multiple_demands_not_merged",
        len(shared.get("routes") or []) == 2
        and len({item.get("capability_candidate_ref") for item in shared.get("routes")}) == 1
        and len({item.get("source_observation_demand_ref") for item in shared.get("routes")}) == 2,
    )
    for case_id in (
        "NO_OBSERVATION_DEMAND", "NO_CAPABILITY_REQUIREMENT", "NO_MATCHING_CAPABILITY",
        "CAPABILITY_UNAVAILABLE", "CAPABILITY_NOT_ADMITTED",
    ):
        result = _case(cases, case_id).get("result") or {}
        _check(checks, f"{case_id}:zero_route", not result.get("routes"))

    _check(
        checks,
        "invalid_resolution_candidate_fails_closed",
        not (_case(cases, "INVALID_RESOLUTION_CANDIDATE").get("result") or {}).get("routes"),
    )
    _check(
        checks,
        "demand_capability_lineage_mismatch_fails_closed",
        not (_case(cases, "DEMAND_CAPABILITY_LINEAGE_MISMATCH").get("result") or {}).get("routes"),
    )
    _check(
        checks,
        "scenario12_signage_no_ocr_route_inference",
        all(
            "ocr" not in (route.get("capability_class_ref") or "").lower()
            and route.get("provider_binding") is False
            and route.get("model_binding") is False
            for route in ((_case(cases, "SCENARIO_12_SIGNAGE").get("result") or {}).get("routes") or [])
        ),
    )
    _check(
        checks,
        "scenario12_flow_no_model_route_inference",
        all(
            route.get("provider_binding") is False
            and route.get("model_binding") is False
            and "vlm" not in (route.get("capability_class_ref") or "").lower()
            for route in ((_case(cases, "SCENARIO_12_HUMAN_FLOW").get("result") or {}).get("routes") or [])
        ),
    )
    scenario12 = _case(cases, "SCENARIO_12_BOTH_STRATEGIES").get("result") or {}
    _check(
        checks,
        "scenario12_two_routes",
        len(scenario12.get("routes") or []) == 2
        and len({item.get("source_observation_demand_ref") for item in scenario12.get("routes")}) == 2,
    )

    all_routes = [
        route
        for item in cases_list
        for route in (item.get("result") or {}).get("routes") or []
    ]
    _check(
        checks,
        "all_routes_candidate_only_read_only_non_truth",
        all(
            route.get("candidate_only") is True
            and route.get("read_only") is True
            and route.get("truth_declared") is False
            and route.get("world_truth_declared") is False
            for route in all_routes
        ),
    )
    _check(
        checks,
        "all_routes_source_valid_demand",
        all(
            route.get("source_observation_demand_ref") in {
                demand.get("observation_demand_ref")
                for demand in (item.get("request") or {}).get("observation_demands") or []
                if isinstance(demand, dict)
            }
            for item in cases_list
            for route in (item.get("result") or {}).get("routes") or []
        ),
    )
    _check(
        checks,
        "all_routes_source_valid_resolution_candidate",
        all(
            route.get("source_capability_resolution_candidate_ref") in {
                candidate.get("capability_resolution_candidate_ref")
                for candidate in (((item.get("request") or {}).get("resolution_result") or {}).get("resolved_candidates") or [])
                if isinstance(candidate, dict)
            }
            for item in cases_list
            for route in (item.get("result") or {}).get("routes") or []
        ),
    )
    _check(
        checks,
        "all_routes_capability_class_coherent",
        all(
            route.get("capability_class_ref") == candidate.get("capability_class_ref")
            for item in cases_list
            for route in (item.get("result") or {}).get("routes") or []
            for candidate in (((item.get("request") or {}).get("resolution_result") or {}).get("resolved_candidates") or [])
            if candidate.get("capability_resolution_candidate_ref") == route.get("source_capability_resolution_candidate_ref")
        ),
    )
    _check(
        checks,
        "all_routes_lineage_preserved",
        all(
            route.get("source_observation_demand_ref") in (route.get("lineage_refs") or [])
            and route.get("source_capability_resolution_candidate_ref") in (route.get("lineage_refs") or [])
            and route.get("source_capability_requirement_ref") in (route.get("lineage_refs") or [])
            for route in all_routes
        ),
    )
    _check(
        checks,
        "upstream_snapshots_unchanged",
        all(
            item.get("observation_demand_snapshot_before") == item.get("observation_demand_snapshot_after")
            and item.get("capability_requirement_snapshot_before") == item.get("capability_requirement_snapshot_after")
            and item.get("resolution_candidate_snapshot_before") == item.get("resolution_candidate_snapshot_after")
            for item in cases_list
        ),
    )
    _check(
        checks,
        "input_resolution_refs_coherent",
        all(
            (item.get("result") or {}).get("input_resolution_candidate_refs")
            == (((item.get("request") or {}).get("resolution_result") or {}).get("resolved_candidate_refs") or [])
            for item in cases_list
            if (item.get("result") or {}).get("formation_status") != "INVALID_INPUT"
        ),
    )
    _check(
        checks,
        "deterministic_replay",
        all(
            (item.get("result") or {}).get("routing_candidate_refs")
            == item.get("deterministic_replay_route_refs")
            for item in cases_list
        ),
    )
    _check(
        checks,
        "malformed_input_fails_closed",
        (_case(cases, "MALFORMED_INPUT_SHAPE").get("result") or {}).get("formation_status") == "INVALID_INPUT"
        and not (_case(cases, "MALFORMED_INPUT_SHAPE").get("result") or {}).get("routes"),
    )

    failed = [item["check_id"] for item in checks if not item["passed"]]
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "checks": checks,
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify controlled Perception Routing Candidate formation."
    )
    parser.add_argument("--smoke-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = json.loads(
        (args.smoke_root / "runner_summary_v1.json").read_text(encoding="utf-8")
    )
    report = verify(summary)
    (args.smoke_root / "verifier_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["OUTPUT_DIR", "REQUIRED_CASES", "verify", "main"]
