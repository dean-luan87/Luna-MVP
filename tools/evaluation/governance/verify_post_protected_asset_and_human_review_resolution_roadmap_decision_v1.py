#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post Protected Asset and Human Review Resolution Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-Protected-Asset-and-Human-Review-Resolution-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_ROADMAP_DECISION_READY_FOR_MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001"
NEXT_PHASE_GUARDED = "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001"
SELECTED_ROUTE = "Main Project Structure Migration Readiness and Test Plan"
WHITEBOX_DEFER_REASON = "requires_post_migration_test_and_design_discussion"

MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160

EXPECTED_ROUTES = [
    ("A", SELECTED_ROUTE, "P0", True, NEXT_PHASE),
    ("K", "Main Project Structure Migration Guarded Planning", "P1", False, NEXT_PHASE_GUARDED),
    ("L", "Whitebox and Test Center Structure Optimization Planning", "deferred", False, "Phase-Whitebox-and-Test-Center-Structure-Optimization-Planning-v1-001"),
    ("B", "Developer Backend Extraction Planning", "deferred", False, "Phase-Developer-Backend-Extraction-Planning-v1-001"),
    ("C", "Docs Reorganization Planning", "P2", False, "Phase-Docs-Reorganization-Planning-v1-001"),
    ("D", "Human Review Execution Planning", "blocked", False, "Phase-Human-Review-Execution-Planning-v1-001"),
    ("E", "Protected Asset Manual Override Policy", "blocked", False, "Phase-Protected-Asset-Manual-Override-Policy-v1-001"),
    ("F", "Real Structure Migration Planning", "blocked", False, NEXT_PHASE_GUARDED),
    ("G", "Client / Developer Backend Boundary Hardening Planning", "P1", False, NEXT_PHASE),
    ("H", "MidPlatform Physical Modularization Planning", "deferred", False, "Phase-MidPlatform-Physical-Modularization-Planning-v1-001"),
    ("I", "WorldModel / Memory / Library / Emotion Placeholder Review", "discussion", False, "Phase-Future-Module-Discussion-v1-001"),
    ("J", "Return to Mainline Capability Development", "P2", False, "Phase-Return-to-Mainline-Capability-Development-v1-001"),
]

FUTURE_RESERVED_MODULES = ["WorldModel", "Memory Center", "Library", "Emotion Engine", "Exploration Drive"]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    status_summary = _load_json(root / "protected_asset_resolution_closure_status_summary.json")
    route_matrix = _load_json(root / "route_option_matrix.json")
    priority = _load_json(root / "priority_ranking.json")
    next_phase_dec = _load_json(root / "recommended_next_phase_decision.json")
    migration_route = _load_json(root / "main_project_migration_readiness_route_decision.json")
    deferred_whitebox = _load_json(root / "deferred_whitebox_test_center_structure_optimization_register.json")
    whitebox_route = _load_json(root / "whitebox_test_center_route_decision.json")
    deferred_backend = _load_json(root / "deferred_developer_backend_architecture_register.json")
    deferred_docs = _load_json(root / "deferred_docs_reorganization_register.json")
    deferred_hr = _load_json(root / "deferred_human_review_execution_register.json")
    deferred_migration = _load_json(root / "deferred_real_migration_register.json")
    future_reserved = _load_json(root / "future_reserved_module_discussion_register.json")
    boundary = _load_json(root / "boundary_freeze.json")
    non_claims = _load_json(root / "non_claims_register.json")
    debt = _load_json(root / "governance_debt_roadmap_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")

    ok("summary.decision_scope", summary.get("decision_scope") == "post_protected_asset_and_human_review_resolution_roadmap_decision_only")

    for field in (
        "protected_asset_resolution_closure_input_loaded",
        "protected_asset_resolution_post_review_input_loaded",
        "protected_asset_resolution_dryrun_input_loaded",
        "protected_asset_resolution_planning_input_loaded",
        "consolidation_roadmap_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_dryrun_input_loaded",
        "gate_taxonomy_input_loaded",
        "closure_status_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "main_project_migration_readiness_route_decision_generated",
        "whitebox_test_center_route_decision_generated",
        "deferred_whitebox_test_center_structure_optimization_register_generated",
        "deferred_developer_backend_architecture_register_generated",
        "deferred_docs_reorganization_register_generated",
        "deferred_human_review_execution_register_generated",
        "deferred_real_migration_register_generated",
        "future_reserved_module_discussion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "protected_asset_resolution_closed",
        "main_project_migration_readiness_selected",
        "whitebox_test_center_structure_optimization_deferred",
        "test_after_main_project_migration_required",
        "whitebox_test_center_must_align_with_main_project_structure",
        "developer_backend_architecture_deferred",
        "developer_backend_full_extraction_deferred",
        "developer_backend_overall_structure_deferred",
        "docs_reorganization_deferred",
        "human_review_execution_deferred",
        "protected_asset_manual_override_deferred",
        "real_structure_migration_blocked",
        "midplatform_physical_modularization_deferred",
        "return_to_mainline_deferred",
        "backend_overall_structure_deferred_by_user",
        "worldmodel_future_reserved",
        "memory_center_future_reserved",
        "library_future_reserved",
        "emotion_engine_future_reserved",
        "exploration_drive_future_reserved",
        "future_reserved_modules_discussion_required",
        "no_runtime_executed",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    ok("summary.whitebox_test_center_structure_optimization_selected=false", summary.get("whitebox_test_center_structure_optimization_selected") is False)
    ok("summary.only_whitebox_and_test_center_allowed_now=false", summary.get("only_whitebox_and_test_center_allowed_now") is False)
    ok("summary.whitebox_defer_reason", summary.get("whitebox_test_center_structure_optimization_defer_reason") == WHITEBOX_DEFER_REASON)

    ok("summary.route_option_count>=8", summary.get("route_option_count", 0) >= 8)
    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.human_review_case_count==240", summary.get("human_review_case_count") == 240)
    ok("summary.permanent_dnae_case_count==914", summary.get("permanent_dnae_case_count") == 914)
    ok("summary.permanent_dnae_preserved_count==914", summary.get("permanent_dnae_preserved_count") == 914)
    ok("summary.forced_future_module_finalization_allowed=false", summary.get("forced_future_module_finalization_allowed") is False)

    for field in (
        "real_migration_allowed",
        "ready_for_real_human_review_execution",
        "ready_for_protected_asset_modification",
        "ready_for_permanent_block_override",
        "ready_for_real_migration",
    ):
        ok(f"summary.{field}=false", summary.get(field) is False, summary.get(field))

    side_effect_false = (
        "actual_human_review_executed",
        "protected_assets_modified",
        "permanent_blocks_modified",
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
    ok("next.priority_note", bool(next_phase.get("priority_note")))
    ok("next.phase_sequence>=4", len(next_phase.get("recommended_phase_sequence") or []) >= 4)

    ok("status.closed", status_summary.get("protected_asset_resolution_closed") is True)
    ok("status.hr==240", status_summary.get("human_review_case_count") == 240)
    ok("status.permanent==914", status_summary.get("permanent_dnae_preserved_count") == 914)

    routes = {r.get("route_id"): r for r in route_matrix.get("routes") or []}
    ok("route_matrix.count>=10", route_matrix.get("route_option_count", 0) >= 10)
    ok("route_matrix.selected_route", route_matrix.get("selected_route") == SELECTED_ROUTE)
    for rid, name, priority_level, selected, phase in EXPECTED_ROUTES:
        r = routes.get(rid, {})
        ok(f"route.{rid}.name", r.get("route_name") == name)
        ok(f"route.{rid}.priority", r.get("recommended_priority") == priority_level)
        ok(f"route.{rid}.selected_now", r.get("selected_now") is selected)
        ok(f"route.{rid}.phase", r.get("recommended_phase_name") == phase)

    ok("route.L.defer_reason", routes.get("L", {}).get("defer_reason") == WHITEBOX_DEFER_REASON)

    ok("next_phase_dec.selected_route", next_phase_dec.get("selected_route") == SELECTED_ROUTE)
    ok("next_phase_dec.next_phase", next_phase_dec.get("recommended_next_phase") == NEXT_PHASE)

    ok("migration_route.selected", migration_route.get("selected_now") is True)
    ok("migration_route.planning_only", migration_route.get("planning_only") is True)
    ok("migration_route.test_after_migration", migration_route.get("test_after_main_project_migration_required") is True)
    ok("migration_route.next_phase", migration_route.get("recommended_next_phase") == NEXT_PHASE)
    ok("migration_route.guarded_after", migration_route.get("next_phase_after_readiness") == NEXT_PHASE_GUARDED)

    ok("deferred_whitebox.deferred", deferred_whitebox.get("deferred") is True)
    ok("deferred_whitebox.reason", deferred_whitebox.get("reason") == WHITEBOX_DEFER_REASON)
    ok("deferred_whitebox.test_required", deferred_whitebox.get("test_after_main_project_migration_required") is True)
    ok("deferred_whitebox.align", deferred_whitebox.get("whitebox_test_center_must_align_with_main_project_structure") is True)
    ok("whitebox_route.selected=false", whitebox_route.get("selected_now") is False)

    ok("deferred_backend.deferred", deferred_backend.get("deferred") is True)
    ok("deferred_backend.user_deferred", deferred_backend.get("backend_overall_structure_deferred_by_user") is True)
    ok("deferred_hr.deferred", deferred_hr.get("deferred") is True)
    ok("deferred_migration.ready=false", deferred_migration.get("ready_for_real_migration") is False)
    ok("deferred_migration.guarded_phase", deferred_migration.get("guarded_migration_phase") == NEXT_PHASE_GUARDED)

    ok("boundary.whitebox_deferred", boundary.get("whitebox-test-center-structure-optimization-deferred") is True)
    ok("boundary.test_after_migration", boundary.get("test-after-main-project-migration-required") is True)
    ok("boundary.align_main", boundary.get("whitebox-test-center-must-align-with-main-project") is True)
    ok("boundary.migration_readiness", boundary.get("main-project-migration-readiness-selected") is True)

    rankings = {r.get("route_id"): r for r in priority.get("rankings") or []}
    ok("priority.A.rank1", rankings.get("A", {}).get("rank") == 1)
    ok("priority.A.selected", rankings.get("A", {}).get("selected_now") is True)
    ok("priority.L.deferred", rankings.get("L", {}).get("selected_now") is False)

    ok("debt.primary_track", debt.get("primary_resolution_track") == SELECTED_ROUTE)
    ok("debt.count>=6", debt.get("debt_count", 0) >= 6)
    for i, item in enumerate(debt.get("debt_items") or []):
        ok(f"debt.item[{i}]", bool(item))

    ok("non_claims.count>=10", len(non_claims.get("non_claims") or []) >= 10)
    for i, claim in enumerate(non_claims.get("non_claims") or []):
        ok(f"non_claims[{i}]", bool(claim))

    for i, note in enumerate(next_phase_dec.get("selection_rationale") or []):
        ok(f"rationale[{i}]", bool(note))

    for i, risk in enumerate(deferred_whitebox.get("risk_if_premature") or []):
        ok(f"whitebox.risk[{i}]", bool(risk))

    ok("deferred_whitebox.observation_role", deferred_whitebox.get("whitebox_role") == "main_project_observation_system")
    ok("deferred_whitebox.verification_role", deferred_whitebox.get("test_center_role") == "main_project_verification_system")
    ok("deferred_docs.deferred", deferred_docs.get("deferred") is True)
    ok("summary.main_project_migration_guarded_deferred", summary.get("main_project_migration_guarded_planning_deferred_until_readiness") is True)

    for mod in FUTURE_RESERVED_MODULES:
        modules_by_name = {m.get("module_name"): m for m in future_reserved.get("modules") or []}
        m = modules_by_name.get(mod, {})
        ok(f"future.{mod}.reserved", m.get("future_reserved_module") is True)

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "protected_asset_resolution_closure",
        "protected_asset_resolution_post_review",
        "protected_asset_resolution_dryrun",
        "protected_asset_resolution_planning",
        "consolidation_roadmap",
        "consolidation_closure",
        "structure_map_dryrun",
        "gate_taxonomy_planning",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("no_move.decision_only", no_move.get("decision_only") is True)

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
