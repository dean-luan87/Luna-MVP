#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Structure Consolidation Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001"
SELECTED_ROUTE = "Protected Asset and Human Review Resolution Planning"

MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160

EXPECTED_ROUTES = [
    ("A", "Protected Asset and Human Review Resolution Planning", "P0", True, NEXT_PHASE),
    ("B", "Developer Backend Extraction Planning", "P1", False, "Phase-Developer-Backend-Extraction-Planning-v1-001"),
    ("C", "Docs Reorganization Planning", "P2", False, "Phase-Docs-Reorganization-Planning-v1-001"),
    ("D", "MidPlatform Physical Modularization Planning", "P2", False, "Phase-MidPlatform-Physical-Modularization-Planning-v1-001"),
    ("E", "Client / Developer Backend Boundary Hardening Planning", "P1", False, "Phase-Client-Developer-Backend-Boundary-Hardening-Planning-v1-001"),
    ("F", "Human Review Execution Trial", "P3", False, "Phase-Human-Review-Execution-Trial-v1-001"),
    ("G", "Real Structure Migration Guarded Planning", "blocked", False, "Phase-Real-Structure-Migration-Guarded-Planning-v1-001"),
    ("H", "Legacy Archive Planning", "P3", False, "Phase-Legacy-Archive-Planning-v1-001"),
    ("I", "Return to Mainline Capability Development", "P2", False, "Phase-Return-to-Mainline-Capability-Development-v1-001"),
    ("J", "Protected Asset Policy", "P0", False, NEXT_PHASE),
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "luna_project_structure_consolidation_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    status_summary = _load_json(root / "consolidation_closure_status_summary.json")
    route_matrix = _load_json(root / "route_option_matrix.json")
    priority = _load_json(root / "priority_ranking.json")
    next_phase_dec = _load_json(root / "recommended_next_phase_decision.json")
    route_a = _load_json(root / "protected_asset_and_human_review_route_decision.json")
    deferred_migration = _load_json(root / "deferred_real_migration_register.json")
    deferred_backend = _load_json(root / "deferred_developer_backend_extraction_register.json")
    deferred_docs = _load_json(root / "deferred_docs_reorganization_register.json")
    deferred_mp = _load_json(root / "deferred_midplatform_modularization_register.json")
    deferred_mainline = _load_json(root / "deferred_mainline_return_register.json")
    boundary = _load_json(root / "boundary_freeze.json")
    non_claims = _load_json(root / "non_claims_register.json")
    debt = _load_json(root / "governance_debt_roadmap_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")

    ok("summary.decision_scope", summary.get("decision_scope") == "luna_project_structure_consolidation_roadmap_decision_only")

    for field in (
        "consolidation_closure_input_loaded",
        "consolidation_post_review_input_loaded",
        "consolidation_dryrun_input_loaded",
        "consolidation_planning_input_loaded",
        "structure_map_dryrun_input_loaded",
        "project_structure_governance_planning_input_loaded",
        "gate_taxonomy_input_loaded",
        "closure_status_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "protected_asset_and_human_review_route_decision_generated",
        "deferred_real_migration_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "consolidation_closed",
        "protected_asset_policy_required",
        "human_review_resolution_required",
        "permanent_block_resolution_required",
        "developer_backend_extraction_deferred",
        "docs_reorganization_deferred",
        "midplatform_physical_modularization_deferred",
        "real_structure_migration_deferred",
        "return_to_mainline_deferred",
        "no_runtime_executed",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    ok("summary.route_option_count>=8", summary.get("route_option_count", 0) >= 8)
    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.plan_revision_required==0", summary.get("plan_revision_required") == 0)
    ok("summary.human_review_required==240", summary.get("human_review_required") == 240)
    ok("summary.permanent_do_not_auto_execute==914", summary.get("permanent_do_not_auto_execute") == 914)

    for field in (
        "real_migration_allowed",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
    ):
        ok(f"summary.{field}=false", summary.get(field) is False, summary.get(field))

    side_effect_false = (
        "actual_consolidation_execution",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_decision",
        "readme_modified_by_decision",
        "phase_verdict_table_modified_by_decision",
        "existing_phase_result_changed",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
        "exists_invoked",
        "file_opened",
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "navigation_action_triggered",
        "speech_gate_invoked",
        "tts_invoked",
    )
    for k in side_effect_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("status.consolidation_closed", status_summary.get("consolidation_closed") is True)
    ok("status.human==240", status_summary.get("human_review_required") == 240)
    ok("status.permanent==914", status_summary.get("permanent_do_not_auto_execute") == 914)
    ok("status.real_migration=false", status_summary.get("real_migration_allowed") is False)

    routes = {r.get("route_id"): r for r in route_matrix.get("routes") or []}
    ok("route_matrix.count>=10", route_matrix.get("route_option_count", 0) >= 10)
    ok("route_matrix.selected_route", route_matrix.get("selected_route") == SELECTED_ROUTE)
    for rid, name, priority_level, selected, phase in EXPECTED_ROUTES:
        r = routes.get(rid, {})
        ok(f"route.{rid}.name", r.get("route_name") == name)
        ok(f"route.{rid}.priority", r.get("recommended_priority") == priority_level)
        ok(f"route.{rid}.selected_now", r.get("selected_now") is selected)
        ok(f"route.{rid}.phase", r.get("recommended_phase_name") == phase)

    ok("next_phase_dec.selected_route", next_phase_dec.get("selected_route") == SELECTED_ROUTE)
    ok("next_phase_dec.next_phase", next_phase_dec.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase_dec.real_migration_deferred", next_phase_dec.get("real_migration_deferred") is True)
    for i, note in enumerate(next_phase_dec.get("selection_rationale") or []):
        ok(f"next_phase_dec.rationale[{i}]", bool(note))

    ok("route_a.selected_now", route_a.get("selected_now") is True)
    ok("route_a.planning_only", route_a.get("planning_only") is True)
    ok("route_a.auto_execute=false", route_a.get("auto_execute_allowed") is False)
    ok("route_a.human_count==240", route_a.get("human_review_count") == 240)
    ok("route_a.permanent_count==914", route_a.get("permanent_block_count") == 914)
    ok("route_a.next_phase", route_a.get("recommended_next_phase") == NEXT_PHASE)

    ok("deferred_migration.deferred", deferred_migration.get("deferred") is True)
    ok("deferred_migration.ready_for_real_migration=false", deferred_migration.get("ready_for_real_migration") is False)
    ok("deferred_backend.deferred", deferred_backend.get("deferred") is True)
    ok("deferred_docs.deferred", deferred_docs.get("deferred") is True)
    ok("deferred_mp.deferred", deferred_mp.get("deferred") is True)
    ok("deferred_mainline.deferred", deferred_mainline.get("deferred") is True)

    ok("boundary.no-real-migration", boundary.get("no-real-migration") is True)
    ok("boundary.no-human-review-execution", boundary.get("no-human-review-execution") is True)
    ok("boundary.no-protected-asset-handling", boundary.get("no-protected-asset-handling") is True)
    ok("boundary.roadmap-decision-only", boundary.get("roadmap-decision-only") is True)

    ok("non_claims.count>=8", len(non_claims.get("non_claims") or []) >= 8)
    for i, claim in enumerate((non_claims.get("non_claims") or [])[:8]):
        ok(f"non_claims[{i}]", bool(claim))

    ok("debt.count>=9", debt.get("debt_count", 0) >= 9)
    ok("debt.primary_track", debt.get("primary_resolution_track") == SELECTED_ROUTE)
    for i, item in enumerate(debt.get("debt_items") or []):
        ok(f"debt[{i}]", bool(item))

    rankings = priority.get("rankings") or []
    ok("priority.rank1_is_A", rankings[0].get("route_id") == "A" if rankings else False)
    ok("priority.rank1_selected", rankings[0].get("selected_now") is True if rankings else False)
    for i, rank in enumerate(rankings):
        ok(f"priority[{i}].route_id", bool(rank.get("route_id")))
        ok(f"priority[{i}].rank", rank.get("rank") == i + 1)

    for report, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
    ):
        ok(f"{name}.decision_only", report.get("decision_only") is True)
        ok(f"{name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{name}.violations.empty", report.get("violations") == [])
        ok(f"{name}.no_runtime_executed", report.get("no_runtime_executed") is True)

    for i, row in enumerate(input_root_matrix.get("rows", [])):
        ok(f"input_row[{i}].loaded", row.get("loaded") is True)
        ok(f"input_row[{i}].fact_status", row.get("fact_status") == "not_fact")

    ok("summary.source_chain", summary.get("source_chain") == "luna_project_structure_consolidation_roadmap_decision_v1")
    ok("route_a.fact_status", route_a.get("fact_status") == "not_fact")

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "verifier": "GO" if passed else "NO_GO",
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "verifier": report["verifier"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
