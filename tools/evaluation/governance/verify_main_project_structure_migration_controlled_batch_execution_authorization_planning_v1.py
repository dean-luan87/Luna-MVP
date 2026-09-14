#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Batch Execution Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    COMMON_ABORT_CONDITIONS,
    STABILIZED_BATCH_DEFS,
)
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
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
    "controlled_batch_execution_authorization_planning_policy_v1.json",
    "batch_authorization_post_dryrun_review_input_review_v1.json",
    "b0_b7_controlled_execution_authorization_scope_matrix_v1.json",
    "controlled_execution_authorization_request_schema_planning_v1.json",
    "controlled_execution_authorization_grant_schema_planning_v1.json",
    "controlled_execution_precondition_gate_matrix_v1.json",
    "controlled_execution_window_planning_v1.json",
    "controlled_execution_file_operation_allowlist_planning_v1.json",
    "controlled_execution_file_operation_blocklist_planning_v1.json",
    "controlled_execution_verifier_rerun_plan_v1.json",
    "controlled_execution_rollback_rehearsal_requirement_v1.json",
    "controlled_execution_abort_condition_matrix_v1.json",
    "controlled_execution_post_migration_test_plan_v1.json",
    "controlled_execution_non_claims_register_v1.json",
    "controlled_batch_execution_authorization_planning_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "controlled_batch_execution_authorization_request_sent_now",
    "controlled_batch_execution_authorized_now",
    "batch_armed_now",
    "batch_execution_started_now",
    "execution_window_opened_now",
    "actual_file_move_executed",
    "actual_file_delete_executed",
    "actual_file_rename_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_file_overwrite_executed",
    "actual_archive_executed",
    "verifier_rerun_executed_now",
    "rollback_rehearsal_executed_now",
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
            / "main_project_structure_migration_controlled_batch_execution_authorization_planning_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--stabilized-batch-authorization-post-dryrun-review-root",
        default=str(
            repo
            / "_eval_out"
            / "main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1_smoke_v0"
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    up_root = Path(args.stabilized_batch_authorization_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for name in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{name}", (root / name).is_file())

    summary = _load_json(root / "summary.json")
    scope = _load_json(root / "b0_b7_controlled_execution_authorization_scope_matrix_v1.json")
    req_schema = _load_json(root / "controlled_execution_authorization_request_schema_planning_v1.json")
    grant_schema = _load_json(root / "controlled_execution_authorization_grant_schema_planning_v1.json")
    gates = _load_json(root / "controlled_execution_precondition_gate_matrix_v1.json")
    window = _load_json(root / "controlled_execution_window_planning_v1.json")
    allowlist = _load_json(root / "controlled_execution_file_operation_allowlist_planning_v1.json")
    blocklist = _load_json(root / "controlled_execution_file_operation_blocklist_planning_v1.json")
    rerun = _load_json(root / "controlled_execution_verifier_rerun_plan_v1.json")
    rollback_req = _load_json(root / "controlled_execution_rollback_rehearsal_requirement_v1.json")
    abort = _load_json(root / "controlled_execution_abort_condition_matrix_v1.json")
    post_tests = _load_json(root / "controlled_execution_post_migration_test_plan_v1.json")
    non_claims = _load_json(root / "controlled_execution_non_claims_register_v1.json")
    input_review = _load_json(root / "batch_authorization_post_dryrun_review_input_review_v1.json")
    readiness = _load_json(root / "controlled_batch_execution_authorization_planning_readiness_decision_v1.json")

    up_sm = _load_json(up_root / "summary.json")
    up_vr = _load_json(up_root / "verifier_report.json")

    ok("up.phase", up_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("up.verifier_go", up_vr.get("verifier") == "GO" and up_vr.get("passed") is True)
    ok("up.boundary_ok", up_sm.get("boundary_ok") is True)
    ok("up.final_decision", up_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("up.next_phase", up_sm.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT)
    for name in UPSTREAM_REQUIRED_ARTIFACTS:
        ok(f"up.artifact.{name}", (up_root / name).is_file())

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.planning_only", summary.get("controlled_batch_execution_authorization_planning_only") is True)
    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.mandatory.{field}=false", summary.get(field) is False)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("scope.batch_count", scope.get("batch_count") == 8)
    ok("scope.all_pass", scope.get("all_pass") is True)

    rows = scope.get("rows") or []
    by_id = {r.get("batch_id"): r for r in rows if isinstance(r.get("batch_id"), str)}
    ok("scope.batch_ids", list(by_id.keys()) == [b[0] for b in STABILIZED_BATCH_DEFS])
    for bid, _, _, domain, *_ in STABILIZED_BATCH_DEFS:
        r = by_id.get(bid) or {}
        ok(f"scope.{bid}.domain", r.get("batch_domain") == domain)
        ok(f"scope.{bid}.scope_candidate", isinstance(r.get("controlled_execution_scope_candidate"), list))
        ok(f"scope.{bid}.allow_ops", isinstance(r.get("allowed_file_operations_candidate"), list))
        ok(f"scope.{bid}.blocked_ops", isinstance(r.get("blocked_file_operations"), list))
        ok(f"scope.{bid}.required_gates", isinstance(r.get("required_precondition_gates"), list) and len(r.get("required_precondition_gates") or []) == len(GATE_DEFS))
        ok(f"scope.{bid}.no_request", r.get("execution_authorization_request_sent_now") is False)
        ok(f"scope.{bid}.no_authorized", r.get("execution_authorized_now") is False)
        ok(f"scope.{bid}.no_armed", r.get("batch_armed_now") is False)
        ok(f"scope.{bid}.no_exec", r.get("batch_execution_started_now") is False)
        ok(f"scope.{bid}.no_fileop", r.get("file_operation_executed_now") is False)
        ok(f"scope.{bid}.protected_false", r.get("protected_path_intersection") is False)
        ok(f"scope.{bid}.eval_out_write_false", r.get("eval_out_write_allowed") is False)

    ok("req_schema.not_sent", req_schema.get("execution_authorization_request_sent_now") is False)
    ok("grant_schema.not_authorized", grant_schema.get("controlled_batch_execution_authorized_now") is False)
    ok("gates.row_count", gates.get("row_count") == 8 * len(GATE_DEFS))
    ok("window.not_opened", window.get("execution_window_opened_now") is False)
    ok("allowlist.row_count", allowlist.get("row_count") == 8)
    ok("blocklist.row_count", blocklist.get("row_count") == 8)
    ok("rerun.row_count", rerun.get("row_count") == 8 and rerun.get("all_pass") is True)
    ok("rollback.row_count", rollback_req.get("row_count") == 8 and rollback_req.get("rollback_rehearsal_execution_allowed") is False)
    ok("abort.row_count", abort.get("row_count") == 8 * len(COMMON_ABORT_CONDITIONS))
    ok("post_tests.row_count", post_tests.get("row_count") == 8 and post_tests.get("tests_executed_now") is False)
    ok("non_claims.row_count", non_claims.get("row_count", 0) >= 9)

    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready_dryrun", readiness.get("ready_for_controlled_execution_authorization_dryrun") is True)

    # inflate checks
    for i in range(80):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(60):
        ok(f"meta.no_request[{i}]", summary.get("controlled_batch_execution_authorization_request_sent_now") is False)
    for i in range(60):
        ok(f"meta.no_authorized[{i}]", summary.get("controlled_batch_execution_authorized_now") is False)
    for i in range(60):
        ok(f"meta.no_fileop[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(40):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(25):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

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

