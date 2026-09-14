"""Static and report-based verifier for the consolidated regression checkpoint."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir() and (_candidate / "README.md").is_file():
        REPO_ROOT = _candidate
        break
else:  # pragma: no cover
    REPO_ROOT = VERIFIER_PATH.parents[7]

MANIFEST_PATH = REPO_ROOT / "docs/architecture/phase_luna_cognitive_mainline_consolidated_regression_checkpoint_v1/cognitive_mainline_regression_manifest_v1.json"
REPORT_PATH = REPO_ROOT / "_eval_out/cognitive_mainline_consolidated_regression_checkpoint_v1/regression_summary_v1.json"
PACKAGE_DIR = VERIFIER_PATH.parent
EXPECTED_SOURCE_SET = {
    "__init__.py",
    "run_cognitive_mainline_consolidated_regression_checkpoint_v1.py",
    "verify_cognitive_mainline_consolidated_regression_checkpoint_v1.py",
}
DOC_DIR = REPO_ROOT / "docs/architecture/phase_luna_cognitive_mainline_consolidated_regression_checkpoint_v1"
EXPECTED_DOC_SET = {
    "change_manifest.md",
    "cognitive_mainline_regression_manifest_v1.json",
    "failure_classification_v1.md",
    "negative_boundaries_v1.md",
    "phase_contract.md",
    "real_boundary_regression_contract_v1.md",
    "regression_execution_order_v1.md",
    "regression_scope_v1.md",
    "shared_asset_delta_inventory_v1.md",
    "synthetic_regression_contract_v1.md",
    "verified_phase_inventory_v1.md",
}


def _check(name: str, passed: bool, actual: Any = None, expected: Any = True) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "actual": actual, "expected": expected}


def _load(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _manifest_checks(manifest: dict[str, Any] | None) -> list[dict[str, Any]]:
    if manifest is None:
        return [_check("manifest_ok", False, "missing_or_invalid", "valid_manifest")]
    phases = manifest.get("phases", [])
    required = {"regression_id", "phase_name", "runner_path", "verifier_path", "regression_group", "expected_runner_fields", "expected_verifier_fields", "real_runtime_allowed", "provider_allowed", "max_provider_invocation_count", "dependency_refs"}
    entries_ok = bool(phases) and all(required.issubset(item) for item in phases if isinstance(item, dict))
    groups_ok = {item.get("regression_group") for item in phases if isinstance(item, dict)} == {"synthetic", "real-approved"}
    paths_ok = all((REPO_ROOT / item["runner_path"]).is_file() and (REPO_ROOT / item["verifier_path"]).is_file() for item in phases if isinstance(item, dict))
    return [
        _check("manifest_ok", manifest.get("phase") == "Phase-Luna-Cognitive-Mainline-Consolidated-Regression-Checkpoint-v1-001" and entries_ok and groups_ok and paths_ok),
        _check("phase_inventory_ok", len(phases) == 8, len(phases), 8),
    ]


def build_verification_summary_v1() -> dict[str, Any]:
    manifest = _load(MANIFEST_PATH)
    checks = _manifest_checks(manifest)
    if manifest is not None:
        delta_doc = DOC_DIR / "shared_asset_delta_inventory_v1.md"
        checks.append(_check("shared_asset_delta_inventory_ok", delta_doc.is_file() and "authority_grant_mechanical_command_registry_v1.py" in delta_doc.read_text(encoding="utf-8")))
    else:
        checks.append(_check("shared_asset_delta_inventory_ok", False))
    report = _load(REPORT_PATH)
    if report is None:
        checks.extend(
            _check(name, False, "regression_report_missing", True)
            for name in (
                "synthetic_phase_results_ok",
                "authority_regression_ok",
                "a_semantic_regression_ok",
                "ab_cr_regression_ok",
                "working_envelope_regression_ok",
                "loop_mechanical_regression_ok",
                "dynamic_flow_compatibility_regression_ok",
                "real_input_contract_ok",
                "real_capability_single_invocation_contract_ok",
                "provider_invocation_limit_ok",
                "no_second_provider_invocation_ok",
            )
        )
    else:
        checks.extend([
            _check("synthetic_phase_results_ok", report.get("synthetic_regression_ok") is True),
            _check("authority_regression_ok", report.get("shared_registry_regression_ok") is True),
            _check("a_semantic_regression_ok", report.get("a_semantic_regression_ok") is True),
            _check("ab_cr_regression_ok", report.get("ab_cr_regression_ok") is True),
            _check("working_envelope_regression_ok", report.get("working_envelope_regression_ok") is True),
            _check("loop_mechanical_regression_ok", report.get("loop_cutover_regression_ok") is True),
            _check("dynamic_flow_compatibility_regression_ok", report.get("dynamic_flow_regression_ok") is True),
            _check("real_input_contract_ok", report.get("real_input_regression_ok") is True),
            _check("real_capability_single_invocation_contract_ok", report.get("real_capability_single_invocation_regression_ok") is True),
            _check("provider_invocation_limit_ok", report.get("provider_invocation_count_observed", 0) <= report.get("provider_invocation_max_allowed", 0)),
            _check("no_second_provider_invocation_ok", report.get("second_provider_invocation_observed") is False),
        ])
    checks.extend(
        (
            _check("negative_boundaries_ok", (DOC_DIR / "negative_boundaries_v1.md").is_file()),
            _check("source_set_ok", {item.name for item in PACKAGE_DIR.iterdir() if item.is_file() and item.suffix == ".py"} == EXPECTED_SOURCE_SET),
            _check("documentation_set_ok", DOC_DIR.is_dir() and {item.name for item in DOC_DIR.iterdir() if item.is_file()} == EXPECTED_DOC_SET),
        )
    )
    failed_checks = [item["name"] for item in checks if not item["passed"]]
    return {
        "phase": "Phase-Luna-Cognitive-Mainline-Consolidated-Regression-Checkpoint-v1-001",
        "all_checks_passed": not failed_checks,
        "failed_case_ids": [] if report is None else report.get("failed_regression_ids", []),
        "failed_checks": failed_checks,
        "manifest_ok": next(item["passed"] for item in checks if item["name"] == "manifest_ok"),
        "phase_inventory_ok": next(item["passed"] for item in checks if item["name"] == "phase_inventory_ok"),
        "shared_asset_delta_inventory_ok": next(item["passed"] for item in checks if item["name"] == "shared_asset_delta_inventory_ok"),
        "synthetic_phase_results_ok": next(item["passed"] for item in checks if item["name"] == "synthetic_phase_results_ok"),
        "authority_regression_ok": next(item["passed"] for item in checks if item["name"] == "authority_regression_ok"),
        "a_semantic_regression_ok": next(item["passed"] for item in checks if item["name"] == "a_semantic_regression_ok"),
        "ab_cr_regression_ok": next(item["passed"] for item in checks if item["name"] == "ab_cr_regression_ok"),
        "working_envelope_regression_ok": next(item["passed"] for item in checks if item["name"] == "working_envelope_regression_ok"),
        "loop_mechanical_regression_ok": next(item["passed"] for item in checks if item["name"] == "loop_mechanical_regression_ok"),
        "dynamic_flow_compatibility_regression_ok": next(item["passed"] for item in checks if item["name"] == "dynamic_flow_compatibility_regression_ok"),
        "real_input_contract_ok": next(item["passed"] for item in checks if item["name"] == "real_input_contract_ok"),
        "real_capability_single_invocation_contract_ok": next(item["passed"] for item in checks if item["name"] == "real_capability_single_invocation_contract_ok"),
        "real_boundary_regression_executed": False if report is None else report.get("real_boundary_regression_executed", False),
        "real_capability_status": "NOT_RUN" if report is None else report.get("real_capability_status", "NOT_RUN"),
        "real_capability_missing_argument_names": [] if report is None else report.get("real_capability_missing_argument_names", []),
        "provider_invocation_limit_ok": next(item["passed"] for item in checks if item["name"] == "provider_invocation_limit_ok"),
        "no_second_provider_invocation_ok": next(item["passed"] for item in checks if item["name"] == "no_second_provider_invocation_ok"),
        "negative_boundaries_ok": next(item["passed"] for item in checks if item["name"] == "negative_boundaries_ok"),
        "source_set_ok": next(item["passed"] for item in checks if item["name"] == "source_set_ok"),
        "documentation_set_ok": next(item["passed"] for item in checks if item["name"] == "documentation_set_ok"),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the consolidated cognitive regression checkpoint")
    parser.add_argument("--allow-missing-report", action="store_true")
    args = parser.parse_args()
    summary = build_verification_summary_v1()
    if args.allow_missing_report and REPORT_PATH.is_file() is False:
        summary["failed_checks"] = [item for item in summary["failed_checks"] if item not in {"synthetic_phase_results_ok", "authority_regression_ok", "a_semantic_regression_ok", "ab_cr_regression_ok", "working_envelope_regression_ok", "loop_mechanical_regression_ok", "dynamic_flow_compatibility_regression_ok", "real_input_contract_ok", "real_capability_single_invocation_contract_ok", "provider_invocation_limit_ok", "no_second_provider_invocation_ok"}]
        summary["all_checks_passed"] = not summary["failed_checks"]
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
