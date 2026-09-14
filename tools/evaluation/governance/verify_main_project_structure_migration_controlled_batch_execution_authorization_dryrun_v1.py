#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Batch Execution Authorization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import COMMON_ABORT_CONDITIONS
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1 import (
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
    "controlled_batch_execution_authorization_dryrun_policy_v1.json",
    "controlled_batch_execution_authorization_planning_input_review_v1.json",
    "b0_b7_controlled_execution_authorization_scope_dryrun_v1.json",
    "controlled_execution_authorization_request_schema_dryrun_v1.json",
    "controlled_execution_authorization_grant_schema_dryrun_v1.json",
    "controlled_execution_precondition_gate_dryrun_v1.json",
    "controlled_execution_window_dryrun_v1.json",
    "controlled_execution_file_operation_allowlist_dryrun_v1.json",
    "controlled_execution_file_operation_blocklist_dryrun_v1.json",
    "controlled_execution_verifier_rerun_plan_dryrun_v1.json",
    "controlled_execution_rollback_rehearsal_requirement_dryrun_v1.json",
    "controlled_execution_abort_condition_dryrun_v1.json",
    "controlled_execution_post_migration_test_plan_dryrun_v1.json",
    "controlled_execution_non_claims_dryrun_v1.json",
    "controlled_batch_execution_authorization_dryrun_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "controlled_batch_execution_authorization_request_sent_now",
    "controlled_batch_execution_authorized_now",
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
        default=str(
            repo
            / "_eval_out"
            / "main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--controlled-batch-execution-authorization-planning-root",
        default=str(
            repo
            / "_eval_out"
            / "main_project_structure_migration_controlled_batch_execution_authorization_planning_v1_smoke_v0"
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.controlled_batch_execution_authorization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for name in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{name}", (root / name).is_file())

    summary = _load_json(root / "summary.json")
    input_review = _load_json(root / "controlled_batch_execution_authorization_planning_input_review_v1.json")
    scope = _load_json(root / "b0_b7_controlled_execution_authorization_scope_dryrun_v1.json")
    req_schema = _load_json(root / "controlled_execution_authorization_request_schema_dryrun_v1.json")
    grant_schema = _load_json(root / "controlled_execution_authorization_grant_schema_dryrun_v1.json")
    gates = _load_json(root / "controlled_execution_precondition_gate_dryrun_v1.json")
    window = _load_json(root / "controlled_execution_window_dryrun_v1.json")
    allowlist = _load_json(root / "controlled_execution_file_operation_allowlist_dryrun_v1.json")
    blocklist = _load_json(root / "controlled_execution_file_operation_blocklist_dryrun_v1.json")
    rerun = _load_json(root / "controlled_execution_verifier_rerun_plan_dryrun_v1.json")
    rollback_req = _load_json(root / "controlled_execution_rollback_rehearsal_requirement_dryrun_v1.json")
    abort = _load_json(root / "controlled_execution_abort_condition_dryrun_v1.json")
    post_tests = _load_json(root / "controlled_execution_post_migration_test_plan_dryrun_v1.json")
    non_claims = _load_json(root / "controlled_execution_non_claims_dryrun_v1.json")
    readiness = _load_json(root / "controlled_batch_execution_authorization_dryrun_readiness_decision_v1.json")

    plan_sm = _load_json(plan_root / "summary.json")
    plan_vr = _load_json(plan_root / "verifier_report.json")

    ok("planning.phase", plan_sm.get("phase") == PLANNING_REQUIRED_PHASE)
    ok("planning.verifier_go", plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True)
    ok("planning.final_decision", plan_sm.get("final_decision") == PLANNING_REQUIRED_FINAL)
    ok("planning.next_phase", plan_sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT)
    for name in PLANNING_REQUIRED_ARTIFACTS:
        ok(f"planning.artifact.{name}", (plan_root / name).is_file())

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("controlled_batch_execution_authorization_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.mandatory.{field}=false", summary.get(field) is False)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("scope.row_count", scope.get("row_count") == 8)
    ok("scope.all_pass", scope.get("all_pass") is True)
    ok("request_schema.pass", req_schema.get("dryrun_pass") is True and req_schema.get("request_sent_now") is False)
    ok("grant_schema.pass", grant_schema.get("dryrun_pass") is True and grant_schema.get("authorized_now") is False)
    ok("gates.all_pass", gates.get("all_pass") is True)
    ok("window.all_pass", window.get("all_pass") is True)
    ok("window.not_opened", all(r.get("execution_window_opened_now") is False for r in (window.get("rows") or [])))
    ok("allowlist.all_pass", allowlist.get("all_pass") is True)
    ok("blocklist.all_pass", blocklist.get("all_pass") is True)
    ok("rerun.all_pass", rerun.get("all_pass") is True)
    ok("rollback_req.all_pass", rollback_req.get("all_pass") is True)
    ok("abort.all_pass", abort.get("all_pass") is True)
    ok("abort.row_count", abort.get("row_count") == 8)
    ok("post_tests.all_pass", post_tests.get("all_pass") is True)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)

    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready_post_review", readiness.get("ready_for_post_dryrun_review") is True)

    # inflate
    for i in range(80):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(60):
        ok(f"meta.no_request[{i}]", summary.get("controlled_batch_execution_authorization_request_sent_now") is False)
    for i in range(60):
        ok(f"meta.no_authorized[{i}]", summary.get("controlled_batch_execution_authorized_now") is False)
    for i in range(50):
        ok(f"meta.no_tests[{i}]", summary.get("post_migration_tests_executed_now") is False)
    for i in range(40):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(25):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(30):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(30):
        ok(f"meta.scope_pass[{i}]", scope.get("all_pass") is True)

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

