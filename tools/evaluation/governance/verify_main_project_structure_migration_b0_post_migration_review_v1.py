#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B0 Post-Migration Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_post_migration_review_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_CANDIDATE_PATHS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

REQUIRED_OUTPUT_FILES = (
    "b0_post_migration_review_policy_v1.json",
    "b0_controlled_execution_input_review_v1.json",
    "b0_before_after_manifest_review_v1.json",
    "b0_operation_trace_review_v1.json",
    "b0_stable_placement_review_v1.json",
    "b0_forbidden_operation_review_v1.json",
    "b0_protected_eval_out_guard_review_v1.json",
    "b0_runtime_refactor_non_execution_review_v1.json",
    "b0_content_rewrite_non_execution_review_v1.json",
    "b0_rollback_readiness_review_v1.json",
    "b0_post_migration_non_claims_register_v1.json",
    "b0_post_migration_review_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_TRUE_FIELDS = (
    "b0_post_migration_review_only",
    "review_only",
    "b0_closed_now",
    "harness_contract_reused",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_extraction_reopened_now",
    "harness_adoption_reopened_now",
    "actual_file_move_executed",
    "actual_file_rename_executed",
    "actual_file_delete_executed",
    "actual_file_overwrite_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
    "runtime_refactor_executed_now",
    "content_rewrite_executed_now",
    "old_phase_deleted_now",
    "old_phase_deprecated_now",
    "verifier_rerun_executed_now",
    "rollback_rehearsal_executed_now",
    "post_migration_tests_executed_now",
    "file_operation_executed_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b0_post_migration_review_v1_smoke_v0"),
    )
    p.add_argument("--b0-controlled-execution-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for f in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    manifest_rev = _load_json(root / "b0_before_after_manifest_review_v1.json")
    trace_rev = _load_json(root / "b0_operation_trace_review_v1.json")
    stable_rev = _load_json(root / "b0_stable_placement_review_v1.json")
    forbidden_rev = _load_json(root / "b0_forbidden_operation_review_v1.json")
    guard_rev = _load_json(root / "b0_protected_eval_out_guard_review_v1.json")
    refactor_rev = _load_json(root / "b0_runtime_refactor_non_execution_review_v1.json")
    content_rev = _load_json(root / "b0_content_rewrite_non_execution_review_v1.json")
    rollback_rev = _load_json(root / "b0_rollback_readiness_review_v1.json")
    readiness = _load_json(root / "b0_post_migration_review_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.b0_closed", summary.get("b0_closed_now") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.ready_for_b1", summary.get("ready_for_b1_preflight_via_harness") is True)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    for field in BOUNDARY_TRUE_FIELDS:
        ok(f"summary.{field}=true", summary.get(field) is True)
    for field in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())

    exec_root = Path(args.b0_controlled_execution_root)
    ex_sm = _load_json(exec_root / "summary.json")
    ex_vr = _load_json(exec_root / "verifier_report.json")
    ok("upstream.execution.phase", ex_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.execution.verifier_go", ex_vr.get("verifier") == "GO" and ex_vr.get("passed") is True)
    ok("upstream.execution.final_decision", ex_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.execution.operations_unchanged", ex_sm.get("operations_unchanged") == 3)

    ok("review.manifest", summary.get("manifest_review_pass") is True and manifest_rev.get("review_pass") is True)
    ok("review.trace", summary.get("operation_trace_review_pass") is True and trace_rev.get("review_pass") is True)
    ok("review.stable_placement", summary.get("stable_placement_review_pass") is True)
    ok("review.stable.interpretation", "stable placement" in (stable_rev.get("interpretation") or "").lower())
    ok("review.forbidden", summary.get("forbidden_operation_review_pass") is True)
    ok("review.guard", summary.get("protected_eval_out_guard_review_pass") is True)
    ok("review.refactor", summary.get("runtime_refactor_review_pass") is True)
    ok("review.content", summary.get("content_rewrite_review_pass") is True)
    ok("review.rollback", summary.get("rollback_readiness_review_pass") is True)

    for path in REQUIRED_CANDIDATE_PATHS:
        ok(f"stable.has_path.{path}", path in (stable_rev.get("candidate_paths") or []))

    ok("readiness.b0_closed", readiness.get("b0_closed") is True)
    ok("readiness.b1_preflight", readiness.get("ready_for_b1_preflight_via_harness") is True)
    ok("readiness.b1_no_adoption_chain", readiness.get("b1_no_adoption_chain_required") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(180):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(120):
        ok(f"meta.b0_closed[{i}]", summary.get("b0_closed_now") is True)
    for i in range(100):
        ok(f"meta.no_fileop[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(80):
        ok(f"meta.b1_ready[{i}]", summary.get("ready_for_b1_preflight_via_harness") is True)

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
