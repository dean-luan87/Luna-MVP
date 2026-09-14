"""Verifier for the Route-B architecture/order adjudication evaluation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/perception_routing_admission_order_adjudication_v1")
REQUIRED_CASES = {
    "ADMISSION_CONTRACT_REQUIRES_PROVIDER",
    "ADMISSION_CONTRACT_REQUIRES_RUNTIME_TARGET",
    "MODEL_METADATA_NOT_REQUIRED_BY_GATEWAY_PROOF",
    "COMPATIBILITY_CANDIDATE_LACKS_PROVIDER",
    "COMPATIBILITY_CANDIDATE_LACKS_MODEL",
    "NO_FABRICATION",
    "CURRENT_ORDER_BLOCKED",
    "NO_COMPATIBILITY_CANDIDATE",
    "INVALID_COMPATIBILITY_CANDIDATE",
    "SCENARIO12_SIGNAGE",
    "SCENARIO12_HUMAN_FLOW",
    "SCENARIO12_BOTH",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
}


def _check(name: str, passed: bool, detail: str = "") -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def _contains_key(value: Any, forbidden: set[str]) -> bool:
    if isinstance(value, dict):
        return any(key in forbidden or _contains_key(item, forbidden) for key, item in value.items())
    if isinstance(value, list):
        return any(_contains_key(item, forbidden) for item in value)
    return False


def _formed_input_is_candidate_only(item: dict[str, Any]) -> bool:
    if item.get("formation_status") != "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION":
        return True
    candidates = item.get("compatibility_candidates_snapshot_before") or []
    return all(
        isinstance(candidate, dict)
        and candidate.get("candidate_only") is True
        and candidate.get("read_only") is True
        and candidate.get("truth_declared") is False
        and candidate.get("world_truth_declared") is False
        for candidate in candidates
    )


def main() -> None:
    summary_path = OUTPUT_DIR / "runner_summary_v1.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    cases = {item["case_id"]: item for item in summary["cases"]}
    checks = []
    checks.append(_check("required_cases_present", REQUIRED_CASES.issubset(cases)))
    checks.append(_check("route_b_selected", summary.get("route") == "ROUTE_B_ARCHITECTURE_ORDER_ADJUDICATION"))
    checks.append(_check("controlled_markers", summary.get("synthetic_only") is True and summary.get("controlled_only") is True))
    checks.append(_check("no_standalone_runtime_admission_owner", summary.get("standalone_runtime_admission_owner_created") is False))
    checks.append(_check("provider_precedes_runtime_admission", summary.get("provider_binding_precedes_runtime_admission") is True))
    checks.append(_check("model_requirement_not_invented", summary.get("runtime_admission_requires_model") is False))
    checks.append(_check("no_runtime_execution", summary.get("runtime_admission_execution") is False and summary.get("gateway_submission") is False))
    checks.append(_check("no_provider_model_binding", summary.get("provider_binding") is False and summary.get("model_binding") is False))
    checks.append(_check("no_world_or_truth_mutation", summary.get("current_world_mutation") is False and summary.get("field_mutation") is False and summary.get("truth_declared") is False and summary.get("world_truth_declared") is False))

    for case_id, item in cases.items():
        expected_status = item["expected_status"]
        expected_count = item["expected_candidate_count"]
        checks.append(_check(f"{case_id}:status", item["formation_status"] == expected_status))
        checks.append(_check(f"{case_id}:candidate_count", len(item["decisions"]) == expected_count))
        checks.append(_check(f"{case_id}:snapshot_unchanged", item["compatibility_candidates_snapshot_before"] == item["compatibility_candidates_snapshot_after"]))
        checks.append(_check(f"{case_id}:upstream_candidate_only", _formed_input_is_candidate_only(item)))
        checks.append(_check(f"{case_id}:no_runtime_flags", all(not item.get(flag) for flag in ("runtime_admission_execution", "gateway_submission", "provider_binding", "model_binding", "provider_invocation", "model_invocation", "observation_execution", "capability_activation", "slot_reservation", "resource_scheduling"))))
        checks.append(_check(f"{case_id}:no_fabricated_provider_model", not _contains_key(item["decisions"], {"provider_ref", "model_ref", "provider_name", "model_name", "runtime_handle"})))

    valid = cases["ADMISSION_CONTRACT_REQUIRES_PROVIDER"]
    checks.append(_check("runtime_contract_requires_provider", valid["admission_contract_requires_provider"] is True))
    checks.append(_check("runtime_contract_requires_runtime_target", valid["admission_contract_requires_runtime_observation"] is True and valid["admission_contract_requires_execution_instance"] is True))
    checks.append(_check("no_runtime_admission_candidate_formed", all(item["runtime_admission_candidate_formed"] is False for case in cases.values() for item in case["decisions"])))
    checks.append(_check("scenario12_two_lineages", len(cases["SCENARIO12_BOTH"]["decisions"]) == 2 and len({item["source_observation_demand_ref"] for item in cases["SCENARIO12_BOTH"]["decisions"]}) == 2))
    replay = cases["DETERMINISTIC_REPLAY"]
    checks.append(_check("deterministic_replay", replay["formation_status"] == replay["replay_formation_status"] and replay["compatibility_candidate_refs"] == replay["replay_decision_refs"]))
    checks.append(_check("malformed_input_fails_closed", cases["MALFORMED_INPUT_SHAPE"]["formation_status"] == "INVALID_INPUT" and not cases["MALFORMED_INPUT_SHAPE"]["decisions"]))
    checks.append(_check("no_gateway_or_fpo_runtime", summary.get("gateway_submission") is False and summary.get("fpo_runtime_invocation") is False))

    failed = [item["name"] for item in checks if not item["passed"]]
    report = {
        "phase": summary["phase"],
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "failed_checks": failed,
        "contract_failures": failed,
        "cognitive_logic_observations": [],
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }
    (OUTPUT_DIR / "verifier_report_v1.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
