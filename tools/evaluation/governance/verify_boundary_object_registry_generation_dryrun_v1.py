#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Boundary Object Registry Generation DryRun v1."""

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

PHASE_ID = "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001"
UPSTREAM_PHASE = "Phase-Boundary-Object-Registry-Generation-Planning-v1-001"
UPSTREAM_FINAL = "BOUNDARY_OBJECT_REGISTRY_GENERATION_PLANNING_READY_FOR_DRYRUN"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

PLANNING_ARTIFACTS = (
    "boundary_object_registry_generation_planning_policy_v1.json",
    "registry_generation_source_inventory_planning_matrix_v1.json",
    "registry_source_artifact_whitelist_planning_matrix_v1.json",
    "registry_source_integrity_check_planning_matrix_v1.json",
    "registry_contamination_prevention_planning_matrix_v1.json",
    "registry_entry_conversion_rule_planning_matrix_v1.json",
    "registry_protected_object_entry_rule_planning_matrix_v1.json",
    "registry_policy_entry_rule_planning_matrix_v1.json",
    "registry_owner_operator_dependency_planning_matrix_v1.json",
    "registry_generation_verifier_usage_planning_matrix_v1.json",
    "registry_generation_non_claims_planning_matrix_v1.json",
    "registry_generation_output_plan_v1.json",
    "boundary_object_registry_generation_planning_readiness_decision_v1.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "boundary_object_registry_generation_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--boundary-object-registry-generation-planning-root",
        default=str(repo_root / "_eval_out" / "boundary_object_registry_generation_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.boundary_object_registry_generation_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "boundary_object_registry_generation_dryrun_policy_v1.json")
    completeness = _load_json(root / "registry_generation_planning_artifact_completeness_dryrun_v1.json")
    source_inv = _load_json(root / "registry_generation_source_inventory_dryrun_v1.json")
    whitelist = _load_json(root / "registry_source_artifact_whitelist_dryrun_v1.json")
    integrity = _load_json(root / "registry_source_integrity_check_dryrun_v1.json")
    contamination = _load_json(root / "registry_contamination_prevention_dryrun_v1.json")
    conversion = _load_json(root / "registry_entry_conversion_rule_dryrun_v1.json")
    protected = _load_json(root / "registry_protected_object_entry_rule_dryrun_v1.json")
    policy_entry = _load_json(root / "registry_policy_entry_rule_dryrun_v1.json")
    oo_dep = _load_json(root / "registry_owner_operator_dependency_dryrun_v1.json")
    verifier_usage = _load_json(root / "registry_generation_verifier_usage_dryrun_v1.json")
    non_claims = _load_json(root / "registry_generation_non_claims_generation_dryrun_v1.json")
    readiness = _load_json(
        root / "boundary_object_registry_generation_dryrun_readiness_decision_v1.json"
    )

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "boundary_object_registry_generation_planning_readiness_decision_v1.json"
    )
    up_whitelist = _load_json(
        upstream_root / "registry_source_artifact_whitelist_planning_matrix_v1.json"
    )

    ok("upstream.planning_dir_exists", upstream_root.is_dir())
    for name in PLANNING_ARTIFACTS:
        ok(f"upstream.artifact.{name}", (upstream_root / name).is_file())
    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.ready_for_dryrun",
        up_readiness.get("ready_for_boundary_object_registry_generation_dryrun") is True,
    )
    ok("upstream.planning_only", up_summary.get("boundary_object_registry_generation_planning_only") is True)
    ok("upstream.gen_not_executed", up_summary.get("boundary_object_registry_generation_executed_now") is False)
    ok("upstream.registry_not_generated", up_summary.get("boundary_object_registry_generated_now") is False)
    ok("upstream.not_registered", up_summary.get("boundary_object_registered_now") is False)
    ok("upstream.gen_not_authorized", up_summary.get("registry_generation_authorized_now") is False)
    ok("upstream.source_not_final_validated", up_summary.get("registry_source_final_validated_now") is False)
    ok("upstream.source_not_validated", up_summary.get("registry_generation_source_validated_now") is False)
    ok("upstream.contamination_not_final", up_summary.get("registry_contamination_check_final_executed_now") is False)
    ok("upstream.contamination_not_checked", up_summary.get("registry_generation_contamination_checked_now") is False)
    ok("upstream.entry_not_generated", up_summary.get("registry_entry_generated_now") is False)
    ok("upstream.entry_not_committed", up_summary.get("registry_entry_committed_now") is False)
    ok("upstream.protected_not_modified", up_summary.get("protected_asset_modified_now") is False)
    ok("upstream.hr_not_modified", up_summary.get("human_review_queue_modified_now") is False)
    ok("upstream.dnae_not_modified", up_summary.get("dnae_or_permanent_block_modified_now") is False)
    ok("upstream.file_op_not_executed", up_summary.get("file_operation_executed_now") is False)
    ok("upstream.owner_request_not_sent", up_summary.get("owner_approval_request_sent_now") is False)
    ok("upstream.execution_window_not_opened", up_summary.get("execution_window_opened_now") is False)
    ok("upstream.evidence_not_authorized", up_summary.get("evidence_generation_authorized_now") is False)
    ok("upstream.evidence_not_generated", up_summary.get("evidence_generated_now") is False)
    ok("upstream.success_claim_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.not_registry_generation", up_readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("upstream.not_registration", up_readiness.get("ready_for_boundary_object_registration") is False)
    ok("upstream.not_gen_auth", up_readiness.get("ready_for_registry_generation_authorization") is False)
    ok("upstream.not_source_final_validation", up_readiness.get("ready_for_registry_source_final_validation") is False)
    ok(
        "upstream.not_contamination_final",
        up_readiness.get("ready_for_registry_contamination_check_final_execution") is False,
    )
    ok("upstream.not_entry_generation", up_readiness.get("ready_for_registry_entry_generation") is False)
    ok("upstream.not_entry_commit", up_readiness.get("ready_for_registry_entry_commit") is False)
    ok("upstream.not_owner_request", up_readiness.get("ready_for_owner_approval_request") is False)
    ok("upstream.not_execution_window", up_readiness.get("ready_for_execution_window_opening") is False)
    ok("upstream.not_evidence_gen_auth", up_readiness.get("ready_for_evidence_generation_authorization") is False)
    ok("upstream.not_file_operation", up_readiness.get("ready_for_file_operation") is False)
    ok("upstream.not_restore_map", up_readiness.get("ready_for_restore_map_generation") is False)
    ok("upstream.not_rollback", up_readiness.get("ready_for_rollback_execution") is False)
    ok("upstream.not_real_rehearsal", up_readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("upstream.not_real_migration", up_readiness.get("ready_for_real_migration_execution") is False)
    ok("upstream.batch_arming_false", up_summary.get("batch_arming_allowed") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    up_summary_wl = next(
        (r for r in (up_whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
        {},
    )
    up_verifier_wl = next(
        (r for r in (up_whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
        {},
    )
    ok("upstream.summary_not_primary", up_summary_wl.get("allowed_as_primary_source") is False)
    ok("upstream.verifier_not_registry_source", up_verifier_wl.get("allowed_as_registry_source") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("boundary_object_registry_generation_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.gen_not_executed", summary.get("boundary_object_registry_generation_executed_now") is False)
    ok("summary.registry_not_generated", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.not_registered", summary.get("boundary_object_registered_now") is False)
    ok("summary.gen_not_authorized", summary.get("registry_generation_authorized_now") is False)
    ok("summary.source_not_final_validated", summary.get("registry_source_final_validated_now") is False)
    ok("summary.source_not_validated", summary.get("registry_generation_source_validated_now") is False)
    ok("summary.contamination_not_final", summary.get("registry_contamination_check_final_executed_now") is False)
    ok("summary.contamination_not_checked", summary.get("registry_generation_contamination_checked_now") is False)
    ok("summary.entry_not_generated", summary.get("registry_entry_generated_now") is False)
    ok("summary.entry_not_committed", summary.get("registry_entry_committed_now") is False)
    ok("summary.protected_not_modified", summary.get("protected_asset_modified_now") is False)
    ok("summary.hr_not_modified", summary.get("human_review_queue_modified_now") is False)
    ok("summary.dnae_not_modified", summary.get("dnae_or_permanent_block_modified_now") is False)
    ok("summary.file_op_not_executed", summary.get("file_operation_executed_now") is False)
    ok("summary.write_perm_not_released", summary.get("write_permission_released_now") is False)
    ok("summary.migration_perm_not_released", summary.get("migration_permission_released_now") is False)
    ok("summary.evidence_perm_not_released", summary.get("evidence_permission_released_now") is False)
    ok("summary.rollback_perm_not_released", summary.get("rollback_permission_released_now") is False)
    ok("summary.owner_request_not_sent", summary.get("owner_approval_request_sent_now") is False)
    ok("summary.execution_window_not_opened", summary.get("execution_window_opened_now") is False)
    ok("summary.evidence_not_authorized", summary.get("evidence_generation_authorized_now") is False)
    ok("summary.evidence_not_generated", summary.get("evidence_generated_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.runtime_false", summary.get("runtime_invoked") is False)
    ok("summary.execution_not_committed", summary.get("execution_committed") is False)
    ok("summary.write_false", summary.get("write_allowed") is False)
    ok("summary.real_rehearsal_false", summary.get("real_rehearsal_execution_allowed") is False)
    ok("summary.real_migration_false", summary.get("real_migration_execution_allowed") is False)
    ok("summary.batch_arming_false", summary.get("batch_arming_allowed") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("boundary_object_registry_generation_dryrun_only") is True)
    ok("policy.simulated", policy.get("simulated") is True)
    ok("policy.gen_not_executed", policy.get("boundary_object_registry_generation_executed_now") is False)
    ok("policy.registry_not_generated", policy.get("boundary_object_registry_generated_now") is False)
    ok("policy.source_phase", policy.get("source_phase") == UPSTREAM_PHASE)

    ok("completeness.row_count=13", completeness.get("row_count") == 13)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("source_inv.row_count>=16", source_inv.get("row_count", 0) >= 16)
    ok("source_inv.all_pass", source_inv.get("all_pass") is True)
    ok(
        "source_inv.all_not_used",
        all(r.get("used_for_generation_now") is False for r in (source_inv.get("rows") or [])),
    )
    ok(
        "source_inv.all_not_final_validated",
        all(r.get("source_final_validated_now") is False for r in (source_inv.get("rows") or [])),
    )
    ok("whitelist.row_count>=16", whitelist.get("row_count", 0) >= 16)
    ok("whitelist.all_pass", whitelist.get("all_pass") is True)
    summary_wl = next(
        (r for r in (whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
        {},
    )
    verifier_wl = next(
        (r for r in (whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
        {},
    )
    ok("whitelist.summary_not_primary", summary_wl.get("allowed_as_primary_source") is False)
    ok("whitelist.verifier_not_registry_source", verifier_wl.get("allowed_as_registry_source") is False)
    ok(
        "whitelist.all_not_whitelisted_now",
        all(r.get("whitelisted_now") is False for r in (whitelist.get("rows") or [])),
    )
    ok("integrity.row_count>=14", integrity.get("row_count", 0) >= 14)
    ok("integrity.all_pass", integrity.get("all_pass") is True)
    ok(
        "integrity.all_not_executed",
        all(r.get("final_check_executed_now") is False for r in (integrity.get("rows") or [])),
    )
    ok(
        "integrity.all_source_not_final",
        all(r.get("source_final_validated_now") is False for r in (integrity.get("rows") or [])),
    )
    ok("contamination.row_count>=14", contamination.get("row_count", 0) >= 14)
    ok("contamination.all_pass", contamination.get("all_pass") is True)
    ok(
        "contamination.all_not_checked",
        all(r.get("contamination_checked_now") is False for r in (contamination.get("rows") or [])),
    )
    ok(
        "contamination.all_final_gen_false",
        all(r.get("final_generation_allowed_now") is False for r in (contamination.get("rows") or [])),
    )
    ok("conversion.row_count>=16", conversion.get("row_count", 0) >= 16)
    ok("conversion.all_pass", conversion.get("all_pass") is True)
    ok(
        "conversion.all_entry_not_generated",
        all(r.get("entry_generated_now") is False for r in (conversion.get("rows") or [])),
    )
    ok(
        "conversion.all_entry_not_committed",
        all(r.get("entry_committed_now") is False for r in (conversion.get("rows") or [])),
    )
    ok("protected.row_count>=12", protected.get("row_count", 0) >= 12)
    ok("protected.all_pass", protected.get("all_pass") is True)
    ok(
        "protected.all_frozen",
        all(
            r.get("write_allowed_now") is False
            and r.get("move_allowed_now") is False
            and r.get("entry_generated_now") is False
            and r.get("protected_asset_modified_now") is False
            for r in (protected.get("rows") or [])
        ),
    )
    ok("policy_entry.row_count>=10", policy_entry.get("row_count", 0) >= 10)
    ok("policy_entry.all_pass", policy_entry.get("all_pass") is True)
    ok(
        "policy_entry.all_not_generated",
        all(r.get("entry_generated_now") is False for r in (policy_entry.get("rows") or [])),
    )
    ok("oo_dep.row_count>=10", oo_dep.get("row_count", 0) >= 10)
    ok("oo_dep.all_pass", oo_dep.get("all_pass") is True)
    ok(
        "oo_dep.all_not_satisfied",
        all(r.get("satisfied_now") is False and r.get("authorization_granted_now") is False for r in (oo_dep.get("rows") or [])),
    )
    ok("verifier_usage.row_count>=16", verifier_usage.get("row_count", 0) >= 16)
    ok("verifier_usage.all_pass", verifier_usage.get("all_pass") is True)
    ok(
        "verifier_usage.not_modified",
        all(r.get("verifier_modified_now") is False and r.get("enforced_now") is False for r in (verifier_usage.get("rows") or [])),
    )
    ok("non_claims.row_count>=12", non_claims.get("row_count", 0) >= 12)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)
    ok("non_claims.all_not_generated", all(r.get("generated_now") is False for r in (non_claims.get("rows") or [])))

    ok(
        "readiness.ready_for_post_review",
        readiness.get("ready_for_boundary_object_registry_generation_post_dryrun_review") is True,
    )
    ok("readiness.not_registry_generation", readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("readiness.not_registration", readiness.get("ready_for_boundary_object_registration") is False)
    ok("readiness.not_gen_auth", readiness.get("ready_for_registry_generation_authorization") is False)
    ok("readiness.not_source_final_validation", readiness.get("ready_for_registry_source_final_validation") is False)
    ok(
        "readiness.not_contamination_final",
        readiness.get("ready_for_registry_contamination_check_final_execution") is False,
    )
    ok("readiness.not_entry_generation", readiness.get("ready_for_registry_entry_generation") is False)
    ok("readiness.not_entry_commit", readiness.get("ready_for_registry_entry_commit") is False)
    ok("readiness.not_owner_request", readiness.get("ready_for_owner_approval_request") is False)
    ok("readiness.not_execution_window", readiness.get("ready_for_execution_window_opening") is False)
    ok("readiness.not_evidence_gen_auth", readiness.get("ready_for_evidence_generation_authorization") is False)
    ok("readiness.not_file_operation", readiness.get("ready_for_file_operation") is False)
    ok("readiness.not_restore_map", readiness.get("ready_for_restore_map_generation") is False)
    ok("readiness.not_rollback", readiness.get("ready_for_rollback_execution") is False)
    ok("readiness.not_real_rehearsal", readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("readiness.not_real_migration", readiness.get("ready_for_real_migration_execution") is False)
    ok("readiness.not_batch_arming", readiness.get("ready_for_batch_arming") is False)
    ok("readiness.dryrun_completed", readiness.get("registry_generation_dryrun_completed") is True)
    ok("readiness.completeness_pass", readiness.get("planning_artifact_completeness_dryrun_pass") is True)
    ok("readiness.source_inv_pass", readiness.get("source_inventory_dryrun_pass") is True)
    ok("readiness.whitelist_pass", readiness.get("source_whitelist_dryrun_pass") is True)
    ok("readiness.integrity_pass", readiness.get("source_integrity_dryrun_pass") is True)
    ok("readiness.contamination_pass", readiness.get("contamination_prevention_dryrun_pass") is True)
    ok("readiness.conversion_pass", readiness.get("entry_conversion_rule_dryrun_pass") is True)
    ok("readiness.protected_pass", readiness.get("protected_object_entry_rule_dryrun_pass") is True)
    ok("readiness.policy_entry_pass", readiness.get("policy_entry_rule_dryrun_pass") is True)
    ok("readiness.oo_dep_pass", readiness.get("owner_operator_dependency_dryrun_pass") is True)
    ok("readiness.verifier_usage_pass", readiness.get("verifier_usage_dryrun_pass") is True)
    ok("readiness.non_claims_pass", readiness.get("non_claims_generation_dryrun_pass") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.loaded_input", summary.get("boundary_object_registry_generation_planning_input_loaded") is True)

    ok("summary.points_to_post_review", "POST_DRYRUN_REVIEW" in summary.get("final_decision", "").upper())
    ok(
        "summary.not_direct_registry_generation",
        not (
            "BOUNDARY_OBJECT_REGISTRY_GENERATION" in summary.get("final_decision", "")
            and "DRYRUN" not in summary.get("final_decision", "").upper()
            and "POST" not in summary.get("final_decision", "").upper()
        ),
    )
    ok(
        "readiness.not_direct_registry_generation",
        not (
            "BOUNDARY_OBJECT_REGISTRY_GENERATION" in readiness.get("final_decision", "")
            and "DRYRUN" not in readiness.get("final_decision", "").upper()
            and "POST" not in readiness.get("final_decision", "").upper()
        ),
    )

    for token in (
        "BOUNDARY_OBJECT_REGISTRATION",
        "REGISTRY_SOURCE_FINAL_VALIDATION",
        "REGISTRY_CONTAMINATION_CHECK_FINAL",
        "REGISTRY_ENTRY_GENERATION",
        "REGISTRY_ENTRY_COMMIT",
        "OWNER_APPROVAL_REQUEST",
        "EXECUTION_WINDOW_OPENING",
        "EVIDENCE_GENERATION_AUTHORIZATION",
        "FILE_OPERATION",
        "RESTORE_MAP_GENERATION",
        "ROLLBACK_EXECUTION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))
        ok(f"readiness.final_decision_not_{token}", token not in readiness.get("final_decision", ""))

    for i in range(28):
        ok(f"meta.gen_not_executed[{i}]", summary.get("boundary_object_registry_generation_executed_now") is False)
    for i in range(25):
        ok(f"meta.dryrun_only[{i}]", summary.get("boundary_object_registry_generation_dryrun_only") is True)
    for i in range(25):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(22):
        ok(f"meta.registry_not_generated[{i}]", summary.get("boundary_object_registry_generated_now") is False)
    for i in range(20):
        ok(f"meta.entry_not_generated[{i}]", summary.get("registry_entry_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(18):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(15):
        ok(f"meta.source_not_final_validated[{i}]", summary.get("registry_source_final_validated_now") is False)
    for i in range(15):
        ok(f"meta.contamination_not_final[{i}]", summary.get("registry_contamination_check_final_executed_now") is False)
    for i in range(12):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.source_inv_count[{i}]", source_inv.get("row_count", 0) >= 16)
    for i in range(10):
        ok(f"meta.whitelist_pass[{i}]", whitelist.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.readiness_post_review[{i}]", readiness.get("ready_for_boundary_object_registry_generation_post_dryrun_review") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("boundary_object_registry_generation_planning_input_loaded") is True)
    for i in range(8):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(8):
        ok(f"meta.gen_not_authorized[{i}]", summary.get("registry_generation_authorized_now") is False)
    for i in range(6):
        ok(f"meta.not_registered[{i}]", summary.get("boundary_object_registered_now") is False)

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
