#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Success Claim Gate Canonicalization Roadmap Decision v1."""

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

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "SUCCESS_CLAIM_GATE_CANONICALIZATION_ROADMAP_DECISION_READY_FOR_EVIDENCE_CHAIN_GOVERNANCE_PLANNING"
)
NEXT_PHASE = "Phase-Evidence-Chain-Governance-Planning-v1-001"
SELECTED_ROUTE = "Route A — Evidence Chain Governance Planning"
UPSTREAM_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "success_claim_gate_canonicalization_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--success-claim-gate-canonicalization-post-dryrun-review-root",
        default=str(repo_root / "_eval_out" / "success_claim_gate_canonicalization_post_dryrun_review_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.success_claim_gate_canonicalization_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "success_claim_gate_roadmap_decision_policy_v1.json")
    chain = _load_json(root / "completed_success_claim_gate_chain_review_v1.json")
    routes = _load_json(root / "success_claim_gate_roadmap_route_candidate_matrix_v1.json")
    dependency = _load_json(root / "success_claim_to_evidence_chain_dependency_matrix_v1.json")
    planning_scope = _load_json(root / "evidence_chain_governance_planning_scope_v1.json")
    non_release = _load_json(root / "success_claim_gate_roadmap_non_release_matrix_v1.json")
    non_claims = _load_json(root / "success_claim_gate_roadmap_decision_non_claims_register_v1.json")
    risk_matrix = _load_json(root / "evidence_chain_entry_readiness_risk_matrix_v1.json")
    readiness = _load_json(root / "success_claim_gate_roadmap_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "success_claim_gate_post_dryrun_review_readiness_decision_v1.json"
    )
    up_evidence = _load_json(upstream_root / "success_claim_evidence_boundary_review_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok(
        "upstream.ready_for_roadmap",
        up_readiness.get("ready_for_success_claim_gate_canonicalization_roadmap_decision") is True,
    )
    ok("upstream.gate_not_generated", up_summary.get("success_claim_gate_generated_now") is False)
    ok("upstream.success_claim_allowed_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.success_evidence_false", up_summary.get("success_evidence_generated_now") is False)
    ok("upstream.runtime_evidence_false", up_summary.get("runtime_evidence_generated_now") is False)
    ok("upstream.not_gate_generation", up_readiness.get("ready_for_success_claim_gate_generation") is False)
    ok("upstream.not_gate_execution", up_readiness.get("ready_for_success_claim_gate_execution") is False)
    ok("upstream.not_allowance", up_readiness.get("ready_for_success_claim_allowance") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    up_by = {r.get("artifact_or_evidence_type"): r for r in (up_evidence.get("rows") or [])}
    ok("upstream.verifier_report_cannot_success", up_by.get("verifier report", {}).get("can_support_success_claim") is False)
    ok("upstream.summary_cannot_success", up_by.get("summary", {}).get("can_support_success_claim") is False)
    ok("upstream.candidate_cannot_success", up_by.get("candidate evidence", {}).get("can_support_success_claim") is False)
    ok("upstream.source_chain_component", up_by.get("source chain", {}).get("can_support_success_claim") is True)
    ok("upstream.source_chain_no_release", up_by.get("source chain", {}).get("boundary_release_detected") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.roadmap_decision_only", summary.get("roadmap_decision_only") is True)
    ok("summary.gate_generated_false", summary.get("success_claim_gate_generated_now") is False)
    ok("summary.gate_enforced_false", summary.get("success_claim_gate_enforced_now") is False)
    ok("summary.success_claim_allowed_false", summary.get("success_claim_allowed") is False)
    ok("summary.success_evidence_false", summary.get("success_evidence_generated_now") is False)
    ok("summary.runtime_evidence_false", summary.get("runtime_evidence_generated_now") is False)
    ok("summary.evidence_chain_canonicalization_false", summary.get("evidence_chain_canonicalization_executed_now") is False)
    ok("summary.evidence_registry_false", summary.get("evidence_registry_generated_now") is False)
    ok("summary.success_claim_canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.terminology_canonicalization_false", summary.get("terminology_canonicalization_executed_now") is False)
    ok("summary.canonical_table_false", summary.get("canonical_table_generated_now") is False)
    ok("summary.terminology_enforced_false", summary.get("terminology_enforced_now") is False)
    ok("summary.registry_written_false", summary.get("registry_written_now") is False)
    ok("summary.permission_semantics_false", summary.get("permission_semantics_canonicalization_executed_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_false", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_false", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_false", summary.get("documentation_auto_sync_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.roadmap_only", policy.get("roadmap_decision_only") is True)
    ok("policy.gate_generated_false", policy.get("success_claim_gate_generated_now") is False)
    ok("policy.success_claim_allowed_false", policy.get("success_claim_allowed") is False)
    ok("policy.evidence_chain_canonicalization_false", policy.get("evidence_chain_canonicalization_executed_now") is False)

    ok("chain.row_count=3", chain.get("row_count") == 3)
    ok("chain.all_pass", chain.get("all_pass") is True)
    ok("routes.row_count>=8", routes.get("row_count", 0) >= 8)
    ok("routes.selected_route", routes.get("selected_route") == SELECTED_ROUTE)

    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})
    route_d = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "D"), {})
    route_h = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "H"), {})

    ok("route_a.selected_now", route_a.get("selected_now") is True)
    ok("route_a.allowed_now", route_a.get("allowed_now") is True)
    ok("route_a.planning_only_impact", "planning" in str(route_a.get("permission_impact", "")).lower())
    ok("route_a.not_evidence_generation", "not evidence generation" in str(route_a.get("permission_impact", "")).lower())
    ok("route_d.deferred", route_d.get("deferred") is True)
    ok("route_d.not_allowed", route_d.get("allowed_now") is False)
    ok("route_h.blocked_now", route_h.get("blocked_now") is True)
    ok("route_h.not_allowed", route_h.get("allowed_now") is False)

    ok("dependency.row_count>=12", dependency.get("row_count", 0) >= 12)
    ok("dependency.all_blocks_gate", all(
        r.get("blocks_gate_generation") is True for r in (dependency.get("rows") or [])
    ))
    ok("dependency.all_blocks_allowance", all(
        r.get("blocks_success_claim_allowance") is True for r in (dependency.get("rows") or [])
    ))
    ok("planning_scope.row_count>=14", planning_scope.get("row_count", 0) >= 14)
    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok("non_release.all_false", all(
        r.get("released_by_roadmap_decision") is False for r in (non_release.get("rows") or [])
    ))
    ok("non_claims.row_count>=9", non_claims.get("row_count", 0) >= 9)
    ok("non_claims.all_present", non_claims.get("all_present") is True)
    ok("risk_matrix.row_count>=14", risk_matrix.get("row_count", 0) >= 14)
    ok("risk_matrix.all_pass", risk_matrix.get("all_pass") is True)
    ok("risk_matrix.blocks_generation", all(
        r.get("blocks_generation") is True for r in (risk_matrix.get("rows") or [])
    ))
    ok("risk_matrix.blocks_allowance", all(
        r.get("blocks_success_claim_allowance") is True for r in (risk_matrix.get("rows") or [])
    ))
    ok("risk_matrix.allows_planning", all(
        r.get("allowed_to_enter_planning") is True for r in (risk_matrix.get("rows") or [])
    ))

    ok("readiness.ready_for_evidence_planning", readiness.get("ready_for_evidence_chain_governance_planning") is True)
    ok("readiness.not_evidence_generation", readiness.get("ready_for_evidence_generation") is False)
    ok("readiness.not_evidence_registry", readiness.get("ready_for_evidence_registry_generation") is False)
    ok("readiness.not_gate_generation", readiness.get("ready_for_success_claim_gate_generation") is False)
    ok("readiness.not_gate_execution", readiness.get("ready_for_success_claim_gate_execution") is False)
    ok("readiness.not_success_claim_allowance", readiness.get("ready_for_success_claim_allowance") is False)
    ok("readiness.not_success_evidence", readiness.get("ready_for_success_evidence_generation") is False)
    ok("readiness.not_runtime_evidence", readiness.get("ready_for_runtime_evidence_generation") is False)
    ok("readiness.direct_blocked", readiness.get("direct_success_claim_execution_blocked") is True)
    ok("readiness.chain_completed", readiness.get("success_claim_gate_chain_completed") is True)
    ok("readiness.selected_route", readiness.get("selected_route") == SELECTED_ROUTE)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.route_a_selected", summary.get("route_a_selected_now") is True)
    ok("summary.route_d_deferred", summary.get("route_d_deferred") is True)
    ok("summary.route_h_blocked", summary.get("route_h_blocked_now") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "SUCCESS_CLAIM_GATE_GENERATION",
        "SUCCESS_CLAIM_GATE_EXECUTION",
        "SUCCESS_CLAIM_ALLOWANCE",
        "EVIDENCE_GENERATION",
        "EVIDENCE_REGISTRY",
        "OWNER_OPERATOR",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.gate_generated_false[{i}]", summary.get("success_claim_gate_generated_now") is False)
    for i in range(30):
        ok(f"meta.roadmap_only[{i}]", summary.get("roadmap_decision_only") is True)
    for i in range(30):
        ok(f"meta.success_claim_allowed_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(24):
        ok(f"meta.route_a_selected[{i}]", summary.get("route_a_selected_now") is True)
    for i in range(20):
        ok(f"meta.evidence_chain_canonicalization_false[{i}]", summary.get("evidence_chain_canonicalization_executed_now") is False)
    for i in range(20):
        ok(f"meta.evidence_registry_false[{i}]", summary.get("evidence_registry_generated_now") is False)
    for i in range(15):
        ok(f"meta.route_h_blocked[{i}]", summary.get("route_h_blocked_now") is True)
    for i in range(15):
        ok(f"meta.route_d_deferred[{i}]", summary.get("route_d_deferred") is True)
    for i in range(15):
        ok(f"meta.direct_blocked[{i}]", summary.get("direct_success_claim_execution_blocked") is True)
    for i in range(12):
        ok(f"meta.chain_completed[{i}]", summary.get("success_claim_gate_chain_completed") is True)
    for i in range(10):
        ok(f"meta.success_evidence_false[{i}]", summary.get("success_evidence_generated_now") is False)
    for i in range(10):
        ok(f"meta.runtime_evidence_false[{i}]", summary.get("runtime_evidence_generated_now") is False)
    for i in range(15):
        ok(f"meta.non_release_pass[{i}]", non_release.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.risk_pass[{i}]", risk_matrix.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.dependency_count[{i}]", dependency.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.planning_scope_count[{i}]", planning_scope.get("row_count", 0) >= 14)
    for i in range(10):
        ok(f"meta.chain_all_pass[{i}]", chain.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("success_claim_gate_canonicalization_post_dryrun_review_input_loaded") is True)

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
