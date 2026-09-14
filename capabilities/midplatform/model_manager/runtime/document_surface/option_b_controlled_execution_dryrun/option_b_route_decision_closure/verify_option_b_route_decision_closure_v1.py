#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path(
    "capabilities/midplatform/model_manager/runtime/document_surface/"
    "option_b_controlled_execution_dryrun/option_b_route_decision_closure"
)

MARKDOWN_PATH = BASE / "option_b_route_decision_closure_v1.md"
SUMMARY_PATH = BASE / "option_b_route_decision_closure_summary_v1.json"

checks = {}
failed_checks = []

for path in [MARKDOWN_PATH, SUMMARY_PATH]:
    checks[f"{path.name}_exists"] = path.is_file()
    if not path.is_file():
        failed_checks.append(f"{path.name}_exists")

if checks.get("option_b_route_decision_closure_v1.md_exists", False) and checks.get(
    "option_b_route_decision_closure_summary_v1.json_exists", False
):
    try:
        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        checks["summary_json_valid"] = True
    except json.JSONDecodeError:
        checks["summary_json_valid"] = False
        failed_checks.append("summary_json_valid")
        summary = {}
else:
    summary = {}

checks["review_completed_true"] = summary.get("review_completed") is True
checks["route_decision_completed_true"] = (
    summary.get("route_decision_completed") is True
)
checks["reviewed_candidate_count_2"] = summary.get("reviewed_candidate_count") == 2
checks["passed_check_count_37"] = summary.get("passed_check_count") == 37
checks["failed_check_count_0"] = summary.get("failed_check_count") == 0
checks["blocker_count_0"] = summary.get("blocker_count") == 0
checks["dependency_confirmed_count_0"] = summary.get("dependency_confirmed_count") == 0
checks["adapter_confirmed_count_0"] = summary.get("adapter_confirmed_count") == 0
checks["execution_admitted_candidate_count_0"] = (
    summary.get("execution_admitted_candidate_count") == 0
)
checks["option_a_status_baseline"] = (
    summary.get("option_a_status") == "baseline_candidate_retained"
)
checks["option_b_status_deferred"] = (
    summary.get("option_b_status") == "deferred_candidate_route"
)
checks["option_b_execution_allowed_false"] = (
    summary.get("option_b_execution_allowed") is False
)
checks["segmentation_execution_allowed_false"] = (
    summary.get("segmentation_execution_allowed") is False
)
checks["active_model_selected_false"] = summary.get("active_model_selected") is False
checks["active_skill_selected_false"] = summary.get("active_skill_selected") is False
checks["active_registry_update_allowed_false"] = (
    summary.get("active_registry_update_allowed") is False
)
checks["runtime_activation_allowed_false"] = (
    summary.get("runtime_activation_allowed") is False
)
checks["production_activation_allowed_false"] = (
    summary.get("production_activation_allowed") is False
)
checks["candidate_only_true"] = summary.get("candidate_only") is True
checks["not_fact_true"] = summary.get("not_fact") is True
checks["boundary_status_frozen"] = summary.get("boundary_status") == "frozen"
checks["route_decision_matches"] = (
    summary.get("route_decision") == "OPTION_B_DEFERRED_RETURN_TO_MAINLINE"
)
checks["final_decision_matches"] = (
    summary.get("final_decision") == "OPTION_B_ROUTE_DECISION_CLOSURE_GO"
)
checks["recommended_next_phase_matches"] = (
    summary.get("recommended_next_phase") == "RETURN_TO_LUNA_MAINLINE_ROADMAP_DECISION"
)

for name in [
    "review_completed_true",
    "route_decision_completed_true",
    "reviewed_candidate_count_2",
    "passed_check_count_37",
    "failed_check_count_0",
    "blocker_count_0",
    "dependency_confirmed_count_0",
    "adapter_confirmed_count_0",
    "execution_admitted_candidate_count_0",
    "option_a_status_baseline",
    "option_b_status_deferred",
    "option_b_execution_allowed_false",
    "segmentation_execution_allowed_false",
    "active_model_selected_false",
    "active_skill_selected_false",
    "active_registry_update_allowed_false",
    "runtime_activation_allowed_false",
    "production_activation_allowed_false",
    "candidate_only_true",
    "not_fact_true",
    "boundary_status_frozen",
    "route_decision_matches",
    "final_decision_matches",
    "recommended_next_phase_matches",
]:
    if not checks[name]:
        failed_checks.append(name)

passed_count = sum(1 for value in checks.values() if value is True)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = "OPTION_B_ROUTE_DECISION_CLOSURE_GO"
route_decision = "OPTION_B_DEFERRED_RETURN_TO_MAINLINE"
if failed_count > 0:
    final_decision = "OPTION_B_ROUTE_DECISION_CLOSURE_BLOCKED"
    route_decision = "OPTION_B_DEFERRED_RETURN_TO_MAINLINE_BLOCKED"

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
print("ROUTE_DECISION")
print(route_decision)
print("NEXT")
print("RETURN_TO_LUNA_MAINLINE_ROADMAP_DECISION")

sys.exit(1 if failed_count > 0 else 0)
