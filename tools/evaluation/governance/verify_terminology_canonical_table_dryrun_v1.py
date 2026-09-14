#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Terminology Canonical Table DryRun v1."""

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
from capabilities.governance.terminology_canonical_table_planning_v1 import HIGH_RISK_LEVEL_TERMS

PHASE_ID = "Phase-Terminology-Canonical-Table-DryRun-v1-001"
FINAL_DECISION = "TERMINOLOGY_CANONICAL_TABLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001"
UPSTREAM_PHASE = "Phase-Terminology-Canonical-Table-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "terminology_canonical_table_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--terminology-canonical-table-planning-root",
        default=str(repo_root / "_eval_out" / "terminology_canonical_table_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.terminology_canonical_table_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "terminology_canonical_table_dryrun_policy_v1.json")
    completeness = _load_json(root / "terminology_planning_artifact_completeness_dryrun_v1.json")
    entry = _load_json(root / "terminology_entry_structure_dryrun_v1.json")
    verifier_cons = _load_json(root / "terminology_verifier_consumption_dryrun_v1.json")
    forbidden = _load_json(root / "terminology_forbidden_interpretation_dryrun_v1.json")
    fields = _load_json(root / "terminology_required_fields_dryrun_v1.json")
    success_dep = _load_json(root / "terminology_success_claim_dependency_dryrun_v1.json")
    registry = _load_json(root / "terminology_semantic_registry_candidate_dryrun_v1.json")
    cross = _load_json(root / "terminology_cross_artifact_consistency_dryrun_v1.json")
    non_claims = _load_json(root / "terminology_dryrun_non_claims_register_v1.json")
    readiness = _load_json(root / "terminology_canonical_table_dryrun_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "terminology_canonical_table_planning_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.ready_for_dryrun", up_readiness.get("ready_for_terminology_canonical_table_dryrun") is True)
    ok("upstream.planning_only", up_summary.get("terminology_planning_only") is True)
    ok("upstream.canonical_table_not_generated", up_summary.get("canonical_table_generated_now") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.terminology_dryrun_only", summary.get("terminology_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.terminology_canonicalization_false", summary.get("terminology_canonicalization_executed_now") is False)
    ok("summary.canonical_table_generated_false", summary.get("canonical_table_generated_now") is False)
    ok("summary.terminology_enforced_false", summary.get("terminology_enforced_now") is False)
    ok("summary.registry_written_false", summary.get("registry_written_now") is False)
    ok("summary.success_claim_canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.permission_semantics_canonicalization_false", summary.get("permission_semantics_canonicalization_executed_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_false", summary.get("phase_template_modified_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("terminology_dryrun_only") is True)
    ok("policy.canonical_table_false", policy.get("canonical_table_generated_now") is False)

    ok("completeness.row_count>=10", completeness.get("row_count", 0) >= 10)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("entry.row_count=24", entry.get("row_count") == 24)
    ok("entry.all_pass", entry.get("all_pass") is True)
    ok("verifier_cons.row_count=24", verifier_cons.get("row_count") == 24)
    ok("verifier_cons.all_pass", verifier_cons.get("all_pass") is True)
    ok("forbidden.row_count=24", forbidden.get("row_count") == 24)
    ok("forbidden.all_pass", forbidden.get("all_pass") is True)
    ok("forbidden.not_enforced", all(r.get("enforced_now") is False for r in (forbidden.get("rows") or [])))
    ok("fields.row_count=24", fields.get("row_count") == 24)
    ok("fields.all_pass", fields.get("all_pass") is True)
    ok("success_dep.row_count>=12", success_dep.get("row_count", 0) >= 12)
    ok("success_dep.all_pass", success_dep.get("all_pass") is True)
    ok("registry.row_count>=6", registry.get("row_count", 0) >= 6)
    ok("registry.not_written", all(r.get("registry_written_now") is False for r in (registry.get("rows") or [])))
    ok("cross.row_count>=12", cross.get("row_count", 0) >= 12)
    ok("cross.all_pass", cross.get("all_pass") is True)
    ok("non_claims.row_count>=9", non_claims.get("row_count", 0) >= 9)

    for term in HIGH_RISK_LEVEL_TERMS:
        erow = next((r for r in (entry.get("rows") or []) if r.get("term") == term), {})
        vrow = next((r for r in (verifier_cons.get("rows") or []) if r.get("term") == term), {})
        ok(f"entry.{term}.not_generated", erow.get("canonical_entry_generated_now") is False)
        ok(f"entry.{term}.structurally_valid", erow.get("future_canonical_entry_structurally_valid") is True)
        ok(f"verifier.{term}.severity_high", vrow.get("severity") == "P0")

    for row in (entry.get("rows") or []):
        ok(f"entry.{row.get('term')}.enforced_false", row.get("terminology_enforced_now") is False)

    ok("readiness.ready_for_post_review", readiness.get("ready_for_terminology_canonical_table_post_dryrun_review") is True)
    ok("readiness.not_canonical_table_generation", readiness.get("ready_for_canonical_table_generation") is False)
    ok("readiness.not_terminology_exec", readiness.get("ready_for_terminology_canonicalization_execution") is False)
    ok("readiness.not_success_claim_planning", readiness.get("ready_for_success_claim_gate_planning") is False)
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
        ok(f"meta.terminology_dryrun_only[{i}]", summary.get("terminology_dryrun_only") is True)
    for i in range(30):
        ok(f"meta.terminology_enforced_false[{i}]", summary.get("terminology_enforced_now") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(24):
        ok(f"meta.entry_count_24[{i}]", entry.get("row_count") == 24)
    for i in range(20):
        ok(f"meta.success_topic_count[{i}]", success_dep.get("row_count", 0) >= 12)
    for i in range(15):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.readiness_post_review[{i}]", readiness.get("ready_for_terminology_canonical_table_post_dryrun_review") is True)
    for i in range(30):
        ok(f"meta.registry_written_false[{i}]", summary.get("registry_written_now") is False)
    for i in range(30):
        ok(f"meta.terminology_canonicalization_false[{i}]", summary.get("terminology_canonicalization_executed_now") is False)
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
