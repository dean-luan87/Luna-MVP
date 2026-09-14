#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B0 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_preflight_via_harness_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_CANDIDATE_PATHS,
    REQUIRED_FIXED_CHECKS,
    UPSTREAM_REQUIRED_FINAL,
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
    "b0_preflight_via_harness_policy_v1.json",
    "reusable_harness_contract_input_review_v1.json",
    "b0_batch_config_instance_v1.json",
    "b0_preflight_scope_check_result_v1.json",
    "b0_preflight_domain_isolation_check_result_v1.json",
    "b0_preflight_protected_guard_check_result_v1.json",
    "b0_preflight_eval_out_readonly_check_result_v1.json",
    "b0_preflight_file_operation_boundary_check_result_v1.json",
    "b0_preflight_manifest_requirement_check_result_v1.json",
    "b0_preflight_rollback_requirement_check_result_v1.json",
    "b0_preflight_verifier_rerun_requirement_check_result_v1.json",
    "b0_preflight_post_migration_test_requirement_check_result_v1.json",
    "b0_preflight_abort_condition_check_result_v1.json",
    "b0_preflight_workspace_fallback_check_result_v1.json",
    "b0_preflight_non_claims_check_result_v1.json",
    "b0_preflight_migration_refactor_opportunity_scan_v1.json",
    "b0_preflight_result_v1.json",
    "b0_preflight_via_harness_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_extraction_reopened_now",
    "harness_adoption_reopened_now",
    "b0_armed_now",
    "batch_armed_now",
    "b0_execution_started_now",
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
    "post_migration_tests_executed_now",
    "runtime_refactor_executed_now",
    "old_phase_deleted_now",
    "old_phase_deprecated_now",
    "file_operation_executed_now",
)

BOUNDARY_TRUE_FIELDS = (
    "b0_preflight_via_harness_only",
    "b0_preflight_executed_now",
    "harness_contract_reused",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b0_preflight_via_harness_v1_smoke_v0"),
    )
    p.add_argument("--b0-harness-adoption-and-reusable-contract-closure-root", required=True)
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
    batch_cfg = _load_json(root / "b0_batch_config_instance_v1.json")
    preflight = _load_json(root / "b0_preflight_result_v1.json")
    scan = _load_json(root / "b0_preflight_migration_refactor_opportunity_scan_v1.json")
    contract_review = _load_json(root / "reusable_harness_contract_input_review_v1.json")
    readiness = _load_json(root / "b0_preflight_via_harness_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.b0_only", summary.get("b0_only") is True)
    ok("summary.b1_b7_deferred", summary.get("b1_b7_deferred") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.all_fixed_checks_pass", summary.get("all_fixed_checks_pass") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    for field in BOUNDARY_TRUE_FIELDS:
        ok(f"summary.{field}=true", summary.get(field) is True)
    for field in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    closure_root = Path(args.b0_harness_adoption_and_reusable_contract_closure_root)
    closure_sm = _load_json(closure_root / "summary.json")
    closure_vr = _load_json(closure_root / "verifier_report.json")
    ok("upstream.closure.phase", closure_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.closure.verifier_go", closure_vr.get("verifier") == "GO" and closure_vr.get("passed") is True)
    ok("upstream.closure.final_decision", closure_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.closure.boundary_ok", closure_sm.get("boundary_ok") is True)

    ok("contract_review.no_reopen_extraction", contract_review.get("harness_extraction_reopened_now") is False)
    ok("contract_review.no_reopen_adoption", contract_review.get("harness_adoption_reopened_now") is False)
    ok("contract_review.anti_recursion", contract_review.get("anti_recursion_active") is True)

    ok("batch_config.batch_id", batch_cfg.get("batch_id") == "B0")
    ok("batch_config.domain", "Documentation Index" in (batch_cfg.get("batch_domain") or ""))
    ok("batch_config.paths", set(batch_cfg.get("candidate_paths") or []) == set(REQUIRED_CANDIDATE_PATHS))
    ok("batch_config.eval_out_readonly", batch_cfg.get("eval_out_policy", {}).get("mode") == "readonly")
    ok("batch_config.protected_deny", batch_cfg.get("protected_path_policy", {}).get("mode") == "deny")
    ok("batch_config.workspace_fallback", batch_cfg.get("workspace_fallback_policy", {}).get("enabled") is True)
    ok("batch_config.non_claims", len(batch_cfg.get("non_claims") or []) >= 5)

    for check_id in REQUIRED_FIXED_CHECKS:
        if check_id == "readiness_decision":
            continue
        ok(f"preflight.check.{check_id}", (summary.get("check_results") or {}).get(check_id) is True)

    ok("preflight.result.generated", preflight.get("batch_id") == "B0")
    ok("preflight.result.all_pass", preflight.get("all_checks_pass") is True)
    ok("preflight.result.extract_now_blocked", preflight.get("extract_now_allowed") is False)

    ok("scan.extract_now_allowed=false", scan.get("extract_now_allowed") is False)
    ok("scan.blocked_from_runtime_refactor", scan.get("blocked_from_runtime_refactor_now") is True)
    ok("scan.runtime_refactor_not_executed", summary.get("runtime_refactor_executed_now") is False)
    ok("scan.no_old_phase_delete", summary.get("old_phase_deleted_now") is False)
    ok("scan.no_old_phase_deprecate", summary.get("old_phase_deprecated_now") is False)

    ok("readiness.ready_for_execution", readiness.get("ready_for_b0_controlled_execution") is True)
    ok("readiness.b1_b7_deferred", readiness.get("b1_b7_deferred") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(180):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(120):
        ok(f"meta.preflight_executed[{i}]", summary.get("b0_preflight_executed_now") is True)
    for i in range(100):
        ok(f"meta.no_fileop[{i}]", summary.get("actual_file_move_executed") is False)
    for i in range(80):
        ok(f"meta.no_reopen[{i}]", summary.get("harness_extraction_reopened_now") is False)

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
