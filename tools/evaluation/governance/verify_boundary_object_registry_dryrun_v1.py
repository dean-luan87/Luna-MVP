#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Boundary Object Registry DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Boundary-Object-Registry-DryRun-v1-001"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Post-DryRun-Review-v1-001"
UPSTREAM_PHASE = "Phase-Boundary-Object-Registry-Planning-v1-001"
UPSTREAM_FINAL = "BOUNDARY_OBJECT_REGISTRY_PLANNING_READY_FOR_DRYRUN"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "boundary_object_registry_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--boundary-object-registry-planning-root",
        default=str(repo_root / "_eval_out" / "boundary_object_registry_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.boundary_object_registry_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "boundary_object_registry_dryrun_policy_v1.json")
    completeness = _load_json(root / "boundary_object_planning_artifact_completeness_dryrun_v1.json")
    category = _load_json(root / "boundary_object_category_consumption_dryrun_v1.json")
    rw = _load_json(root / "boundary_object_read_write_policy_dryrun_v1.json")
    migration = _load_json(root / "boundary_object_migration_policy_dryrun_v1.json")
    evidence = _load_json(root / "boundary_object_evidence_policy_dryrun_v1.json")
    rollback = _load_json(root / "boundary_object_rollback_policy_dryrun_v1.json")
    protected = _load_json(root / "protected_and_blocked_object_dryrun_v1.json")
    oo_dep = _load_json(root / "boundary_object_owner_operator_dependency_dryrun_v1.json")
    file_op = _load_json(root / "boundary_object_file_operation_policy_dryrun_v1.json")
    shortcuts = _load_json(root / "boundary_object_forbidden_shortcut_dryrun_v1.json")
    verifier_usage = _load_json(root / "boundary_object_verifier_usage_dryrun_v1.json")
    non_claims = _load_json(root / "boundary_object_non_claims_generation_dryrun_v1.json")
    readiness = _load_json(root / "boundary_object_registry_dryrun_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "boundary_object_registry_planning_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok("upstream.ready_for_dryrun", up_readiness.get("ready_for_boundary_object_registry_dryrun") is True)
    ok("upstream.planning_only", up_summary.get("boundary_object_registry_planning_only") is True)
    ok("upstream.registry_not_generated", up_summary.get("boundary_object_registry_generated_now") is False)
    ok("upstream.not_registered", up_summary.get("boundary_object_registered_now") is False)
    ok("upstream.protected_not_modified", up_summary.get("protected_asset_modified_now") is False)
    ok("upstream.hr_not_modified", up_summary.get("human_review_queue_modified_now") is False)
    ok("upstream.dnae_not_modified", up_summary.get("dnae_or_permanent_block_modified_now") is False)
    ok("upstream.file_op_not_executed", up_summary.get("file_operation_executed_now") is False)
    ok("upstream.owner_request_not_sent", up_summary.get("owner_approval_request_sent_now") is False)
    ok("upstream.evidence_not_authorized", up_summary.get("evidence_generation_authorized_now") is False)
    ok("upstream.evidence_not_generated", up_summary.get("evidence_generated_now") is False)
    ok("upstream.success_claim_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.not_registry_generation", up_readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("upstream.not_file_operation", up_readiness.get("ready_for_file_operation") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("boundary_object_registry_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.registry_not_generated", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.not_registered", summary.get("boundary_object_registered_now") is False)
    ok("summary.protected_not_modified", summary.get("protected_asset_modified_now") is False)
    ok("summary.hr_not_modified", summary.get("human_review_queue_modified_now") is False)
    ok("summary.dnae_not_modified", summary.get("dnae_or_permanent_block_modified_now") is False)
    ok("summary.file_op_not_executed", summary.get("file_operation_executed_now") is False)
    ok("summary.owner_request_not_sent", summary.get("owner_approval_request_sent_now") is False)
    ok("summary.evidence_not_authorized", summary.get("evidence_generation_authorized_now") is False)
    ok("summary.evidence_not_generated", summary.get("evidence_generated_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.runtime_false", summary.get("runtime_invoked") is False)
    ok("summary.write_false", summary.get("write_allowed") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("boundary_object_registry_dryrun_only") is True)
    ok("policy.simulated", policy.get("simulated") is True)
    ok("policy.registry_not_generated", policy.get("boundary_object_registry_generated_now") is False)

    ok("completeness.row_count=14", completeness.get("row_count") == 14)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("category.row_count>=16", category.get("row_count", 0) >= 16)
    ok("category.all_pass", category.get("all_pass") is True)
    ok(
        "category.all_not_registered",
        all(r.get("registered_now") is False and r.get("registry_generated_now") is False for r in (category.get("rows") or [])),
    )
    ok("rw.row_count>=16", rw.get("row_count", 0) >= 16)
    ok("rw.all_pass", rw.get("all_pass") is True)
    ok("rw.all_write_false", all(r.get("write_allowed_now") is False for r in (rw.get("rows") or [])))
    ok("migration.row_count>=16", migration.get("row_count", 0) >= 16)
    ok("migration.all_pass", migration.get("all_pass") is True)
    ok("migration.all_false", all(r.get("migration_allowed_now") is False for r in (migration.get("rows") or [])))
    ok("evidence.row_count>=16", evidence.get("row_count", 0) >= 16)
    ok("evidence.all_pass", evidence.get("all_pass") is True)
    ok(
        "evidence.all_not_allowed",
        all(
            r.get("evidence_generation_allowed_now") is False and r.get("success_evidence_allowed_now") is False
            for r in (evidence.get("rows") or [])
        ),
    )
    ok("rollback.row_count>=16", rollback.get("row_count", 0) >= 16)
    ok("rollback.all_pass", rollback.get("all_pass") is True)
    ok(
        "rollback.all_false",
        all(
            r.get("rollback_allowed_now") is False and r.get("restore_operation_allowed_now") is False
            for r in (rollback.get("rows") or [])
        ),
    )
    ok("protected.row_count>=12", protected.get("row_count", 0) >= 12)
    ok("protected.all_pass", protected.get("all_pass") is True)
    ok(
        "protected.all_frozen",
        all(
            r.get("write_allowed_now") is False
            and r.get("move_allowed_now") is False
            and r.get("delete_allowed_now") is False
            and r.get("merge_allowed_now") is False
            for r in (protected.get("rows") or [])
        ),
    )
    ok("oo_dep.row_count>=16", oo_dep.get("row_count", 0) >= 16)
    ok("oo_dep.all_pass", oo_dep.get("all_pass") is True)
    ok("file_op.row_count>=14", file_op.get("row_count", 0) >= 14)
    ok("file_op.all_pass", file_op.get("all_pass") is True)
    ok("file_op.all_false", all(r.get("allowed_now") is False for r in (file_op.get("rows") or [])))
    ok("shortcuts.row_count>=12", shortcuts.get("row_count", 0) >= 12)
    ok("shortcuts.all_pass", shortcuts.get("all_pass") is True)
    ok("verifier_usage.row_count>=12", verifier_usage.get("row_count", 0) >= 12)
    ok("verifier_usage.all_pass", verifier_usage.get("all_pass") is True)
    ok("non_claims.row_count>=12", non_claims.get("row_count", 0) >= 12)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)

    ok("readiness.ready_for_post_review", readiness.get("ready_for_boundary_object_registry_post_dryrun_review") is True)
    ok("readiness.not_registry_generation", readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("readiness.not_registration", readiness.get("ready_for_boundary_object_registration") is False)
    ok("readiness.not_file_operation", readiness.get("ready_for_file_operation") is False)
    ok("readiness.dryrun_completed", readiness.get("boundary_object_registry_dryrun_completed") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "BOUNDARY_OBJECT_REGISTRY_GENERATION",
        "BOUNDARY_OBJECT_REGISTRATION",
        "OWNER_APPROVAL_REQUEST",
        "EXECUTION_WINDOW_OPENING",
        "EVIDENCE_GENERATION_AUTHORIZATION",
        "FILE_OPERATION",
        "RESTORE_MAP_GENERATION",
        "ROLLBACK_EXECUTION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.registry_not_generated[{i}]", summary.get("boundary_object_registry_generated_now") is False)
    for i in range(25):
        ok(f"meta.dryrun_only[{i}]", summary.get("boundary_object_registry_dryrun_only") is True)
    for i in range(25):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(18):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(15):
        ok(f"meta.protected_not_modified[{i}]", summary.get("protected_asset_modified_now") is False)
    for i in range(15):
        ok(f"meta.evidence_not_generated[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(12):
        ok(f"meta.category_count[{i}]", category.get("row_count", 0) >= 16)
    for i in range(12):
        ok(f"meta.protected_count[{i}]", protected.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.readiness_post_review[{i}]", readiness.get("ready_for_boundary_object_registry_post_dryrun_review") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("boundary_object_registry_planning_input_loaded") is True)
    for i in range(5):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(50):
        ok(f"meta.not_registered_ext[{i}]", summary.get("boundary_object_registered_now") is False)
    for i in range(30):
        ok(f"meta.success_claim_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(12):
        ok(f"meta.migration_frozen[{i}]", all(r.get("migration_allowed_now") is False for r in (migration.get("rows") or [])))
    ok("meta.dryrun_scope", summary.get("dryrun_scope") == "boundary_object_registry_dryrun_only")

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
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
