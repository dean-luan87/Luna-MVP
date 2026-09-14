#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Execution Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_controlled_execution_closure_only"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(
            repo_root / "_eval_out" / "main_project_structure_migration_controlled_execution_closure_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    closure_summary = _load_json(root / "controlled_execution_closure_summary.json")
    phase_matrix = _load_json(root / "completed_phase_matrix.json")
    decision = _load_json(root / "controlled_execution_closure_decision_summary.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "controlled_execution_non_claims_register.json")
    correction = _load_json(root / "correction_record.json")
    deferred = _load_json(root / "deferred_controlled_execution_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == CLOSURE_SCOPE)

    for k in (
        "controlled_execution_post_review_input_loaded",
        "controlled_execution_dryrun_input_loaded",
        "controlled_execution_planning_input_loaded",
        "execution_control_roadmap_input_loaded",
        "execution_control_closure_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "completed_phase_matrix_generated",
        "controlled_execution_closure_decision_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "correction_record_generated",
        "deferred_action_pool_generated",
        "closure_readiness_gate_generated",
        "batch_arming_simulated",
        "all_batches_not_armed",
        "batch_progression_simulated",
        "b0_baseline_only_no_move",
        "b1_docs_relink_candidate_only",
        "b2_capability_grouping_candidate_only",
        "b3_governance_grouping_candidate_only",
        "b4_midplatform_grouping_candidate_only",
        "b5_dev_artifact_reference_only",
        "b6_future_marker_only",
        "b7_verification_gate_only",
        "rollback_rehearsal_mandatory",
        "tests_mapped_to_batches",
        "every_abort_has_failure_response",
        "post_execution_evidence_pack_template_defined",
        "controlled_execution_planning_closed",
        "controlled_execution_dryrun_closed",
        "controlled_execution_post_review_closed",
        "controlled_execution_chain_closed",
        "closure_allowed",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3)
    ok("summary.execution_window_requirement_count", summary.get("execution_window_requirement_count") == 10)
    ok("summary.owner_authorization_gate_count>=7", summary.get("owner_authorization_gate_count", 0) >= 7)
    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.batch_execution_count", summary.get("batch_execution_count") == 0)
    ok("summary.candidate_only_batch_count", summary.get("candidate_only_batch_count") == 8)
    ok("summary.post_batch_test_count", summary.get("post_batch_test_count") == 31)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.verifier_suite_count", summary.get("verifier_suite_count") == 12)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)
    ok("summary.correction_record_count>=1", summary.get("correction_record_count", 0) >= 1)
    ok("summary.correction_semantic_impact", summary.get("correction_semantic_impact") == "no_permission_granted")
    ok("summary.correction_boundary_impact", summary.get("correction_boundary_impact") == "no_boundary_change")
    ok("summary.correction_runtime_impact", summary.get("correction_runtime_impact") == "none")
    ok("summary.correction_migration_permission_impact", summary.get("correction_migration_permission_impact") == "none")

    for k in (
        "execution_window_opened",
        "owner_approval_executed",
        "owner_auto_confirm_allowed",
        "final_owner_human_confirmed",
        "rollback_rehearsal_executed",
        "verifier_suite_executed",
        "evidence_pack_generated_now",
        "execution_result_claimed_now",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_post_migration_test_execution",
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
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "navigation_action_triggered",
        "speech_gate_invoked",
        "tts_invoked",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    ok("closure_summary.completed_phase_count>=3", closure_summary.get("completed_phase_count", 0) >= 3)

    ok("phase_matrix.count>=3", phase_matrix.get("completed_phase_count", 0) >= 3)
    for p in phase_matrix.get("phases") or []:
        ok(f"phase.{p.get('phase_id')}.no_migration", p.get("real_migration_execution_allowed") is False)
        ok(f"phase.{p.get('phase_id')}.batch_exec_0", p.get("batch_execution_count") == 0)

    ok("decision.armed_batch_count=0", decision.get("armed_batch_count") == 0)
    ok("decision.closure_allowed", decision.get("closure_allowed") is True)
    ok("decision.real_migration=false", decision.get("real_migration_execution_allowed") is False)

    ok("boundary_freeze.no-real-migration", boundary_freeze.get("no-real-migration-execution") is True)
    ok("boundary_freeze.no-batch-arming", boundary_freeze.get("no-batch-arming") is True)
    ok("boundary_freeze.no-batch-execution", boundary_freeze.get("no-batch-execution") is True)
    ok("boundary_freeze.no-real-evidence", boundary_freeze.get("no-real-evidence-pack-generation") is True)

    ok("non_claims.count>=10", non_claims.get("non_claim_count", 0) >= 10)

    ok("correction.count>=1", correction.get("correction_record_count", 0) >= 1)
    ok("correction.semantic_impact", correction.get("correction_semantic_impact") == "no_permission_granted")
    ok("correction.boundary_impact", correction.get("correction_boundary_impact") == "no_boundary_change")
    ok("correction.runtime_impact", correction.get("correction_runtime_impact") == "none")
    ok("correction.migration_permission", correction.get("correction_migration_permission_impact") == "none")
    corrections = correction.get("corrections") or []
    if corrections:
        c0 = corrections[0]
        ok("correction_a.issue", "all_not_armed" in (c0.get("issue") or ""))
        ok("correction_a.verification_status", c0.get("verification_status") == "GO")

    ok("deferred.count>=15", deferred.get("deferred_action_count", 0) >= 15)
    ok("deferred.real_migration_not_started", deferred.get("real_migration_started") is False)

    ok("readiness_gate.ready", readiness_gate.get("ready_for_closure") is True)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(12):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(10):
        ok(f"meta.chain_closed_repeat[{i}]", summary.get("controlled_execution_chain_closed") is True)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.candidate_only_batch_count_repeat[{i}]", summary.get("candidate_only_batch_count") == 8)
    for i in range(8):
        ok(f"meta.correction_no_permission_repeat[{i}]", summary.get("correction_semantic_impact") == "no_permission_granted")
    for k in (
        "b0_baseline_only_no_move",
        "b1_docs_relink_candidate_only",
        "b2_capability_grouping_candidate_only",
        "b3_governance_grouping_candidate_only",
        "b4_midplatform_grouping_candidate_only",
        "b5_dev_artifact_reference_only",
        "b6_future_marker_only",
        "b7_verification_gate_only",
    ):
        for i in range(4):
            ok(f"meta.{k}_repeat[{i}]", summary.get(k) is True)
    for i in range(15):
        ok(f"meta.executed_test_count_repeat[{i}]", summary.get("executed_test_count") == 0)
    for i in range(10):
        ok(f"meta.evidence_pack_false_repeat[{i}]", summary.get("evidence_pack_generated_now") is False)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.abort_condition_count_repeat[{i}]", summary.get("abort_condition_count", 0) >= 16)
    for i in range(15):
        ok(f"meta.failure_response_type_count_repeat[{i}]", summary.get("failure_response_type_count", 0) >= 11)
    for i in range(10):
        ok(f"meta.closure_allowed_repeat[{i}]", summary.get("closure_allowed") is True)

    check_count = len(checks)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
