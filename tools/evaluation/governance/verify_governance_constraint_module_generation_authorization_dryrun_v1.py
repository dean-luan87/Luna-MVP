#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Generation Authorization DryRun v1."""

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

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001"
FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001"
UPSTREAM_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
MAIN_MIGRATION_RESUME = "Phase-Registry-Generation-Authorization-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "AUTHORIZATION_REQUEST",
    "AUTHORIZATION_GRANT",
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
            repo_root / "_eval_out" / "governance_constraint_module_generation_authorization_dryrun_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-planning-root",
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_generation_authorization_planning_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_generation_authorization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "governance_constraint_module_generation_authorization_dryrun_policy_v1.json")
    request_schema = _load_json(root / "authorization_request_schema_consumption_dryrun_v1.json")
    grant_schema = _load_json(root / "authorization_grant_schema_consumption_dryrun_v1.json")
    source_set = _load_json(root / "source_set_final_approval_authority_dryrun_v1.json")
    domain_preservation = _load_json(root / "domain_specific_preservation_approval_dryrun_v1.json")
    authority_matrix = _load_json(root / "module_generation_authority_dryrun_v1.json")
    integration_boundary = _load_json(root / "future_integration_boundary_dryrun_v1.json")
    post_review = _load_json(root / "post_generation_review_authority_dryrun_v1.json")
    abort_rollback = _load_json(root / "abort_and_rollback_authority_dryrun_v1.json")
    verifier_usage = _load_json(root / "authorization_verifier_usage_dryrun_v1.json")
    non_claims = _load_json(root / "authorization_non_claims_generation_dryrun_v1.json")
    readiness = _load_json(
        root / "governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json"
    )

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "governance_constraint_module_generation_authorization_planning_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.auth_planning_only",
        up_summary.get("governance_constraint_module_generation_authorization_planning_only") is True,
    )
    ok(
        "upstream.ready_for_dryrun",
        up_readiness.get("ready_for_governance_constraint_module_generation_authorization_dryrun") is True,
    )
    ok("upstream.auth_request_not_sent", up_summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("upstream.auth_not_granted", up_summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("upstream.source_set_not_approved", up_summary.get("source_set_final_approved_now") is False)
    ok("upstream.domain_not_approved", up_summary.get("domain_specific_preservation_approved_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.all_not_generated", up_summary.get("all_not_generated_now") is True)
    ok("upstream.not_auth_request", up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request") is False)
    ok("upstream.not_auth_grant", up_readiness.get("ready_for_governance_constraint_module_generation_authorization_grant") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.main_not_resumed", up_summary.get("main_migration_chain_resumed_now") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)
    ok("upstream.domain_rules_preserved", up_summary.get("domain_specific_rules_preserved") is True)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok(
        "summary.auth_dryrun_only",
        summary.get("governance_constraint_module_generation_authorization_dryrun_only") is True,
    )
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.auth_request_not_sent", summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("summary.auth_not_granted", summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("summary.source_set_not_approved", summary.get("source_set_final_approved_now") is False)
    ok("summary.domain_not_approved", summary.get("domain_specific_preservation_approved_now") is False)
    ok("summary.authority_not_released", summary.get("module_generation_authority_released_now") is False)
    ok("summary.verifier_boundary_not_confirmed", summary.get("future_verifier_integration_boundary_confirmed_now") is False)
    ok("summary.template_boundary_not_confirmed", summary.get("future_phase_template_integration_boundary_confirmed_now") is False)
    ok("summary.post_review_not_executed", summary.get("post_generation_review_executed_now") is False)
    ok("summary.abort_not_confirmed", summary.get("module_generation_abort_authority_confirmed_now") is False)
    ok("summary.rollback_not_confirmed", summary.get("module_generation_rollback_authority_confirmed_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.module_not_registered", summary.get("constraint_module_registered_now") is False)
    ok("summary.constraint_not_enforced", summary.get("constraint_enforced_now") is False)
    ok("summary.verifier_integration_not_executed", summary.get("verifier_integration_executed_now") is False)
    ok("summary.verifier_not_modified", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_not_modified", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_not_implemented", summary.get("automation_implemented_now") is False)
    ok("summary.legacy_not_modified", summary.get("legacy_phase_modified_now") is False)
    ok("summary.legacy_as_source", summary.get("legacy_as_source_evidence") is True)
    ok("summary.legacy_not_template", summary.get("legacy_as_template_source") is False)
    ok("summary.domain_rules_preserved", summary.get("domain_specific_rules_preserved") is True)
    ok("summary.frozen_not_enforced", summary.get("frozen_fields_enforced_now") is False)
    ok("summary.baseline_not_integrated", summary.get("verifier_baseline_integrated_now") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.authorization_not_granted", summary.get("authorization_granted_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.all_dryrun_pass", summary.get("all_dryrun_pass") is True)
    ok("summary.domain_differentiation", summary.get("domain_differentiation_preserved") is True)
    ok("summary.independent_paths", summary.get("independent_consumption_paths_verified") is True)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok(
        "policy.auth_dryrun_only",
        policy.get("governance_constraint_module_generation_authorization_dryrun_only") is True,
    )
    ok("policy.simulated", policy.get("simulated") is True)
    ok("policy.source_verifier_go", policy.get("source_verifier_go_observed") is True)
    ok("policy.source_boundary_ok", policy.get("source_boundary_ok_observed") is True)
    ok("policy.auth_request_not_sent", policy.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("request_schema.row_count>=12", request_schema.get("row_count", 0) >= 12)
    ok("request_schema.all_pass", request_schema.get("all_pass") is True)
    ok(
        "request_schema.simulated_consumption",
        all(r.get("simulated_schema_consumption") is True for r in (request_schema.get("rows") or [])),
    )
    ok(
        "request_schema.not_sent",
        all(r.get("request_sent_now") is False for r in (request_schema.get("rows") or [])),
    )
    ok(
        "request_schema.not_generated",
        all(r.get("authorization_request_generated_now") is False for r in (request_schema.get("rows") or [])),
    )
    ok("grant_schema.row_count>=12", grant_schema.get("row_count", 0) >= 12)
    ok("grant_schema.all_pass", grant_schema.get("all_pass") is True)
    ok(
        "grant_schema.simulated_consumption",
        all(r.get("simulated_schema_consumption") is True for r in (grant_schema.get("rows") or [])),
    )
    ok(
        "grant_schema.not_issued",
        all(r.get("grant_issued_now") is False for r in (grant_schema.get("rows") or [])),
    )
    ok(
        "grant_schema.not_granted",
        all(r.get("authorization_granted_now") is False for r in (grant_schema.get("rows") or [])),
    )
    ok("source_set.row_count>=12", source_set.get("row_count", 0) >= 12)
    ok("source_set.all_pass", source_set.get("all_pass") is True)
    ok(
        "source_set.simulated_check",
        all(r.get("simulated_approval_check") is True for r in (source_set.get("rows") or [])),
    )
    ok(
        "source_set.not_approved",
        all(r.get("final_approved_now") is False for r in (source_set.get("rows") or [])),
    )
    ok("domain.row_count>=12", domain_preservation.get("row_count", 0) >= 12)
    ok("domain.all_pass", domain_preservation.get("all_pass") is True)
    ok("domain.differentiation_preserved", domain_preservation.get("domain_differentiation_preserved") is True)
    ok("domain.independent_paths", domain_preservation.get("independent_consumption_paths_verified") is True)
    for dname in INDEPENDENT_PATH_DOMAINS:
        row = next(
            (r for r in (domain_preservation.get("rows") or []) if r.get("domain_constraint_name") == dname),
            {},
        )
        ok(
            f"domain.independent.{dname}",
            row.get("independent_consumption_path_required") is True and row.get("dryrun_status") == "pass",
        )
    ok(
        "domain.not_approved",
        all(r.get("approved_now") is False for r in (domain_preservation.get("rows") or [])),
    )
    ok("authority.row_count>=12", authority_matrix.get("row_count", 0) >= 12)
    ok("authority.all_pass", authority_matrix.get("all_pass") is True)
    ok(
        "authority.simulated_check",
        all(r.get("simulated_authority_check") is True for r in (authority_matrix.get("rows") or [])),
    )
    ok(
        "authority.not_authorized",
        all(r.get("authorized_now") is False for r in (authority_matrix.get("rows") or [])),
    )
    ok("integration.row_count>=10", integration_boundary.get("row_count", 0) >= 10)
    ok("integration.all_pass", integration_boundary.get("all_pass") is True)
    ok(
        "integration.simulated_check",
        all(r.get("simulated_boundary_check") is True for r in (integration_boundary.get("rows") or [])),
    )
    ok(
        "integration.not_confirmed",
        all(r.get("confirmed_now") is False for r in (integration_boundary.get("rows") or [])),
    )
    ok("post_review.row_count>=12", post_review.get("row_count", 0) >= 12)
    ok("post_review.all_pass", post_review.get("all_pass") is True)
    ok(
        "post_review.simulated_check",
        all(r.get("simulated_review_authority_check") is True for r in (post_review.get("rows") or [])),
    )
    ok(
        "post_review.not_executed",
        all(r.get("review_executed_now") is False for r in (post_review.get("rows") or [])),
    )
    ok("abort_rollback.row_count>=12", abort_rollback.get("row_count", 0) >= 12)
    ok("abort_rollback.all_pass", abort_rollback.get("all_pass") is True)
    ok(
        "abort_rollback.simulated_check",
        all(r.get("simulated_authority_check") is True for r in (abort_rollback.get("rows") or [])),
    )
    ok(
        "abort_rollback.not_confirmed",
        all(r.get("confirmed_now") is False for r in (abort_rollback.get("rows") or [])),
    )
    ok("verifier_usage.row_count>=12", verifier_usage.get("row_count", 0) >= 12)
    ok("verifier_usage.all_pass", verifier_usage.get("all_pass") is True)
    ok(
        "verifier_usage.simulated",
        all(r.get("simulated_verifier_usage") is True for r in (verifier_usage.get("rows") or [])),
    )
    ok("verifier_usage.not_modified", verifier_usage.get("verifier_modified_now") is False)
    ok("non_claims.row_count>=10", non_claims.get("row_count", 0) >= 10)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)
    ok(
        "non_claims.simulated",
        all(r.get("simulated_generation") is True for r in (non_claims.get("rows") or [])),
    )
    ok(
        "non_claims.not_generated",
        all(r.get("generated_now") is False for r in (non_claims.get("rows") or [])),
    )

    ok(
        "readiness.ready_for_post_review",
        readiness.get("ready_for_governance_constraint_module_generation_authorization_post_dryrun_review") is True,
    )
    ok("readiness.not_auth_request", readiness.get("ready_for_governance_constraint_module_generation_authorization_request") is False)
    ok("readiness.not_auth_grant", readiness.get("ready_for_governance_constraint_module_generation_authorization_grant") is False)
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.dryrun_completed", readiness.get("authorization_dryrun_completed") is True)
    ok("readiness.request_schema_pass", readiness.get("authorization_request_schema_dryrun_pass") is True)
    ok("readiness.grant_schema_pass", readiness.get("authorization_grant_schema_dryrun_pass") is True)
    ok("readiness.source_set_pass", readiness.get("source_set_final_approval_authority_dryrun_pass") is True)
    ok("readiness.domain_pass", readiness.get("domain_specific_preservation_approval_dryrun_pass") is True)
    ok("readiness.authority_pass", readiness.get("module_generation_authority_dryrun_pass") is True)
    ok("readiness.integration_pass", readiness.get("future_integration_boundary_dryrun_pass") is True)
    ok("readiness.post_review_pass", readiness.get("post_generation_review_authority_dryrun_pass") is True)
    ok("readiness.abort_rollback_pass", readiness.get("abort_and_rollback_authority_dryrun_pass") is True)
    ok("readiness.verifier_usage_pass", readiness.get("verifier_usage_dryrun_pass") is True)
    ok("readiness.non_claims_pass", readiness.get("non_claims_generation_dryrun_pass") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.points_to_post_review", "Authorization-Post-DryRun-Review" in summary.get("recommended_next_phase", ""))
    ok("summary.main_migration_paused", summary.get("main_migration_chain_paused") is True)
    ok("summary.main_migration_resume_phase", summary.get("main_migration_resume_phase") == MAIN_MIGRATION_RESUME)
    ok(
        "summary.planning_input_loaded",
        summary.get("governance_constraint_module_generation_authorization_planning_input_loaded") is True,
    )

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        if token == "CONSTRAINT_MODULE_GENERATION":
            ok(
                f"summary.final_decision_not_{token}",
                not (
                    token in summary.get("final_decision", "")
                    and "AUTHORIZATION_DRYRUN" not in summary.get("final_decision", "")
                    and "AUTHORIZATION_PLANNING" not in summary.get("final_decision", "")
                ),
            )
        else:
            ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(25):
        ok(
            f"meta.auth_dryrun_only[{i}]",
            summary.get("governance_constraint_module_generation_authorization_dryrun_only") is True,
        )
    for i in range(25):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(12):
        ok(f"meta.request_count[{i}]", request_schema.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.grant_count[{i}]", grant_schema.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.source_set_count[{i}]", source_set.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.domain_count[{i}]", domain_preservation.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.authority_count[{i}]", authority_matrix.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.integration_count[{i}]", integration_boundary.get("row_count", 0) >= 10)
    for i in range(10):
        ok(f"meta.post_review_count[{i}]", post_review.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.abort_count[{i}]", abort_rollback.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.verifier_usage_count[{i}]", verifier_usage.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 10)
    for i in range(8):
        ok(f"meta.all_dryrun_pass[{i}]", summary.get("all_dryrun_pass") is True)
    for i in range(8):
        ok(f"meta.auth_request_not_sent[{i}]", summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    for i in range(8):
        ok(f"meta.auth_not_granted[{i}]", summary.get("governance_constraint_module_generation_authorized_now") is False)
    for i in range(8):
        ok(f"meta.source_set_not_approved[{i}]", summary.get("source_set_final_approved_now") is False)
    for i in range(8):
        ok(f"meta.domain_not_approved[{i}]", summary.get("domain_specific_preservation_approved_now") is False)
    for i in range(8):
        ok(f"meta.authority_not_released[{i}]", summary.get("module_generation_authority_released_now") is False)
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
    for i in range(12):
        ok(f"meta.verifier_integration_not_executed[{i}]", summary.get("verifier_integration_executed_now") is False)
    for i in range(12):
        ok(f"meta.automation_not_implemented[{i}]", summary.get("automation_implemented_now") is False)
    for i in range(10):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(8):
        ok(
            f"meta.readiness_post_review[{i}]",
            readiness.get("ready_for_governance_constraint_module_generation_authorization_post_dryrun_review") is True,
        )
    for i in range(8):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(8):
        ok(f"meta.domain_rules_preserved[{i}]", summary.get("domain_specific_rules_preserved") is True)
    for i in range(8):
        ok(f"meta.frozen_not_enforced[{i}]", summary.get("frozen_fields_enforced_now") is False)

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
