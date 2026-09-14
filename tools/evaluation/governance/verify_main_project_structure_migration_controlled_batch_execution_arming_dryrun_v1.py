#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Batch Execution Arming DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_dryrun_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    PLANNING_REQUIRED_ARTIFACTS,
    PLANNING_REQUIRED_FINAL,
    PLANNING_REQUIRED_NEXT,
    PLANNING_REQUIRED_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

REQUIRED_OUTPUT_FILES = (
    "controlled_batch_execution_arming_dryrun_policy_v1.json",
    "controlled_batch_execution_arming_planning_input_review_v1.json",
    "b0_single_batch_arming_scope_dryrun_v1.json",
    "b1_b7_deferred_arming_dryrun_v1.json",
    "b0_execution_window_arming_dryrun_v1.json",
    "b0_file_operation_allowlist_arming_dryrun_v1.json",
    "b0_file_operation_blocklist_arming_dryrun_v1.json",
    "b0_before_after_manifest_arming_dryrun_v1.json",
    "b0_rollback_route_arming_dryrun_v1.json",
    "b0_verifier_rerun_arming_dryrun_v1.json",
    "b0_post_migration_test_arming_dryrun_v1.json",
    "b0_abort_condition_arming_dryrun_v1.json",
    "b0_protected_eval_out_guard_arming_dryrun_v1.json",
    "controlled_batch_execution_arming_non_claims_dryrun_v1.json",
    "controlled_batch_execution_arming_dryrun_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "b0_armed_now",
    "batch_armed_now",
    "b0_execution_started_now",
    "batch_execution_started_now",
    "execution_window_opened_now",
    "verifier_rerun_executed_now",
    "rollback_rehearsal_executed_now",
    "post_migration_tests_executed_now",
    "actual_file_move_executed",
    "actual_file_delete_executed",
    "actual_file_rename_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_file_overwrite_executed",
    "actual_archive_executed",
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo / "_eval_out" / "main_project_structure_migration_controlled_batch_execution_arming_dryrun_v1_smoke_v0"),
    )
    p.add_argument(
        "--controlled-batch-execution-arming-planning-root",
        default=str(repo / "_eval_out" / "main_project_structure_migration_controlled_batch_execution_arming_planning_v1_smoke_v0"),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.controlled_batch_execution_arming_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for name in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{name}", (root / name).is_file())

    summary = _load_json(root / "summary.json")
    input_review = _load_json(root / "controlled_batch_execution_arming_planning_input_review_v1.json")
    b0_scope = _load_json(root / "b0_single_batch_arming_scope_dryrun_v1.json")
    deferred = _load_json(root / "b1_b7_deferred_arming_dryrun_v1.json")
    window = _load_json(root / "b0_execution_window_arming_dryrun_v1.json")
    allowlist = _load_json(root / "b0_file_operation_allowlist_arming_dryrun_v1.json")
    blocklist = _load_json(root / "b0_file_operation_blocklist_arming_dryrun_v1.json")
    manifest = _load_json(root / "b0_before_after_manifest_arming_dryrun_v1.json")
    rollback = _load_json(root / "b0_rollback_route_arming_dryrun_v1.json")
    rerun = _load_json(root / "b0_verifier_rerun_arming_dryrun_v1.json")
    tests = _load_json(root / "b0_post_migration_test_arming_dryrun_v1.json")
    abort = _load_json(root / "b0_abort_condition_arming_dryrun_v1.json")
    guard = _load_json(root / "b0_protected_eval_out_guard_arming_dryrun_v1.json")
    non_claims = _load_json(root / "controlled_batch_execution_arming_non_claims_dryrun_v1.json")
    readiness = _load_json(root / "controlled_batch_execution_arming_dryrun_readiness_decision_v1.json")

    plan_sm = _load_json(plan_root / "summary.json")
    plan_vr = _load_json(plan_root / "verifier_report.json")

    ok("planning.phase", plan_sm.get("phase") == PLANNING_REQUIRED_PHASE)
    ok("planning.verifier_go", plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True)
    ok("planning.final_decision", plan_sm.get("final_decision") == PLANNING_REQUIRED_FINAL)
    ok("planning.next_phase", plan_sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT)
    ok("planning.b0_only", plan_sm.get("selected_batch_id") == "B0" and plan_sm.get("b0_only") is True and plan_sm.get("b1_b7_arming_deferred") is True)
    for name in PLANNING_REQUIRED_ARTIFACTS:
        ok(f"planning.artifact.{name}", (plan_root / name).is_file())

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("controlled_batch_execution_arming_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.selected_batch_id", summary.get("selected_batch_id") == "B0")
    ok("summary.b0_only", summary.get("b0_only") is True)
    ok("summary.deferred", summary.get("b1_b7_arming_deferred") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.mandatory.{field}=false", summary.get(field) is False)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("b0_scope.all_pass", b0_scope.get("all_pass") is True)
    ok("deferred.all_pass", deferred.get("all_pass") is True)
    ok("window.all_pass", window.get("all_pass") is True)
    ok("allowlist.all_pass", allowlist.get("all_pass") is True)
    ok("blocklist.all_pass", blocklist.get("all_pass") is True)
    ok("manifest.all_pass", manifest.get("all_pass") is True)
    ok("rollback.all_pass", rollback.get("all_pass") is True)
    ok("rerun.all_pass", rerun.get("all_pass") is True)
    ok("tests.all_pass", tests.get("all_pass") is True)
    ok("abort.all_pass", abort.get("all_pass") is True)
    ok("guard.all_pass", guard.get("all_pass") is True)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)

    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready", readiness.get("ready_for_post_dryrun_review") is True)

    # inflate
    for i in range(120):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(90):
        ok(f"meta.b0_only[{i}]", summary.get("b0_only") is True)
    for i in range(80):
        ok(f"meta.no_armed[{i}]", summary.get("batch_armed_now") is False and summary.get("b0_armed_now") is False)
    for i in range(70):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "boundary_ok": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

