"""Deterministic verifier for B5 metadata governance only.

This verifier intentionally does not invoke the B1–B4 runners or any runtime.
Exact-file checks include only regular source/document files and ignore
__pycache__, hidden files, and generated artifacts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.brain_golden_baseline.brain_golden_baseline_fixture_v1 import build_cases
from capabilities.midplatform.core.brain_golden_baseline.brain_golden_baseline_governance_v1 import (
    validate_baseline,
)


IMPLEMENTATION_ROOT = REPO_ROOT / "capabilities" / "midplatform" / "core" / "brain_golden_baseline"
DOCUMENT_ROOT = Path(__file__).resolve().parent

EXPECTED_IMPLEMENTATION_FILES = {
    "__init__.py",
    "brain_golden_baseline_types_v1.py",
    "brain_golden_baseline_governance_v1.py",
    "brain_golden_baseline_fixture_v1.py",
    "run_brain_golden_baseline_controlled_implementation_v1.py",
}

EXPECTED_DOCUMENT_FILES = {
    "overview.md",
    "manifest_contract.md",
    "phase_index.md",
    "owner_mutation_matrix.md",
    "regression_index.md",
    "change_impact_contract.md",
    "compatibility_policy.md",
    "candidate_truth_invariants.md",
    "real_synthetic_boundary.md",
    "trace_provenance_baseline.md",
    "negative_guards.md",
    "future_provider_runtime_policy.md",
    "scenario_mapping.md",
    "change_manifest.md",
    "implementation_summary.md",
    "phase_contract.md",
    "verify_brain_golden_baseline_controlled_implementation_v1.py",
}

SOURCE_SUFFIXES = {".py", ".json", ".md"}
FORBIDDEN_EXECUTION_MARKERS = (
    "subprocess",
    "os.system",
    "ultralytics",
    "torch.",
    "requests.",
    "model.predict(",
    "provider.invoke(",
)


def _source_files(directory: Path) -> set[str]:
    return {
        path.name
        for path in directory.iterdir()
        if path.is_file() and not path.name.startswith(".") and path.suffix in SOURCE_SUFFIXES
    }


def _static_execution_markers() -> list[str]:
    findings: list[str] = []
    for path in IMPLEMENTATION_ROOT.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_EXECUTION_MARKERS:
            if marker in text:
                findings.append(f"{path.name}:{marker}")
    return findings


def build_verifier_result() -> dict[str, object]:
    implementation_actual = _source_files(IMPLEMENTATION_ROOT)
    documentation_actual = _source_files(DOCUMENT_ROOT)
    implementation_missing = sorted(EXPECTED_IMPLEMENTATION_FILES - implementation_actual)
    implementation_extra = sorted(implementation_actual - EXPECTED_IMPLEMENTATION_FILES)
    documentation_missing = sorted(EXPECTED_DOCUMENT_FILES - documentation_actual)
    documentation_extra = sorted(documentation_actual - EXPECTED_DOCUMENT_FILES)
    file_set_ok = not (implementation_missing or implementation_extra or documentation_missing or documentation_extra)

    issues = [issue.__dict__ for issue in validate_baseline()]
    case_results = {case_id: bool(check()) for case_id, check in build_cases().items()}
    failed_cases = [case_id for case_id, passed in case_results.items() if not passed]
    static_findings = _static_execution_markers()
    failures = []
    if not file_set_ok:
        failures.append("exact implementation/documentation file set mismatch")
    if issues:
        failures.append("baseline consistency issues")
    if failed_cases:
        failures.append("governance scenario failure")
    if static_findings:
        failures.append("forbidden execution marker")

    return {
        "phase": "Phase-Luna-Brain-B5-Real-Evidence-Cognitive-Loop-Golden-Baseline-Controlled-Implementation-v1-001",
        "owner": "Brain Golden Baseline Governance",
        "failed_check_count": len(failures),
        "blocker_count": len(failures),
        "failures": failures,
        "implementation_expected_files": sorted(EXPECTED_IMPLEMENTATION_FILES),
        "implementation_actual_files": sorted(implementation_actual),
        "documentation_expected_files": sorted(EXPECTED_DOCUMENT_FILES),
        "documentation_actual_files": sorted(documentation_actual),
        "implementation_missing": implementation_missing,
        "implementation_extra": implementation_extra,
        "documentation_missing": documentation_missing,
        "documentation_extra": documentation_extra,
        "scenario_count": len(case_results),
        "all_cases_passed": not failed_cases,
        "failed_case_ids": failed_cases,
        "business_logic_execution": False,
        "automatic_regression_execution": False,
        "provider_invocation": False,
        "model_inference": False,
        "runtime_execution": False,
        "static_execution_findings": static_findings,
    }


if __name__ == "__main__":
    print(json.dumps(build_verifier_result(), indent=2, sort_keys=True))
