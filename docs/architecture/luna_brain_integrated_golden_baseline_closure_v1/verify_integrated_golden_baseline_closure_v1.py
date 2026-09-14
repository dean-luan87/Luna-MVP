"""Deterministic verifier for integrated closure metadata only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.brain_golden_baseline.brain_golden_baseline_governance_v1 import load_baseline_snapshot, validate_baseline
from capabilities.midplatform.core.brain_golden_baseline.integrated_closure.integrated_closure_fixture_v1 import build_cases
from capabilities.midplatform.core.brain_golden_baseline.integrated_closure.integrated_closure_governance_v1 import _continuity_checks


IMPLEMENTATION_ROOT = REPO_ROOT / "capabilities" / "midplatform" / "core" / "brain_golden_baseline" / "integrated_closure"
DOCUMENT_ROOT = Path(__file__).resolve().parent
SOURCE_SUFFIXES = {".py", ".md", ".json"}

EXPECTED_IMPLEMENTATION_FILES = {
    "__init__.py",
    "integrated_closure_types_v1.py",
    "integrated_closure_governance_v1.py",
    "integrated_closure_fixture_v1.py",
    "run_integrated_golden_baseline_closure_v1.py",
}

EXPECTED_DOCUMENT_FILES = {
    "overview.md",
    "overall_test_plan.md",
    "phase_regression_index.md",
    "cross_phase_contract_matrix.md",
    "owner_mutation_continuity.md",
    "candidate_truth_continuity.md",
    "trace_provenance_continuity.md",
    "real_synthetic_continuity.md",
    "terminal_evidence_contract.md",
    "terminal_evidence_registration_v1.json",
    "freeze_candidate_contract.md",
    "negative_guards.md",
    "scenario_mapping.md",
    "change_manifest.md",
    "implementation_summary.md",
    "phase_contract.md",
    "verify_integrated_golden_baseline_closure_v1.py",
}

FORBIDDEN_EXECUTION_MARKERS = (
    "subprocess",
    "os.system",
    "ultralytics",
    "torch.",
    "requests.",
    "model.predict(",
    "provider.invoke(",
)


def _files(directory: Path) -> set[str]:
    return {
        path.name
        for path in directory.iterdir()
        if path.is_file() and not path.name.startswith(".") and path.suffix in SOURCE_SUFFIXES
    }


def _execution_markers() -> list[str]:
    findings: list[str] = []
    for path in IMPLEMENTATION_ROOT.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_EXECUTION_MARKERS:
            if marker in text:
                findings.append(f"{path.name}:{marker}")
    return findings


def build_verifier_result() -> dict[str, object]:
    implementation_actual = _files(IMPLEMENTATION_ROOT)
    documentation_actual = _files(DOCUMENT_ROOT)
    implementation_missing = sorted(EXPECTED_IMPLEMENTATION_FILES - implementation_actual)
    implementation_extra = sorted(implementation_actual - EXPECTED_IMPLEMENTATION_FILES)
    documentation_missing = sorted(EXPECTED_DOCUMENT_FILES - documentation_actual)
    documentation_extra = sorted(documentation_actual - EXPECTED_DOCUMENT_FILES)
    case_results = {case_id: bool(check()) for case_id, check in build_cases().items()}
    failed_cases = [case_id for case_id, passed in case_results.items() if not passed]
    continuity = _continuity_checks(load_baseline_snapshot())
    failures: list[str] = []
    if implementation_missing or implementation_extra or documentation_missing or documentation_extra:
        failures.append("exact implementation/documentation file set mismatch")
    if validate_baseline():
        failures.append("B5 consistency failure")
    if failed_cases:
        failures.append("closure scenario failure")
    if not all(continuity.values()):
        failures.append("cross-phase continuity failure")
    if _execution_markers():
        failures.append("forbidden execution marker")
    return {
        "phase": "Phase-Luna-Brain-Integrated-Golden-Baseline-Closure-v1-001",
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
        "continuity": continuity,
        "automatic_regression_execution": False,
        "business_logic_execution": False,
        "provider_invocation": False,
        "runtime_execution": False,
        "freeze_is_automatic": False,
    }


if __name__ == "__main__":
    print(json.dumps(build_verifier_result(), indent=2, sort_keys=True))
