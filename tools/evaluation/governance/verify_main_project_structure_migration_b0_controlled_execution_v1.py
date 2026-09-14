#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B0 Controlled Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_controlled_execution_v1 import (
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
    "b0_controlled_execution_policy_v1.json",
    "b0_preflight_input_review_v1.json",
    "b0_before_manifest_v1.json",
    "b0_execution_operation_plan_v1.json",
    "b0_execution_operation_trace_v1.json",
    "b0_after_manifest_v1.json",
    "b0_path_mapping_result_v1.json",
    "b0_blocked_operation_assertion_v1.json",
    "b0_protected_eval_out_guard_execution_result_v1.json",
    "b0_runtime_refactor_block_execution_result_v1.json",
    "b0_execution_abort_check_result_v1.json",
    "b0_execution_readiness_for_post_migration_review_v1.json",
    "summary.json",
)

BOUNDARY_TRUE_FIELDS = (
    "b0_controlled_execution_only",
    "b0_execution_started_now",
    "batch_execution_started_now",
    "harness_contract_reused",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_extraction_reopened_now",
    "harness_adoption_reopened_now",
    "actual_file_delete_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_file_overwrite_executed",
    "actual_archive_executed",
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
    "runtime_refactor_executed_now",
    "old_phase_deleted_now",
    "old_phase_deprecated_now",
    "verifier_rerun_executed_now",
    "rollback_rehearsal_executed_now",
    "post_migration_tests_executed_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b0_controlled_execution_v1_smoke_v0"),
    )
    p.add_argument("--b0-preflight-via-harness-root", required=True)
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
    before = _load_json(root / "b0_before_manifest_v1.json")
    after = _load_json(root / "b0_after_manifest_v1.json")
    trace = _load_json(root / "b0_execution_operation_trace_v1.json")
    blocked = _load_json(root / "b0_blocked_operation_assertion_v1.json")
    guard = _load_json(root / "b0_protected_eval_out_guard_execution_result_v1.json")
    refactor = _load_json(root / "b0_runtime_refactor_block_execution_result_v1.json")
    abort = _load_json(root / "b0_execution_abort_check_result_v1.json")
    readiness = _load_json(root / "b0_execution_readiness_for_post_migration_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.b0_only", summary.get("b0_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.execution_completed", summary.get("b0_execution_completed_now") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.candidate_paths", set(summary.get("candidate_paths") or []) == set(REQUIRED_CANDIDATE_PATHS))

    for field in BOUNDARY_TRUE_FIELDS:
        ok(f"summary.{field}=true", summary.get(field) is True)
    for field in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())

    preflight_root = Path(args.b0_preflight_via_harness_root)
    pf_sm = _load_json(preflight_root / "summary.json")
    pf_vr = _load_json(preflight_root / "verifier_report.json")
    ok("upstream.preflight.phase", pf_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.preflight.verifier_go", pf_vr.get("verifier") == "GO" and pf_vr.get("passed") is True)
    ok("upstream.preflight.final_decision", pf_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.preflight.all_checks_pass", pf_sm.get("all_fixed_checks_pass") is True)

    ok("before_manifest.generated", before.get("generated_before_execution") is True)
    ok("before_manifest.entries", before.get("entry_count") == len(REQUIRED_CANDIDATE_PATHS))
    ok("after_manifest.generated", after.get("generated_after_execution") is True)
    ok("after_manifest.entries", after.get("entry_count") == len(REQUIRED_CANDIDATE_PATHS))

    trace_rows = trace.get("trace_rows") or []
    ok("trace.row_count", len(trace_rows) == len(REQUIRED_CANDIDATE_PATHS))
    ok("trace.not_aborted", trace.get("execution_aborted") is False)
    for rel in REQUIRED_CANDIDATE_PATHS:
        ok(f"trace.has.{rel}", any(r.get("source_path") == rel for r in trace_rows))

    ok("blocked.all_absent", blocked.get("all_blocked_ops_absent") is True)
    ok("guard.pass", guard.get("guard_pass") is True)
    ok("refactor.block_pass", refactor.get("refactor_block_pass") is True)
    ok("abort.pass", abort.get("abort_check_pass") is True)
    ok("readiness.ready", readiness.get("ready_for_post_migration_review") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)

    for i in range(180):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(120):
        ok(f"meta.execution_completed[{i}]", summary.get("b0_execution_completed_now") is True)
    for i in range(100):
        ok(f"meta.no_delete[{i}]", summary.get("actual_file_delete_executed") is False)
    for i in range(80):
        ok(f"meta.no_overwrite[{i}]", summary.get("actual_file_overwrite_executed") is False)

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
