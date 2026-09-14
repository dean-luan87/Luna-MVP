"""Structural verifier for the controlled integrated cognitive loop."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


VERIFIER_PATH = Path(__file__).resolve()


def _resolve_repo_root() -> Path:
    for candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_flow.integration.real_input_dynamic_cognitive_loop_controlled.run_real_input_dynamic_cognitive_loop_integrated_controlled_implementation_v1 import (  # noqa: E402
    PHASE,
    build_runner_result,
)


SOURCE_ROOT = REPO_ROOT / "capabilities/midplatform/core/cognitive_flow/integration/real_input_dynamic_cognitive_loop_controlled"
DOC_ROOT = REPO_ROOT / "docs/architecture/phase_luna_real_input_dynamic_cognitive_loop_integrated_controlled_implementation_v1"
SOURCE_SET = {
    "__init__.py",
    "real_input_dynamic_cognitive_loop_integration_types_v1.py",
    "real_input_dynamic_cognitive_loop_integration_adapter_v1.py",
    "real_input_dynamic_cognitive_loop_integration_fixture_v1.py",
    "run_real_input_dynamic_cognitive_loop_integrated_controlled_implementation_v1.py",
    "verify_real_input_dynamic_cognitive_loop_integrated_controlled_implementation_v1.py",
}
DOCUMENTATION_SET = {
    "phase_contract.json",
    "inventory_v1.json",
    "integrated_flow_contract_v1.json",
    "real_synthetic_boundary_v1.json",
    "scenario_mapping_v1.json",
    "negative_guards_v1.json",
    "change_manifest_v1.json",
    "verifier_scope_v1.json",
    "implementation_summary_v1.md",
}


def _check(name: str, expected: Any, actual: Any) -> Dict[str, Any]:
    return {"name": name, "expected": expected, "actual": actual, "passed": expected == actual}


def verify() -> Dict[str, Any]:
    runner = build_runner_result()
    checks = [
        _check("phase", PHASE, runner.get("phase")),
        _check("scenario_count", 28, runner.get("scenario_count")),
        _check("scenario_cases_ok", True, runner.get("all_cases_passed")),
        _check("negative_guards_ok", True, all(runner.get("key_dynamic_loop_guards", {}).values())),
        _check("source_set_ok", True, {path.name for path in SOURCE_ROOT.iterdir() if path.is_file()} == SOURCE_SET),
        _check("documentation_set_ok", True, {path.name for path in DOC_ROOT.iterdir() if path.is_file()} == DOCUMENTATION_SET),
        _check("candidate_only", True, runner.get("candidate_only")),
        _check("real_provider_execution", False, runner.get("real_provider_execution")),
        _check("model_runtime_execution", False, runner.get("model_runtime_execution")),
        _check("camera_activation", False, runner.get("camera_activation")),
        _check("action_execution", False, runner.get("action_execution")),
        _check("learning", False, runner.get("learning")),
        _check("memory_mutation", False, runner.get("memory_mutation")),
    ]
    failed_checks = [item["name"] for item in checks if not item["passed"]]
    failed_case_ids = list(runner.get("failed_case_ids", ()))
    return {
        "phase": PHASE,
        "all_checks_passed": not failed_checks and not failed_case_ids,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "scenario_cases_ok": runner.get("all_cases_passed", False),
        "negative_guards_ok": all(runner.get("key_dynamic_loop_guards", {}).values()),
        "source_set_ok": next(item["actual"] for item in checks if item["name"] == "source_set_ok"),
        "documentation_set_ok": next(item["actual"] for item in checks if item["name"] == "documentation_set_ok"),
        "checks": checks,
    }


if __name__ == "__main__":
    summary = verify()
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if summary["all_checks_passed"] else 1)


__all__ = ["verify"]
