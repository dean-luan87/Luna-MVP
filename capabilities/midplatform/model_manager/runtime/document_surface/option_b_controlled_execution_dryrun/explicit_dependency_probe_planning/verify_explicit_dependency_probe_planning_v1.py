#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path(
    "capabilities/midplatform/model_manager/runtime/document_surface/"
    "option_b_controlled_execution_dryrun/explicit_dependency_probe_planning"
)

PLAN_PATH = BASE / "explicit_dependency_probe_plan_v1.md"
CONTRACT_PATH = BASE / "explicit_dependency_probe_contract_v1.json"
SUMMARY_PATH = BASE / "explicit_dependency_probe_summary_v1.json"

EXPECTED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-"
    "Ownership-Document-Surface-Detector-OptionB-Controlled-Execution-"
    "DryRun-Explicit-Dependency-Probe-DryRun-v1-001"
)

REQUIRED_CONTRACT_FIELDS = [
    "dependency_name",
    "dependency_category",
    "expected_version",
    "version_required",
    "probe_strategy",
    "probe_result_type",
    "candidate_only",
    "not_fact",
]

checks = {}
failed_checks = []

files_exist = PLAN_PATH.is_file() and CONTRACT_PATH.is_file() and SUMMARY_PATH.is_file()
checks["input_files_exist"] = files_exist
if not files_exist:
    failed_checks.append("input_files_exist")

if files_exist:
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        checks["contract_json_valid"] = True
        checks["summary_json_valid"] = True
    except json.JSONDecodeError:
        checks["contract_json_valid"] = False
        checks["summary_json_valid"] = False
        failed_checks.append("contract_json_valid")
        failed_checks.append("summary_json_valid")
        contract = {}
        summary = {}

    if not checks.get("contract_json_valid", False):
        contract = {}
    if not checks.get("summary_json_valid", False):
        summary = {}

    missing_fields = [
        field for field in REQUIRED_CONTRACT_FIELDS if field not in contract
    ]
    checks["contract_has_required_fields"] = len(missing_fields) == 0
    if not checks["contract_has_required_fields"]:
        failed_checks.append("contract_has_required_fields")

    checks["contract_candidate_only_true"] = contract.get("candidate_only") is True
    checks["contract_not_fact_true"] = contract.get("not_fact") is True
    if not checks["contract_candidate_only_true"]:
        failed_checks.append("contract_candidate_only_true")
    if not checks["contract_not_fact_true"]:
        failed_checks.append("contract_not_fact_true")

    checks["summary_planning_completed_true"] = (
        summary.get("planning_completed") is True
    )
    checks["summary_probe_execution_allowed_false"] = (
        summary.get("probe_execution_allowed") is False
    )
    checks["summary_import_allowed_false"] = summary.get("import_allowed") is False
    checks["summary_pip_allowed_false"] = summary.get("pip_allowed") is False
    checks["summary_subprocess_allowed_false"] = (
        summary.get("subprocess_allowed") is False
    )
    checks["summary_runtime_allowed_false"] = summary.get("runtime_allowed") is False
    checks["summary_candidate_only_true"] = summary.get("candidate_only") is True
    checks["summary_not_fact_true"] = summary.get("not_fact") is True
    checks["summary_blocker_count_zero"] = summary.get("blocker_count") == 0
    checks["summary_final_decision_matches"] = (
        summary.get("final_decision") == "EXPLICIT_DEPENDENCY_PROBE_PLANNING_GO"
    )
    checks["summary_next_phase_matches"] = (
        summary.get("recommended_next_phase") == EXPECTED_NEXT_PHASE
    )

    for name in [
        "summary_planning_completed_true",
        "summary_probe_execution_allowed_false",
        "summary_import_allowed_false",
        "summary_pip_allowed_false",
        "summary_subprocess_allowed_false",
        "summary_runtime_allowed_false",
        "summary_candidate_only_true",
        "summary_not_fact_true",
        "summary_blocker_count_zero",
        "summary_final_decision_matches",
        "summary_next_phase_matches",
    ]:
        if not checks[name]:
            failed_checks.append(name)

passed_count = sum(1 for value in checks.values() if value is True)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = "EXPLICIT_DEPENDENCY_PROBE_PLANNING_GO"
if failed_count > 0:
    final_decision = "EXPLICIT_DEPENDENCY_PROBE_PLANNING_BLOCKED"

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
