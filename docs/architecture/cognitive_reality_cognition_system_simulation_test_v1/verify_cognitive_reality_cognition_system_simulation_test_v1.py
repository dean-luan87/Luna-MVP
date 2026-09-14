#!/usr/bin/env python3
"""User-terminal V2 verifier for controlled Reality Cognition simulation v1."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCENARIOS = (
    "level1_gully_child",
    "level1_gully_cattle",
    "level1_low_resource_navigation",
    "level2_risk_route_choice",
    "level2_information_insufficient",
    "level3_prediction_error_environment_change",
    "level3_capability_constraint",
)
REQUIRED_TRACE_FIELDS = (
    "input", "self_state", "world_state", "situation_candidate", "decision_candidate",
    "expected_outcome", "simulated_outcome", "difference", "failure_classification",
    "experience_candidate", "metrics", "authority_check", "trace_signature",
)
FORBIDDEN_AUTHORITY = (
    "real_action_executed", "provider_called", "hardware_accessed", "runtime_started",
    "scheduler_started", "b_reflection_used", "automatic_learning", "self_model_modified",
    "state_mutation_requested",
)


def workspace_root() -> Path:
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / "cognitive/validation").is_dir():
            return candidate
    raise FileNotFoundError("workspace root with cognitive/validation was not found")


def invoke(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="/private/tmp/luna-reality-cognition-system-simulation-v1")
    args = parser.parse_args()
    root = workspace_root()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    runner = root / "cognitive/validation/run_reality_cognition_simulation_test_v1.py"
    component = root / "cognitive/validation/verify_reality_cognition_simulation_test_result_v1.py"
    schema = root / "cognitive/validation/reality_cognition_simulation_trace_schema_v1.json"
    failures: list[str] = []
    checks = 0
    for asset in (runner, component, schema):
        checks += 1
        if not asset.is_file():
            failures.append(f"missing required asset: {asset.relative_to(root)}")
    checks += 1
    try:
        json.loads(schema.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        failures.append(f"trace schema parse failure: {type(exc).__name__}")
    for scenario in SCENARIOS:
        first = output_dir / f"{scenario}.json"
        replay = output_dir / f"{scenario}.replay.json"
        for target in (first, replay):
            checks += 1
            result = invoke([sys.executable, str(runner), "--scenario", scenario, "--output", str(target)])
            if result.returncode != 0:
                failures.append(f"runner failed for {scenario}: {result.stderr.strip() or result.stdout.strip()}")
        checks += 1
        component_result = invoke([sys.executable, str(component), "--input", str(first), "--replay", str(replay)])
        if component_result.returncode != 0 or "FINAL_DECISION: COMPONENT_VALIDATION_PASSED" not in component_result.stdout:
            failures.append(f"component validation failed for {scenario}: {component_result.stderr.strip() or component_result.stdout.strip()}")
            continue
        checks += 1
        try:
            trace = json.loads(first.read_text(encoding="utf-8"))
            missing = [key for key in REQUIRED_TRACE_FIELDS if key not in trace]
            if missing:
                failures.append(f"trace missing fields for {scenario}: {missing}")
            authority = trace.get("authority_check", {})
            for key in FORBIDDEN_AUTHORITY:
                if authority.get(key) is not False:
                    failures.append(f"forbidden authority for {scenario}: {key}")
            if set(trace.get("metrics", {})) != {"self_awareness", "reality_grounding", "situation_quality", "decision_reasoning", "feedback_quality"}:
                failures.append(f"metric schema mismatch for {scenario}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"trace parse failure for {scenario}: {type(exc).__name__}")

    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
