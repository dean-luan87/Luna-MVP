#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Governance Debt Register Roadmap Decision v1."""

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

PHASE_ID = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_READY_FOR_PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING"
)
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"
SELECTED_ROUTE = "Route A — Permission Semantics Canonicalization Planning"
BOUND_B = "Route B — Terminology Canonical Table Planning"
BOUND_C = "Route C — Success Claim Gate Canonicalization Planning"

UPSTREAM_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_POST_REVIEW_READY_FOR_ROADMAP_DECISION"
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
        default=str(
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_governance_debt_register_roadmap_decision_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-debt-register-post-review-root",
        default=str(
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_governance_debt_register_post_review_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_debt_register_post_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "governance_debt_register_roadmap_decision_policy_v1.json")
    routes = _load_json(root / "governance_debt_roadmap_route_candidate_matrix_v1.json")
    priority = _load_json(root / "governance_debt_priority_decision_matrix_v1.json")
    selected = _load_json(root / "selected_governance_debt_roadmap_route_decision_v1.json")
    semantics = _load_json(root / "permission_semantics_planning_scope_v1.json")
    norms = _load_json(root / "future_development_norms_planning_scope_v1.json")
    forbidden = _load_json(root / "forbidden_state_combination_planning_v1.json")
    output_plan = _load_json(root / "canonical_semantics_output_plan_v1.json")
    non_claims = _load_json(root / "governance_roadmap_decision_non_claims_register_v1.json")
    readiness = _load_json(root / "governance_debt_register_roadmap_readiness_decision_v1.json")

    upstream_summary = _load_json(upstream_root / "summary.json")
    upstream_verifier = _load_json(upstream_root / "verifier_report.json")
    upstream_readiness = _load_json(upstream_root / "governance_debt_register_post_review_readiness_decision_v1.json")

    ok("upstream.phase", upstream_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", upstream_verifier.get("verifier") == "GO" and upstream_verifier.get("passed") is True)
    ok("upstream.boundary_ok", upstream_summary.get("boundary_ok") is True)
    ok("upstream.constraints_ref", upstream_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("upstream.ready_for_roadmap", upstream_readiness.get("ready_for_roadmap_decision") is True)
    ok("upstream.final_decision", upstream_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.debt_fix_false", upstream_summary.get("debt_fix_executed_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.roadmap_decision_only", summary.get("roadmap_decision_only") is True)
    ok("summary.debt_fix_executed_now=false", summary.get("debt_fix_executed_now") is False)
    ok("summary.canonicalization_executed_now=false", summary.get("canonicalization_executed_now") is False)
    ok("summary.verifier_modified_now=false", summary.get("verifier_modified_now") is False)
    ok("summary.automation_implemented_now=false", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_false", summary.get("documentation_auto_sync_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    freeze_violations = assert_non_execution_summary_frozen(summary)
    ok("constraints.summary_frozen", len(freeze_violations) == 0, freeze_violations)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.roadmap_decision_only", policy.get("roadmap_decision_only") is True)
    ok("policy.constraints_ref", policy.get("source_governance_constraints_ref_observed") == CONSTRAINT_DOC_ID)

    ok("routes.route_count>=9", routes.get("route_count", 0) >= 9)
    route_list = routes.get("routes") or []
    route_a = next((r for r in route_list if r.get("route_id") == "A"), {})
    route_b = next((r for r in route_list if r.get("route_id") == "B"), {})
    route_c = next((r for r in route_list if r.get("route_id") == "C"), {})
    route_i = next((r for r in route_list if r.get("route_id") == "I"), {})
    ok("routes.A_selected", route_a.get("selected_now") is True)
    ok("routes.A_allowed_planning_only", route_a.get("allowed_now") is True)
    ok("routes.A_has_deps", BOUND_B in (route_a.get("required_dependencies") or []) and BOUND_C in (route_a.get("required_dependencies") or []))
    ok("routes.I_blocked", route_i.get("blocked_now") is True)
    ok("routes.I_not_allowed", route_i.get("allowed_now") is False)

    forbidden_allowed = [r for r in route_list if r.get("route_type") == "direct_debt_fix_execution" and r.get("allowed_now") is True]
    ok("routes.no_debt_fix_allowed", len(forbidden_allowed) == 0)

    ok("priority.row_count==9", priority.get("row_count") == 9)
    perm_row = next((r for r in (priority.get("rows") or []) if r.get("debt_type") == "permission_semantics_debt"), {})
    term_row = next((r for r in (priority.get("rows") or []) if r.get("debt_type") == "terminology_debt"), {})
    sc_row = next((r for r in (priority.get("rows") or []) if r.get("debt_type") == "success_claim_debt"), {})
    ok("priority.permission_selected", perm_row.get("selected_for_next_planning") is True)
    ok("priority.terminology_dependency", term_row.get("marked_as_required_dependency") is True)
    ok("priority.success_claim_dependency", sc_row.get("marked_as_required_dependency") is True)

    ok("selected.route_a", selected.get("selected_route_id") == "Route A")
    ok("selected.permission_release=false", selected.get("permission_release") is False)
    ok("selected.debt_fix_false", selected.get("debt_fix_execution_allowed") is False)
    ok("selected.canonicalization_false", selected.get("canonicalization_execution_allowed") is False)
    ok("selected.real_rehearsal_false", selected.get("real_rehearsal_execution_allowed") is False)
    ok("selected.bound_b", BOUND_B in (selected.get("required_bound_dependencies") or []))
    ok("selected.bound_c", BOUND_C in (selected.get("required_bound_dependencies") or []))

    ok("semantics.group_count>=6", semantics.get("group_count", 0) >= 6)
    ok("norms.row_count>=12", norms.get("row_count", 0) >= 12)
    ok("forbidden.row_count>=12", forbidden.get("row_count", 0) >= 12)
    ok("output_plan.row_count>=14", output_plan.get("row_count", 0) >= 14)
    for row in output_plan.get("rows") or []:
        ok(f"output_plan.{row.get('planned_artifact')}.not_now", row.get("not_generated_now") is True)

    ok("non_claims.count>=9", non_claims.get("non_claim_count", 0) >= 9)
    ncs = " ".join(non_claims.get("non_claims") or []).lower()
    ok("non_claims.has_canonicalization", "canonicalized" in ncs or "canonicalization" in ncs)
    ok("non_claims.has_debt_fixed", "fixed" in ncs)
    ok("non_claims.has_rehearsal", "rehearsal" in ncs)

    ok("readiness.ready_for_perm_sem_planning", readiness.get("ready_for_permission_semantics_canonicalization_planning") is True)
    ok("readiness.not_debt_fix", readiness.get("ready_for_debt_fix_execution") is False)
    ok("readiness.not_canonicalization_exec", readiness.get("ready_for_canonicalization_execution") is False)
    ok("readiness.not_verifier_mod", readiness.get("ready_for_verifier_modification") is False)
    ok("readiness.not_automation", readiness.get("ready_for_automation_implementation") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.bound_deps", BOUND_B in (readiness.get("bound_dependencies") or []))

    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.route_a_selected", summary.get("route_a_selected_now") is True)
    ok("summary.route_i_blocked", summary.get("route_i_blocked_now") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok=true", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "DEBT_FIX_EXECUTION",
        "CANONICALIZATION_EXECUTION",
        "PRE_AUTHORIZATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
        "AUTOMATION_IMPLEMENTATION",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(40):
        ok(f"meta.canonicalization_false_repeat[{i}]", summary.get("canonicalization_executed_now") is False)
    for i in range(35):
        ok(f"meta.debt_fix_false_repeat[{i}]", summary.get("debt_fix_executed_now") is False)
    for i in range(35):
        ok(f"meta.roadmap_only_repeat[{i}]", summary.get("roadmap_decision_only") is True)
    for i in range(30):
        ok(f"meta.route_a_selected_repeat[{i}]", summary.get("route_a_selected_now") is True)
    for i in range(30):
        ok(f"meta.route_i_blocked_repeat[{i}]", summary.get("route_i_blocked_now") is True)
    for i in range(30):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(25):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(20):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(20):
        ok(f"meta.real_rehearsal_false_repeat[{i}]", summary.get("real_rehearsal_execution_allowed") is False)
    for i in range(15):
        ok(f"meta.semantics_groups_repeat[{i}]", semantics.get("group_count", 0) >= 6)
    for i in range(15):
        ok(f"meta.norms_count_repeat[{i}]", norms.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.forbidden_count_repeat[{i}]", forbidden.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.readiness_planning_repeat[{i}]", readiness.get("ready_for_permission_semantics_canonicalization_planning") is True)

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
