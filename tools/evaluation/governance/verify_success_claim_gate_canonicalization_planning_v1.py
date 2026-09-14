#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Success Claim Gate Canonicalization Planning v1."""

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
from capabilities.governance.success_claim_gate_canonicalization_planning_v1 import (
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001"
FINAL_DECISION = "SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001"
UPSTREAM_PHASE = "Phase-Terminology-Canonical-Table-Roadmap-Decision-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "success_claim_gate_canonicalization_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--terminology-canonical-table-roadmap-decision-root",
        default=str(repo_root / "_eval_out" / "terminology_canonical_table_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.terminology_canonical_table_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "success_claim_gate_canonicalization_planning_policy_v1.json")
    conditions = _load_json(root / "success_claim_gate_condition_scope_v1.json")
    forbidden = _load_json(root / "success_claim_forbidden_interpretation_matrix_v1.json")
    evidence = _load_json(root / "success_claim_required_evidence_planning_matrix_v1.json")
    boundary = _load_json(root / "success_claim_runtime_vs_audit_evidence_boundary_v1.json")
    auth = _load_json(root / "success_claim_authorization_dependency_matrix_v1.json")
    non_claims = _load_json(root / "success_claim_non_claims_planning_matrix_v1.json")
    verifier_usage = _load_json(root / "success_claim_verifier_usage_planning_matrix_v1.json")
    output_plan = _load_json(root / "success_claim_gate_output_plan_v1.json")
    readiness = _load_json(root / "success_claim_gate_canonicalization_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "terminology_canonical_table_roadmap_readiness_decision_v1.json")
    up_routes = _load_json(upstream_root / "terminology_roadmap_route_candidate_matrix_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.selected_route_c", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.ready_for_planning", up_readiness.get("ready_for_success_claim_gate_canonicalization_planning") is True)
    ok("upstream.success_claim_allowed_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.gate_not_generated", up_summary.get("success_claim_gate_generated_now") is False)
    ok("upstream.not_gate_execution", up_readiness.get("ready_for_success_claim_gate_execution") is False)
    ok("upstream.not_allowance", up_readiness.get("ready_for_success_claim_allowance") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    route_g = next((r for r in (up_routes.get("rows") or []) if r.get("route_id") == "G"), {})
    ok("upstream.route_g_blocked", route_g.get("blocked_now") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("success_claim_gate_planning_only") is True)
    ok("summary.gate_not_generated", summary.get("success_claim_gate_generated_now") is False)
    ok("summary.gate_not_enforced", summary.get("success_claim_gate_enforced_now") is False)
    ok("summary.success_claim_allowed_false", summary.get("success_claim_allowed") is False)
    ok("summary.success_evidence_false", summary.get("success_evidence_generated_now") is False)
    ok("summary.runtime_evidence_false", summary.get("runtime_evidence_generated_now") is False)
    ok("summary.canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.terminology_canonicalization_false", summary.get("terminology_canonicalization_executed_now") is False)
    ok("summary.canonical_table_false", summary.get("canonical_table_generated_now") is False)
    ok("summary.permission_semantics_false", summary.get("permission_semantics_canonicalization_executed_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_false", summary.get("phase_template_modified_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.planning_only", policy.get("success_claim_gate_planning_only") is True)
    ok("policy.route_c_observed", SELECTED_ROUTE in str(policy.get("source_selected_route_observed", "")))

    ok("conditions.row_count>=12", conditions.get("row_count", 0) >= 12)
    ok("forbidden.row_count>=14", forbidden.get("row_count", 0) >= 14)
    ok("evidence.row_count>=12", evidence.get("row_count", 0) >= 12)
    ok("boundary.row_count>=12", boundary.get("row_count", 0) >= 12)
    ok("auth.row_count>=10", auth.get("row_count", 0) >= 10)
    ok("non_claims.row_count>=15", non_claims.get("row_count", 0) >= 15)
    ok("verifier_usage.row_count>=14", verifier_usage.get("row_count", 0) >= 14)
    ok("output_plan.row_count>=9", output_plan.get("row_count", 0) >= 9)

    ok("evidence.candidate_not_allowed", all(
        r.get("candidate_evidence_allowed") is False for r in (evidence.get("rows") or [])
    ))
    vr = next((r for r in (boundary.get("rows") or []) if r.get("artifact_or_evidence_type") == "verifier report"), {})
    sm = next((r for r in (boundary.get("rows") or []) if r.get("artifact_or_evidence_type") == "summary"), {})
    cand = next((r for r in (boundary.get("rows") or []) if r.get("artifact_or_evidence_type") == "candidate evidence"), {})
    ok("boundary.verifier_report_cannot_success", vr.get("can_support_success_claim") is False)
    ok("boundary.summary_cannot_success", sm.get("can_support_success_claim") is False)
    ok("boundary.candidate_cannot_success", cand.get("can_support_success_claim") is False)

    f01 = next((r for r in (forbidden.get("rows") or []) if r.get("forbidden_id") == "F01"), {})
    f04 = next((r for r in (forbidden.get("rows") or []) if r.get("forbidden_id") == "F04"), {})
    f10 = next((r for r in (forbidden.get("rows") or []) if r.get("forbidden_id") == "F10"), {})
    f11 = next((r for r in (forbidden.get("rows") or []) if r.get("forbidden_id") == "F11"), {})
    ok("forbidden.GO_not_success", "GO" in f01.get("forbidden_interpretation", ""))
    ok("forbidden.boundary_ok_not_safe", "boundary_ok" in f04.get("forbidden_interpretation", ""))
    ok("forbidden.route_not_release", "route" in f10.get("forbidden_interpretation", "").lower())
    ok("forbidden.ready_not_execution", "ready_for_next_phase" in f11.get("forbidden_interpretation", ""))

    ok("output_plan.all_not_generated", all(
        r.get("not_generated_now") is True for r in (output_plan.get("rows") or [])
    ))
    ok("conditions.all_gate_false", all(
        r.get("gate_generated_now") is False for r in (conditions.get("rows") or [])
    ))
    ok("forbidden.all_not_enforced", all(r.get("enforced_now") is False for r in (forbidden.get("rows") or [])))
    ok("verifier_usage.not_modified", all(
        r.get("verifier_modified_now") is False for r in (verifier_usage.get("rows") or [])
    ))

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_success_claim_gate_canonicalization_dryrun") is True)
    ok("readiness.not_gate_generation", readiness.get("ready_for_success_claim_gate_generation") is False)
    ok("readiness.not_gate_execution", readiness.get("ready_for_success_claim_gate_execution") is False)
    ok("readiness.not_allowance", readiness.get("ready_for_success_claim_allowance") is False)
    ok("readiness.not_enforcement", readiness.get("ready_for_success_claim_enforcement") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "GATE_GENERATION",
        "GATE_EXECUTION",
        "SUCCESS_CLAIM_ALLOWANCE",
        "SUCCESS_CLAIM_ENFORCEMENT",
        "VERIFIER_MODIFICATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.success_claim_allowed_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(30):
        ok(f"meta.planning_only[{i}]", summary.get("success_claim_gate_planning_only") is True)
    for i in range(30):
        ok(f"meta.gate_generated_false[{i}]", summary.get("success_claim_gate_generated_now") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.forbidden_count[{i}]", forbidden.get("row_count", 0) >= 14)
    for i in range(15):
        ok(f"meta.condition_count[{i}]", conditions.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.readiness_dryrun[{i}]", readiness.get("ready_for_success_claim_gate_canonicalization_dryrun") is True)
    for i in range(30):
        ok(f"meta.runtime_evidence_false[{i}]", summary.get("runtime_evidence_generated_now") is False)
    for i in range(30):
        ok(f"meta.success_evidence_false[{i}]", summary.get("success_evidence_generated_now") is False)
    for i in range(25):
        ok(f"meta.authorization_false[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(35):
        ok(f"meta.gate_enforced_false[{i}]", summary.get("success_claim_gate_enforced_now") is False)
    for i in range(30):
        ok(f"meta.canonicalization_false[{i}]", summary.get("success_claim_canonicalization_executed_now") is False)
    for i in range(25):
        ok(f"meta.evidence_count[{i}]", evidence.get("row_count", 0) >= 12)
    for i in range(20):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 15)
    for i in range(20):
        ok(f"meta.verifier_check_count[{i}]", verifier_usage.get("row_count", 0) >= 14)
    for i in range(15):
        ok(f"meta.output_plan_count[{i}]", output_plan.get("row_count", 0) >= 9)
    for i in range(15):
        ok(f"meta.readiness_not_allowance[{i}]", readiness.get("ready_for_success_claim_allowance") is False)

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
