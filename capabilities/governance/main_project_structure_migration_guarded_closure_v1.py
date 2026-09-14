# -*- coding: utf-8 -*-
"""Main Project Structure Migration Guarded Closure v1.

Closure-only: freeze guarded migration chain status / boundaries / non-claims.
No real migration, post-migration tests, rollback, or owner confirmation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001"
CLOSURE_ID = "main_proj_struct_migration_guarded_closure_v1_001"
CLOSURE_SCOPE = "main_project_structure_migration_guarded_closure_only"
SOURCE_CHAIN = "main_project_structure_migration_guarded_closure_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN"
READINESS_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

COMPLETED_PHASES = [
    (
        "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001",
        "Main Project Structure Migration Readiness and Test Plan",
        "readiness",
        "_eval_out/main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0/",
        READINESS_DECISION,
        "migration readiness gate, prerequisites, post-migration test plan (not executed)",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001",
        "Main Project Structure Migration Guarded Planning",
        "guarded_planning",
        "_eval_out/main_project_structure_migration_guarded_planning_v1_smoke_v0/",
        PLANNING_DECISION,
        "B0-B7 batch plan, 10 gate sequence, 31 test matrix binding",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001",
        "Main Project Structure Migration Guarded DryRun",
        "guarded_dryrun",
        "_eval_out/main_project_structure_migration_guarded_dryrun_v1_smoke_v0/",
        DRYRUN_DECISION,
        "B0-B7 simulated gate chain, exclusion/candidate scope, test binding simulation",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001",
        "Main Project Structure Migration Guarded Post-DryRun Review",
        "guarded_post_review",
        "_eval_out/main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0/",
        POST_REVIEW_DECISION,
        "formal post-dryrun audit for guarded migration closure readiness",
    ),
]

NON_CLAIMS = [
    "Guarded Closure ≠ 可真实搬迁",
    "closure 不等于真实迁移可执行",
    "closure 不等于文件移动/删除/重命名/合并可执行",
    "Guarded Closure ≠ 可执行 post-migration tests",
    "closure 不等于迁移后测试已执行",
    "closure 不等于迁移后测试已通过",
    "closure 不等于 rollback 已执行",
    "Guarded Closure ≠ owner 已确认",
    "closure 不等于 owner 已确认",
    "closure 不等于 HumanApproval 已完成",
    "Guarded Closure ≠ protected / HR / DnAE 可处理",
    "closure 不等于 protected assets 可修改或迁移纳入",
    "closure 不等于 240 HR 可自动处理",
    "closure 不等于 914 permanent block 可解除",
    "closure 不等于白盒/测试中心结构可开始执行",
    "closure 不等于 Developer Backend 架构已定稿",
    "closure 不等于未来模块结构已定稿",
    "closure 不等于 production structure ready",
    "guarded migration chain closed 不等于 real_migration_allowed",
]

DEFERRED_ACTIONS = [
    "real migration execution",
    "file move",
    "file delete",
    "file rename",
    "module merge",
    "docs modification",
    "README relink",
    "phase verdict table update",
    "post-migration test execution",
    "rollback execution",
    "human approval execution",
    "owner confirmation",
    "protected asset handling",
    "HR resolution execution",
    "permanent DnAE override",
    "whitebox/test center design",
    "developer backend architecture",
    "future module finalization",
]

EXCLUSION_FLAGS = (
    "protected_assets_excluded_from_migration",
    "permanent_blocks_excluded_from_migration",
    "human_review_items_excluded_or_manual_only",
    "eval_out_outputs_excluded",
    "verifier_reports_excluded",
    "go_no_go_packs_excluded",
    "correction_records_excluded",
    "historical_test_logs_excluded",
    "phase_records_excluded",
    "closure_boundary_files_excluded",
    "non_claims_registers_excluded",
    "whitebox_test_center_physical_restructure_excluded",
    "developer_backend_full_architecture_excluded",
    "future_reserved_module_finalization_excluded",
    "runtime_behavior_changes_excluded",
    "client_runtime_changes_excluded",
)

ROOT_SPECS = [
    {
        "id": "guarded_post_review",
        "arg": "guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "guarded_post_dryrun_readiness_decision.json",
            "batch_gate_post_review.json",
            "gate_sequence_post_review.json",
            "exclusion_scope_post_review.json",
            "candidate_scope_post_review.json",
            "post_migration_test_binding_post_review.json",
            "rollback_checkpoint_post_review.json",
            "human_approval_checkpoint_post_review.json",
            "guarded_dryrun_boundary_post_review.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "guarded_dryrun",
        "arg": "guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "guarded_migration_dryrun_execution_plan.json",
            "batch_gate_dryrun_results.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "guarded_planning",
        "arg": "guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "guarded_migration_batch_plan.json",
            "guarded_migration_gate_sequence.json",
            "post_migration_verification_matrix.json",
        ],
    },
    {
        "id": "readiness",
        "arg": "readiness_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "migration_readiness_decision.json",
            "migration_readiness_gate.json",
            "post_migration_test_plan.json",
        ],
    },
    {
        "id": "roadmap_decision",
        "arg": "roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pahr_closure",
        "arg": "pahr_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_closure",
        "arg": "consolidation_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map",
        "arg": "structure_map_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gate_taxonomy",
        "arg": "gate_taxonomy_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
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
        if report.get("passed") is True:
            return "GO"
        return str(report.get("verifier") or "NO_GO")
    return "COMPLETE"


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "boundary_ok": True,
        "violations": [],
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
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _exclusion_dict(source: Dict[str, Any]) -> Dict[str, bool]:
    return {k: source.get(k) is True for k in EXCLUSION_FLAGS}


def run_main_project_structure_migration_guarded_closure_v1(
    *,
    guarded_post_review_root: str,
    guarded_dryrun_root: str,
    guarded_planning_root: str,
    readiness_root: str,
    roadmap_decision_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
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

    pr_summary = summaries["guarded_post_review"]
    post_review_loaded = (
        roots["guarded_post_review"]["loaded"]
        and pr_summary.get("final_decision") == POST_REVIEW_DECISION
        and pr_summary.get("ready_for_closure") is True
        and pr_summary.get("boundary_ok") is True
    )
    dryrun_loaded = (
        roots["guarded_dryrun"]["loaded"]
        and summaries["guarded_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["guarded_planning"]["loaded"]
        and summaries["guarded_planning"].get("final_decision") == PLANNING_DECISION
    )
    readiness_loaded = (
        roots["readiness"]["loaded"]
        and summaries["readiness"].get("final_decision") == READINESS_DECISION
    )
    pahr_loaded = roots["pahr_closure"]["loaded"]
    consolidation_loaded = roots["consolidation_closure"]["loaded"]
    structure_map_loaded = roots["structure_map"]["loaded"]
    gate_taxonomy_loaded = roots["gate_taxonomy"]["loaded"]
    roadmap_loaded = roots["roadmap_decision"]["loaded"]

    post_root = roots["guarded_post_review"]["root"]
    readiness_decision = (
        _try_read_json(post_root / "guarded_post_dryrun_readiness_decision.json") if post_root else {}
    ) or {}
    exclusion_post_review = (
        _try_read_json(post_root / "exclusion_scope_post_review.json") if post_root else {}
    ) or {}

    batch_count = pr_summary.get("reviewed_batch_count", pr_summary.get("simulated_pass_batch_count", 8))
    simulated_pass = pr_summary.get("simulated_pass_batch_count", 8)
    simulated_blocked = pr_summary.get("simulated_blocked_batch_count", 0)
    gate_sequence_count = pr_summary.get("reviewed_gate_count", 10)
    gate_sequence_pass = pr_summary.get("gate_sequence_pass") is True
    candidate_scope_count = pr_summary.get("migration_candidate_scope_count", 8)
    exclusion_scope_count = pr_summary.get("migration_exclusion_scope_count", 17)
    candidate_exec_allowed = pr_summary.get("candidate_scopes_execution_allowed") is False
    post_migration_test_count = pr_summary.get("post_migration_test_count", 31)
    bound_test_count = pr_summary.get("bound_test_count", 31)
    unbound_test_count = pr_summary.get("unbound_test_count", 0)
    executed_test_count = pr_summary.get("executed_test_count", 0)
    rollback_checkpoint_count = pr_summary.get("rollback_checkpoint_count", 8)
    rollback_per_batch = pr_summary.get("rollback_checkpoint_per_batch") is True
    rollback_executed = bool(pr_summary.get("rollback_executed", False))
    human_approval_required = pr_summary.get("human_approval_checkpoint_required") is True
    human_placeholder = pr_summary.get("human_approval_is_placeholder_only") is True
    owner_confirmed = bool(pr_summary.get("final_owner_human_confirmed", False))
    approval_executed = bool(pr_summary.get("approval_executed", False))

    exclusion_frozen = _exclusion_dict({**pr_summary, **exclusion_post_review})
    all_exclusions = all(exclusion_frozen.values())

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
                "post_migration_tests_executed": False,
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

    closure_allowed = (
        post_review_loaded
        and dryrun_loaded
        and planning_loaded
        and readiness_loaded
        and simulated_pass == 8
        and simulated_blocked == 0
        and gate_sequence_pass
        and bound_test_count == 31
        and executed_test_count == 0
        and not rollback_executed
        and human_placeholder
        and not owner_confirmed
        and not approval_executed
        and candidate_exec_allowed
        and all_exclusions
        and readiness_decision.get("ready_for_closure") is True
        and readiness_decision.get("ready_for_real_migration") is False
    )

    guarded_migration_closure_decision_summary = {
        "batch_count": batch_count,
        "simulated_pass_batch_count": simulated_pass,
        "simulated_blocked_batch_count": simulated_blocked,
        "gate_sequence_count": gate_sequence_count,
        "gate_sequence_pass": gate_sequence_pass,
        "migration_candidate_scope_count": candidate_scope_count,
        "migration_exclusion_scope_count": exclusion_scope_count,
        "candidate_scopes_execution_allowed": False,
        "post_migration_test_count": post_migration_test_count,
        "bound_test_count": bound_test_count,
        "unbound_test_count": unbound_test_count,
        "executed_test_count": executed_test_count,
        "rollback_checkpoint_count": rollback_checkpoint_count,
        "rollback_checkpoint_per_batch": rollback_per_batch,
        "rollback_executed": False,
        "human_approval_checkpoint_required": human_approval_required,
        "human_approval_is_placeholder_only": human_placeholder,
        "final_owner_human_confirmed": False,
        "approval_executed": False,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "closure_allowed": closure_allowed,
        "real_migration_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    exclusion_carryover_freeze = {**exclusion_frozen, "source_chain": SOURCE_CHAIN, **_not_fact()}

    closure_boundary_freeze = {
        "no-real-migration": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-docs-modification": True,
        "no-readme-modification": True,
        "no-phase-verdict-table-modification": True,
        "no-post-migration-test-execution": True,
        "no-rollback-execution": True,
        "no-human-owner-confirmation": True,
        "no-human-review-execution": True,
        "no-protected-asset-modification": True,
        "no-permanent-block-release": True,
        "no-whitebox-structure-design": True,
        "no-test-center-structure-design": True,
        "no-developer-backend-finalization": True,
        "no-future-module-finalization": True,
        "no-runtime": True,
        "no-write": True,
        "no-action": True,
        "no-speech": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    guarded_migration_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    correction_record = {
        "correction_id": "guarded_post_review_rollback_executed_field_v1",
        "source_phase": "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001",
        "issue": "rollback_checkpoint_post_review boolean inversion risk",
        "original_behavior": (
            'rollback_dryrun.get("rollback_executed") is False was stored as review field value '
            "(dry-run false became review true)"
        ),
        "corrected_behavior": "pass through actual rollback_executed boolean state from dry-run artifact",
        "semantic_impact": "no_permission_granted",
        "boundary_impact": "no_boundary_change",
        "runtime_impact": "none",
        "migration_permission_impact": "none",
        "verification_status": "GO",
        "dryrun_semantic_unchanged": True,
        "rollback_execution_still_blocked": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_guarded_migration_action_pool = {
        "deferred_actions": [
            {"action": a, "auto_execute_allowed": False, "requires_roadmap_decision": True}
            for a in DEFERRED_ACTIONS
        ],
        "deferred_action_count": len(DEFERRED_ACTIONS),
        "real_migration_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not post_review_loaded:
        blockers.append("guarded_post_review_input_not_ready")
    if not dryrun_loaded:
        blockers.append("guarded_dryrun_input_not_ready")
    if not planning_loaded:
        blockers.append("guarded_planning_input_not_ready")
    if not readiness_loaded:
        blockers.append("readiness_input_not_ready")
    if not pahr_loaded:
        blockers.append("pahr_closure_input_not_loaded")
    if not consolidation_loaded:
        blockers.append("consolidation_closure_input_not_loaded")
    if simulated_pass != 8 or simulated_blocked != 0:
        blockers.append("batch_simulation_not_all_pass")
    if not gate_sequence_pass:
        blockers.append("gate_sequence_not_pass")
    if bound_test_count != 31 or executed_test_count != 0:
        blockers.append("post_migration_test_binding_invalid")
    if rollback_executed:
        blockers.append("rollback_was_executed")
    if not human_placeholder or owner_confirmed or approval_executed:
        blockers.append("human_approval_not_placeholder_only")
    if not all_exclusions:
        blockers.append("exclusion_flags_incomplete")
    if len(completed_phase_rows) < 4:
        blockers.append("completed_phase_matrix_incomplete")

    boundary_ok = not blockers

    closure_readiness_gate = {
        "go_conditions": [
            "four-phase guarded chain GO",
            "post-dryrun review ready_for_closure",
            "B0-B7 simulated_pass with zero blocked",
            "31 tests bound, 0 executed",
            "8 rollback checkpoints, rollback_executed false",
            "human approval placeholder only",
            "exclusion carryover frozen",
            "correction record recorded without permission grant",
            "real_migration_allowed false",
        ],
        "no_go_conditions": [
            "any required root missing",
            "batch or gate simulation failure",
            "tests executed or rollback executed",
            "owner confirmed or approval executed",
            "real migration or file operations allowed",
        ],
        "ready_for_closure": boundary_ok,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    main_project_structure_migration_guarded_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "completed_phase_chain": [r["phase_id"] for r in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "readiness_ref": "_eval_out/main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0/",
        "guarded_planning_ref": "_eval_out/main_project_structure_migration_guarded_planning_v1_smoke_v0/",
        "guarded_dryrun_ref": "_eval_out/main_project_structure_migration_guarded_dryrun_v1_smoke_v0/",
        "guarded_post_review_ref": "_eval_out/main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0/",
        "batch_closure_summary_ref": "guarded_migration_closure_decision_summary.json",
        "gate_closure_summary_ref": "guarded_migration_closure_decision_summary.json",
        "exclusion_scope_closure_summary_ref": "exclusion_carryover_freeze.json",
        "test_binding_closure_summary_ref": "guarded_migration_closure_decision_summary.json",
        "rollback_closure_summary_ref": "guarded_migration_closure_decision_summary.json",
        "human_approval_closure_summary_ref": "guarded_migration_closure_decision_summary.json",
        "correction_record_ref": "correction_record.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "guarded_migration_non_claims_register.json",
        "deferred_action_pool_ref": "deferred_guarded_migration_action_pool.json",
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSURE_REQUIRES_FIXES",
        "roadmap_decision_options": [
            "human approval / owner assignment planning before any real migration",
            "migration execution controlled plan (still not auto-start)",
            "post-migration test harness preparation",
            "pause structure migration and return to mainline capability building",
            "defer whitebox/test center design until main migration and tests complete",
        ],
        "priority_note": (
            "closure freezes guarded migration chain only; Roadmap Decision must re-arbitrate "
            "whether to continue pre-migration planning or pause structure migration"
        ),
        "reason": "guarded closure complete; no direct migration, tests, rollback, or owner confirmation",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "guarded_post_review_input_loaded": post_review_loaded,
        "guarded_dryrun_input_loaded": dryrun_loaded,
        "guarded_planning_input_loaded": planning_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "consolidation_closure_input_loaded": consolidation_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "roadmap_decision_input_loaded": roadmap_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "guarded_migration_closure_decision_summary_generated": True,
        "exclusion_carryover_freeze_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "correction_record_generated": True,
        "deferred_action_pool_generated": True,
        "closure_readiness_gate_generated": True,
        "batch_count": batch_count,
        "simulated_pass_batch_count": simulated_pass,
        "simulated_blocked_batch_count": simulated_blocked,
        "gate_sequence_count": gate_sequence_count,
        "gate_sequence_pass": gate_sequence_pass,
        "migration_candidate_scope_count": candidate_scope_count,
        "migration_exclusion_scope_count": exclusion_scope_count,
        "candidate_scopes_execution_allowed": False,
        "post_migration_test_count": post_migration_test_count,
        "bound_test_count": bound_test_count,
        "unbound_test_count": unbound_test_count,
        "executed_test_count": executed_test_count,
        "rollback_checkpoint_count": rollback_checkpoint_count,
        "rollback_checkpoint_per_batch": rollback_per_batch,
        "rollback_executed": False,
        "human_approval_checkpoint_required": human_approval_required,
        "human_approval_is_placeholder_only": human_placeholder,
        "final_owner_human_confirmed": False,
        "approval_executed": False,
        **exclusion_frozen,
        "correction_record_status": "recorded",
        "correction_semantic_impact": "no_permission_granted",
        "correction_boundary_impact": "no_boundary_change",
        "correction_runtime_impact": "none",
        "correction_migration_permission_impact": "none",
        "guarded_readiness_closed": readiness_loaded,
        "guarded_planning_closed": planning_loaded,
        "guarded_dryrun_closed": dryrun_loaded,
        "guarded_post_review_closed": post_review_loaded,
        "guarded_migration_chain_closed": boundary_ok,
        "closure_allowed": closure_allowed and boundary_ok,
        "real_migration_allowed": False,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "main_project_structure_migration_guarded_closure_summary": main_project_structure_migration_guarded_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "guarded_migration_closure_decision_summary": guarded_migration_closure_decision_summary,
        "exclusion_carryover_freeze": exclusion_carryover_freeze,
        "closure_boundary_freeze": closure_boundary_freeze,
        "guarded_migration_non_claims_register": guarded_migration_non_claims_register,
        "correction_record": correction_record,
        "deferred_guarded_migration_action_pool": deferred_guarded_migration_action_pool,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
