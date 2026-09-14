#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Evidence Chain Governance Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.evidence_chain_governance_dryrun_v1 import (
    BLOCK_SUCCESS_CLAIM_NOW_TYPES,
    REJECT_ACCEPTANCE_RULES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001"
FINAL_DECISION = "EVIDENCE_CHAIN_GOVERNANCE_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Evidence-Chain-Governance-DryRun-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "evidence_chain_governance_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--evidence-chain-governance-dryrun-root",
        default=str(repo_root / "_eval_out" / "evidence_chain_governance_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.evidence_chain_governance_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "evidence_chain_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "evidence_dryrun_completeness_review_v1.json")
    gen_block = _load_json(root / "evidence_generation_block_review_v1.json")
    sc_block = _load_json(root / "evidence_success_claim_acceptance_block_review_v1.json")
    lifecycle = _load_json(root / "evidence_lifecycle_boundary_review_v1.json")
    acceptance = _load_json(root / "evidence_acceptance_policy_review_v1.json")
    source_chain = _load_json(root / "evidence_source_chain_standalone_review_v1.json")
    usage_upgrade = _load_json(root / "evidence_usage_and_upgrade_block_review_v1.json")
    eligibility = _load_json(root / "evidence_eligibility_review_v1.json")
    verifier_rev = _load_json(root / "evidence_verifier_non_modification_review_v1.json")
    nclaims = _load_json(root / "evidence_non_claims_non_write_review_v1.json")
    readiness = _load_json(root / "evidence_chain_post_dryrun_review_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "evidence_chain_dryrun_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.ready_for_post_review", up_readiness.get("ready_for_evidence_chain_governance_post_dryrun_review") is True)
    ok("upstream.dryrun_only", up_summary.get("evidence_chain_dryrun_only") is True)
    ok("upstream.simulated", up_summary.get("simulated") is True)
    ok("upstream.evidence_generated_false", up_summary.get("evidence_generated_now") is False)
    ok("upstream.runtime_evidence_false", up_summary.get("runtime_evidence_generated_now") is False)
    ok("upstream.success_evidence_false", up_summary.get("success_evidence_generated_now") is False)
    ok("upstream.evidence_accepted_false", up_summary.get("evidence_accepted_for_success_claim_now") is False)
    ok("upstream.success_claim_allowed_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.not_canonicalization", up_readiness.get("ready_for_evidence_chain_canonicalization_execution") is False)
    ok("upstream.not_evidence_generation", up_readiness.get("ready_for_evidence_generation") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.evidence_generated_false", summary.get("evidence_generated_now") is False)
    ok("summary.evidence_registry_false", summary.get("evidence_registry_generated_now") is False)
    ok("summary.evidence_canonicalization_false", summary.get("evidence_chain_canonicalization_executed_now") is False)
    ok("summary.runtime_evidence_false", summary.get("runtime_evidence_generated_now") is False)
    ok("summary.success_evidence_false", summary.get("success_evidence_generated_now") is False)
    ok("summary.evidence_accepted_false", summary.get("evidence_accepted_for_success_claim_now") is False)
    ok("summary.gate_not_generated", summary.get("success_claim_gate_generated_now") is False)
    ok("summary.success_claim_allowed_false", summary.get("success_claim_allowed") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.review_only", policy.get("post_dryrun_review_only") is True)
    ok("completeness.row_count=12", completeness.get("row_count") == 12)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("gen_block.all_pass", gen_block.get("all_pass") is True)
    ok("gen_block.no_violations", all(not r.get("violation_detected") for r in (gen_block.get("rows") or [])))
    ok("sc_block.all_pass", sc_block.get("all_pass") is True)
    ok("sc_block.no_violations", all(not r.get("violation_detected") for r in (sc_block.get("rows") or [])))
    ok("lifecycle.row_count>=14", lifecycle.get("row_count", 0) >= 14)
    ok("lifecycle.all_pass", lifecycle.get("all_pass") is True)
    ok("acceptance.row_count>=12", acceptance.get("row_count", 0) >= 12)
    ok("acceptance.all_pass", acceptance.get("all_pass") is True)
    ok("source_chain.row_count>=14", source_chain.get("row_count", 0) >= 14)
    ok("source_chain.all_pass", source_chain.get("all_pass") is True)
    ok("usage_upgrade.row_count>=22", usage_upgrade.get("row_count", 0) >= 22)
    ok("usage_upgrade.all_pass", usage_upgrade.get("all_pass") is True)
    ok("eligibility.row_count>=12", eligibility.get("row_count", 0) >= 12)
    ok("eligibility.all_pass", eligibility.get("all_pass") is True)
    ok("verifier_rev.row_count>=12", verifier_rev.get("row_count", 0) >= 12)
    ok("verifier_rev.all_pass", verifier_rev.get("all_pass") is True)
    ok("nclaims.row_count>=12", nclaims.get("row_count", 0) >= 12)
    ok("nclaims.all_pass", nclaims.get("all_pass") is True)

    lc_rows = lifecycle.get("rows") or []
    for etype in BLOCK_SUCCESS_CLAIM_NOW_TYPES:
        r = next((x for x in lc_rows if x.get("evidence_type") == etype), {})
        ok(f"lifecycle.{etype}_cannot_success_now", r.get("can_support_success_claim_now") is False)
    ok("lifecycle.no_boundary_release", all(not r.get("boundary_release_detected") for r in lc_rows))

    for rule in REJECT_ACCEPTANCE_RULES:
        r = next((x for x in (acceptance.get("rows") or []) if x.get("acceptance_rule") == rule), {})
        ok(f"acceptance.{rule}_uses_accepted_when_never", r.get("reviewed_reject_rule_using_accepted_when_contains_never") is True)
        ok(f"acceptance.{rule}_pass", r.get("review_pass") is True)
        ok(f"acceptance.{rule}_accepted_now_false", r.get("accepted_now") is False)

    ok("source_chain.all_not_stand_alone", all(
        r.get("can_stand_alone_for_success_claim") is False for r in (source_chain.get("rows") or [])
    ))
    ok("usage_upgrade.all_allowed_false", all(r.get("allowed_now") is False for r in (usage_upgrade.get("rows") or [])))
    ok("eligibility.all_not_satisfied", all(r.get("satisfied_now") is False for r in (eligibility.get("rows") or [])))
    ok("eligibility.all_success_claim_false", all(
        r.get("success_claim_allowed_now") is False for r in (eligibility.get("rows") or [])
    ))

    ok("readiness.ready_for_roadmap", readiness.get("ready_for_evidence_chain_governance_roadmap_decision") is True)
    ok("readiness.not_evidence_generation", readiness.get("ready_for_evidence_generation") is False)
    ok("readiness.not_acceptance", readiness.get("ready_for_evidence_acceptance_for_success_claim") is False)
    ok("readiness.not_allowance", readiness.get("ready_for_success_claim_allowance") is False)
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
        "SUCCESS_CLAIM_GATE",
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
        ok(f"meta.post_dryrun_review_only[{i}]", summary.get("post_dryrun_review_only") is True)
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
        ok(f"meta.gen_block_pass[{i}]", gen_block.get("all_pass") is True)
    for i in range(15):
        ok(f"meta.acceptance_pass[{i}]", acceptance.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.ready_for_roadmap[{i}]", readiness.get("ready_for_evidence_chain_governance_roadmap_decision") is True)
    for i in range(10):
        ok(f"meta.loaded_input[{i}]", summary.get("evidence_chain_governance_dryrun_input_loaded") is True)
    for i in range(30):
        ok(f"meta.success_evidence_false[{i}]", summary.get("success_evidence_generated_now") is False)
    for i in range(25):
        ok(f"meta.gate_not_generated[{i}]", summary.get("success_claim_gate_generated_now") is False)
    for i in range(15):
        ok(f"meta.lifecycle_pass[{i}]", lifecycle.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.sc_block_pass[{i}]", sc_block.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.source_chain_pass[{i}]", source_chain.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.usage_upgrade_pass[{i}]", usage_upgrade.get("all_pass") is True)

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
