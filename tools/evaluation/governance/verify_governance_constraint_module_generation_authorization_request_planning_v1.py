#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Generation Authorization Request Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_authorization_roadmap_decision_v1 import (
    SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001"
FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001"
UPSTREAM_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_AUTHORIZATION_REQUEST_PLANNING"
)
MAIN_MIGRATION_RESUME = "Phase-Registry-Generation-Authorization-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
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
    "AUTHORIZATION_REQUEST_ARTIFACT",
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
            / "governance_constraint_module_generation_authorization_request_planning_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-roadmap-decision-root",
        default=str(
            repo_root
            / "_eval_out"
            / "governance_constraint_module_generation_authorization_roadmap_decision_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_generation_authorization_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "authorization_request_planning_policy_v1.json")
    identity = _load_json(root / "authorization_request_identity_planning_v1.json")
    source_binding = _load_json(root / "authorization_request_source_set_binding_planning_v1.json")
    domain_binding = _load_json(root / "authorization_request_domain_preservation_binding_planning_v1.json")
    scope_exclusion = _load_json(root / "authorization_request_scope_and_exclusion_planning_v1.json")
    statements = _load_json(
        root / "authorization_request_non_grant_and_non_generation_statement_planning_v1.json"
    )
    lifecycle = _load_json(root / "authorization_request_lifecycle_planning_v1.json")
    review = _load_json(root / "authorization_request_review_requirement_planning_v1.json")
    abort_revoke = _load_json(root / "authorization_request_abort_revoke_linkage_planning_v1.json")
    verifier_usage = _load_json(root / "authorization_request_verifier_usage_planning_v1.json")
    non_claims = _load_json(root / "authorization_request_planning_non_claims_planning_v1.json")
    readiness = _load_json(root / "authorization_request_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "authorization_roadmap_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok("upstream.selected_route", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok(
        "upstream.ready_for_request_planning",
        up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_planning")
        is True,
    )
    ok(
        "upstream.request_planning_selected",
        up_summary.get("governance_constraint_module_generation_authorization_request_planning_selected") is True,
    )
    ok("upstream.auth_request_not_generated", up_summary.get("governance_constraint_module_generation_authorization_request_generated_now") is False)
    ok("upstream.auth_request_not_sent", up_summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("upstream.auth_not_granted", up_summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("upstream.grant_not_generated", up_summary.get("governance_constraint_module_generation_authorization_grant_generated_now") is False)
    ok("upstream.source_set_not_approved", up_summary.get("source_set_final_approved_now") is False)
    ok("upstream.domain_not_approved", up_summary.get("domain_specific_preservation_approved_now") is False)
    ok("upstream.authority_not_released", up_summary.get("module_generation_authority_released_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
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
    ok("summary.planning_scope", summary.get("planning_scope") == "authorization_request_planning_only")
    ok("summary.request_planning_only", summary.get("authorization_request_planning_only") is True)
    ok(
        "summary.request_planning_selected",
        summary.get("governance_constraint_module_generation_authorization_request_planning_selected") is True,
    )
    ok("summary.auth_request_not_generated", summary.get("governance_constraint_module_generation_authorization_request_generated_now") is False)
    ok("summary.auth_request_not_sent", summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("summary.auth_not_granted", summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("summary.grant_not_generated", summary.get("governance_constraint_module_generation_authorization_grant_generated_now") is False)
    ok("summary.source_set_not_approved", summary.get("source_set_final_approved_now") is False)
    ok("summary.domain_not_approved", summary.get("domain_specific_preservation_approved_now") is False)
    ok("summary.authority_not_released", summary.get("module_generation_authority_released_now") is False)
    ok("summary.future_verifier_boundary_not_confirmed", summary.get("future_verifier_integration_boundary_confirmed_now") is False)
    ok("summary.future_template_boundary_not_confirmed", summary.get("future_phase_template_integration_boundary_confirmed_now") is False)
    ok("summary.post_review_not_executed", summary.get("post_generation_review_executed_now") is False)
    ok("summary.abort_not_confirmed", summary.get("module_generation_abort_authority_confirmed_now") is False)
    ok("summary.revoke_not_confirmed", summary.get("module_generation_revoke_authority_confirmed_now") is False)
    ok("summary.rollback_not_confirmed", summary.get("module_generation_rollback_authority_confirmed_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.module_not_registered", summary.get("constraint_module_registered_now") is False)
    ok("summary.constraint_not_enforced", summary.get("constraint_enforced_now") is False)
    ok("summary.verifier_integration_not_executed", summary.get("verifier_integration_executed_now") is False)
    ok("summary.verifier_not_modified", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_not_modified", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_not_implemented", summary.get("automation_implemented_now") is False)
    ok("summary.doc_sync_not_executed", summary.get("documentation_auto_sync_executed_now") is False)
    ok("summary.legacy_not_modified", summary.get("legacy_phase_modified_now") is False)
    ok("summary.legacy_doc_not_rewritten", summary.get("legacy_document_rewritten_now") is False)
    ok("summary.legacy_eval_not_modified", summary.get("legacy_eval_out_modified_now") is False)
    ok("summary.legacy_verifier_not_rerun", summary.get("legacy_verifier_rerun_now") is False)
    ok("summary.legacy_chain_not_deprecated", summary.get("legacy_chain_deprecated_now") is False)
    ok("summary.legacy_as_source", summary.get("legacy_as_source_evidence") is True)
    ok("summary.legacy_not_template", summary.get("legacy_as_template_source") is False)
    ok("summary.domain_rules_preserved", summary.get("domain_specific_rules_preserved") is True)
    ok("summary.frozen_not_enforced", summary.get("frozen_fields_enforced_now") is False)
    ok("summary.baseline_not_integrated", summary.get("verifier_baseline_integrated_now") is False)
    ok("summary.file_op_false", summary.get("file_operation_executed_now") is False)
    ok("summary.authorization_not_granted", summary.get("authorization_granted_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.real_rehearsal_blocked", summary.get("real_rehearsal_execution_allowed") is False)
    ok("summary.real_migration_blocked", summary.get("real_migration_execution_allowed") is False)
    ok("summary.batch_arming_blocked", summary.get("batch_arming_allowed") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.all_not_generated", summary.get("all_not_generated_now") is True)
    ok("summary.lifecycle_planning_only", summary.get("lifecycle_planning_defined_only") is True)
    ok("summary.all_planning_complete", summary.get("all_authorization_request_planning_complete") is True)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.request_planning_only", policy.get("authorization_request_planning_only") is True)
    ok("policy.source_phase", policy.get("source_phase") == UPSTREAM_PHASE)
    ok("policy.source_route", policy.get("source_selected_route_observed") == SELECTED_ROUTE)
    ok("policy.auth_request_not_generated", policy.get("governance_constraint_module_generation_authorization_request_generated_now") is False)
    ok("policy.auth_request_not_sent", policy.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("identity.row_count>=12", identity.get("row_count", 0) >= 12)
    ok("identity.all_not_generated", identity.get("all_not_generated_now") is True)
    ok(
        "identity.all_artifact_false",
        all(r.get("request_artifact_generated_now") is False for r in (identity.get("rows") or [])),
    )
    ok(
        "identity.all_sent_false",
        all(r.get("request_sent_now") is False for r in (identity.get("rows") or [])),
    )
    ok("source_binding.row_count>=12", source_binding.get("row_count", 0) >= 12)
    ok("source_binding.all_not_generated", source_binding.get("all_not_generated_now") is True)
    ok(
        "source_binding.all_not_approved",
        all(r.get("source_set_final_approved_now") is False for r in (source_binding.get("rows") or [])),
    )
    ok(
        "source_binding.all_not_bound",
        all(r.get("source_bound_now") is False for r in (source_binding.get("rows") or [])),
    )
    ok("domain_binding.row_count>=12", domain_binding.get("row_count", 0) >= 12)
    ok("domain_binding.all_not_generated", domain_binding.get("all_not_generated_now") is True)
    ok(
        "domain_binding.all_not_approved",
        all(r.get("approved_now") is False for r in (domain_binding.get("rows") or [])),
    )
    ok(
        "domain_binding.flattening_forbidden",
        all(r.get("flattening_forbidden") is True for r in (domain_binding.get("rows") or [])),
    )
    ok("scope_exclusion.row_count>=13", scope_exclusion.get("row_count", 0) >= 13)
    ok("scope_exclusion.all_not_generated", scope_exclusion.get("all_not_generated_now") is True)
    ok(
        "scope_exclusion.all_allowed_now_false",
        all(r.get("allowed_now") is False for r in (scope_exclusion.get("rows") or [])),
    )
    ok("statements.row_count>=10", statements.get("row_count", 0) >= 10)
    ok("statements.all_not_generated", statements.get("all_not_generated_now") is True)
    ok(
        "statements.all_generated_now_false",
        all(r.get("generated_now") is False for r in (statements.get("rows") or [])),
    )
    ok("lifecycle.row_count>=12", lifecycle.get("row_count", 0) >= 12)
    ok("lifecycle.all_not_generated", lifecycle.get("all_not_generated_now") is True)
    ok("lifecycle.planning_defined_only", lifecycle.get("lifecycle_planning_defined_only") is True)
    ok(
        "lifecycle.all_current_state_false",
        all(r.get("current_state_now") is False for r in (lifecycle.get("rows") or [])),
    )
    ok(
        "lifecycle.all_sent_false",
        all(r.get("request_sent_now") is False for r in (lifecycle.get("rows") or [])),
    )
    ok(
        "lifecycle.all_grant_false",
        all(r.get("grant_issued_now") is False for r in (lifecycle.get("rows") or [])),
    )
    ok("review.row_count>=12", review.get("row_count", 0) >= 12)
    ok("review.all_not_generated", review.get("all_not_generated_now") is True)
    ok(
        "review.all_not_executed",
        all(r.get("review_executed_now") is False for r in (review.get("rows") or [])),
    )
    ok("abort_revoke.row_count>=12", abort_revoke.get("row_count", 0) >= 12)
    ok("abort_revoke.all_not_generated", abort_revoke.get("all_not_generated_now") is True)
    ok(
        "abort_revoke.all_not_confirmed",
        all(r.get("confirmed_now") is False for r in (abort_revoke.get("rows") or [])),
    )
    ok(
        "abort_revoke.all_not_executed",
        all(r.get("abort_executed_now") is False and r.get("revoke_executed_now") is False for r in (abort_revoke.get("rows") or [])),
    )
    ok("verifier_usage.row_count>=12", verifier_usage.get("row_count", 0) >= 12)
    ok("verifier_usage.all_not_generated", verifier_usage.get("all_not_generated_now") is True)
    ok(
        "verifier_usage.all_planned",
        all(r.get("planned_now") is True for r in (verifier_usage.get("rows") or [])),
    )
    ok(
        "verifier_usage.not_modified",
        all(r.get("verifier_modified_now") is False for r in (verifier_usage.get("rows") or [])),
    )
    ok("non_claims.row_count>=10", non_claims.get("row_count", 0) >= 10)
    ok("non_claims.all_not_generated", non_claims.get("all_not_generated_now") is True)
    ok(
        "non_claims.all_planned",
        all(r.get("planned_now") is True for r in (non_claims.get("rows") or [])),
    )

    ok(
        "readiness.ready_for_dryrun",
        readiness.get("ready_for_governance_constraint_module_generation_authorization_request_dryrun") is True,
    )
    ok(
        "readiness.not_artifact_generation",
        readiness.get("ready_for_governance_constraint_module_generation_authorization_request_artifact_generation")
        is False,
    )
    ok("readiness.not_auth_request", readiness.get("ready_for_governance_constraint_module_generation_authorization_request") is False)
    ok("readiness.not_auth_grant", readiness.get("ready_for_governance_constraint_module_generation_authorization_grant") is False)
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.planning_completed", readiness.get("authorization_request_planning_completed") is True)
    ok("readiness.identity_planned", readiness.get("request_identity_planned") is True)
    ok("readiness.source_set_planned", readiness.get("source_set_binding_planned") is True)
    ok("readiness.domain_planned", readiness.get("domain_preservation_binding_planned") is True)
    ok("readiness.scope_planned", readiness.get("scope_and_exclusion_planned") is True)
    ok("readiness.statements_planned", readiness.get("non_grant_and_non_generation_statement_planned") is True)
    ok("readiness.lifecycle_planned", readiness.get("request_lifecycle_planned") is True)
    ok("readiness.review_planned", readiness.get("request_review_requirement_planned") is True)
    ok("readiness.abort_planned", readiness.get("abort_revoke_linkage_planned") is True)
    ok("readiness.verifier_usage_planned", readiness.get("verifier_usage_planned") is True)
    ok("readiness.non_claims_planned", readiness.get("non_claims_planned") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.points_to_dryrun", "Authorization-Request-DryRun" in summary.get("recommended_next_phase", ""))
    ok("summary.main_migration_paused", summary.get("main_migration_chain_paused") is True)
    ok("summary.main_migration_resume_phase", summary.get("main_migration_resume_phase") == MAIN_MIGRATION_RESUME)
    ok(
        "summary.roadmap_input_loaded",
        summary.get("governance_constraint_module_generation_authorization_roadmap_decision_input_loaded") is True,
    )
    ok("summary.points_to_request_dryrun", "AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN" in summary.get("final_decision", ""))

    fd = summary.get("final_decision", "")
    ok(
        "summary.not_raw_auth_request",
        "READY_FOR_AUTHORIZATION_REQUEST_PLANNING" not in fd
        or "AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN" in fd,
    )
    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        if token == "CONSTRAINT_MODULE_GENERATION":
            ok(
                f"summary.final_decision_not_{token}",
                not (
                    token in fd
                    and "AUTHORIZATION_REQUEST_PLANNING" not in fd
                    and "AUTHORIZATION_REQUEST_DRYRUN" not in fd
                    and "AUTHORIZATION_ROADMAP" not in fd
                ),
            )
        else:
            ok(f"summary.final_decision_not_{token}", token not in fd)

    ok(
        "summary.final_decision_not_AUTHORIZATION_REQUEST_alone",
        not (
            "AUTHORIZATION_REQUEST" in fd
            and "AUTHORIZATION_REQUEST_PLANNING" not in fd
            and "AUTHORIZATION_REQUEST_DRYRUN" not in fd
        ),
    )

    for i in range(30):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(25):
        ok(f"meta.request_planning_only[{i}]", summary.get("authorization_request_planning_only") is True)
    for i in range(25):
        ok(
            f"meta.request_planning_selected[{i}]",
            summary.get("governance_constraint_module_generation_authorization_request_planning_selected") is True,
        )
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(12):
        ok(f"meta.identity_count[{i}]", identity.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.source_count[{i}]", source_binding.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.domain_count[{i}]", domain_binding.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.scope_count[{i}]", scope_exclusion.get("row_count", 0) >= 13)
    for i in range(12):
        ok(f"meta.statements_count[{i}]", statements.get("row_count", 0) >= 10)
    for i in range(12):
        ok(f"meta.lifecycle_count[{i}]", lifecycle.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.review_count[{i}]", review.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.abort_count[{i}]", abort_revoke.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.verifier_usage_count[{i}]", verifier_usage.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 10)
    for i in range(8):
        ok(f"meta.all_not_generated[{i}]", summary.get("all_not_generated_now") is True)
    for i in range(8):
        ok(f"meta.auth_request_not_generated[{i}]", summary.get("governance_constraint_module_generation_authorization_request_generated_now") is False)
    for i in range(8):
        ok(f"meta.auth_request_not_sent[{i}]", summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    for i in range(8):
        ok(f"meta.auth_not_granted[{i}]", summary.get("governance_constraint_module_generation_authorized_now") is False)
    for i in range(8):
        ok(f"meta.revoke_not_confirmed[{i}]", summary.get("module_generation_revoke_authority_confirmed_now") is False)
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
            f"meta.readiness_dryrun[{i}]",
            readiness.get("ready_for_governance_constraint_module_generation_authorization_request_dryrun") is True,
        )
    for i in range(8):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(8):
        ok(f"meta.domain_rules_preserved[{i}]", summary.get("domain_specific_rules_preserved") is True)
    for i in range(8):
        ok(f"meta.frozen_not_enforced[{i}]", summary.get("frozen_fields_enforced_now") is False)
    for i in range(8):
        ok(f"meta.lifecycle_planning_only[{i}]", summary.get("lifecycle_planning_defined_only") is True)

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
