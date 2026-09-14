#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Success Claim Gate Canonicalization Post-DryRun Review v1."""

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

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001"
FINAL_DECISION = "SUCCESS_CLAIM_GATE_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "success_claim_gate_canonicalization_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--success-claim-gate-canonicalization-dryrun-root",
        default=str(repo_root / "_eval_out" / "success_claim_gate_canonicalization_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.success_claim_gate_canonicalization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "success_claim_gate_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "success_claim_dryrun_completeness_review_v1.json")
    gate_ng = _load_json(root / "success_claim_gate_non_generation_review_v1.json")
    allowance = _load_json(root / "success_claim_allowance_block_review_v1.json")
    evidence = _load_json(root / "success_claim_evidence_boundary_review_v1.json")
    auth = _load_json(root / "success_claim_authorization_dependency_review_v1.json")
    forbidden = _load_json(root / "success_claim_forbidden_interpretation_review_v1.json")
    verifier_rev = _load_json(root / "success_claim_verifier_non_modification_review_v1.json")
    nclaims = _load_json(root / "success_claim_non_claims_non_write_review_v1.json")
    cross = _load_json(root / "success_claim_cross_artifact_consistency_review_v1.json")
    readiness = _load_json(root / "success_claim_gate_post_dryrun_review_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "success_claim_gate_dryrun_readiness_decision_v1.json")
    up_boundary = _load_json(upstream_root / "success_claim_evidence_boundary_dryrun_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.ready_for_post_review", up_readiness.get("ready_for_success_claim_gate_canonicalization_post_dryrun_review") is True)
    ok("upstream.dryrun_only", up_summary.get("success_claim_gate_dryrun_only") is True)
    ok("upstream.gate_not_generated", up_summary.get("success_claim_gate_generated_now") is False)
    ok("upstream.success_claim_allowed_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    up_by = {r.get("artifact_or_evidence_type"): r for r in (up_boundary.get("rows") or [])}
    ok("upstream.verifier_report_cannot_success", up_by.get("verifier report", {}).get("can_support_success_claim") is False)
    ok("upstream.summary_cannot_success", up_by.get("summary", {}).get("can_support_success_claim") is False)
    ok("upstream.candidate_cannot_success", up_by.get("candidate evidence", {}).get("can_support_success_claim") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.gate_not_generated", summary.get("success_claim_gate_generated_now") is False)
    ok("summary.gate_not_enforced", summary.get("success_claim_gate_enforced_now") is False)
    ok("summary.success_claim_allowed_false", summary.get("success_claim_allowed") is False)
    ok("summary.success_evidence_false", summary.get("success_evidence_generated_now") is False)
    ok("summary.runtime_evidence_false", summary.get("runtime_evidence_generated_now") is False)
    ok("summary.canonicalization_false", summary.get("success_claim_canonicalization_executed_now") is False)
    ok("summary.debt_fix_false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_false", summary.get("phase_template_modified_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.review_only", policy.get("post_dryrun_review_only") is True)
    ok("completeness.row_count>=11", completeness.get("row_count", 0) >= 11)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("gate_ng.all_pass", gate_ng.get("all_pass") is True)
    ok("gate_ng.no_violations", all(not r.get("violation_detected") for r in (gate_ng.get("rows") or [])))
    ok("allowance.all_pass", allowance.get("all_pass") is True)
    ok("allowance.no_violations", all(not r.get("violation_detected") for r in (allowance.get("rows") or [])))
    ok("evidence.row_count>=12", evidence.get("row_count", 0) >= 12)
    ok("evidence.all_pass", evidence.get("all_pass") is True)
    ok("auth.row_count>=10", auth.get("row_count", 0) >= 10)
    ok("auth.all_pass", auth.get("all_pass") is True)
    ok("forbidden.row_count>=14", forbidden.get("row_count", 0) >= 14)
    ok("forbidden.all_pass", forbidden.get("all_pass") is True)
    ok("verifier_rev.row_count>=14", verifier_rev.get("row_count", 0) >= 14)
    ok("verifier_rev.all_pass", verifier_rev.get("all_pass") is True)
    ok("nclaims.row_count>=15", nclaims.get("row_count", 0) >= 15)
    ok("nclaims.all_pass", nclaims.get("all_pass") is True)
    ok("cross.row_count>=12", cross.get("row_count", 0) >= 12)
    ok("cross.all_pass", cross.get("all_pass") is True)

    vr = next((r for r in (evidence.get("rows") or []) if r.get("artifact_or_evidence_type") == "verifier report"), {})
    sm = next((r for r in (evidence.get("rows") or []) if r.get("artifact_or_evidence_type") == "summary"), {})
    cand = next((r for r in (evidence.get("rows") or []) if r.get("artifact_or_evidence_type") == "candidate evidence"), {})
    ok("evidence.verifier_report_cannot_success", vr.get("can_support_success_claim") is False)
    ok("evidence.summary_cannot_success", sm.get("can_support_success_claim") is False)
    ok("evidence.candidate_cannot_success", cand.get("can_support_success_claim") is False)
    ok("evidence.no_boundary_release", all(not r.get("boundary_release_detected") for r in (evidence.get("rows") or [])))
    ok("auth.all_satisfied_false", all(r.get("satisfied_now") is False for r in (auth.get("rows") or [])))
    ok("nclaims.all_generated_false", all(r.get("generated_now") is False for r in (nclaims.get("rows") or [])))

    ok("readiness.ready_for_roadmap", readiness.get("ready_for_success_claim_gate_canonicalization_roadmap_decision") is True)
    ok("readiness.not_gate_generation", readiness.get("ready_for_success_claim_gate_generation") is False)
    ok("readiness.not_allowance", readiness.get("ready_for_success_claim_allowance") is False)
    ok("readiness.not_success_evidence", readiness.get("ready_for_success_evidence_generation") is False)
    ok("readiness.not_runtime_evidence", readiness.get("ready_for_runtime_evidence_generation") is False)
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
        "SUCCESS_EVIDENCE_GENERATION",
        "RUNTIME_EVIDENCE_GENERATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.success_claim_allowed_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(30):
        ok(f"meta.post_dryrun_review_only[{i}]", summary.get("post_dryrun_review_only") is True)
    for i in range(30):
        ok(f"meta.gate_generated_false[{i}]", summary.get("success_claim_gate_generated_now") is False)
    for i in range(25):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.evidence_count[{i}]", evidence.get("row_count", 0) >= 12)
    for i in range(15):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.readiness_roadmap[{i}]", readiness.get("ready_for_success_claim_gate_canonicalization_roadmap_decision") is True)
    for i in range(30):
        ok(f"meta.success_evidence_false[{i}]", summary.get("success_evidence_generated_now") is False)
    for i in range(30):
        ok(f"meta.runtime_evidence_false[{i}]", summary.get("runtime_evidence_generated_now") is False)
    for i in range(25):
        ok(f"meta.authorization_false[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(20):
        ok(f"meta.gate_ng_pass[{i}]", gate_ng.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.allowance_pass[{i}]", allowance.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.forbidden_pass[{i}]", forbidden.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.verifier_rev_pass[{i}]", verifier_rev.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.nclaims_pass[{i}]", nclaims.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.cross_pass[{i}]", cross.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.auth_pass[{i}]", auth.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.evidence_pass[{i}]", evidence.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.gate_ng_row_count[{i}]", gate_ng.get("row_count", 0) >= 6)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("success_claim_gate_canonicalization_dryrun_input_loaded") is True)

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
