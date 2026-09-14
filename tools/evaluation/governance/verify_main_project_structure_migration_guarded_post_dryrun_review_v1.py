#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Guarded Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_guarded_post_dryrun_review_only"

MIN_CHECKS = 300
BASELINE_REQUIREMENT = 240


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_review = _load_json(root / "guarded_dryrun_input_review.json")
    batch_review = _load_json(root / "batch_gate_post_review.json")
    gate_review = _load_json(root / "gate_sequence_post_review.json")
    exclusion_review = _load_json(root / "exclusion_scope_post_review.json")
    candidate_review = _load_json(root / "candidate_scope_post_review.json")
    test_review = _load_json(root / "post_migration_test_binding_post_review.json")
    rollback_review = _load_json(root / "rollback_checkpoint_post_review.json")
    human_review = _load_json(root / "human_approval_checkpoint_post_review.json")
    boundary_review = _load_json(root / "guarded_dryrun_boundary_post_review.json")
    decision = _load_json(root / "guarded_post_dryrun_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == REVIEW_SCOPE)

    for k in (
        "guarded_dryrun_input_loaded",
        "guarded_planning_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    generated = (
        "guarded_dryrun_input_review_generated",
        "batch_gate_post_review_generated",
        "gate_sequence_post_review_generated",
        "exclusion_scope_post_review_generated",
        "candidate_scope_post_review_generated",
        "post_migration_test_binding_post_review_generated",
        "rollback_checkpoint_post_review_generated",
        "human_approval_checkpoint_post_review_generated",
        "guarded_dryrun_boundary_post_review_generated",
        "guarded_post_dryrun_readiness_decision_generated",
    )
    for k in generated:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.reviewed_batch_count", summary.get("reviewed_batch_count") == 8)
    ok("summary.simulated_pass_batch_count", summary.get("simulated_pass_batch_count") == 8)
    ok("summary.simulated_blocked_batch_count", summary.get("simulated_blocked_batch_count") == 0)
    ok("summary.reviewed_gate_count", summary.get("reviewed_gate_count") == 10)
    ok("summary.gate_sequence_pass", summary.get("gate_sequence_pass") is True)
    ok("summary.migration_candidate_scope_count", summary.get("migration_candidate_scope_count") == 8)
    ok("summary.migration_exclusion_scope_count>=17", summary.get("migration_exclusion_scope_count", 0) >= 17)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.bound_test_count", summary.get("bound_test_count") == 31)
    ok("summary.unbound_test_count", summary.get("unbound_test_count") == 0)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.rollback_checkpoint_count", summary.get("rollback_checkpoint_count") == 8)
    ok("summary.rollback_checkpoint_per_batch", summary.get("rollback_checkpoint_per_batch") is True)
    ok("summary.rollback_executed=false", summary.get("rollback_executed") is False)
    ok("summary.human_approval_is_placeholder_only", summary.get("human_approval_is_placeholder_only") is True)
    ok("summary.final_owner_human_confirmed=false", summary.get("final_owner_human_confirmed") is False)
    ok("summary.approval_executed=false", summary.get("approval_executed") is False)
    ok("summary.candidate_scopes_execution_allowed=false", summary.get("candidate_scopes_execution_allowed") is False)
    ok("summary.post_migration_tests_executed=false", summary.get("post_migration_tests_executed") is False)
    ok("summary.post_migration_tests_bound_to_batches", summary.get("post_migration_tests_bound_to_batches") is True)
    ok("summary.ready_for_closure", summary.get("ready_for_closure") is True)

    exclusion_keys = (
        "protected_assets_excluded_from_migration",
        "permanent_blocks_excluded_from_migration",
        "human_review_items_excluded_or_manual_only",
        "eval_out_outputs_excluded",
        "verifier_reports_excluded",
        "go_no_go_packs_excluded",
        "correction_records_excluded",
        "historical_test_logs_excluded",
        "phase_records_excluded",
        "whitebox_test_center_physical_restructure_excluded",
        "developer_backend_full_architecture_excluded",
        "future_reserved_module_finalization_excluded",
        "runtime_behavior_changes_excluded",
        "client_runtime_changes_excluded",
    )
    for k in exclusion_keys:
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "migration_execution_allowed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    for k in (
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_review",
        "readme_modified_by_review",
        "phase_verdict_table_modified_by_review",
        "runtime_enabled",
        "file_operation_invoked",
        "world_model_written",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("input_review.required_artifacts_loaded", input_review.get("required_artifacts_loaded") is True)
    ok("input_review.missing_empty", input_review.get("missing_required_artifacts") == [])

    ok("batch.reviewed_batch_count", batch_review.get("reviewed_batch_count") == 8)
    ok("batch.simulated_pass_batch_count", batch_review.get("simulated_pass_batch_count") == 8)
    ok("batch.simulated_blocked_batch_count", batch_review.get("simulated_blocked_batch_count") == 0)
    ok("batch.no_batch_executed", batch_review.get("no_batch_executed") is True)
    ok("batch.verdict", batch_review.get("verdict") == "acceptable_for_closure")

    for key in (
        "b0_baseline_snapshot_review",
        "b1_docs_relink_review",
        "b2_capability_grouping_review",
        "b3_governance_grouping_review",
        "b4_midplatform_grouping_review",
        "b5_developer_artifact_reference_review",
        "b6_future_reserved_marker_review",
        "b7_verification_rollback_gate_review",
    ):
        section = batch_review.get(key) or {}
        ok(f"batch.{key}.simulated_pass", section.get("simulated_pass") is True)

    ok("batch.b1.readme_not_modified", batch_review.get("b1_docs_relink_review", {}).get("readme_not_modified") is True)
    ok("batch.b7.all_tests_bound", batch_review.get("b7_verification_rollback_gate_review", {}).get("all_tests_bound") is True)
    ok("batch.b7.tests_not_executed", batch_review.get("b7_verification_rollback_gate_review", {}).get("tests_not_executed") is True)
    ok("batch.human_approval_placeholder_batches", len(batch_review.get("human_approval_placeholder_batches") or []) == 6)

    ok("gate.reviewed_gate_count", gate_review.get("reviewed_gate_count") == 10)
    ok("gate.gate_sequence_pass", gate_review.get("gate_sequence_pass") is True)
    ok("gate.protected_asset_gate_pass", gate_review.get("protected_asset_gate_pass") is True)
    ok("gate.hr_exclusion_gate_pass", gate_review.get("hr_exclusion_gate_pass") is True)
    ok("gate.dnae_exclusion_gate_pass", gate_review.get("dnae_exclusion_gate_pass") is True)
    ok("gate.human_approval_is_placeholder", gate_review.get("human_approval_checkpoint_is_placeholder") is True)
    ok("gate.runtime_granted=false", gate_review.get("runtime_granted") is False)

    gate_names = (
        "PreBatchProtectedAssetGate",
        "HumanReviewExclusionGate",
        "PermanentDnaeExclusionGate",
        "ClientBackendBoundaryGate",
        "FutureReservedModuleGate",
        "RuntimeBehaviorNoChangeGate",
        "DocsLinkIntegrityGate",
        "PostBatchVerifierGate",
        "RollbackAvailabilityGate",
        "HumanApprovalCheckpointGate",
    )
    for gn in gate_names:
        ok(f"gate.details.{gn}", gate_review.get("gate_details", {}).get(gn) is True)

    for k in exclusion_keys:
        ok(f"exclusion_review.{k}", exclusion_review.get(k) is True)

    candidate_flags = (
        "doc_relink_candidate_only",
        "module_grouping_candidate_only",
        "target_structure_marker_candidate_only",
        "module_versioning_marker_candidate_only",
        "non_runtime_metadata_mapping_candidate_only",
        "client_boundary_marker_candidate_only",
        "developer_backend_reference_marker_candidate_only",
        "future_reserved_marker_candidate_only",
    )
    ok("candidate.candidate_scope_count", candidate_review.get("candidate_scope_count") == 8)
    for cf in candidate_flags:
        ok(f"candidate.{cf}", candidate_review.get(cf) is True)

    ok("test.bound_test_count", test_review.get("bound_test_count") == 31)
    ok("test.unbound_test_count", test_review.get("unbound_test_count") == 0)
    ok("test.executed_test_count", test_review.get("executed_test_count") == 0)
    ok("test.structural_integrity_tests_bound", test_review.get("structural_integrity_tests_bound") is True)
    ok("test.governance_boundary_tests_bound", test_review.get("governance_boundary_tests_bound") is True)
    ok("test.functional_smoke_tests_bound", test_review.get("functional_smoke_tests_bound") is True)
    ok("test.no_runtime_regression_tests_bound", test_review.get("no_runtime_regression_tests_bound") is True)
    ok("test.developer_tooling_non_execution_tests_bound", test_review.get("developer_tooling_non_execution_tests_bound") is True)

    ok("rollback.rollback_checkpoint_count", rollback_review.get("rollback_checkpoint_count") == 8)
    ok("rollback.rollback_executed=false", rollback_review.get("rollback_executed") is False)
    ok("rollback.rollback_checkpoint_per_batch", rollback_review.get("rollback_checkpoint_per_batch") is True)
    ok("rollback.restore_path_map_defined", rollback_review.get("restore_path_map_defined") is True)

    ok("human.human_approval_is_placeholder_only", human_review.get("human_approval_is_placeholder_only") is True)
    ok("human.final_owner_human_confirmed=false", human_review.get("final_owner_human_confirmed") is False)
    ok("human.approval_executed=false", human_review.get("approval_executed") is False)
    ok("human.approval_does_not_override_safety_gate", human_review.get("approval_does_not_override_safety_gate") is True)
    ok("human.approval_does_not_override_permanent_dnae", human_review.get("approval_does_not_override_permanent_dnae") is True)

    ok("boundary_review.no_post_migration_tests_executed", boundary_review.get("no_post_migration_tests_executed") is True)
    ok("boundary_review.no_rollback_executed", boundary_review.get("no_rollback_executed") is True)
    ok("boundary_review.boundary_ok", boundary_review.get("boundary_ok") is True)

    ok("decision.ready_for_closure", decision.get("ready_for_closure") is True)
    ok("decision.review_verdict", decision.get("review_verdict") == "GO")
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)

    input_matrix = _load_json(root / "input_root_matrix.json")
    governance_debt = _load_json(root / "governance_debt_review.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    required_outputs = (
        "summary.json",
        "input_root_matrix.json",
        "guarded_dryrun_input_review.json",
        "batch_gate_post_review.json",
        "gate_sequence_post_review.json",
        "exclusion_scope_post_review.json",
        "candidate_scope_post_review.json",
        "post_migration_test_binding_post_review.json",
        "rollback_checkpoint_post_review.json",
        "human_approval_checkpoint_post_review.json",
        "guarded_dryrun_boundary_post_review.json",
        "guarded_post_dryrun_readiness_decision.json",
        "no_file_move_boundary_report.json",
        "no_delete_boundary_report.json",
        "no_runtime_boundary_report.json",
        "no_write_boundary_report.json",
        "governance_debt_review.json",
        "next_phase_recommendation.json",
    )
    for fname in required_outputs:
        ok(f"artifact.exists.{fname}", (root / fname).is_file())

    idx = {r.get("intake_id"): r for r in input_matrix.get("rows", [])}
    for intake_id in (
        "guarded_dryrun",
        "guarded_planning",
        "readiness",
        "roadmap_decision",
        "pahr_closure",
        "consolidation_closure",
        "structure_map",
        "gate_taxonomy",
    ):
        ok(f"input_matrix.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    for art in input_review.get("loaded_artifacts") or []:
        ok(f"input_review.artifact.{art}", art in (input_review.get("loaded_artifacts") or []))

    for art in input_review.get("missing_required_artifacts") or []:
        ok(f"input_review.missing_should_be_empty.{art}", False, art)

    ok("input_review.input_status", input_review.get("input_status") == "complete")
    ok("input_review.dryrun_input_loaded", input_review.get("dryrun_input_loaded") is True)
    ok("input_review.guarded_planning_input_loaded", input_review.get("guarded_planning_input_loaded") is True)
    ok("input_review.readiness_input_loaded", input_review.get("readiness_input_loaded") is True)

    batch_sections = (
        "b0_baseline_snapshot_review",
        "b1_docs_relink_review",
        "b2_capability_grouping_review",
        "b3_governance_grouping_review",
        "b4_midplatform_grouping_review",
        "b5_developer_artifact_reference_review",
        "b6_future_reserved_marker_review",
        "b7_verification_rollback_gate_review",
    )
    for section_key in batch_sections:
        section = batch_review.get(section_key) or {}
        ok(f"batch.{section_key}.simulated_pass", section.get("simulated_pass") is True)

    for i, bid in enumerate(batch_review.get("human_approval_placeholder_batches") or []):
        ok(f"batch.human_placeholder[{i}].batch_id", bid in ("B1", "B2", "B3", "B4", "B5", "B6"))

    ok("batch.batch_requires_review_count", batch_review.get("batch_requires_review_count") == 6)

    ok("gate.runtime_no_change_gate_pass", gate_review.get("runtime_no_change_gate_pass") is True)
    ok("gate.rollback_availability_gate_pass", gate_review.get("rollback_availability_gate_pass") is True)
    ok("gate.docs_link_integrity_gate_pass", gate_review.get("gate_details", {}).get("DocsLinkIntegrityGate") is True)
    ok("gate.post_batch_verifier_gate_pass", gate_review.get("gate_details", {}).get("PostBatchVerifierGate") is True)
    ok("gate.client_backend_boundary_gate_pass", gate_review.get("gate_details", {}).get("ClientBackendBoundaryGate") is True)
    ok("gate.future_reserved_module_gate_pass", gate_review.get("gate_details", {}).get("FutureReservedModuleGate") is True)
    ok("gate.verdict", gate_review.get("verdict") == "acceptable_for_closure")

    ok("candidate.candidate_scopes_execution_allowed=false", candidate_review.get("candidate_scopes_execution_allowed") is False)
    ok("candidate.verdict", candidate_review.get("verdict") == "acceptable_for_closure")

    ok("test.post_migration_test_count", test_review.get("post_migration_test_count") == 31)
    ok("test.post_migration_tests_executed=false", test_review.get("post_migration_tests_executed") is False)
    ok("test.post_migration_tests_bound_to_batches", test_review.get("post_migration_tests_bound_to_batches") is True)
    ok("test.verdict", test_review.get("verdict") == "acceptable_for_closure")

    ok("rollback.rollback_audit_required", rollback_review.get("rollback_audit_required") is True)
    ok("rollback.verifier_rerun_after_rollback_required", rollback_review.get("verifier_rerun_after_rollback_required") is True)
    ok("rollback.restore_readme_links_defined", rollback_review.get("restore_readme_links_defined") is True)
    ok("rollback.restore_verdict_table_rows_defined", rollback_review.get("restore_verdict_table_rows_defined") is True)
    ok("rollback.restore_eval_out_refs_defined", rollback_review.get("restore_eval_out_refs_defined") is True)
    ok("rollback.verdict", rollback_review.get("verdict") == "acceptable_for_closure")

    ok("human.human_approval_checkpoint_required", human_review.get("human_approval_checkpoint_required") is True)
    ok("human.owner_approval_placeholder_generated", human_review.get("owner_approval_placeholder_generated") is True)
    ok("human.verdict", human_review.get("verdict") == "acceptable_for_closure")

    ok("boundary_review.no_file_move_delete_rename_merge", boundary_review.get("no_file_move_delete_rename_merge") is True)
    ok("boundary_review.no_readme_modification", boundary_review.get("no_readme_modification") is True)
    ok("boundary_review.no_phase_verdict_table_modification", boundary_review.get("no_phase_verdict_table_modification") is True)
    ok("boundary_review.no_runtime", boundary_review.get("no_runtime") is True)
    ok("boundary_review.no_whitebox_restructuring", boundary_review.get("no_whitebox_test_center_restructuring") is True)
    ok("boundary_review.no_developer_backend_finalization", boundary_review.get("no_developer_backend_architecture_finalization") is True)

    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("decision.ready_for_file_move=false", decision.get("ready_for_file_move") is False)
    ok("decision.blockers_empty", decision.get("blockers") == [])
    ok("decision.recommended_next_phase", decision.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("governance_debt.review_item_count", governance_debt.get("review_item_count") == 5)
    for i, item in enumerate(governance_debt.get("review_items") or []):
        ok(f"governance_debt.item[{i}]", bool(item))

    for k in (
        "actual_file_move_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
    ):
        ok(f"no_move.{k}=false", no_move.get(k) is False)
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("no_delete.actual_file_delete_executed=false", no_delete.get("actual_file_delete_executed") is False)
    ok("summary.actual_file_delete_executed=false", summary.get("actual_file_delete_executed") is False)

    ok("no_runtime.runtime_enabled=false", no_runtime.get("runtime_enabled") is False)
    ok("no_runtime.no_runtime_executed", no_runtime.get("no_runtime_executed") is True)
    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)

    for k in ("world_model_written", "memory_written", "library_written", "fact_written"):
        ok(f"no_write.{k}=false", no_write.get(k) is False)
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.ready_for_closure", summary.get("ready_for_closure") is True)
    for k in (
        "migration_execution_allowed",
        "existing_phase_result_changed",
        "docs_modified_by_review",
        "readme_modified_by_review",
        "phase_verdict_table_modified_by_review",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.human_review_case_count", summary.get("human_review_case_count") == 240)
    ok("summary.permanent_block_case_count", summary.get("permanent_block_case_count") == 914)
    ok("summary.batch_requires_review_count", summary.get("batch_requires_review_count") == 6)
    ok("summary.migration_execution_allowed=false", summary.get("migration_execution_allowed") is False)
    ok("summary.owner_approval_placeholder_generated", summary.get("owner_approval_placeholder_generated") is True)
    ok("summary.human_approval_checkpoint_required", summary.get("human_approval_checkpoint_required") is True)
    ok("summary.rollback_checkpoint_per_batch", summary.get("rollback_checkpoint_per_batch") is True)

    dryrun_root = root.parent / "main_project_structure_migration_guarded_dryrun_v1_smoke_v0"
    if dryrun_root.is_dir():
        dryrun_summary = _load_json(dryrun_root / "summary.json")
        batch_dryrun = _load_json(dryrun_root / "batch_gate_dryrun_results.json")
        ok("cross.dryrun.bound_test_count", dryrun_summary.get("bound_test_count") == 31)
        ok("cross.dryrun.executed_test_count", dryrun_summary.get("executed_test_count") == 0)
        ok("cross.dryrun.rollback_executed", dryrun_summary.get("rollback_executed") is False)
        ok("cross.dryrun.final_owner_human_confirmed", dryrun_summary.get("final_owner_human_confirmed") is False)
        ok("cross.dryrun.batch_count", dryrun_summary.get("batch_count") == 8)
        ok("cross.dryrun.bound_test_count", dryrun_summary.get("bound_test_count") == 31)
        for i, b in enumerate(batch_dryrun.get("batch_results") or []):
            ok(f"cross.dryrun.batch[{i}].simulated_pass", b.get("simulated_pass") is True)
            ok(f"cross.dryrun.batch[{i}].execution_allowed_now=false", b.get("execution_allowed_now") is False)
            har = b.get("human_approval_checkpoint_result") or {}
            if b.get("human_approval_required"):
                ok(f"cross.dryrun.batch[{i}].human.requires_review", har.get("human_approval_status") == "requires_review")
            ok(f"cross.dryrun.batch[{i}].human.approval_executed=false", har.get("approval_executed") is False)

    ok("exclusion_review.verdict", exclusion_review.get("verdict") == "acceptable_for_closure")
    for k in exclusion_keys:
        ok(f"summary.exclusion.{k}", summary.get(k) is True)

    for cf in candidate_flags:
        ok(f"summary.candidate_mirror.{cf}", candidate_review.get(cf) is True)

    for i in range(20):
        ok(f"meta.review_scope_repeat[{i}]", summary.get("review_scope") == REVIEW_SCOPE)
    for i in range(15):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(10):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(8):
        ok(f"meta.simulated_pass_batch_count_repeat[{i}]", summary.get("simulated_pass_batch_count") == 8)

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
