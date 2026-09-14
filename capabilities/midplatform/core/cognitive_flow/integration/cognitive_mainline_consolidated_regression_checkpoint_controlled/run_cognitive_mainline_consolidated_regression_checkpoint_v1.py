"""Orchestrate existing phase Runner/Verifier entrypoints without reimplementing them."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir() and (_candidate / "README.md").is_file():
        REPO_ROOT = _candidate
        break
else:  # pragma: no cover
    REPO_ROOT = RUNNER_PATH.parents[7]

MANIFEST_PATH = REPO_ROOT / "docs/architecture/phase_luna_cognitive_mainline_consolidated_regression_checkpoint_v1/cognitive_mainline_regression_manifest_v1.json"
REPORT_DIR = REPO_ROOT / "_eval_out/cognitive_mainline_consolidated_regression_checkpoint_v1"
REPORT_PATH = REPORT_DIR / "regression_summary_v1.json"
PHASE = "Phase-Luna-Cognitive-Mainline-Consolidated-Regression-Checkpoint-v1-001"
REAL_CAPABILITY_REGRESSION_ID = "REAL-CAPABILITY"
REAL_CAPABILITY_FORWARDING_ARGS = {
    "source": "--source",
    "model_path": "--model-path",
    "dependency_status": "--dependency-status",
    "declared_checksum": "--declared-checksum",
    "observed_checksum": "--observed-checksum",
}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _read_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _parse_json_stdout(stdout: str) -> dict[str, Any] | None:
    for line in reversed([item.strip() for item in stdout.splitlines() if item.strip()]):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def _failure_class(check_name: str, *, real: bool = False) -> str:
    lowered = check_name.lower()
    if "readiness" in lowered or "argument" in lowered:
        return "ADMISSION_READINESS"
    if "source" in lowered:
        return "SOURCE_MANIFEST"
    if "documentation" in lowered:
        return "DOCUMENTATION"
    if "authority" in lowered or "grant" in lowered:
        return "AUTHORITY" if "grant" not in lowered else "GRANT"
    if "semantic" in lowered or lowered.startswith("a_"):
        return "A_SEMANTIC"
    if "b_" in lowered or "contingency" in lowered:
        return "B_CR"
    if "loop" in lowered or "mechanical" in lowered or "resume" in lowered or "closure" in lowered:
        return "LOOP_MECHANICAL"
    if "dynamic" in lowered or "compatibility" in lowered:
        return "DYNAMIC_COMPATIBILITY"
    if "envelope" in lowered or "requirement" in lowered:
        return "WORKING_ENVELOPE"
    if "observation" in lowered or "capability" in lowered:
        return "OBSERVATION" if "observation" in lowered else "CAPABILITY"
    if "provider" in lowered or "invocation" in lowered:
        return "REAL_PROVIDER_SINGLE_INVOCATION" if real else "CAPABILITY"
    if "input" in lowered or "world" in lowered:
        return "REAL_INPUT"
    if "trace" in lowered or "provenance" in lowered:
        return "TRACE_PROVENANCE"
    return "SCENARIO"


def _invoke(entry: dict[str, Any], key: str, extra_args: tuple[str, ...] = ()) -> tuple[int, dict[str, Any] | None, str, str]:
    relative_path = entry[key]
    path = REPO_ROOT / relative_path
    if not path.is_file():
        return 127, None, "", f"missing entrypoint: {relative_path}"
    completed = subprocess.run(
        [sys.executable, str(path), *extra_args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, _parse_json_stdout(completed.stdout), completed.stdout, completed.stderr.strip()


def _real_capability_forwarding(entry: dict[str, Any], values: dict[str, str | None]) -> tuple[tuple[str, ...], list[str]]:
    if entry.get("regression_id") != REAL_CAPABILITY_REGRESSION_ID:
        return (), []
    missing = [REAL_CAPABILITY_FORWARDING_ARGS[name] for name, value in values.items() if not value]
    if missing:
        return (), missing
    forwarded: list[str] = []
    for name, option in REAL_CAPABILITY_FORWARDING_ARGS.items():
        forwarded.extend((option, str(values[name])))
    return tuple(forwarded), []


def _phase_result(entry: dict[str, Any], real_capability_values: dict[str, str | None]) -> dict[str, Any]:
    real = entry["regression_group"] == "real-approved"
    child_args, missing_readiness = _real_capability_forwarding(entry, real_capability_values)
    if missing_readiness:
        return {
            "regression_id": entry["regression_id"],
            "phase_name": entry["phase_name"],
            "regression_group": entry["regression_group"],
            "status": "READINESS_ARGUMENTS_REQUIRED",
            "executed": False,
            "passed": False,
            "failed_case_ids": [],
            "failures": [{"class": "ADMISSION_READINESS", "reason": "READINESS_ARGUMENTS_REQUIRED"}],
            "missing_argument_names": missing_readiness,
            "provider_invocation_attempted": False,
            "runner_exit_code": None,
            "verifier_exit_code": None,
            "runner_stdout": "",
            "runner_stderr": "",
            "runner_summary": None,
            "verifier_stdout": "",
            "verifier_stderr": "",
            "verifier_summary": None,
            "runner_stderr_present": False,
            "verifier_stderr_present": False,
        }
    runner_rc, runner_payload, runner_stdout, runner_stderr = _invoke(entry, "runner_path", child_args)
    verifier_executed = runner_rc == 0 and runner_payload is not None
    if verifier_executed:
        verifier_rc, verifier_payload, verifier_stdout, verifier_stderr = _invoke(entry, "verifier_path")
    else:
        verifier_rc, verifier_payload, verifier_stdout, verifier_stderr = None, None, "", ""
    failures: list[dict[str, str]] = []
    expected_count = entry.get("expected_scenario_count")
    if runner_payload is None:
        failures.append({"class": "ENTRYPOINT", "reason": "runner_json_missing"})
    elif expected_count is not None and runner_payload.get("scenario_count") != expected_count:
        failures.append({"class": "SCENARIO", "reason": "runner_scenario_count"})
    if runner_rc != 0:
        failures.append({
            "class": "SCENARIO" if runner_payload is not None and runner_payload.get("all_cases_passed") is not True else "ENTRYPOINT",
            "reason": "runner_exit_code",
        })
    if runner_payload and runner_payload.get("all_cases_passed") is not True:
        failures.append({"class": "SCENARIO", "reason": "runner_cases_failed"})
    if verifier_executed:
        if verifier_payload is None:
            failures.append({"class": "ENTRYPOINT", "reason": "verifier_json_missing"})
        if verifier_rc != 0:
            failures.append({"class": "UNKNOWN", "reason": "verifier_exit_code"})
        if verifier_payload and verifier_payload.get("all_checks_passed") is not True:
            failed_checks = verifier_payload.get("failed_checks") or ["verifier_checks_failed"]
            failures.extend({"class": _failure_class(str(item), real=real), "reason": str(item)} for item in failed_checks)
    if runner_payload:
        for key in entry.get("expected_runner_fields", ()): 
            if key not in runner_payload:
                failures.append({"class": "UNKNOWN", "reason": f"missing_runner_field:{key}"})
    if verifier_payload:
        for key in entry.get("expected_verifier_fields", ()):
            if key not in verifier_payload:
                failures.append({"class": "UNKNOWN", "reason": f"missing_verifier_field:{key}"})
    runner_failed_ids = list((runner_payload or {}).get("failed_case_ids", ()))
    verifier_failed_ids = list((verifier_payload or {}).get("failed_case_ids", ()))
    passed = not failures
    result = {
        "regression_id": entry["regression_id"],
        "phase_name": entry["phase_name"],
        "regression_group": entry["regression_group"],
        "status": "PASS" if passed else "FAIL",
        "executed": True,
        "passed": passed,
        "failed_case_ids": sorted(set(runner_failed_ids + verifier_failed_ids)),
        "failures": failures,
        "missing_argument_names": [],
        "provider_invocation_attempted": bool(
            entry.get("regression_id") == REAL_CAPABILITY_REGRESSION_ID and runner_payload is not None
        ),
        "runner_exit_code": runner_rc,
        "verifier_exit_code": verifier_rc,
        "runner_summary": runner_payload,
        "verifier_summary": verifier_payload,
        "runner_stderr_present": bool(runner_stderr),
        "verifier_stderr_present": bool(verifier_stderr),
    }
    if real and not passed:
        result.update(
            {
                "runner_stdout": runner_stdout,
                "runner_stderr": runner_stderr,
                "verifier_stdout": verifier_stdout,
                "verifier_stderr": verifier_stderr,
            }
        )
    return result


def build_regression_summary_v1(group: str = "synthetic", real_capability_values: dict[str, str | None] | None = None) -> dict[str, Any]:
    manifest = _read_manifest()
    entries = [item for item in manifest["phases"] if group == "all" or item["regression_group"] == group]
    values = real_capability_values or {}
    results = [_phase_result(item, values) for item in entries]
    synthetic_results = [item for item in results if item["regression_group"] == "synthetic"]
    real_results = [item for item in results if item["regression_group"] == "real-approved"]
    failed = [item["regression_id"] for item in results if not item["passed"]]
    provider_counts = [
        int((item.get("runner_summary") or {}).get("real_provider_invocation_count", 0))
        for item in real_results
    ]
    second_invocation = any(
        bool((item.get("runner_summary") or {}).get("second_real_invocation_allowed", False))
        for item in real_results
    )
    by_id = {item["regression_id"]: item["passed"] for item in results}
    return {
        "phase": PHASE,
        "group": group,
        "regression_case_count": len(results),
        "passed_regression_count": sum(item["passed"] for item in results),
        "failed_regression_count": len(failed),
        "failed_regression_ids": failed,
        "synthetic_regression_executed": bool(synthetic_results),
        "synthetic_regression_ok": all(item["passed"] for item in synthetic_results) if synthetic_results else True,
        "real_boundary_regression_executed": bool(real_results) and all(item["executed"] for item in real_results),
        "real_boundary_regression_ok": all(item["passed"] for item in real_results) if real_results else True,
        "shared_registry_regression_ok": by_id.get("AG-MECHANICAL", False) if "AG-MECHANICAL" in by_id else True,
        "a_semantic_regression_ok": by_id.get("A-SEMANTIC", False) if "A-SEMANTIC" in by_id else True,
        "ab_cr_regression_ok": by_id.get("AB-CR", False) if "AB-CR" in by_id else True,
        "working_envelope_regression_ok": by_id.get("A-WORKING-ENVELOPE", False) if "A-WORKING-ENVELOPE" in by_id else True,
        "loop_cutover_regression_ok": by_id.get("LOOP-CUTOVER", False) if "LOOP-CUTOVER" in by_id else True,
        "dynamic_flow_regression_ok": by_id.get("DYNAMIC-COMPATIBILITY", False) if "DYNAMIC-COMPATIBILITY" in by_id else True,
        "real_input_regression_ok": by_id.get("REAL-INPUT", False) if "REAL-INPUT" in by_id else True,
        "real_capability_single_invocation_regression_ok": by_id.get("REAL-CAPABILITY", False) if "REAL-CAPABILITY" in by_id else True,
        "provider_invocation_count_observed": max(provider_counts, default=0),
        "provider_invocation_max_allowed": max((item["max_provider_invocation_count"] for item in entries), default=0),
        "second_provider_invocation_observed": second_invocation,
        "provider_invocation_attempted": any(item.get("provider_invocation_attempted", False) for item in real_results),
        "real_capability_status": next((item["status"] for item in real_results if item["regression_id"] == REAL_CAPABILITY_REGRESSION_ID), "NOT_RUN"),
        "real_capability_missing_argument_names": next((item.get("missing_argument_names", []) for item in real_results if item["regression_id"] == REAL_CAPABILITY_REGRESSION_ID), []),
        "failure_classifications": sorted({failure["class"] for item in results for failure in item["failures"]}),
        "all_regressions_passed": not failed,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Consolidated Luna cognitive mainline regression checkpoint")
    parser.add_argument("--group", choices=("synthetic", "real-approved", "all"), default="synthetic")
    parser.add_argument("--real-capability-source")
    parser.add_argument("--real-capability-model-path")
    parser.add_argument("--real-capability-dependency-status")
    parser.add_argument("--real-capability-declared-checksum")
    parser.add_argument("--real-capability-observed-checksum")
    args = parser.parse_args()
    summary = build_regression_summary_v1(
        args.group,
        {
            "source": args.real_capability_source,
            "model_path": args.real_capability_model_path,
            "dependency_status": args.real_capability_dependency_status,
            "declared_checksum": args.real_capability_declared_checksum,
            "observed_checksum": args.real_capability_observed_checksum,
        },
    )
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(_jsonable(summary), ensure_ascii=False, indent=2), encoding="utf-8")
    compact = dict(summary)
    compact.pop("results", None)
    print(json.dumps(_jsonable(compact), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_regressions_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
