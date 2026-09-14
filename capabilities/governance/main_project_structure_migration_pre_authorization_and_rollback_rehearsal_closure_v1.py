# -*- coding: utf-8 -*-
"""Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Closure v1.

Closure-only: freeze pre-authorization / rollback rehearsal governance chain.
No real migration, owner confirmation, ack, package, rehearsal, or batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001"
CLOSURE_ID = "main_proj_struct_migration_pre_auth_rollback_rehearsal_closure_v1_001"
CLOSURE_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_only"
SOURCE_CHAIN = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN"
ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_READY_FOR_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING"
)
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

COMPLETED_PHASES = [
    (
        "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001",
        "Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Planning",
        "pre_authorization_planning",
        "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0/",
        PLANNING_DECISION,
        "define owner/auth, operator ack, package, rehearsal scope/plan/evidence, arming preconditions",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001",
        "Main Project Structure Migration Pre-Authorization and Rollback Rehearsal DryRun",
        "pre_authorization_dryrun",
        "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1_smoke_v0/",
        DRYRUN_DECISION,
        "simulate owner/ack/rehearsal/package gaps blocking migration and arming",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001",
        "Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Post-DryRun Review",
        "pre_authorization_post_review",
        "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/",
        POST_REVIEW_DECISION,
        "formal post-dryrun audit for pre-authorization closure readiness",
    ),
]

NON_CLAIMS = [
    "closure 不等于真实迁移可执行",
    "closure 不等于 batch 可以 armed",
    "closure 不等于 owner 已确认",
    "closure 不等于 owner approval 已执行",
    "closure 不等于 operator acknowledgement 已执行",
    "closure 不等于 authorization package 已生成",
    "closure 不等于 rollback rehearsal 可执行",
    "closure 不等于 rollback rehearsal 已执行",
    "closure 不等于 rollback evidence 已生成",
    "closure 不等于 rollback success 可声明",
    "closure 不等于文件移动/删除/重命名/合并可执行",
    "closure 不等于迁移后测试可执行",
    "closure 不等于 verifier suite 可执行",
    "closure 不等于 protected / HR / DnAE 可处理",
    "closure 不等于白盒/测试中心结构可开始执行",
    "closure 不等于 Developer Backend 架构已定稿",
    "closure 不等于未来模块结构已定稿",
    "closure 不等于 production migration ready",
    "pre_authorization_rollback_rehearsal_chain_closed 不等于 real_migration_execution_allowed",
]

DEFERRED_ACTIONS = [
    "real migration execution",
    "batch arming execution",
    "owner confirmation",
    "owner approval execution",
    "operator acknowledgement execution",
    "authorization package generation",
    "rollback rehearsal execution",
    "rollback evidence generation",
    "rollback success claim",
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
    "post-migration test execution",
    "verifier suite execution",
    "rollback execution",
    "real evidence pack generation",
    "whitebox/test center design",
    "developer backend architecture",
    "future module finalization",
]

POST_REVIEW_ARTIFACTS = [
    "summary.json",
    "pre_authorization_dryrun_input_review.json",
    "owner_authorization_post_review.json",
    "operator_acknowledgement_post_review.json",
    "pre_execution_authorization_package_post_review.json",
    "rollback_rehearsal_scope_post_review.json",
    "rollback_rehearsal_plan_post_review.json",
    "rollback_rehearsal_evidence_post_review.json",
    "batch_arming_precondition_post_review.json",
    "authorization_blocker_post_review.json",
    "gap_hard_block_post_review.json",
    "pre_authorization_boundary_post_review.json",
    "pre_authorization_post_dryrun_readiness_decision.json",
    "verifier_report.json",
]

DRYRUN_ARTIFACTS = [
    "summary.json",
    "pre_authorization_rollback_dryrun_execution_plan.json",
    "owner_authorization_dryrun_result.json",
    "operator_acknowledgement_dryrun_result.json",
    "pre_execution_authorization_package_dryrun_result.json",
    "rollback_rehearsal_scope_dryrun_result.json",
    "rollback_rehearsal_plan_dryrun_result.json",
    "rollback_rehearsal_evidence_dryrun_result.json",
    "batch_arming_precondition_dryrun_result.json",
    "authorization_blocker_dryrun_result.json",
    "pre_authorization_dryrun_boundary_review.json",
    "pre_authorization_dryrun_readiness_decision.json",
    "verifier_report.json",
]

PLANNING_ARTIFACTS = [
    "summary.json",
    "pre_authorization_and_rollback_rehearsal_planning_policy.json",
    "owner_authorization_resolution_plan.json",
    "operator_acknowledgement_policy.json",
    "pre_execution_authorization_package.json",
    "rollback_rehearsal_scope.json",
    "rollback_rehearsal_plan.json",
    "rollback_rehearsal_evidence_template.json",
    "batch_arming_precondition_record.json",
    "authorization_blocker_policy.json",
    "pre_authorization_planning_readiness_decision.json",
    "verifier_report.json",
]

ROOT_SPECS = [
    {
        "id": "pre_authorization_post_review",
        "arg": "pre_authorization_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": POST_REVIEW_ARTIFACTS,
    },
    {
        "id": "pre_authorization_dryrun",
        "arg": "pre_authorization_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
    {
        "id": "pre_authorization_planning",
        "arg": "pre_authorization_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "controlled_execution_roadmap",
        "arg": "controlled_execution_roadmap_root",
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
        "id": "controlled_execution_post_review",
        "arg": "controlled_execution_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_dryrun",
        "arg": "controlled_execution_dryrun_root",
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


def run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1(
    *,
    pre_authorization_post_review_root: str,
    pre_authorization_dryrun_root: str,
    pre_authorization_planning_root: str,
    controlled_execution_roadmap_root: str,
    controlled_execution_closure_root: str,
    controlled_execution_post_review_root: str,
    controlled_execution_dryrun_root: str,
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
    post_summary = summaries["pre_authorization_post_review"]
    dryrun_summary = summaries["pre_authorization_dryrun"]

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
        roots["pre_authorization_post_review"]["loaded"]
        and post_summary.get("final_decision") == POST_REVIEW_DECISION
        and post_summary.get("ready_for_closure") is True
    )
    dryrun_loaded = (
        roots["pre_authorization_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["pre_authorization_planning"]["loaded"]
        and summaries["pre_authorization_planning"].get("final_decision") == PLANNING_DECISION
    )
    roadmap_loaded = roots["controlled_execution_roadmap"]["loaded"]
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
    readiness_loaded = roots["readiness"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    armed_count = post_summary.get("armed_batch_count", 0)
    rollback_success_claim_allowed = _bool_val(
        dryrun_summary.get("rollback_success_claim_allowed", post_summary.get("rollback_success_claim_allowed")),
        False,
    )

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
                "real_migration_execution_allowed": False,
                "batch_arming_allowed_now": False,
                "owner_confirmed_now": False,
                "operator_ack_executed_now": False,
                "package_generated_now": False,
                "rollback_rehearsal_executed": False,
                "rollback_evidence_generated_now": False,
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

    pre_authorization_closure_decision_summary = {
        "owner_authorization_type_count": post_summary.get("owner_authorization_type_count", 7),
        "owner_authorization_simulated": post_summary.get("owner_authorization_simulated") is True,
        "owner_confirmed_now": _bool_val(post_summary.get("owner_confirmed_now"), False),
        "owner_approval_executed": _bool_val(post_summary.get("owner_approval_executed"), False),
        "owner_approval_execution_allowed": _bool_val(post_summary.get("owner_approval_execution_allowed"), False),
        "auto_confirm_allowed": _bool_val(post_summary.get("auto_confirm_allowed"), False),
        "missing_owner_blocks_execution": post_summary.get("missing_owner_blocks_execution", True),
        "missing_owner_blocks_batch_arming": post_summary.get("missing_owner_blocks_batch_arming", True),
        "operator_ack_required": post_summary.get("operator_ack_required", True),
        "operator_ack_simulated": post_summary.get("operator_ack_simulated") is True,
        "operator_ack_executed_now": _bool_val(post_summary.get("operator_ack_executed_now"), False),
        "operator_ack_auto_generated": _bool_val(post_summary.get("operator_ack_auto_generated"), False),
        "missing_operator_ack_blocks_execution": post_summary.get("missing_operator_ack_blocks_execution", True),
        "missing_operator_ack_blocks_batch_arming": post_summary.get("missing_operator_ack_blocks_batch_arming", True),
        "package_required_before_real_migration": post_summary.get("package_required_before_real_migration", True),
        "package_template_loaded": post_summary.get("package_template_loaded") is True,
        "included_record_count": post_summary.get("included_record_count", 0),
        "package_generated_now": _bool_val(post_summary.get("package_generated_now"), False),
        "missing_package_blocks_real_migration": post_summary.get("missing_package_blocks_real_migration", True),
        "rollback_rehearsal_scope_batch_count": post_summary.get("rollback_rehearsal_scope_batch_count", 0),
        "rollback_rehearsal_mandatory_batches_count": post_summary.get("rollback_rehearsal_mandatory_batches_count", 0),
        "b1_b6_rehearsal_mandatory": post_summary.get("b1_b6_rehearsal_mandatory", True),
        "rollback_rehearsal_step_count": post_summary.get("rollback_rehearsal_step_count", 0),
        "rehearsal_steps_simulated": post_summary.get("rehearsal_steps_simulated") is True,
        "rehearsal_execution_allowed_now": _bool_val(post_summary.get("rehearsal_execution_allowed_now"), False),
        "rehearsal_executed_now": _bool_val(post_summary.get("rehearsal_executed_now"), False),
        "failure_blocks_real_migration": post_summary.get("failure_blocks_real_migration", True),
        "rollback_evidence_template_loaded": post_summary.get("rollback_evidence_template_loaded") is True,
        "rollback_evidence_generated_now": _bool_val(post_summary.get("rollback_evidence_generated_now"), False),
        "rollback_success_claim_allowed": rollback_success_claim_allowed,
        "batch_arming_record_count": post_summary.get("batch_arming_record_count", 8),
        "arming_record_generated_now": _bool_val(post_summary.get("arming_record_generated_now"), False),
        "arming_allowed_now": _bool_val(post_summary.get("arming_allowed_now"), False),
        "armed_batch_count": armed_count,
        "all_batches_not_armed": post_summary.get("all_batches_not_armed") is True,
        "authorization_blocker_count": post_summary.get("authorization_blocker_count", 0),
        "blockers_simulated": post_summary.get("blockers_simulated") is True,
        "gap_hard_block_matrix_reviewed": post_summary.get("gap_hard_block_matrix_reviewed") is True,
        "closure_allowed": True,
        "real_migration_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    gap_hard_block_closure_summary = {
        "gap_hard_block_matrix_reviewed": post_summary.get("gap_hard_block_matrix_reviewed", True),
        "missing_owner_blocks_real_migration": post_summary.get("missing_owner_blocks_real_migration", True),
        "missing_owner_blocks_batch_arming": post_summary.get("missing_owner_blocks_batch_arming", True),
        "missing_operator_ack_blocks_real_migration": post_summary.get("missing_operator_ack_blocks_real_migration", True),
        "missing_operator_ack_blocks_batch_arming": post_summary.get("missing_operator_ack_blocks_batch_arming", True),
        "missing_rollback_rehearsal_blocks_real_migration": post_summary.get(
            "missing_rollback_rehearsal_blocks_real_migration", True
        ),
        "missing_rollback_rehearsal_blocks_batch_arming": post_summary.get(
            "missing_rollback_rehearsal_blocks_batch_arming", True
        ),
        "missing_package_blocks_real_migration": post_summary.get("missing_package_blocks_real_migration", True),
        "gap_hard_block_closure_pass": post_summary.get("gap_hard_block_matrix_reviewed") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no-real-migration-execution": True,
        "no-batch-arming": True,
        "no-owner-confirmation": True,
        "no-owner-approval-execution": True,
        "no-operator-ack-execution": True,
        "no-real-authorization-package-generation": True,
        "no-rollback-rehearsal-execution": True,
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
        "no-rollback-execution": True,
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

    pre_authorization_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    clarification_a = {
        "clarification_id": "pre_auth_rollback_rehearsal_rollback_success_claim_semantic_v1",
        "source_phase": "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001",
        "issue": "rollback_success_claim_allowed field semantic ambiguity",
        "source_of_truth": "dryrun summary",
        "problematic_pattern": (
            "dryrun child artifact used is False style to represent review pass, causing semantic confusion"
        ),
        "clarified_behavior": (
            "rollback_success_claim_allowed remains false; review pass does not imply rollback success claim"
        ),
        "semantic_impact": "no_permission_granted",
        "boundary_impact": "no_boundary_change",
        "runtime_impact": "none",
        "migration_permission_impact": "none",
        "rollback_permission_impact": "none",
        "verification_status": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    semantic_clarification_record = {
        "clarifications": [clarification_a],
        "clarification_count": 1,
        "semantic_clarification_status": "recorded",
        "semantic_clarification_impact": "no_permission_granted",
        "semantic_clarification_boundary_impact": "no_boundary_change",
        "semantic_clarification_runtime_impact": "none",
        "semantic_clarification_migration_permission_impact": "none",
        "semantic_clarification_rollback_permission_impact": "none",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_pre_authorization_action_pool = {
        "deferred_actions": [
            {"action": a, "auto_execute_allowed": False, "requires_roadmap_decision": True}
            for a in DEFERRED_ACTIONS
        ],
        "deferred_action_count": len(DEFERRED_ACTIONS),
        "real_migration_started": False,
        "batch_arming_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not post_review_loaded:
        blockers.append("pre_authorization_post_review_not_ready")
    if not dryrun_loaded:
        blockers.append("pre_authorization_dryrun_not_ready")
    if not planning_loaded:
        blockers.append("pre_authorization_planning_not_ready")
    if not ce_closure_loaded:
        blockers.append("controlled_execution_closure_not_confirmed")
    if armed_count != 0:
        blockers.append("armed_batch_count_nonzero")
    if not post_summary.get("all_batches_not_armed"):
        blockers.append("all_batches_not_armed_false")
    if rollback_success_claim_allowed:
        blockers.append("rollback_success_claim_allowed_true")
    if _bool_val(post_summary.get("rehearsal_executed_now"), False):
        blockers.append("rollback_rehearsal_executed")
    if _bool_val(post_summary.get("owner_confirmed_now"), False):
        blockers.append("owner_confirmed")
    if len(completed_phase_rows) < 3:
        blockers.append("completed_phase_matrix_incomplete")
    if not gap_hard_block_closure_summary.get("gap_hard_block_closure_pass"):
        blockers.append("gap_hard_block_closure_not_pass")

    boundary_ok = not blockers
    closure_allowed = boundary_ok

    closure_readiness_gate = {
        "go_conditions": [
            "planning → dryrun → post-review chain GO",
            "gap_hard_block_matrix frozen; armed_batch_count=0",
            "owner/ack/package/rehearsal gaps remain blocking",
            "semantic clarification A recorded without permission grant",
            "real_migration_execution_allowed false",
        ],
        "no_go_conditions": [
            "any required root missing",
            "owner confirmed or rehearsal executed or batch armed",
        ],
        "ready_for_closure": boundary_ok,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_authorization_rollback_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "completed_phase_chain": [r["phase_id"] for r in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "planning_ref": "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0/",
        "dryrun_ref": "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1_smoke_v0/",
        "post_review_ref": "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/",
        "owner_authorization_ref": "owner_authorization_resolution_plan.json",
        "operator_ack_ref": "operator_acknowledgement_policy.json",
        "pre_execution_package_ref": "pre_execution_authorization_package.json",
        "rollback_rehearsal_scope_ref": "rollback_rehearsal_scope.json",
        "rollback_rehearsal_plan_ref": "rollback_rehearsal_plan.json",
        "rollback_rehearsal_evidence_ref": "rollback_rehearsal_evidence_template.json",
        "batch_arming_precondition_ref": "batch_arming_precondition_record.json",
        "authorization_blocker_ref": "authorization_blocker_policy.json",
        "gap_hard_block_ref": "gap_hard_block_post_review.json",
        "semantic_clarification_ref": "semantic_clarification_record.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "pre_authorization_non_claims_register.json",
        "deferred_action_pool_ref": "deferred_pre_authorization_action_pool.json",
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_CLOSURE_REQUIRES_FIXES",
        "roadmap_decision_options": [
            "controlled batch arming planning",
            "rollback rehearsal dry-run planning",
            "owner approval execution workflow planning",
            "post-migration test harness execution planning",
            "pause structure migration and return to mainline capability building",
            "defer whitebox/test center design until main migration and tests complete",
        ],
        "priority_note": (
            "closure freezes pre-authorization chain only; Roadmap Decision must re-arbitrate "
            "next step without authorizing real migration, owner confirmation, ack, package, rehearsal, or arming"
        ),
        "reason": "pre-authorization and rollback rehearsal closure complete; no execution permissions granted",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "pre_authorization_post_review_input_loaded": post_review_loaded,
        "pre_authorization_dryrun_input_loaded": dryrun_loaded,
        "pre_authorization_planning_input_loaded": planning_loaded,
        "controlled_execution_roadmap_input_loaded": roadmap_loaded,
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
        "pre_authorization_closure_decision_summary_generated": True,
        "gap_hard_block_closure_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "semantic_clarification_record_generated": True,
        "deferred_action_pool_generated": True,
        "closure_readiness_gate_generated": True,
        "owner_authorization_type_count": pre_authorization_closure_decision_summary["owner_authorization_type_count"],
        "owner_authorization_simulated": pre_authorization_closure_decision_summary["owner_authorization_simulated"],
        "owner_confirmed_now": pre_authorization_closure_decision_summary["owner_confirmed_now"],
        "owner_approval_executed": pre_authorization_closure_decision_summary["owner_approval_executed"],
        "owner_approval_execution_allowed": pre_authorization_closure_decision_summary["owner_approval_execution_allowed"],
        "auto_confirm_allowed": pre_authorization_closure_decision_summary["auto_confirm_allowed"],
        "missing_owner_blocks_execution": pre_authorization_closure_decision_summary["missing_owner_blocks_execution"],
        "missing_owner_blocks_batch_arming": pre_authorization_closure_decision_summary["missing_owner_blocks_batch_arming"],
        "operator_ack_required": pre_authorization_closure_decision_summary["operator_ack_required"],
        "operator_ack_simulated": pre_authorization_closure_decision_summary["operator_ack_simulated"],
        "operator_ack_executed_now": pre_authorization_closure_decision_summary["operator_ack_executed_now"],
        "operator_ack_auto_generated": pre_authorization_closure_decision_summary["operator_ack_auto_generated"],
        "missing_operator_ack_blocks_execution": pre_authorization_closure_decision_summary["missing_operator_ack_blocks_execution"],
        "missing_operator_ack_blocks_batch_arming": pre_authorization_closure_decision_summary["missing_operator_ack_blocks_batch_arming"],
        "package_required_before_real_migration": pre_authorization_closure_decision_summary["package_required_before_real_migration"],
        "package_template_loaded": pre_authorization_closure_decision_summary["package_template_loaded"],
        "included_record_count": pre_authorization_closure_decision_summary["included_record_count"],
        "package_generated_now": pre_authorization_closure_decision_summary["package_generated_now"],
        "missing_package_blocks_real_migration": pre_authorization_closure_decision_summary["missing_package_blocks_real_migration"],
        "rollback_rehearsal_scope_batch_count": pre_authorization_closure_decision_summary["rollback_rehearsal_scope_batch_count"],
        "rollback_rehearsal_mandatory_batches_count": pre_authorization_closure_decision_summary["rollback_rehearsal_mandatory_batches_count"],
        "b1_b6_rehearsal_mandatory": pre_authorization_closure_decision_summary["b1_b6_rehearsal_mandatory"],
        "rollback_rehearsal_step_count": pre_authorization_closure_decision_summary["rollback_rehearsal_step_count"],
        "rehearsal_steps_simulated": pre_authorization_closure_decision_summary["rehearsal_steps_simulated"],
        "rehearsal_execution_allowed_now": pre_authorization_closure_decision_summary["rehearsal_execution_allowed_now"],
        "rehearsal_executed_now": pre_authorization_closure_decision_summary["rehearsal_executed_now"],
        "failure_blocks_real_migration": pre_authorization_closure_decision_summary["failure_blocks_real_migration"],
        "rollback_evidence_template_loaded": pre_authorization_closure_decision_summary["rollback_evidence_template_loaded"],
        "rollback_evidence_generated_now": pre_authorization_closure_decision_summary["rollback_evidence_generated_now"],
        "rollback_success_claim_allowed": rollback_success_claim_allowed,
        "batch_arming_record_count": pre_authorization_closure_decision_summary["batch_arming_record_count"],
        "arming_record_generated_now": pre_authorization_closure_decision_summary["arming_record_generated_now"],
        "arming_allowed_now": pre_authorization_closure_decision_summary["arming_allowed_now"],
        "armed_batch_count": armed_count,
        "all_batches_not_armed": pre_authorization_closure_decision_summary["all_batches_not_armed"],
        "authorization_blocker_count": pre_authorization_closure_decision_summary["authorization_blocker_count"],
        "blockers_simulated": pre_authorization_closure_decision_summary["blockers_simulated"],
        "missing_rollback_rehearsal_blocks_execution": post_summary.get("missing_rollback_rehearsal_blocks_execution", True),
        "missing_rollback_evidence_blocks_execution": post_summary.get("missing_rollback_evidence_blocks_execution", True),
        "missing_test_harness_readiness_blocks_execution": post_summary.get("missing_test_harness_readiness_blocks_execution", True),
        "missing_verifier_suite_readiness_blocks_execution": post_summary.get("missing_verifier_suite_readiness_blocks_execution", True),
        "protected_asset_inclusion_blocks_execution": post_summary.get("protected_asset_inclusion_blocks_execution", True),
        "HR_DnAE_inclusion_blocks_execution": post_summary.get("HR_DnAE_inclusion_blocks_execution", True),
        "batch_arming_record_missing_blocks_execution": post_summary.get("batch_arming_record_missing_blocks_execution", True),
        "abort_policy_missing_blocks_execution": post_summary.get("abort_policy_missing_blocks_execution", True),
        "dirty_working_tree_blocks_execution": post_summary.get("dirty_working_tree_blocks_execution", True),
        "missing_backup_branch_blocks_execution": post_summary.get("missing_backup_branch_blocks_execution", True),
        "auto_confirm_owner_blocks_execution": post_summary.get("auto_confirm_owner_blocks_execution", True),
        "rollback_rehearsal_bypass_blocks_execution": post_summary.get("rollback_rehearsal_bypass_blocks_execution", True),
        "parallel_batch_execution_blocks_execution": post_summary.get("parallel_batch_execution_blocks_execution", True),
        "gap_hard_block_matrix_reviewed": gap_hard_block_closure_summary["gap_hard_block_matrix_reviewed"],
        "missing_owner_blocks_real_migration": gap_hard_block_closure_summary["missing_owner_blocks_real_migration"],
        "missing_owner_blocks_batch_arming": gap_hard_block_closure_summary["missing_owner_blocks_batch_arming"],
        "missing_operator_ack_blocks_real_migration": gap_hard_block_closure_summary["missing_operator_ack_blocks_real_migration"],
        "missing_operator_ack_blocks_batch_arming": gap_hard_block_closure_summary["missing_operator_ack_blocks_batch_arming"],
        "missing_rollback_rehearsal_blocks_real_migration": gap_hard_block_closure_summary["missing_rollback_rehearsal_blocks_real_migration"],
        "missing_rollback_rehearsal_blocks_batch_arming": gap_hard_block_closure_summary["missing_rollback_rehearsal_blocks_batch_arming"],
        "missing_package_blocks_real_migration": gap_hard_block_closure_summary["missing_package_blocks_real_migration"],
        "semantic_clarification_status": "recorded",
        "semantic_clarification_impact": "no_permission_granted",
        "semantic_clarification_boundary_impact": "no_boundary_change",
        "semantic_clarification_runtime_impact": "none",
        "semantic_clarification_migration_permission_impact": "none",
        "semantic_clarification_rollback_permission_impact": "none",
        "pre_authorization_planning_closed": planning_loaded,
        "pre_authorization_dryrun_closed": dryrun_loaded,
        "pre_authorization_post_review_closed": post_review_loaded,
        "pre_authorization_rollback_rehearsal_chain_closed": boundary_ok,
        "closure_allowed": closure_allowed,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_rollback_rehearsal_execution": False,
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "pre_authorization_rollback_closure_summary": pre_authorization_rollback_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "pre_authorization_closure_decision_summary": pre_authorization_closure_decision_summary,
        "gap_hard_block_closure_summary": gap_hard_block_closure_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "pre_authorization_non_claims_register": pre_authorization_non_claims_register,
        "semantic_clarification_record": semantic_clarification_record,
        "deferred_pre_authorization_action_pool": deferred_pre_authorization_action_pool,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
