"""Fail-closed normalization for child synthetic Runner/Verifier output."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from .manifest_v1 import ChildModuleSpecV1


def _json_object(raw: str) -> Optional[Dict[str, Any]]:
    try:
        value = json.loads(raw)
    except (TypeError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def normalize_runner_output(
    spec: ChildModuleSpecV1,
    *,
    attempt_id: str,
    returncode: int,
    stdout: str,
    stderr: str,
) -> Dict[str, Any]:
    summary = _json_object(stdout) if returncode == 0 else None
    shape_ok = summary is not None and isinstance(summary.get("case_results"), list)
    count_ok = shape_ok and summary.get("scenario_count") == spec.expected_scenario_count
    runner_passed = bool(shape_ok and count_ok and summary.get("all_cases_passed") is True)
    return {
        "module_id": spec.module_id,
        "attempt_id": attempt_id,
        "artifact_mode": "current_in_memory_stdout",
        "runner_exit_code": returncode,
        "runner_stdout_present": bool(stdout),
        "runner_stderr": stderr[-2000:],
        "runner_json_shape_ok": shape_ok,
        "runner_scenario_count_ok": count_ok,
        "runner_passed": runner_passed,
        "summary": summary,
        "verifier_called": False,
        "verifier_passed": False,
        "verifier_checks": {},
        "stale_artifact_used": False,
    }


def normalize_verifier_output(
    child: Dict[str, Any],
    *,
    attempt_id: str,
    returncode: int,
    stdout: str,
    stderr: str,
) -> Dict[str, Any]:
    checks = _json_object(stdout) if returncode == 0 else None
    checks_ok = bool(checks is not None and checks and all(value is True for value in checks.values()))
    child.update({
        "attempt_id": attempt_id,
        "verifier_called": True,
        "verifier_exit_code": returncode,
        "verifier_stdout_present": bool(stdout),
        "verifier_stderr": stderr[-2000:],
        "verifier_checks": checks or {},
        "verifier_passed": checks_ok,
    })
    return child

