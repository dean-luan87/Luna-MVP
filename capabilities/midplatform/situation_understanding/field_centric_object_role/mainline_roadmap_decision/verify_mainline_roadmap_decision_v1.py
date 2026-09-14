#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path(
    "capabilities/midplatform/situation_understanding/"
    "field_centric_object_role/mainline_roadmap_decision"
)

MARKDOWN_PATH = BASE / "mainline_roadmap_decision_v1.md"
SUMMARY_PATH = BASE / "mainline_roadmap_decision_summary_v1.json"

checks = {}
failed_checks = []

for path in [MARKDOWN_PATH, SUMMARY_PATH]:
    checks[f"{path.name}_exists"] = path.is_file()
    if not path.is_file():
        failed_checks.append(f"{path.name}_exists")

if checks.get("mainline_roadmap_decision_v1.md_exists", False) and checks.get(
    "mainline_roadmap_decision_summary_v1.json_exists", False
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

checks["decision_completed_true"] = summary.get("decision_completed") is True
checks["closed_route_status_deferred"] = (
    summary.get("closed_route_status") == "deferred_candidate_route"
)
checks["selected_route_field_centric_object_role_dryrun"] = (
    summary.get("selected_route") == "field_centric_object_role_dryrun"
)
checks["selected_route_priority_p0"] = summary.get("selected_route_priority") == "P0"
checks["field_first_alignment_true"] = summary.get("field_first_alignment") is True
checks["minimum_sufficient_representation_alignment_true"] = (
    summary.get("minimum_sufficient_representation_alignment") is True
)
checks["predictive_field_cognition_alignment_true"] = (
    summary.get("predictive_field_cognition_alignment") is True
)
checks["option_b_execution_allowed_false"] = (
    summary.get("option_b_execution_allowed") is False
)
checks["runtime_activation_allowed_false"] = (
    summary.get("runtime_activation_allowed") is False
)
checks["production_activation_allowed_false"] = (
    summary.get("production_activation_allowed") is False
)
checks["blocker_count_zero"] = summary.get("blocker_count") == 0
checks["final_decision_matches"] = (
    summary.get("final_decision")
    == "LUNA_MAINLINE_ROADMAP_DECISION_FIELD_CENTRIC_OBJECT_ROLE_DRYRUN_GO"
)
checks["recommended_next_phase_matches"] = (
    summary.get("recommended_next_phase")
    == "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
)

for name in [
    "decision_completed_true",
    "closed_route_status_deferred",
    "selected_route_field_centric_object_role_dryrun",
    "selected_route_priority_p0",
    "field_first_alignment_true",
    "minimum_sufficient_representation_alignment_true",
    "predictive_field_cognition_alignment_true",
    "option_b_execution_allowed_false",
    "runtime_activation_allowed_false",
    "production_activation_allowed_false",
    "blocker_count_zero",
    "final_decision_matches",
    "recommended_next_phase_matches",
]:
    if not checks[name]:
        failed_checks.append(name)

passed_count = sum(1 for value in checks.values() if value is True)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = "LUNA_MAINLINE_ROADMAP_DECISION_FIELD_CENTRIC_OBJECT_ROLE_DRYRUN_GO"
selected_route = "field_centric_object_role_dryrun"
if failed_count > 0:
    final_decision = (
        "LUNA_MAINLINE_ROADMAP_DECISION_FIELD_CENTRIC_OBJECT_ROLE_DRYRUN_BLOCKED"
    )
    selected_route = "field_centric_object_role_dryrun_blocked"

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
print("SELECTED_ROUTE")
print(selected_route)
print("NEXT")
print(
    "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
)

sys.exit(1 if failed_count > 0 else 0)
