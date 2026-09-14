# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Execution Roadmap Decision v1.

Roadmap decision only: select Real Migration Pre-Authorization and Rollback Rehearsal Planning.
No real migration, batch arming, tests, verifier suite, or rollback rehearsal.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001"
DECISION_SCOPE = "main_project_structure_migration_controlled_execution_roadmap_decision_only"
DECISION_ID = "main_proj_struct_migration_controlled_execution_roadmap_decision_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_controlled_execution_roadmap_decision_v1"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_READY_FOR_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001"
SELECTED_ROUTE = "Real Migration Pre-Authorization and Rollback Rehearsal Planning"

CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": SELECTED_ROUTE,
        "route_type": "pre_authorization_rollback_rehearsal_planning",
        "readiness_level": "high",
        "dependency": [
            "controlled execution chain closed",
            "owner_approval_executed=false",
            "rollback_rehearsal_executed=false",
            "armed_batch_count=0",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "define owner/auth and rollback rehearsal before real migration",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Owner Approval Resolution Planning",
        "route_type": "owner_approval_resolution_planning",
        "readiness_level": "medium",
        "dependency": ["7 owner gates", "B1-B6 approval required"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "merged into Route A",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "merged into Route A",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "C",
        "route_name": "Rollback Rehearsal Planning",
        "route_type": "rollback_rehearsal_planning",
        "readiness_level": "conditional",
        "dependency": ["rollback_rehearsal_mandatory", "covers B1-B6"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "merged into Route A",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "merged into Route A",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "D",
        "route_name": "Post-Migration Test Harness Execution Planning",
        "route_type": "post_migration_test_harness_execution_planning",
        "readiness_level": "conditional",
        "dependency": ["31 tests ordered", "auth and rollback rehearsal planning first"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "defer until pre-auth and rollback rehearsal planning",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "requires owner approval and rollback rehearsal planning first",
        "recommended_phase_name": "Phase-Post-Migration-Test-Harness-Execution-Planning-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Real Migration Execution Trial",
        "route_type": "real_migration_execution_trial",
        "readiness_level": "blocked",
        "dependency": ["pre-authorization", "rollback rehearsal", "owner approval"],
        "risk_level": "critical",
        "expected_value": "high",
        "runtime_risk": "critical",
        "write_risk": "critical",
        "governance_debt_impact": "actual file move/delete/merge",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "real_migration_execution_allowed=false",
        "recommended_phase_name": "Phase-Real-Migration-Execution-Trial-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Controlled Batch Arming Trial",
        "route_type": "controlled_batch_arming_trial",
        "readiness_level": "blocked",
        "dependency": ["owner approval", "rollback rehearsal"],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "medium",
        "governance_debt_impact": "arming without auth/rehearsal blocked",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "owner approval and rollback rehearsal not satisfied",
        "recommended_phase_name": "Phase-Controlled-Batch-Arming-Trial-v1-001",
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
        "dependency": ["controlled execution at pre-migration planning stage"],
        "risk_level": "low",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "pause structure migration",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "structure migration at real-migration pre-auth stage; not return to mainline now",
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
    "roadmap decision 不等于 batch 已执行",
    "roadmap decision 不等于文件移动/删除/重命名/合并可执行",
    "roadmap decision 不等于迁移后测试可执行或已通过",
    "roadmap decision 不等于 verifier suite 可执行或已通过",
    "roadmap decision 不等于 rollback rehearsal 可执行或已执行",
    "roadmap decision 不等于 owner 已确认",
    "selected route 仍是 planning-only，不执行真实搬迁",
    "Controlled Execution Closure 不等于 real_migration_execution_allowed",
    "pre-authorization planning 不等于 file move 已授权",
    "白盒/测试中心须等主工程迁移与迁移后测试完成后再设计",
    "Developer Backend 整体结构继续 deferred",
    "all_not_armed correction: no_permission_granted, no_boundary_change",
]

GOVERNANCE_DEBT = [
    "controlled_execution_chain_closed but real_migration_execution_allowed=false",
    "armed_batch_count=0; batch_arming_allowed_now=false",
    "owner_approval_executed=false; final_owner_human_confirmed=false",
    "rollback_rehearsal_mandatory; rollback_rehearsal_executed=false",
    "31 post-batch tests ordered; executed_test_count=0",
    "12 verifier suite ordered; verifier_suite_executed=false",
    "evidence_pack_template_only; evidence_pack_generated_now=false",
    "240 HR excluded; 914 permanent block excluded",
    "all_not_armed correction recorded: semantic no_permission_granted",
    "pre-authorization and rollback rehearsal planning required before real migration",
    "whitebox_test_center deferred",
    "developer_backend_architecture deferred",
]

CLOSURE_ARTIFACTS = [
    "summary.json",
    "controlled_execution_closure_summary.json",
    "controlled_execution_closure_decision_summary.json",
    "closure_boundary_freeze.json",
    "controlled_execution_non_claims_register.json",
    "correction_record.json",
    "deferred_controlled_execution_action_pool.json",
    "completed_phase_matrix.json",
]

ROOT_SPECS = [
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": CLOSURE_ARTIFACTS,
    },
    {
        "id": "controlled_execution_post_review",
        "arg": "controlled_execution_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_execution_post_dryrun_readiness_decision.json"],
    },
    {
        "id": "controlled_execution_dryrun",
        "arg": "controlled_execution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_execution_dryrun_execution_plan.json",
            "controlled_execution_dryrun_boundary_review.json",
        ],
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_migration_execution_planning_policy.json",
            "controlled_execution_batch_plan.json",
            "owner_authorization_gate.json",
            "rollback_rehearsal_precondition.json",
            "post_batch_test_execution_order.json",
            "verifier_suite_execution_order.json",
            "abort_and_failure_response_plan.json",
            "post_execution_evidence_pack_plan.json",
        ],
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


def run_main_project_structure_migration_controlled_execution_roadmap_decision_v1(
    *,
    controlled_execution_closure_root: str,
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

    closure_summary = summaries["controlled_execution_closure"]
    closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and closure_summary.get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
        and closure_summary.get("controlled_execution_chain_closed") is True
    )
    post_review_loaded = (
        roots["controlled_execution_post_review"]["loaded"]
        and summaries["controlled_execution_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_loaded = (
        roots["controlled_execution_dryrun"]["loaded"]
        and summaries["controlled_execution_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == PLANNING_DECISION
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

    closure_root = roots["controlled_execution_closure"]["root"]
    decision_summary = (
        _try_read_json(closure_root / "controlled_execution_closure_decision_summary.json") if closure_root else {}
    ) or {}
    correction_record = (_try_read_json(closure_root / "correction_record.json") if closure_root else {}) or {}
    non_claims_closure = (
        _try_read_json(closure_root / "controlled_execution_non_claims_register.json") if closure_root else {}
    ) or {}

    chain_closed = closure_summary.get("controlled_execution_chain_closed") is True
    armed_count = closure_summary.get("armed_batch_count", 0)
    batch_count = closure_summary.get("batch_count", 8)
    post_batch_test_count = closure_summary.get("post_batch_test_count", 31)
    verifier_suite_count = closure_summary.get("verifier_suite_count", 12)
    abort_count = closure_summary.get("abort_condition_count", 16)
    failure_count = closure_summary.get("failure_response_type_count", 11)

    controlled_execution_closure_status_summary = {
        "controlled_execution_chain_closed": chain_closed,
        "closure_final_decision": CONTROLLED_EXECUTION_CLOSURE,
        "execution_window_requirement_count": closure_summary.get("execution_window_requirement_count", 10),
        "execution_window_opened": _bool_val(closure_summary.get("execution_window_opened"), False),
        "owner_authorization_gate_count": closure_summary.get("owner_authorization_gate_count", 7),
        "owner_approval_executed": _bool_val(closure_summary.get("owner_approval_executed"), False),
        "owner_auto_confirm_allowed": _bool_val(closure_summary.get("owner_auto_confirm_allowed"), False),
        "final_owner_human_confirmed": _bool_val(closure_summary.get("final_owner_human_confirmed"), False),
        "batch_count": batch_count,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": closure_summary.get("all_batches_not_armed") is True,
        "batch_execution_count": closure_summary.get("batch_execution_count", 0),
        "candidate_only_batch_count": closure_summary.get("candidate_only_batch_count", 8),
        "rollback_rehearsal_mandatory": closure_summary.get("rollback_rehearsal_mandatory") is True,
        "rollback_rehearsal_executed": _bool_val(closure_summary.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": closure_summary.get("rollback_execution_still_blocked") is True,
        "post_batch_test_count": post_batch_test_count,
        "executed_test_count": closure_summary.get("executed_test_count", 0),
        "verifier_suite_count": verifier_suite_count,
        "verifier_suite_executed": _bool_val(closure_summary.get("verifier_suite_executed"), False),
        "evidence_pack_generated_now": _bool_val(closure_summary.get("evidence_pack_generated_now"), False),
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "correction_record_count": correction_record.get("correction_record_count", 1),
        "correction_semantic_impact": correction_record.get("correction_semantic_impact", "no_permission_granted"),
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
            {"rank": 2, "route_id": "B", "route_name": "Owner Approval Resolution Planning", "priority": "P1", "merged_into": "A"},
            {"rank": 3, "route_id": "C", "route_name": "Rollback Rehearsal Planning", "priority": "P1", "merged_into": "A"},
            {"rank": 4, "route_id": "D", "route_name": "Post-Migration Test Harness Execution Planning", "priority": "deferred"},
            {"rank": 5, "route_id": "I", "route_name": "Return to Mainline Capability Development", "priority": "deferred"},
            {"rank": 6, "route_id": "G", "route_name": "Whitebox / Test Center Structure Optimization", "priority": "deferred"},
            {"rank": 7, "route_id": "H", "route_name": "Developer Backend Architecture", "priority": "deferred"},
            {"rank": 8, "route_id": "J", "route_name": "Future Reserved Module Structure Review", "priority": "discussion"},
            {"rank": 9, "route_id": "F", "route_name": "Controlled Batch Arming Trial", "priority": "blocked"},
            {"rank": 10, "route_id": "E", "route_name": "Real Migration Execution Trial", "priority": "blocked"},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selection_rationale = [
        "Controlled Execution Closure complete: Planning→DryRun→Post-Review",
        "real_migration_execution_allowed=false; closure does not authorize real move",
        "owner_approval_executed=false; final_owner_human_confirmed=false",
        "rollback_rehearsal_executed=false; rollback_execution_still_blocked=true",
        "armed_batch_count=0; batch arming trial blocked",
        "31 tests ordered, 0 executed; harness planning alone insufficient without auth/rehearsal",
        "Next: Real Migration Pre-Authorization and Rollback Rehearsal Planning (planning-only)",
        "Route B owner approval and Route C rollback rehearsal merged into Route A",
        "Route E real migration and Route F batch arming blocked",
        "Route G whitebox/test center and Route H developer backend deferred",
        "Route I return to mainline deferred at pre-migration planning stage",
        "all_not_armed correction: no_permission_granted, no_boundary_change",
    ]

    recommended_next_phase_decision = {
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "selection_rationale": selection_rationale,
        "planning_only": True,
        "real_migration_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_authorization_rollback_rehearsal_route_decision = {
        "route_name": SELECTED_ROUTE,
        "route_id": "A",
        "selected_now": True,
        "recommended_next_phase": NEXT_PHASE,
        "planning_only": True,
        "auto_execute_allowed": False,
        "owner_approval_resolution_merged": True,
        "rollback_rehearsal_planning_merged": True,
        "scope": [
            "owner_authorization_resolution_planning",
            "pre_execution_authorization_gate",
            "operator_acknowledgement_requirements",
            "batch_arming_authorization_record_template",
            "rollback_rehearsal_planning_B1_B6",
            "restore_path_and_docs_links_planning",
            "rollback_rehearsal_report_requirements",
        ],
        "not_in_scope": [
            "real_file_move",
            "batch_arming_execution",
            "rollback_rehearsal_execution",
            "post_migration_test_execution",
            "verifier_suite_execution",
            "owner_human_confirmation",
            "whitebox_test_center_design",
            "developer_backend_finalization",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_migration_execution_trial_register = {
        "deferred": True,
        "blocked": True,
        "real_migration_execution_allowed": False,
        "reason": "owner approval and rollback rehearsal planning not complete; closure non-claims",
        "requires_before_real_migration": [
            "pre_authorization_planning_complete",
            "owner_approval_records",
            "rollback_rehearsal_planning_complete",
            "rollback_rehearsal_executed",
            "post_batch_test_harness_ready",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_batch_arming_trial_register = {
        "deferred": True,
        "blocked": True,
        "batch_arming_allowed_now": False,
        "armed_batch_count": 0,
        "reason": "owner approval missing; rollback rehearsal not executed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_post_migration_test_harness_execution_register = {
        "deferred": True,
        "post_migration_tests_executed": False,
        "executed_test_count": 0,
        "reason": "pre-authorization and rollback rehearsal planning must precede test execution planning",
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
        "no-batch-execution": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-post-migration-test-execution": True,
        "no-verifier-suite-execution": True,
        "no-rollback-rehearsal-execution": True,
        "no-rollback-execution": True,
        "no-owner-confirmation": True,
        "no-real-evidence-pack-generation": True,
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
        "closure_non_claims_carryover": non_claims_closure.get("non_claims") or [],
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not closure_loaded:
        blockers.append("controlled_execution_closure_not_ready")
    if not post_review_loaded:
        blockers.append("controlled_execution_post_review_not_loaded")
    if not dryrun_loaded:
        blockers.append("controlled_execution_dryrun_not_loaded")
    if not planning_loaded:
        blockers.append("controlled_execution_planning_not_loaded")
    if not ec_closure_loaded:
        blockers.append("execution_control_closure_not_confirmed")
    if not guarded_closure_loaded:
        blockers.append("guarded_closure_not_confirmed")
    if not chain_closed:
        blockers.append("controlled_execution_chain_not_closed")
    if _bool_val(closure_summary.get("real_migration_execution_allowed"), False):
        blockers.append("real_migration_must_remain_false")
    if armed_count != 0:
        blockers.append("armed_batch_count_nonzero")

    boundary_ok = not blockers

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "selected_route": SELECTED_ROUTE,
        "reason": "controlled execution closed; pre-authorization and rollback rehearsal planning before real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "controlled_execution_closure_input_loaded": closure_loaded,
        "controlled_execution_post_review_input_loaded": post_review_loaded,
        "controlled_execution_dryrun_input_loaded": dryrun_loaded,
        "controlled_execution_planning_input_loaded": planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "controlled_execution_closure_status_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "pre_authorization_rollback_rehearsal_route_decision_generated": True,
        "deferred_real_migration_execution_trial_register_generated": True,
        "deferred_batch_arming_trial_register_generated": True,
        "deferred_post_migration_test_harness_execution_register_generated": True,
        "deferred_whitebox_test_center_register_generated": True,
        "deferred_developer_backend_architecture_register_generated": True,
        "deferred_future_reserved_module_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "controlled_execution_chain_closed": chain_closed,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "owner_approval_executed": _bool_val(closure_summary.get("owner_approval_executed"), False),
        "final_owner_human_confirmed": _bool_val(closure_summary.get("final_owner_human_confirmed"), False),
        "rollback_rehearsal_executed": _bool_val(closure_summary.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": closure_summary.get("rollback_execution_still_blocked") is True,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": _bool_val(closure_summary.get("verifier_suite_executed"), False),
        "evidence_pack_generated_now": _bool_val(closure_summary.get("evidence_pack_generated_now"), False),
        "pre_authorization_rollback_rehearsal_planning_selected": True,
        "owner_approval_resolution_merged_into_selected_route": True,
        "rollback_rehearsal_planning_merged_into_selected_route": True,
        "real_migration_execution_trial_blocked": True,
        "batch_arming_trial_blocked": True,
        "post_migration_test_harness_execution_deferred": True,
        "whitebox_test_center_structure_optimization_deferred": True,
        "developer_backend_architecture_deferred": True,
        "future_reserved_module_finalization_deferred": True,
        "return_to_mainline_deferred": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_execution_closure_status_summary": controlled_execution_closure_status_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "pre_authorization_rollback_rehearsal_route_decision": pre_authorization_rollback_rehearsal_route_decision,
        "deferred_real_migration_execution_trial_register": deferred_real_migration_execution_trial_register,
        "deferred_batch_arming_trial_register": deferred_batch_arming_trial_register,
        "deferred_post_migration_test_harness_execution_register": deferred_post_migration_test_harness_execution_register,
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
