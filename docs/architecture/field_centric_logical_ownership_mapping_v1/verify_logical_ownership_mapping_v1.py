#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path("docs/architecture/field_centric_logical_ownership_mapping_v1")

REQUIRED_FILES = [
    "logical_ownership_mapping_plan_v1.md",
    "existing_module_logical_ownership_matrix_v1.json",
    "cognitive_layer_module_binding_v1.json",
    "governance_asset_reuse_decision_v1.json",
    "migration_wave_decision_v1.json",
    "minimum_vertical_slice_ownership_binding_v1.json",
    "logical_ownership_mapping_summary_v1.json",
]

checks = {}
failed_checks = []

# existence
for name in REQUIRED_FILES:
    checks[f"{name}_exists"] = (BASE / name).is_file()
    if not (BASE / name).is_file():
        failed_checks.append(f"{name}_exists")

# json validity
json_files = [
    BASE / "existing_module_logical_ownership_matrix_v1.json",
    BASE / "cognitive_layer_module_binding_v1.json",
    BASE / "governance_asset_reuse_decision_v1.json",
    BASE / "migration_wave_decision_v1.json",
    BASE / "minimum_vertical_slice_ownership_binding_v1.json",
    BASE / "logical_ownership_mapping_summary_v1.json",
]
for p in json_files:
    if p.is_file():
        try:
            json.loads(p.read_text(encoding="utf-8"))
            checks[f"{p.name}_json_valid"] = True
        except json.JSONDecodeError:
            checks[f"{p.name}_json_valid"] = False
            failed_checks.append(f"{p.name}_json_valid")

# coverage checks
module_matrix = json.loads(
    (BASE / "existing_module_logical_ownership_matrix_v1.json").read_text(
        encoding="utf-8"
    )
)
modules = module_matrix.get("modules", [])
required_module_names = [
    "Situation Understanding",
    "Observation Attention",
    "Region Intelligence",
    "Ownership Understanding",
    "Field-Centric Object Role",
    "Model Manager",
    "Model Test Lens",
    "Human Correction Layer",
    "Followup Runner",
    "Controlled Runner Execution",
    "OCR Evidence",
    "Vision Evidence",
    "Network-Assisted Situation Learning",
    "Document Surface Detector",
    "Option A baseline",
    "Option B deferred route",
    "Task Manager",
    "Protocol Governance",
    "Evidence Chain",
    "Runtime Boundary",
    "Model / Skill Admission",
    "Candidate / Fact Admission",
    "Change Control",
    "Permission / Owner Approval",
    "Diagnostics",
    "Post-Review / Freeze",
]
checks["module_matrix_covers_required_modules"] = all(
    any(m.get("module_name") == name for m in modules) for name in required_module_names
)
if not checks["module_matrix_covers_required_modules"]:
    failed_checks.append("module_matrix_covers_required_modules")

# layer bindings
bindings = json.loads(
    (BASE / "cognitive_layer_module_binding_v1.json").read_text(encoding="utf-8")
)
checks["layer_bindings_count_10"] = len(bindings.get("bindings", [])) == 10
if not checks["layer_bindings_count_10"]:
    failed_checks.append("layer_bindings_count_10")

# governance assets
governance = json.loads(
    (BASE / "governance_asset_reuse_decision_v1.json").read_text(encoding="utf-8")
)
checks["governance_assets_covered"] = len(governance.get("governance_assets", [])) >= 18
if not checks["governance_assets_covered"]:
    failed_checks.append("governance_assets_covered")

# rewrite_required defaults
checks["core_protocols_rewrite_false"] = all(
    not g.get("rewrite_required", False)
    for g in governance.get("governance_assets", [])
)
if not checks["core_protocols_rewrite_false"]:
    failed_checks.append("core_protocols_rewrite_false")

# waves
waves = json.loads(
    (BASE / "migration_wave_decision_v1.json").read_text(encoding="utf-8")
)
checks["wave_count_6"] = len(waves.get("waves", [])) == 6
checks["wave_1_selected_now"] = any(
    w.get("wave_id") == "Wave 1" and w.get("selected_now")
    for w in waves.get("waves", [])
)
checks["wave_3_to_5_blocked"] = all(
    any(
        w.get("wave_id") == wid and w.get("status", "").startswith("blocked")
        for w in waves.get("waves", [])
    )
    for wid in ["Wave 3", "Wave 4", "Wave 5"]
)
if not checks["wave_count_6"]:
    failed_checks.append("wave_count_6")
if not checks["wave_1_selected_now"]:
    failed_checks.append("wave_1_selected_now")
if not checks["wave_3_to_5_blocked"]:
    failed_checks.append("wave_3_to_5_blocked")

# physical move flags
checks["all_physical_move_allowed_false"] = all(
    not m.get("physical_move_allowed", True) for m in modules
)
if not checks["all_physical_move_allowed_false"]:
    failed_checks.append("all_physical_move_allowed_false")

# minimum slice order
slice_binding = json.loads(
    (BASE / "minimum_vertical_slice_ownership_binding_v1.json").read_text(
        encoding="utf-8"
    )
)
expected_order = [
    "field_candidate",
    "expectation_candidate",
    "attention_candidate",
    "region_evidence_candidate",
    "role_candidate",
    "interaction_decision_candidate",
    "feedback_candidate",
]
actual_order = [s.get("step_id") for s in slice_binding.get("slice_binding", [])]
checks["minimum_slice_order_matches"] = actual_order == expected_order
if not checks["minimum_slice_order_matches"]:
    failed_checks.append("minimum_slice_order_matches")

# summary checks
summary = json.loads(
    (BASE / "logical_ownership_mapping_summary_v1.json").read_text(encoding="utf-8")
)
checks["summary_flags_false"] = (
    summary.get("real_directory_migration_allowed") is False
    and summary.get("bulk_import_change_allowed") is False
    and summary.get("legacy_deletion_allowed") is False
    and summary.get("compatibility_adapter_execution_allowed") is False
    and summary.get("runtime_activation_allowed") is False
    and summary.get("production_activation_allowed") is False
)
if not checks["summary_flags_false"]:
    failed_checks.append("summary_flags_false")
checks["summary_candidate_only_true"] = summary.get("candidate_only") is True
checks["summary_not_fact_true"] = summary.get("not_fact") is True
checks["summary_blocker_count_zero"] = summary.get("blocker_count") == 0
checks["summary_final_decision_matches"] = (
    summary.get("final_decision") == "LUNA_FIELD_CENTRIC_LOGICAL_OWNERSHIP_MAPPING_GO"
)
checks["summary_next_phase_matches"] = (
    summary.get("recommended_next_phase")
    == "Phase-Luna-Field-Centric-Minimum-Vertical-Cognitive-Slice-Roadmap-Decision-v1-001"
)
for name in [
    "summary_candidate_only_true",
    "summary_not_fact_true",
    "summary_blocker_count_zero",
    "summary_final_decision_matches",
    "summary_next_phase_matches",
]:
    if not checks[name]:
        failed_checks.append(name)

passed_count = sum(1 for v in checks.values() if v)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = (
    "LUNA_FIELD_CENTRIC_LOGICAL_OWNERSHIP_MAPPING_GO"
    if failed_count == 0
    else "LUNA_FIELD_CENTRIC_LOGICAL_OWNERSHIP_MAPPING_BLOCKED"
)
selected_wave = "wave_1_logical_ownership_mapping"

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
print("SELECTED_WAVE")
print(selected_wave)
print("NEXT")
print(
    "Phase-Luna-Field-Centric-Minimum-Vertical-Cognitive-Slice-Roadmap-Decision-v1-001"
)

sys.exit(1 if failed_count > 0 else 0)
