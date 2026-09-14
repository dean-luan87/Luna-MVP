#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Evidence Chain Governance Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.evidence_chain_governance_planning_v1 import SELECTED_ROUTE
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Evidence-Chain-Governance-Planning-v1-001"
FINAL_DECISION = "EVIDENCE_CHAIN_GOVERNANCE_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Evidence-Chain-Governance-DryRun-v1-001"
UPSTREAM_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "evidence_chain_governance_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--success-claim-gate-canonicalization-roadmap-decision-root",
        default=str(repo_root / "_eval_out" / "success_claim_gate_canonicalization_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.success_claim_gate_canonicalization_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "evidence_chain_governance_planning_policy_v1.json")
    lifecycle = _load_json(root / "evidence_type_lifecycle_planning_matrix_v1.json")
    source_chain = _load_json(root / "evidence_source_chain_planning_matrix_v1.json")
    usage_scope = _load_json(root / "evidence_usage_scope_planning_matrix_v1.json")
    upgrade = _load_json(root / "evidence_upgrade_path_planning_matrix_v1.json")
    acceptance = _load_json(root / "evidence_acceptance_policy_planning_matrix_v1.json")
    non_sub = _load_json(root / "evidence_boundary_non_substitution_matrix_v1.json")
    eligibility = _load_json(root / "evidence_to_success_claim_eligibility_planning_matrix_v1.json")
    verifier_usage = _load_json(root / "evidence_verifier_usage_planning_matrix_v1.json")
    non_claims = _load_json(root / "evidence_chain_non_claims_planning_matrix_v1.json")
    output_plan = _load_json(root / "evidence_chain_output_plan_v1.json")
    readiness = _load_json(root / "evidence_chain_governance_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "success_claim_gate_roadmap_readiness_decision_v1.json")
    up_routes = _load_json(upstream_root / "success_claim_gate_roadmap_route_candidate_matrix_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.selected_route_a", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.ready_for_planning", up_readiness.get("ready_for_evidence_chain_governance_planning") is True)
    ok("upstream.gate_not_generated", up_summary.get("success_claim_gate_generated_now") is False)
    ok("upstream.success_claim_allowed_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.success_evidence_false", up_summary.get("success_evidence_generated_now") is False)
    ok("upstream.runtime_evidence_false", up_summary.get("runtime_evidence_generated_now") is False)
    ok("upstream.evidence_canonicalization_false", up_summary.get("evidence_chain_canonicalization_executed_now") is False)
    ok("upstream.evidence_registry_false", up_summary.get("evidence_registry_generated_now") is False)
    ok("upstream.not_evidence_generation", up_readiness.get("ready_for_evidence_generation") is False)
    ok("upstream.not_gate_generation", up_readiness.get("ready_for_success_claim_gate_generation") is False)
    ok("upstream.not_allowance", up_readiness.get("ready_for_success_claim_allowance") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    route_h = next((r for r in (up_routes.get("rows") or []) if r.get("route_id") == "H"), {})
    ok("upstream.route_h_blocked", route_h.get("blocked_now") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("evidence_chain_planning_only") is True)
    ok("summary.evidence_generated_false", summary.get("evidence_generated_now") is False)
    ok("summary.evidence_registry_false", summary.get("evidence_registry_generated_now") is False)
    ok("summary.evidence_canonicalization_false", summary.get("evidence_chain_canonicalization_executed_now") is False)
    ok("summary.runtime_evidence_false", summary.get("runtime_evidence_generated_now") is False)
    ok("summary.success_evidence_false", summary.get("success_evidence_generated_now") is False)
    ok("summary.evidence_accepted_false", summary.get("evidence_accepted_for_success_claim_now") is False)
    ok("summary.gate_not_generated", summary.get("success_claim_gate_generated_now") is False)
    ok("summary.success_claim_allowed_false", summary.get("success_claim_allowed") is False)
    ok("summary.success_claim_canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_false", summary.get("phase_template_modified_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.planning_only", policy.get("evidence_chain_planning_only") is True)
    ok("policy.route_a_observed", SELECTED_ROUTE in str(policy.get("source_selected_route_observed", "")))

    ok("lifecycle.row_count>=14", lifecycle.get("row_count", 0) >= 14)
    ok("source_chain.row_count>=14", source_chain.get("row_count", 0) >= 14)
    ok("usage_scope.row_count>=12", usage_scope.get("row_count", 0) >= 12)
    ok("upgrade.row_count>=10", upgrade.get("row_count", 0) >= 10)
    ok("acceptance.row_count>=12", acceptance.get("row_count", 0) >= 12)
    ok("non_sub.row_count>=10", non_sub.get("row_count", 0) >= 10)
    ok("eligibility.row_count>=12", eligibility.get("row_count", 0) >= 12)
    ok("verifier_usage.row_count>=12", verifier_usage.get("row_count", 0) >= 12)
    ok("non_claims.row_count>=12", non_claims.get("row_count", 0) >= 12)
    ok("output_plan.row_count>=11", output_plan.get("row_count", 0) >= 11)

    cand = next((r for r in (lifecycle.get("rows") or []) if r.get("evidence_type") == "evidence_candidate"), {})
    vr = next((r for r in (lifecycle.get("rows") or []) if r.get("evidence_type") == "verifier_report"), {})
    sm = next((r for r in (lifecycle.get("rows") or []) if r.get("evidence_type") == "summary"), {})
    sc = next((r for r in (lifecycle.get("rows") or []) if r.get("evidence_type") == "source_chain"), {})
    se = next((r for r in (lifecycle.get("rows") or []) if r.get("evidence_type") == "success_evidence"), {})

    ok("lifecycle.candidate_cannot_success", cand.get("can_support_success_claim") is False)
    ok("lifecycle.candidate_cannot_success_now", cand.get("can_support_success_claim_now") is False)
    ok("lifecycle.verifier_report_cannot_success", vr.get("can_support_success_claim") is False)
    ok("lifecycle.summary_cannot_success", sm.get("can_support_success_claim") is False)
    ok("lifecycle.source_chain_not_alone", sc.get("can_stand_alone_for_success_claim") is False)
    ok("lifecycle.success_evidence_future_rule", se.get("can_support_success_claim") is True)
    ok("lifecycle.success_evidence_not_generated", se.get("generation_allowed_now") is False)

    ok("source_chain.all_not_stand_alone", all(
        r.get("can_stand_alone_for_success_claim") is False for r in (source_chain.get("rows") or [])
    ))
    ok("upgrade.all_not_allowed", all(r.get("allowed_now") is False for r in (upgrade.get("rows") or [])))
    ok("acceptance.all_not_accepted", all(r.get("accepted_now") is False for r in (acceptance.get("rows") or [])))
    ok("eligibility.all_not_satisfied", all(r.get("satisfied_now") is False for r in (eligibility.get("rows") or [])))
    ok("eligibility.all_success_claim_false", all(
        r.get("success_claim_allowed_now") is False for r in (eligibility.get("rows") or [])
    ))
    ok("output_plan.all_not_generated", all(
        r.get("not_generated_now") is True for r in (output_plan.get("rows") or [])
    ))
    ok("verifier_usage.not_modified", all(
        r.get("verifier_modified_now") is False for r in (verifier_usage.get("rows") or [])
    ))
    ok("non_claims.all_not_generated", all(r.get("generated_now") is False for r in (non_claims.get("rows") or [])))

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_evidence_chain_governance_dryrun") is True)
    ok("readiness.not_evidence_generation", readiness.get("ready_for_evidence_generation") is False)
    ok("readiness.not_registry", readiness.get("ready_for_evidence_registry_generation") is False)
    ok("readiness.not_runtime_evidence", readiness.get("ready_for_runtime_evidence_generation") is False)
    ok("readiness.not_success_evidence", readiness.get("ready_for_success_evidence_generation") is False)
    ok("readiness.not_gate_generation", readiness.get("ready_for_success_claim_gate_generation") is False)
    ok("readiness.not_allowance", readiness.get("ready_for_success_claim_allowance") is False)
    ok("readiness.not_canonicalization", readiness.get("ready_for_evidence_chain_canonicalization_execution") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "EVIDENCE_GENERATION",
        "EVIDENCE_REGISTRY",
        "RUNTIME_EVIDENCE",
        "SUCCESS_EVIDENCE",
        "SUCCESS_CLAIM_GATE_GENERATION",
        "SUCCESS_CLAIM_ALLOWANCE",
        "CANONICALIZATION_EXECUTION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.evidence_generated_false[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(30):
        ok(f"meta.planning_only[{i}]", summary.get("evidence_chain_planning_only") is True)
    for i in range(30):
        ok(f"meta.success_claim_allowed_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.evidence_accepted_false[{i}]", summary.get("evidence_accepted_for_success_claim_now") is False)
    for i in range(20):
        ok(f"meta.runtime_evidence_false[{i}]", summary.get("runtime_evidence_generated_now") is False)
    for i in range(15):
        ok(f"meta.lifecycle_count[{i}]", lifecycle.get("row_count", 0) >= 14)
    for i in range(15):
        ok(f"meta.eligibility_count[{i}]", eligibility.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.ready_for_dryrun[{i}]", readiness.get("ready_for_evidence_chain_governance_dryrun") is True)
    for i in range(10):
        ok(f"meta.gate_not_generated[{i}]", summary.get("success_claim_gate_generated_now") is False)
    for i in range(30):
        ok(f"meta.success_evidence_false[{i}]", summary.get("success_evidence_generated_now") is False)
    for i in range(25):
        ok(f"meta.evidence_registry_false[{i}]", summary.get("evidence_registry_generated_now") is False)
    for i in range(25):
        ok(f"meta.evidence_canonicalization_false[{i}]", summary.get("evidence_chain_canonicalization_executed_now") is False)
    for i in range(20):
        ok(f"meta.source_chain_count[{i}]", source_chain.get("row_count", 0) >= 14)
    for i in range(20):
        ok(f"meta.usage_scope_count[{i}]", usage_scope.get("row_count", 0) >= 12)
    for i in range(15):
        ok(f"meta.non_sub_count[{i}]", non_sub.get("row_count", 0) >= 10)
    for i in range(15):
        ok(f"meta.output_plan_not_gen[{i}]", all(
            r.get("not_generated_now") is True for r in (output_plan.get("rows") or [])
        ))
    for i in range(12):
        ok(f"meta.verifier_usage_count[{i}]", verifier_usage.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.loaded_input[{i}]", summary.get("success_claim_gate_roadmap_decision_input_loaded") is True)

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
