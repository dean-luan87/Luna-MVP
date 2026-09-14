"""Read-only verifier for the persisted one-invocation trial snapshot."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


VERIFIER_PATH = Path(__file__).resolve()
PHASE = "Phase-Luna-Dynamic-Cognitive-Flow-Real-Capability-Single-Invocation-Trial-v1-001"
OUT_DIR_NAME = "luna_dynamic_cognitive_flow_real_capability_single_invocation_trial_v1"


def _resolve_repo_root() -> Path:
    for candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
OUT_DIR = REPO_ROOT / "_eval_out" / OUT_DIR_NAME
SOURCE_ROOT = REPO_ROOT / "capabilities/midplatform/core/cognitive_flow/integration/dynamic_cognitive_flow_real_capability_single_invocation_trial"
DOC_ROOT = REPO_ROOT / "docs/architecture/phase_luna_dynamic_cognitive_flow_real_capability_single_invocation_trial_v1"
SOURCE_SET = {
    "__init__.py",
    "dynamic_cognitive_flow_real_capability_trial_types_v1.py",
    "dynamic_cognitive_flow_real_capability_trial_fixture_v1.py",
    "dynamic_cognitive_flow_real_capability_trial_adapter_v1.py",
    "real_capability_runtime_admission_compatibility_adapter_v1.py",
    "run_dynamic_cognitive_flow_real_capability_single_invocation_trial_v1.py",
    "verify_dynamic_cognitive_flow_real_capability_single_invocation_trial_v1.py",
}
DOCUMENTATION_SET = {
    "phase_contract.json",
    "inventory_v1.json",
    "resolution_path_v1.json",
    "real_boundary_v1.json",
    "scenario_mapping_v1.json",
    "negative_guards_v1.json",
    "change_manifest_v1.json",
    "verifier_scope_v1.json",
    "implementation_summary_v1.md",
}


def _check(name: str, expected: Any, actual: Any) -> Dict[str, Any]:
    return {"name": name, "expected": expected, "actual": actual, "passed": expected == actual}


def verify() -> Dict[str, Any]:
    checks = []
    summary_path = OUT_DIR / "trial_summary_v1.json"
    snapshot_path = OUT_DIR / "trial_snapshot_v1.json"
    if not summary_path.is_file() or not snapshot_path.is_file():
        checks.append(_check("runner_snapshot_present", True, False))
        return {
            "phase": PHASE,
            "all_checks_passed": False,
            "failed_case_ids": [],
            "failed_checks": ["runner_snapshot_present"],
            "scenario_cases_ok": False,
            "negative_guards_ok": False,
            "source_set_ok": {path.name for path in SOURCE_ROOT.iterdir() if path.is_file()} == SOURCE_SET,
            "documentation_set_ok": {path.name for path in DOC_ROOT.iterdir() if path.is_file()} == DOCUMENTATION_SET,
            "checks": checks,
        }
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    source_set_ok = {path.name for path in SOURCE_ROOT.iterdir() if path.is_file()} == SOURCE_SET
    documentation_set_ok = {path.name for path in DOC_ROOT.iterdir() if path.is_file()} == DOCUMENTATION_SET
    checks.extend(
        [
            _check("phase", PHASE, summary.get("phase")),
            _check("scenario_count", 22, summary.get("scenario_count")),
            _check("scenario_cases_ok", True, summary.get("all_cases_passed")),
            _check("real_provider_invocation_count", 1, summary.get("real_provider_invocation_count")),
            _check("runtime_admission_boundary_ok", "READY_FOR_EXECUTABLE_CANDIDATE", summary.get("runtime_admission_status")),
            _check("logical_ready_not_executable_ready", True, summary.get("logical_resolution_status") == "READY_CANDIDATE" and summary.get("executable_capability_created") is True),
            _check("executable_candidate_required", True, summary.get("executable_capability_created") is True and summary.get("runtime_admission_bypassed") is False),
            _check("provider_single_invocation_ok", True, summary.get("real_provider_invocation_count", 0) <= 1 and summary.get("second_provider_invocation") is False),
            _check("request_more_evidence_no_second_invocation", True, summary.get("real_provider_invocation_count", 0) == 1 and summary.get("second_provider_invocation") is False),
            _check("a_semantic_cutover_preserved", True, summary.get("a_interpretation_reached") is True),
            _check("dynamic_compatibility_boundary_ok", False, summary.get("dynamic_flow_semantic_authority")),
            _check("max_real_provider_invocation", 1, summary.get("max_real_provider_invocation")),
            _check("single_frame", True, summary.get("single_frame")),
            _check("gateway_admitted", True, summary.get("gateway_admitted")),
            _check("current_world_created", True, summary.get("current_world_created")),
            _check("candidate_only", True, summary.get("candidate_only")),
            _check("provider_semantic_authority", False, summary.get("provider_semantic_authority")),
            _check("world_truth_authority", False, summary.get("world_truth_authority")),
            _check("second_real_invocation_allowed", False, summary.get("second_real_invocation_allowed")),
            _check("continuous_camera_allowed", False, summary.get("continuous_camera_allowed")),
            _check("model_download_allowed", False, summary.get("model_download_allowed")),
            _check("action_execution", False, summary.get("action_execution")),
            _check("learning_execution", False, summary.get("learning_execution")),
            _check("memory_mutation", False, summary.get("memory_mutation")),
            _check("source_set_ok", True, source_set_ok),
            _check("documentation_set_ok", True, documentation_set_ok),
            _check("snapshot_trial_id", True, bool(snapshot.get("trial_id"))),
            _check("snapshot_requirement_ref", True, bool(snapshot.get("requirement_ref"))),
        ]
    )
    failed_case_ids = list(summary.get("failed_case_ids", ()))
    failed_checks = [item["name"] for item in checks if not item["passed"]]
    return {
        "phase": PHASE,
        "all_checks_passed": not failed_case_ids and not failed_checks,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "scenario_cases_ok": bool(summary.get("all_cases_passed")),
        "negative_guards_ok": not any(
            summary.get(name, False)
            for name in ("provider_semantic_authority", "world_truth_authority", "second_real_invocation_allowed", "continuous_camera_allowed", "model_download_allowed", "action_execution", "learning_execution", "memory_mutation")
        ),
        "source_set_ok": source_set_ok,
        "documentation_set_ok": documentation_set_ok,
        "checks": checks,
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["all_checks_passed"] else 1)


__all__ = ["verify"]
