"""Static/contract verifier for the responsibility and binding seam."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


OUTPUT_DIR = Path("_eval_out/provider_binding_runtime_preparation_responsibility_v1")
REQUIRED_CASES = {
    "COMPLETE_REQUIREMENT_REACHES_PROVIDER", "INCOMPLETE_REQUIREMENT_NOT_REPAIRED_DOWNSTREAM",
    "PROVIDER_DOES_NOT_REINTERPRET_DEMAND", "PROVIDER_DOES_NOT_CREATE_CAPABILITY_REQUIREMENT",
    "GATEWAY_DOES_NOT_SELECT_PROVIDER", "FPO_DOES_NOT_BIND_PROVIDER",
    "MODEL_MANAGER_DOES_NOT_CREATE_COGNITIVE_NEED", "REQUESTER_OWNS_MISSING_TARGET",
    "PROVIDER_OWNS_PROVIDER_UNAVAILABLE", "RESOURCE_FAILURE_NOT_RECAST_AS_COGNITIVE_FAILURE",
    "EXECUTION_FAILURE_NOT_RECAST_AS_DEMAND_MUTATION", "SINGLE_PROVIDER_TARGET",
    "MULTIPLE_PROVIDER_TARGETS", "SAME_PROVIDER_MULTI_DEMAND", "SAME_CLASS_DISTINCT_PROVIDERS",
    "NO_PROVIDER_TARGET", "INVALID_PROVIDER_TARGET", "LINEAGE_MISMATCH", "MODEL_OPTIONAL",
    "NO_MODEL_INFERENCE", "NO_EXECUTION_INSTANCE", "NO_RUNTIME_ALLOCATION", "NO_GATEWAY_SUBMISSION",
    "SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW", "SCENARIO12_BOTH", "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT",
}


def _result(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("result") or {}


def _candidates(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(_result(case).get("candidates") or [])


def _run_checks(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    cases = {item.get("case_id"): item for item in summary.get("cases", [])}
    checks: List[Dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    check("required_cases_present", REQUIRED_CASES.issubset(cases), "all 28 controlled cases")
    check("controlled_marker", summary.get("source_mode") == "CONTROLLED_PROVIDER_BINDING_RUNTIME_PREPARATION")
    check("provider_owner_reused", summary.get("canonical_owner") == "Provider Governance" and summary.get("provider_governance_reused") is True)
    check("requester_owns_requirement_complexity", summary.get("requester_owns_requirement_complexity") is True)
    check("executor_owns_execution_complexity", summary.get("executor_owns_execution_complexity") is True)
    check("no_new_owners", summary.get("new_cognitive_owner_created") is False and summary.get("second_provider_owner_created") is False)

    forbidden_true = (
        "provider_binding_formed", "runtime_allocation_formed", "execution_instance_created", "provider_session_started",
        "gateway_submission", "runtime_admission_executed", "provider_invocation", "model_invocation", "capability_activation",
        "slot_reservation", "resource_scheduling", "runtime_observation_created", "observation_execution", "attention_formed",
        "decision_formed", "task_formed", "action_formed", "current_world_mutation", "field_mutation", "memory_pcn_mutation",
    )
    check("no_operational_execution", all(summary.get(key) is False for key in forbidden_true))
    check("candidate_only", summary.get("candidate_only") is True and all(_result(case).get("candidate_only") is True for case in cases.values()))
    check("read_only", summary.get("read_only") is True and all(_result(case).get("read_only") is True for case in cases.values()))
    check("non_truth", summary.get("truth_declared") is False and summary.get("world_truth_declared") is False)
    check("responsibility_matrix_present", {item.get("module") for item in summary.get("responsibility_matrix", [])} >= {"Observation Demand", "Provider Target Preparation", "Provider Binding", "Runtime Allocation", "Execution Instance", "Observation Gateway Runtime Admission"})
    check("failure_ownership_matrix_present", len(summary.get("failure_ownership_matrix", [])) >= 8)

    for case_id, case in cases.items():
        result = _result(case)
        check(f"{case_id}:status", result.get("formation_status") == case.get("expected_status"))
        check(f"{case_id}:candidate_count", len(_candidates(case)) == case.get("expected_candidate_count"))
        check(f"{case_id}:snapshot_unchanged", case.get("request_snapshot_before") == case.get("request_snapshot_after"))
        for candidate in _candidates(case):
            check(f"{case_id}:candidate_only", candidate.get("candidate_only") is True)
            check(f"{case_id}:read_only", candidate.get("read_only") is True)
            check(f"{case_id}:non_truth", candidate.get("truth_declared") is False and candidate.get("world_truth_declared") is False)
            check(f"{case_id}:lineage", all(candidate.get(key) for key in ("source_provider_target_candidate_ref", "source_admission_compatibility_candidate_ref", "source_observation_demand_ref", "provider_candidate_ref", "lineage_refs")))
            check(f"{case_id}:no_runtime_flags", all(candidate.get(key) is False for key in forbidden_true if key in candidate))
            check(f"{case_id}:no_binding_identity", all(key not in candidate for key in ("selected_provider_ref", "bound_provider_ref", "winner_provider_ref", "execution_instance_ref")))

    def exact(case_id: str, status: str, count: int, check_id: str) -> None:
        case = cases.get(case_id, {})
        check(check_id, _result(case).get("formation_status") == status and len(_candidates(case)) == count)

    exact("SINGLE_PROVIDER_TARGET", "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "single_provider_target")
    multi = _candidates(cases.get("MULTIPLE_PROVIDER_TARGETS", {}))
    check("multiple_provider_targets", len(multi) == 2 and len({x.get("provider_candidate_ref") for x in multi}) == 2)
    shared = _candidates(cases.get("SAME_PROVIDER_MULTI_DEMAND", {}))
    check("same_provider_multi_demand_not_merged", len(shared) == 2 and len({x.get("provider_candidate_ref") for x in shared}) == 1 and len({x.get("source_observation_demand_ref") for x in shared}) == 2)
    same_class = _candidates(cases.get("SAME_CLASS_DISTINCT_PROVIDERS", {}))
    check("same_class_distinct_providers", len(same_class) == 2 and len({x.get("provider_class_ref") for x in same_class}) == 1 and len({x.get("provider_candidate_ref") for x in same_class}) == 2)
    exact("NO_PROVIDER_TARGET", "NO_PROVIDER_BINDING_PREPARATION_CANDIDATE", 0, "zero_target")
    for case_id in ("INCOMPLETE_REQUIREMENT_NOT_REPAIRED_DOWNSTREAM", "REQUESTER_OWNS_MISSING_TARGET", "INVALID_PROVIDER_TARGET", "LINEAGE_MISMATCH", "MALFORMED_INPUT"):
        exact(case_id, "INVALID_INPUT", 0, f"{case_id.lower()}:fail_closed")
    check("model_optional", len(_candidates(cases.get("MODEL_OPTIONAL", {}))) == 1 and _candidates(cases.get("MODEL_OPTIONAL", {}))[0].get("source_model_ref") is None)
    check("no_model_inference", len(_candidates(cases.get("NO_MODEL_INFERENCE", {}))) == 1 and _candidates(cases.get("NO_MODEL_INFERENCE", {}))[0].get("source_model_ref") is None)
    for case_id in ("NO_EXECUTION_INSTANCE", "NO_RUNTIME_ALLOCATION", "NO_GATEWAY_SUBMISSION"):
        exact(case_id, "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, f"{case_id.lower()}:no_downstream_operation")
    for case_id, forbidden in (("SCENARIO12_SIGNAGE", ("ocr", "camera")), ("SCENARIO12_HUMAN_FLOW", ("vlm", "detector", "slam"))):
        case = cases.get(case_id, {})
        payload = json.dumps({"request": case.get("request"), "result": case.get("result")}, ensure_ascii=False).lower()
        check(f"{case_id.lower()}:no_semantic_inference", not any(item in payload for item in forbidden))
    both = _candidates(cases.get("SCENARIO12_BOTH", {}))
    check("scenario12_independent_targets", len(both) == 2 and len({x.get("source_observation_demand_ref") for x in both}) == 2)
    replay = cases.get("DETERMINISTIC_REPLAY", {})
    check("deterministic_replay", [x.get("provider_binding_preparation_candidate_ref") for x in _candidates(replay)] == replay.get("deterministic_replay", {}).get("candidate_refs"))
    check("all_candidates_source_valid_target", all(candidate.get("source_provider_target_candidate_ref") in (_result(case).get("input_provider_target_candidate_refs") or []) for case in cases.values() for candidate in _candidates(case)))
    check("all_provider_refs_preserved", all(candidate.get("provider_candidate_ref") and candidate.get("provider_class_ref") for case in cases.values() for candidate in _candidates(case)))
    check("no_upstream_semantic_invention", all(candidate.get("source_observation_demand_ref") in candidate.get("lineage_refs", []) and candidate.get("source_capability_requirement_ref") in candidate.get("lineage_refs", []) for case in cases.values() for candidate in _candidates(case)))
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Provider Binding preparation responsibility.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = json.loads((args.output_root / "runner_summary_v1.json").read_text(encoding="utf-8"))
    checks = _run_checks(summary)
    failed = [item["check_id"] for item in checks if not item["passed"]]
    all_checks_passed = not failed
    contract_failures = failed
    cognitive_logic_result = "PASS" if not failed else "FAIL"
    operational_result = "PASS" if not failed else "FAIL"
    final_decision = (
        "GO"
        if all_checks_passed
        and not contract_failures
        and cognitive_logic_result == "PASS"
        and operational_result == "PASS"
        else "NO_GO"
    )
    report = {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "passed_count": len(checks) - len(failed),
        "failed_checks": failed,
        "contract_failures": contract_failures,
        "all_checks_passed": all_checks_passed,
        "cognitive_logic_result": cognitive_logic_result,
        "operational_result": operational_result,
        "final_decision": final_decision,
        "cognitive_logic_observations": [],
        "checks": checks,
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "verification_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
