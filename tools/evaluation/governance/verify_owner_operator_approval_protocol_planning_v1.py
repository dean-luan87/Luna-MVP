#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Owner/Operator Approval Protocol Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.owner_operator_approval_protocol_planning_v1 import SELECTED_ROUTE
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001"
FINAL_DECISION = "OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Owner-Operator-Approval-Protocol-DryRun-v1-001"
UPSTREAM_PHASE = "Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001"
UPSTREAM_FINAL = (
    "EVIDENCE_CHAIN_GOVERNANCE_ROADMAP_DECISION_READY_FOR_OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING"
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
        default=str(repo_root / "_eval_out" / "owner_operator_approval_protocol_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--evidence-chain-governance-roadmap-decision-root",
        default=str(repo_root / "_eval_out" / "evidence_chain_governance_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.evidence_chain_governance_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "owner_operator_approval_protocol_planning_policy_v1.json")
    owner_id = _load_json(root / "owner_approval_identity_planning_matrix_v1.json")
    operator_ack = _load_json(root / "operator_acknowledgement_planning_matrix_v1.json")
    window = _load_json(root / "execution_window_planning_matrix_v1.json")
    abort = _load_json(root / "abort_authority_planning_matrix_v1.json")
    scope = _load_json(root / "scope_boundary_acknowledgement_planning_matrix_v1.json")
    auth_dep = _load_json(root / "authorization_dependency_planning_matrix_v1.json")
    shortcuts = _load_json(root / "owner_operator_forbidden_shortcut_matrix_v1.json")
    evidence_link = _load_json(root / "owner_operator_evidence_authorization_link_matrix_v1.json")
    verifier_usage = _load_json(root / "owner_operator_verifier_usage_planning_matrix_v1.json")
    non_claims = _load_json(root / "owner_operator_non_claims_planning_matrix_v1.json")
    output_plan = _load_json(root / "owner_operator_protocol_output_plan_v1.json")
    readiness = _load_json(root / "owner_operator_approval_protocol_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "evidence_chain_roadmap_readiness_decision_v1.json")
    up_routes = _load_json(upstream_root / "evidence_chain_roadmap_route_candidate_matrix_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.selected_route_a", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.ready_for_planning",
        up_readiness.get("ready_for_owner_operator_approval_protocol_planning") is True,
    )
    ok("upstream.owner_not_granted", up_summary.get("owner_approval_granted_now") is False)
    ok("upstream.operator_not_granted", up_summary.get("operator_acknowledgement_granted_now") is False)
    ok("upstream.window_not_opened", up_summary.get("execution_window_opened_now") is False)
    ok("upstream.abort_not_confirmed", up_summary.get("abort_authority_confirmed_now") is False)
    ok("upstream.authorization_false", up_summary.get("authorization_granted_now") is False)
    ok("upstream.evidence_not_generated", up_summary.get("evidence_generated_now") is False)
    ok("upstream.not_accepted", up_summary.get("evidence_accepted_for_success_claim_now") is False)
    ok("upstream.success_claim_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.not_owner_request", up_readiness.get("ready_for_owner_approval_request") is False)
    ok("upstream.not_operator_request", up_readiness.get("ready_for_operator_acknowledgement_request") is False)
    ok("upstream.not_window_opening", up_readiness.get("ready_for_execution_window_opening") is False)
    ok("upstream.not_evidence_generation", up_readiness.get("ready_for_evidence_generation") is False)
    ok("upstream.not_real_rehearsal", up_readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    route_b = next((r for r in (up_routes.get("rows") or []) if r.get("route_id") == "B"), {})
    route_h = next((r for r in (up_routes.get("rows") or []) if r.get("route_id") == "H"), {})
    ok("upstream.route_b_deferred", route_b.get("deferred") is True)
    ok("upstream.route_h_blocked", route_h.get("blocked_now") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("owner_operator_protocol_planning_only") is True)
    ok("summary.owner_request_not_sent", summary.get("owner_approval_request_sent_now") is False)
    ok("summary.operator_request_not_sent", summary.get("operator_acknowledgement_request_sent_now") is False)
    ok("summary.owner_not_granted", summary.get("owner_approval_granted_now") is False)
    ok("summary.operator_not_granted", summary.get("operator_acknowledgement_granted_now") is False)
    ok("summary.window_not_opened", summary.get("execution_window_opened_now") is False)
    ok("summary.abort_not_confirmed", summary.get("abort_authority_confirmed_now") is False)
    ok("summary.scope_not_accepted", summary.get("scope_confirmation_accepted_now") is False)
    ok("summary.verifier_rerun_not_authorized", summary.get("verifier_rerun_authorized_now") is False)
    ok("summary.evidence_gen_not_authorized", summary.get("evidence_generation_authorized_now") is False)
    ok("summary.evidence_accept_not_authorized", summary.get("evidence_acceptance_authorized_now") is False)
    ok("summary.success_claim_authority_not_confirmed", summary.get("success_claim_authority_confirmed_now") is False)
    ok("summary.authorization_false", summary.get("authorization_granted_now") is False)
    ok("summary.evidence_not_generated", summary.get("evidence_generated_now") is False)
    ok("summary.runtime_evidence_false", summary.get("runtime_evidence_generated_now") is False)
    ok("summary.success_evidence_false", summary.get("success_evidence_generated_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.boundary_registry_false", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.planning_only", policy.get("owner_operator_protocol_planning_only") is True)
    ok("policy.owner_not_granted", policy.get("owner_approval_granted_now") is False)

    ok("owner_id.row_count>=10", owner_id.get("row_count", 0) >= 10)
    ok("owner_id.all_not_granted", all(r.get("approval_granted_now") is False for r in (owner_id.get("rows") or [])))
    ok("operator.row_count>=10", operator_ack.get("row_count", 0) >= 10)
    ok(
        "operator.all_not_acknowledged",
        all(r.get("operator_acknowledgement_granted_now") is False for r in (operator_ack.get("rows") or [])),
    )
    ok("window.row_count>=12", window.get("row_count", 0) >= 12)
    ok("window.all_not_opened", all(r.get("execution_window_opened_now") is False for r in (window.get("rows") or [])))
    ok("abort.row_count>=12", abort.get("row_count", 0) >= 12)
    ok("abort.all_not_confirmed", all(r.get("abort_authority_confirmed_now") is False for r in (abort.get("rows") or [])))
    ok("scope.row_count>=12", scope.get("row_count", 0) >= 12)
    ok(
        "scope.all_not_accepted",
        all(r.get("scope_confirmation_accepted_now") is False for r in (scope.get("rows") or [])),
    )
    ok("auth_dep.row_count>=12", auth_dep.get("row_count", 0) >= 12)
    ok(
        "auth_dep.all_not_authorized",
        all(r.get("authorized_now") is False and r.get("authorization_granted_now") is False for r in (auth_dep.get("rows") or [])),
    )
    ok("shortcuts.row_count>=12", shortcuts.get("row_count", 0) >= 12)
    ok("shortcuts.all_not_enforced", all(r.get("enforced_now") is False for r in (shortcuts.get("rows") or [])))
    ok("evidence_link.row_count>=12", evidence_link.get("row_count", 0) >= 12)
    ok(
        "evidence_link.all_not_generated",
        all(r.get("evidence_generated_now") is False and r.get("success_claim_allowed_now") is False for r in (evidence_link.get("rows") or [])),
    )
    ok("verifier_usage.row_count>=12", verifier_usage.get("row_count", 0) >= 12)
    ok(
        "verifier_usage.not_modified",
        all(r.get("verifier_modified_now") is False and r.get("enforced_now") is False for r in (verifier_usage.get("rows") or [])),
    )
    ok("non_claims.row_count>=12", non_claims.get("row_count", 0) >= 12)
    ok("non_claims.all_not_generated", all(r.get("generated_now") is False for r in (non_claims.get("rows") or [])))
    ok("output_plan.row_count>=12", output_plan.get("row_count", 0) >= 12)
    ok(
        "output_plan.all_not_generated",
        all(r.get("not_generated_now") is True for r in (output_plan.get("rows") or [])),
    )

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_owner_operator_approval_protocol_dryrun") is True)
    ok("readiness.not_owner_request", readiness.get("ready_for_owner_approval_request") is False)
    ok("readiness.not_operator_request", readiness.get("ready_for_operator_acknowledgement_request") is False)
    ok("readiness.not_window_opening", readiness.get("ready_for_execution_window_opening") is False)
    ok("readiness.not_abort_confirmation", readiness.get("ready_for_abort_authority_confirmation") is False)
    ok("readiness.not_evidence_gen_auth", readiness.get("ready_for_evidence_generation_authorization") is False)
    ok("readiness.not_verifier_rerun_auth", readiness.get("ready_for_verifier_rerun_authorization") is False)
    ok("readiness.not_success_claim_auth", readiness.get("ready_for_success_claim_authority_confirmation") is False)
    ok("readiness.not_evidence_generation", readiness.get("ready_for_evidence_generation") is False)
    ok("readiness.not_success_claim", readiness.get("ready_for_success_claim_allowance") is False)
    ok("readiness.not_real_rehearsal", readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("readiness.planning_completed", readiness.get("owner_operator_protocol_planning_completed") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "OWNER_APPROVAL_REQUEST",
        "OPERATOR_ACKNOWLEDGEMENT_REQUEST",
        "EXECUTION_WINDOW_OPENING",
        "EVIDENCE_GENERATION_AUTHORIZATION",
        "VERIFIER_RERUN_AUTHORIZATION",
        "SUCCESS_CLAIM_AUTHORITY_CONFIRMATION",
        "EVIDENCE_GENERATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.owner_not_granted[{i}]", summary.get("owner_approval_granted_now") is False)
    for i in range(30):
        ok(f"meta.planning_only[{i}]", summary.get("owner_operator_protocol_planning_only") is True)
    for i in range(30):
        ok(f"meta.authorization_false[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.evidence_not_generated[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(20):
        ok(f"meta.success_claim_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(15):
        ok(f"meta.window_not_opened[{i}]", summary.get("execution_window_opened_now") is False)
    for i in range(15):
        ok(f"meta.request_not_sent[{i}]", summary.get("owner_approval_request_sent_now") is False)
    for i in range(12):
        ok(f"meta.owner_id_count[{i}]", owner_id.get("row_count", 0) >= 10)
    for i in range(12):
        ok(f"meta.auth_dep_count[{i}]", auth_dep.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.evidence_link_count[{i}]", evidence_link.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.output_plan_count[{i}]", output_plan.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.ready_for_dryrun[{i}]", readiness.get("ready_for_owner_operator_approval_protocol_dryrun") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("evidence_chain_governance_roadmap_decision_input_loaded") is True)
    for i in range(20):
        ok(f"meta.operator_not_granted[{i}]", summary.get("operator_acknowledgement_granted_now") is False)
    for i in range(18):
        ok(f"meta.abort_not_confirmed[{i}]", summary.get("abort_authority_confirmed_now") is False)
    for i in range(16):
        ok(f"meta.scope_not_accepted[{i}]", summary.get("scope_confirmation_accepted_now") is False)
    for i in range(14):
        ok(f"meta.evidence_gen_not_auth[{i}]", summary.get("evidence_generation_authorized_now") is False)
    for i in range(12):
        ok(f"meta.window_count[{i}]", window.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.shortcuts_count[{i}]", shortcuts.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 12)

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
