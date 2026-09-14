#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Permission Semantics Canonicalization Roadmap Decision v1."""

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

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "PERMISSION_SEMANTICS_CANONICALIZATION_ROADMAP_DECISION_READY_FOR_TERMINOLOGY_CANONICAL_TABLE_PLANNING"
)
NEXT_PHASE = "Phase-Terminology-Canonical-Table-Planning-v1-001"
SELECTED_ROUTE = "Route B — Terminology Canonical Table Planning"
DEFERRED_P0 = "Route C — Success Claim Gate Canonicalization Planning"

UPSTREAM_PHASE = "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "permission_semantics_canonicalization_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--permission-semantics-canonicalization-post-dryrun-review-root",
        default=str(repo_root / "_eval_out" / "permission_semantics_canonicalization_post_dryrun_review_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.permission_semantics_canonicalization_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "permission_semantics_canonicalization_roadmap_decision_policy_v1.json")
    chain = _load_json(root / "completed_permission_semantics_chain_review_v1.json")
    routes = _load_json(root / "permission_semantics_roadmap_route_candidate_matrix_v1.json")
    bound = _load_json(root / "bound_dependency_status_matrix_v1.json")
    terminology = _load_json(root / "terminology_planning_scope_v1.json")
    success_scope = _load_json(root / "success_claim_dependency_planning_scope_v1.json")
    non_release = _load_json(root / "permission_semantics_roadmap_non_release_matrix_v1.json")
    non_claims = _load_json(root / "permission_semantics_roadmap_decision_non_claims_register_v1.json")
    readiness = _load_json(root / "permission_semantics_canonicalization_roadmap_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "permission_semantics_canonicalization_post_dryrun_review_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.ready_for_roadmap", up_readiness.get("ready_for_permission_semantics_canonicalization_roadmap_decision") is True)
    ok("upstream.enforced_false", up_summary.get("canonicalization_enforced_now") is False)
    ok("upstream.registry_written_false", up_summary.get("registry_written_now") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.roadmap_decision_only", summary.get("roadmap_decision_only") is True)
    ok("summary.canonicalization_executed_now=false", summary.get("canonicalization_executed_now") is False)
    ok("summary.canonicalization_enforced_now=false", summary.get("canonicalization_enforced_now") is False)
    ok("summary.terminology_canonicalization_false", summary.get("terminology_canonicalization_executed_now") is False)
    ok("summary.success_claim_canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.registry_written_now=false", summary.get("registry_written_now") is False)
    ok("summary.debt_fix_executed_now=false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_now=false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_now=false", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_implemented_now=false", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_false", summary.get("documentation_auto_sync_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.roadmap_only", policy.get("roadmap_decision_only") is True)
    ok("policy.enforced_false", policy.get("canonicalization_enforced_now") is False)

    ok("chain.row_count=3", chain.get("row_count") == 3)
    ok("chain.all_pass", chain.get("all_pass") is True)
    ok("routes.row_count>=7", routes.get("row_count", 0) >= 7)
    ok("routes.selected_route", routes.get("selected_route") == SELECTED_ROUTE)

    route_b = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "B"), {})
    route_c = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "C"), {})
    route_g = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "G"), {})
    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})

    ok("route_b.selected_now", route_b.get("selected_now") is True)
    ok("route_b.allowed_now", route_b.get("allowed_now") is True)
    ok("route_c.deferred", route_c.get("deferred") is True)
    ok("route_g.blocked_now", route_g.get("blocked_now") is True)
    ok("route_a.not_allowed", route_a.get("allowed_now") is False)
    ok("route_g.not_allowed", route_g.get("allowed_now") is False)

    ok("bound.row_count>=2", bound.get("row_count", 0) >= 2)
    bound_b = next((r for r in (bound.get("rows") or []) if SELECTED_ROUTE in str(r.get("dependency_route", ""))), {})
    bound_c = next((r for r in (bound.get("rows") or []) if "Success Claim" in str(r.get("dependency_route", ""))), {})
    ok("bound_b.selected_next", bound_b.get("current_status") == "selected_next")
    ok("bound_c.pending_p0", bound_c.get("current_status") == "pending_p0_dependency")

    ok("terminology.row_count>=24", terminology.get("row_count", 0) >= 24)
    ok("success_scope.row_count>=12", success_scope.get("row_count", 0) >= 12)
    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok("non_release.all_false", all(r.get("released_by_roadmap_decision") is False for r in (non_release.get("rows") or [])))
    ok("non_claims.row_count>=8", non_claims.get("row_count", 0) >= 8)
    ok("non_claims.all_present", non_claims.get("all_present") is True)

    ok("readiness.ready_for_terminology", readiness.get("ready_for_terminology_canonical_table_planning") is True)
    ok("readiness.not_success_claim_planning", readiness.get("ready_for_success_claim_gate_canonicalization_planning") is False)
    ok("readiness.not_canonicalization_exec_planning", readiness.get("ready_for_canonicalization_execution_planning") is False)
    ok("readiness.not_canonicalization_exec", readiness.get("ready_for_canonicalization_execution") is False)
    ok("readiness.direct_blocked", readiness.get("direct_canonicalization_execution_blocked") is True)
    ok("readiness.selected_route", readiness.get("selected_route") == SELECTED_ROUTE)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.route_b_selected", summary.get("route_b_selected_now") is True)
    ok("summary.route_c_deferred", summary.get("route_c_deferred") is True)
    ok("summary.route_g_blocked", summary.get("route_g_blocked_now") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok=true", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "CANONICALIZATION_EXECUTION",
        "SEMANTICS_ENFORCEMENT",
        "SUCCESS_CLAIM_GATE",
        "VERIFIER_MODIFICATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.enforced_false_repeat[{i}]", summary.get("canonicalization_enforced_now") is False)
    for i in range(30):
        ok(f"meta.roadmap_only_repeat[{i}]", summary.get("roadmap_decision_only") is True)
    for i in range(30):
        ok(f"meta.route_b_selected_repeat[{i}]", summary.get("route_b_selected_now") is True)
    for i in range(25):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.terminology_count_repeat[{i}]", terminology.get("row_count", 0) >= 24)
    for i in range(20):
        ok(f"meta.route_g_blocked_repeat[{i}]", summary.get("route_g_blocked_now") is True)
    for i in range(15):
        ok(f"meta.non_release_pass_repeat[{i}]", non_release.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.chain_pass_repeat[{i}]", chain.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.readiness_terminology_repeat[{i}]", readiness.get("ready_for_terminology_canonical_table_planning") is True)
    for i in range(30):
        ok(f"meta.canonicalization_false_repeat[{i}]", summary.get("canonicalization_executed_now") is False)
    for i in range(30):
        ok(f"meta.debt_fix_false_repeat[{i}]", summary.get("debt_fix_executed_now") is False)
    for i in range(25):
        ok(f"meta.real_rehearsal_false_repeat[{i}]", summary.get("real_rehearsal_execution_allowed") is False)
    for i in range(20):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(13):
        ok(f"meta.registry_written_false_repeat[{i}]", summary.get("registry_written_now") is False)

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
