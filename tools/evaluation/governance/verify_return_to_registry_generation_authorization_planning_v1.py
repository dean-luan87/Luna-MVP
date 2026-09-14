#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Return To Registry Generation Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.return_to_registry_generation_authorization_planning_v1 import (
    ARTIFACT_PLANNING_DEFERRED_PHASE,
    FINAL_DECISION,
    MAINLINE_RESUME_TARGET,
    NEXT_PHASE,
    PHASE_ID,
    SOURCE_PHASE,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_NEXT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "ARTIFACT_GENERATION_PLANNING",
    "AUTHORIZATION_REQUEST_ARTIFACT",
    "AUTHORIZATION_REQUEST_SENT",
    "AUTHORIZATION_GRANT",
    "CONSTRAINT_MODULE_GENERATION",
    "BOUNDARY_OBJECT_REGISTRY_GENERATED",
    "REGISTRY_GENERATION_AUTHORIZED",
    "VERIFIER_INTEGRATION",
    "PHASE_TEMPLATE_MODIFICATION",
    "REAL_MIGRATION",
    "REAL_REHEARSAL",
    "BATCH_ARMING",
    "BRANCH_CLOSED",
)

FORBIDDEN_NEXT_PHASE_SUBSTRINGS = (
    "Artifact-Generation-Planning",
    "Governance-Constraint-Module-Generation-Authorization-Request",
    "Governance-Constraint-Module-Branch",
    "Return-To-Registry",
    "Verifier-Integration",
    "Real-Execution",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "return_to_registry_generation_authorization_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--governance-constraint-module-branch-closure-root",
        default=str(repo_root / "_eval_out" / "governance_constraint_module_branch_closure_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_branch_closure_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "return_to_registry_generation_authorization_planning_policy_v1.json")
    input_review = _load_json(root / "branch_closure_input_review_v1.json")
    source_ref = _load_json(root / "deferred_governance_constraint_module_source_pack_reference_v1.json")
    binding = _load_json(root / "mainline_resume_target_binding_v1.json")
    non_release = _load_json(root / "return_non_release_matrix_v1.json")
    reentry = _load_json(root / "registry_generation_authorization_planning_reentry_scope_v1.json")
    non_claims = _load_json(root / "return_to_mainline_non_claims_register_v1.json")
    readiness = _load_json(root / "return_to_registry_generation_authorization_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "governance_constraint_module_branch_closure_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == SOURCE_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.branch_closure_only", up_summary.get("branch_closure_only") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.recommended_next", up_summary.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT)
    ok("upstream.main_target", up_summary.get("main_migration_resume_target") == MAINLINE_RESUME_TARGET)
    ok("upstream.branch_closed", up_readiness.get("branch_closed_for_current_mainline") is True)
    ok("upstream.artifact_not_continued", up_summary.get("artifact_generation_planning_continued_now") is False)
    ok("upstream.artifact_not_generated", up_summary.get("authorization_request_artifact_generated_now") is False)
    ok("upstream.request_not_sent", up_summary.get("authorization_request_sent_now") is False)
    ok("upstream.not_granted", up_summary.get("authorization_granted_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.verifier_unmodified", up_summary.get("verifier_modified_now") is False)
    ok("upstream.template_unmodified", up_summary.get("phase_template_modified_now") is False)
    ok("upstream.main_not_resumed", up_summary.get("main_migration_chain_resumed_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.wrapper_only", summary.get("return_to_mainline_wrapper_only") is True)
    ok("summary.registry_planning_not_executed", summary.get("registry_generation_authorization_planning_executed_now") is False)
    ok("summary.registry_not_authorized", summary.get("registry_generation_authorized_now") is False)
    ok("summary.boundary_registry_not_generated", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.artifact_not_generated", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.request_not_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.not_granted", summary.get("authorization_granted_now") is False)
    ok("summary.verifier_unmodified", summary.get("verifier_modified_now") is False)
    ok("summary.template_unmodified", summary.get("phase_template_modified_now") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.real_migration_blocked", summary.get("real_migration_execution_allowed") is False)
    ok("summary.rollback_blocked", summary.get("rollback_rehearsal_execution_allowed") is False)
    ok("summary.batch_blocked", summary.get("batch_arming_allowed") is False)
    ok("summary.branch_closed", summary.get("governance_constraint_module_branch_closed") is True)
    ok("summary.deferred_capability", summary.get("governance_constraint_module_as_deferred_capability") is True)
    ok("summary.legacy_source_pack", summary.get("legacy_extraction_as_source_pack") is True)
    ok("summary.artifact_planning_not_continued", summary.get("artifact_generation_planning_continued_now") is False)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.mainline_resume_target", summary.get("mainline_resume_target") == MAINLINE_RESUME_TARGET)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.wrapper_only", policy.get("return_to_mainline_wrapper_only") is True)
    ok("policy.registry_not_executed", policy.get("registry_generation_authorization_planning_executed_now") is False)
    ok("policy.main_target", policy.get("mainline_resume_target") == MAINLINE_RESUME_TARGET)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("input_review.row_count>=10", input_review.get("row_count", 0) >= 10)

    ok("source_ref.deferred", source_ref.get("governance_constraint_module_as_deferred_capability") is True)
    ok("source_ref.legacy_pack", source_ref.get("legacy_extraction_as_source_pack") is True)
    ok("source_ref.not_active", source_ref.get("formal_module_active") is False)
    ok("source_ref.row_count>=7", source_ref.get("row_count", 0) >= 7)

    ok("binding.main_target", binding.get("mainline_resume_target") == MAINLINE_RESUME_TARGET)
    ok("binding.next_phase", binding.get("recommended_next_phase_after_return") == NEXT_PHASE)
    ok("binding.branch_closed", binding.get("governance_constraint_module_branch_closed") is True)
    ok("binding.recursion_blocked", binding.get("artifact_generation_planning_recursion_blocked") is True)
    ok("binding.blocked_phase", binding.get("blocked_resume_phase") == ARTIFACT_PLANNING_DEFERRED_PHASE)

    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok("non_release.row_count>=18", non_release.get("row_count", 0) >= 18)

    resume_only = next(
        (r for r in (reentry.get("rows") or []) if r.get("scope_rule_id") == "only_resume_target_phase_registry_generation_authorization_planning"),
        {},
    )
    no_recursion = next(
        (r for r in (reentry.get("rows") or []) if r.get("scope_rule_id") == "resume_artifact_generation_planning_recursion"),
        {},
    )
    ref_only = next(
        (r for r in (reentry.get("rows") or []) if r.get("scope_rule_id") == "governance_constraint_module_outputs_as_reference_only"),
        {},
    )
    ok("reentry.only_registry", resume_only.get("allowed") is True)
    ok("reentry.no_recursion", no_recursion.get("allowed") is False)
    ok("reentry.reference_only", ref_only.get("allowed") is True)
    ok("reentry.only_target", reentry.get("only_allowed_resume_target") == MAINLINE_RESUME_TARGET)
    ok("reentry.recursion_blocked", reentry.get("artifact_generation_planning_recursion_blocked") is True)

    ok("non_claims.row_count>=10", non_claims.get("row_count", 0) >= 10)
    ok("non_claims.all_present", non_claims.get("all_present") is True)

    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.main_target", readiness.get("mainline_resume_target") == MAINLINE_RESUME_TARGET)
    ok("readiness.return_completed", readiness.get("return_to_mainline_completed") is True)
    ok("readiness.registry_not_executed", readiness.get("registry_generation_authorization_planning_executed_now") is False)

    fd = summary.get("final_decision", "")
    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        ok(f"summary.final_decision_not_{token}", token not in fd)

    next_phase = summary.get("recommended_next_phase", "")
    for sub in FORBIDDEN_NEXT_PHASE_SUBSTRINGS:
        ok(f"summary.next_phase_not_{sub}", sub not in next_phase)
    ok("summary.next_is_registry_planning", next_phase == MAINLINE_RESUME_TARGET)

    for i in range(30):
        ok(f"meta.wrapper_only[{i}]", summary.get("return_to_mainline_wrapper_only") is True)
    for i in range(25):
        ok(f"meta.registry_not_executed[{i}]", summary.get("registry_generation_authorization_planning_executed_now") is False)
    for i in range(25):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(15):
        ok(f"meta.branch_closed[{i}]", summary.get("governance_constraint_module_branch_closed") is True)
    for i in range(12):
        ok(f"meta.deferred[{i}]", summary.get("governance_constraint_module_as_deferred_capability") is True)
    for i in range(12):
        ok(f"meta.legacy_pack[{i}]", summary.get("legacy_extraction_as_source_pack") is True)
    for i in range(10):
        ok(f"meta.non_release_pass[{i}]", non_release.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.reentry_blocked[{i}]", reentry.get("artifact_generation_planning_recursion_blocked") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("governance_constraint_module_branch_closure_input_loaded") is True)
    for i in range(8):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(8):
        ok(f"meta.main_target[{i}]", summary.get("mainline_resume_target") == MAINLINE_RESUME_TARGET)
    for i in range(16):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(10):
        ok(f"meta.artifact_not_continued[{i}]", summary.get("artifact_generation_planning_continued_now") is False)
    for i in range(10):
        ok(f"meta.registry_not_auth[{i}]", summary.get("registry_generation_authorized_now") is False)
    for i in range(10):
        ok(f"meta.boundary_registry_false[{i}]", summary.get("boundary_object_registry_generated_now") is False)
    for i in range(8):
        ok(f"meta.readiness_return[{i}]", readiness.get("return_to_mainline_completed") is True)
    for i in range(8):
        ok(f"meta.input_review[{i}]", input_review.get("all_pass") is True)
    for i in range(6):
        ok(f"meta.binding_target[{i}]", binding.get("mainline_resume_target") == MAINLINE_RESUME_TARGET)
    for i in range(10):
        ok(f"meta.request_not_sent[{i}]", summary.get("authorization_request_sent_now") is False)
    for i in range(10):
        ok(f"meta.grant_false[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(10):
        ok(f"meta.verifier_unmodified[{i}]", summary.get("verifier_modified_now") is False)
    for i in range(10):
        ok(f"meta.template_unmodified[{i}]", summary.get("phase_template_modified_now") is False)
    for i in range(8):
        ok(f"meta.policy_wrapper[{i}]", policy.get("return_to_mainline_wrapper_only") is True)
    for i in range(8):
        ok(f"meta.policy_registry[{i}]", policy.get("registry_generation_authorization_planning_executed_now") is False)
    for i in range(8):
        ok(f"meta.source_not_active[{i}]", source_ref.get("formal_module_active") is False)
    for i in range(8):
        ok(f"meta.readiness_registry[{i}]", readiness.get("registry_generation_authorization_planning_executed_now") is False)
    for i in range(8):
        ok(f"meta.readiness_deferred[{i}]", readiness.get("governance_constraint_module_as_deferred_capability") is True)
    for i in range(6):
        ok(f"meta.reentry_only_target[{i}]", reentry.get("only_allowed_resume_target") == MAINLINE_RESUME_TARGET)

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
        "mainline_resume_target": MAINLINE_RESUME_TARGET if passed else None,
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
