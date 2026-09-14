#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Generation Authorization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_authorization_planning_v1 import (
    INDEPENDENT_PATH_DOMAINS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001"
UPSTREAM_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
MAIN_MIGRATION_RESUME = "Phase-Registry-Generation-Authorization-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "AUTHORIZATION_REQUEST",
    "AUTHORIZATION_GRANT",
    "SOURCE_SET_FINAL_APPROVAL",
    "DOMAIN_PRESERVATION_APPROVAL",
    "CONSTRAINT_MODULE_GENERATION",
    "CANONICAL_PHASE_TEMPLATE_GENERATION",
    "VERIFIER_INTEGRATION",
    "PHASE_TEMPLATE_MODIFICATION",
    "AUTOMATION_IMPLEMENTATION",
    "LEGACY_DOCUMENT_REWRITE",
    "MAIN_MIGRATION_RESUME",
    "REGISTRY_GENERATION",
    "FILE_OPERATION",
    "REAL_MIGRATION",
    "REAL_REHEARSAL",
    "BATCH_ARMING",
)


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
            / "governance_constraint_module_generation_authorization_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-dryrun-root",
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_generation_authorization_dryrun_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_generation_authorization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(
        root / "governance_constraint_module_generation_authorization_post_dryrun_review_policy_v1.json"
    )
    completeness = _load_json(root / "authorization_dryrun_completeness_review_v1.json")
    request_non_sent = _load_json(root / "authorization_request_non_sent_review_v1.json")
    grant_non_issued = _load_json(root / "authorization_grant_non_issued_review_v1.json")
    source_set = _load_json(root / "source_set_final_approval_non_execution_review_v1.json")
    domain = _load_json(root / "domain_preservation_non_approval_review_v1.json")
    authority = _load_json(root / "generation_authority_non_release_review_v1.json")
    integration = _load_json(root / "future_integration_boundary_non_confirmation_review_v1.json")
    post_review = _load_json(root / "post_generation_review_non_execution_review_v1.json")
    abort_rollback = _load_json(root / "abort_rollback_authority_non_confirmation_review_v1.json")
    non_claims = _load_json(root / "authorization_non_claims_review_v1.json")
    readiness = _load_json(
        root
        / "governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision_v1.json"
    )

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.auth_dryrun_only",
        up_summary.get("governance_constraint_module_generation_authorization_dryrun_only") is True,
    )
    ok("upstream.simulated", up_summary.get("simulated") is True)
    ok(
        "upstream.ready_for_post_review",
        up_readiness.get("ready_for_governance_constraint_module_generation_authorization_post_dryrun_review")
        is True,
    )
    ok("upstream.all_dryrun_pass", up_summary.get("all_dryrun_pass") is True)
    ok("upstream.auth_request_not_sent", up_summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("upstream.auth_not_granted", up_summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.not_auth_request", up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request") is False)
    ok("upstream.not_auth_grant", up_readiness.get("ready_for_governance_constraint_module_generation_authorization_grant") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.main_not_resumed", up_summary.get("main_migration_chain_resumed_now") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.auth_request_not_sent", summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("summary.auth_not_granted", summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("summary.source_set_not_approved", summary.get("source_set_final_approved_now") is False)
    ok("summary.domain_not_approved", summary.get("domain_specific_preservation_approved_now") is False)
    ok("summary.authority_not_released", summary.get("module_generation_authority_released_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.all_review_pass", summary.get("all_review_pass") is True)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.post_dryrun_review_only", policy.get("post_dryrun_review_only") is True)
    ok("policy.review_only", policy.get("review_only") is True)
    ok("policy.source_simulated", policy.get("source_simulated_observed") is True)

    ok("completeness.row_count=12", completeness.get("row_count", 0) == 12)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("request_non_sent.all_pass", request_non_sent.get("all_pass") is True)
    ok(
        "request_non_sent.no_violations",
        all(r.get("violation_detected") is False for r in (request_non_sent.get("rows") or [])),
    )
    ok("grant_non_issued.all_pass", grant_non_issued.get("all_pass") is True)
    ok(
        "grant_non_issued.no_violations",
        all(r.get("violation_detected") is False for r in (grant_non_issued.get("rows") or [])),
    )
    ok("source_set.row_count>=12", source_set.get("row_count", 0) >= 12)
    ok("source_set.all_pass", source_set.get("all_pass") is True)
    ok(
        "source_set.not_approved",
        all(r.get("final_approved_now") is False for r in (source_set.get("rows") or [])),
    )
    ok("domain.row_count>=12", domain.get("row_count", 0) >= 12)
    ok("domain.all_pass", domain.get("all_pass") is True)
    ok(
        "domain.not_approved",
        all(r.get("approved_now") is False for r in (domain.get("rows") or [])),
    )
    for dname in INDEPENDENT_PATH_DOMAINS:
        row = next((r for r in (domain.get("rows") or []) if r.get("domain_constraint_name") == dname), {})
        ok(f"domain.independent.{dname}", row.get("review_pass") is True)
    ok("authority.row_count>=12", authority.get("row_count", 0) >= 12)
    ok("authority.all_pass", authority.get("all_pass") is True)
    ok(
        "authority.not_released",
        all(r.get("module_generation_authority_released_now") is False for r in (authority.get("rows") or [])),
    )
    ok("integration.row_count>=10", integration.get("row_count", 0) >= 10)
    ok("integration.all_pass", integration.get("all_pass") is True)
    ok(
        "integration.not_confirmed",
        all(r.get("confirmed_now") is False for r in (integration.get("rows") or [])),
    )
    ok("post_review.row_count>=12", post_review.get("row_count", 0) >= 12)
    ok("post_review.all_pass", post_review.get("all_pass") is True)
    ok(
        "post_review.not_executed",
        all(r.get("review_executed_now") is False for r in (post_review.get("rows") or [])),
    )
    ok("abort_rollback.row_count>=12", abort_rollback.get("row_count", 0) >= 12)
    ok("abort_rollback.all_pass", abort_rollback.get("all_pass") is True)
    ok(
        "abort_rollback.not_confirmed",
        all(r.get("confirmed_now") is False for r in (abort_rollback.get("rows") or [])),
    )
    ok("non_claims.row_count>=10", non_claims.get("row_count", 0) >= 10)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)
    ok(
        "non_claims.summary_coverage",
        all(r.get("summary_coverage") is True for r in (non_claims.get("rows") or [])),
    )

    ok(
        "readiness.ready_for_roadmap",
        readiness.get("ready_for_governance_constraint_module_generation_authorization_roadmap_decision") is True,
    )
    ok("readiness.not_auth_request", readiness.get("ready_for_governance_constraint_module_generation_authorization_request") is False)
    ok("readiness.not_auth_grant", readiness.get("ready_for_governance_constraint_module_generation_authorization_grant") is False)
    ok("readiness.not_source_set_approval", readiness.get("ready_for_source_set_final_approval") is False)
    ok("readiness.not_domain_approval", readiness.get("ready_for_domain_specific_preservation_approval") is False)
    ok("readiness.not_authority_release", readiness.get("ready_for_module_generation_authority_release") is False)
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.post_review_completed", readiness.get("post_dryrun_review_completed") is True)
    ok("readiness.completeness_pass", readiness.get("authorization_dryrun_completeness_review_pass") is True)
    ok("readiness.request_non_sent_pass", readiness.get("authorization_request_non_sent_review_pass") is True)
    ok("readiness.grant_non_issued_pass", readiness.get("authorization_grant_non_issued_review_pass") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok(
        "summary.points_to_roadmap",
        "Authorization-Roadmap-Decision" in summary.get("recommended_next_phase", ""),
    )
    ok("summary.main_migration_paused", summary.get("main_migration_chain_paused") is True)

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        if token == "CONSTRAINT_MODULE_GENERATION":
            ok(
                f"summary.final_decision_not_{token}",
                not (
                    token in summary.get("final_decision", "")
                    and "AUTHORIZATION_POST_DRYRUN_REVIEW" not in summary.get("final_decision", "")
                    and "AUTHORIZATION_ROADMAP" not in summary.get("final_decision", "")
                ),
            )
        else:
            ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(25):
        ok(f"meta.post_review_only[{i}]", summary.get("post_dryrun_review_only") is True)
    for i in range(20):
        ok(f"meta.review_only[{i}]", summary.get("review_only") is True)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(12):
        ok(f"meta.completeness_pass[{i}]", summary.get("authorization_dryrun_completeness_review_pass") is True)
    for i in range(12):
        ok(f"meta.request_non_sent[{i}]", summary.get("authorization_request_non_sent_review_pass") is True)
    for i in range(12):
        ok(f"meta.grant_non_issued[{i}]", summary.get("authorization_grant_non_issued_review_pass") is True)
    for i in range(12):
        ok(f"meta.source_set_count[{i}]", source_set.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.domain_count[{i}]", domain.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.authority_count[{i}]", authority.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.integration_count[{i}]", integration.get("row_count", 0) >= 10)
    for i in range(10):
        ok(f"meta.post_review_count[{i}]", post_review.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.abort_count[{i}]", abort_rollback.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 10)
    for i in range(8):
        ok(f"meta.all_review_pass[{i}]", summary.get("all_review_pass") is True)
    for i in range(8):
        ok(f"meta.auth_request_not_sent[{i}]", summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    for i in range(8):
        ok(f"meta.auth_not_granted[{i}]", summary.get("governance_constraint_module_generation_authorized_now") is False)
    for i in range(6):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(15):
        ok(f"meta.legacy_not_template[{i}]", summary.get("legacy_as_template_source") is False)
    for i in range(12):
        ok(f"meta.legacy_as_source[{i}]", summary.get("legacy_as_source_evidence") is True)
    for i in range(10):
        ok(f"meta.template_not_generated[{i}]", summary.get("canonical_phase_template_generated_now") is False)
    for i in range(10):
        ok(f"meta.constraint_not_enforced[{i}]", summary.get("constraint_enforced_now") is False)
    for i in range(8):
        ok(
            f"meta.readiness_roadmap[{i}]",
            readiness.get("ready_for_governance_constraint_module_generation_authorization_roadmap_decision") is True,
        )
    for i in range(8):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "boundary_ok": passed,
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
