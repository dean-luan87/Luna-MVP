"""Static/contract verifier for Provider Runtime Target Preparation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


OUTPUT_DIR = Path("_eval_out/perception_provider_runtime_target_preparation_v1")
REQUIRED_CASES = {
    "SINGLE_COMPATIBILITY_SINGLE_PROVIDER",
    "SINGLE_COMPATIBILITY_MULTIPLE_PROVIDERS",
    "MULTIPLE_COMPATIBILITY_CANDIDATES",
    "SAME_PROVIDER_CLASS_TWO_PROVIDER_CANDIDATES",
    "SAME_PROVIDER_MULTIPLE_DEMANDS",
    "SAME_CAPABILITY_MULTIPLE_PROVIDERS",
    "NO_COMPATIBILITY_CANDIDATE",
    "NO_PROVIDER_MAPPING",
    "NO_MATCHING_PROVIDER",
    "PROVIDER_UNAVAILABLE",
    "PROVIDER_NOT_ADMITTED",
    "INVALID_COMPATIBILITY_CANDIDATE",
    "LINEAGE_MISMATCH",
    "DUPLICATE_PROVIDER_CANDIDATE",
    "MODEL_REF_OPTIONAL",
    "NO_MODEL_INFERENCE",
    "NO_EXECUTION_INSTANCE_CREATION",
    "NO_PROVIDER_BINDING",
    "NO_GATEWAY_ADMISSION",
    "SCENARIO12_SIGNAGE",
    "SCENARIO12_HUMAN_FLOW",
    "SCENARIO12_BOTH",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
}


def _case(summary: Dict[str, Any], case_id: str) -> Dict[str, Any]:
    return next(case for case in summary.get("cases", []) if case.get("case_id") == case_id)


def _result(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("result") or {}


def _targets(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(_result(case).get("targets") or [])


def _run_checks(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    cases = {case.get("case_id"): case for case in summary.get("cases", [])}
    checks: List[Dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    check("required_cases_present", REQUIRED_CASES.issubset(cases), "all 24 controlled cases")
    check("controlled_marker", summary.get("source_mode") == "CONTROLLED_PROVIDER_RUNTIME_TARGET_PREPARATION")
    check("controlled_inventory_and_mapping", summary.get("provider_inventory_snapshot_controlled") is True and summary.get("provider_mapping_explicit_governed_input") is True and summary.get("provider_registry_runtime_read") is False)
    check("provider_owner_reused", summary.get("canonical_owner") == "Provider Governance" and summary.get("provider_runtime_governance_reused") is True)
    check("no_second_provider_owner", summary.get("second_provider_owner_created") is False)

    forbidden_true = (
        "provider_binding", "model_binding", "provider_selection", "provider_ranking", "provider_winner",
        "execution_instance_created", "provider_session_started", "runtime_admission_requested",
        "runtime_admission_executed", "gateway_submission", "capability_activation", "capability_reservation",
        "slot_reservation", "resource_scheduling", "provider_invocation", "model_invocation",
        "camera_execution", "ocr_execution", "slam_execution", "vlm_execution", "observation_execution",
        "evidence_ingress", "evidence_fusion", "attention_formed", "decision_formed", "task_formed",
        "action_formed", "current_world_mutation", "field_mutation", "memory_pcn_mutation",
    )
    check("no_execution_or_binding", all(summary.get(key) is False for key in forbidden_true))
    check("candidate_only", summary.get("candidate_only") is True and all(c.get("result", {}).get("candidate_only") is True for c in cases.values()))
    check("read_only", summary.get("read_only") is True and all(c.get("result", {}).get("read_only") is True for c in cases.values()))
    check("non_truth", summary.get("truth_declared") is False and summary.get("world_truth_declared") is False)

    for case_id, case in cases.items():
        result = _result(case)
        check(f"{case_id}:status", result.get("formation_status") == case.get("expected_status"))
        check(f"{case_id}:target_count", len(_targets(case)) == case.get("expected_target_count"))
        check(f"{case_id}:snapshot_unchanged", case.get("request_snapshot_before") == case.get("request_snapshot_after"))
        for target in _targets(case):
            check(f"{case_id}:target_candidate_only:{target.get('provider_target_candidate_ref')}", target.get("candidate_only") is True)
            check(f"{case_id}:target_read_only:{target.get('provider_target_candidate_ref')}", target.get("read_only") is True)
            check(f"{case_id}:target_non_truth:{target.get('provider_target_candidate_ref')}", target.get("truth_declared") is False and target.get("world_truth_declared") is False)
            check(f"{case_id}:target_no_runtime:{target.get('provider_target_candidate_ref')}", all(target.get(key) is False for key in forbidden_true if key in target))
            check(f"{case_id}:target_has_lineage:{target.get('provider_target_candidate_ref')}", all(target.get(key) for key in ("source_admission_compatibility_candidate_ref", "source_observation_demand_ref", "source_capability_resolution_candidate_ref", "provider_candidate_ref", "lineage_refs")))

    def exact(case_id: str, status: str, count: int, check_id: str) -> None:
        item = cases.get(case_id, {})
        check(check_id, _result(item).get("formation_status") == status and len(_targets(item)) == count)

    exact("SINGLE_COMPATIBILITY_SINGLE_PROVIDER", "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "single_provider_candidate")
    multiple = _targets(cases.get("SINGLE_COMPATIBILITY_MULTIPLE_PROVIDERS", {}))
    check("multiple_providers_all_retained", len(multiple) == 2 and len({x.get("provider_candidate_ref") for x in multiple}) == 2)
    check("same_provider_class_not_deduplicated", len(_targets(cases.get("SAME_PROVIDER_CLASS_TWO_PROVIDER_CANDIDATES", {}))) == 2 and len({x.get("provider_class_ref") for x in _targets(cases.get("SAME_PROVIDER_CLASS_TWO_PROVIDER_CANDIDATES", {}))}) == 1 and len({x.get("provider_candidate_ref") for x in _targets(cases.get("SAME_PROVIDER_CLASS_TWO_PROVIDER_CANDIDATES", {}))}) == 2)
    shared = _targets(cases.get("SAME_PROVIDER_MULTIPLE_DEMANDS", {}))
    check("same_provider_multiple_demands_not_merged", len(shared) == 2 and len({x.get("source_observation_demand_ref") for x in shared}) == 2 and len({x.get("provider_candidate_ref") for x in shared}) == 1)
    same_cap = _targets(cases.get("SAME_CAPABILITY_MULTIPLE_PROVIDERS", {}))
    check("same_capability_multiple_providers_retained", len(same_cap) == 2 and len({x.get("provider_candidate_ref") for x in same_cap}) == 2)
    check("zero_input_zero_candidate", _result(cases.get("NO_COMPATIBILITY_CANDIDATE", {})).get("formation_status") == "NO_PROVIDER_TARGET_CANDIDATE" and not _targets(cases.get("NO_COMPATIBILITY_CANDIDATE", {})))
    check("no_mapping_fails_closed", _result(cases.get("NO_PROVIDER_MAPPING", {})).get("formation_status") == "NO_PROVIDER_MAPPING" and not _targets(cases.get("NO_PROVIDER_MAPPING", {})))
    check("no_match_fails_closed", _result(cases.get("NO_MATCHING_PROVIDER", {})).get("formation_status") == "NO_MATCHING_PROVIDER" and not _targets(cases.get("NO_MATCHING_PROVIDER", {})))
    check("unavailable_fails_closed", _result(cases.get("PROVIDER_UNAVAILABLE", {})).get("formation_status") == "PROVIDER_UNAVAILABLE" and not _targets(cases.get("PROVIDER_UNAVAILABLE", {})))
    check("not_admitted_fails_closed", _result(cases.get("PROVIDER_NOT_ADMITTED", {})).get("formation_status") == "PROVIDER_NOT_ADMITTED" and not _targets(cases.get("PROVIDER_NOT_ADMITTED", {})))
    for case_id in ("INVALID_COMPATIBILITY_CANDIDATE", "LINEAGE_MISMATCH", "DUPLICATE_PROVIDER_CANDIDATE", "MALFORMED_INPUT_SHAPE"):
        exact(case_id, "INVALID_INPUT", 0, f"{case_id.lower()}:fail_closed")
    optional_target = _targets(cases.get("MODEL_REF_OPTIONAL", {}))
    no_model_target = _targets(cases.get("NO_MODEL_INFERENCE", {}))
    check("model_optional", len(optional_target) == 1 and optional_target[0].get("source_model_ref") == "model:controlled:opaque")
    check("no_model_inference", len(no_model_target) == 1 and no_model_target[0].get("source_model_ref") is None)
    check("no_execution_instance", all("execution_instance_ref" not in target for target in _targets(cases.get("NO_EXECUTION_INSTANCE_CREATION", {}))))
    check("no_provider_binding", all(target.get("provider_binding") is False for target in _targets(cases.get("NO_PROVIDER_BINDING", {}))))
    check("no_gateway_admission", all(target.get("runtime_admission_requested") is False and target.get("gateway_submission") is False for target in _targets(cases.get("NO_GATEWAY_ADMISSION", {}))))
    for case_id, forbidden in (("SCENARIO12_SIGNAGE", ("ocr", "camera")), ("SCENARIO12_HUMAN_FLOW", ("vlm", "detector", "slam"))):
        # Inspect formation data only.  The case marker may name the guard
        # being tested (for example ``no_ocr_inference``) and is not a
        # semantic routing/provider reference.
        scenario_case = cases.get(case_id, {})
        serialized = json.dumps(
            {
                "request": scenario_case.get("request"),
                "result": scenario_case.get("result"),
            },
            ensure_ascii=False,
        ).lower()
        check(f"{case_id.lower()}:no_semantic_inference", not any(token in serialized for token in forbidden))
    both = _targets(cases.get("SCENARIO12_BOTH", {}))
    check("scenario12_independent_targets", len(both) == 2 and len({x.get("source_observation_demand_ref") for x in both}) == 2)
    replay = cases.get("DETERMINISTIC_REPLAY", {})
    check("deterministic_replay", [x.get("provider_target_candidate_ref") for x in _targets(replay)] == replay.get("deterministic_replay", {}).get("provider_target_candidate_refs") and _result(replay).get("formation_status") == replay.get("deterministic_replay", {}).get("formation_status"))
    check("all_targets_source_valid_compatibility", all(target.get("source_admission_compatibility_candidate_ref") in (_result(case).get("input_compatibility_candidate_refs") or []) for case in cases.values() for target in _targets(case)))
    check("all_capability_refs_coherent", all(target.get("capability_class_ref") and target.get("capability_candidate_ref") for case in cases.values() for target in _targets(case)))
    check("no_provider_binding_field", all("selected_provider_ref" not in target and "bound_provider_ref" not in target and "winner_provider_ref" not in target for case in cases.values() for target in _targets(case)))
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Provider runtime target preparation.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary_path = args.output_root / "runner_summary_v1.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    checks = _run_checks(summary)
    failed = [item["check_id"] for item in checks if not item["passed"]]
    all_checks_passed = not failed
    cognitive_logic_result = "PASS" if all_checks_passed else "FAIL"
    operational_result = "PASS" if all_checks_passed else "FAIL"
    final_decision = (
        "GO"
        if (
            all_checks_passed
            and cognitive_logic_result == "PASS"
            and operational_result == "PASS"
            and not failed
        )
        else "NO_GO"
    )
    report = {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "passed_count": len(checks) - len(failed),
        "failed_checks": failed,
        "all_checks_passed": all_checks_passed,
        "cognitive_logic_result": cognitive_logic_result,
        "operational_result": operational_result,
        "final_decision": final_decision,
        "checks": checks,
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "verification_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
