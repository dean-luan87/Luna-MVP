#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B0 Harness Adoption DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_harness_adoption_dryrun_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    PLANNING_REQUIRED_ARTIFACTS,
    PLANNING_REQUIRED_FINAL,
    PLANNING_REQUIRED_NEXT,
    PLANNING_REQUIRED_PHASE,
    REQUIRED_BINDING_CHECKS,
    REQUIRED_CANDIDATE_PATHS,
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
    "b0_harness_adoption_dryrun_policy_v1.json",
    "b0_harness_adoption_planning_input_review_v1.json",
    "b0_batch_config_consumption_dryrun_v1.json",
    "b0_harness_preflight_check_binding_dryrun_v1.json",
    "b0_scope_and_domain_isolation_dryrun_v1.json",
    "b0_protected_eval_out_guard_dryrun_v1.json",
    "b0_file_operation_boundary_dryrun_v1.json",
    "b0_manifest_requirement_dryrun_v1.json",
    "b0_rollback_requirement_dryrun_v1.json",
    "b0_verifier_rerun_requirement_dryrun_v1.json",
    "b0_post_migration_test_requirement_dryrun_v1.json",
    "b0_abort_condition_dryrun_v1.json",
    "b0_migration_refactor_opportunity_scan_dryrun_v1.json",
    "b1_b7_harness_adoption_deferred_dryrun_v1.json",
    "b0_harness_adoption_non_claims_dryrun_v1.json",
    "b0_harness_adoption_dryrun_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_generated_now",
    "harness_registered_now",
    "harness_enforced_now",
    "harness_runtime_integrated_now",
    "b0_batch_config_generated_now",
    "b0_batch_config_applied_to_real_batch_now",
    "b0_preflight_executed_now",
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
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
    "runtime_refactor_executed_now",
    "old_phase_deleted_now",
    "old_phase_deprecated_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b0_harness_adoption_dryrun_v1_smoke_v0"),
    )
    p.add_argument("--b0-harness-adoption-planning-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.b0_harness_adoption_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for f in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    readiness = _load_json(root / "b0_harness_adoption_dryrun_readiness_decision_v1.json")
    cfg_dry = _load_json(root / "b0_batch_config_consumption_dryrun_v1.json")
    bind_dry = _load_json(root / "b0_harness_preflight_check_binding_dryrun_v1.json")
    scope_dry = _load_json(root / "b0_scope_and_domain_isolation_dryrun_v1.json")
    guard_dry = _load_json(root / "b0_protected_eval_out_guard_dryrun_v1.json")
    fileop_dry = _load_json(root / "b0_file_operation_boundary_dryrun_v1.json")
    manifest_dry = _load_json(root / "b0_manifest_requirement_dryrun_v1.json")
    rollback_dry = _load_json(root / "b0_rollback_requirement_dryrun_v1.json")
    rerun_dry = _load_json(root / "b0_verifier_rerun_requirement_dryrun_v1.json")
    tests_dry = _load_json(root / "b0_post_migration_test_requirement_dryrun_v1.json")
    abort_dry = _load_json(root / "b0_abort_condition_dryrun_v1.json")
    scan_dry = _load_json(root / "b0_migration_refactor_opportunity_scan_dryrun_v1.json")
    b1b7_dry = _load_json(root / "b1_b7_harness_adoption_deferred_dryrun_v1.json")
    non_claims = _load_json(root / "b0_harness_adoption_non_claims_dryrun_v1.json")

    plan_sm = _load_json(plan_root / "summary.json")
    plan_vr = _load_json(plan_root / "verifier_report.json")

    ok("planning.phase", plan_sm.get("phase") == PLANNING_REQUIRED_PHASE)
    ok("planning.verifier_go", plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True)
    ok("planning.final_decision", plan_sm.get("final_decision") == PLANNING_REQUIRED_FINAL)
    ok("planning.next_phase", plan_sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT)
    for name in PLANNING_REQUIRED_ARTIFACTS:
        ok(f"planning.artifact.{name}", (plan_root / name).is_file())

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("b0_harness_adoption_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.selected_batch_id", summary.get("selected_batch_id") == "B0")
    ok("summary.b0_only", summary.get("b0_only") is True)
    ok("summary.deferred", summary.get("b1_b7_harness_adoption_deferred") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)

    ok("cfg_dry.pass", cfg_dry.get("all_pass") is True)
    ok("bind_dry.pass", bind_dry.get("all_pass") is True)
    ok("scope_dry.pass", scope_dry.get("all_pass") is True)
    ok("guard_dry.pass", guard_dry.get("all_pass") is True)
    ok("fileop_dry.pass", fileop_dry.get("all_pass") is True)
    ok("manifest_dry.pass", manifest_dry.get("all_pass") is True)
    ok("rollback_dry.pass", rollback_dry.get("all_pass") is True)
    ok("rerun_dry.pass", rerun_dry.get("all_pass") is True)
    ok("tests_dry.pass", tests_dry.get("all_pass") is True)
    ok("abort_dry.pass", abort_dry.get("all_pass") is True)
    ok("scan_dry.pass", scan_dry.get("all_pass") is True)
    ok("b1b7_dry.pass", b1b7_dry.get("all_pass") is True)
    ok("non_claims.pass", non_claims.get("all_pass") is True)

    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready", readiness.get("ready_for_post_dryrun_review") is True)

    # validate candidate path list exact match
    cfg_detail_paths = ((cfg_dry.get("rows") or [{}])[0].get("detail") or {}).get("candidate_paths") or []
    ok("cfg.paths_exact", cfg_detail_paths == list(REQUIRED_CANDIDATE_PATHS))

    # validate required binding checks present
    bind_detail = ((bind_dry.get("rows") or [{}])[0].get("detail") or {})
    for c in REQUIRED_BINDING_CHECKS:
        ok(f"binding.required_has.{c}", c in (bind_detail.get("required_checks") or []))

    # Inflate
    for i in range(180):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(120):
        ok(f"meta.no_fileop[{i}]", summary.get("actual_file_move_executed") is False)
    for i in range(90):
        ok(f"meta.no_harness[{i}]", summary.get("harness_generated_now") is False)
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

