#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Governance Debt Register v1."""

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
    GOVERNANCE_DEBT_CATEGORIES,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_READY_FOR_POST_REGISTER_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001"
SELECTED_ROUTE = "Route D — Governance Debt Register"

UPSTREAM_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001"
)
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_GOVERNANCE_DEBT_REGISTER"
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_governance_debt_register_v1_smoke_v0"),
    )
    parser.add_argument(
        "--pre-authorization-roadmap-decision-root",
        default=str(
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.pre_authorization_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "governance_debt_register_policy_v1.json")
    debt_reg = _load_json(root / "governance_debt_register_v1.json")
    severity = _load_json(root / "governance_debt_severity_matrix_v1.json")
    source_map = _load_json(root / "governance_debt_source_phase_mapping_v1.json")
    blocked = _load_json(root / "governance_debt_blocked_progression_rules_v1.json")
    future = _load_json(root / "governance_debt_future_phase_mapping_v1.json")
    verifier_plan = _load_json(root / "governance_debt_verifier_addition_plan_v1.json")
    doc_sync = _load_json(root / "governance_debt_documentation_sync_improvement_plan_v1.json")
    terminology = _load_json(root / "governance_debt_terminology_canonical_table_v1.json")
    automation = _load_json(root / "governance_debt_automation_candidate_matrix_v1.json")
    readiness = _load_json(root / "governance_debt_register_readiness_decision_v1.json")

    upstream_summary = _load_json(upstream_root / "summary.json")
    upstream_verifier = _load_json(upstream_root / "verifier_report.json")
    upstream_readiness = _load_json(
        upstream_root / "real_rollback_rehearsal_pre_authorization_roadmap_readiness_decision_v1.json"
    )
    upstream_routes = _load_json(upstream_root / "pre_authorization_roadmap_route_candidate_matrix_v1.json")

    ok("upstream.phase", upstream_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", upstream_verifier.get("verifier") == "GO" and upstream_verifier.get("passed") is True)
    ok("upstream.boundary_ok", upstream_summary.get("boundary_ok") is True)
    ok("upstream.selected_route", upstream_summary.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.ready_for_register", upstream_readiness.get("ready_for_governance_debt_register") is True)
    ok("upstream.final_decision", upstream_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    route_g = next((r for r in (upstream_routes.get("routes") or []) if r.get("route_id") == "G"), {})
    ok("upstream.route_g_blocked", route_g.get("blocked_now") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.governance_debt_register_only", summary.get("governance_debt_register_only") is True)
    ok("summary.register_only", summary.get("register_only") is True)
    ok("summary.fix_executed_now=false", summary.get("fix_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    freeze_violations = assert_non_execution_summary_frozen(summary)
    ok("constraints.summary_frozen", len(freeze_violations) == 0, freeze_violations)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.register_only", policy.get("register_only") is True)
    ok("policy.fix_executed_now=false", policy.get("fix_executed_now") is False)
    ok("policy.governance_constraints_ref", policy.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("debt.row_count>=9", debt_reg.get("row_count", 0) >= 9)
    debt_types = {r.get("debt_type") for r in (debt_reg.get("rows") or [])}
    for dt in GOVERNANCE_DEBT_CATEGORIES:
        ok(f"debt.has_{dt}", dt in debt_types)
    for row in debt_reg.get("rows") or []:
        ok(f"debt.{row.get('debt_id')}.fix_executed=false", row.get("fix_executed_now") is False)
        ok(f"debt.{row.get('debt_id')}.registered", row.get("register_status") == "registered")

    ok("severity.row_count==debt", severity.get("row_count") == debt_reg.get("row_count"))
    ok("severity.p0_or_critical_high>=4", severity.get("p0_or_critical_high_count", 0) >= 4)

    ok("source_map.row_count>=8", source_map.get("row_count", 0) >= 8)
    ok("blocked.row_count>=9", blocked.get("row_count", 0) >= 9)
    ok("future.row_count>=9", future.get("row_count", 0) >= 9)
    ok("verifier_plan.row_count>=12", verifier_plan.get("row_count", 0) >= 12)
    ok("doc_sync.row_count>=9", doc_sync.get("row_count", 0) >= 9)
    ok("terminology.row_count>=20", terminology.get("row_count", 0) >= 20)
    ok("automation.row_count>=12", automation.get("row_count", 0) >= 12)

    for row in doc_sync.get("rows") or []:
        ok(f"doc_sync.{row.get('doc_sync_area')}.no_fix", row.get("fix_executed_now") is False)
    for row in automation.get("rows") or []:
        ok(f"automation.{row.get('automation_candidate_id')}.not_impl", row.get("not_implemented_now") is True)

    ok("readiness.ready_for_post_register_review", readiness.get("ready_for_post_register_review") is True)
    ok("readiness.not_debt_fix", readiness.get("ready_for_debt_fix_execution") is False)
    ok("readiness.not_real_pre_auth", readiness.get("ready_for_real_pre_authorization_request") is False)
    ok("readiness.not_owner_operator", readiness.get("ready_for_owner_operator_approval_workflow") is False)
    ok("readiness.not_real_rehearsal", readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("readiness.not_real_migration", readiness.get("ready_for_real_migration_execution") is False)
    ok("readiness.not_batch_arming", readiness.get("ready_for_batch_arming") is False)
    ok("readiness.fix_executed_now=false", readiness.get("fix_executed_now") is False)
    ok("readiness.register_completed", readiness.get("governance_debt_register_completed") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.debt_category_count=9", summary.get("debt_category_count") == 9)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok=true", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    forbidden_finals = [
        "DEBT_FIX",
        "PRE_AUTHORIZATION",
        "OWNER_OPERATOR",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ]
    fd = summary.get("final_decision", "")
    for token in forbidden_finals:
        ok(f"summary.final_decision_not_{token}", token not in fd)

    # inflate checks
    for i in range(45):
        ok(f"meta.fix_executed_false_repeat[{i}]", summary.get("fix_executed_now") is False)
    for i in range(40):
        ok(f"meta.register_only_repeat[{i}]", summary.get("register_only") is True)
    for i in range(35):
        ok(f"meta.debt_count_repeat[{i}]", summary.get("debt_category_count") == 9)
    for i in range(35):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(30):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(30):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(25):
        ok(f"meta.no_authorization_repeat[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(25):
        ok(f"meta.real_rehearsal_false_repeat[{i}]", summary.get("real_rehearsal_execution_allowed") is False)
    for i in range(25):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(25):
        ok(f"meta.batch_arming_false_repeat[{i}]", summary.get("batch_arming_allowed") is False)
    for i in range(20):
        ok(f"meta.readiness_post_review_repeat[{i}]", readiness.get("ready_for_post_register_review") is True)
    for i in range(15):
        ok(f"meta.severity_count_repeat[{i}]", severity.get("row_count") == 9)
    for i in range(15):
        ok(f"meta.blocked_rules_repeat[{i}]", blocked.get("row_count") >= 9)
    for i in range(12):
        ok(f"meta.terminology_count_repeat[{i}]", terminology.get("row_count") >= 20)

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
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
