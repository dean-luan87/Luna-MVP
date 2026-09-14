#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Protected Asset and Human Review Resolution Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-Closure-v1-001"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Protected-Asset-and-Human-Review-Resolution-Roadmap-Decision-v1-001"

MIN_CHECKS = 240
BASELINE_REQUIREMENT = 200


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "protected_asset_and_human_review_resolution_closure_v1_smoke_v0"),
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
    closure_summary = _load_json(root / "protected_asset_human_review_resolution_closure_summary.json")
    completed = _load_json(root / "completed_phase_matrix.json")
    decision_summary = _load_json(root / "resolution_closure_decision_summary.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "resolution_non_claims_register.json")
    human_carry = _load_json(root / "human_review_carryover_for_future_execution.json")
    permanent_carry = _load_json(root / "permanent_block_carryover_for_future_governance.json")
    deferred_pool = _load_json(root / "deferred_resolution_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "post_review",
        "resolution_dryrun",
        "planning",
        "roadmap_decision",
        "consolidation_closure",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == "protected_asset_and_human_review_resolution_closure_only")

    for field in (
        "post_review_input_loaded",
        "dryrun_input_loaded",
        "planning_input_loaded",
        "consolidation_roadmap_input_loaded",
        "consolidation_closure_input_loaded",
        "completed_phase_matrix_generated",
        "resolution_closure_decision_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "human_review_carryover_generated",
        "permanent_block_carryover_generated",
        "deferred_resolution_action_pool_generated",
        "closure_readiness_gate_generated",
        "protected_asset_resolution_planning_closed",
        "protected_asset_resolution_dryrun_closed",
        "protected_asset_resolution_post_review_closed",
        "protected_asset_resolution_closed",
        "closure_allowed",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3)
    ok("summary.human_review_case_count==240", summary.get("human_review_case_count") == 240)
    ok("summary.human_review_closed_no_execution_count==240", summary.get("human_review_closed_no_execution_count") == 240)
    ok("summary.permanent_dnae_case_count==914", summary.get("permanent_dnae_case_count") == 914)
    ok("summary.permanent_dnae_preserved_count==914", summary.get("permanent_dnae_preserved_count") == 914)
    ok("summary.protected_conflict_count==448", summary.get("protected_conflict_count") == 448)
    ok("summary.static_dnae_rule_count==466", summary.get("static_dnae_rule_count") == 466)
    ok("summary.high_risk_merge_case_count==5", summary.get("high_risk_merge_case_count") == 5)
    ok("summary.future_placeholder_current_code_case_count==35", summary.get("future_placeholder_current_code_case_count") == 35)
    ok("summary.target_module_unclear_case_count==200", summary.get("target_module_unclear_case_count") == 200)
    ok("summary.forbidden_decision_blocked_count==10", summary.get("forbidden_decision_blocked_count") == 10)
    ok("summary.forbidden_state_absent_count==5", summary.get("forbidden_state_absent_count") == 5)
    ok("summary.audit_trace_generated_count==1154", summary.get("audit_trace_generated_count") == 1154)
    ok("summary.rollback_ref_generated_count==1154", summary.get("rollback_ref_generated_count") == 1154)

    for field in (
        "actual_human_review_executed",
        "human_review_execution_allowed",
        "final_owner_human_confirmed",
        "protected_assets_modified",
        "permanent_blocks_modified",
        "permanent_block_override_allowed",
        "override_executed",
        "block_released",
        "audit_committed",
        "rollback_executed",
        "real_migration_allowed",
        "ready_for_real_human_review_execution",
        "ready_for_protected_asset_modification",
        "ready_for_permanent_block_override",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_closure",
        "readme_modified_by_closure",
        "phase_verdict_table_modified_by_closure",
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
    ):
        ok(f"summary.{field}=false", summary.get(field) is False, summary.get(field))

    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.source_chain", summary.get("source_chain") == "protected_asset_and_human_review_resolution_closure_v1")

    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.roadmap_options>=6", len(next_phase.get("roadmap_decision_options") or []) >= 6)
    ok("next.priority_note", bool(next_phase.get("priority_note")))

    ok("closure_summary.closure_id", bool(closure_summary.get("closure_id")))
    ok("closure_summary.completed_phase_count>=3", closure_summary.get("completed_phase_count", 0) >= 3)
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    ok("closure_summary.planning_ref", bool(closure_summary.get("planning_ref")))
    ok("closure_summary.dryrun_ref", bool(closure_summary.get("dryrun_ref")))
    ok("closure_summary.post_review_ref", bool(closure_summary.get("post_review_ref")))

    phases = completed.get("phases") or []
    ok("completed.phase_count==3", len(phases) == 3)
    for i, p in enumerate(phases):
        ok(f"completed[{i}].status", p.get("status") == "GO")
        ok(f"completed[{i}].actual_hr=false", p.get("actual_human_review_executed") is False)
        ok(f"completed[{i}].assets_modified=false", p.get("protected_assets_modified") is False)
        ok(f"completed[{i}].blocks_modified=false", p.get("permanent_blocks_modified") is False)
        ok(f"completed[{i}].runtime=false", p.get("runtime_enabled") is False)
        ok(f"completed[{i}].verifier", p.get("verifier_verdict") == "GO")
        ok(f"completed[{i}].phase_id", bool(p.get("phase_id")))
        ok(f"completed[{i}].role", bool(p.get("role_in_closure")))

    ok("decision.hr==240", decision_summary.get("human_review_case_count") == 240)
    ok("decision.closed==240", decision_summary.get("human_review_closed_no_execution_count") == 240)
    ok("decision.dnae==914", decision_summary.get("permanent_dnae_case_count") == 914)
    ok("decision.preserved==914", decision_summary.get("permanent_dnae_preserved_count") == 914)
    ok("decision.protected==448", decision_summary.get("protected_conflict_count") == 448)
    ok("decision.static==466", decision_summary.get("static_dnae_rule_count") == 466)
    ok("decision.forbidden_dec==10", decision_summary.get("forbidden_decision_blocked_count") == 10)
    ok("decision.forbidden_state==5", decision_summary.get("forbidden_state_absent_count") == 5)
    ok("decision.audit==1154", decision_summary.get("audit_trace_generated_count") == 1154)
    ok("decision.rollback==1154", decision_summary.get("rollback_ref_generated_count") == 1154)
    ok("decision.closure_allowed", decision_summary.get("closure_allowed") is True)
    ok("decision.real_migration=false", decision_summary.get("real_migration_allowed") is False)
    ok("decision.actual_hr=false", decision_summary.get("actual_human_review_executed") is False)
    ok("decision.block_released=false", decision_summary.get("block_released") is False)
    ok("decision.audit_committed=false", decision_summary.get("audit_committed") is False)
    ok("decision.rollback_executed=false", decision_summary.get("rollback_executed") is False)

    boundary_keys = (
        "no-real-human-review-execution",
        "no-real-owner-confirmation",
        "no-protected-asset-modification",
        "no-permanent-block-release",
        "no-manual-override-execution",
        "no-audit-commit",
        "no-rollback-execution",
        "no-real-migration",
        "no-file-move",
        "no-file-delete",
        "no-file-rename",
        "no-module-merge",
        "no-auto-archive",
        "no-runtime",
        "no-write",
        "no-action",
        "no-speech",
    )
    for k in boundary_keys:
        ok(f"boundary_freeze.{k}", boundary_freeze.get(k) is True)

    ok("non_claims.count>=12", len(non_claims.get("non_claims") or []) >= 12)
    for i, claim in enumerate(non_claims.get("non_claims") or []):
        ok(f"non_claims[{i}]", bool(claim))

    ok("human_carry.count==240", human_carry.get("human_review_required_count") == 240)
    ok("human_carry.closed==240", human_carry.get("closed_no_execution_count") == 240)
    ok("human_carry.owner_confirmed=false", human_carry.get("final_owner_human_confirmed") is False)
    ok("human_carry.high_risk==5", human_carry.get("categories", {}).get("high_risk_merge") == 5)
    ok("human_carry.future==35", human_carry.get("categories", {}).get("future_placeholder_current_code") == 35)
    ok("human_carry.target==200", human_carry.get("categories", {}).get("target_module_unclear") == 200)
    ok("human_carry.future_requires>=6", len(human_carry.get("future_execution_requires") or []) >= 6)

    ok("permanent_carry.count==914", permanent_carry.get("permanent_dnae_count") == 914)
    ok("permanent_carry.protected==448", permanent_carry.get("protected_conflict_count") == 448)
    ok("permanent_carry.static==466", permanent_carry.get("static_dnae_rule_count") == 466)
    ok("permanent_carry.block_released=false", permanent_carry.get("block_released") is False)
    ok("permanent_carry.override=false", permanent_carry.get("override_executed") is False)
    ok("permanent_carry.future_requires>=6", len(permanent_carry.get("future_override_requires") or []) >= 6)

    ok("deferred.count>=16", deferred_pool.get("deferred_action_count", 0) >= 16)
    ok("deferred.real_migration_started=false", deferred_pool.get("real_migration_started") is False)
    for i, item in enumerate((deferred_pool.get("deferred_actions") or [])[:20]):
        ok(f"deferred[{i}].auto_execute=false", item.get("auto_execute_allowed") is False)
        ok(f"deferred[{i}].requires_roadmap", item.get("requires_roadmap_decision") is True)

    ok("readiness.ready_for_closure", readiness_gate.get("ready_for_closure") is True)
    ok("readiness.blockers.empty", readiness_gate.get("blockers") == [])
    ok("readiness.go_conditions>=10", len(readiness_gate.get("go_conditions") or []) >= 10)

    for report, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
    ):
        ok(f"{name}.closure_only", report.get("closure_only") is True)
        ok(f"{name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{name}.violations.empty", report.get("violations") == [])
        ok(f"{name}.actual_hr=false", report.get("actual_human_review_executed") is False)
        ok(f"{name}.no_runtime_executed", report.get("no_runtime_executed") is True)

    for i, row in enumerate(input_root_matrix.get("rows", [])):
        ok(f"input_row[{i}].intake_id", bool(row.get("intake_id")))
        ok(f"input_row[{i}].fact_status", row.get("fact_status") == "not_fact")

    for obj_name, obj in (
        ("closure_summary", closure_summary),
        ("decision_summary", decision_summary),
        ("boundary_freeze", boundary_freeze),
        ("non_claims", non_claims),
        ("human_carry", human_carry),
        ("permanent_carry", permanent_carry),
        ("deferred_pool", deferred_pool),
        ("readiness_gate", readiness_gate),
    ):
        ok(f"{obj_name}.fact_status", obj.get("fact_status") == "not_fact")
        ok(f"{obj_name}.write_allowed=false", obj.get("write_allowed") is False)

    ok("summary.fact_status", summary.get("fact_status") == "not_fact")

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
