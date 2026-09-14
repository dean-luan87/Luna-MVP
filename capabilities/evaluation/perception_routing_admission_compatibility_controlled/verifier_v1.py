"""Fail-closed verifier for the candidate-only FPO compatibility seam."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/perception_routing_admission_compatibility_v1")
REQUIRED_CASES = {
    "SINGLE_ROUTING_CANDIDATE_COMPATIBLE",
    "MULTIPLE_ROUTING_CANDIDATES",
    "SAME_CLASS_MULTIPLE_ROUTES",
    "SAME_CAPABILITY_MULTIPLE_DEMANDS",
    "NO_ROUTING_CANDIDATE",
    "INVALID_ROUTING_CANDIDATE",
    "LINEAGE_MISMATCH",
    "MISSING_REQUIRED_TARGET_FIELD",
    "HISTORICAL_REQUEST_REQUIRES_PROVIDER_FIELD",
    "HISTORICAL_REQUEST_REQUIRES_MODEL_FIELD",
    "CAPABILITY_ADMITTED_BUT_RUNTIME_NOT_AUTO_ADMITTED",
    "SCENARIO12_SIGNAGE",
    "SCENARIO12_HUMAN_FLOW",
    "SCENARIO12_BOTH",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
    "UNSUPPORTED_OBSERVATION_CLASS",
}


def _check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    detail: Any = None,
) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _case(cases: dict[str, dict[str, Any]], case_id: str) -> dict[str, Any]:
    return cases.get(case_id, {})


def _result(cases: dict[str, dict[str, Any]], case_id: str) -> dict[str, Any]:
    return _case(cases, case_id).get("result") or {}


def _request_route_refs(item: dict[str, Any]) -> set[str]:
    routes = (item.get("request") or {}).get("routing_candidates") or []
    if not isinstance(routes, list):
        return set()
    return {
        route.get("perception_routing_candidate_ref")
        for route in routes
        if isinstance(route, dict) and route.get("perception_routing_candidate_ref")
    }


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    cases_list = summary.get("cases") or []
    cases = {item.get("case_id"): item for item in cases_list}
    _check(checks, "required_cases_present", set(cases) == REQUIRED_CASES)
    _check(
        checks,
        "controlled_marker",
        summary.get("source_mode") == "CONTROLLED_PERCEPTION_ROUTING_ADMISSION_COMPATIBILITY",
    )
    _check(
        checks,
        "owner_reused_or_gap_explicit",
        summary.get("canonical_owner")
        == "Field Perception Orchestrator / Active Observation Control",
    )
    _check(checks, "no_second_admission_owner", summary.get("routing_admission_owner_created") is False)
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)
    _check(
        checks,
        "no_runtime_or_downstream_execution",
        all(
            summary.get(key) is False
            for key in (
                "gateway_runtime_called",
                "fpo_runtime_called",
                "runtime_admission_executed",
                "gateway_submission",
                "provider_binding",
                "provider_invocation",
                "model_binding",
                "model_invocation",
                "capability_activation",
                "slot_reservation",
                "resource_scheduling",
                "observation_execution",
                "attention_formed",
                "decision_formed",
                "task_formed",
                "action_formed",
            )
        ),
    )
    _check(
        checks,
        "no_mutation_or_truth",
        all(
            summary.get(key) is False
            for key in (
                "truth_declared",
                "world_truth_declared",
                "current_world_mutation",
                "field_mutation",
                "memory_pcn_mutation",
            )
        ),
    )

    expected = {
        "SINGLE_ROUTING_CANDIDATE_COMPATIBLE": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1),
        "MULTIPLE_ROUTING_CANDIDATES": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2),
        "SAME_CLASS_MULTIPLE_ROUTES": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2),
        "SAME_CAPABILITY_MULTIPLE_DEMANDS": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2),
        "NO_ROUTING_CANDIDATE": ("NO_ADMISSION_COMPATIBILITY_CANDIDATE", 0),
        "INVALID_ROUTING_CANDIDATE": ("INVALID_INPUT", 0),
        "LINEAGE_MISMATCH": ("INVALID_INPUT", 0),
        "MISSING_REQUIRED_TARGET_FIELD": ("ADMISSION_COMPATIBILITY_GAP", 0),
        "HISTORICAL_REQUEST_REQUIRES_PROVIDER_FIELD": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1),
        "HISTORICAL_REQUEST_REQUIRES_MODEL_FIELD": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1),
        "CAPABILITY_ADMITTED_BUT_RUNTIME_NOT_AUTO_ADMITTED": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1),
        "SCENARIO12_SIGNAGE": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1),
        "SCENARIO12_HUMAN_FLOW": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1),
        "SCENARIO12_BOTH": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2),
        "DETERMINISTIC_REPLAY": ("ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2),
        "MALFORMED_INPUT_SHAPE": ("INVALID_INPUT", 0),
        "UNSUPPORTED_OBSERVATION_CLASS": ("ADMISSION_COMPATIBILITY_GAP", 0),
    }
    for case_id, (status, count) in expected.items():
        item = _case(cases, case_id)
        result = item.get("result") or {}
        _check(checks, f"{case_id}:status", result.get("formation_status") == status)
        _check(checks, f"{case_id}:candidate_count", len(result.get("candidates") or []) == count)
        _check(checks, f"{case_id}:expected_count", item.get("expected_candidate_count") == count)

    multiple = _result(cases, "MULTIPLE_ROUTING_CANDIDATES")
    _check(
        checks,
        "multiple_routes_independent",
        len(multiple.get("candidates") or []) == 2
        and len({item.get("source_perception_routing_candidate_ref") for item in multiple.get("candidates")}) == 2,
    )
    _check(
        checks,
        "multiple_routes_no_winner",
        multiple.get("runtime_admission_executed") is False
        and multiple.get("admission_compatibility_candidate_refs")
        == [item.get("admission_compatibility_candidate_ref") for item in multiple.get("candidates")],
    )

    same_class = _result(cases, "SAME_CLASS_MULTIPLE_ROUTES")
    same_class_candidates = same_class.get("candidates") or []
    _check(
        checks,
        "same_class_not_deduplicated",
        len(same_class_candidates) == 2
        and len({item.get("capability_class_ref") for item in same_class_candidates}) == 1
        and len({item.get("capability_candidate_ref") for item in same_class_candidates}) == 2
        and len({item.get("source_perception_routing_candidate_ref") for item in same_class_candidates}) == 2,
    )

    shared = _result(cases, "SAME_CAPABILITY_MULTIPLE_DEMANDS")
    shared_candidates = shared.get("candidates") or []
    _check(
        checks,
        "same_capability_multiple_demands_not_merged",
        len(shared_candidates) == 2
        and len({item.get("capability_candidate_ref") for item in shared_candidates}) == 1
        and len({item.get("source_observation_demand_ref") for item in shared_candidates}) == 2,
    )

    _check(checks, "zero_route_zero_candidate", not _result(cases, "NO_ROUTING_CANDIDATE").get("candidates"))
    _check(checks, "invalid_route_fails_closed", not _result(cases, "INVALID_ROUTING_CANDIDATE").get("candidates"))
    _check(checks, "lineage_mismatch_fails_closed", not _result(cases, "LINEAGE_MISMATCH").get("candidates"))
    _check(checks, "missing_target_fails_closed", not _result(cases, "MISSING_REQUIRED_TARGET_FIELD").get("candidates"))

    for case_id in (
        "HISTORICAL_REQUEST_REQUIRES_PROVIDER_FIELD",
        "HISTORICAL_REQUEST_REQUIRES_MODEL_FIELD",
    ):
        candidates = _result(cases, case_id).get("candidates") or []
        _check(
            checks,
            f"{case_id}:no_provider_model_fabrication",
            all("provider_ref" not in item and "model_ref" not in item for item in candidates),
        )

    no_auto = _result(cases, "CAPABILITY_ADMITTED_BUT_RUNTIME_NOT_AUTO_ADMITTED")
    _check(
        checks,
        "capability_admission_does_not_imply_runtime_admission",
        no_auto.get("runtime_admission_requested") is False
        and no_auto.get("runtime_admission_executed") is False
        and all(item.get("runtime_admission_requested") is False for item in no_auto.get("candidates") or []),
    )

    signage = _result(cases, "SCENARIO12_SIGNAGE").get("candidates") or []
    flow = _result(cases, "SCENARIO12_HUMAN_FLOW").get("candidates") or []
    _check(
        checks,
        "scenario12_signage_no_ocr_inference",
        bool(signage)
        and all("provider_ref" not in item and "model_ref" not in item for item in signage),
    )
    _check(
        checks,
        "scenario12_flow_no_model_inference",
        bool(flow)
        and all("provider_ref" not in item and "model_ref" not in item for item in flow),
    )
    scenario12_both = _result(cases, "SCENARIO12_BOTH")
    _check(
        checks,
        "scenario12_two_candidates",
        len(scenario12_both.get("candidates") or []) == 2
        and len({item.get("source_observation_demand_ref") for item in scenario12_both.get("candidates")}) == 2,
    )

    all_candidates = [
        candidate
        for item in cases_list
        for candidate in (item.get("result") or {}).get("candidates") or []
    ]
    _check(
        checks,
        "all_candidates_candidate_only_read_only_non_truth",
        all(
            candidate.get("candidate_only") is True
            and candidate.get("read_only") is True
            and candidate.get("truth_declared") is False
            and candidate.get("world_truth_declared") is False
            for candidate in all_candidates
        ),
    )
    _check(
        checks,
        "all_candidates_source_valid_route",
        all(
            candidate.get("source_perception_routing_candidate_ref")
            in _request_route_refs(item)
            for item in cases_list
            for candidate in (item.get("result") or {}).get("candidates") or []
        ),
    )
    _check(
        checks,
        "all_lineage_preserved",
        all(
            candidate.get("source_observation_demand_ref") in (candidate.get("lineage_refs") or [])
            and candidate.get("source_capability_requirement_ref") in (candidate.get("lineage_refs") or [])
            and candidate.get("source_capability_resolution_candidate_ref") in (candidate.get("lineage_refs") or [])
            and candidate.get("source_perception_routing_candidate_ref") in (candidate.get("lineage_refs") or [])
            for candidate in all_candidates
        ),
    )
    _check(
        checks,
        "upstream_snapshots_unchanged",
        all(item.get("request_snapshot_before") == item.get("request_snapshot_after") for item in cases_list),
    )
    _check(
        checks,
        "deterministic_replay",
        all(
            (item.get("result") or {}).get("admission_compatibility_candidate_refs")
            == item.get("deterministic_replay_candidate_refs")
            for item in cases_list
        ),
    )
    _check(
        checks,
        "malformed_input_fails_closed",
        _result(cases, "MALFORMED_INPUT_SHAPE").get("formation_status") == "INVALID_INPUT"
        and not _result(cases, "MALFORMED_INPUT_SHAPE").get("candidates"),
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
        description="Verify candidate-only Perception Routing admission compatibility."
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
