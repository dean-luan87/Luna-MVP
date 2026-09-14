"""Static/contract verifier for controlled capability resolution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/observation_capability_resolution_v1")
REQUIRED_CASES = {
    "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH",
    "SINGLE_DEMAND_MULTIPLE_CAPABILITY_MATCHES",
    "TWO_INDEPENDENT_DEMANDS",
    "NO_OBSERVATION_DEMAND",
    "MISSING_GOVERNED_CAPABILITY_MAPPING",
    "NO_MATCHING_CAPABILITY",
    "MATCHING_CAPABILITY_UNAVAILABLE",
    "NOT_ADMITTED_CAPABILITY",
    "SCENARIO_12_SIGNAGE_DEMAND",
    "SCENARIO_12_HUMAN_FLOW_DEMAND",
    "SAME_CLASS_MULTIPLE_DEMANDS",
    "INVALID_DEMAND_INPUT",
    "UNSUPPORTED_MULTI_CLASS_REQUIREMENT",
    "DETERMINISTIC_REPLAY",
}


def _check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    cases_list = summary.get("cases", [])
    cases = {case.get("case_id"): case for case in cases_list}
    _check(checks, "required_cases_present", REQUIRED_CASES.issubset(cases))
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)
    _check(
        checks,
        "no_provider_model_runtime",
        all(summary.get(key) is False for key in (
            "provider_binding", "model_binding", "capability_activation",
            "capability_reservation", "capability_scheduling", "capability_execution",
            "provider_invocation", "model_invocation", "perception_routing",
            "observation_gateway_request", "fpo_runtime_request", "resource_acquisition",
        )),
    )
    _check(
        checks,
        "no_ranking_winner_or_mutation",
        all(summary.get(key) is False for key in (
            "ranking_executed", "winner_selected", "current_world_mutation",
            "field_mutation", "memory_pcn_mutation", "truth_declared", "world_truth_declared",
        )),
    )

    expected = {
        "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH": ("CAPABILITY_CANDIDATES_RESOLVED", 1),
        "SINGLE_DEMAND_MULTIPLE_CAPABILITY_MATCHES": ("CAPABILITY_CANDIDATES_RESOLVED", 2),
        "TWO_INDEPENDENT_DEMANDS": ("CAPABILITY_CANDIDATES_RESOLVED", 2),
        "NO_OBSERVATION_DEMAND": ("NO_CAPABILITY_REQUIREMENT", 0),
        "MISSING_GOVERNED_CAPABILITY_MAPPING": ("NO_CAPABILITY_REQUIREMENT", 0),
        "NO_MATCHING_CAPABILITY": ("NO_MATCHING_CAPABILITY", 0),
        "MATCHING_CAPABILITY_UNAVAILABLE": ("CAPABILITY_UNAVAILABLE", 0),
        "NOT_ADMITTED_CAPABILITY": ("CAPABILITY_UNAVAILABLE", 0),
        "SCENARIO_12_SIGNAGE_DEMAND": ("CAPABILITY_CANDIDATES_RESOLVED", 1),
        "SCENARIO_12_HUMAN_FLOW_DEMAND": ("CAPABILITY_CANDIDATES_RESOLVED", 1),
        "SAME_CLASS_MULTIPLE_DEMANDS": ("CAPABILITY_CANDIDATES_RESOLVED", 2),
        "INVALID_DEMAND_INPUT": ("INVALID_INPUT", 0),
        "UNSUPPORTED_MULTI_CLASS_REQUIREMENT": ("UNSUPPORTED_REQUIREMENT_SHAPE", 0),
        "DETERMINISTIC_REPLAY": ("CAPABILITY_CANDIDATES_RESOLVED", 1),
    }
    for case_id, (status, count) in expected.items():
        result = cases.get(case_id, {}).get("result", {})
        _check(checks, f"{case_id}:status", result.get("resolution_status") == status)
        _check(checks, f"{case_id}:candidate_count", len(result.get("resolved_candidates", [])) == count)

    multiple = cases.get("SINGLE_DEMAND_MULTIPLE_CAPABILITY_MATCHES", {}).get("result", {})
    _check(checks, "multiple_matches_no_winner", len(multiple.get("resolved_candidate_refs", [])) == 2 and multiple.get("winner_selected") is False)
    two = cases.get("TWO_INDEPENDENT_DEMANDS", {}).get("result", {}).get("resolved_candidates", [])
    _check(checks, "two_demands_lineage_independent", len(two) == 2 and len({item.get("source_observation_demand_ref") for item in two}) == 2 and len({item.get("source_requirement_ref") for item in two}) == 2)
    _check(checks, "zero_demand_no_requirement", not cases.get("NO_OBSERVATION_DEMAND", {}).get("result", {}).get("requirements"))
    _check(checks, "missing_mapping_no_requirement", not cases.get("MISSING_GOVERNED_CAPABILITY_MAPPING", {}).get("result", {}).get("resolved_candidates"))
    _check(checks, "no_matching_fails_closed", not cases.get("NO_MATCHING_CAPABILITY", {}).get("result", {}).get("resolved_candidates"))
    _check(checks, "unavailable_not_active", not cases.get("MATCHING_CAPABILITY_UNAVAILABLE", {}).get("result", {}).get("resolved_candidates"))
    _check(checks, "not_admitted_not_active", not cases.get("NOT_ADMITTED_CAPABILITY", {}).get("result", {}).get("resolved_candidates"))
    _check(checks, "scenario12_signage_no_ocr_inference", bool(cases.get("SCENARIO_12_SIGNAGE_DEMAND", {}).get("result", {}).get("resolved_candidates")) and all(item.get("capability_class_ref") != "OCR" for item in cases.get("SCENARIO_12_SIGNAGE_DEMAND", {}).get("result", {}).get("resolved_candidates", [])))
    _check(checks, "scenario12_flow_no_model_inference", bool(cases.get("SCENARIO_12_HUMAN_FLOW_DEMAND", {}).get("result", {}).get("resolved_candidates")) and all(item.get("model_binding") is False for item in cases.get("SCENARIO_12_HUMAN_FLOW_DEMAND", {}).get("result", {}).get("resolved_candidates", [])))
    same_class = cases.get("SAME_CLASS_MULTIPLE_DEMANDS", {}).get("result", {}).get("resolved_candidates", [])
    _check(checks, "same_class_demands_not_merged", len(same_class) == 2 and len({item.get("source_observation_demand_ref") for item in same_class}) == 2)
    _check(checks, "invalid_input_fails_closed", not cases.get("INVALID_DEMAND_INPUT", {}).get("result", {}).get("resolved_candidates"))
    _check(checks, "unsupported_multi_class_fails_closed", not cases.get("UNSUPPORTED_MULTI_CLASS_REQUIREMENT", {}).get("result", {}).get("resolved_candidates"))

    immutable = all(
        case.get("observation_demand_snapshot_before") == case.get("observation_demand_snapshot_after")
        for case in cases_list
    )
    _check(checks, "demand_snapshot_unchanged", immutable)
    deterministic = all(
        case.get("result", {}).get("resolved_candidate_refs", []) == case.get("deterministic_replay_candidate_refs", [])
        for case in cases_list
    )
    _check(checks, "deterministic_replay", deterministic)

    all_candidates = [candidate for case in cases_list for candidate in case.get("result", {}).get("resolved_candidates", [])]
    _check(checks, "all_candidates_candidate_only", all(candidate.get("candidate_only") is True for candidate in all_candidates))
    _check(checks, "all_candidates_read_only_non_truth", all(candidate.get("read_only") is True and candidate.get("truth_declared") is False and candidate.get("world_truth_declared") is False for candidate in all_candidates))
    _check(
        checks,
        "all_candidates_source_valid_demand",
        all(
            candidate.get("source_observation_demand_ref")
            in {item.get("observation_demand_ref") for item in case.get("request", {}).get("observation_demands", [])}
            for case in cases_list
            for candidate in case.get("result", {}).get("resolved_candidates", [])
        ),
    )

    all_class_matches = True
    all_available = True
    all_governance_valid = True
    for case in cases_list:
        request = case.get("request", {})
        demands = {item.get("observation_demand_ref"): item for item in request.get("observation_demands", [])}
        mappings = {item.get("observation_demand_ref"): item for item in request.get("governed_requirement_mappings", [])}
        inventory = {item.get("capability_candidate_ref"): item for item in request.get("capability_inventory", [])}
        requirements = {item.get("requirement_ref"): item for item in case.get("result", {}).get("requirements", [])}
        for candidate in case.get("result", {}).get("resolved_candidates", []):
            requirement = requirements.get(candidate.get("source_requirement_ref"), {})
            mapping = mappings.get(candidate.get("source_observation_demand_ref"), {})
            entry = inventory.get(candidate.get("capability_candidate_ref"), {})
            required_class = requirement.get("required_capability_class_ref") or (mapping.get("required_capability_class_refs") or [None])[0]
            all_class_matches = all_class_matches and candidate.get("capability_class_ref") == required_class
            all_available = all_available and entry.get("availability_status") == "AVAILABLE"
            all_governance_valid = all_governance_valid and entry.get("admission_status") == "ADMITTED" and entry.get("eligible") is True
    _check(checks, "all_candidates_match_required_class", all_class_matches)
    _check(checks, "all_active_candidates_available", all_available)
    _check(checks, "all_active_candidates_governance_valid", all_governance_valid)

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
    parser = argparse.ArgumentParser(description="Verify controlled Observation Demand capability resolution.")
    parser.add_argument("--smoke-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary_path = args.smoke_root / "runner_summary_v1.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    report = verify(summary)
    (args.smoke_root / "verifier_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["main", "verify"]
