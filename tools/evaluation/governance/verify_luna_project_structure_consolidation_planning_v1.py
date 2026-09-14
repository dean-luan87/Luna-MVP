#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Structure Consolidation Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Planning-v1-001"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "luna_project_structure_consolidation_planning_v1_smoke_v0"),
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
    policy = _load_json(root / "consolidation_planning_policy.json")
    merge_reg = _load_json(root / "merge_plan_register.json")
    archive_reg = _load_json(root / "archive_plan_register.json")
    split_reg = _load_json(root / "split_plan_register.json")
    keep_reg = _load_json(root / "keep_plan_register.json")
    defer_reg = _load_json(root / "defer_plan_register.json")
    batch_seq = _load_json(root / "consolidation_batch_sequence.json")
    dep_graph = _load_json(root / "consolidation_dependency_graph.json")
    life_matrix = _load_json(root / "life_system_consolidation_matrix.json")
    dev_plan = _load_json(root / "developer_backend_consolidation_plan.json")
    mp_plan = _load_json(root / "midplatform_consolidation_plan.json")
    cog_plan = _load_json(root / "cognition_placeholder_consolidation_plan.json")
    client_plan = _load_json(root / "client_boundary_consolidation_plan.json")
    risk = _load_json(root / "consolidation_risk_register.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    ok("input.structure_map_dryrun.loaded", idx.get("structure_map_dryrun", {}).get("loaded") is True)
    ok("input.project_structure_governance_planning.loaded", idx.get("project_structure_governance_planning", {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == "luna_project_structure_consolidation_planning_only")

    for k in (
        "structure_map_dryrun_input_loaded",
        "project_structure_governance_planning_input_loaded",
        "merge_plan_register_generated",
        "archive_plan_register_generated",
        "split_plan_register_generated",
        "keep_plan_register_generated",
        "defer_plan_register_generated",
        "consolidation_batch_sequence_generated",
        "consolidation_dependency_graph_generated",
        "life_system_consolidation_matrix_generated",
        "developer_backend_consolidation_plan_generated",
        "midplatform_consolidation_plan_generated",
        "cognition_placeholder_consolidation_plan_generated",
        "client_boundary_consolidation_plan_generated",
        "consolidation_risk_register_generated",
        "no_file_move_boundary_report_generated",
        "all_plan_rows_have_future_life_system_mapping",
        "future_life_system_mapping_required",
        "no_runtime_executed",
        "boundary_ok",
    ):
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    for k in ("actual_file_move_executed", "actual_module_merge_executed", "actual_consolidation_execution", "runtime_enabled"):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.inventory_entry_count>=50", summary.get("inventory_entry_count", 0) >= 50)
    ok("summary.consolidation_batch_count>=6", summary.get("consolidation_batch_count", 0) >= 6)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("policy.future_life_system_mapping_required", policy.get("future_life_system_mapping_required") is True)
    ok("policy.actual_consolidation_execution=false", policy.get("actual_consolidation_execution") is False)

    registers = {
        "merge": merge_reg,
        "archive": archive_reg,
        "split": split_reg,
        "keep": keep_reg,
        "defer": defer_reg,
    }
    total_rows = 0
    for name, reg in registers.items():
        ok(f"{name}.planned_action", reg.get("planned_action") == name)
        ok(f"{name}.row_count", reg.get("row_count") == len(reg.get("rows") or []))
        ok(f"{name}.all_rows_have_future_life_system_mapping", reg.get("all_rows_have_future_life_system_mapping") is True)
        ok(f"{name}.actual_move_executed=false", reg.get("actual_move_executed") is False)
        ok(f"{name}.execution_status", reg.get("execution_status") == "planning_only")
        total_rows += reg.get("row_count", 0)
        for i, row in enumerate((reg.get("rows") or [])[:40]):
            ok(f"{name}.row[{i}].future_life_system_mapping", bool(row.get("future_life_system_mapping")))
            ok(f"{name}.row[{i}].planned_action", row.get("planned_action") == name)
            ok(f"{name}.row[{i}].actual_move_executed=false", row.get("actual_move_executed") is False)
            ok(f"{name}.row[{i}].execution_status", row.get("execution_status") == "planning_only")
        for i, g in enumerate((reg.get("consolidation_groups") or [])[:20]):
            ok(f"{name}.group[{i}].future_life_system_mapping", bool(g.get("future_life_system_mapping")))
            ok(f"{name}.group[{i}].planned_action", g.get("planned_action") == name)

    ok("registers.total_row_count>=50", total_rows >= 50, total_rows)

    ok("batch_seq.batch_count>=6", batch_seq.get("batch_count", 0) >= 6)
    ok("batch_seq.actual_batch_execution=false", batch_seq.get("actual_batch_execution") is False)
    for i, b in enumerate(batch_seq.get("batches") or []):
        ok(f"batch[{i}].batch_id", bool(b.get("batch_id")))
        ok(f"batch[{i}].execution_status", b.get("execution_status") == "planning_only")

    ok("dep_graph.edge_count>=5", dep_graph.get("edge_count", 0) >= 5)

    ok("life_matrix.all_rows_have_future_life_system_mapping", life_matrix.get("all_rows_have_future_life_system_mapping") is True)
    for i, r in enumerate(life_matrix.get("life_system_rows") or []):
        ok(f"life_row[{i}].life_system_id", bool(r.get("life_system_id")))
        ok(f"life_row[{i}].future_life_system_mapping", r.get("future_life_system_mapping") == r.get("life_system_id"))

    for plan_name, plan in (
        ("dev", dev_plan),
        ("midplatform", mp_plan),
        ("cognition", cog_plan),
        ("client", client_plan),
    ):
        ok(f"{plan_name}.execution_status", plan.get("execution_status") == "planning_only")
        ok(f"{plan_name}.actual_move_executed=false", plan.get("actual_move_executed") is False)

    ok("risk.risk_count>=8", risk.get("risk_count", 0) >= 8)
    ok("risk.plan_rows_missing_life_system_mapping==0", risk.get("plan_rows_missing_life_system_mapping") == 0)

    for k in (
        "actual_file_move_executed",
        "actual_module_merge_executed",
        "actual_rename_executed",
        "actual_delete_executed",
        "runtime_enabled",
        "world_model_written",
        "memory_written",
    ):
        ok(f"no_move.{k}=false", no_move.get(k) is False)
    ok("no_move.boundary_ok", no_move.get("boundary_ok") is True)
    ok("no_move.planning_only", no_move.get("planning_only") is True)

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
