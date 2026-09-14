#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Terminology Canonical Table Post-DryRun Review v1."""

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
from capabilities.governance.terminology_canonical_table_planning_v1 import REQUIRED_TERMS

PHASE_ID = "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001"
FINAL_DECISION = "TERMINOLOGY_CANONICAL_TABLE_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Terminology-Canonical-Table-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Terminology-Canonical-Table-DryRun-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "terminology_canonical_table_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--terminology-canonical-table-dryrun-root",
        default=str(repo_root / "_eval_out" / "terminology_canonical_table_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.terminology_canonical_table_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "terminology_canonical_table_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "terminology_dryrun_completeness_review_v1.json")
    formal = _load_json(root / "terminology_formal_table_non_generation_review_v1.json")
    entry_sim = _load_json(root / "terminology_entry_simulation_review_v1.json")
    verifier_rev = _load_json(root / "terminology_verifier_non_modification_review_v1.json")
    forbidden_rev = _load_json(root / "terminology_forbidden_interpretation_non_enforcement_review_v1.json")
    fields_rev = _load_json(root / "terminology_required_fields_simulation_review_v1.json")
    registry_rev = _load_json(root / "terminology_registry_write_review_v1.json")
    success_rev = _load_json(root / "terminology_success_claim_dependency_review_v1.json")
    non_claims = _load_json(root / "terminology_post_dryrun_review_non_claims_register_v1.json")
    readiness = _load_json(root / "terminology_canonical_table_post_dryrun_review_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "terminology_canonical_table_dryrun_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.ready_for_post_review", up_readiness.get("ready_for_terminology_canonical_table_post_dryrun_review") is True)
    ok("upstream.terminology_dryrun_only", up_summary.get("terminology_dryrun_only") is True)
    ok("upstream.simulated", up_summary.get("simulated") is True)
    ok("upstream.canonical_table_false", up_summary.get("canonical_table_generated_now") is False)
    ok("upstream.terminology_enforced_false", up_summary.get("terminology_enforced_now") is False)
    ok("upstream.registry_written_false", up_summary.get("registry_written_now") is False)
    ok("upstream.verifier_modified_false", up_summary.get("verifier_modified_now") is False)
    ok("upstream.not_success_claim_planning", up_readiness.get("ready_for_success_claim_gate_planning") is False)
    ok("upstream.not_terminology_exec", up_readiness.get("ready_for_terminology_canonicalization_execution") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.terminology_canonicalization_false", summary.get("terminology_canonicalization_executed_now") is False)
    ok("summary.canonical_table_generated_false", summary.get("canonical_table_generated_now") is False)
    ok("summary.terminology_enforced_false", summary.get("terminology_enforced_now") is False)
    ok("summary.registry_written_false", summary.get("registry_written_now") is False)
    ok("summary.success_claim_canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.permission_semantics_canonicalization_false", summary.get("permission_semantics_canonicalization_executed_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_false", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_false", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_false", summary.get("documentation_auto_sync_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.review_only", policy.get("post_dryrun_review_only") is True)
    ok("policy.canonical_table_false", policy.get("canonical_table_generated_now") is False)
    ok("policy.terminology_enforced_false", policy.get("terminology_enforced_now") is False)

    ok("completeness.row_count>=11", completeness.get("row_count", 0) >= 11)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("formal.all_pass", formal.get("all_pass") is True)
    ok("formal.no_violations", all(not r.get("violation_detected") for r in (formal.get("rows") or [])))
    ok("entry_sim.row_count=24", entry_sim.get("row_count") == 24)
    ok("entry_sim.all_pass", entry_sim.get("all_pass") is True)
    ok("entry_sim.simulated_only", all(r.get("simulated_only") is True for r in (entry_sim.get("rows") or [])))
    ok("verifier_rev.row_count>=24", verifier_rev.get("row_count", 0) >= 24)
    ok("verifier_rev.all_pass", verifier_rev.get("all_pass") is True)
    ok("verifier_rev.not_modified", all(r.get("verifier_modified_now") is False for r in (verifier_rev.get("rows") or [])))
    ok("forbidden_rev.row_count>=24", forbidden_rev.get("row_count", 0) >= 24)
    ok("forbidden_rev.all_pass", forbidden_rev.get("all_pass") is True)
    ok("forbidden_rev.not_enforced", all(r.get("enforced_now") is False for r in (forbidden_rev.get("rows") or [])))
    ok("fields_rev.row_count>=24", fields_rev.get("row_count", 0) >= 24)
    ok("fields_rev.all_pass", fields_rev.get("all_pass") is True)
    ok("registry_rev.row_count>=6", registry_rev.get("row_count", 0) >= 6)
    ok("registry_rev.all_pass", registry_rev.get("all_pass") is True)
    ok("registry_rev.not_written", all(r.get("registry_written_now") is False for r in (registry_rev.get("rows") or [])))
    ok("success_rev.row_count>=12", success_rev.get("row_count", 0) >= 12)
    ok("success_rev.all_pass", success_rev.get("all_pass") is True)
    ok("success_rev.not_ready_planning", all(
        r.get("ready_for_success_claim_gate_planning") is False for r in (success_rev.get("rows") or [])
    ))
    ok("non_claims.row_count>=9", non_claims.get("row_count", 0) >= 9)
    ok("non_claims.all_present", non_claims.get("all_present") is True)

    for term in REQUIRED_TERMS:
        erow = next((r for r in (entry_sim.get("rows") or []) if r.get("term") == term), {})
        ok(f"entry.{term}.canonical_entry_false", erow.get("canonical_entry_generated_now") is False)
        ok(f"entry.{term}.review_pass", erow.get("review_pass") is True)

    ok("readiness.ready_for_roadmap", readiness.get("ready_for_terminology_canonical_table_roadmap_decision") is True)
    ok("readiness.not_canonical_table_generation", readiness.get("ready_for_canonical_table_generation") is False)
    ok("readiness.not_terminology_exec", readiness.get("ready_for_terminology_canonicalization_execution") is False)
    ok("readiness.not_enforcement", readiness.get("ready_for_terminology_enforcement") is False)
    ok("readiness.not_success_claim_planning", readiness.get("ready_for_success_claim_gate_planning") is False)
    ok("readiness.not_permission_semantics_exec", readiness.get("ready_for_permission_semantics_canonicalization_execution") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "TERMINOLOGY_CANONICALIZATION_EXECUTION",
        "TERMINOLOGY_ENFORCEMENT",
        "CANONICAL_TABLE_GENERATION",
        "SUCCESS_CLAIM_GATE",
        "PERMISSION_SEMANTICS",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.canonical_table_generated_false[{i}]", summary.get("canonical_table_generated_now") is False)
    for i in range(30):
        ok(f"meta.post_dryrun_review_only[{i}]", summary.get("post_dryrun_review_only") is True)
    for i in range(30):
        ok(f"meta.terminology_enforced_false[{i}]", summary.get("terminology_enforced_now") is False)
    for i in range(25):
        ok(f"meta.registry_written_false[{i}]", summary.get("registry_written_now") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(24):
        ok(f"meta.entry_count_24[{i}]", entry_sim.get("row_count") == 24)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.formal_pass[{i}]", formal.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.readiness_roadmap[{i}]", readiness.get("ready_for_terminology_canonical_table_roadmap_decision") is True)
    for i in range(30):
        ok(f"meta.terminology_canonicalization_false[{i}]", summary.get("terminology_canonicalization_executed_now") is False)
    for i in range(30):
        ok(f"meta.success_claim_canonicalization_false[{i}]", summary.get("success_claim_canonicalization_executed_now") is False)
    for i in range(25):
        ok(f"meta.authorization_false[{i}]", summary.get("authorization_granted_now") is False)

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
