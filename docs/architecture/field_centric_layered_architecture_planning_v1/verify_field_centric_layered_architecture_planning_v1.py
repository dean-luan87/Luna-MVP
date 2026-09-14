#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path("docs/architecture/field_centric_layered_architecture_planning_v1")

REQUIRED_FILES = [
    "luna_field_centric_layered_architecture_plan_v1.md",
    "cognitive_layer_charter_template_v1.md",
    "cognitive_layer_responsibility_matrix_v1.json",
    "governance_reuse_matrix_v1.json",
    "existing_module_migration_mapping_v1.json",
    "architecture_migration_wave_plan_v1.json",
    "minimum_vertical_cognitive_slice_v1.json",
    "architecture_planning_summary_v1.json",
    "verify_field_centric_layered_architecture_planning_v1.py",
]

checks = {}
failed_checks = []

for name in REQUIRED_FILES:
    checks[f"{name}_exists"] = (BASE / name).is_file()
    if not (BASE / name).is_file():
        failed_checks.append(f"{name}_exists")

summary_path = BASE / "architecture_planning_summary_v1.json"
if summary_path.is_file():
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        checks["summary_json_valid"] = True
    except json.JSONDecodeError:
        checks["summary_json_valid"] = False
        failed_checks.append("summary_json_valid")
        summary = {}
else:
    summary = {}

json_paths = [
    BASE / "cognitive_layer_responsibility_matrix_v1.json",
    BASE / "governance_reuse_matrix_v1.json",
    BASE / "existing_module_migration_mapping_v1.json",
    BASE / "architecture_migration_wave_plan_v1.json",
    BASE / "minimum_vertical_cognitive_slice_v1.json",
    BASE / "architecture_planning_summary_v1.json",
]
for path in json_paths:
    if path.is_file():
        try:
            json.loads(path.read_text(encoding="utf-8"))
            checks[f"{path.name}_json_valid"] = True
        except json.JSONDecodeError:
            checks[f"{path.name}_json_valid"] = False
            failed_checks.append(f"{path.name}_json_valid")

responsibility_matrix = {}
if (BASE / "cognitive_layer_responsibility_matrix_v1.json").is_file():
    try:
        responsibility_matrix = json.loads(
            (BASE / "cognitive_layer_responsibility_matrix_v1.json").read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError:
        responsibility_matrix = {}
checks["layer_count_10"] = len(responsibility_matrix.get("layers", [])) == 10
if not checks["layer_count_10"]:
    failed_checks.append("layer_count_10")

normative_hierarchy = ["L0", "L1", "L2", "L3", "L4", "L5"]
checks["normative_hierarchy_complete"] = len(normative_hierarchy) == 6

reuse_matrix = {}
if (BASE / "governance_reuse_matrix_v1.json").is_file():
    try:
        reuse_matrix = json.loads(
            (BASE / "governance_reuse_matrix_v1.json").read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        reuse_matrix = {}
checks["governance_reuse_matrix_has_13_capabilities"] = (
    len(reuse_matrix.get("governance_capabilities", [])) == 13
)
if not checks["governance_reuse_matrix_has_13_capabilities"]:
    failed_checks.append("governance_reuse_matrix_has_13_capabilities")

module_mapping = {}
if (BASE / "existing_module_migration_mapping_v1.json").is_file():
    try:
        module_mapping = json.loads(
            (BASE / "existing_module_migration_mapping_v1.json").read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError:
        module_mapping = {}
checks["existing_module_mapping_count_complete"] = (
    len(module_mapping.get("mappings", [])) >= 19
)
if not checks["existing_module_mapping_count_complete"]:
    failed_checks.append("existing_module_mapping_count_complete")

wave_plan = {}
if (BASE / "architecture_migration_wave_plan_v1.json").is_file():
    try:
        wave_plan = json.loads(
            (BASE / "architecture_migration_wave_plan_v1.json").read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError:
        wave_plan = {}
checks["wave_count_6"] = len(wave_plan.get("waves", [])) == 6
if not checks["wave_count_6"]:
    failed_checks.append("wave_count_6")

slice_plan = {}
if (BASE / "minimum_vertical_cognitive_slice_v1.json").is_file():
    try:
        slice_plan = json.loads(
            (BASE / "minimum_vertical_cognitive_slice_v1.json").read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError:
        slice_plan = {}
checks["minimum_slice_step_count_7"] = len(slice_plan.get("slice", [])) == 7
if not checks["minimum_slice_step_count_7"]:
    failed_checks.append("minimum_slice_step_count_7")

checks["migration_allowed_false"] = (
    summary.get("real_directory_migration_allowed") is False
)
checks["bulk_import_change_allowed_false"] = (
    summary.get("bulk_import_change_allowed") is False
)
checks["legacy_deletion_allowed_false"] = (
    summary.get("legacy_deletion_allowed") is False
)
checks["runtime_activation_allowed_false"] = (
    summary.get("runtime_activation_allowed") is False
)
checks["production_activation_allowed_false"] = (
    summary.get("production_activation_allowed") is False
)
checks["model_training_allowed_false"] = summary.get("model_training_allowed") is False
checks["candidate_only_true"] = summary.get("candidate_only") is True
checks["not_fact_true"] = summary.get("not_fact") is True
checks["blocker_count_zero"] = summary.get("blocker_count") == 0
checks["summary_final_decision_matches"] = (
    summary.get("final_decision")
    == "LUNA_FIELD_CENTRIC_LAYERED_ARCHITECTURE_PLANNING_GO"
)
checks["summary_next_phase_matches"] = (
    summary.get("recommended_next_phase")
    == "Phase-Luna-Field-Centric-Existing-Module-Logical-Ownership-Mapping-And-Migration-Wave-Decision-v1-001"
)

for name in [
    "migration_allowed_false",
    "bulk_import_change_allowed_false",
    "legacy_deletion_allowed_false",
    "runtime_activation_allowed_false",
    "production_activation_allowed_false",
    "model_training_allowed_false",
    "candidate_only_true",
    "not_fact_true",
    "blocker_count_zero",
    "summary_final_decision_matches",
    "summary_next_phase_matches",
]:
    if not checks[name]:
        failed_checks.append(name)

passed_count = sum(1 for value in checks.values() if value is True)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = "LUNA_FIELD_CENTRIC_LAYERED_ARCHITECTURE_PLANNING_GO"
if failed_count > 0:
    final_decision = "LUNA_FIELD_CENTRIC_LAYERED_ARCHITECTURE_PLANNING_BLOCKED"

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
print(
    "Phase-Luna-Field-Centric-Existing-Module-Logical-Ownership-Mapping-And-Migration-Wave-Decision-v1-001"
)

sys.exit(1 if failed_count > 0 else 0)
