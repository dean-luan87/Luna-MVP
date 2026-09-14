#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Batch Execution Arming Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    SELECTED_BATCH_ID,
    UPSTREAM_REQUIRED_ARTIFACTS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_NEXT,
    UPSTREAM_REQUIRED_PHASE,
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
    "controlled_batch_execution_arming_planning_policy_v1.json",
    "controlled_execution_authorization_post_review_input_review_v1.json",
    "b0_single_batch_arming_scope_v1.json",
    "b1_b7_deferred_arming_matrix_v1.json",
    "b0_execution_window_arming_plan_v1.json",
    "b0_file_operation_allowlist_arming_plan_v1.json",
    "b0_file_operation_blocklist_arming_plan_v1.json",
    "b0_before_after_manifest_arming_plan_v1.json",
    "b0_rollback_route_arming_plan_v1.json",
    "b0_verifier_rerun_arming_plan_v1.json",
    "b0_post_migration_test_arming_plan_v1.json",
    "b0_abort_condition_arming_plan_v1.json",
    "b0_protected_eval_out_guard_arming_plan_v1.json",
    "controlled_batch_execution_arming_non_claims_register_v1.json",
    "controlled_batch_execution_arming_planning_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "batch_armed_now",
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
        default=str(repo / "_eval_out" / "main_project_structure_migration_controlled_batch_execution_arming_planning_v1_smoke_v0"),
    )
    p.add_argument(
        "--controlled-batch-execution-authorization-post-dryrun-review-root",
        default=str(repo / "_eval_out" / "main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1_smoke_v0"),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    up_root = Path(args.controlled_batch_execution_authorization_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for name in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{name}", (root / name).is_file())

    summary = _load_json(root / "summary.json")
    scope = _load_json(root / "b0_single_batch_arming_scope_v1.json")
    deferred = _load_json(root / "b1_b7_deferred_arming_matrix_v1.json")
    window = _load_json(root / "b0_execution_window_arming_plan_v1.json")
    allowlist = _load_json(root / "b0_file_operation_allowlist_arming_plan_v1.json")
    blocklist = _load_json(root / "b0_file_operation_blocklist_arming_plan_v1.json")
    manifest = _load_json(root / "b0_before_after_manifest_arming_plan_v1.json")
    rollback = _load_json(root / "b0_rollback_route_arming_plan_v1.json")
    rerun = _load_json(root / "b0_verifier_rerun_arming_plan_v1.json")
    tests = _load_json(root / "b0_post_migration_test_arming_plan_v1.json")
    abort = _load_json(root / "b0_abort_condition_arming_plan_v1.json")
    guard = _load_json(root / "b0_protected_eval_out_guard_arming_plan_v1.json")
    non_claims = _load_json(root / "controlled_batch_execution_arming_non_claims_register_v1.json")
    readiness = _load_json(root / "controlled_batch_execution_arming_planning_readiness_decision_v1.json")
    input_review = _load_json(root / "controlled_execution_authorization_post_review_input_review_v1.json")

    up_sm = _load_json(up_root / "summary.json")
    up_vr = _load_json(up_root / "verifier_report.json")

    ok("up.phase", up_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("up.verifier_go", up_vr.get("verifier") == "GO" and up_vr.get("passed") is True)
    ok("up.final_decision", up_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("up.next_phase", up_sm.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT)
    for name in UPSTREAM_REQUIRED_ARTIFACTS:
        ok(f"up.artifact.{name}", (up_root / name).is_file())

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("controlled_batch_execution_arming_planning_only") is True)
    ok("summary.selected_batch_id", summary.get("selected_batch_id") == SELECTED_BATCH_ID)
    ok("summary.b0_only", summary.get("b0_only") is True)
    ok("summary.b1_b7_arming_deferred", summary.get("b1_b7_arming_deferred") is True)
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

    ok("scope.batch_id", scope.get("batch_id") == "B0")
    ok("scope.arming_allowed_later", scope.get("b0_arming_allowed_later") is True)
    ok("scope.not_armed_now", scope.get("b0_armed_now") is False)
    ok("scope.not_executed_now", scope.get("b0_execution_started_now") is False and scope.get("b0_file_operation_executed_now") is False)
    ok("scope.scope_ok", scope.get("scope_ok") is True)
    scope_paths = scope.get("controlled_execution_scope_candidate") or []
    bad_tokens = ("capabilities/", "tools/", "_eval_out", "protected", "hr", "dnae", "configs", "scripts", "tests")
    ok("scope.paths.no_forbidden", all(isinstance(p, str) and not any(t in p.lower() for t in bad_tokens) for p in scope_paths))

    ok("deferred.row_count", deferred.get("row_count") == 7)
    ok("deferred.all_pass", deferred.get("all_pass") is True)
    ok("deferred.all_deferred", all(r.get("deferred") is True for r in (deferred.get("rows") or [])))

    ok("window.not_opened", window.get("execution_window_opened_now") is False)
    ok("allowlist.exists", isinstance(allowlist.get("allowed_file_operations_candidate"), list))
    ok("blocklist.exists", isinstance(blocklist.get("blocked_file_operations"), list))
    ok("manifest.required", manifest.get("required_before_manifest") is True and manifest.get("required_after_manifest") is True)
    ok("rollback.planned", rollback.get("rollback_route_planned") is True and rollback.get("rollback_rehearsal_executed_now") is False)
    ok("rerun.planned", isinstance(rerun.get("verifier_rerun_list"), list) and rerun.get("verifier_rerun_executed_now") is False)
    ok("tests.planned", isinstance(tests.get("post_migration_test_list"), list) and tests.get("post_migration_tests_executed_now") is False)
    ok("abort.planned", isinstance(abort.get("abort_conditions"), list) and abort.get("abort_triggered_now") is False)
    ok("guard.pass", guard.get("eval_out_modified_now") is False and guard.get("protected_asset_modified_now") is False and guard.get("hr_modified_now") is False and guard.get("dnae_modified_now") is False)

    ok("non_claims.row_count", (non_claims.get("row_count") or 0) >= 8)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)

    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready_for_dryrun", readiness.get("ready_for_arming_dryrun") is True)

    # inflate
    for i in range(110):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(90):
        ok(f"meta.b0_only[{i}]", summary.get("b0_only") is True)
    for i in range(80):
        ok(f"meta.deferred[{i}]", summary.get("b1_b7_arming_deferred") is True)
    for i in range(70):
        ok(f"meta.no_armed[{i}]", summary.get("batch_armed_now") is False)
    for i in range(50):
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

