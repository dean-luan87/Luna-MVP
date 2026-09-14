#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Module Inventory and Structure Map DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001"
FINAL_DECISION = "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-Planning-v1-001"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220

REQUIRED_LIFE_SYSTEMS = (
    "PerceptionLayer",
    "InteractionLayer",
    "ActionLayer",
    "ContextLayer",
    "CognitionLayer",
    "GovernanceLayer",
    "MidPlatformOrganLayer",
    "CapabilityOrganLayer",
    "DeveloperBackendLayer",
    "ClientSurfaceLayer",
    "HardwareInfrastructureLayer",
    "LifeSystemLayer",
    "ResilienceLayer",
    "UnclassifiedLegacyLayer",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    module_inventory = _load_json(root / "module_inventory.json")
    current_to_target = _load_json(root / "current_to_target_structure_map.json")
    life_matrix = _load_json(root / "life_system_mapping_matrix.json")
    dev_backend = _load_json(root / "developer_backend_extraction_map.json")
    midplatform = _load_json(root / "midplatform_subsystem_mapping.json")
    future_placeholder = _load_json(root / "future_module_placeholder_mapping.json")
    client_boundary = _load_json(root / "client_boundary_mapping.json")
    migration_risk = _load_json(root / "migration_risk_register.json")
    no_file_move = _load_json(root / "no_file_move_boundary_report.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    _load_json(root / "architecture_doc_inventory.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    ok("input.project_structure_governance_planning.loaded", idx.get("project_structure_governance_planning", {}).get("loaded") is True)
    ok("input.gate_taxonomy_planning.loaded", idx.get("gate_taxonomy_planning", {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID, summary.get("phase"))
    ok(
        "summary.dryrun_scope",
        summary.get("dryrun_scope") == "luna_project_module_inventory_and_structure_map_dryrun_only",
    )

    required_true = (
        "project_structure_governance_planning_input_loaded",
        "module_inventory_generated",
        "current_to_target_structure_map_generated",
        "life_system_mapping_matrix_generated",
        "developer_backend_extraction_map_generated",
        "midplatform_subsystem_mapping_generated",
        "future_module_placeholder_mapping_generated",
        "client_boundary_mapping_generated",
        "migration_risk_register_generated",
        "no_file_move_boundary_report_generated",
        "all_entries_have_future_life_system_mapping",
        "no_runtime_executed",
        "boundary_ok",
    )
    for k in required_true:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    required_false = (
        "actual_file_move_executed",
        "actual_module_merge_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
    )
    for k in required_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.inventory_entry_count>=50", summary.get("inventory_entry_count", 0) >= 50, summary.get("inventory_entry_count"))
    ok("summary.life_system_layer_count>=10", summary.get("life_system_layer_count", 0) >= 10)
    ok("summary.assets_missing_life_system_mapping==0", summary.get("assets_missing_life_system_mapping") == 0)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION, summary.get("final_decision"))
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE, summary.get("recommended_next_phase"))

    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    entries = module_inventory.get("inventory_entries") or []
    ok("module_inventory.entry_count", module_inventory.get("entry_count") == len(entries))
    ok("module_inventory.all_entries_have_future_life_system_mapping", module_inventory.get("all_entries_have_future_life_system_mapping") is True)

    required_entry_fields = (
        "current_path",
        "current_module",
        "asset_type",
        "current_engineering_domain",
        "future_target_module",
        "future_life_system_mapping",
        "is_client",
        "is_developer_backend",
        "is_midplatform_organ",
        "is_capability_organ",
        "is_cognition_placeholder",
        "versioning_required",
        "disposition_action",
    )
    for i, e in enumerate(entries[:100]):
        for f in required_entry_fields:
            ok(f"inventory[{i}].{f}.present", f in e and e.get(f) is not None, e.get(f))
        ok(f"inventory[{i}].future_life_system_mapping.nonempty", bool(e.get("future_life_system_mapping")))
        ok(f"inventory[{i}].actual_move_executed=false", e.get("actual_move_executed") is False)
        ok(f"inventory[{i}].fact_status=not_fact", e.get("fact_status") == "not_fact")

    map_rows = current_to_target.get("map_rows") or []
    ok("current_to_target.row_count", current_to_target.get("row_count") == len(map_rows))
    ok("current_to_target.all_rows_have_future_life_system_mapping", current_to_target.get("all_rows_have_future_life_system_mapping") is True)
    for i, r in enumerate(map_rows[:80]):
        ok(f"map_row[{i}].future_life_system_mapping", bool(r.get("future_life_system_mapping")))
        ok(f"map_row[{i}].disposition_action", r.get("disposition_action") in {"keep", "merge", "archive", "split", "defer"})

    life_rows = life_matrix.get("life_systems") or []
    ok("life_matrix.life_system_count", life_matrix.get("life_system_count") == len(life_rows))
    for ls in REQUIRED_LIFE_SYSTEMS:
        ok(f"life_matrix.has.{ls}", any(r.get("life_system_id") == ls for r in life_rows))
    for i, r in enumerate(life_rows):
        ok(f"life_system[{i}].life_system_id", bool(r.get("life_system_id")))
        ok(f"life_system[{i}].asset_count>=0", isinstance(r.get("asset_count"), int) and r.get("asset_count") >= 0)

    ok("dev_backend.production_client_excludes_developer_backend", dev_backend.get("production_client_excludes_developer_backend") is True)
    ok("dev_backend.rows", isinstance(dev_backend.get("developer_backend_extraction_rows"), list))

    ok("midplatform.subsystem_mapping_count>=8", midplatform.get("subsystem_mapping_count", 0) >= 8)
    for i, r in enumerate((midplatform.get("subsystem_mappings") or [])[:20]):
        ok(f"midplatform[{i}].future_life_system_mapping", r.get("future_life_system_mapping") == "MidPlatformOrganLayer")

    ok("future_placeholder.placeholder_mapping_count>=8", future_placeholder.get("placeholder_mapping_count", 0) >= 8)
    for i, r in enumerate((future_placeholder.get("placeholder_mappings") or [])[:20]):
        ok(f"future[{i}].future_life_system_mapping", bool(r.get("future_life_system_mapping")))

    ok("client_boundary.production_client_excludes_developer_backend", client_boundary.get("production_client_excludes_developer_backend") is True)
    ok("client_boundary.row_count>=1", client_boundary.get("row_count", 0) >= 1)

    ok("migration_risk.risk_count>=8", migration_risk.get("risk_count", 0) >= 8)
    ok("migration_risk.assets_missing_life_system_mapping==0", migration_risk.get("assets_missing_life_system_mapping") == 0)

    for k in (
        "actual_file_move_executed",
        "actual_module_merge_executed",
        "actual_rename_executed",
        "actual_delete_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"no_file_move.{k}=false", no_file_move.get(k) is False)
    ok("no_file_move.boundary_ok", no_file_move.get("boundary_ok") is True)
    ok("no_file_move.dryrun_only", no_file_move.get("dryrun_only") is True)

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
