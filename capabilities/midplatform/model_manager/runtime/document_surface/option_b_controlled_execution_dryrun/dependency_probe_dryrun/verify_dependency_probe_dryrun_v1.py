#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any

BASE = Path(
    "capabilities/midplatform/model_manager/runtime/document_surface/"
    "option_b_controlled_execution_dryrun/dependency_probe_dryrun"
)

RESULT_PATH = BASE / "dependency_probe_dryrun_result_v1.json"
SUMMARY_PATH = BASE / "dependency_probe_dryrun_summary_v1.json"

EXPECTED_CANDIDATES = [
    "A1_classical_helper_ok_candidate",
    "C1_document_specific_surface_model_ok_for_preflight",
]

EXPECTED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-"
    "Ownership-Document-Surface-Detector-OptionB-Dependency-And-Adapter-"
    "Probe-PostReview-v1-001"
)


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"missing required input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


checks: dict[str, bool] = {}
failed_checks: list[str] = []

try:
    result = load_json(RESULT_PATH)
    summary = load_json(SUMMARY_PATH)
    checks["input_files_exist_and_are_valid_json"] = True
except (FileNotFoundError, ValueError) as exc:
    print(f"ERROR: {exc}")
    checks["input_files_exist_and_are_valid_json"] = False
    result = {}
    summary = {}

if not checks.get("input_files_exist_and_are_valid_json", False):
    failed_checks.append("input_files_exist_and_are_valid_json")
else:
    candidate_records = result.get("candidate_records", [])
    candidate_ids = [item.get("candidate_id") for item in candidate_records]
    checks["candidate_ids_match_expected"] = candidate_ids == EXPECTED_CANDIDATES
    if not checks["candidate_ids_match_expected"]:
        failed_checks.append("candidate_ids_match_expected")

    for candidate in candidate_records:
        cid = candidate.get("candidate_id")
        if cid not in EXPECTED_CANDIDATES:
            continue
        checks[f"{cid}_dependency_present_unknown"] = (
            candidate.get("dependency_present") == "unknown"
        )
        checks[f"{cid}_adapter_present_unknown"] = (
            candidate.get("adapter_present") == "unknown"
        )
        checks[f"{cid}_probe_performed_false"] = (
            candidate.get("probe_performed") is False
        )
        checks[f"{cid}_candidate_only_true"] = candidate.get("candidate_only") is True
        checks[f"{cid}_not_fact_true"] = candidate.get("not_fact") is True

        if not checks[f"{cid}_dependency_present_unknown"]:
            failed_checks.append(f"{cid}_dependency_present_unknown")
        if not checks[f"{cid}_adapter_present_unknown"]:
            failed_checks.append(f"{cid}_adapter_present_unknown")
        if not checks[f"{cid}_probe_performed_false"]:
            failed_checks.append(f"{cid}_probe_performed_false")
        if not checks[f"{cid}_candidate_only_true"]:
            failed_checks.append(f"{cid}_candidate_only_true")
        if not checks[f"{cid}_not_fact_true"]:
            failed_checks.append(f"{cid}_not_fact_true")

    checks["summary_candidate_count_2"] = summary.get("candidate_count") == 2
    checks["summary_probe_performed_count_0"] = (
        summary.get("probe_performed_count") == 0
    )
    checks["summary_dependency_confirmed_count_0"] = (
        summary.get("dependency_confirmed_count") == 0
    )
    checks["summary_adapter_confirmed_count_0"] = (
        summary.get("adapter_confirmed_count") == 0
    )
    checks["summary_execution_count_0"] = summary.get("execution_count") == 0
    checks["summary_download_count_0"] = summary.get("download_count") == 0
    checks["summary_install_count_0"] = summary.get("install_count") == 0
    checks["summary_runtime_activation_count_0"] = (
        summary.get("runtime_activation_count") == 0
    )
    checks["summary_blocker_count_0"] = summary.get("blocker_count") == 0
    checks["summary_candidate_only_true"] = summary.get("candidate_only") is True
    checks["summary_not_fact_true"] = summary.get("not_fact") is True
    checks["summary_final_decision_matches"] = (
        summary.get("final_decision") == "DEPENDENCY_AND_ADAPTER_PROBE_DRYRUN_GO"
    )
    checks["summary_next_phase_matches"] = (
        summary.get("recommended_next_phase") == EXPECTED_NEXT_PHASE
    )

    for name in [
        "summary_candidate_count_2",
        "summary_probe_performed_count_0",
        "summary_dependency_confirmed_count_0",
        "summary_adapter_confirmed_count_0",
        "summary_execution_count_0",
        "summary_download_count_0",
        "summary_install_count_0",
        "summary_runtime_activation_count_0",
        "summary_blocker_count_0",
        "summary_candidate_only_true",
        "summary_not_fact_true",
        "summary_final_decision_matches",
        "summary_next_phase_matches",
    ]:
        if not checks[name]:
            failed_checks.append(name)

passed_count = sum(1 for value in checks.values() if value is True)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = "DEPENDENCY_AND_ADAPTER_PROBE_DRYRUN_GO"
if failed_count > 0:
    final_decision = "DEPENDENCY_AND_ADAPTER_PROBE_DRYRUN_BLOCKED"

print("CHECKS")
print(json.dumps(checks, ensure_ascii=False, indent=2))
print("FAILED_CHECKS")
print(json.dumps(failed_checks, ensure_ascii=False, indent=2))
print("PASSED_CHECK_COUNT")
print(passed_count)
print("FAILED_CHECK_COUNT")
print(failed_count)
print("BLOCKER_COUNT")
print(blocker_count)
print("FINAL_DECISION")
print(final_decision)
print("NEXT")
print(EXPECTED_NEXT_PHASE)

sys.exit(1 if failed_count > 0 else 0)
