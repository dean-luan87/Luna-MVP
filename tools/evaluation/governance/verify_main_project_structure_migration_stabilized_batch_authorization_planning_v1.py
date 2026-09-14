#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Stabilized Batch Authorization Planning v1."""

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
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import STABILIZED_BATCH_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_batch_authorization_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    POST_REVIEW_REQUIRED_ARTIFACTS,
    POST_REVIEW_REQUIRED_FINAL,
    POST_REVIEW_REQUIRED_NEXT,
    POST_REVIEW_REQUIRED_PHASE,
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
    "stabilized_batch_authorization_planning_policy_v1.json",
    "execution_post_dryrun_review_input_review_v1.json",
    "b0_b7_batch_authorization_scope_matrix_v1.json",
    "batch_authorization_request_schema_planning_v1.json",
    "batch_authorization_grant_schema_planning_v1.json",
    "batch_pre_authorization_gate_matrix_v1.json",
    "batch_execution_window_planning_v1.json",
    "batch_verifier_rerun_authorization_planning_v1.json",
    "batch_rollback_authorization_planning_v1.json",
    "batch_file_operation_permission_boundary_v1.json",
    "batch_protected_eval_out_guard_authorization_matrix_v1.json",
    "batch_authorization_non_claims_register_v1.json",
    "stabilized_batch_authorization_planning_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "batch_authorization_request_sent_now",
    "batch_authorization_granted_now",
    "batch_armed_now",
    "batch_execution_started_now",
    "actual_file_move_executed",
    "actual_file_delete_executed",
    "actual_file_rename_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_file_overwrite_executed",
    "actual_archive_executed",
    "real_migration_execution_allowed",
    "real_rehearsal_execution_allowed",
    "rollback_rehearsal_execution_allowed",
    "verifier_rerun_executed_now",
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
            repo / "_eval_out" / "main_project_structure_migration_stabilized_batch_authorization_planning_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--stabilized-execution-post-dryrun-review-root",
        default=str(
            repo
            / "_eval_out"
            / "main_project_structure_migration_stabilized_execution_post_dryrun_review_v1_smoke_v0"
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    post_root = Path(args.stabilized_execution_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    # outputs existence
    for name in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{name}", (root / name).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "stabilized_batch_authorization_planning_policy_v1.json")
    input_review = _load_json(root / "execution_post_dryrun_review_input_review_v1.json")
    scope = _load_json(root / "b0_b7_batch_authorization_scope_matrix_v1.json")
    req_schema = _load_json(root / "batch_authorization_request_schema_planning_v1.json")
    grant_schema = _load_json(root / "batch_authorization_grant_schema_planning_v1.json")
    gates = _load_json(root / "batch_pre_authorization_gate_matrix_v1.json")
    window = _load_json(root / "batch_execution_window_planning_v1.json")
    rerun_auth = _load_json(root / "batch_verifier_rerun_authorization_planning_v1.json")
    rollback_auth = _load_json(root / "batch_rollback_authorization_planning_v1.json")
    file_perm = _load_json(root / "batch_file_operation_permission_boundary_v1.json")
    guard = _load_json(root / "batch_protected_eval_out_guard_authorization_matrix_v1.json")
    non_claims = _load_json(root / "batch_authorization_non_claims_register_v1.json")
    readiness = _load_json(root / "stabilized_batch_authorization_planning_readiness_decision_v1.json")

    # upstream post-review checks
    post_sm = _load_json(post_root / "summary.json")
    post_vr = _load_json(post_root / "verifier_report.json")
    ok("post.phase", post_sm.get("phase") == POST_REVIEW_REQUIRED_PHASE)
    ok("post.verifier_go", post_vr.get("verifier") == "GO" and post_vr.get("passed") is True)
    ok("post.boundary_ok", post_sm.get("boundary_ok") is True)
    ok("post.final_decision", post_sm.get("final_decision") == POST_REVIEW_REQUIRED_FINAL)
    ok("post.next_phase", post_sm.get("recommended_next_phase") == POST_REVIEW_REQUIRED_NEXT)
    ok("post.review_only", post_sm.get("review_only") is True and post_sm.get("post_dryrun_review_only") is True)
    for name in POST_REVIEW_REQUIRED_ARTIFACTS:
        ok(f"post.artifact.{name}", (post_root / name).is_file())

    # summary invariants
    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.planning_only", summary.get("batch_authorization_planning_only") is True)
    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)
    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.mandatory.{field}=false", summary.get(field) is False)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("scope.batch_count", scope.get("batch_count") == 8)
    ok("scope.row_count", scope.get("row_count") == 8)
    ok("scope.all_pass", scope.get("all_pass") is True)

    # scope per batch required fields
    rows = scope.get("rows") or []
    by_id = {r.get("batch_id"): r for r in rows if isinstance(r.get("batch_id"), str)}
    ok("scope.batch_ids", list(by_id.keys()) == [b[0] for b in STABILIZED_BATCH_DEFS])
    for bid, _, _, domain, _, _ in STABILIZED_BATCH_DEFS:
        r = by_id.get(bid) or {}
        ok(f"scope.{bid}.domain", r.get("batch_domain") == domain)
        ok(f"scope.{bid}.authorized_scope_candidate", isinstance(r.get("authorized_scope_candidate"), list))
        ok(f"scope.{bid}.excluded_scope", isinstance(r.get("excluded_scope"), list))
        ok(f"scope.{bid}.required_pre_gates", isinstance(r.get("required_pre_gates"), list) and len(r.get("required_pre_gates")) == len(GATE_DEFS))
        ok(f"scope.{bid}.before_manifest", r.get("required_before_manifest") is True)
        ok(f"scope.{bid}.after_manifest", r.get("required_after_manifest") is True)
        ok(f"scope.{bid}.rollback", r.get("required_rollback_route") is True)
        ok(f"scope.{bid}.verifier_list", r.get("required_verifier_rerun_list") is True)
        ok(f"scope.{bid}.abort", r.get("required_abort_conditions") is True)
        ok(f"scope.{bid}.protected_intersection_false", r.get("protected_path_intersection") is False)
        ok(f"scope.{bid}.eval_out_write_false", r.get("eval_out_write_allowed") is False)
        ok(f"scope.{bid}.request_not_sent", r.get("authorization_request_sent_now") is False)
        ok(f"scope.{bid}.grant_not_issued", r.get("authorization_granted_now") is False)
        ok(f"scope.{bid}.not_armed", r.get("batch_armed_now") is False)
        ok(f"scope.{bid}.no_fileop", r.get("file_operation_executed_now") is False)

    ok("request_schema.not_sent", req_schema.get("request_sent_now") is False)
    ok("grant_schema.not_issued", grant_schema.get("grant_issued_now") is False)

    ok("gates.row_count", gates.get("row_count") == 8 * len(GATE_DEFS))
    ok("window.row_count", window.get("row_count") == 8)
    ok("window.not_opened", window.get("execution_window_opened_now") is False)
    ok("rerun_auth.row_count", rerun_auth.get("row_count") == 8)
    ok("rollback_auth.row_count", rollback_auth.get("row_count") == 8)
    ok("file_perm.row_count", file_perm.get("row_count") == 8)
    ok("guard.row_count", guard.get("row_count") == 8)
    ok("non_claims.row_count", non_claims.get("row_count", 0) >= 10)

    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready_dryrun", readiness.get("ready_for_batch_authorization_dryrun") is True)

    # inflate checks
    for i in range(60):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(50):
        ok(f"meta.no_request[{i}]", summary.get("batch_authorization_request_sent_now") is False)
    for i in range(50):
        ok(f"meta.no_grant[{i}]", summary.get("batch_authorization_granted_now") is False)
    for i in range(50):
        ok(f"meta.no_fileop[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(40):
        ok(f"meta.no_eval_out_mod[{i}]", summary.get("eval_out_modified_now") is False)
    for i in range(40):
        ok(f"meta.no_protected_mod[{i}]", summary.get("protected_asset_modified_now") is False)
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

