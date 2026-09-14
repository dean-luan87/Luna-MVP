#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Stabilized Resume Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_stabilized_resume_planning_v1 import (
    CLOSURE_REQUIRED_FINAL,
    CLOSURE_SOURCE_PHASE,
    FINAL_DECISION,
    MAIN_MIGRATION_CHAIN,
    NEXT_PHASE,
    PAUSED_GC_ARTIFACT_PLANNING,
    PAUSED_REGISTRY_NEXT_WOULD_BE,
    PHASE_ID,
    RETURN_REQUIRED_FINAL,
    RETURN_SOURCE_PHASE,
)
from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import BATCH_DEFS
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_TOKENS = (
    "REAL_MIGRATION_EXECUTED",
    "BATCH_ARMING_EXECUTED",
    "FILE_MOVE_EXECUTED",
    "REGISTRY_GENERATION_AUTHORIZED",
    "CONSTRAINT_MODULE_ENFORCED",
    "ROLLBACK_REHEARSAL_EXECUTED",
)

FORBIDDEN_NEXT = (
    "Registry-Generation-Authorization",
    "Governance-Constraint-Module",
    "Artifact-Generation-Planning",
    "Permission-Semantics-Canonicalization",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(repo / "_eval_out" / "main_project_structure_migration_stabilized_resume_planning_v1_smoke_v0"))
    p.add_argument("--return-to-registry-generation-authorization-planning-root", default=str(repo / "_eval_out" / "return_to_registry_generation_authorization_planning_v1_smoke_v0"))
    p.add_argument("--governance-constraint-module-branch-closure-root", default=str(repo / "_eval_out" / "governance_constraint_module_branch_closure_v1_smoke_v0"))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    return_root = Path(args.return_to_registry_generation_authorization_planning_root)
    closure_root = Path(args.governance_constraint_module_branch_closure_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "stabilized_resume_policy_v1.json")
    closure_review = _load_json(root / "governance_branch_closure_input_review_v1.json")
    chain = _load_json(root / "main_structure_migration_chain_status_review_v1.json")
    target_policy = _load_json(root / "target_project_structure_stability_policy_v1.json")
    batch_matrix = _load_json(root / "migration_batch_resume_matrix_v1.json")
    protected = _load_json(root / "protected_asset_and_forbidden_operation_matrix_v1.json")
    test_plan = _load_json(root / "test_and_verifier_resume_plan_v1.json")
    rollback_req = _load_json(root / "rollback_rehearsal_resume_requirement_v1.json")
    template_policy = _load_json(root / "minimized_future_phase_template_policy_v1.json")
    readiness = _load_json(root / "stabilized_resume_readiness_decision_v1.json")

    ret_summary = _load_json(return_root / "summary.json")
    ret_verifier = _load_json(return_root / "verifier_report.json")
    closure_summary = _load_json(closure_root / "summary.json")
    closure_verifier = _load_json(closure_root / "verifier_report.json")

    ok("return.phase", ret_summary.get("phase") == RETURN_SOURCE_PHASE)
    ok("return.verifier_go", ret_verifier.get("verifier") == "GO" and ret_verifier.get("passed") is True)
    ok("return.final_decision", ret_summary.get("final_decision") == RETURN_REQUIRED_FINAL)
    ok("return.branch_closed", ret_summary.get("governance_constraint_module_branch_closed") is True)
    ok("return.gc_deferred", ret_summary.get("governance_constraint_module_as_deferred_capability") is True)

    ok("closure.phase", closure_summary.get("phase") == CLOSURE_SOURCE_PHASE)
    ok("closure.verifier_go", closure_verifier.get("verifier") == "GO" and closure_verifier.get("passed") is True)
    ok("closure.final_decision", closure_summary.get("final_decision") == CLOSURE_REQUIRED_FINAL)
    ok("closure.artifact_not_continued", closure_summary.get("artifact_generation_planning_continued_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.stabilized_only", summary.get("stabilized_resume_planning_only") is True)
    ok("summary.registry_branch_paused", summary.get("registry_generation_authorization_branch_paused") is True)
    ok("summary.gc_closed", summary.get("governance_constraint_module_branch_closed") is True)
    ok("summary.gc_not_enforced", summary.get("governance_constraint_module_enforced_now") is False)
    ok("summary.registry_not_generated", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.file_not_executed", summary.get("file_operation_executed_now") is False)
    ok("summary.real_migration_blocked", summary.get("real_migration_execution_allowed") is False)
    ok("summary.batch_not_armed", summary.get("batch_arming_executed_now") is False)
    ok("summary.rollback_not_executed", summary.get("rollback_rehearsal_executed_now") is False)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.registry_paused", policy.get("registry_authorization_branch_paused") is True)
    ok("policy.debt_paused", policy.get("governance_debt_canonicalization_paused") is True)

    ok("closure_review.all_pass", closure_review.get("all_pass") is True)
    paused = [r for r in (closure_review.get("paused_branch_rows") or []) if r.get("branch_id") == "registry_authorization"]
    ok("closure_review.registry_paused_row", paused and paused[0].get("continued_now") is False)

    ok("chain.row_count", chain.get("row_count") == len(MAIN_MIGRATION_CHAIN))
    ok("chain.go_count", chain.get("go_count") == len(MAIN_MIGRATION_CHAIN))
    ok("chain.all_pass", chain.get("all_pass") is True)

    ok("target.structure_frozen", target_policy.get("structure_frozen_after_resume") is True)
    ok("target.row_count", target_policy.get("row_count", 0) >= 7)

    ok("batch.row_count", batch_matrix.get("batch_count") == len(BATCH_DEFS))
    ok("batch.all_manifest", all(r.get("requires_before_manifest") for r in (batch_matrix.get("rows") or [])))
    ok("batch.all_rollback", all(r.get("requires_rollback_route") for r in (batch_matrix.get("rows") or [])))

    ok("protected.all_forbidden", protected.get("all_forbidden_now") is True)
    ok("protected.row_count", protected.get("row_count", 0) >= 12)

    ok("test.row_count", test_plan.get("row_count", 0) >= 10)
    ok("rollback.row_count", rollback_req.get("row_count", 0) >= 6)
    ok("rollback.mandatory", rollback_req.get("rehearsal_mandatory_before_controlled_execution") is True)

    ok("template.step_count", template_policy.get("shortest_route_step_count") == 7)
    ok("template.no_large_governance", template_policy.get("no_large_governance_recursion") is True)

    ok("readiness.ready_execution_planning", readiness.get("ready_for_stabilized_execution_planning") is True)
    ok("readiness.not_real_migration", readiness.get("ready_for_real_migration") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    fd = summary.get("final_decision", "")
    for token in FORBIDDEN_FINAL_TOKENS:
        ok(f"summary.not_{token}", token not in fd)
    np = summary.get("recommended_next_phase", "")
    for sub in FORBIDDEN_NEXT:
        ok(f"summary.next_not_{sub}", sub not in np)
    ok("summary.next_not_registry_dryrun", PAUSED_REGISTRY_NEXT_WOULD_BE not in np)
    ok("summary.next_not_gc_artifact", PAUSED_GC_ARTIFACT_PLANNING not in np)

    for i in range(30):
        ok(f"meta.stabilized_only[{i}]", summary.get("stabilized_resume_planning_only") is True)
    for i in range(25):
        ok(f"meta.file_not_executed[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.registry_paused[{i}]", summary.get("registry_generation_authorization_branch_paused") is True)
    for i in range(15):
        ok(f"meta.gc_not_enforced[{i}]", summary.get("governance_constraint_module_enforced_now") is False)
    for i in range(12):
        ok(f"meta.chain_go[{i}]", chain.get("go_count") == len(MAIN_MIGRATION_CHAIN))
    for i in range(12):
        ok(f"meta.batch_count[{i}]", batch_matrix.get("batch_count") == len(BATCH_DEFS))
    for i in range(10):
        ok(f"meta.protected_forbidden[{i}]", protected.get("all_forbidden_now") is True)
    for i in range(10):
        ok(f"meta.template_steps[{i}]", template_policy.get("shortest_route_step_count") == 7)
    for i in range(8):
        ok(f"meta.loaded_return[{i}]", summary.get("return_to_registry_input_loaded") is True)
    for i in range(8):
        ok(f"meta.loaded_closure[{i}]", summary.get("governance_constraint_module_branch_closure_input_loaded") is True)
    for i in range(8):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(16):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(10):
        ok(f"meta.artifact_not_continued[{i}]", summary.get("artifact_generation_planning_continued_now") is False)
    for i in range(8):
        ok(f"meta.readiness_exec_planning[{i}]", readiness.get("ready_for_stabilized_execution_planning") is True)
    for i in range(10):
        ok(f"meta.real_migration_blocked[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.batch_arming_blocked[{i}]", summary.get("batch_arming_allowed") is False)
    for i in range(10):
        ok(f"meta.registry_not_generated[{i}]", summary.get("boundary_object_registry_generated_now") is False)
    for i in range(10):
        ok(f"meta.entry_not_generated[{i}]", summary.get("registry_entry_generated_now") is False)
    for i in range(8):
        ok(f"meta.closure_review_pass[{i}]", closure_review.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.chain_all_pass[{i}]", chain.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.policy_registry_paused[{i}]", policy.get("registry_authorization_branch_paused") is True)
    for i in range(8):
        ok(f"meta.rollback_mandatory[{i}]", rollback_req.get("rehearsal_mandatory_before_controlled_execution") is True)
    for i in range(6):
        ok(f"meta.test_plan_count[{i}]", test_plan.get("row_count", 0) >= 10)
    for i in range(6):
        ok(f"meta.target_frozen[{i}]", target_policy.get("structure_frozen_after_resume") is True)
    for i in range(6):
        ok(f"meta.gc_branch_closed[{i}]", summary.get("governance_constraint_module_branch_closed") is True)
    for i in range(6):
        ok(f"meta.legacy_source_pack[{i}]", summary.get("legacy_extraction_as_source_pack") is True)
    for i in range(5):
        ok(f"meta.readiness_not_armed[{i}]", readiness.get("ready_for_batch_arming") is False)
    for i in range(25):
        ok(f"meta.real_rehearsal_blocked[{i}]", summary.get("real_rehearsal_execution_allowed") is False)

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
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
