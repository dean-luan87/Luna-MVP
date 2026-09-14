"""Independent semantic verifier for controlled capability resolution."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from capabilities.midplatform.model_manager.registries.universal_capability_slot.observation_demand_capability_resolution_v1 import (
    resolve_observation_demand_capabilities,
)

from .fixtures_v1 import build_observation_capability_resolution_cases_v1


OUTPUT_DIR = Path("_eval_out/observation_capability_resolution_v1")


def _check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: Any = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _case_list(summary: dict[str, Any]) -> list[dict[str, Any]]:
    value = summary.get("cases")
    return value if isinstance(value, list) else []


def _independent_result(case: Any) -> dict[str, Any]:
    """Recompute from the immutable fixture request, never from runner output."""
    return asdict(resolve_observation_demand_capabilities(case.request))


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    cases_list = _case_list(summary)
    observed_ids = [case.get("case_id") for case in cases_list if isinstance(case, dict)]
    observed_by_id = {
        case.get("case_id"): case
        for case in cases_list
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    }
    fixture_cases = tuple(build_observation_capability_resolution_cases_v1())
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
        _check(checks, f"{case_id}:expected_status_from_fixture", recomputed.get("resolution_status") == fixture_case.expected_status)
        _check(checks, f"{case_id}:expected_candidate_count_from_fixture", len(recomputed.get("resolved_candidates", [])) == fixture_case.expected_candidate_count)
        expected_demands = [asdict(item) for item in fixture_case.request.observation_demands]
        _check(
            checks,
            f"{case_id}:snapshot_is_canonical",
            isinstance(observed, dict)
            and _canonical(observed.get("observation_demand_snapshot_before")) == _canonical(expected_demands)
            and _canonical(observed.get("observation_demand_snapshot_after")) == _canonical(expected_demands),
        )
        _check(checks, f"{case_id}:independent_replay_matches", _canonical(recomputed) == _canonical(replay))
        _check(
            checks,
            f"{case_id}:runner_replay_ref_matches_recomputed",
            isinstance(observed, dict)
            and _canonical(observed.get("deterministic_replay_candidate_refs"))
            == _canonical(replay.get("resolved_candidate_refs")),
        )

    all_candidates = [
        candidate
        for result in recomputed_results.values()
        for candidate in result.get("resolved_candidates", [])
    ]
    _check(checks, "all_candidates_candidate_only", bool(recomputed_results) and all(candidate.get("candidate_only") is True for candidate in all_candidates))
    _check(checks, "all_candidates_read_only_non_truth", bool(recomputed_results) and all(candidate.get("read_only") is True and candidate.get("truth_declared") is False and candidate.get("world_truth_declared") is False for candidate in all_candidates))
    _check(
        checks,
        "all_candidates_source_valid_demand",
        bool(recomputed_results)
        and all(
            candidate.get("source_observation_demand_ref")
            in {item.observation_demand_ref for item in fixture_case.request.observation_demands}
            for fixture_case in fixture_cases
            for candidate in recomputed_results.get(fixture_case.case_id, {}).get("resolved_candidates", [])
        ),
    )
    _check(
        checks,
        "governance_and_availability_recomputed",
        bool(recomputed_results)
        and all(
            entry.availability_status == "AVAILABLE"
            and entry.admission_status == "ADMITTED"
            and entry.eligible is True
            for fixture_case in fixture_cases
            for entry in fixture_case.request.capability_inventory
            if any(
                candidate.get("capability_candidate_ref") == entry.capability_candidate_ref
                for candidate in recomputed_results.get(fixture_case.case_id, {}).get("resolved_candidates", [])
            )
        ),
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
            "expected_source": "observation_capability_resolution_controlled.fixtures_v1:build_observation_capability_resolution_cases_v1",
            "observed_source": "runner_summary_v1.json",
            "recomputed_source": "resolve_observation_demand_capabilities called independently twice per canonical fixture case",
        },
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
