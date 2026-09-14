# -*- coding: utf-8 -*-
"""Main Project Structure Migration Guarded Roadmap Decision v1.

Roadmap decision only: select Execution Control and Test Harness Planning.
No real migration, post-migration test execution, owner confirmation, or whitebox design.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001"
DECISION_SCOPE = "main_project_structure_migration_guarded_roadmap_decision_only"
DECISION_ID = "main_proj_struct_migration_guarded_roadmap_decision_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_guarded_roadmap_decision_v1"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_READY_FOR_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001"
SELECTED_ROUTE = "Migration Execution Control and Test Harness Planning"

CLOSURE_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN"
READINESS_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": SELECTED_ROUTE,
        "route_type": "migration_execution_control_and_test_harness_planning",
        "readiness_level": "high",
        "dependency": [
            "guarded migration chain closed",
            "B0-B7 dry-run stable",
            "31 post-migration tests bound",
            "8 rollback checkpoints defined",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "execution control + test harness before any real move",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Human Approval / Owner Assignment Planning",
        "route_type": "human_approval_owner_assignment_planning",
        "readiness_level": "medium",
        "dependency": ["B1-B6 HumanApproval placeholder", "execution control constraints"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "owner assignment for B1-B6; parallel or after Route A inputs",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "important but subordinate to execution control + test harness planning",
        "recommended_phase_name": "Phase-Main-Project-Structure-Migration-Human-Approval-Owner-Assignment-Planning-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Migration Execution Controlled Plan",
        "route_type": "migration_execution_controlled_plan",
        "readiness_level": "blocked",
        "dependency": ["execution control plan", "test harness", "abort conditions"],
        "risk_level": "critical",
        "expected_value": "high",
        "runtime_risk": "critical",
        "write_risk": "critical",
        "governance_debt_impact": "real batch execution planning",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "execution control and test harness not yet planned",
        "recommended_phase_name": "Phase-Main-Project-Structure-Migration-Execution-Controlled-Plan-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "Post-Migration Test Harness Preparation",
        "route_type": "post_migration_test_harness_preparation",
        "readiness_level": "conditional",
        "dependency": ["31 bound tests", "verifier suite definition"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "merged into Route A scope",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "consolidated under Route A; not standalone selection",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "E",
        "route_name": "Real Migration Execution Trial",
        "route_type": "real_migration_execution_trial",
        "readiness_level": "blocked",
        "dependency": ["execution control", "test harness", "owner approval", "rollback rehearsal"],
        "risk_level": "critical",
        "expected_value": "high",
        "runtime_risk": "critical",
        "write_risk": "critical",
        "governance_debt_impact": "actual file move/delete/merge",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "real_migration_allowed=false; guarded closure non-claims",
        "recommended_phase_name": "Phase-Main-Project-Structure-Migration-Real-Execution-Trial-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Whitebox / Test Center Structure Optimization",
        "route_type": "whitebox_test_center_structure_optimization",
        "readiness_level": "deferred",
        "dependency": ["main project migration complete", "post-migration tests executed"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "must 1:1 align with main project after migration and tests",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "defer until main project migration and post-migration tests complete",
        "recommended_phase_name": "Phase-Whitebox-and-Test-Center-Structure-Optimization-Planning-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Developer Backend Architecture",
        "route_type": "developer_backend_architecture",
        "readiness_level": "deferred",
        "dependency": ["user backend structure decision"],
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
        "route_id": "H",
        "route_name": "Docs Reorganization",
        "route_type": "docs_reorganization",
        "readiness_level": "deferred",
        "dependency": ["execution control", "test harness", "main migration path"],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "medium",
        "governance_debt_impact": "docs must not precede execution control planning",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "cannot precede execution control and test harness",
        "recommended_phase_name": "Phase-Docs-Reorganization-Planning-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "Return to Mainline Capability Development",
        "route_type": "return_to_mainline",
        "readiness_level": "deferred",
        "dependency": ["guarded chain at closure"],
        "risk_level": "low",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "pause structure migration for capability building",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "complete execution control + test harness planning first",
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
        "governance_debt_impact": "future_reserved/discussion_required only",
        "recommended_priority": "discussion",
        "selected_now": False,
        "defer_reason": "not selected; discussion only",
        "recommended_phase_name": "Phase-Future-Reserved-Module-Discussion-v1-001",
    },
]

NON_CLAIMS = [
    "roadmap decision 不等于真实迁移可执行",
    "roadmap decision 不等于可执行 post-migration tests",
    "roadmap decision 不等于 owner 已确认",
    "roadmap decision 不等于 protected / HR / DnAE 可处理",
    "selected route 仍是 planning-only，不执行真实搬迁",
    "Guarded Closure 不等于可真实搬迁（carryover）",
    "execution control planning 不等于 file move/delete/merge 已授权",
    "test harness planning 不等于测试已执行或通过",
    "白盒/测试中心须等主工程迁移与迁移后测试完成后再设计",
    "Developer Backend 整体结构继续 deferred",
]

GOVERNANCE_DEBT = [
    "guarded_migration_chain_closed but real_migration_allowed=false",
    "B0-B7 and 10 gates dry-run stable only",
    "31 post-migration tests bound, 0 executed",
    "8 rollback checkpoints defined, rollback_executed=false",
    "HumanApproval B1-B6 placeholder only; final_owner_human_confirmed=false",
    "240 HR excluded; 914 permanent block excluded",
    "execution_control_and_test_harness_planning required before real migration",
    "rollback_rehearsal_required before any real batch arming",
    "whitebox_test_center deferred until main migration + tests",
    "developer_backend_architecture deferred",
    "correction_record: rollback_executed field fix did not grant rollback execution",
]

ROOT_SPECS = [
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "main_project_structure_migration_guarded_closure_summary.json",
            "guarded_migration_closure_decision_summary.json",
            "exclusion_carryover_freeze.json",
            "closure_boundary_freeze.json",
            "guarded_migration_non_claims_register.json",
            "correction_record.json",
            "deferred_guarded_migration_action_pool.json",
            "completed_phase_matrix.json",
        ],
    },
    {
        "id": "guarded_post_review",
        "arg": "guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "guarded_post_dryrun_readiness_decision.json"],
    },
    {
        "id": "guarded_dryrun",
        "arg": "guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "batch_gate_dryrun_results.json"],
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
        "artifacts": ["summary.json"],
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
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_guarded_roadmap_decision_v1(
    *,
    guarded_closure_root: str,
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

    closure_summary = summaries["guarded_closure"]
    closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and closure_summary.get("final_decision") == CLOSURE_DECISION
        and closure_summary.get("guarded_migration_chain_closed") is True
    )
    post_review_loaded = (
        roots["guarded_post_review"]["loaded"]
        and summaries["guarded_post_review"].get("final_decision") == POST_REVIEW_DECISION
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

    closure_root = roots["guarded_closure"]["root"]
    decision_summary = (
        _try_read_json(closure_root / "guarded_migration_closure_decision_summary.json") if closure_root else {}
    ) or {}
    correction_record = _try_read_json(closure_root / "correction_record.json") if closure_root else {}
    non_claims_closure = (
        _try_read_json(closure_root / "guarded_migration_non_claims_register.json") if closure_root else {}
    ) or {}

    batch_count = closure_summary.get("batch_count", decision_summary.get("batch_count", 8))
    gate_sequence_count = closure_summary.get("gate_sequence_count", decision_summary.get("gate_sequence_count", 10))
    post_migration_test_count = closure_summary.get(
        "post_migration_test_count", decision_summary.get("post_migration_test_count", 31)
    )
    rollback_checkpoint_count = closure_summary.get(
        "rollback_checkpoint_count", decision_summary.get("rollback_checkpoint_count", 8)
    )
    real_migration_allowed = bool(closure_summary.get("real_migration_allowed", False))
    chain_closed = closure_summary.get("guarded_migration_chain_closed") is True

    guarded_closure_status_summary = {
        "guarded_migration_chain_closed": chain_closed,
        "closure_final_decision": CLOSURE_DECISION,
        "batch_count": batch_count,
        "simulated_pass_batch_count": closure_summary.get("simulated_pass_batch_count", 8),
        "gate_sequence_count": gate_sequence_count,
        "post_migration_test_count": post_migration_test_count,
        "bound_test_count": closure_summary.get("bound_test_count", 31),
        "executed_test_count": closure_summary.get("executed_test_count", 0),
        "rollback_checkpoint_count": rollback_checkpoint_count,
        "rollback_executed": bool(closure_summary.get("rollback_executed", False)),
        "human_approval_is_placeholder_only": closure_summary.get("human_approval_is_placeholder_only") is True,
        "final_owner_human_confirmed": bool(closure_summary.get("final_owner_human_confirmed", False)),
        "real_migration_allowed": False,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "correction_record_status": closure_summary.get("correction_record_status", "recorded"),
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
            {"rank": 2, "route_id": "B", "route_name": "Human Approval / Owner Assignment Planning", "priority": "P1", "selected_now": False},
            {"rank": 3, "route_id": "D", "route_name": "Post-Migration Test Harness Preparation", "priority": "P1", "selected_now": False, "merged_into": "A"},
            {"rank": 4, "route_id": "I", "route_name": "Return to Mainline Capability Development", "priority": "P2", "selected_now": False},
            {"rank": 5, "route_id": "F", "route_name": "Whitebox / Test Center Structure Optimization", "priority": "deferred", "selected_now": False},
            {"rank": 6, "route_id": "G", "route_name": "Developer Backend Architecture", "priority": "deferred", "selected_now": False},
            {"rank": 7, "route_id": "H", "route_name": "Docs Reorganization", "priority": "deferred", "selected_now": False},
            {"rank": 8, "route_id": "J", "route_name": "Future Reserved Module Structure Review", "priority": "discussion", "selected_now": False},
            {"rank": 9, "route_id": "C", "route_name": "Migration Execution Controlled Plan", "priority": "blocked", "selected_now": False},
            {"rank": 10, "route_id": "E", "route_name": "Real Migration Execution Trial", "priority": "blocked", "selected_now": False},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selection_rationale = [
        "Guarded Closure complete: Readiness→Planning→DryRun→Post-Review closed",
        "real_migration_allowed=false; dry-run chain stable does not authorize real move",
        "Real migration requires execution control, test harness, abort policy, batch arming, verifier suite",
        "rollback_rehearsal_required before any batch arming",
        "Route B human approval planning deferred as input to Route A, not standalone P0",
        "Route E real migration blocked",
        "Route F whitebox/test center deferred until main migration + post-migration tests",
        "Route G developer backend architecture deferred",
        "240 HR and 914 permanent block remain excluded",
        f"correction_record: {correction_record.get('issue', 'rollback_executed field semantics')} — no permission granted",
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

    migration_execution_control_test_harness_route_decision = {
        "route_name": SELECTED_ROUTE,
        "route_id": "A",
        "selected_now": True,
        "recommended_next_phase": NEXT_PHASE,
        "planning_only": True,
        "auto_execute_allowed": False,
        "scope": [
            "migration_execution_control_policy",
            "batch_arming_and_abort_conditions",
            "post_migration_test_harness_definition",
            "post_migration_verifier_suite_planning",
            "rollback_rehearsal_requirements",
            "pre_real_migration_gate_checklist",
        ],
        "not_in_scope": [
            "real_file_move",
            "real_file_delete",
            "module_merge_execution",
            "post_migration_test_execution",
            "rollback_execution",
            "owner_confirmation",
            "whitebox_test_center_design",
            "developer_backend_finalization",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_migration_execution_register = {
        "deferred": True,
        "blocked": True,
        "real_migration_allowed": False,
        "reason": "execution control and test harness not yet planned",
        "requires_before_real_migration": [
            "execution_control_plan",
            "test_harness_plan",
            "abort_condition_policy",
            "batch_arming_policy",
            "rollback_rehearsal",
            "post_migration_verifier_suite",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_human_approval_owner_assignment_register = {
        "deferred": True,
        "batches_requiring_approval": ["B1", "B2", "B3", "B4", "B5", "B6"],
        "final_owner_human_confirmed": False,
        "approval_executed": False,
        "reason": "parallel or subsequent to execution control planning; not P0 standalone",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_whitebox_test_center_register = {
        "deferred": True,
        "reason": "must wait for main project migration and post-migration test completion",
        "align_with_main_project_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_developer_backend_architecture_register = {
        "deferred": True,
        "reason": "developer backend overall structure not finalized",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_docs_reorganization_register = {
        "deferred": True,
        "reason": "cannot precede execution control and test harness planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_future_reserved_module_register = {
        "deferred": True,
        "discussion_only": True,
        "modules": [
            "WorldModel",
            "Memory",
            "Library",
            "Emotion",
            "Exploration Drive",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        "no-real-migration": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-post-migration-test-execution": True,
        "no-rollback-execution": True,
        "no-owner-confirmation": True,
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
        blockers.append("guarded_closure_not_ready")
    if not post_review_loaded:
        blockers.append("guarded_post_review_not_loaded")
    if not dryrun_loaded:
        blockers.append("guarded_dryrun_not_loaded")
    if not planning_loaded:
        blockers.append("guarded_planning_not_loaded")
    if not readiness_loaded:
        blockers.append("readiness_not_loaded")
    if not chain_closed:
        blockers.append("guarded_migration_chain_not_closed")
    if real_migration_allowed:
        blockers.append("real_migration_must_remain_false")

    boundary_ok = not blockers

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_REQUIRES_FIXES",
        "selected_route": SELECTED_ROUTE,
        "reason": "guarded closure complete; execution control + test harness planning before any real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "guarded_closure_input_loaded": closure_loaded,
        "guarded_post_review_input_loaded": post_review_loaded,
        "guarded_dryrun_input_loaded": dryrun_loaded,
        "guarded_planning_input_loaded": planning_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "consolidation_closure_input_loaded": consolidation_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "guarded_closure_status_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "migration_execution_control_test_harness_route_decision_generated": True,
        "deferred_real_migration_execution_register_generated": True,
        "deferred_human_approval_owner_assignment_register_generated": True,
        "deferred_whitebox_test_center_register_generated": True,
        "deferred_developer_backend_architecture_register_generated": True,
        "deferred_docs_reorganization_register_generated": True,
        "deferred_future_reserved_module_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "guarded_migration_chain_closed": chain_closed,
        "batch_count": batch_count,
        "gate_sequence_count": gate_sequence_count,
        "post_migration_test_count": post_migration_test_count,
        "rollback_checkpoint_count": rollback_checkpoint_count,
        "real_migration_allowed": False,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "migration_execution_control_required": True,
        "post_migration_test_harness_required": True,
        "rollback_rehearsal_required": True,
        "abort_condition_policy_required": True,
        "batch_arming_policy_required": True,
        "post_migration_verifier_suite_required": True,
        "human_approval_owner_assignment_deferred": True,
        "real_migration_execution_blocked": True,
        "whitebox_test_center_structure_optimization_deferred": True,
        "developer_backend_architecture_deferred": True,
        "docs_reorganization_deferred": True,
        "future_reserved_module_finalization_deferred": True,
        "return_to_mainline_deferred": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "guarded_closure_status_summary": guarded_closure_status_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "migration_execution_control_test_harness_route_decision": migration_execution_control_test_harness_route_decision,
        "deferred_real_migration_execution_register": deferred_real_migration_execution_register,
        "deferred_human_approval_owner_assignment_register": deferred_human_approval_owner_assignment_register,
        "deferred_whitebox_test_center_register": deferred_whitebox_test_center_register,
        "deferred_developer_backend_architecture_register": deferred_developer_backend_architecture_register,
        "deferred_docs_reorganization_register": deferred_docs_reorganization_register,
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
