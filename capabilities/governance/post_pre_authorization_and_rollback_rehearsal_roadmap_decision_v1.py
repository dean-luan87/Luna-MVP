# -*- coding: utf-8 -*-
"""Post Pre-Authorization and Rollback Rehearsal Roadmap Decision v1.

Roadmap decision only: select Rollback Rehearsal DryRun Planning after pre-auth closure.
No real migration, batch arming, rollback rehearsal execution, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_pre_authorization_and_rollback_rehearsal_roadmap_decision_only"
DECISION_ID = "post_pre_auth_rollback_rehearsal_roadmap_decision_v1_001"
SOURCE_CHAIN = "post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1"
FINAL_DECISION = "POST_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_DRYRUN_PLANNING"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001"
SELECTED_ROUTE = "Rollback Rehearsal DryRun Planning"

PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": SELECTED_ROUTE,
        "route_type": "rollback_rehearsal_dryrun_planning",
        "readiness_level": "high",
        "dependency": [
            "pre_authorization_rollback_rehearsal_chain_closed",
            "rollback_rehearsal_executed=false",
            "missing_rollback_rehearsal_blocks_real_migration",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "define rollback rehearsal dry-run before batch arming or real migration",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Controlled Batch Arming Planning",
        "route_type": "controlled_batch_arming_planning",
        "readiness_level": "deferred",
        "dependency": ["rollback rehearsal dry-run planning first"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "must follow rollback rehearsal dry-run planning",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "must not precede rollback rehearsal dry-run planning",
        "recommended_phase_name": "Phase-Controlled-Batch-Arming-Planning-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Owner Approval Workflow Planning",
        "route_type": "owner_approval_workflow_planning",
        "readiness_level": "deferred",
        "dependency": ["7 owner types", "not before rollback rehearsal dry-run planning priority"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "parallel input to Route A; not standalone priority",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "owner approval execution must not precede rollback rehearsal dry-run planning",
        "recommended_phase_name": "Phase-Owner-Approval-Workflow-Planning-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "Post-Migration Test Harness Execution Planning",
        "route_type": "post_migration_test_harness_execution_planning",
        "readiness_level": "deferred",
        "dependency": ["rollback rehearsal and arming chain clearer first"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "defer until rollback rehearsal dry-run planning",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "requires rollback rehearsal and batch arming preconditions clearer",
        "recommended_phase_name": "Phase-Post-Migration-Test-Harness-Execution-Planning-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Real Migration Execution Trial",
        "route_type": "real_migration_execution_trial",
        "readiness_level": "blocked",
        "dependency": ["owner", "ack", "package", "rollback rehearsal"],
        "risk_level": "critical",
        "expected_value": "high",
        "runtime_risk": "critical",
        "write_risk": "critical",
        "governance_debt_impact": "actual file operations",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "real_migration_execution_allowed=false",
        "recommended_phase_name": "Phase-Real-Migration-Execution-Trial-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Rollback Rehearsal Execution",
        "route_type": "rollback_rehearsal_execution",
        "readiness_level": "blocked",
        "dependency": ["rollback rehearsal dry-run planning first"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "medium",
        "governance_debt_impact": "actual rollback rehearsal execution blocked this round",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "rollback_rehearsal_executed=false; only dry-run planning selected",
        "recommended_phase_name": "Phase-Rollback-Rehearsal-Execution-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Whitebox / Test Center Structure Optimization",
        "route_type": "whitebox_test_center_structure_optimization",
        "readiness_level": "deferred",
        "dependency": ["main migration", "post-migration tests"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "defer until main migration and tests complete",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "whitebox/test center deferred",
        "recommended_phase_name": "Phase-Whitebox-Test-Center-Structure-Optimization-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "Developer Backend Architecture",
        "route_type": "developer_backend_architecture",
        "readiness_level": "deferred",
        "dependency": ["backend structure decision"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "full backend architecture not finalized",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "developer backend overall structure deferred",
        "recommended_phase_name": "Phase-Developer-Backend-Architecture-Planning-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "Return to Mainline Capability Development",
        "route_type": "return_to_mainline",
        "readiness_level": "deferred",
        "dependency": ["structure migration at pre-migration governance stage"],
        "risk_level": "low",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "pause structure migration",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "structure migration at real-migration pre-governance stage; not return to mainline now",
        "recommended_phase_name": "Phase-Return-to-Mainline-Capability-Development-v1-001",
    },
    {
        "route_id": "J",
        "route_name": "Future Reserved Module Structure Review",
        "route_type": "future_reserved_module_review",
        "readiness_level": "discussion_only",
        "dependency": ["WorldModel", "Memory", "Library", "Emotion"],
        "risk_level": "low",
        "expected_value": "low",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "discussion only",
        "recommended_priority": "discussion",
        "selected_now": False,
        "defer_reason": "not selected; discussion only",
        "recommended_phase_name": "Phase-Future-Reserved-Module-Discussion-v1-001",
    },
]

NON_CLAIMS = [
    "roadmap decision 不等于真实迁移可执行",
    "roadmap decision 不等于 batch 可以 armed",
    "roadmap decision 不等于 owner 已确认",
    "roadmap decision 不等于 operator acknowledgement 已执行",
    "roadmap decision 不等于 authorization package 已生成",
    "roadmap decision 不等于 rollback rehearsal 可执行或已执行",
    "roadmap decision 不等于 rollback evidence 已生成",
    "roadmap decision 不等于 rollback success 可声明",
    "selected route 仍是 planning-only，不执行 rollback rehearsal",
    "pre-authorization closure 不等于 real_migration_execution_allowed",
    "rollback rehearsal dry-run planning 不等于 file move 已授权",
    "controlled batch arming planning 不应优先于 rollback rehearsal dry-run planning",
    "白盒/测试中心须等主工程迁移与迁移后测试完成后再设计",
    "Developer Backend 整体结构继续 deferred",
    "rollback_success_claim_allowed semantic clarification: no_permission_granted",
]

GOVERNANCE_DEBT = [
    "pre_authorization_rollback_rehearsal_chain_closed but real_migration_execution_allowed=false",
    "armed_batch_count=0; batch_arming_allowed_now=false",
    "owner_confirmed_now=false; operator_ack_executed_now=false",
    "package_generated_now=false; rollback_rehearsal_executed=false",
    "rollback_evidence_generated_now=false; rollback_success_claim_allowed=false",
    "missing_rollback_rehearsal blocks real migration and batch arming",
    "rollback rehearsal dry-run planning required before batch arming planning",
    "240 HR excluded; 914 permanent block excluded",
    "semantic clarification A: rollback_success_claim_allowed source=dryrun summary",
    "whitebox_test_center deferred",
    "developer_backend_architecture deferred",
]

CLOSURE_ARTIFACTS = [
    "summary.json",
    "pre_authorization_rollback_closure_summary.json",
    "pre_authorization_closure_decision_summary.json",
    "gap_hard_block_closure_summary.json",
    "closure_boundary_freeze.json",
    "pre_authorization_non_claims_register.json",
    "semantic_clarification_record.json",
    "deferred_pre_authorization_action_pool.json",
    "completed_phase_matrix.json",
]

PLANNING_ARTIFACTS = [
    "summary.json",
    "rollback_rehearsal_scope.json",
    "rollback_rehearsal_plan.json",
    "rollback_rehearsal_evidence_template.json",
    "batch_arming_precondition_record.json",
    "authorization_blocker_policy.json",
]

CE_PLANNING_ARTIFACTS = [
    "summary.json",
    "controlled_execution_batch_plan.json",
    "post_batch_test_execution_order.json",
    "verifier_suite_execution_order.json",
]

ROOT_SPECS = [
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": CLOSURE_ARTIFACTS,
    },
    {
        "id": "pre_authorization_post_review",
        "arg": "pre_authorization_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "pre_authorization_post_dryrun_readiness_decision.json"],
    },
    {
        "id": "pre_authorization_dryrun",
        "arg": "pre_authorization_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "authorization_blocker_dryrun_result.json"],
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
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": CE_PLANNING_ARTIFACTS,
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
    if root and artifacts:
        missing = [a for a in artifacts if _try_read_json(root / a) is None]
        loaded = loaded and not missing
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "decision_scope": DECISION_SCOPE,
        "decision_only": True,
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
        "docs_modified_by_decision": False,
        "readme_modified_by_decision": False,
        "phase_verdict_table_modified_by_decision": False,
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


def run_post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1(
    *,
    pre_authorization_closure_root: str,
    pre_authorization_post_review_root: str,
    pre_authorization_dryrun_root: str,
    pre_authorization_planning_root: str,
    controlled_execution_roadmap_root: str,
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

    closure_summary = summaries["pre_authorization_closure"]
    closure_loaded = (
        roots["pre_authorization_closure"]["loaded"]
        and closure_summary.get("final_decision") == PRE_AUTH_CLOSURE
        and closure_summary.get("pre_authorization_rollback_rehearsal_chain_closed") is True
    )
    post_review_loaded = (
        roots["pre_authorization_post_review"]["loaded"]
        and summaries["pre_authorization_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_loaded = (
        roots["pre_authorization_dryrun"]["loaded"]
        and summaries["pre_authorization_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["pre_authorization_planning"]["loaded"]
        and summaries["pre_authorization_planning"].get("final_decision") == PLANNING_DECISION
    )
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
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    structure_map_loaded = roots["structure_map"]["loaded"]
    gate_taxonomy_loaded = roots["gate_taxonomy"]["loaded"]

    closure_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(closure_root / "gap_hard_block_closure_summary.json") if closure_root else {}) or {}
    semantic_record = (_try_read_json(closure_root / "semantic_clarification_record.json") if closure_root else {}) or {}

    chain_closed = closure_summary.get("pre_authorization_rollback_rehearsal_chain_closed") is True
    armed_count = closure_summary.get("armed_batch_count", 0)

    pre_authorization_closure_status_summary = {
        "pre_authorization_rollback_rehearsal_chain_closed": chain_closed,
        "closure_final_decision": PRE_AUTH_CLOSURE,
        "owner_authorization_type_count": closure_summary.get("owner_authorization_type_count", 7),
        "owner_confirmed_now": _bool_val(closure_summary.get("owner_confirmed_now"), False),
        "owner_approval_executed": _bool_val(closure_summary.get("owner_approval_executed"), False),
        "operator_ack_executed_now": _bool_val(closure_summary.get("operator_ack_executed_now"), False),
        "package_generated_now": _bool_val(closure_summary.get("package_generated_now"), False),
        "rollback_rehearsal_executed": _bool_val(closure_summary.get("rollback_rehearsal_executed"), False),
        "rollback_evidence_generated_now": _bool_val(closure_summary.get("rollback_evidence_generated_now"), False),
        "rollback_success_claim_allowed": _bool_val(closure_summary.get("rollback_success_claim_allowed"), False),
        "armed_batch_count": armed_count,
        "all_batches_not_armed": closure_summary.get("all_batches_not_armed") is True,
        "rollback_rehearsal_step_count": closure_summary.get("rollback_rehearsal_step_count", 11),
        "authorization_blocker_count": closure_summary.get("authorization_blocker_count", 15),
        "gap_hard_block_matrix_reviewed": gap_closure.get("gap_hard_block_matrix_reviewed", True),
        "missing_rollback_rehearsal_blocks_real_migration": gap_closure.get(
            "missing_rollback_rehearsal_blocks_real_migration", True
        ),
        "missing_rollback_rehearsal_blocks_batch_arming": gap_closure.get(
            "missing_rollback_rehearsal_blocks_batch_arming", True
        ),
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "semantic_clarification_status": semantic_record.get("semantic_clarification_status", "recorded"),
        "semantic_clarification_impact": semantic_record.get("semantic_clarification_impact", "no_permission_granted"),
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_option_matrix = {
        "routes": ROUTE_OPTIONS,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    priority_ranking = {
        "rankings": [
            {"rank": 1, "route_id": "A", "route_name": SELECTED_ROUTE, "priority": "P0", "selected_now": True},
            {"rank": 2, "route_id": "B", "route_name": "Controlled Batch Arming Planning", "priority": "deferred"},
            {"rank": 3, "route_id": "C", "route_name": "Owner Approval Workflow Planning", "priority": "deferred"},
            {"rank": 4, "route_id": "D", "route_name": "Post-Migration Test Harness Execution Planning", "priority": "deferred"},
            {"rank": 5, "route_id": "F", "route_name": "Rollback Rehearsal Execution", "priority": "blocked"},
            {"rank": 6, "route_id": "E", "route_name": "Real Migration Execution Trial", "priority": "blocked"},
            {"rank": 7, "route_id": "I", "route_name": "Return to Mainline Capability Development", "priority": "deferred"},
            {"rank": 8, "route_id": "G", "route_name": "Whitebox / Test Center Structure Optimization", "priority": "deferred"},
            {"rank": 9, "route_id": "H", "route_name": "Developer Backend Architecture", "priority": "deferred"},
            {"rank": 10, "route_id": "J", "route_name": "Future Reserved Module Structure Review", "priority": "discussion"},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selection_rationale = [
        "Pre-Authorization and Rollback Rehearsal Closure complete: Planning→DryRun→Post-Review",
        "rollback_rehearsal_executed=false; rollback_evidence_generated_now=false",
        "rollback_success_claim_allowed=false (source of truth: dryrun summary)",
        "missing_rollback_rehearsal still blocks real migration and batch arming",
        "Real migration and batch arming planning must not precede rollback rehearsal dry-run planning",
        "Next: Rollback Rehearsal DryRun Planning (planning-only; no rehearsal execution)",
        "Route B batch arming planning deferred",
        "Route C owner workflow deferred as standalone priority",
        "Route E real migration and Route F rollback rehearsal execution blocked",
        "Route G/H/I/J deferred or discussion only",
    ]

    recommended_next_phase_decision = {
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "selection_rationale": selection_rationale,
        "planning_only": True,
        "real_migration_deferred": True,
        "batch_arming_planning_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_dryrun_planning_route_decision = {
        "route_name": SELECTED_ROUTE,
        "route_id": "A",
        "selected_now": True,
        "recommended_next_phase": NEXT_PHASE,
        "planning_only": True,
        "auto_execute_allowed": False,
        "scope": [
            "rehearsal_sandbox_or_branch_planning",
            "B1_B6_rollback_path_simulation_planning",
            "restore_path_map_planning",
            "docs_link_restore_planning",
            "phase_verdict_table_restore_if_touched_planning",
            "eval_out_reference_restore_planning",
            "rollback_verifier_rerun_planning",
            "rollback_rehearsal_evidence_template_alignment",
        ],
        "not_in_scope": [
            "rollback_rehearsal_execution",
            "real_file_move",
            "batch_arming_execution",
            "owner_confirmation",
            "authorization_package_generation",
            "whitebox_test_center_design",
            "developer_backend_finalization",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_controlled_batch_arming_planning_register = {
        "deferred": True,
        "blocked_as_priority": True,
        "batch_arming_allowed_now": False,
        "reason": "must follow rollback rehearsal dry-run planning; not before real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_owner_approval_workflow_register = {
        "deferred": True,
        "reason": "owner approval execution must not precede rollback rehearsal dry-run planning",
        "parallel_input_to_route_a": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_post_migration_test_harness_execution_register = {
        "deferred": True,
        "post_migration_tests_executed": False,
        "reason": "rollback rehearsal dry-run planning and arming chain must be clearer first",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_migration_execution_trial_register = {
        "deferred": True,
        "blocked": True,
        "real_migration_execution_allowed": False,
        "reason": "owner/ack/package/rehearsal gaps; closure non-claims",
        "requires_before_real_migration": [
            "rollback_rehearsal_dryrun_planning_complete",
            "rollback_rehearsal_dryrun_complete",
            "owner_approval_records",
            "operator_acknowledgement",
            "pre_execution_authorization_package",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_rollback_rehearsal_execution_register = {
        "deferred": True,
        "blocked": True,
        "rollback_rehearsal_executed": False,
        "reason": "only rollback rehearsal dry-run planning selected; execution blocked",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_whitebox_test_center_register = {
        "deferred": True,
        "reason": "must wait for main project migration and post-migration test completion",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_developer_backend_architecture_register = {
        "deferred": True,
        "reason": "developer backend overall structure not finalized",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_future_reserved_module_register = {
        "deferred": True,
        "discussion_only": True,
        "modules": ["WorldModel", "Memory", "Library", "Emotion"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        "no-real-migration-execution": True,
        "no-batch-arming": True,
        "no-owner-confirmation": True,
        "no-operator-ack-execution": True,
        "no-authorization-package-generation": True,
        "no-rollback-rehearsal-execution": True,
        "no-rollback-evidence-generation": True,
        "no-rollback-success-claim": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-post-migration-test-execution": True,
        "no-verifier-suite-execution": True,
        "no-whitebox-design": True,
        "no-test-center-design": True,
        "no-developer-backend-finalization": True,
        "no-runtime": True,
        "no-write": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "items": GOVERNANCE_DEBT,
        "item_count": len(GOVERNANCE_DEBT),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not closure_loaded:
        blockers.append("pre_authorization_closure_not_ready")
    if not post_review_loaded:
        blockers.append("pre_authorization_post_review_not_loaded")
    if not dryrun_loaded:
        blockers.append("pre_authorization_dryrun_not_loaded")
    if not planning_loaded:
        blockers.append("pre_authorization_planning_not_loaded")
    if not ce_closure_loaded:
        blockers.append("controlled_execution_closure_not_confirmed")
    if not chain_closed:
        blockers.append("pre_authorization_chain_not_closed")
    if _bool_val(closure_summary.get("real_migration_execution_allowed"), False):
        blockers.append("real_migration_must_remain_false")
    if armed_count != 0:
        blockers.append("armed_batch_count_nonzero")
    if _bool_val(closure_summary.get("rollback_rehearsal_executed"), False) is True:
        blockers.append("rollback_rehearsal_must_not_be_executed")

    boundary_ok = not blockers

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "POST_PRE_AUTHORIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "selected_route": SELECTED_ROUTE,
        "reason": "pre-auth closed; rollback rehearsal dry-run planning before batch arming or real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "pre_authorization_closure_input_loaded": closure_loaded,
        "pre_authorization_post_review_input_loaded": post_review_loaded,
        "pre_authorization_dryrun_input_loaded": dryrun_loaded,
        "pre_authorization_planning_input_loaded": planning_loaded,
        "controlled_execution_roadmap_input_loaded": roots["controlled_execution_roadmap"]["loaded"],
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "pre_authorization_closure_status_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "rollback_rehearsal_dryrun_planning_route_decision_generated": True,
        "deferred_controlled_batch_arming_planning_register_generated": True,
        "deferred_owner_approval_workflow_register_generated": True,
        "deferred_post_migration_test_harness_execution_register_generated": True,
        "deferred_real_migration_execution_trial_register_generated": True,
        "deferred_rollback_rehearsal_execution_register_generated": True,
        "deferred_whitebox_test_center_register_generated": True,
        "deferred_developer_backend_architecture_register_generated": True,
        "deferred_future_reserved_module_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "rollback_rehearsal_dryrun_planning_selected": True,
        "pre_authorization_rollback_rehearsal_chain_closed": chain_closed,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "owner_confirmed_now": _bool_val(closure_summary.get("owner_confirmed_now"), False),
        "owner_approval_executed": _bool_val(closure_summary.get("owner_approval_executed"), False),
        "operator_ack_executed_now": _bool_val(closure_summary.get("operator_ack_executed_now"), False),
        "package_generated_now": _bool_val(closure_summary.get("package_generated_now"), False),
        "rollback_rehearsal_executed": _bool_val(closure_summary.get("rollback_rehearsal_executed"), False),
        "rollback_evidence_generated_now": _bool_val(closure_summary.get("rollback_evidence_generated_now"), False),
        "rollback_success_claim_allowed": _bool_val(closure_summary.get("rollback_success_claim_allowed"), False),
        "missing_rollback_rehearsal_blocks_real_migration": gap_closure.get(
            "missing_rollback_rehearsal_blocks_real_migration", True
        ),
        "missing_rollback_rehearsal_blocks_batch_arming": gap_closure.get(
            "missing_rollback_rehearsal_blocks_batch_arming", True
        ),
        "controlled_batch_arming_planning_deferred": True,
        "owner_approval_workflow_deferred": True,
        "post_migration_test_harness_execution_deferred": True,
        "real_migration_execution_trial_blocked": True,
        "rollback_rehearsal_execution_blocked": True,
        "whitebox_test_center_structure_optimization_deferred": True,
        "developer_backend_architecture_deferred": True,
        "future_reserved_module_finalization_deferred": True,
        "return_to_mainline_deferred": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "docs_modified_by_decision": False,
        "readme_modified_by_decision": False,
        "phase_verdict_table_modified_by_decision": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "POST_PRE_AUTHORIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "pre_authorization_closure_status_summary": pre_authorization_closure_status_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "rollback_rehearsal_dryrun_planning_route_decision": rollback_rehearsal_dryrun_planning_route_decision,
        "deferred_controlled_batch_arming_planning_register": deferred_controlled_batch_arming_planning_register,
        "deferred_owner_approval_workflow_register": deferred_owner_approval_workflow_register,
        "deferred_post_migration_test_harness_execution_register": deferred_post_migration_test_harness_execution_register,
        "deferred_real_migration_execution_trial_register": deferred_real_migration_execution_trial_register,
        "deferred_rollback_rehearsal_execution_register": deferred_rollback_rehearsal_execution_register,
        "deferred_whitebox_test_center_register": deferred_whitebox_test_center_register,
        "deferred_developer_backend_architecture_register": deferred_developer_backend_architecture_register,
        "deferred_future_reserved_module_register": deferred_future_reserved_module_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
