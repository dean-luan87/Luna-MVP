"""Verifier for the synthetic candidate-only Cognitive Loop skeleton."""

from __future__ import annotations

import json
import sys
from pathlib import Path


VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_continuity_candidate_adapter_v1 import (  # noqa: E402
    PHASE,
    build_candidate_loop_run_v1,
)


REQUIRED_NEGATIVE_GUARDS = (
    "provider_invocation",
    "yolo",
    "camera",
    "ocr",
    "action_execution",
    "learning",
    "memory_mutation",
    "experience_mutation",
    "autonomous_scheduling",
    "autonomous_loop_spawning",
    "new_cognitive_owner",
    "loop_manager",
    "loop_planner",
    "world_truth_declaration",
    "brain_provider_selection",
    "stale_requirement_direct_invocation",
    "cross_loop_local_state_mutation",
    "emotion_learning",
    "semantic_compression",
)


def _check(check_id: str, actual: object, expected: object) -> dict[str, object]:
    return {
        "check_id": check_id,
        "actual": actual,
        "expected": expected,
        "passed": actual == expected,
    }


def build_verification_summary_v1() -> dict[str, object]:
    payload = build_candidate_loop_run_v1()
    summary = payload["summary"]
    cases = summary["cases"]
    checks = [
        _check("phase", summary["phase"], PHASE),
        _check("scenario_cases_ok", summary["all_cases_passed"], True),
        _check("negative_guards_ok", summary["negative_guards_ok"], True),
        _check("candidate_only", summary["candidate_only"], True),
        _check("synthetic_only", summary["synthetic_only"], True),
        _check("no_provider_invocation", summary["provider_invocation"], False),
        _check("no_scheduler", summary["autonomous_scheduling"], False),
        _check("no_autonomous_loop_spawn", summary["autonomous_loop_spawning"], False),
        _check("materialization_guard", summary["materialization_guard"], True),
        _check("multi_loop_isolation_guard", summary["multi_loop_isolation_guard"], True),
        _check("stale_requirement_forces_invocation", summary["stale_requirement_forces_invocation"], False),
        _check("outcome_world_truth", summary["outcome_world_truth"], False),
        _check("outcome_action_execution", summary["outcome_action_execution"], False),
        _check("outcome_memory_mutation", summary["outcome_memory_mutation"], False),
        _check("outcome_experience_mutation", summary["outcome_experience_mutation"], False),
        _check("documentation_set_ok", _documentation_set_ok(), True),
        _check("source_set_ok", bool(cases) and summary["canonical_owner"] == "Cognitive Flow Governance", True),
    ]
    for case in cases:
        case_guards = case["negative_guards"]
        for guard in REQUIRED_NEGATIVE_GUARDS:
            checks.append(_check(f"{case['scenario_id']}:{guard}", case_guards.get(guard), False))
        checks.append(_check(f"{case['scenario_id']}:passed", all(item["passed"] for item in case["checks"]), True))
    failed_checks = [item["check_id"] for item in checks if not item["passed"]]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed_checks,
        "failed_checks": failed_checks,
        "failed_case_ids": sorted({check.split(":", 1)[0] for check in failed_checks if ":" in check}),
        "scenario_cases_ok": all(item["passed"] for item in checks if item["check_id"].endswith(":passed")),
        "negative_guards_ok": not any(
            item["check_id"].split(":", 1)[-1] in REQUIRED_NEGATIVE_GUARDS and not item["passed"]
            for item in checks
        ),
        "source_set_ok": next(item["passed"] for item in checks if item["check_id"] == "source_set_ok"),
        "documentation_set_ok": next(item["passed"] for item in checks if item["check_id"] == "documentation_set_ok"),
        "scenario_count": summary["scenario_count"],
        "checks": checks,
    }


def _documentation_set_ok() -> bool:
    root = Path(__file__).resolve()
    for parent in root.parents:
        if (parent / "docs" / "architecture").is_dir():
            phase_dir = parent / "docs" / "architecture" / "phase_luna_dynamic_cognitive_flow_governed_multi_loop_observation_planning_v1"
            return all(
                (phase_dir / name).is_file()
                for name in (
                    "brain_loop_boundary_contract_v1.md",
                    "loop_continuity_contract_v1.md",
                    "loop_growth_boundary_v1.md",
                    "implementation_delta_inventory_v1.md",
                )
            )
    return False


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_verification_summary_v1", "main"]
