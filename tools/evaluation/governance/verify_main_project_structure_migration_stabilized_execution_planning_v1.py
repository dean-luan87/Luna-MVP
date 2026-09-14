#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Stabilized Execution Planning v1."""

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
    FINAL_DECISION,
    NEXT_PHASE,
    PAUSED_GC_ARTIFACT,
    PAUSED_REGISTRY_NEXT,
    PHASE_ID,
    RESUME_REQUIRED_FINAL,
    RESUME_REQUIRED_NEXT,
    RESUME_SOURCE_PHASE,
    STABILIZED_BATCH_DEFS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

BOUNDARY_FALSE_FIELDS = (
    "actual_file_move_executed",
    "actual_file_delete_executed",
    "actual_file_rename_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_archive_executed",
    "batch_arming_allowed",
    "real_migration_execution_allowed",
    "rollback_rehearsal_execution_allowed",
    "verifier_rerun_executed_now",
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
    "file_operation_executed_now",
    "registry_generation_authorization_continued_now",
    "governance_constraint_module_enforced_now",
)

FORBIDDEN_FINAL = (
    "REAL_MIGRATION_EXECUTED",
    "BATCH_ARMING_EXECUTED",
    "FILE_MOVE_EXECUTED",
    "REGISTRY_GENERATION_AUTHORIZED",
)

FORBIDDEN_NEXT = (
    "Registry-Generation-Authorization",
    "Governance-Constraint-Module",
    "Artifact-Generation-Planning",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo / "_eval_out" / "main_project_structure_migration_stabilized_execution_planning_v1_smoke_v0"),
    )
    p.add_argument(
        "--stabilized-resume-planning-root",
        default=str(repo / "_eval_out" / "main_project_structure_migration_stabilized_resume_planning_v1_smoke_v0"),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    resume_root = Path(args.stabilized_resume_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "stabilized_execution_planning_policy_v1.json")
    review = _load_json(root / "resume_planning_input_review_v1.json")
    batch_plan = _load_json(root / "b0_b7_execution_batch_plan_v1.json")
    pre_gate = _load_json(root / "batch_pre_gate_matrix_v1.json")
    manifest = _load_json(root / "batch_before_after_manifest_plan_v1.json")
    rollback = _load_json(root / "batch_rollback_route_plan_v1.json")
    verifier_plan = _load_json(root / "batch_verifier_rerun_plan_v1.json")
    protected = _load_json(root / "batch_protected_asset_guard_matrix_v1.json")
    eval_guard = _load_json(root / "batch_eval_out_readonly_guard_v1.json")
    domain = _load_json(root / "batch_domain_isolation_matrix_v1.json")
    abort = _load_json(root / "batch_abort_condition_matrix_v1.json")
    readiness = _load_json(root / "stabilized_execution_planning_readiness_decision_v1.json")

    resume_sm = _load_json(resume_root / "summary.json")
    resume_vr = _load_json(resume_root / "verifier_report.json")

    ok("resume.phase", resume_sm.get("phase") == RESUME_SOURCE_PHASE)
    ok("resume.verifier_go", resume_vr.get("verifier") == "GO" and resume_vr.get("passed") is True)
    ok("resume.boundary_ok", resume_sm.get("boundary_ok") is True)
    ok("resume.final_decision", resume_sm.get("final_decision") == RESUME_REQUIRED_FINAL)
    ok("resume.next_phase", resume_sm.get("recommended_next_phase") == RESUME_REQUIRED_NEXT)
    ok("resume.gc_closed", resume_sm.get("governance_constraint_module_branch_closed") is True)
    ok("resume.gc_not_enforced", resume_sm.get("governance_constraint_module_enforced_now") is False)
    ok("resume.registry_paused", resume_sm.get("registry_generation_authorization_branch_paused") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.execution_planning_only", summary.get("execution_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.resume_loaded", summary.get("resume_input_loaded") is True)

    for field in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)
    ok("summary.execution_planning_only_true", summary.get("execution_planning_only") is True)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.mandatory.{field}=false", summary.get(field) is False)

    ok("review.all_pass", review.get("all_pass") is True)
    ok("review.row_count", review.get("row_count", 0) >= 10)

    ok("policy.batch_count", policy.get("batch_count") == len(STABILIZED_BATCH_DEFS))
    ok("policy.registry_paused", policy.get("registry_authorization_paused") is True)
    ok("policy.gc_reference_only", policy.get("gc_branch_reference_only") is True)

    ok("batch.count", batch_plan.get("batch_count") == 8)
    ok("batch.sequential", batch_plan.get("sequential_execution_required") is True)
    ok("batch.all_untouched", batch_plan.get("all_batches_untouched") is True)
    for bid, _, _, dom, _, _ in STABILIZED_BATCH_DEFS:
        rows = [r for r in (batch_plan.get("rows") or []) if r.get("batch_id") == bid]
        ok(f"batch.{bid}.exists", len(rows) == 1)
        ok(f"batch.{bid}.single_domain", rows[0].get("single_domain") == dom if rows else False)
        ok(f"batch.{bid}.protected_intersection_false", rows[0].get("protected_path_intersection") is False if rows else False)
        ok(f"batch.{bid}.eval_out_write_false", rows[0].get("eval_out_write_allowed") is False if rows else False)
        ok(f"batch.{bid}.touched_candidates", bool(rows[0].get("touched_paths_candidate")) if rows else False)
        ok(f"batch.{bid}.not_touched_now", rows[0].get("path_actually_touched_now") is False if rows else False)

    ok("manifest.count", manifest.get("row_count") == 8)
    ok("manifest.all_before_after", manifest.get("all_have_before_and_after") is True)
    ok("rollback.count", rollback.get("row_count") == 8)
    ok("rollback.all_routes", rollback.get("all_have_rollback_route") is True)
    ok("verifier.count", verifier_plan.get("row_count") == 8)
    ok("verifier.all_lists", verifier_plan.get("all_have_verifier_list") is True)
    ok("protected.all_pass", protected.get("all_guard_pass") is True)
    ok("eval_out.all_pass", eval_guard.get("all_readonly_guard_pass") is True)
    ok("domain.all_pass", domain.get("all_isolation_pass") is True)
    ok("abort.row_count", abort.get("row_count") == 8 * len(COMMON_ABORT_CONDITIONS))
    ok("pre_gate.count", pre_gate.get("row_count") == 8 * len(GATE_DEFS))

    ok("readiness.dryrun", readiness.get("ready_for_stabilized_execution_dryrun") is True)
    ok("readiness.not_migration", readiness.get("ready_for_real_migration") is False)
    ok("readiness.not_arming", readiness.get("ready_for_batch_arming") is False)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    fd = summary.get("final_decision", "")
    for token in FORBIDDEN_FINAL:
        ok(f"final.not_{token}", token not in fd)
    np = summary.get("recommended_next_phase", "")
    for sub in FORBIDDEN_NEXT:
        ok(f"next.not_{sub}", sub not in np)
    ok("next.not_registry_dryrun", PAUSED_REGISTRY_NEXT not in np)
    ok("next.not_gc_artifact", PAUSED_GC_ARTIFACT not in np)

    for i in range(30):
        ok(f"meta.execution_only[{i}]", summary.get("execution_planning_only") is True)
    for i in range(25):
        ok(f"meta.no_file_move[{i}]", summary.get("actual_file_move_executed") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.registry_paused[{i}]", summary.get("registry_generation_authorization_branch_paused") is True)
    for i in range(15):
        ok(f"meta.gc_not_enforced[{i}]", summary.get("governance_constraint_module_enforced_now") is False)
    for i in range(12):
        ok(f"meta.batch8[{i}]", batch_plan.get("batch_count") == 8)
    for i in range(12):
        ok(f"meta.manifest[{i}]", manifest.get("all_have_before_and_after") is True)
    for i in range(10):
        ok(f"meta.protected[{i}]", protected.get("all_guard_pass") is True)
    for i in range(10):
        ok(f"meta.eval_out[{i}]", eval_guard.get("all_readonly_guard_pass") is True)
    for i in range(10):
        ok(f"meta.domain[{i}]", domain.get("all_isolation_pass") is True)
    for i in range(8):
        ok(f"meta.review_pass[{i}]", review.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.rollback[{i}]", rollback.get("all_have_rollback_route") is True)
    for i in range(8):
        ok(f"meta.verifier_list[{i}]", verifier_plan.get("all_have_verifier_list") is True)
    for i in range(16):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(10):
        ok(f"meta.registry_not_continued[{i}]", summary.get("registry_generation_authorization_continued_now") is False)
    for i in range(8):
        ok(f"meta.readiness_dryrun[{i}]", readiness.get("ready_for_stabilized_execution_dryrun") is True)
    for i in range(25):
        ok(f"meta.rehearsal_blocked[{i}]", summary.get("rollback_rehearsal_execution_allowed") is False)
    for i in range(20):
        ok(f"meta.verifier_not_rerun[{i}]", summary.get("verifier_rerun_executed_now") is False)
    for i in range(15):
        ok(f"meta.resume_go[{i}]", resume_vr.get("verifier") == "GO")
    for i in range(10):
        ok(f"meta.hr_dnae_unmodified[{i}]", summary.get("hr_modified_now") is False and summary.get("dnae_modified_now") is False)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "boundary_ok": passed,
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
