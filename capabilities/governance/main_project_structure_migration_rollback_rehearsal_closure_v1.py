# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal Closure v1.

Closure-only: freeze rollback rehearsal dry-run governance chain (Planning→DryRun→Post-Review).
No rollback rehearsal execution, sandbox/branch creation, real migration, or batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001"
CLOSURE_ID = "main_proj_struct_migration_rollback_rehearsal_closure_v1_001"
CLOSURE_SCOPE = "main_project_structure_migration_rollback_rehearsal_closure_only"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_closure_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN"
ROADMAP_FINAL = (
    "POST_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_DRYRUN_PLANNING"
)
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

COMPLETED_PHASES = [
    (
        "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001",
        "Main Project Structure Migration Rollback Rehearsal DryRun Planning",
        "rollback_rehearsal_dryrun_planning",
        "_eval_out/main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0/",
        PLANNING_DECISION,
        "define sandbox/B0-B7 restore paths, verifier rerun, evidence template, success claim policy",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001",
        "Main Project Structure Migration Rollback Rehearsal DryRun",
        "rollback_rehearsal_dryrun",
        "_eval_out/main_project_structure_migration_rollback_rehearsal_dryrun_v1_smoke_v0/",
        DRYRUN_DECISION,
        "simulate sandbox/scope/restore/docs/verdict/eval_out/linkage/verifier/evidence chain",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001",
        "Main Project Structure Migration Rollback Rehearsal Post-DryRun Review",
        "rollback_rehearsal_post_review",
        "_eval_out/main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/",
        POST_REVIEW_DECISION,
        "formal post-dryrun audit for rollback rehearsal closure readiness",
    ),
]

NON_CLAIMS = [
    "closure 不等于 rollback rehearsal 可执行",
    "closure 不等于 rollback rehearsal 已执行",
    "closure 不等于 rollback 已执行",
    "closure 不等于 sandbox 已创建",
    "closure 不等于 branch 已创建",
    "closure 不等于 restore path map 已生成",
    "closure 不等于 docs link restore 已执行",
    "closure 不等于 verdict table restore 已执行",
    "closure 不等于 eval_out reference restore 已执行",
    "closure 不等于 linkage restore 已执行",
    "closure 不等于 verifier rerun 已执行",
    "closure 不等于 rollback evidence 已生成",
    "closure 不等于 rollback success 可声明",
    "closure 不等于真实迁移可执行",
    "closure 不等于 batch arming 可执行",
    "closure 不等于文件移动/删除/重命名/合并可执行",
    "closure 不等于迁移后测试可执行",
    "closure 不等于 verifier suite 可执行",
    "closure 不等于 protected / HR / DnAE 可处理",
    "closure 不等于白盒/测试中心结构可开始执行",
    "closure 不等于 Developer Backend 架构已定稿",
    "closure 不等于未来模块结构已定稿",
    "closure 不等于 production migration ready",
    "rollback_rehearsal_chain_closed 不等于 real_migration_execution_allowed",
]

DEFERRED_ACTIONS = [
    "real migration execution",
    "batch arming execution",
    "rollback rehearsal execution",
    "rollback execution",
    "sandbox creation",
    "branch creation",
    "restore path map generation",
    "docs link restore execution",
    "verdict table restore execution",
    "eval_out reference restore execution",
    "linkage restore execution",
    "verifier rerun execution",
    "rollback evidence generation",
    "rollback success claim",
    "post-migration test execution",
    "verifier suite execution",
    "owner approval execution",
    "operator acknowledgement execution",
    "authorization package generation",
    "human review execution",
    "protected asset handling",
    "HR resolution execution",
    "permanent DnAE override",
    "file move",
    "file delete",
    "file rename",
    "module merge",
    "docs modification",
    "README relink",
    "phase verdict table update",
    "real evidence pack generation",
    "whitebox/test center design",
    "developer backend architecture",
    "future module finalization",
]

POST_REVIEW_ARTIFACTS = [
    "summary.json",
    "rollback_rehearsal_dryrun_input_review.json",
    "rehearsal_sandbox_post_review.json",
    "rollback_rehearsal_scope_post_review.json",
    "rollback_restore_path_map_post_review.json",
    "docs_link_restore_post_review.json",
    "verdict_table_restore_post_review.json",
    "eval_out_reference_restore_post_review.json",
    "capability_runner_verifier_doc_linkage_restore_post_review.json",
    "rollback_verifier_rerun_post_review.json",
    "rollback_rehearsal_evidence_post_review.json",
    "rollback_success_claim_post_review.json",
    "rollback_rehearsal_boundary_post_review.json",
    "rollback_rehearsal_post_dryrun_readiness_decision.json",
    "verifier_report.json",
]

DRYRUN_ARTIFACTS = [
    "summary.json",
    "rollback_rehearsal_dryrun_execution_plan.json",
    "rehearsal_sandbox_dryrun_result.json",
    "rollback_rehearsal_scope_dryrun_result.json",
    "rollback_restore_path_map_dryrun_result.json",
    "docs_link_restore_dryrun_result.json",
    "verdict_table_restore_dryrun_result.json",
    "eval_out_reference_restore_dryrun_result.json",
    "capability_runner_verifier_doc_linkage_restore_dryrun_result.json",
    "rollback_verifier_rerun_dryrun_result.json",
    "rollback_rehearsal_evidence_dryrun_result.json",
    "rollback_success_claim_dryrun_result.json",
    "rollback_rehearsal_dryrun_boundary_review.json",
    "rollback_rehearsal_dryrun_readiness_decision.json",
    "verifier_report.json",
]

PLANNING_ARTIFACTS = [
    "summary.json",
    "rollback_rehearsal_dryrun_planning_policy.json",
    "rehearsal_sandbox_policy.json",
    "rollback_rehearsal_dryrun_scope.json",
    "rollback_restore_path_map_plan.json",
    "rollback_success_claim_policy.json",
    "verifier_report.json",
]

ROOT_SPECS = [
    {
        "id": "rollback_rehearsal_post_review",
        "arg": "rollback_rehearsal_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": POST_REVIEW_ARTIFACTS,
    },
    {
        "id": "rollback_rehearsal_dryrun",
        "arg": "rollback_rehearsal_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
    {
        "id": "rollback_rehearsal_dryrun_planning",
        "arg": "rollback_rehearsal_dryrun_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "post_pre_auth_roadmap",
        "arg": "post_pre_authorization_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gap_hard_block_closure_summary.json"],
    },
    {
        "id": "pre_authorization_post_review",
        "arg": "pre_authorization_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pre_authorization_dryrun",
        "arg": "pre_authorization_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pre_authorization_planning",
        "arg": "pre_authorization_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "execution_control_closure",
        "arg": "execution_control_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "readiness",
        "arg": "readiness_root",
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


def _bool_val(val: Any, default: bool = False) -> bool:
    if val is None:
        return default
    return bool(val)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root and artifacts:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
        loaded = loaded and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary_payload or {},
        "artifacts": art,
        "missing_artifacts": missing,
    }


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
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": False,
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


def _phase_matrix_flags(post_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sandbox_created_now": _bool_val(post_summary.get("sandbox_created_now"), False),
        "branch_created_now": _bool_val(post_summary.get("branch_created_now"), False),
        "restore_path_map_generated_now": _bool_val(post_summary.get("restore_path_map_generated_now"), False),
        "docs_link_restore_executed_now": _bool_val(post_summary.get("docs_link_restore_executed_now"), False),
        "verdict_table_restore_executed_now": _bool_val(post_summary.get("verdict_table_restore_executed_now"), False),
        "eval_out_reference_restore_executed_now": _bool_val(
            post_summary.get("eval_out_reference_restore_executed_now"), False
        ),
        "linkage_restore_executed_now": _bool_val(post_summary.get("linkage_restore_executed_now"), False),
        "verifier_rerun_executed_now": _bool_val(post_summary.get("verifier_rerun_executed_now"), False),
        "evidence_generated_now": _bool_val(post_summary.get("evidence_generated_now"), False),
        "rollback_success_claim_allowed": _bool_val(post_summary.get("rollback_success_claim_allowed"), False),
        "rollback_rehearsal_execution_allowed": _bool_val(
            post_summary.get("rollback_rehearsal_execution_allowed"), False
        ),
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "runtime_enabled": False,
    }


def run_main_project_structure_migration_rollback_rehearsal_closure_v1(
    *,
    rollback_rehearsal_post_review_root: str,
    rollback_rehearsal_dryrun_root: str,
    rollback_rehearsal_dryrun_planning_root: str,
    post_pre_authorization_roadmap_root: str,
    pre_authorization_closure_root: str,
    pre_authorization_post_review_root: str,
    pre_authorization_dryrun_root: str,
    pre_authorization_planning_root: str,
    controlled_execution_closure_root: str,
    controlled_execution_planning_root: str,
    execution_control_closure_root: str,
    guarded_closure_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}
    post_summary = summaries["rollback_rehearsal_post_review"]
    dryrun_summary = summaries["rollback_rehearsal_dryrun"]

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "missing_artifacts": meta.get("missing_artifacts") or [],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    post_review_loaded = (
        roots["rollback_rehearsal_post_review"]["loaded"]
        and post_summary.get("final_decision") == POST_REVIEW_DECISION
        and post_summary.get("ready_for_closure") is True
    )
    dryrun_loaded = (
        roots["rollback_rehearsal_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["rollback_rehearsal_dryrun_planning"]["loaded"]
        and summaries["rollback_rehearsal_dryrun_planning"].get("final_decision") == PLANNING_DECISION
    )
    roadmap_loaded = (
        roots["post_pre_auth_roadmap"]["loaded"]
        and summaries["post_pre_auth_roadmap"].get("final_decision") == ROADMAP_FINAL
    )
    pre_auth_closure_loaded = (
        roots["pre_authorization_closure"]["loaded"]
        and summaries["pre_authorization_closure"].get("final_decision") == PRE_AUTH_CLOSURE
    )
    pre_auth_post_review_loaded = roots["pre_authorization_post_review"]["loaded"]
    pre_auth_dryrun_loaded = roots["pre_authorization_dryrun"]["loaded"]
    ce_closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and summaries["controlled_execution_closure"].get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
    )
    ce_planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == CE_PLANNING_FINAL
    )
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    structure_loaded = roots["structure_map"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    pa_closure_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(pa_closure_root / "gap_hard_block_closure_summary.json") if pa_closure_root else {}) or {}

    matrix_flags = _phase_matrix_flags(post_summary)
    rollback_success_claim_allowed = _bool_val(post_summary.get("rollback_success_claim_allowed"), False)

    completed_phase_rows: List[Dict[str, Any]] = []
    for phase_id, phase_name, root_key, output_dir, final_decision, role in COMPLETED_PHASES:
        sm = summaries.get(root_key, {})
        verifier_report = roots.get(root_key, {}).get("artifacts", {}).get("verifier_report.json") or {}
        completed_phase_rows.append(
            {
                "phase_id": phase_id,
                "phase_name": phase_name,
                "status": "GO",
                "output_dir": output_dir,
                "verifier_verdict": verifier_report.get("verifier", "GO"),
                "final_decision": sm.get("final_decision", final_decision),
                "role_in_closure": role,
                **matrix_flags,
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

    rollback_rehearsal_closure_decision_summary = {
        "scope_batch_count": post_summary.get("scope_batch_count", 8),
        "mandatory_rollback_path_count": post_summary.get("mandatory_rollback_path_count", 6),
        "verifier_suite_count": post_summary.get("verifier_suite_count", 12),
        "required_verifier_count": post_summary.get("required_verifier_count", 4),
        "rollback_specific_verifier_count": post_summary.get("rollback_specific_verifier_count", 4),
        "sandbox_simulated": post_summary.get("sandbox_simulated") is True,
        "sandbox_created_now": _bool_val(post_summary.get("sandbox_created_now"), False),
        "branch_created_now": _bool_val(post_summary.get("branch_created_now"), False),
        "b0_baseline_restore_check_simulated": post_summary.get("b0_baseline_restore_check_simulated") is True,
        "b1_docs_relink_rollback_path_simulated": post_summary.get("b1_docs_relink_rollback_path_simulated") is True,
        "b2_capability_grouping_rollback_path_simulated": post_summary.get(
            "b2_capability_grouping_rollback_path_simulated"
        )
        is True,
        "b3_governance_grouping_rollback_path_simulated": post_summary.get(
            "b3_governance_grouping_rollback_path_simulated"
        )
        is True,
        "b4_midplatform_core_rollback_path_simulated": post_summary.get("b4_midplatform_core_rollback_path_simulated")
        is True,
        "b5_dev_artifact_reference_rollback_path_simulated": post_summary.get(
            "b5_dev_artifact_reference_rollback_path_simulated"
        )
        is True,
        "b6_future_marker_rollback_path_simulated": post_summary.get("b6_future_marker_rollback_path_simulated")
        is True,
        "b7_verification_gate_restore_check_simulated": post_summary.get(
            "b7_verification_gate_restore_check_simulated"
        )
        is True,
        "rollback_reverse_mapping_simulated": post_summary.get("rollback_reverse_mapping_simulated") is True,
        "protected_asset_restore_rule_simulated": post_summary.get("protected_asset_restore_rule_simulated") is True,
        "HR_DnAE_restore_rule_simulated": post_summary.get("HR_DnAE_restore_rule_simulated") is True,
        "path_conflict_detection_simulated": post_summary.get("path_conflict_detection_simulated") is True,
        "restore_path_map_generated_now": False,
        "docs_link_restore_executed_now": False,
        "verdict_table_restore_executed_now": False,
        "eval_out_reference_restore_executed_now": False,
        "linkage_restore_executed_now": False,
        "verifier_rerun_simulated": post_summary.get("verifier_rerun_simulated") is True,
        "verifier_rerun_executed_now": False,
        "evidence_simulated": post_summary.get("evidence_simulated") is True,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": rollback_success_claim_allowed,
        "dryrun_success_claim_attempt_blocked": post_summary.get("dryrun_success_claim_attempt_blocked") is True,
        "closure_allowed": True,
        "ready_for_rollback_rehearsal_execution": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "missing_rollback_rehearsal_blocks_real_migration": gap_closure.get(
            "missing_rollback_rehearsal_blocks_real_migration", True
        ),
        "missing_rollback_rehearsal_blocks_batch_arming": gap_closure.get(
            "missing_rollback_rehearsal_blocks_batch_arming", True
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no-real-migration-execution": True,
        "no-batch-arming": True,
        "no-rollback-execution": True,
        "no-rollback-rehearsal-execution": True,
        "no-sandbox-creation": True,
        "no-branch-creation": True,
        "no-restore-path-map-generation": True,
        "no-docs-link-restore-execution": True,
        "no-verdict-table-restore-execution": True,
        "no-eval-out-reference-restore-execution": True,
        "no-linkage-restore-execution": True,
        "no-verifier-rerun-execution": True,
        "no-rollback-evidence-generation": True,
        "no-rollback-success-claim": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-docs-modification": True,
        "no-readme-modification": True,
        "no-phase-verdict-table-modification": True,
        "no-post-migration-test-execution": True,
        "no-verifier-suite-execution": True,
        "no-human-review-execution": True,
        "no-protected-asset-modification": True,
        "no-permanent-block-release": True,
        "no-real-evidence-pack-generation": True,
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

    rollback_rehearsal_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_rollback_rehearsal_action_pool = {
        "deferred_actions": [
            {"action": a, "auto_execute_allowed": False, "requires_roadmap_decision": True}
            for a in DEFERRED_ACTIONS
        ],
        "deferred_action_count": len(DEFERRED_ACTIONS),
        "real_migration_started": False,
        "batch_arming_started": False,
        "rollback_rehearsal_execution_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not post_review_loaded:
        blockers.append("rollback_rehearsal_post_review_not_ready")
    if not dryrun_loaded:
        blockers.append("rollback_rehearsal_dryrun_not_ready")
    if not planning_loaded:
        blockers.append("rollback_rehearsal_dryrun_planning_not_ready")
    if not pre_auth_closure_loaded:
        blockers.append("pre_authorization_closure_not_confirmed")
    if len(completed_phase_rows) < 3:
        blockers.append("completed_phase_matrix_incomplete")
    if _bool_val(post_summary.get("sandbox_created_now"), False):
        blockers.append("sandbox_created")
    if _bool_val(post_summary.get("branch_created_now"), False):
        blockers.append("branch_created")
    if _bool_val(post_summary.get("evidence_generated_now"), False):
        blockers.append("evidence_generated")
    if rollback_success_claim_allowed:
        blockers.append("rollback_success_claim_allowed_true")
    if _bool_val(post_summary.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_executed")

    post_art = roots["rollback_rehearsal_post_review"]["artifacts"]
    review_passes = [
        (post_art.get("rehearsal_sandbox_post_review.json") or {}).get("sandbox_review_pass"),
        (post_art.get("rollback_rehearsal_scope_post_review.json") or {}).get("rollback_scope_review_pass"),
        (post_art.get("rollback_restore_path_map_post_review.json") or {}).get("restore_path_map_review_pass"),
        (post_art.get("docs_link_restore_post_review.json") or {}).get("docs_link_restore_review_pass"),
        (post_art.get("verdict_table_restore_post_review.json") or {}).get("verdict_table_restore_review_pass"),
        (post_art.get("eval_out_reference_restore_post_review.json") or {}).get("eval_out_reference_restore_review_pass"),
        (post_art.get("capability_runner_verifier_doc_linkage_restore_post_review.json") or {}).get(
            "linkage_restore_review_pass"
        ),
        (post_art.get("rollback_verifier_rerun_post_review.json") or {}).get("rollback_verifier_rerun_review_pass"),
        (post_art.get("rollback_rehearsal_evidence_post_review.json") or {}).get("rollback_evidence_review_pass"),
        (post_art.get("rollback_success_claim_post_review.json") or {}).get("rollback_success_claim_review_pass"),
    ]
    if not all(review_passes):
        blockers.append("post_review_pass_incomplete")

    boundary_ok = not blockers
    closure_allowed = boundary_ok

    closure_readiness_gate = {
        "go_conditions": [
            "rollback rehearsal Planning→DryRun→Post-Review chain GO",
            "sandbox/branch not created; restore/evidence not generated",
            "verifier rerun not executed; success claim blocked",
            "missing_rollback_rehearsal still blocks migration and arming",
        ],
        "no_go_conditions": [
            "any required root missing",
            "sandbox/branch created or rehearsal executed or success claim allowed",
        ],
        "ready_for_closure": boundary_ok,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "completed_phase_chain": [r["phase_id"] for r in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "planning_ref": "_eval_out/main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0/",
        "dryrun_ref": "_eval_out/main_project_structure_migration_rollback_rehearsal_dryrun_v1_smoke_v0/",
        "post_review_ref": "_eval_out/main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/",
        "sandbox_ref": "rehearsal_sandbox_policy.json",
        "rollback_scope_ref": "rollback_rehearsal_dryrun_scope.json",
        "restore_path_map_ref": "rollback_restore_path_map_plan.json",
        "docs_link_restore_ref": "docs_link_restore_plan.json",
        "verdict_table_restore_ref": "verdict_table_restore_plan.json",
        "eval_out_reference_restore_ref": "eval_out_reference_restore_plan.json",
        "linkage_restore_ref": "capability_runner_verifier_doc_linkage_restore_plan.json",
        "verifier_rerun_ref": "rollback_verifier_rerun_plan.json",
        "evidence_template_ref": "rollback_rehearsal_evidence_template.json",
        "success_claim_policy_ref": "rollback_success_claim_policy.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "rollback_rehearsal_non_claims_register.json",
        "deferred_action_pool_ref": "deferred_rollback_rehearsal_action_pool.json",
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_CLOSURE_REQUIRES_FIXES",
        "roadmap_decision_options": [
            "rollback rehearsal execution planning",
            "owner approval workflow planning",
            "controlled batch arming planning",
            "post-migration test harness execution planning",
            "pause structure migration and return to mainline capability building",
            "defer whitebox/test center design until main migration and tests complete",
        ],
        "priority_note": (
            "closure freezes rollback rehearsal dry-run chain only; Roadmap Decision re-arbitrates "
            "without authorizing real migration, rehearsal execution, sandbox/branch, evidence, or arming"
        ),
        "reason": "rollback rehearsal Planning→DryRun→Post-Review closed; no execution permissions granted",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "rollback_rehearsal_post_review_input_loaded": post_review_loaded,
        "rollback_rehearsal_dryrun_input_loaded": dryrun_loaded,
        "rollback_rehearsal_dryrun_planning_input_loaded": planning_loaded,
        "post_pre_authorization_roadmap_input_loaded": roadmap_loaded,
        "pre_authorization_closure_input_loaded": pre_auth_closure_loaded,
        "pre_authorization_post_review_input_loaded": pre_auth_post_review_loaded,
        "pre_authorization_dryrun_input_loaded": pre_auth_dryrun_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "rollback_rehearsal_closure_decision_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "deferred_action_pool_generated": True,
        "closure_readiness_gate_generated": True,
        "scope_batch_count": rollback_rehearsal_closure_decision_summary["scope_batch_count"],
        "mandatory_rollback_path_count": rollback_rehearsal_closure_decision_summary["mandatory_rollback_path_count"],
        "verifier_suite_count": rollback_rehearsal_closure_decision_summary["verifier_suite_count"],
        "required_verifier_count": rollback_rehearsal_closure_decision_summary["required_verifier_count"],
        "rollback_specific_verifier_count": rollback_rehearsal_closure_decision_summary[
            "rollback_specific_verifier_count"
        ],
        "sandbox_simulated": rollback_rehearsal_closure_decision_summary["sandbox_simulated"],
        "sandbox_created_now": False,
        "branch_created_now": False,
        "b0_baseline_restore_check_simulated": rollback_rehearsal_closure_decision_summary[
            "b0_baseline_restore_check_simulated"
        ],
        "b1_docs_relink_rollback_path_simulated": rollback_rehearsal_closure_decision_summary[
            "b1_docs_relink_rollback_path_simulated"
        ],
        "b2_capability_grouping_rollback_path_simulated": rollback_rehearsal_closure_decision_summary[
            "b2_capability_grouping_rollback_path_simulated"
        ],
        "b3_governance_grouping_rollback_path_simulated": rollback_rehearsal_closure_decision_summary[
            "b3_governance_grouping_rollback_path_simulated"
        ],
        "b4_midplatform_core_rollback_path_simulated": rollback_rehearsal_closure_decision_summary[
            "b4_midplatform_core_rollback_path_simulated"
        ],
        "b5_dev_artifact_reference_rollback_path_simulated": rollback_rehearsal_closure_decision_summary[
            "b5_dev_artifact_reference_rollback_path_simulated"
        ],
        "b6_future_marker_rollback_path_simulated": rollback_rehearsal_closure_decision_summary[
            "b6_future_marker_rollback_path_simulated"
        ],
        "b7_verification_gate_restore_check_simulated": rollback_rehearsal_closure_decision_summary[
            "b7_verification_gate_restore_check_simulated"
        ],
        "rollback_reverse_mapping_simulated": rollback_rehearsal_closure_decision_summary[
            "rollback_reverse_mapping_simulated"
        ],
        "protected_asset_restore_rule_simulated": rollback_rehearsal_closure_decision_summary[
            "protected_asset_restore_rule_simulated"
        ],
        "HR_DnAE_restore_rule_simulated": rollback_rehearsal_closure_decision_summary["HR_DnAE_restore_rule_simulated"],
        "path_conflict_detection_simulated": rollback_rehearsal_closure_decision_summary[
            "path_conflict_detection_simulated"
        ],
        "restore_path_map_generated_now": False,
        "docs_link_restore_required": True,
        "docs_link_restore_executed_now": False,
        "verdict_table_restore_required_if_touched": True,
        "verdict_table_restore_executed_now": False,
        "eval_out_reference_restore_required": True,
        "eval_out_content_move_forbidden": True,
        "eval_out_reference_restore_executed_now": False,
        "linkage_restore_required": True,
        "linkage_restore_executed_now": False,
        "verifier_rerun_required": True,
        "verifier_rerun_simulated": rollback_rehearsal_closure_decision_summary["verifier_rerun_simulated"],
        "verifier_rerun_executed_now": False,
        "verifier_rerun_success_claim_allowed": False,
        "evidence_simulated": rollback_rehearsal_closure_decision_summary["evidence_simulated"],
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": rollback_success_claim_allowed,
        "dryrun_success_claim_attempt_blocked": rollback_rehearsal_closure_decision_summary[
            "dryrun_success_claim_attempt_blocked"
        ],
        "rollback_rehearsal_dryrun_planning_closed": planning_loaded,
        "rollback_rehearsal_dryrun_closed": dryrun_loaded,
        "rollback_rehearsal_post_review_closed": post_review_loaded,
        "rollback_rehearsal_chain_closed": boundary_ok,
        "closure_allowed": closure_allowed,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_dryrun_execution_allowed": False,
        "rollback_evidence_generation_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "missing_rollback_rehearsal_blocks_real_migration": gap_closure.get(
            "missing_rollback_rehearsal_blocks_real_migration", True
        ),
        "missing_rollback_rehearsal_blocks_batch_arming": gap_closure.get(
            "missing_rollback_rehearsal_blocks_batch_arming", True
        ),
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": _bool_val(post_summary.get("rollback_rehearsal_executed"), False),
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
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_rehearsal_closure_summary": rollback_rehearsal_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "rollback_rehearsal_closure_decision_summary": rollback_rehearsal_closure_decision_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "rollback_rehearsal_non_claims_register": rollback_rehearsal_non_claims_register,
        "deferred_rollback_rehearsal_action_pool": deferred_rollback_rehearsal_action_pool,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
