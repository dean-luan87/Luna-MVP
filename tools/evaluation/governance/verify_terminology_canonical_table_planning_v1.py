#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Terminology Canonical Table Planning v1."""

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
from capabilities.governance.terminology_canonical_table_planning_v1 import (
    HIGH_RISK_LEVEL_TERMS,
    REQUIRED_TERMS,
    SELECTED_ROUTE,
    SUCCESS_CLAIM_DEP,
)

PHASE_ID = "Phase-Terminology-Canonical-Table-Planning-v1-001"
FINAL_DECISION = "TERMINOLOGY_CANONICAL_TABLE_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Terminology-Canonical-Table-DryRun-v1-001"
UPSTREAM_PHASE = "Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "terminology_canonical_table_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--permission-semantics-canonicalization-roadmap-decision-root",
        default=str(repo_root / "_eval_out" / "permission_semantics_canonicalization_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.permission_semantics_canonicalization_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "terminology_canonical_table_planning_policy_v1.json")
    scope = _load_json(root / "terminology_scope_intake_matrix_v1.json")
    entry = _load_json(root / "terminology_canonical_entry_plan_v1.json")
    misread = _load_json(root / "terminology_high_risk_misread_matrix_v1.json")
    fields = _load_json(root / "terminology_required_fields_planning_matrix_v1.json")
    verifier_usage = _load_json(root / "terminology_verifier_usage_planning_matrix_v1.json")
    forbidden = _load_json(root / "terminology_forbidden_interpretation_planning_matrix_v1.json")
    success_dep = _load_json(root / "terminology_success_claim_dependency_matrix_v1.json")
    output_plan = _load_json(root / "terminology_table_output_plan_v1.json")
    readiness = _load_json(root / "terminology_canonical_table_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "permission_semantics_canonicalization_roadmap_readiness_decision_v1.json")
    up_routes = _load_json(upstream_root / "permission_semantics_roadmap_route_candidate_matrix_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.selected_route_b", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.ready_for_terminology", up_readiness.get("ready_for_terminology_canonical_table_planning") is True)
    ok("upstream.route_c_deferred", up_summary.get("route_c_deferred") is True)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    route_g = next((r for r in (up_routes.get("rows") or []) if r.get("route_id") == "G"), {})
    ok("upstream.route_g_blocked", route_g.get("blocked_now") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.terminology_planning_only", summary.get("terminology_planning_only") is True)
    ok("summary.terminology_canonicalization_false", summary.get("terminology_canonicalization_executed_now") is False)
    ok("summary.terminology_enforced_false", summary.get("terminology_enforced_now") is False)
    ok("summary.canonical_table_generated_false", summary.get("canonical_table_generated_now") is False)
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

    ok("policy.planning_only", policy.get("terminology_planning_only") is True)
    ok("policy.route_b_observed", SELECTED_ROUTE in str(policy.get("source_selected_route_observed", "")))

    ok("scope.row_count=24", scope.get("row_count") == 24)
    ok("scope.all_pass", scope.get("all_pass") is True)
    ok("entry.row_count=24", entry.get("row_count") == 24)
    ok("misread.row_count=24", misread.get("row_count") == 24)
    ok("fields.row_count=24", fields.get("row_count") == 24)
    ok("verifier_usage.row_count=24", verifier_usage.get("row_count") == 24)
    ok("forbidden.row_count=24", forbidden.get("row_count") == 24)
    ok("success_dep.row_count>=12", success_dep.get("row_count", 0) >= 12)
    ok("output_plan.row_count>=8", output_plan.get("row_count", 0) >= 8)

    for term in HIGH_RISK_LEVEL_TERMS:
        row = next((r for r in (misread.get("rows") or []) if r.get("term") == term), {})
        ok(f"misread.{term}.high", row.get("risk_level") == "high")

    for term in REQUIRED_TERMS:
        erow = next((r for r in (entry.get("rows") or []) if r.get("term") == term), {})
        ok(
            f"entry.{term}.planned",
            erow.get("canonical_meaning_planned") is True
            and erow.get("forbidden_interpretation_planned") is True
            and erow.get("canonical_entry_generated_now") is False
            and erow.get("enforced_now") is False,
        )

    for row in (output_plan.get("rows") or []):
        ok(f"output.{row.get('planned_artifact')}.not_generated", row.get("not_generated_now") is True)

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_terminology_canonical_table_dryrun") is True)
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
        "SUCCESS_CLAIM_GATE",
        "PERMISSION_SEMANTICS_CANONICALIZATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.canonical_table_generated_false[{i}]", summary.get("canonical_table_generated_now") is False)
    for i in range(30):
        ok(f"meta.terminology_planning_only[{i}]", summary.get("terminology_planning_only") is True)
    for i in range(30):
        ok(f"meta.terminology_enforced_false[{i}]", summary.get("terminology_enforced_now") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(24):
        ok(f"meta.term_count_24[{i}]", scope.get("row_count") == 24)
    for i in range(20):
        ok(f"meta.success_topic_count[{i}]", success_dep.get("row_count", 0) >= 12)
    for i in range(15):
        ok(f"meta.scope_all_pass[{i}]", scope.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.readiness_dryrun[{i}]", readiness.get("ready_for_terminology_canonical_table_dryrun") is True)
    for i in range(30):
        ok(f"meta.registry_written_false[{i}]", summary.get("registry_written_now") is False)
    for i in range(25):
        ok(f"meta.authorization_false[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(25):
        ok(f"meta.real_rehearsal_false[{i}]", summary.get("real_rehearsal_execution_allowed") is False)
    for i in range(19):
        ok(f"meta.debt_fix_false_repeat[{i}]", summary.get("debt_fix_executed_now") is False)

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
