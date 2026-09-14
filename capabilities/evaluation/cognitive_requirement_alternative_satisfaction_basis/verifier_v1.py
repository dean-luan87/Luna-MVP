"""Fail-closed verifier for controlled alternative satisfaction basis semantics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .fixtures_v1 import (
    BASIS_A,
    LEGACY_COVERAGE_REF,
    LEGACY_REQUIREMENT_REF,
    REQUIREMENT_REF,
    SOURCE_MODE,
)


PHASE = "Phase-Cognitive-Requirement-Alternative-Satisfaction-Basis-Controlled-Implementation-v1-001"


def _check(checks: dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    cases = {item.get("case_id"): item for item in summary.get("cases", ())}
    required_cases = {
        "LEGACY_EXACT_COVERAGE",
        "LEGACY_EXACT_COVERAGE_MISSING",
        "ALTERNATIVE_BASIS_A",
        "ALTERNATIVE_BASIS_B",
        "NO_ALTERNATIVE_BASIS_COVERED",
        "MULTIPLE_ALTERNATIVE_BASES_COVERED",
    }
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_marker", summary.get("source_mode") == SOURCE_MODE)
    _check(checks, "required_cases", set(cases) == required_cases)
    _check(
        checks,
        "need_core_subtraction_unchanged",
        summary.get("information_need_core_subtraction_changed") is False,
    )

    expected = {
        "LEGACY_EXACT_COVERAGE": ("SATISFIED", [LEGACY_COVERAGE_REF]),
        "LEGACY_EXACT_COVERAGE_MISSING": ("UNSATISFIED", []),
        "ALTERNATIVE_BASIS_A": ("SATISFIED", [BASIS_A]),
        "ALTERNATIVE_BASIS_B": ("SATISFIED", ["basis:controlled:exit-direction:b:v1"]),
        "NO_ALTERNATIVE_BASIS_COVERED": ("UNSATISFIED", []),
        "MULTIPLE_ALTERNATIVE_BASES_COVERED": ("SATISFIED", [BASIS_A]),
    }
    for case_id, item in cases.items():
        result = item.get("result") or {}
        candidates = result.get("candidates") or []
        expected_status, expected_coverage = expected.get(case_id, (None, None))
        _check(checks, f"{case_id}:status", result.get("status") == item.get("expected_status"))
        _check(checks, f"{case_id}:active_single_requirement", result.get("active_required_condition_refs") == [
            LEGACY_REQUIREMENT_REF if case_id.startswith("LEGACY") else REQUIREMENT_REF
        ])
        _check(
            checks,
            f"{case_id}:satisfaction_status",
            bool(candidates)
            and candidates[0].get("satisfaction_status") == expected_status,
        )
        _check(
            checks,
            f"{case_id}:actual_satisfaction_coverage",
            bool(candidates)
            and candidates[0].get("satisfaction_coverage_refs") == expected_coverage,
        )
        _check(checks, f"{case_id}:one_candidate", len(candidates) == 1)
        _check(
            checks,
            f"{case_id}:candidate_only_non_truth",
            result.get("candidate_only") is True
            and result.get("read_only") is True
            and result.get("truth_declared") is False
            and result.get("world_truth_declared") is False,
        )
        _check(
            checks,
            f"{case_id}:no_side_effects",
            not any(
                result.get(name)
                for name in (
                    "provider_invocation",
                    "model_invocation",
                    "observation_execution",
                    "observation_demand_formed",
                    "capability_selection_executed",
                    "decision_execution",
                    "task_execution",
                    "action_execution",
                    "field_mutation",
                    "current_world_mutation",
                    "memory_mutation",
                    "pcn_mutation",
                )
            ),
        )

    sandbox = summary.get("sandbox_regressions") or {}
    scenario_12 = sandbox.get("scenario_12") or {}
    round_zero = scenario_12.get("round_0") or {}
    round_one = scenario_12.get("round_1") or {}
    round_zero_candidates = round_zero.get("required_condition_candidates") or []
    round_one_candidates = round_one.get("required_condition_candidates") or []
    _check(checks, "scenario12:single_semantic_requirement", round_zero.get("required_condition_refs") == [
        "condition:sandbox:12:exit-direction-known"
    ])
    _check(checks, "scenario12:round0_need", len(round_zero.get("information_needs") or []) == 1)
    _check(checks, "scenario12:round0_multiple_strategies", len(round_zero.get("strategy_candidates") or []) == 2)
    _check(
        checks,
        "scenario12:round0_unsatisfied",
        len(round_zero_candidates) == 1
        and round_zero_candidates[0].get("satisfaction_status") == "UNSATISFIED",
    )
    _check(checks, "scenario12:round1_need_suppressed", len(round_one.get("information_needs") or []) == 0)
    _check(checks, "scenario12:round1_no_branch", len(round_one.get("branches") or []) == 0)
    _check(checks, "scenario12:round1_no_strategy", len(round_one.get("strategy_candidates") or []) == 0)
    _check(
        checks,
        "scenario12:round1_signage_basis_satisfies_requirement",
        len(round_one_candidates) == 1
        and round_one_candidates[0].get("satisfaction_status") == "SATISFIED"
        and round_one_candidates[0].get("satisfaction_coverage_refs") == [
            "basis:sandbox:12:signage"
        ],
    )

    scenario_10 = sandbox.get("scenario_10") or {}
    scenario_10_round = scenario_10.get("round_0") or {}
    _check(checks, "scenario10:need_without_strategy_preserved", len(scenario_10_round.get("information_needs") or []) == 1 and not (scenario_10_round.get("strategy_candidates") or []))
    scenario_11 = sandbox.get("scenario_11") or {}
    _check(
        checks,
        "scenario11:irrelevant_change_stable",
        (scenario_11.get("round_0") or {}).get("cognitive_economy")
        == (scenario_11.get("round_1") or {}).get("cognitive_economy"),
    )

    guards = summary.get("negative_guards") or {}
    _check(checks, "negative_guards", all(value is False for value in guards.values()))
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify alternative satisfaction basis semantics."
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path(
            "_eval_out/cognitive_requirement_alternative_satisfaction_basis_v1/runner_summary_v1.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "_eval_out/cognitive_requirement_alternative_satisfaction_basis_v1/verifier_result_v1.json"
        ),
    )
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["verify", "main"]
