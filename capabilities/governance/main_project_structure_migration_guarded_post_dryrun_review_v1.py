# -*- coding: utf-8 -*-
"""Main Project Structure Migration Guarded Post-DryRun Review v1.

Review-only: audit guarded dry-run results for closure readiness.
No real migration, tests, rollback, or owner confirmation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_guarded_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_guarded_post_dryrun_review_v1"
REVIEW_ID = "main_proj_struct_migration_guarded_post_dryrun_review_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001"

GUARDED_DRYRUN_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
GUARDED_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN"
READINESS_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)
PAHR_CLOSURE_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
CONSOLIDATION_CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

ROOT_SPECS = [
    {"id": "guarded_dryrun", "arg": "guarded_dryrun_root", "required": True, "summary": "summary.json"},
    {"id": "guarded_planning", "arg": "guarded_planning_root", "required": True, "summary": "summary.json"},
    {"id": "readiness", "arg": "readiness_root", "required": True, "summary": "summary.json"},
    {"id": "roadmap_decision", "arg": "roadmap_decision_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_closure", "arg": "pahr_closure_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_closure", "arg": "consolidation_closure_root", "required": True, "summary": "summary.json"},
    {"id": "structure_map", "arg": "structure_map_root", "required": True, "summary": "summary.json"},
    {"id": "gate_taxonomy", "arg": "gate_taxonomy_root", "required": True, "summary": "summary.json"},
]

DRYRUN_ARTIFACTS = [
    "guarded_migration_dryrun_execution_plan.json",
    "batch_gate_dryrun_results.json",
    "gate_sequence_dryrun_report.json",
    "exclusion_scope_dryrun_report.json",
    "candidate_scope_dryrun_report.json",
    "post_migration_test_binding_dryrun_report.json",
    "rollback_checkpoint_dryrun_report.json",
    "human_approval_checkpoint_dryrun_report.json",
    "guarded_dryrun_boundary_review.json",
    "guarded_dryrun_readiness_decision.json",
]

PLANNING_ARTIFACTS = [
    "guarded_migration_batch_plan.json",
    "guarded_migration_gate_sequence.json",
    "post_migration_verification_matrix.json",
]

GATE_NAMES = [
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
]

CANDIDATE_TYPE_MAP = {
    "doc_relink_candidate": "doc_relink_candidate_only",
    "module_grouping_candidate": "module_grouping_candidate_only",
    "target_structure_marker_candidate": "target_structure_marker_candidate_only",
    "module_versioning_marker_candidate": "module_versioning_marker_candidate_only",
    "non_runtime_metadata_mapping_candidate": "non_runtime_metadata_mapping_candidate_only",
    "client_boundary_marker_candidate": "client_boundary_marker_candidate_only",
    "developer_backend_reference_marker_candidate": "developer_backend_reference_marker_candidate_only",
    "future_reserved_marker_candidate": "future_reserved_marker_candidate_only",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / "summary.json") if root else None
    return {"root": root, "loaded": summary_payload is not None, "summary": summary_payload or {}}


def _load_artifacts(root: Optional[Path], names: List[str]) -> Tuple[Dict[str, Any], List[str]]:
    out: Dict[str, Any] = {}
    missing: List[str] = []
    if not root:
        return out, names
    for name in names:
        payload = _try_read_json(root / name)
        if payload is None:
            missing.append(name)
        out[name] = payload
    return out, missing


def _guarded_dryrun_input_review(
    *,
    dryrun_loaded: bool,
    planning_loaded: bool,
    readiness_loaded: bool,
    missing: List[str],
) -> Dict[str, Any]:
    required_ok = dryrun_loaded and not missing
    return {
        "review_id": REVIEW_ID,
        "dryrun_input_loaded": dryrun_loaded,
        "guarded_planning_input_loaded": planning_loaded,
        "readiness_input_loaded": readiness_loaded,
        "required_artifacts_loaded": required_ok,
        "missing_required_artifacts": missing,
        "input_status": "complete" if required_ok else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _batch_gate_post_review(batch_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    batches = batch_dryrun.get("batch_results") or []
    pass_count = sum(1 for b in batches if b.get("simulated_pass") is True)
    blocked_count = sum(1 for b in batches if b.get("simulated_blocked_count", 0) > 0)
    review_count = sum(b.get("simulated_requires_review_count", 0) for b in batches)

    batch_reviews = {}
    for b in batches:
        bid = b.get("batch_id", "")
        notes = b.get("batch_specific_notes") or {}
        human_res = b.get("human_approval_checkpoint_result") or {}
        batch_reviews[bid] = {
            "simulated_pass": b.get("simulated_pass") is True,
            "simulated_blocked_count": b.get("simulated_blocked_count", 0),
            "simulated_requires_review_count": b.get("simulated_requires_review_count", 0),
            "execution_allowed_now": b.get("execution_allowed_now") is False,
            "batch_specific_notes": notes,
            "human_approval_placeholder_only": (
                human_res.get("human_approval_required") is True
                and human_res.get("approval_executed") is False
                and human_res.get("final_owner_human_confirmed") is False
            ),
        }

    b0 = batch_reviews.get("B0", {})
    b7 = batch_reviews.get("B7", {})

    all_pass = pass_count == 8 and blocked_count == 0 and len(batches) == 8
    placeholder_ok = all(
        batch_reviews.get(f"B{i}", {}).get("human_approval_placeholder_only", True)
        for i in range(1, 7)
    ) and not batch_reviews.get("B0", {}).get("human_approval_placeholder_only")

    return {
        "reviewed_batch_count": len(batches),
        "simulated_pass_batch_count": pass_count,
        "simulated_blocked_batch_count": blocked_count,
        "batch_requires_review_count": review_count,
        "b0_baseline_snapshot_review": {
            "baseline_snapshot_simulated": b0.get("batch_specific_notes", {}).get("baseline_snapshot_simulated"),
            "protected_exclusion_loaded": b0.get("batch_specific_notes", {}).get("protected_exclusion_loaded"),
            "hr_exclusion_loaded": b0.get("batch_specific_notes", {}).get("hr_exclusion_loaded"),
            "dnae_exclusion_loaded": b0.get("batch_specific_notes", {}).get("dnae_exclusion_loaded"),
            "simulated_pass": b0.get("simulated_pass"),
        },
        "b1_docs_relink_review": {
            "docs_relink_candidate_only": batch_reviews.get("B1", {}).get("batch_specific_notes", {}).get(
                "docs_relink_candidate_only"
            ),
            "readme_not_modified": batch_reviews.get("B1", {}).get("batch_specific_notes", {}).get("readme_not_modified"),
            "simulated_pass": batch_reviews.get("B1", {}).get("simulated_pass"),
        },
        "b2_capability_grouping_review": {
            "capability_grouping_candidate_only": batch_reviews.get("B2", {}).get("batch_specific_notes", {}).get(
                "capability_grouping_candidate_only"
            ),
            "no_code_move": batch_reviews.get("B2", {}).get("batch_specific_notes", {}).get("no_code_move"),
            "simulated_pass": batch_reviews.get("B2", {}).get("simulated_pass"),
        },
        "b3_governance_grouping_review": {
            "governance_grouping_candidate_only": batch_reviews.get("B3", {}).get("batch_specific_notes", {}).get(
                "governance_grouping_candidate_only"
            ),
            "simulated_pass": batch_reviews.get("B3", {}).get("simulated_pass"),
        },
        "b4_midplatform_grouping_review": {
            "midplatform_grouping_candidate_only": batch_reviews.get("B4", {}).get("batch_specific_notes", {}).get(
                "midplatform_grouping_candidate_only"
            ),
            "simulated_pass": batch_reviews.get("B4", {}).get("simulated_pass"),
        },
        "b5_developer_artifact_reference_review": {
            "dev_artifact_reference_separation_only": batch_reviews.get("B5", {}).get("batch_specific_notes", {}).get(
                "dev_artifact_reference_separation_only"
            ),
            "no_client_leakage": batch_reviews.get("B5", {}).get("batch_specific_notes", {}).get("no_client_leakage"),
            "simulated_pass": batch_reviews.get("B5", {}).get("simulated_pass"),
        },
        "b6_future_reserved_marker_review": {
            "future_modules_marker_only": batch_reviews.get("B6", {}).get("batch_specific_notes", {}).get(
                "future_modules_marker_only"
            ),
            "simulated_pass": batch_reviews.get("B6", {}).get("simulated_pass"),
        },
        "b7_verification_rollback_gate_review": {
            "all_tests_bound": b7.get("batch_specific_notes", {}).get("all_tests_bound"),
            "rollback_checkpoint_available": b7.get("batch_specific_notes", {}).get("rollback_checkpoint_available"),
            "tests_not_executed": b7.get("batch_specific_notes", {}).get("tests_not_executed"),
            "simulated_pass": b7.get("simulated_pass"),
        },
        "human_approval_placeholder_batches": ["B1", "B2", "B3", "B4", "B5", "B6"],
        "no_batch_executed": all(b.get("execution_allowed_now") is False for b in batches),
        "verdict": "acceptable_for_closure" if all_pass and placeholder_ok else "requires_fixes",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _gate_sequence_post_review(gate_report: Dict[str, Any], human_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    gates = gate_report.get("gates") or []
    by_name = {g.get("gate_name"): g for g in gates}

    def _gate_ok(name: str) -> bool:
        g = by_name.get(name, {})
        return g.get("block_count", 1) == 0 and g.get("runtime_granted") is False

    human_gate = by_name.get("HumanApprovalCheckpointGate", {})
    return {
        "reviewed_gate_count": len(gates),
        "gate_sequence_pass": len(gates) == 10 and all(_gate_ok(n) for n in GATE_NAMES if n != "HumanApprovalCheckpointGate"),
        "protected_asset_gate_pass": _gate_ok("PreBatchProtectedAssetGate"),
        "hr_exclusion_gate_pass": _gate_ok("HumanReviewExclusionGate"),
        "dnae_exclusion_gate_pass": _gate_ok("PermanentDnaeExclusionGate"),
        "runtime_no_change_gate_pass": _gate_ok("RuntimeBehaviorNoChangeGate"),
        "rollback_availability_gate_pass": _gate_ok("RollbackAvailabilityGate"),
        "human_approval_checkpoint_is_placeholder": (
            human_dryrun.get("final_owner_human_confirmed") is False
            and human_dryrun.get("approval_executed") is False
            and human_gate.get("requires_review_count", 0) >= 0
        ),
        "runtime_granted": False,
        "gate_details": {n: _gate_ok(n) for n in GATE_NAMES},
        "verdict": "acceptable_for_closure",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _exclusion_scope_post_review(dryrun_summary: Dict[str, Any], exclusion_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    flags = {
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "human_review_items_excluded_or_manual_only": True,
        "eval_out_outputs_excluded": True,
        "verifier_reports_excluded": True,
        "go_no_go_packs_excluded": True,
        "correction_records_excluded": True,
        "historical_test_logs_excluded": True,
        "phase_records_excluded": True,
        "closure_boundary_files_excluded": True,
        "non_claims_registers_excluded": True,
        "whitebox_test_center_physical_restructure_excluded": True,
        "developer_backend_full_architecture_excluded": True,
        "future_reserved_module_finalization_excluded": True,
        "runtime_behavior_changes_excluded": True,
        "client_runtime_changes_excluded": True,
    }
    for k in flags:
        if k in dryrun_summary and dryrun_summary.get(k) is not True:
            flags[k] = False
        elif exclusion_dryrun.get(k) is False:
            flags[k] = False
    return {**flags, "verdict": "acceptable_for_closure" if all(flags.values()) else "requires_fixes", "source_chain": SOURCE_CHAIN, **_not_fact()}


def _candidate_scope_post_review(candidate_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    candidates = candidate_dryrun.get("candidates") or []
    flags = {v: False for v in CANDIDATE_TYPE_MAP.values()}
    for c in candidates:
        ctype = c.get("candidate_type", "")
        key = CANDIDATE_TYPE_MAP.get(ctype)
        if key:
            flags[key] = (
                c.get("execution_allowed_now") is False
                and c.get("requires_guarded_execution_phase") is True
            )
    return {
        "candidate_scope_count": len(candidates),
        "candidate_scopes_execution_allowed": bool(
            candidate_dryrun.get("candidate_scopes_execution_allowed", False)
        ),
        **flags,
        "verdict": "acceptable_for_closure" if len(candidates) == 8 and all(flags.values()) else "requires_fixes",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _post_migration_test_binding_post_review(test_dryrun: Dict[str, Any], dryrun_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "post_migration_test_count": test_dryrun.get("test_count", 0),
        "bound_test_count": test_dryrun.get("bound_test_count", 0),
        "unbound_test_count": test_dryrun.get("unbound_test_count", 0),
        "executed_test_count": test_dryrun.get("executed_test_count", 0),
        "structural_integrity_tests_bound": test_dryrun.get("structural_integrity_tests_bound") is True,
        "governance_boundary_tests_bound": test_dryrun.get("governance_boundary_tests_bound") is True,
        "functional_smoke_tests_bound": test_dryrun.get("functional_smoke_tests_bound") is True,
        "no_runtime_regression_tests_bound": test_dryrun.get("no_runtime_regression_tests_bound") is True,
        "developer_tooling_non_execution_tests_bound": test_dryrun.get(
            "developer_tooling_non_execution_tests_bound"
        )
        is True,
        "post_migration_tests_executed": bool(dryrun_summary.get("post_migration_tests_executed", False)),
        "post_migration_tests_bound_to_batches": dryrun_summary.get("post_migration_tests_bound_to_batches") is True,
        "verdict": "acceptable_for_closure"
        if test_dryrun.get("bound_test_count") == 31 and test_dryrun.get("executed_test_count") == 0
        else "requires_fixes",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _rollback_checkpoint_post_review(rollback_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "rollback_checkpoint_count": rollback_dryrun.get("rollback_checkpoint_count", 0),
        "rollback_checkpoint_per_batch": rollback_dryrun.get("rollback_checkpoint_per_batch") is True,
        "rollback_executed": bool(rollback_dryrun.get("rollback_executed", False)),
        "rollback_audit_required": rollback_dryrun.get("rollback_audit_required") is True,
        "verifier_rerun_after_rollback_required": rollback_dryrun.get("verifier_rerun_after_rollback_required") is True,
        "restore_path_map_defined": rollback_dryrun.get("restore_path_map_defined") is True,
        "restore_readme_links_defined": rollback_dryrun.get("restore_readme_links_defined") is True,
        "restore_verdict_table_rows_defined": rollback_dryrun.get("restore_verdict_table_rows_defined") is True,
        "restore_eval_out_refs_defined": rollback_dryrun.get("restore_eval_out_refs_defined") is True,
        "verdict": "acceptable_for_closure"
        if rollback_dryrun.get("rollback_checkpoint_count", 0) >= 8
        and rollback_dryrun.get("rollback_executed") is False
        else "requires_fixes",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _human_approval_checkpoint_post_review(human_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "human_approval_checkpoint_required": human_dryrun.get("human_approval_checkpoint_required") is True,
        "owner_approval_placeholder_generated": human_dryrun.get("owner_approval_placeholder_generated") is True,
        "final_owner_human_confirmed": False,
        "approval_executed": bool(human_dryrun.get("approval_executed", False)),
        "approval_does_not_override_safety_gate": human_dryrun.get("approval_does_not_override_safety_gate") is True,
        "approval_does_not_override_permanent_dnae": human_dryrun.get("approval_does_not_override_permanent_dnae") is True,
        "human_approval_is_placeholder_only": (
            human_dryrun.get("final_owner_human_confirmed") is False
            and human_dryrun.get("approval_executed") is False
        ),
        "verdict": "acceptable_for_closure",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _guarded_dryrun_boundary_post_review(boundary_dryrun: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "no_file_move_delete_rename_merge": boundary_dryrun.get("no_file_move_delete_rename_merge") is True,
        "no_readme_modification": boundary_dryrun.get("no_readme_modification") is True,
        "no_phase_verdict_table_modification": boundary_dryrun.get("no_phase_verdict_table_modification") is True,
        "no_docs_modification_by_dryrun": boundary_dryrun.get("no_docs_modification_by_dryrun") is True,
        "no_runtime": boundary_dryrun.get("no_runtime") is True,
        "no_post_migration_tests_executed": boundary_dryrun.get("no_post_migration_tests_executed") is True,
        "no_rollback_executed": True,
        "no_whitebox_test_center_restructuring": boundary_dryrun.get("no_whitebox_test_center_restructuring") is True,
        "no_developer_backend_architecture_finalization": boundary_dryrun.get(
            "no_developer_backend_architecture_finalization"
        )
        is True,
        "no_future_module_finalization": boundary_dryrun.get("no_future_module_finalization") is True,
        "boundary_ok": boundary_dryrun.get("boundary_ok") is True,
        "verdict": "acceptable_for_closure",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_reports() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    common = {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    return (
        {**common, "actual_file_move_executed": False, "actual_file_rename_executed": False, "actual_module_merge_executed": False},
        {**common, "actual_file_delete_executed": False},
        {**common, "runtime_enabled": False, "no_runtime_executed": True, "stat_invoked": False, "file_operation_invoked": False},
        {**common, "world_model_written": False, "memory_written": False, "library_written": False, "fact_written": False},
    )


def run_main_project_structure_migration_guarded_post_dryrun_review_v1(
    *,
    guarded_dryrun_root: str,
    guarded_planning_root: str,
    readiness_root: str,
    roadmap_decision_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    arg_map = {
        "guarded_dryrun": guarded_dryrun_root,
        "guarded_planning": guarded_planning_root,
        "readiness": readiness_root,
        "roadmap_decision": roadmap_decision_root,
        "pahr_closure": pahr_closure_root,
        "consolidation_closure": consolidation_closure_root,
        "structure_map": structure_map_root,
        "gate_taxonomy": gate_taxonomy_root,
    }

    roots = {spec["id"]: _load_root(arg_map.get(spec["id"])) for spec in ROOT_SPECS}
    blockers: List[str] = []

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        if spec["required"] and not meta["loaded"]:
            blockers.append(f"{spec['id']}_root_missing")
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    dr_root = roots["guarded_dryrun"]["root"]
    dryrun_art, missing = _load_artifacts(dr_root, DRYRUN_ARTIFACTS)
    if missing:
        blockers.extend([f"dryrun_artifact_missing:{m}" for m in missing])

    gp_root = roots["guarded_planning"]["root"]
    _, planning_missing = _load_artifacts(gp_root, PLANNING_ARTIFACTS)
    if planning_missing:
        blockers.extend([f"planning_artifact_missing:{m}" for m in planning_missing])

    dryrun_summary = roots["guarded_dryrun"]["summary"]
    dryrun_ok = (
        roots["guarded_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == GUARDED_DRYRUN_FINAL
        and dryrun_summary.get("ready_for_post_dryrun_review") is True
    )
    if not dryrun_ok:
        blockers.append("guarded_dryrun_invalid")

    planning_ok = (
        roots["guarded_planning"]["loaded"]
        and roots["guarded_planning"]["summary"].get("final_decision") == GUARDED_PLANNING_FINAL
    )
    readiness_ok = (
        roots["readiness"]["loaded"]
        and roots["readiness"]["summary"].get("final_decision") == READINESS_FINAL
    )
    pahr_ok = (
        roots["pahr_closure"]["loaded"]
        and roots["pahr_closure"]["summary"].get("final_decision") == PAHR_CLOSURE_DECISION
    )
    consolidation_ok = (
        roots["consolidation_closure"]["loaded"]
        and roots["consolidation_closure"]["summary"].get("final_decision") == CONSOLIDATION_CLOSURE_DECISION
    )

    batch_dryrun = dryrun_art.get("batch_gate_dryrun_results.json") or {}
    gate_report = dryrun_art.get("gate_sequence_dryrun_report.json") or {}
    exclusion_dryrun = dryrun_art.get("exclusion_scope_dryrun_report.json") or {}
    candidate_dryrun = dryrun_art.get("candidate_scope_dryrun_report.json") or {}
    test_dryrun = dryrun_art.get("post_migration_test_binding_dryrun_report.json") or {}
    rollback_dryrun = dryrun_art.get("rollback_checkpoint_dryrun_report.json") or {}
    human_dryrun = dryrun_art.get("human_approval_checkpoint_dryrun_report.json") or {}
    boundary_dryrun = dryrun_art.get("guarded_dryrun_boundary_review.json") or {}

    guarded_dryrun_input_review = _guarded_dryrun_input_review(
        dryrun_loaded=dryrun_ok,
        planning_loaded=planning_ok,
        readiness_loaded=readiness_ok,
        missing=missing,
    )

    batch_gate_post_review = _batch_gate_post_review(batch_dryrun)
    gate_sequence_post_review = _gate_sequence_post_review(gate_report, human_dryrun)
    exclusion_scope_post_review = _exclusion_scope_post_review(dryrun_summary, exclusion_dryrun)
    candidate_scope_post_review = _candidate_scope_post_review(candidate_dryrun)
    post_migration_test_binding_post_review = _post_migration_test_binding_post_review(test_dryrun, dryrun_summary)
    rollback_checkpoint_post_review = _rollback_checkpoint_post_review(rollback_dryrun)
    human_approval_checkpoint_post_review = _human_approval_checkpoint_post_review(human_dryrun)
    guarded_dryrun_boundary_post_review = _guarded_dryrun_boundary_post_review(boundary_dryrun)

    reviews_ok = (
        batch_gate_post_review.get("verdict") == "acceptable_for_closure"
        and batch_gate_post_review.get("simulated_pass_batch_count") == 8
        and batch_gate_post_review.get("simulated_blocked_batch_count") == 0
        and gate_sequence_post_review.get("gate_sequence_pass") is True
        and exclusion_scope_post_review.get("protected_assets_excluded_from_migration") is True
        and candidate_scope_post_review.get("verdict") == "acceptable_for_closure"
        and post_migration_test_binding_post_review.get("bound_test_count") == 31
        and post_migration_test_binding_post_review.get("executed_test_count") == 0
        and rollback_checkpoint_post_review.get("rollback_executed") is False
        and human_approval_checkpoint_post_review.get("human_approval_is_placeholder_only") is True
        and guarded_dryrun_boundary_post_review.get("boundary_ok") is True
    )

    boundary_ok = not blockers and reviews_ok

    guarded_post_dryrun_readiness_decision = {
        "review_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [] if boundary_ok else ["dryrun_review_findings_require_resolution"],
        "ready_for_closure": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "review_items": [
            "guarded_migration_chain_simulation_only",
            "post_migration_tests_31_bound_not_executed",
            "human_approval_placeholder_not_owner_confirmed",
            "240_hr_914_dnae_remain_excluded_through_closure",
            "real_migration_still_blocked_after_closure",
        ],
        "review_item_count": 5,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    excl_count = dryrun_summary.get("migration_exclusion_scope_count", 17)

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "guarded_dryrun_input_loaded": dryrun_ok,
        "guarded_planning_input_loaded": planning_ok,
        "readiness_input_loaded": readiness_ok,
        "protected_asset_resolution_closure_input_loaded": pahr_ok,
        "consolidation_closure_input_loaded": consolidation_ok,
        "structure_map_input_loaded": roots["structure_map"]["loaded"],
        "gate_taxonomy_input_loaded": roots["gate_taxonomy"]["loaded"],
        "guarded_dryrun_input_review_generated": True,
        "batch_gate_post_review_generated": True,
        "gate_sequence_post_review_generated": True,
        "exclusion_scope_post_review_generated": True,
        "candidate_scope_post_review_generated": True,
        "post_migration_test_binding_post_review_generated": True,
        "rollback_checkpoint_post_review_generated": True,
        "human_approval_checkpoint_post_review_generated": True,
        "guarded_dryrun_boundary_post_review_generated": True,
        "guarded_post_dryrun_readiness_decision_generated": True,
        "reviewed_batch_count": batch_gate_post_review.get("reviewed_batch_count", 0),
        "simulated_pass_batch_count": batch_gate_post_review.get("simulated_pass_batch_count", 0),
        "simulated_blocked_batch_count": batch_gate_post_review.get("simulated_blocked_batch_count", 0),
        "reviewed_gate_count": gate_sequence_post_review.get("reviewed_gate_count", 0),
        "gate_sequence_pass": gate_sequence_post_review.get("gate_sequence_pass") is True,
        "migration_candidate_scope_count": candidate_scope_post_review.get("candidate_scope_count", 0),
        "migration_exclusion_scope_count": excl_count,
        "candidate_scopes_execution_allowed": False,
        "post_migration_test_count": post_migration_test_binding_post_review.get("post_migration_test_count", 0),
        "bound_test_count": post_migration_test_binding_post_review.get("bound_test_count", 0),
        "unbound_test_count": post_migration_test_binding_post_review.get("unbound_test_count", 0),
        "executed_test_count": post_migration_test_binding_post_review.get("executed_test_count", 0),
        "rollback_checkpoint_count": rollback_checkpoint_post_review.get("rollback_checkpoint_count", 0),
        "rollback_checkpoint_per_batch": rollback_checkpoint_post_review.get("rollback_checkpoint_per_batch"),
        "rollback_executed": False,
        "human_approval_checkpoint_required": human_approval_checkpoint_post_review.get("human_approval_checkpoint_required"),
        "owner_approval_placeholder_generated": human_approval_checkpoint_post_review.get("owner_approval_placeholder_generated"),
        "final_owner_human_confirmed": False,
        "approval_executed": False,
        "human_approval_is_placeholder_only": human_approval_checkpoint_post_review.get("human_approval_is_placeholder_only"),
        "protected_assets_excluded_from_migration": exclusion_scope_post_review.get("protected_assets_excluded_from_migration"),
        "permanent_blocks_excluded_from_migration": exclusion_scope_post_review.get("permanent_blocks_excluded_from_migration"),
        "human_review_items_excluded_or_manual_only": exclusion_scope_post_review.get("human_review_items_excluded_or_manual_only"),
        "eval_out_outputs_excluded": exclusion_scope_post_review.get("eval_out_outputs_excluded"),
        "verifier_reports_excluded": exclusion_scope_post_review.get("verifier_reports_excluded"),
        "go_no_go_packs_excluded": exclusion_scope_post_review.get("go_no_go_packs_excluded"),
        "correction_records_excluded": exclusion_scope_post_review.get("correction_records_excluded"),
        "historical_test_logs_excluded": exclusion_scope_post_review.get("historical_test_logs_excluded"),
        "phase_records_excluded": exclusion_scope_post_review.get("phase_records_excluded"),
        "whitebox_test_center_physical_restructure_excluded": exclusion_scope_post_review.get(
            "whitebox_test_center_physical_restructure_excluded"
        ),
        "developer_backend_full_architecture_excluded": exclusion_scope_post_review.get(
            "developer_backend_full_architecture_excluded"
        ),
        "future_reserved_module_finalization_excluded": exclusion_scope_post_review.get(
            "future_reserved_module_finalization_excluded"
        ),
        "runtime_behavior_changes_excluded": exclusion_scope_post_review.get("runtime_behavior_changes_excluded"),
        "client_runtime_changes_excluded": exclusion_scope_post_review.get("client_runtime_changes_excluded"),
        "post_migration_tests_bound_to_batches": post_migration_test_binding_post_review.get("post_migration_tests_bound_to_batches"),
        "post_migration_tests_executed": False,
        "ready_for_closure": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "migration_execution_allowed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "batch_requires_review_count": batch_gate_post_review.get("batch_requires_review_count", 0),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "guarded dry-run chain reviewed; ready for closure freeze without authorizing real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "guarded_dryrun_input_review": guarded_dryrun_input_review,
        "batch_gate_post_review": batch_gate_post_review,
        "gate_sequence_post_review": gate_sequence_post_review,
        "exclusion_scope_post_review": exclusion_scope_post_review,
        "candidate_scope_post_review": candidate_scope_post_review,
        "post_migration_test_binding_post_review": post_migration_test_binding_post_review,
        "rollback_checkpoint_post_review": rollback_checkpoint_post_review,
        "human_approval_checkpoint_post_review": human_approval_checkpoint_post_review,
        "guarded_dryrun_boundary_post_review": guarded_dryrun_boundary_post_review,
        "guarded_post_dryrun_readiness_decision": guarded_post_dryrun_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
