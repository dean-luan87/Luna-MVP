#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path(
    "capabilities/midplatform/model_manager/runtime/document_surface/"
    "option_b_controlled_execution_dryrun/explicit_dependency_probe_dryrun"
)

RESULT_PATH = BASE / "explicit_dependency_probe_dryrun_result_v1.json"
SUMMARY_PATH = BASE / "explicit_dependency_probe_dryrun_summary_v1.json"

EXPECTED_CANDIDATES = [
    "A1_classical_helper_ok_candidate",
    "C1_document_specific_surface_model_ok_for_preflight",
]

EXPECTED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-"
    "Ownership-Document-Surface-Detector-OptionB-Controlled-Execution-"
    "DryRun-Explicit-Dependency-Probe-PostReview-v1-001"
)

checks = {}
failed_checks = []

for path in [RESULT_PATH, SUMMARY_PATH]:
    checks[f"{path.name}_exists"] = path.is_file()
    if not path.is_file():
        failed_checks.append(f"{path.name}_exists")

if checks.get(
    "explicit_dependency_probe_dryrun_result_v1.json_exists", False
) and checks.get("explicit_dependency_probe_dryrun_summary_v1.json_exists", False):
    try:
        result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        checks["result_json_valid"] = True
        checks["summary_json_valid"] = True
    except json.JSONDecodeError:
        checks["result_json_valid"] = False
        checks["summary_json_valid"] = False
        failed_checks.extend(["result_json_valid", "summary_json_valid"])
        result = {}
        summary = {}
else:
    result = {}
    summary = {}

candidate_records = result.get("candidate_records", [])
actual_ids = [item.get("candidate_id") for item in candidate_records]
checks["candidate_ids_match"] = actual_ids == EXPECTED_CANDIDATES
if not checks["candidate_ids_match"]:
    failed_checks.append("candidate_ids_match")

for candidate in candidate_records:
    cid = candidate.get("candidate_id")
    if cid not in EXPECTED_CANDIDATES:
        continue
    checks[f"{cid}_probe_performed_false"] = candidate.get("probe_performed") is False
    checks[f"{cid}_dependency_present_unknown"] = (
        candidate.get("dependency_present") == "unknown"
    )
    checks[f"{cid}_import_performed_false"] = candidate.get("import_performed") is False
    checks[f"{cid}_pip_performed_false"] = candidate.get("pip_performed") is False
    checks[f"{cid}_subprocess_performed_false"] = (
        candidate.get("subprocess_performed") is False
    )
    checks[f"{cid}_candidate_only_true"] = candidate.get("candidate_only") is True
    checks[f"{cid}_not_fact_true"] = candidate.get("not_fact") is True

    if not checks[f"{cid}_probe_performed_false"]:
        failed_checks.append(f"{cid}_probe_performed_false")
    if not checks[f"{cid}_dependency_present_unknown"]:
        failed_checks.append(f"{cid}_dependency_present_unknown")
    if not checks[f"{cid}_import_performed_false"]:
        failed_checks.append(f"{cid}_import_performed_false")
    if not checks[f"{cid}_pip_performed_false"]:
        failed_checks.append(f"{cid}_pip_performed_false")
    if not checks[f"{cid}_subprocess_performed_false"]:
        failed_checks.append(f"{cid}_subprocess_performed_false")
    if not checks[f"{cid}_candidate_only_true"]:
        failed_checks.append(f"{cid}_candidate_only_true")
    if not checks[f"{cid}_not_fact_true"]:
        failed_checks.append(f"{cid}_not_fact_true")

checks["summary_candidate_count_2"] = summary.get("candidate_count") == 2
checks["summary_probe_performed_count_0"] = summary.get("probe_performed_count") == 0
checks["summary_dependency_confirmed_count_0"] = (
    summary.get("dependency_confirmed_count") == 0
)
checks["summary_version_confirmed_count_0"] = (
    summary.get("version_confirmed_count") == 0
)
checks["summary_import_count_0"] = summary.get("import_count") == 0
checks["summary_pip_count_0"] = summary.get("pip_count") == 0
checks["summary_subprocess_count_0"] = summary.get("subprocess_count") == 0
checks["summary_execution_admitted_count_0"] = (
    summary.get("execution_admitted_count") == 0
)
checks["summary_download_count_0"] = summary.get("download_count") == 0
checks["summary_install_count_0"] = summary.get("install_count") == 0
checks["summary_image_read_count_0"] = summary.get("image_read_count") == 0
checks["summary_segmentation_execution_count_0"] = (
    summary.get("segmentation_execution_count") == 0
)
checks["summary_runtime_activation_count_0"] = (
    summary.get("runtime_activation_count") == 0
)
checks["summary_candidate_only_true"] = summary.get("candidate_only") is True
checks["summary_not_fact_true"] = summary.get("not_fact") is True
checks["summary_blocker_count_0"] = summary.get("blocker_count") == 0
checks["summary_final_decision_matches"] = (
    summary.get("final_decision") == "EXPLICIT_DEPENDENCY_PROBE_DRYRUN_GO"
)
checks["summary_next_phase_matches"] = (
    summary.get("recommended_next_phase") == EXPECTED_NEXT_PHASE
)

for name in [
    "summary_candidate_count_2",
    "summary_probe_performed_count_0",
    "summary_dependency_confirmed_count_0",
    "summary_version_confirmed_count_0",
    "summary_import_count_0",
    "summary_pip_count_0",
    "summary_subprocess_count_0",
    "summary_execution_admitted_count_0",
    "summary_download_count_0",
    "summary_install_count_0",
    "summary_image_read_count_0",
    "summary_segmentation_execution_count_0",
    "summary_runtime_activation_count_0",
    "summary_candidate_only_true",
    "summary_not_fact_true",
    "summary_blocker_count_0",
    "summary_final_decision_matches",
    "summary_next_phase_matches",
]:
    if not checks[name]:
        failed_checks.append(name)

passed_count = sum(1 for value in checks.values() if value is True)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = "EXPLICIT_DEPENDENCY_PROBE_DRYRUN_GO"
if failed_count > 0:
    final_decision = "EXPLICIT_DEPENDENCY_PROBE_DRYRUN_BLOCKED"

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
