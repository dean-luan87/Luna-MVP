"""Independent semantic verifier for controlled Observation Demand formation."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import form_observation_demands

from .fixtures_v1 import build_observation_demand_cases_v1


OUTPUT_DIR = Path("_eval_out/observation_demand_v1")


def _check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: Any = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _case_list(summary: dict[str, Any]) -> list[dict[str, Any]]:
    value = summary.get("cases")
    return value if isinstance(value, list) else []


def _independent_result(case: Any) -> dict[str, Any]:
    """Recompute from the immutable fixture request, never from runner output."""
    return asdict(form_observation_demands(case.request))


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    cases_list = _case_list(summary)
    observed_ids = [case.get("case_id") for case in cases_list if isinstance(case, dict)]
    observed_by_id = {
        case.get("case_id"): case
        for case in cases_list
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    }
    fixture_cases = tuple(build_observation_demand_cases_v1())
    fixture_by_id = {case.case_id: case for case in fixture_cases}
    fixture_ids = set(fixture_by_id)
    observed_id_set = set(observed_ids)

    _check(
        checks,
        "required_cases_present_and_exact",
        isinstance(summary.get("cases"), list)
        and len(cases_list) == len(fixture_cases)
        and len(observed_ids) == len(observed_id_set)
        and observed_id_set == fixture_ids,
        {"missing": sorted(fixture_ids - observed_id_set), "unexpected": sorted(observed_id_set - fixture_ids)},
    )
    _check(checks, "case_identity_unique", len(observed_ids) == len(observed_id_set))
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)
    _check(
        checks,
        "no_downstream_execution",
        all(summary.get(key) is False for key in (
            "capability_resolution_executed", "capability_execution", "provider_invocation",
            "model_invocation", "ocr_execution", "camera_execution", "slam_execution",
            "runtime_observation_executed", "resource_acquisition_executed", "resource_scheduling_executed",
            "decision_formed", "task_formed", "action_formed", "attention_formed",
        )),
    )
    _check(
        checks,
        "no_mutation_or_truth",
        all(summary.get(key) is False for key in (
            "current_world_mutation", "field_mutation", "memory_pcn_mutation",
            "truth_declared", "world_truth_declared",
        )),
    )

    recomputed_results: dict[str, dict[str, Any]] = {}
    independent_replays: dict[str, dict[str, Any]] = {}
    for fixture_case in fixture_cases:
        case_id = fixture_case.case_id
        observed = observed_by_id.get(case_id)
        try:
            recomputed = _independent_result(fixture_case)
            replay = _independent_result(fixture_case)
            recomputed_results[case_id] = recomputed
            independent_replays[case_id] = replay
        except Exception as exc:  # controlled verifier failure, without accepting malformed input
            recomputed_results[case_id] = {}
            independent_replays[case_id] = {}
            _check(checks, f"{case_id}:independent_recomputation", False, type(exc).__name__)
            continue

        observed_request = observed.get("request") if isinstance(observed, dict) else None
        observed_result = observed.get("result") if isinstance(observed, dict) else None
        expected_request = asdict(fixture_case.request)
        _check(checks, f"{case_id}:request_matches_canonical_fixture", _canonical(observed_request) == _canonical(expected_request))
        _check(checks, f"{case_id}:result_matches_independent_recomputation", _canonical(observed_result) == _canonical(recomputed))
        _check(checks, f"{case_id}:expected_status_from_fixture", recomputed.get("formation_status") == fixture_case.expected_status)
        _check(checks, f"{case_id}:expected_demand_count_from_fixture", len(recomputed.get("demands", [])) == fixture_case.expected_demand_count)
        expected_strategies = [asdict(item) for item in fixture_case.request.strategy_candidates]
        expected_coordination = asdict(fixture_case.request.coordination_result)
        _check(
            checks,
            f"{case_id}:snapshots_are_canonical",
            isinstance(observed, dict)
            and _canonical(observed.get("strategy_snapshot_before")) == _canonical(expected_strategies)
            and _canonical(observed.get("strategy_snapshot_after")) == _canonical(expected_strategies)
            and _canonical(observed.get("coordination_snapshot_before")) == _canonical(expected_coordination)
            and _canonical(observed.get("coordination_snapshot_after")) == _canonical(expected_coordination),
        )
        _check(checks, f"{case_id}:independent_replay_matches", _canonical(recomputed) == _canonical(replay))
        _check(
            checks,
            f"{case_id}:runner_replay_refs_match_recomputed",
            isinstance(observed, dict)
            and _canonical(observed.get("deterministic_replay_demand_refs"))
            == _canonical(replay.get("demand_refs")),
        )

    all_demands = [
        demand
        for result in recomputed_results.values()
        for demand in result.get("demands", [])
    ]
    _check(checks, "expected_demand_set_is_non_empty_where_required", bool(recomputed_results) and all(
        result.get("formation_status") != "OBSERVATION_DEMANDS_FORMED" or bool(result.get("demand_refs"))
        for result in recomputed_results.values()
    ))
    _check(checks, "all_demands_candidate_only", bool(recomputed_results) and all(d.get("candidate_only") is True for d in all_demands))
    _check(checks, "all_demands_read_only_non_truth", bool(recomputed_results) and all(d.get("read_only") is True and d.get("truth_declared") is False and d.get("world_truth_declared") is False for d in all_demands))
    _check(checks, "lineage_integrity", bool(recomputed_results) and all(d.get("source_strategy_ref") and d.get("source_branch_ref") and d.get("information_need_refs") and d.get("information_gap_refs") and d.get("acquisition_basis_refs") and d.get("lineage_refs") and d.get("provenance_refs") for d in all_demands))
    _check(checks, "no_capability_resolution", bool(recomputed_results) and all(d.get("capability_requirement_formed") is False and d.get("capability_resolution_executed") is False for d in all_demands))
    _check(
        checks,
        "no_attention_or_execution",
        bool(recomputed_results)
        and all(all(d.get(key) is False for key in (
            "attention_formed", "runtime_observation_executed", "capability_execution",
            "provider_invocation", "model_invocation", "ocr_execution", "camera_execution",
            "slam_execution", "resource_acquisition_executed", "decision_formed", "task_formed", "action_formed",
        )) for d in all_demands),
    )

    expected_demand_set: dict[str, set[str]] = {}
    observed_demand_set: dict[str, set[str]] = {}
    for fixture_case in fixture_cases:
        case_id = fixture_case.case_id
        expected_demand_set[case_id] = set(recomputed_results.get(case_id, {}).get("demand_refs", []))
        observed_case = observed_by_id.get(case_id, {})
        observed_demand_set[case_id] = set((observed_case.get("result") or {}).get("demand_refs", []))
    _check(
        checks,
        "demand_identity_uniqueness_and_coverage",
        all(
            len(expected_demand_set[case_id]) == len(recomputed_results.get(case_id, {}).get("demand_refs", []))
            and observed_demand_set[case_id] == expected_demand_set[case_id]
            for case_id in expected_demand_set
        ),
        {"expected": {key: sorted(value) for key, value in expected_demand_set.items()}},
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
        "proof_provenance": {
            "expected_source": "observation_demand_controlled.fixtures_v1:build_observation_demand_cases_v1",
            "observed_source": "runner_summary_v1.json",
            "recomputed_source": "form_observation_demands called independently twice per canonical fixture case",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Observation Demand formation.")
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
