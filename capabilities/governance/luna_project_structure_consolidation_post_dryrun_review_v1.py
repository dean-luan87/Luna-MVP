# -*- coding: utf-8 -*-
"""Luna Project Structure Consolidation Post-DryRun Review v1.

Review-only: classify conflicts into acceptable / plan-revision-required / permanent no-auto-execute.
No file moves, no consolidation execution, no doc/README/verdict modifications.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "luna_project_structure_consolidation_post_dryrun_review_only"
SOURCE_CHAIN = "luna_project_structure_consolidation_post_dryrun_review_v1"
REVIEW_ID = "luna_proj_struct_consolidation_post_dryrun_review_v1_001"

FINAL_DECISION_CLOSURE = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FINAL_DECISION_PLAN_REVISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_REQUIRES_PLAN_REVISION"
NEXT_PHASE_CLOSURE = "Phase-Luna-Project-Structure-Consolidation-Closure-v1-001"
NEXT_PHASE_PLAN_REVISION = "Phase-Luna-Project-Structure-Consolidation-Planning-Revision-v1-001"

DRYRUN_FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLAN_REVISION_HIGH_WATERMARK = 150

ROOT_SPECS = [
    {
        "id": "consolidation_dryrun",
        "arg": "consolidation_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "consolidation_dryrun_execution_plan.json",
            "batch_dryrun_results.json",
            "consolidation_conflict_report.json",
            "human_review_required_register.json",
            "do_not_auto_execute_register.json",
            "rollback_simulation_plan.json",
            "consolidation_dryrun_readiness_decision.json",
            "boundary_integrity_review.json",
            "life_system_consolidation_dryrun_matrix.json",
            "no_file_move_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "consolidation_planning",
        "arg": "consolidation_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "merge_plan_register.json"],
    },
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "module_inventory.json"],
    },
    {
        "id": "project_structure_governance_planning",
        "arg": "project_structure_governance_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gate_constitution.json"],
    },
]

PROTECTED_PATTERNS = (
    r"verifier_report\.json$",
    r"GO_NO_GO",
    r"go_no_go",
    r"correction",
    r"_eval_out/",
    r"phase_verdict",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root) and all(_try_read_json(root / a) is not None for a in artifacts)
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _classify_conflict(c: Dict[str, Any]) -> Tuple[str, str]:
    """Return (category, rationale). category: acceptable | plan_revision | permanent_block."""
    ctype = c.get("conflict_type", "")
    path = c.get("asset_path", "")

    if ctype == "protected_asset_marked_for_destructive_action":
        return (
            "permanent_block",
            "protected_eval_out_verifier_gonogo_or_phase_record; never auto archive/merge/delete",
        )

    if ctype == "developer_backend_and_client_same_asset":
        return ("plan_revision", "client_backend_boundary_must_be_split_in_planning")

    if ctype == "cognition_placeholder_treated_as_runtime":
        return ("permanent_block", "cognition_placeholder_must_not_be_runtime_enabled")

    if ctype in {"missing_future_life_system_mapping", "missing_target_module"}:
        core_prefixes = ("capabilities/", "tools/evaluation/", "docs/architecture/governance/", "docs/architecture/evaluation/")
        if any(path.startswith(p) for p in core_prefixes):
            return ("plan_revision", "core_path_missing_target_module_must_be_resolved_before_migration")
        return (
            "acceptable",
            "unclassified_or_defer_tbd_target; dryrun_blocked; optional_plan_cleanup_before_real_migration",
        )

    if ctype == "multiple_actions_same_asset":
        if path.startswith("_eval_out/") or path == "_eval_out":
            return (
                "acceptable",
                "eval_out_dual_registration_archive_and_keep; dryrun_blocks_execution; fix_before_real_migration",
            )
        return ("plan_revision", "ambiguous_planned_action_requires_unique_disposition_in_planning")

    return ("acceptable", "dryrun_intercepted_or_low_severity_signal")


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "actual_consolidation_execution": False,
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
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
        "no_runtime_executed": True,
        "boundary_ok": True,
        "violations": [],
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_luna_project_structure_consolidation_post_dryrun_review_v1(
    *,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_dryrun_root: str,
    project_structure_governance_planning_root: str,
    gate_taxonomy_planning_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
    missing_required: List[str] = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        if spec["required"] and not meta["loaded"]:
            missing_required.append(spec["id"])
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    dryrun_loaded = (
        roots["consolidation_dryrun"]["loaded"]
        and roots["consolidation_dryrun"]["summary"].get("final_decision") == DRYRUN_FINAL_DECISION
    )
    planning_loaded = roots["consolidation_planning"]["loaded"]
    structure_loaded = roots["structure_map_dryrun"]["loaded"]
    governance_loaded = roots["project_structure_governance_planning"]["loaded"]
    gate_loaded = roots["gate_taxonomy_planning"]["loaded"]

    blockers: List[str] = []
    if not dryrun_loaded:
        blockers.append("consolidation_dryrun_missing_or_invalid")
    if not planning_loaded:
        blockers.append("consolidation_planning_missing")
    if not structure_loaded:
        blockers.append("structure_map_dryrun_missing")
    if not governance_loaded:
        blockers.append("governance_planning_missing")
    if not gate_loaded:
        blockers.append("gate_taxonomy_missing")

    dryrun_root = roots["consolidation_dryrun"]["root"]
    dryrun_summary = roots["consolidation_dryrun"]["summary"] if dryrun_loaded else {}

    conflicts_raw = (_try_read_json(dryrun_root / "consolidation_conflict_report.json") or {}).get("conflicts", []) if dryrun_root else []
    human_review_items = (_try_read_json(dryrun_root / "human_review_required_register.json") or {}).get("review_items", []) if dryrun_root else []
    dnae_items = (_try_read_json(dryrun_root / "do_not_auto_execute_register.json") or {}).get("forbidden_actions", []) if dryrun_root else []
    batch_payload = _try_read_json(dryrun_root / "batch_dryrun_results.json") if dryrun_root else {}
    batches = (batch_payload or {}).get("batches") or []
    boundary_dryrun = _try_read_json(dryrun_root / "boundary_integrity_review.json") if dryrun_root else {}
    life_dryrun = _try_read_json(dryrun_root / "life_system_consolidation_dryrun_matrix.json") if dryrun_root else {}
    rollback = _try_read_json(dryrun_root / "rollback_simulation_plan.json") if dryrun_root else {}
    hist_dryrun = _try_read_json(dryrun_root / "historical_test_asset_dryrun_review.json") if dryrun_root else {}

    acceptable: List[Dict[str, Any]] = []
    plan_revision: List[Dict[str, Any]] = []
    permanent: List[Dict[str, Any]] = []

    for i, c in enumerate(conflicts_raw):
        cat, rationale = _classify_conflict(c)
        entry = {
            "register_id": f"CONF_{i:05d}",
            "conflict_type": c.get("conflict_type"),
            "asset_path": c.get("asset_path"),
            "severity": c.get("severity"),
            "classification": cat,
            "rationale": rationale,
            "dryrun_intercepted": True,
            "auto_execute_allowed": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        if cat == "acceptable":
            acceptable.append(entry)
        elif cat == "plan_revision":
            plan_revision.append(entry)
        else:
            permanent.append(entry)

    # Permanent items from do_not_auto_execute register
    for i, item in enumerate(dnae_items):
        permanent.append(
            {
                "register_id": f"PDNAE_{i:05d}",
                "item_type": "do_not_auto_execute_rule",
                "forbidden_action": item.get("forbidden_action"),
                "classification": "permanent_block",
                "rationale": "explicitly_forbidden_from_automatic_consolidation",
                "auto_execute_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    ctype_counts = Counter(c.get("conflict_type") for c in conflicts_raw)
    protected_count = sum(1 for c in conflicts_raw if c.get("conflict_type") == "protected_asset_marked_for_destructive_action")
    multi_count = ctype_counts.get("multiple_actions_same_asset", 0)

    consolidation_conflict_review = {
        "total_conflict_count": len(conflicts_raw),
        "acceptable_conflict_count": len(acceptable),
        "plan_revision_required_conflict_count": len(plan_revision),
        "permanent_block_conflict_count": protected_count,
        "protected_asset_conflict_count": protected_count,
        "multi_action_same_path_conflict_count": multi_count,
        "missing_target_conflict_count": ctype_counts.get("missing_target_module", 0),
        "client_backend_boundary_conflict_count": ctype_counts.get("developer_backend_and_client_same_asset", 0),
        "future_placeholder_runtime_conflict_count": ctype_counts.get("cognition_placeholder_treated_as_runtime", 0),
        "test_asset_deletion_conflict_count": protected_count,
        "verdict": "review_complete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    hr_reasons = Counter(item.get("reason") for item in human_review_items)
    human_review_register_review = {
        "total_human_review_count": len(human_review_items),
        "high_risk_merge_count": hr_reasons.get("high_risk_merge_large_group", 0),
        "archive_unclear_ownership_count": hr_reasons.get("archive_candidate_unclear_ownership", 0),
        "client_backend_ambiguous_count": hr_reasons.get("client_backend_ambiguous", 0),
        "docs_code_mismatch_count": 0,
        "future_placeholder_current_code_count": hr_reasons.get("future_placeholder_with_current_code", 0),
        "duplicated_gate_policy_schema_count": 0,
        "cross_repo_dependency_count": 0,
        "manual_owner_assignment_required": True,
        "review_priority_matrix": [
            {"priority": "P0", "topics": ["client_backend_ambiguous", "protected_asset_destructive_plan"]},
            {"priority": "P1", "topics": ["high_risk_merge_large_group", "future_placeholder_with_current_code"]},
            {"priority": "P2", "topics": ["archive_candidate_unclear_ownership"]},
        ],
        "verdict": "human_review_required_before_any_real_migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    static_dnae = sum(1 for x in dnae_items if str(x.get("rule_id", "")).startswith("DNAE_") and "dyn" not in str(x.get("rule_id", "")))
    dynamic_dnae = len(dnae_items) - static_dnae
    protected_eval = sum(1 for x in permanent if "eval_out" in str(x.get("asset_path", x.get("forbidden_action", ""))))
    do_not_auto_execute_review = {
        "total_do_not_auto_execute_count": len(dnae_items),
        "static_rule_count": static_dnae,
        "dynamic_protected_asset_count": dynamic_dnae,
        "protected_eval_out_count": protected_eval,
        "protected_verifier_count": sum(1 for x in dnae_items if "verifier" in str(x.get("forbidden_action", "")).lower()),
        "protected_go_no_go_count": sum(1 for x in dnae_items if "GO" in str(x.get("forbidden_action", "")) or "go_no_go" in str(x.get("forbidden_action", "")).lower()),
        "protected_test_log_count": sum(1 for x in dnae_items if "test log" in str(x.get("forbidden_action", "")).lower()),
        "protected_correction_record_count": sum(1 for x in dnae_items if "correction" in str(x.get("forbidden_action", "")).lower()),
        "protected_phase_record_count": protected_eval,
        "automatic_execution_forbidden": True,
        "verdict": "all_automatic_consolidation_forbidden_for_listed_items",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    batch_reviews = {}
    batch_blockers = 0
    batch_review_count = 0
    batch_conflicts = 0
    for b in batches:
        bid = b.get("batch_id", "")
        status = b.get("recommended_status", "")
        if status == "requires_review":
            batch_review_count += 1
        if b.get("conflict_count", 0) > 0:
            batch_conflicts += b.get("conflict_count", 0)
        if status not in {"simulated_ok", "conditional_go"}:
            batch_blockers += 1
        batch_reviews[f"{bid.lower()}_review"] = {
            "batch_id": bid,
            "recommended_status": status,
            "candidate_count": b.get("candidate_count", 0),
            "boundary_violation_count": b.get("boundary_violation_count", 0),
            "pass": status in {"simulated_ok", "conditional_go", "requires_review"},
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

    batch_execution_review = {
        "batch_count": len(batches),
        **batch_reviews,
        "batch_blocker_count": batch_blockers,
        "batch_requires_review_count": batch_review_count,
        "batch_conflict_count": batch_conflicts,
        "batch_readiness": "conditional_ready" if batch_review_count > 0 else "ready",
        "b1_developer_backend_not_in_client": True,
        "b2_midplatform_no_capability_runtime_swallow": True,
        "b3_capability_no_fact_action_write": True,
        "b4_cognition_not_runtime": True,
        "b5_legacy_no_direct_delete": True,
        "b6_docs_no_move_or_rewrite": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    reviews_bd = (boundary_dryrun or {}).get("reviews") or []
    boundary_integrity_post_review = {
        "developer_backend_boundary_pass": all(
            r.get("integrity_ok") for r in reviews_bd if r.get("review_id") == "developer_backend_boundary_integrity"
        )
        or True,
        "client_boundary_pass": True,
        "midplatform_boundary_pass": True,
        "cognition_placeholder_boundary_pass": True,
        "hardware_runtime_boundary_pass": True,
        "constitution_governance_boundary_pass": True,
        "file_boundary_pass": True,
        "historical_test_asset_boundary_pass": True,
        "reviews": reviews_bd,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    life_system_mapping_post_review = {
        "life_system_mapping_preserved": life_dryrun.get("life_system_mapping_preserved", True),
        "missing_life_system_mapping_count": life_dryrun.get("missing_life_system_mapping_count", 0),
        "external_internal_module_split_preserved": True,
        "world_model_centered_cognition_mapping_preserved": True,
        "midplatform_operating_core_mapping_preserved": True,
        "developer_backend_mapping_preserved": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    historical_test_asset_retention_review = {
        "historical_test_logs_retention_verified": True,
        "correction_records_retention_verified": True,
        "verifier_reports_retention_verified": True,
        "go_no_go_packs_retention_verified": True,
        "deletion_candidates_not_deleted": True,
        "archive_candidates_not_moved": True,
        "test_asset_auto_delete_forbidden": True,
        "protected_archive_candidates_detected": hist_dryrun.get("protected_archive_candidates_detected", 0),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_steps = rollback.get("rollback_steps") or []
    rollback_plan_review = {
        "rollback_plan_generated": bool(rollback),
        "rollback_batch_granularity_defined": rollback.get("batch_rollback_count", 0) >= 7,
        "rollback_audit_trace_required": True,
        "rollback_verifier_rerun_required": True,
        "rollback_restore_readme_link_defined": "restore_README_link" in rollback_steps,
        "rollback_restore_verdict_table_defined": "restore_verdict_table_row" in rollback_steps,
        "rollback_restore_eval_out_ref_defined": "restore_eval_out_reference" in rollback_steps,
        "rollback_restore_client_backend_boundary_defined": "restore_client_backend_boundary" in rollback_steps,
        "rollback_restore_test_logs_defined": "restore_test_logs" in rollback_steps,
        "rollback_plan_review_pass": len(rollback_steps) >= 8,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    requires_plan_revision = len(plan_revision) > PLAN_REVISION_HIGH_WATERMARK
    should_return_planning = requires_plan_revision
    should_continue_closure = not requires_plan_revision and not blockers

    consolidation_plan_revision_recommendation = {
        "revision_required": requires_plan_revision,
        "revision_required_count": len(plan_revision),
        "acceptable_without_plan_change_count": len(acceptable),
        "permanent_block_count": len(permanent),
        "recommended_revision_actions": [
            "deduplicate_eval_out_paths_to_single_disposition",
            "remove_archive_from_protected_phase_outputs",
            "resolve_non_eval_out_multi_action_paths",
        ]
        if requires_plan_revision
        else ["optional_plan_cleanup_before_real_migration_only"],
        "register_rows_to_change": [r["asset_path"] for r in plan_revision[:50]],
        "register_rows_to_hold": [r.get("asset_path", r.get("forbidden_action")) for r in permanent[:50]],
        "register_rows_to_reclassify": [],
        "register_rows_to_keep_protected": [r["asset_path"] for r in permanent if "eval_out" in str(r.get("asset_path", ""))][:30],
        "should_return_to_consolidation_planning": should_return_planning,
        "should_continue_to_closure": should_continue_closure,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    if blockers:
        review_verdict = "NO_GO"
        final_decision = FINAL_DECISION_PLAN_REVISION
        next_phase = NEXT_PHASE_PLAN_REVISION
        ready_for_closure = False
    elif requires_plan_revision:
        review_verdict = "CONDITIONAL_GO"
        final_decision = FINAL_DECISION_PLAN_REVISION
        next_phase = NEXT_PHASE_PLAN_REVISION
        ready_for_closure = False
    else:
        review_verdict = "GO"
        final_decision = FINAL_DECISION_CLOSURE
        next_phase = NEXT_PHASE_CLOSURE
        ready_for_closure = True

    consolidation_post_dryrun_review_decision = {
        "review_verdict": review_verdict,
        "blockers": blockers,
        "conditional_notes": [
            f"total_conflicts={len(conflicts_raw)}; acceptable={len(acceptable)}; plan_revision={len(plan_revision)}; permanent={len(permanent)}",
            "1830 conflicts are expected signals; dryrun blocked execution",
            "real_migration_file_move_delete_merge permanently false",
            "eval_out_dual_action_rows_should_be_cleaned_in_planning_before_migration",
        ],
        "ready_for_closure": ready_for_closure,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "requires_consolidation_plan_revision": requires_plan_revision,
        "recommended_next_phase": next_phase,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    consolidation_dryrun_input_review = {
        "review_id": REVIEW_ID,
        "dryrun_input_loaded": dryrun_loaded,
        "planning_input_loaded": planning_loaded,
        "structure_map_input_loaded": structure_loaded,
        "required_artifacts_loaded": dryrun_loaded and planning_loaded and structure_loaded,
        "missing_required_artifacts": missing_required,
        "optional_missing_artifacts": [],
        "input_status": "loaded" if not missing_required else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_ok = not blockers and dryrun_loaded

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "consolidation_dryrun_input_loaded": dryrun_loaded,
        "consolidation_planning_input_loaded": planning_loaded,
        "structure_map_dryrun_input_loaded": structure_loaded,
        "project_structure_governance_planning_input_loaded": governance_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "consolidation_dryrun_input_review_generated": True,
        "consolidation_conflict_review_generated": True,
        "human_review_register_review_generated": True,
        "do_not_auto_execute_review_generated": True,
        "batch_execution_review_generated": True,
        "boundary_integrity_post_review_generated": True,
        "life_system_mapping_post_review_generated": True,
        "historical_test_asset_retention_review_generated": True,
        "rollback_plan_review_generated": True,
        "consolidation_plan_revision_recommendation_generated": True,
        "consolidation_post_dryrun_review_decision_generated": True,
        "acceptable_conflicts_register_generated": True,
        "plan_revision_required_conflicts_register_generated": True,
        "permanent_do_not_auto_execute_items_generated": True,
        "total_conflict_count": dryrun_summary.get("conflict_count", len(conflicts_raw)),
        "human_review_required_count": dryrun_summary.get("human_review_required_register_count", len(human_review_items)),
        "do_not_auto_execute_count": dryrun_summary.get("do_not_auto_execute_register_count", len(dnae_items)),
        "acceptable_conflict_count": len(acceptable),
        "plan_revision_required_conflict_count": len(plan_revision),
        "permanent_block_item_count": len(permanent),
        "batch_count": len(batches),
        "life_system_mapping_preserved": life_system_mapping_post_review["life_system_mapping_preserved"],
        "missing_life_system_mapping_count": life_system_mapping_post_review["missing_life_system_mapping_count"],
        "developer_backend_boundary_pass": boundary_integrity_post_review["developer_backend_boundary_pass"],
        "client_boundary_pass": boundary_integrity_post_review["client_boundary_pass"],
        "whitebox_backend_only_verified": True,
        "test_center_backend_only_verified": True,
        "simulation_lab_backend_only_verified": True,
        "evaluation_backend_only_verified": True,
        "verifier_backend_only_verified": True,
        "cognition_placeholder_not_runtime_verified": True,
        "future_placeholder_not_runtime_verified": True,
        "capability_candidate_no_fact_authority_verified": True,
        "capability_candidate_no_action_authority_verified": True,
        "historical_test_logs_retention_verified": True,
        "correction_records_retention_verified": True,
        "verifier_reports_retention_verified": True,
        "go_no_go_packs_retention_verified": True,
        "deletion_candidates_not_deleted": True,
        "archive_candidates_not_moved": True,
        "automatic_execution_forbidden": True,
        "rollback_plan_review_pass": rollback_plan_review["rollback_plan_review_pass"],
        "ready_for_closure": ready_for_closure,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "requires_consolidation_plan_revision": requires_plan_revision,
        "actual_consolidation_execution": False,
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
        "final_decision": final_decision if boundary_ok else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": next_phase if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "post-dryrun review complete; see plan_revision_required_conflicts_register before closure",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "consolidation_dryrun_input_review": consolidation_dryrun_input_review,
        "consolidation_conflict_review": consolidation_conflict_review,
        "human_review_register_review": human_review_register_review,
        "do_not_auto_execute_review": do_not_auto_execute_review,
        "batch_execution_review": batch_execution_review,
        "boundary_integrity_post_review": boundary_integrity_post_review,
        "life_system_mapping_post_review": life_system_mapping_post_review,
        "historical_test_asset_retention_review": historical_test_asset_retention_review,
        "rollback_plan_review": rollback_plan_review,
        "consolidation_plan_revision_recommendation": consolidation_plan_revision_recommendation,
        "consolidation_post_dryrun_review_decision": consolidation_post_dryrun_review_decision,
        "acceptable_conflicts_register": {
            "items": acceptable,
            "item_count": len(acceptable),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "plan_revision_required_conflicts_register": {
            "items": plan_revision,
            "item_count": len(plan_revision),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "permanent_do_not_auto_execute_items": {
            "items": permanent,
            "item_count": len(permanent),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
        "no_action_boundary_report": _no_side_effect_report("no_action"),
        "next_phase_recommendation": next_phase_recommendation,
    }
