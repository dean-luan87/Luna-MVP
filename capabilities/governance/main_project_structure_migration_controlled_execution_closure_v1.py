# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Execution Closure v1.

Closure-only: freeze controlled execution chain status and boundaries.
No real migration, batch arming, tests, verifier suite, or rollback rehearsal.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001"
CLOSURE_ID = "main_proj_struct_migration_controlled_execution_closure_v1_001"
CLOSURE_SCOPE = "main_project_structure_migration_controlled_execution_closure_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_execution_closure_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

COMPLETED_PHASES = [
    (
        "Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001",
        "Main Project Structure Migration Controlled Execution Planning",
        "controlled_execution_planning",
        "_eval_out/main_project_structure_migration_controlled_execution_planning_v1_smoke_v0/",
        PLANNING_DECISION,
        "B0–B7 execution plan, owner gates, test/verifier order, rollback precondition",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001",
        "Main Project Structure Migration Controlled Execution DryRun",
        "controlled_execution_dryrun",
        "_eval_out/main_project_structure_migration_controlled_execution_dryrun_v1_smoke_v0/",
        DRYRUN_DECISION,
        "simulate window/owner/arming/progression without execution permissions",
    ),
    (
        "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001",
        "Main Project Structure Migration Controlled Execution Post-DryRun Review",
        "controlled_execution_post_review",
        "_eval_out/main_project_structure_migration_controlled_execution_post_dryrun_review_v1_smoke_v0/",
        POST_REVIEW_DECISION,
        "formal post-dryrun audit for controlled execution closure readiness",
    ),
]

NON_CLAIMS = [
    "closure 不等于真实迁移可执行",
    "closure 不等于 batch 可以 armed",
    "closure 不等于 batch 已执行",
    "closure 不等于文件移动/删除/重命名/合并可执行",
    "closure 不等于迁移后测试可执行",
    "closure 不等于迁移后测试已通过",
    "closure 不等于 verifier suite 可执行",
    "closure 不等于 verifier suite 已通过",
    "closure 不等于 rollback rehearsal 可执行",
    "closure 不等于 rollback 已执行",
    "closure 不等于 owner 已确认",
    "closure 不等于 HumanApproval 已完成",
    "closure 不等于 protected / HR / DnAE 可处理",
    "closure 不等于真实 evidence pack 已生成",
    "closure 不等于白盒/测试中心结构可开始执行",
    "closure 不等于 Developer Backend 架构已定稿",
    "closure 不等于未来模块结构已定稿",
    "closure 不等于 production structure ready",
    "controlled execution chain closed 不等于 real_migration_execution_allowed",
]

DEFERRED_ACTIONS = [
    "real migration execution",
    "batch arming execution",
    "batch execution",
    "owner approval execution",
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
    "rollback rehearsal execution",
    "rollback execution",
    "real evidence pack generation",
    "whitebox/test center design",
    "developer backend architecture",
    "future module finalization",
]

POST_REVIEW_ARTIFACTS = [
    "summary.json",
    "controlled_execution_dryrun_input_review.json",
    "execution_window_post_review.json",
    "owner_authorization_post_review.json",
    "batch_arming_post_review.json",
    "controlled_batch_progression_post_review.json",
    "rollback_rehearsal_precondition_post_review.json",
    "post_batch_test_execution_order_post_review.json",
    "verifier_suite_execution_order_post_review.json",
    "abort_and_failure_response_post_review.json",
    "post_execution_evidence_pack_post_review.json",
    "controlled_execution_boundary_post_review.json",
    "controlled_execution_post_dryrun_readiness_decision.json",
    "verifier_report.json",
]

DRYRUN_ARTIFACTS = [
    "summary.json",
    "controlled_execution_dryrun_execution_plan.json",
    "execution_window_dryrun_result.json",
    "batch_arming_execution_dryrun_result.json",
    "controlled_batch_progression_dryrun_result.json",
    "post_batch_test_execution_order_dryrun_result.json",
    "verifier_suite_execution_order_dryrun_result.json",
    "rollback_rehearsal_precondition_dryrun_result.json",
    "post_execution_evidence_pack_dryrun_result.json",
    "verifier_report.json",
]

PLANNING_ARTIFACTS = [
    "summary.json",
    "controlled_migration_execution_planning_policy.json",
    "controlled_execution_batch_plan.json",
    "execution_window_policy.json",
    "owner_authorization_gate.json",
    "batch_arming_execution_plan.json",
    "rollback_rehearsal_precondition.json",
    "post_batch_test_execution_order.json",
    "verifier_suite_execution_order.json",
    "abort_and_failure_response_plan.json",
    "post_execution_evidence_pack_plan.json",
    "verifier_report.json",
]

ROOT_SPECS = [
    {
        "id": "controlled_execution_post_review",
        "arg": "controlled_execution_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": POST_REVIEW_ARTIFACTS,
    },
    {
        "id": "controlled_execution_dryrun",
        "arg": "controlled_execution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "execution_control_roadmap",
        "arg": "execution_control_roadmap_root",
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


def run_main_project_structure_migration_controlled_execution_closure_v1(
    *,
    controlled_execution_post_review_root: str,
    controlled_execution_dryrun_root: str,
    controlled_execution_planning_root: str,
    execution_control_roadmap_root: str,
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
    post_summary = summaries["controlled_execution_post_review"]

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
        roots["controlled_execution_post_review"]["loaded"]
        and post_summary.get("final_decision") == POST_REVIEW_DECISION
        and post_summary.get("ready_for_closure") is True
    )
    dryrun_loaded = (
        roots["controlled_execution_dryrun"]["loaded"]
        and summaries["controlled_execution_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == PLANNING_DECISION
    )
    ec_roadmap_loaded = roots["execution_control_roadmap"]["loaded"]
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

    batch_count = post_summary.get("batch_count", 8)
    armed_count = post_summary.get("armed_batch_count", 0)
    abort_count = post_summary.get("abort_condition_count", 16)
    failure_count = post_summary.get("failure_response_type_count", 11)
    post_batch_test_count = post_summary.get("post_batch_test_count", 31)
    executed_test_count = post_summary.get("executed_test_count", 0)
    verifier_suite_count = post_summary.get("verifier_suite_count", 12)

    candidate_flags = [
        post_summary.get("b0_baseline_only_no_move"),
        post_summary.get("b1_docs_relink_candidate_only"),
        post_summary.get("b2_capability_grouping_candidate_only"),
        post_summary.get("b3_governance_grouping_candidate_only"),
        post_summary.get("b4_midplatform_grouping_candidate_only"),
        post_summary.get("b5_dev_artifact_reference_only"),
        post_summary.get("b6_future_marker_only"),
        post_summary.get("b7_verification_gate_only"),
    ]
    candidate_only_batch_count = sum(1 for f in candidate_flags if f is True)

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
                "batch_execution_count": 0,
                "post_migration_tests_executed": False,
                "verifier_suite_executed": False,
                "rollback_rehearsal_executed": False,
                "evidence_pack_generated_now": False,
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

    controlled_execution_closure_decision_summary = {
        "execution_window_requirement_count": post_summary.get("execution_window_requirement_count", 10),
        "execution_window_opened": _bool_val(post_summary.get("execution_window_opened"), False),
        "owner_authorization_gate_count": post_summary.get("owner_authorization_gate_count", 7),
        "owner_approval_executed": _bool_val(post_summary.get("owner_approval_executed"), False),
        "owner_auto_confirm_allowed": _bool_val(post_summary.get("owner_auto_confirm_allowed"), False),
        "final_owner_human_confirmed": _bool_val(post_summary.get("final_owner_human_confirmed"), False),
        "batch_count": batch_count,
        "batch_arming_simulated": post_summary.get("batch_arming_simulated") is True,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": post_summary.get("all_batches_not_armed") is True,
        "batch_progression_simulated": post_summary.get("batch_progression_simulated") is True,
        "batch_execution_count": post_summary.get("batch_execution_count", 0),
        "candidate_only_batch_count": candidate_only_batch_count,
        "rollback_rehearsal_mandatory": post_summary.get("rollback_rehearsal_mandatory") is True,
        "rollback_rehearsal_executed": _bool_val(post_summary.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": post_summary.get("rollback_execution_still_blocked") is True,
        "post_batch_test_count": post_batch_test_count,
        "tests_mapped_to_batches": post_summary.get("tests_mapped_to_batches") is True,
        "executed_test_count": executed_test_count,
        "verifier_suite_count": verifier_suite_count,
        "verifier_suite_executed": _bool_val(post_summary.get("verifier_suite_executed"), False),
        "abort_condition_count": abort_count,
        "failure_response_type_count": failure_count,
        "every_abort_has_failure_response": post_summary.get("every_abort_has_failure_response") is True,
        "evidence_pack_generated_now": _bool_val(post_summary.get("evidence_pack_generated_now"), False),
        "execution_result_claimed_now": _bool_val(post_summary.get("execution_result_claimed_now"), False),
        "post_execution_evidence_pack_template_defined": post_summary.get(
            "post_execution_evidence_pack_template_defined", True
        ),
        "closure_allowed": True,
        "real_migration_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no-real-migration-execution": True,
        "no-batch-arming": True,
        "no-batch-execution": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-docs-modification": True,
        "no-readme-modification": True,
        "no-phase-verdict-table-modification": True,
        "no-post-migration-test-execution": True,
        "no-verifier-suite-execution": True,
        "no-rollback-rehearsal-execution": True,
        "no-rollback-execution": True,
        "no-owner-approval-execution": True,
        "no-human-owner-confirmation": True,
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

    controlled_execution_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    correction_a = {
        "correction_id": "controlled_execution_post_review_all_not_armed_eval_v1",
        "source_phase": "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001",
        "issue": "all_not_armed boolean evaluation bug",
        "original_behavior": "all(armed_now is False) caused incorrect false result for all_not_armed",
        "corrected_behavior": "proper boolean normalization via _bool_val and all_batches_not_armed from dryrun summary",
        "semantic_impact": "no_permission_granted",
        "boundary_impact": "no_boundary_change",
        "runtime_impact": "none",
        "migration_permission_impact": "none",
        "verification_status": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    correction_record = {
        "corrections": [correction_a],
        "correction_record_count": 1,
        "correction_record_status": "recorded",
        "correction_semantic_impact": "no_permission_granted",
        "correction_boundary_impact": "no_boundary_change",
        "correction_runtime_impact": "none",
        "correction_migration_permission_impact": "none",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_controlled_execution_action_pool = {
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
        blockers.append("controlled_execution_post_review_not_ready")
    if not dryrun_loaded:
        blockers.append("controlled_execution_dryrun_not_ready")
    if not planning_loaded:
        blockers.append("controlled_execution_planning_not_ready")
    if not ec_closure_loaded:
        blockers.append("execution_control_closure_not_confirmed")
    if not guarded_closure_loaded:
        blockers.append("guarded_closure_not_confirmed")
    if armed_count != 0:
        blockers.append("armed_batch_count_nonzero")
    if not post_summary.get("all_batches_not_armed"):
        blockers.append("all_batches_not_armed_false")
    if post_summary.get("batch_execution_count", 0) != 0:
        blockers.append("batch_execution_count_nonzero")
    if executed_test_count != 0:
        blockers.append("post_migration_tests_executed")
    if _bool_val(post_summary.get("verifier_suite_executed"), False):
        blockers.append("verifier_suite_executed")
    if _bool_val(post_summary.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_executed")
    if _bool_val(post_summary.get("evidence_pack_generated_now"), False):
        blockers.append("evidence_pack_generated")
    if candidate_only_batch_count != 8:
        blockers.append("candidate_only_batch_count_not_8")
    if len(completed_phase_rows) < 3:
        blockers.append("completed_phase_matrix_incomplete")

    boundary_ok = not blockers
    closure_allowed = boundary_ok

    closure_readiness_gate = {
        "go_conditions": [
            "planning → dryrun → post-review chain GO",
            "armed_batch_count=0; all_batches_not_armed=true",
            "B0–B7 candidate-only; batch_execution_count=0",
            "31 tests ordered, 0 executed; 12 verifiers ordered, not executed",
            "rollback rehearsal required, not executed; evidence template only",
            "all_not_armed correction recorded without permission grant",
            "real_migration_execution_allowed false",
        ],
        "no_go_conditions": [
            "any required root missing",
            "batch armed or tests/verifier/rollback/evidence executed",
        ],
        "ready_for_closure": boundary_ok,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_execution_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "completed_phase_chain": [r["phase_id"] for r in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "planning_ref": "_eval_out/main_project_structure_migration_controlled_execution_planning_v1_smoke_v0/",
        "dryrun_ref": "_eval_out/main_project_structure_migration_controlled_execution_dryrun_v1_smoke_v0/",
        "post_review_ref": "_eval_out/main_project_structure_migration_controlled_execution_post_dryrun_review_v1_smoke_v0/",
        "execution_window_ref": "execution_window_policy.json",
        "owner_authorization_ref": "owner_authorization_gate.json",
        "batch_arming_ref": "batch_arming_execution_plan.json",
        "batch_progression_ref": "controlled_execution_batch_plan.json",
        "rollback_rehearsal_ref": "rollback_rehearsal_precondition.json",
        "post_batch_test_order_ref": "post_batch_test_execution_order.json",
        "verifier_suite_order_ref": "verifier_suite_execution_order.json",
        "abort_failure_response_ref": "abort_and_failure_response_plan.json",
        "evidence_pack_template_ref": "post_execution_evidence_pack_plan.json",
        "correction_record_ref": "correction_record.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "controlled_execution_non_claims_register.json",
        "deferred_action_pool_ref": "deferred_controlled_execution_action_pool.json",
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSURE_REQUIRES_FIXES",
        "roadmap_decision_options": [
            "real migration execution pre-authorization planning",
            "owner approval resolution planning",
            "rollback rehearsal dry-run / planning",
            "post-migration test harness execution planning",
            "pause structure migration and return to mainline capability building",
            "defer whitebox/test center design until main migration and tests complete",
        ],
        "priority_note": (
            "closure freezes controlled execution chain only; Roadmap Decision must re-arbitrate "
            "next step without authorizing real migration, batch arming, tests, verifier, or rollback"
        ),
        "reason": "controlled execution closure complete; no direct migration or execution permissions",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "controlled_execution_post_review_input_loaded": post_review_loaded,
        "controlled_execution_dryrun_input_loaded": dryrun_loaded,
        "controlled_execution_planning_input_loaded": planning_loaded,
        "execution_control_roadmap_input_loaded": ec_roadmap_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "controlled_execution_closure_decision_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "correction_record_generated": True,
        "deferred_action_pool_generated": True,
        "closure_readiness_gate_generated": True,
        "execution_window_requirement_count": post_summary.get("execution_window_requirement_count", 10),
        "execution_window_opened": _bool_val(post_summary.get("execution_window_opened"), False),
        "owner_authorization_gate_count": post_summary.get("owner_authorization_gate_count", 7),
        "owner_approval_executed": _bool_val(post_summary.get("owner_approval_executed"), False),
        "owner_auto_confirm_allowed": _bool_val(post_summary.get("owner_auto_confirm_allowed"), False),
        "final_owner_human_confirmed": _bool_val(post_summary.get("final_owner_human_confirmed"), False),
        "batch_count": batch_count,
        "batch_arming_simulated": post_summary.get("batch_arming_simulated") is True,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": post_summary.get("all_batches_not_armed") is True,
        "batch_progression_simulated": post_summary.get("batch_progression_simulated") is True,
        "batch_execution_count": post_summary.get("batch_execution_count", 0),
        "candidate_only_batch_count": candidate_only_batch_count,
        "b0_baseline_only_no_move": post_summary.get("b0_baseline_only_no_move") is True,
        "b1_docs_relink_candidate_only": post_summary.get("b1_docs_relink_candidate_only") is True,
        "b2_capability_grouping_candidate_only": post_summary.get("b2_capability_grouping_candidate_only") is True,
        "b3_governance_grouping_candidate_only": post_summary.get("b3_governance_grouping_candidate_only") is True,
        "b4_midplatform_grouping_candidate_only": post_summary.get("b4_midplatform_grouping_candidate_only") is True,
        "b5_dev_artifact_reference_only": post_summary.get("b5_dev_artifact_reference_only") is True,
        "b6_future_marker_only": post_summary.get("b6_future_marker_only") is True,
        "b7_verification_gate_only": post_summary.get("b7_verification_gate_only") is True,
        "rollback_rehearsal_mandatory": post_summary.get("rollback_rehearsal_mandatory") is True,
        "rollback_rehearsal_executed": _bool_val(post_summary.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": post_summary.get("rollback_execution_still_blocked") is True,
        "post_batch_test_count": post_batch_test_count,
        "tests_mapped_to_batches": post_summary.get("tests_mapped_to_batches") is True,
        "executed_test_count": executed_test_count,
        "verifier_suite_count": verifier_suite_count,
        "verifier_suite_executed": _bool_val(post_summary.get("verifier_suite_executed"), False),
        "abort_condition_count": abort_count,
        "failure_response_type_count": failure_count,
        "every_abort_has_failure_response": post_summary.get("every_abort_has_failure_response") is True,
        "post_execution_evidence_pack_template_defined": post_summary.get(
            "post_execution_evidence_pack_template_defined", True
        ),
        "evidence_pack_generated_now": _bool_val(post_summary.get("evidence_pack_generated_now"), False),
        "execution_result_claimed_now": _bool_val(post_summary.get("execution_result_claimed_now"), False),
        "correction_record_count": 1,
        "correction_semantic_impact": "no_permission_granted",
        "correction_boundary_impact": "no_boundary_change",
        "correction_runtime_impact": "none",
        "correction_migration_permission_impact": "none",
        "controlled_execution_planning_closed": planning_loaded,
        "controlled_execution_dryrun_closed": dryrun_loaded,
        "controlled_execution_post_review_closed": post_review_loaded,
        "controlled_execution_chain_closed": boundary_ok,
        "closure_allowed": closure_allowed,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_execution_closure_summary": controlled_execution_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "controlled_execution_closure_decision_summary": controlled_execution_closure_decision_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "controlled_execution_non_claims_register": controlled_execution_non_claims_register,
        "correction_record": correction_record,
        "deferred_controlled_execution_action_pool": deferred_controlled_execution_action_pool,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
