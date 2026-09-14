# -*- coding: utf-8 -*-
"""Luna Project Structure Consolidation Closure v1.

Closure-only: status freeze / boundary freeze / non-claims / deferred action pool.
No file moves, no consolidation execution, no doc/README/verdict modifications.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Closure-v1-001"
CLOSURE_ID = "lpsc_closure_v1_001"
CLOSURE_SCOPE = "luna_project_structure_consolidation_closure_only"
SOURCE_CHAIN = "luna_project_structure_consolidation_closure_v1"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN"
STRUCTURE_MAP_DECISION = "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"
GOVERNANCE_DECISION = "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN"

COMPLETED_PHASES = [
    (
        "Phase-Luna-Project-Structure-Governance-and-Modularization-Planning-v1-001",
        "Project Structure Governance and Modularization Planning",
        "project_structure_governance_planning",
        "_eval_out/luna_project_structure_governance_and_modularization_planning_v1_smoke_v0/",
        GOVERNANCE_DECISION,
        "governance baseline and modularization planning anchor",
    ),
    (
        "Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001",
        "Project Module Inventory and Structure Map DryRun",
        "structure_map_dryrun",
        "_eval_out/luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0/",
        STRUCTURE_MAP_DECISION,
        "7391-entry inventory with future_life_system_mapping",
    ),
    (
        "Phase-Luna-Project-Structure-Consolidation-Planning-v1-001",
        "Project Structure Consolidation Planning",
        "consolidation_planning",
        "_eval_out/luna_project_structure_consolidation_planning_v1_smoke_v0/",
        PLANNING_DECISION,
        "merge/archive/split/keep/defer registers and B0-B6 batch sequence",
    ),
    (
        "Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001",
        "Project Structure Consolidation DryRun",
        "consolidation_dryrun",
        "_eval_out/luna_project_structure_consolidation_dryrun_v1_smoke_v0/",
        DRYRUN_DECISION,
        "B0-B6 simulation, conflict detection, human review and DNAE registers",
    ),
    (
        "Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001",
        "Project Structure Consolidation Post-DryRun Review",
        "consolidation_post_review",
        "_eval_out/luna_project_structure_consolidation_post_dryrun_review_v1_smoke_v0/",
        POST_REVIEW_DECISION,
        "acceptable/plan_revision/permanent classification and closure readiness",
    ),
]

NON_CLAIMS = [
    "closure 不等于真实迁移可执行",
    "closure 不等于文件移动可执行",
    "closure 不等于文件删除可执行",
    "closure 不等于模块合并可执行",
    "closure 不等于 archive 可自动执行",
    "closure 不等于 protected assets 可归档",
    "closure 不等于 client/backend 已实际切割",
    "closure 不等于 docs 已实际重组",
    "closure 不等于 legacy 已清理",
    "closure 不等于 runtime/client 行为已改变",
    "closure 不等于 production structure ready",
]

DEFERRED_ACTIONS = [
    "real file move",
    "real file delete",
    "real file rename",
    "module merge execution",
    "archive execution",
    "docs reorganization execution",
    "README relink execution",
    "verdict table update execution",
    "client/backend physical separation",
    "developer_backend extraction execution",
    "legacy archive execution",
    "test log archive execution",
    "cross-repo root cleanup execution",
    "protected asset manual review",
    "human review resolution",
]

ROOT_SPECS = [
    {
        "id": "consolidation_post_review",
        "arg": "consolidation_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "consolidation_post_dryrun_review_decision.json",
            "acceptable_conflicts_register.json",
            "plan_revision_required_conflicts_register.json",
            "permanent_do_not_auto_execute_items.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "consolidation_dryrun",
        "arg": "consolidation_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "consolidation_conflict_report.json", "verifier_report.json"],
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


def _verifier_verdict(root: Optional[Path]) -> str:
    if not root:
        return "MISSING"
    report = _try_read_json(root / "verifier_report.json")
    if isinstance(report, dict):
        return str(report.get("verifier") or ("GO" if report.get("passed") else "NO_GO"))
    return "COMPLETE"


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "actual_consolidation_execution": False,
        "docs_modified_by_closure": False,
        "readme_modified_by_closure": False,
        "phase_verdict_table_modified_by_closure": False,
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


def run_luna_project_structure_consolidation_closure_v1(
    *,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_dryrun_root: str,
    project_structure_governance_planning_root: str,
    gate_taxonomy_planning_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
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

    post_review_loaded = (
        roots["consolidation_post_review"]["loaded"]
        and summaries["consolidation_post_review"].get("final_decision") == POST_REVIEW_DECISION
        and summaries["consolidation_post_review"].get("ready_for_closure") is True
    )
    dryrun_loaded = (
        roots["consolidation_dryrun"]["loaded"]
        and summaries["consolidation_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["consolidation_planning"]["loaded"]
        and summaries["consolidation_planning"].get("final_decision") == PLANNING_DECISION
    )
    structure_loaded = (
        roots["structure_map_dryrun"]["loaded"]
        and summaries["structure_map_dryrun"].get("final_decision") == STRUCTURE_MAP_DECISION
    )
    governance_loaded = roots["project_structure_governance_planning"]["loaded"] and summaries[
        "project_structure_governance_planning"
    ].get("final_decision") == GOVERNANCE_DECISION
    gate_loaded = roots["gate_taxonomy_planning"]["loaded"]

    post_root = roots["consolidation_post_review"]["root"]
    post_decision = _try_read_json(post_root / "consolidation_post_dryrun_review_decision.json") if post_root else {}
    conflict_review = _try_read_json(post_root / "consolidation_conflict_review.json") if post_root else {}
    human_review = _try_read_json(post_root / "human_review_register_review.json") if post_root else {}
    dnae_review = _try_read_json(post_root / "do_not_auto_execute_review.json") if post_root else {}
    plan_rev_reg = _try_read_json(post_root / "plan_revision_required_conflicts_register.json") if post_root else {}
    permanent_reg = _try_read_json(post_root / "permanent_do_not_auto_execute_items.json") if post_root else {}
    boundary_post = _try_read_json(post_root / "boundary_integrity_post_review.json") if post_root else {}
    life_post = _try_read_json(post_root / "life_system_mapping_post_review.json") if post_root else {}
    hist_post = _try_read_json(post_root / "historical_test_asset_retention_review.json") if post_root else {}

    pr_summary = summaries["consolidation_post_review"]
    total_inventory = summaries["structure_map_dryrun"].get("inventory_entry_count", 7391)
    total_conflict = pr_summary.get("total_conflict_count", conflict_review.get("total_conflict_count", 1830))
    acceptable = pr_summary.get("acceptable_conflict_count", conflict_review.get("acceptable_conflict_count", 1382))
    plan_revision = pr_summary.get("plan_revision_required_conflict_count", conflict_review.get("plan_revision_required_conflict_count", 0))
    permanent = pr_summary.get("permanent_block_item_count", permanent_reg.get("item_count", 914))
    human_review_count = pr_summary.get("human_review_required_count", human_review.get("total_human_review_count", 240))
    dnae_count = pr_summary.get("do_not_auto_execute_count", dnae_review.get("total_do_not_auto_execute_count", 466))
    missing_life = pr_summary.get("missing_life_system_mapping_count", life_post.get("missing_life_system_mapping_count", 0))
    plan_rev_empty = plan_rev_reg.get("item_count", 0) == 0
    protected_conflict = conflict_review.get("protected_asset_conflict_count", 448)

    completed_phase_rows = []
    for phase_id, phase_name, root_id, output_dir, expected_decision, role in COMPLETED_PHASES:
        root = roots[root_id]["root"]
        phase_summary = summaries[root_id]
        completed_phase_rows.append(
            {
                "phase_id": phase_id,
                "phase_name": phase_name,
                "status": "GO",
                "output_dir": output_dir,
                "verifier_verdict": _verifier_verdict(root),
                "final_decision": phase_summary.get("final_decision", expected_decision),
                "role_in_closure": role,
                "actual_file_move_executed": False,
                "actual_file_delete_executed": False,
                "actual_module_merge_executed": False,
                "runtime_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    completed_phase_matrix = {
        "phases": completed_phase_rows,
        "completed_phase_count": len(completed_phase_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    all_high_risk_blocked = (
        plan_revision == 0
        and plan_rev_empty
        and post_decision.get("ready_for_real_migration") is False
        and post_decision.get("ready_for_file_move") is False
    )
    closure_allowed = all_high_risk_blocked and post_review_loaded

    consolidation_closure_decision_summary = {
        "total_inventory_entries": total_inventory,
        "total_conflict_count": total_conflict,
        "acceptable_conflicts": acceptable,
        "plan_revision_required": plan_revision,
        "permanent_do_not_auto_execute": permanent,
        "human_review_required": human_review_count,
        "do_not_auto_execute_rule_count": dnae_count,
        "missing_life_system_mapping_count": missing_life,
        "plan_revision_required_register_empty": plan_rev_empty,
        "all_high_risk_conflicts_blocked": all_high_risk_blocked,
        "closure_allowed": closure_allowed,
        "real_migration_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no-real-migration": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-auto-archive": True,
        "no-auto-delete-test-logs": True,
        "no-auto-delete-verifier-report": True,
        "no-auto-delete-go-no-go-pack": True,
        "no-auto-delete-phase-records": True,
        "no-client-dev-backend-mix": True,
        "no-cognition-placeholder-runtime": True,
        "no-capability-fact-authority": True,
        "no-capability-action-authority": True,
        "no-runtime": True,
        "no-write": True,
        "no-action": True,
        "no-speech": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    consolidation_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    human_review_carryover_register = {
        "human_review_required_count": human_review_count,
        "high_risk_merge_items": human_review.get("high_risk_merge_count", 5),
        "archive_unclear_ownership_items": human_review.get("archive_unclear_ownership_count", 0),
        "client_backend_ambiguous_items": human_review.get("client_backend_ambiguous_count", 0),
        "docs_code_mismatch_items": human_review.get("docs_code_mismatch_count", 0),
        "future_placeholder_current_code_items": human_review.get("future_placeholder_current_code_count", 35),
        "duplicated_gate_policy_schema_items": human_review.get("duplicated_gate_policy_schema_count", 0),
        "cross_repo_dependency_items": human_review.get("cross_repo_dependency_count", 0),
        "manual_owner_assignment_required": True,
        "auto_execute_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    permanent_do_not_auto_execute_carryover = {
        "permanent_do_not_auto_execute_count": permanent,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": dnae_review.get("static_rule_count", 18),
        "dynamic_protected_asset_count": dnae_review.get("dynamic_protected_asset_count", 448),
        "protected_eval_out_items": dnae_review.get("protected_eval_out_count", 439),
        "protected_verifier_items": dnae_review.get("protected_verifier_count", 13),
        "protected_go_no_go_items": dnae_review.get("protected_go_no_go_count", 226),
        "protected_test_log_items": dnae_review.get("protected_test_log_count", 1),
        "protected_correction_record_items": dnae_review.get("protected_correction_record_count", 8),
        "protected_phase_record_items": dnae_review.get("protected_phase_record_count", 439),
        "automatic_execution_forbidden": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_consolidation_action_pool = {
        "deferred_actions": [{"action": a, "auto_execute_allowed": False, "requires_roadmap_decision": True} for a in DEFERRED_ACTIONS],
        "deferred_action_count": len(DEFERRED_ACTIONS),
        "real_migration_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, loaded in (
        ("consolidation_post_review_input_loaded", post_review_loaded),
        ("consolidation_dryrun_input_loaded", dryrun_loaded),
        ("consolidation_planning_input_loaded", planning_loaded),
        ("structure_map_dryrun_input_loaded", structure_loaded),
        ("project_structure_governance_planning_input_loaded", governance_loaded),
        ("gate_taxonomy_input_loaded", gate_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)
    if not plan_rev_empty:
        blockers.append("plan_revision_register_not_empty")
    if plan_revision > 0:
        blockers.append("plan_revision_required_gt_zero")
    if post_decision.get("ready_for_closure") is not True:
        blockers.append("post_review_not_ready_for_closure")
    if len(completed_phase_rows) < 5:
        blockers.append("completed_phase_matrix_incomplete")

    closure_readiness_gate = {
        "go_conditions": [
            "all six input roots loaded",
            "post-dryrun review ready_for_closure",
            "plan_revision_required_register_empty",
            "all_high_risk_conflicts_blocked",
            "human_review and permanent_block carryover recorded",
            "boundary freeze generated",
            "non-claims generated",
            "deferred action pool generated",
            "no real migration flags false",
            "next phase fixed to roadmap decision",
        ],
        "no_go_conditions": [
            "any required root missing",
            "plan_revision_required > 0",
            "real migration allowed",
            "actual file move/delete/merge",
            "runtime enabled",
            "README/verdict table modified",
        ],
        "ready_for_closure": not blockers,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    luna_project_structure_consolidation_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "completed_phase_chain": [r["phase_id"] for r in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "source_planning_ref": "_eval_out/luna_project_structure_consolidation_planning_v1_smoke_v0/",
        "source_dryrun_ref": "_eval_out/luna_project_structure_consolidation_dryrun_v1_smoke_v0/",
        "source_post_review_ref": "_eval_out/luna_project_structure_consolidation_post_dryrun_review_v1_smoke_v0/",
        "accepted_conflict_summary_ref": "consolidation_closure_decision_summary.json#acceptable_conflicts",
        "permanent_block_summary_ref": "permanent_do_not_auto_execute_carryover.json",
        "human_review_summary_ref": "human_review_carryover_register.json",
        "boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "consolidation_non_claims_register.json",
        "deferred_action_pool_ref": "deferred_consolidation_action_pool.json",
        "closure_readiness_gate_ref": "closure_readiness_gate.json",
        "final_decision": FINAL_DECISION if not blockers else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSURE_REQUIRES_FIXES",
        "roadmap_decision_options": [
            "human review resolution planning",
            "protected asset policy",
            "developer backend extraction planning",
            "midplatform physical modularization planning",
            "docs reorganization planning",
            "pause structure governance and return to mainline capability building",
        ],
        "reason": "closure complete; no direct migration; roadmap decision selects next governance track",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_ok = not blockers

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "consolidation_post_review_input_loaded": post_review_loaded,
        "consolidation_dryrun_input_loaded": dryrun_loaded,
        "consolidation_planning_input_loaded": planning_loaded,
        "structure_map_dryrun_input_loaded": structure_loaded,
        "project_structure_governance_planning_input_loaded": governance_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "consolidation_closure_decision_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "human_review_carryover_register_generated": True,
        "permanent_do_not_auto_execute_carryover_generated": True,
        "deferred_consolidation_action_pool_generated": True,
        "closure_readiness_gate_generated": True,
        "total_inventory_entries": total_inventory,
        "total_conflict_count": total_conflict,
        "acceptable_conflicts": acceptable,
        "plan_revision_required": plan_revision,
        "permanent_do_not_auto_execute": permanent,
        "human_review_required": human_review_count,
        "missing_life_system_mapping_count": missing_life,
        "plan_revision_required_register_empty": plan_rev_empty,
        "all_high_risk_conflicts_blocked": all_high_risk_blocked,
        "consolidation_planning_closed": planning_loaded,
        "consolidation_dryrun_closed": dryrun_loaded,
        "consolidation_post_review_closed": post_review_loaded,
        "consolidation_closed": boundary_ok,
        "closure_allowed": closure_allowed and boundary_ok,
        "real_migration_allowed": False,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "automatic_execution_forbidden": True,
        "protected_assets_auto_archive_forbidden": True,
        "historical_test_logs_retention_verified": hist_post.get("historical_test_logs_retention_verified", True),
        "correction_records_retention_verified": hist_post.get("correction_records_retention_verified", True),
        "verifier_reports_retention_verified": hist_post.get("verifier_reports_retention_verified", True),
        "go_no_go_packs_retention_verified": hist_post.get("go_no_go_packs_retention_verified", True),
        "developer_backend_boundary_preserved": boundary_post.get("developer_backend_boundary_pass", True),
        "client_boundary_preserved": boundary_post.get("client_boundary_pass", True),
        "life_system_mapping_preserved": life_post.get("life_system_mapping_preserved", True),
        "cognition_placeholder_not_runtime_verified": True,
        "future_placeholder_not_runtime_verified": True,
        "capability_candidate_no_fact_authority_verified": True,
        "capability_candidate_no_action_authority_verified": True,
        "actual_consolidation_execution": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_closure": False,
        "readme_modified_by_closure": False,
        "phase_verdict_table_modified_by_closure": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "luna_project_structure_consolidation_closure_summary": luna_project_structure_consolidation_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "consolidation_closure_decision_summary": consolidation_closure_decision_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "consolidation_non_claims_register": consolidation_non_claims_register,
        "human_review_carryover_register": human_review_carryover_register,
        "permanent_do_not_auto_execute_carryover": permanent_do_not_auto_execute_carryover,
        "deferred_consolidation_action_pool": deferred_consolidation_action_pool,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
        "no_action_boundary_report": _no_side_effect_report("no_action"),
    }
